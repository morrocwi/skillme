"""Regression coverage for doc_ecosystem_bridge/bridge.py.

Covers bugs found and fixed by a prior ultracode scenario-testing scan
(PRs #11 and #12): directory/symlink handling in attach_communication(),
atomic writes, idempotent README linking, Markdown-cell escaping in
seed_docs()/_escape_cell(), and checkpoint validation refusal.

Follows the convention in test_kernel_self_test.py: sys.path.insert the
target module's directory, import it directly, call real functions
against pytest's tmp_path fixture — no mocking.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "doc_ecosystem_bridge"))
import bridge  # noqa: E402

DOC_ECO_REPO = REPO_ROOT.parent / "human-ai-doc-ecosystem"
INIT_MJS = DOC_ECO_REPO / "plugins/doc-ecosystem/skills/doc-ecosystem/tools/init.mjs"

needs_doc_eco = pytest.mark.skipif(
    shutil.which("node") is None or not INIT_MJS.exists(),
    reason="requires node + sibling human-ai-doc-ecosystem repo with init.mjs",
)


# ---------------------------------------------------------------------------
# attach_communication()
# ---------------------------------------------------------------------------


def test_attach_communication_skips_directory_at_artifact_path(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    # skill_plan.md exists as a directory, not a file
    (source / "skill_plan.md").mkdir()
    target = tmp_path / "target"
    target.mkdir()

    result = bridge.attach_communication(source, target)

    assert result["attached"] == []
    assert len(result["skipped"]) == 1
    name, reason = result["skipped"][0]
    assert name == "skill_plan.md"
    # Exact match on the dedicated is_file() guard's message, not a loose
    # substring check — a loose "directory" substring also matches the
    # incidental OSError text the surrounding read_text()/except OSError
    # handler would produce if the dedicated guard were ever removed, which
    # would let this test keep passing against code that no longer has it
    # (an independent review caught this exact gap during PR verification).
    assert reason == "exists but is not a regular file (e.g. a directory)"


def test_attach_communication_skips_symlink_and_does_not_follow_it(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    outside_secret = tmp_path / "outside_secret.md"
    outside_secret.write_text("SECRET CONTENT OUTSIDE SOURCE_DIR", encoding="utf-8")
    (source / "glossary.md").symlink_to(outside_secret)
    target = tmp_path / "target"
    target.mkdir()

    result = bridge.attach_communication(source, target)

    assert result["attached"] == []
    assert len(result["skipped"]) == 1
    name, reason = result["skipped"][0]
    assert name == "glossary.md"
    assert "symlink" in reason.lower()
    # must NOT have been copied into dest_dir
    assert not (target / "communication" / "glossary.md").exists()


def test_attach_communication_no_stray_tmp_files_after_success(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "kg_raw_word.md").write_text("word graph content", encoding="utf-8")
    (source / "glossary.md").write_text("glossary content", encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()

    result = bridge.attach_communication(source, target)

    assert set(result["attached"]) == {"kg_raw_word.md", "glossary.md"}
    dest_dir = target / "communication"
    leftover_tmp = [p for p in dest_dir.iterdir() if p.suffix == ".tmp" or p.name.endswith(".tmp")]
    assert leftover_tmp == []
    # only the real artifact files should be present
    assert {p.name for p in dest_dir.iterdir()} == {"kg_raw_word.md", "glossary.md"}


def test_attach_communication_target_symlink_exits(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    real_target = tmp_path / "real_target"
    real_target.mkdir()
    target_symlink = tmp_path / "target_link"
    target_symlink.symlink_to(real_target)

    with pytest.raises(SystemExit):
        bridge.attach_communication(source, target_symlink)


def test_attach_communication_dest_dir_symlink_exits(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    target = tmp_path / "target"
    target.mkdir()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    # target/communication is itself a symlink
    (target / "communication").symlink_to(elsewhere)

    with pytest.raises(SystemExit):
        bridge.attach_communication(source, target)


def test_attach_communication_missing_source_dir_exits(tmp_path):
    missing_source = tmp_path / "does_not_exist"
    target = tmp_path / "target"
    target.mkdir()

    with pytest.raises(SystemExit):
        bridge.attach_communication(missing_source, target)


def test_attach_communication_empty_source_dir_returns_empty_no_crash(tmp_path):
    source = tmp_path / "source"
    source.mkdir()  # empty, no matching artifact names
    target = tmp_path / "target"
    target.mkdir()

    result = bridge.attach_communication(source, target)

    assert result == {"attached": [], "skipped": []}


def test_attach_communication_overwrite_on_change_updates_destination(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    target = tmp_path / "target"
    target.mkdir()
    artifact = source / "glossary.md"

    artifact.write_text("version 1 content", encoding="utf-8")
    result1 = bridge.attach_communication(source, target)
    assert result1["attached"] == ["glossary.md"]
    dest = target / "communication" / "glossary.md"
    assert dest.read_text(encoding="utf-8") == "version 1 content"

    artifact.write_text("version 2 content — updated", encoding="utf-8")
    result2 = bridge.attach_communication(source, target)
    assert result2["attached"] == ["glossary.md"]
    assert dest.read_text(encoding="utf-8") == "version 2 content — updated"


# ---------------------------------------------------------------------------
# link_communication_in_readme()
# ---------------------------------------------------------------------------


def test_link_communication_in_readme_idempotent(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    original = "# target\n\nSome original README content.\n"
    (target / "README.md").write_text(original, encoding="utf-8")

    wrote1 = bridge.link_communication_in_readme(target, ["kg_raw_word.md", "skill_plan.md"])
    assert wrote1 is True
    text_after_first = (target / "README.md").read_text(encoding="utf-8")
    assert text_after_first.count(bridge.COMMUNICATION_LINK_MARKER) == 1

    wrote2 = bridge.link_communication_in_readme(target, ["kg_raw_word.md", "skill_plan.md"])
    assert wrote2 is False
    text_after_second = (target / "README.md").read_text(encoding="utf-8")
    assert text_after_second.count(bridge.COMMUNICATION_LINK_MARKER) == 1
    assert text_after_second == text_after_first


def test_link_communication_no_readme_returns_false_no_crash(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    # deliberately no README.md

    result = bridge.link_communication_in_readme(target, ["glossary.md"])

    assert result is False
    assert not (target / "README.md").exists()


def test_link_communication_empty_attached_list_returns_false_no_change(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    original = "# target\n\nOriginal content, byte for byte.\n"
    (target / "README.md").write_text(original, encoding="utf-8")

    result = bridge.link_communication_in_readme(target, [])

    assert result is False
    assert (target / "README.md").read_text(encoding="utf-8") == original


def test_link_communication_preserves_original_content(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    original = "# My Project\n\n## Document map\n\nSome important navigation table.\n"
    (target / "README.md").write_text(original, encoding="utf-8")

    bridge.link_communication_in_readme(target, ["skill_plan.md"])

    text = (target / "README.md").read_text(encoding="utf-8")
    assert text.startswith(original)
    assert "skill_plan.md" in text


# ---------------------------------------------------------------------------
# _escape_cell()
# ---------------------------------------------------------------------------


def test_escape_cell_backtick_removed():
    # backticks are stripped (replaced with a plain quote), not escaped —
    # an unescaped backtick could still break an inline `code` wrapper.
    assert "`" not in bridge._escape_cell("has`backtick")


def test_escape_cell_pipe_is_escaped_not_left_bare():
    # a bare "|" would break a Markdown table row's column count, so it must
    # be turned into the escaped form "\|", never left as a literal "|".
    escaped = bridge._escape_cell("has|pipe")
    assert "\\|" in escaped
    assert "|" not in escaped.replace("\\|", "")


def test_escape_cell_newline_removed():
    assert "\n" not in bridge._escape_cell("has\nnewline")


def test_escape_cell_carriage_return_removed():
    assert "\r" not in bridge._escape_cell("has\rcarriage_return")


def test_escape_cell_all_four_together():
    raw = "a`b|c\nd\re"
    escaped = bridge._escape_cell(raw)
    assert "`" not in escaped
    assert "\n" not in escaped
    assert "\r" not in escaped
    assert "|" not in escaped.replace("\\|", "")


# ---------------------------------------------------------------------------
# seed_docs()
# ---------------------------------------------------------------------------


def test_seed_docs_escapes_backtick_in_hypothesis_card(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    # seed_docs() only requires the file to already exist, not a full scaffold
    (target / "PLAN.md").write_text("# PLAN\n\nplaceholder\n", encoding="utf-8")

    run = {
        "registration": {},
        "issue": {},
        "retained_difference": {},
        "hypothesis_portfolio": {
            "status": "CHECKPOINT",
            "hypothesis_cards": [
                {
                    "hypothesis_id": "H1`; DROP",
                    "lane": "lane-a",
                    "claim": "claim with a `backtick` inside it",
                }
            ],
        },
    }

    n_seeded = bridge.seed_docs(target, run, "checkpoint-ref-1")
    assert n_seeded == 1

    plan_text = (target / "PLAN.md").read_text(encoding="utf-8")
    assert bridge.SEED_DOCS_MARKER in plan_text

    # find the bullet line for this hypothesis card
    bullet_lines = [ln for ln in plan_text.splitlines() if ln.startswith("- ")]
    assert bullet_lines, "expected at least one bullet line in PLAN.md"
    target_line = bullet_lines[-1]
    # the raw backtick from hypothesis_id/claim must not appear unescaped —
    # only the deliberate wrapper backticks written by seed_docs() itself
    # ("`{id}`" / "({lane})") are allowed, so no stray/unpaired backtick.
    assert target_line.count("`") % 2 == 0


def test_seed_docs_idempotent_skips_already_marked_file(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (target / "PLAN.md").write_text("# PLAN\n\nplaceholder\n", encoding="utf-8")
    (target / "GOAL.md").write_text("# GOAL\n\nplaceholder\n", encoding="utf-8")
    (target / "SPEC.md").write_text("# SPEC\n\nplaceholder\n", encoding="utf-8")

    run = {
        "registration": {"query": "q", "success_rule": "s", "failure_rule": "f"},
        "issue": {},
        "retained_difference": {},
        "hypothesis_portfolio": {"status": "CHECKPOINT", "hypothesis_cards": []},
    }

    n1 = bridge.seed_docs(target, run, "cp-1")
    assert n1 == 3
    n2 = bridge.seed_docs(target, run, "cp-1")
    assert n2 == 0  # already marked -> no-op, no duplicate sections


# ---------------------------------------------------------------------------
# seed_sot_docs() / link_sot_docs_in_readme()
# ---------------------------------------------------------------------------


def _sot_test_run():
    return {
        "registration": {
            "success_rule": "urgency detectable in under 90 seconds per case",
            "failure_rule": "any red-flag case missed",
        },
        "hypothesis_portfolio": {
            "hypothesis_cards": [
                {
                    "hypothesis_id": "H1",
                    "claim": "claim text for H1",
                    "mechanism": "mechanism text for H1",
                    "predicted_readout": "predicted readout for H1",
                    "falsifier": "falsifier for H1",
                },
                {
                    "hypothesis_id": "H2",
                    "claim": "claim text for H2",
                    "mechanism": "mechanism text for H2",
                    "predicted_readout": "predicted readout for H2",
                    "falsifier": "falsifier for H2",
                },
            ],
        },
        "hypothesis_evidence_challenge": {
            "hypotheses": [
                {
                    "hypothesis_id": "H1",
                    "international_track": {
                        "sources_searched": ["real international index X"],
                        "result_status": "EVIDENCE_FOUND",
                    },
                    "local_context_track": {
                        "sources_searched": ["real local archive Y"],
                        "result_status": "LOCAL_EVIDENCE_FOUND",
                    },
                    "evidence_gaps": ["gap A for H1"],
                    "next_discriminating_test": "test A for H1",
                    "citation_cards": [
                        {
                            "title": "Real Verified Source",
                            "authors_or_issuer": "Real Org",
                            "year": 2026,
                            "source_type": "journal_article",
                            "quality": "HIGH",
                            "directness": "DIRECT",
                            "context_fit": "HIGH",
                            "metadata_verification": "VERIFIED",
                            "scope_verification": "VERIFIED",
                            "persistent_id_or_official_url": "https://example.org/real-source",
                        },
                        {
                            "title": "[SimulatedData] fixture citation",
                            "authors_or_issuer": "UIA fixture",
                            "year": 2026,
                            "source_type": "synthetic_fixture",
                            "quality": "LOW",
                            "directness": "PARTIAL",
                            "context_fit": "LOW",
                            "metadata_verification": "SIMULATED_ONLY",
                            "scope_verification": "SIMULATED_ONLY",
                            "persistent_id_or_official_url": "fixture://H1",
                        },
                    ],
                },
                {
                    "hypothesis_id": "H2",
                    "international_track": {},
                    "local_context_track": {},
                    "evidence_gaps": [],
                    "next_discriminating_test": None,
                    "citation_cards": [],
                },
            ],
        },
    }


def test_seed_sot_docs_creates_three_files_in_sot_dir(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    written = bridge.seed_sot_docs(target, _sot_test_run(), "cp-sot-1")

    assert sorted(written) == sorted(bridge.SOT_DOC_FILES)
    for name in bridge.SOT_DOC_FILES:
        p = target / "sot" / name
        assert p.exists()
        assert bridge.SOT_DOCS_MARKER in p.read_text(encoding="utf-8")


def test_seed_sot_docs_idempotent(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    run = _sot_test_run()

    written1 = bridge.seed_sot_docs(target, run, "cp-sot-1")
    assert len(written1) == 3
    texts_after_first = {
        name: (target / "sot" / name).read_text(encoding="utf-8") for name in bridge.SOT_DOC_FILES
    }

    written2 = bridge.seed_sot_docs(target, run, "cp-sot-1")
    assert written2 == []
    for name in bridge.SOT_DOC_FILES:
        assert (target / "sot" / name).read_text(encoding="utf-8") == texts_after_first[name]


def test_seed_sot_docs_rag_md_readout_matches_checkpoint_fields(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    bridge.seed_sot_docs(target, _sot_test_run(), "cp-sot-1")

    rag_text = (target / "sot" / "rag.md").read_text(encoding="utf-8")
    assert "real international index X" in rag_text
    assert "real local archive Y" in rag_text
    assert "gap A for H1" in rag_text
    assert "test A for H1" in rag_text
    # H2 has no sources/gaps/test declared — must degrade gracefully, not crash
    # or silently omit H2 from the readout entirely.
    assert "`H2`" in rag_text


def test_seed_sot_docs_cite_md_flags_simulated_only_not_real_citation(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    bridge.seed_sot_docs(target, _sot_test_run(), "cp-sot-1")

    cite_text = (target / "sot" / "cite.md").read_text(encoding="utf-8")
    assert "Real Verified Source" in cite_text
    assert "[SimulatedData] fixture citation" in cite_text
    # only the SIMULATED_ONLY card is flagged in the warning section, not the
    # real one — split on the warning heading and check placement.
    warning_section = cite_text.split("## Citation quality warning")[1]
    assert "[SimulatedData] fixture citation" in warning_section
    assert "Real Verified Source" not in warning_section


def test_seed_sot_docs_eq_md_shows_success_and_failure_rules(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    bridge.seed_sot_docs(target, _sot_test_run(), "cp-sot-1")

    eq_text = (target / "sot" / "eq.md").read_text(encoding="utf-8")
    assert "urgency detectable in under 90 seconds per case" in eq_text
    assert "any red-flag case missed" in eq_text
    assert "claim text for H1" in eq_text
    assert "mechanism text for H2" in eq_text


def test_seed_sot_docs_never_fabricates_content_in_placeholder_sections(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    bridge.seed_sot_docs(target, _sot_test_run(), "cp-sot-1")

    for name in bridge.SOT_DOC_FILES:
        text = (target / "sot" / name).read_text(encoding="utf-8")
        assert "NOT auto-generated" in text
    # eq.md's equations section must stay a placeholder — no fabricated formula.
    eq_text = (target / "sot" / "eq.md").read_text(encoding="utf-8")
    formulas_section = eq_text.split("## Formulas/equations")[1]
    assert "do not fabricate a formula" in formulas_section


def test_seed_sot_docs_handles_missing_evidence_challenge_gracefully(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    run = {
        "registration": {},
        "hypothesis_portfolio": {
            "hypothesis_cards": [{"hypothesis_id": "H1", "claim": "c", "mechanism": "m"}]
        },
        # hypothesis_evidence_challenge entirely absent
    }

    written = bridge.seed_sot_docs(target, run, "cp-sot-2")

    assert sorted(written) == sorted(bridge.SOT_DOC_FILES)
    rag_text = (target / "sot" / "rag.md").read_text(encoding="utf-8")
    assert "(none recorded)" in rag_text


def test_link_sot_docs_in_readme_idempotent(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    original = "# target\n\nSome original README content.\n"
    (target / "README.md").write_text(original, encoding="utf-8")

    wrote1 = bridge.link_sot_docs_in_readme(target, ["rag.md", "cite.md", "eq.md"])
    assert wrote1 is True
    text_after_first = (target / "README.md").read_text(encoding="utf-8")
    assert text_after_first.count(bridge.SOT_LINK_MARKER) == 1

    wrote2 = bridge.link_sot_docs_in_readme(target, ["rag.md", "cite.md", "eq.md"])
    assert wrote2 is False
    text_after_second = (target / "README.md").read_text(encoding="utf-8")
    assert text_after_second.count(bridge.SOT_LINK_MARKER) == 1
    assert text_after_second == text_after_first


def test_link_sot_docs_no_readme_returns_false_no_crash(tmp_path):
    target = tmp_path / "target"
    target.mkdir()

    result = bridge.link_sot_docs_in_readme(target, ["rag.md"])

    assert result is False
    assert not (target / "README.md").exists()


def test_link_sot_docs_empty_written_list_returns_false_no_change(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    original = "# target\n\nOriginal content, byte for byte.\n"
    (target / "README.md").write_text(original, encoding="utf-8")

    result = bridge.link_sot_docs_in_readme(target, [])

    assert result is False
    assert (target / "README.md").read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# validate_checkpoint() / load_kernel()
# ---------------------------------------------------------------------------


def test_validate_checkpoint_refuses_invalid_run_with_systemexit():
    kernel = bridge.load_kernel(REPO_ROOT)
    invalid_run = {}  # nowhere near a valid checkpoint record

    with pytest.raises(SystemExit) as exc_info:
        bridge.validate_checkpoint(kernel, invalid_run)

    assert "REFUSED" in str(exc_info.value)


@needs_doc_eco
def test_validate_checkpoint_accepts_real_demo_checkpoint():
    kernel = bridge.load_kernel(REPO_ROOT)
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "uia_protocol_kernel.py"), "--print-checkpoint-demo"],
        capture_output=True,
        text=True,
        check=True,
    )
    import json

    run = json.loads(result.stdout)
    validated = bridge.validate_checkpoint(kernel, run)
    assert validated["protocol_status"] == "VALID_CHECKPOINT"


# ---------------------------------------------------------------------------
# ensure_scaffold() — needs the real sibling repo + node
# ---------------------------------------------------------------------------


@needs_doc_eco
def test_ensure_scaffold_real_init_mjs_creates_scaffold_and_is_idempotent(tmp_path):
    target = tmp_path / "proj"

    scaffolded = bridge.ensure_scaffold(DOC_ECO_REPO, target)
    assert scaffolded is True
    assert (target / "AGENTS.md").exists()
    assert (target / "README.md").exists()
    assert (target / "DECISIONS.md").exists()

    # second call: AGENTS.md already exists -> no-op, no crash
    scaffolded_again = bridge.ensure_scaffold(DOC_ECO_REPO, target)
    assert scaffolded_again is False


@needs_doc_eco
def test_ensure_scaffold_wrong_doc_eco_repo_exits(tmp_path):
    target = tmp_path / "proj"
    wrong_repo = tmp_path / "not_a_doc_eco_repo"
    wrong_repo.mkdir()

    with pytest.raises(SystemExit):
        bridge.ensure_scaffold(wrong_repo, target)
