import copy
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PLAN = REPO_ROOT / "communication_glossary" / "skill_plan.py"
FIXTURE_DIR = REPO_ROOT / "communication_glossary" / "examples" / "fintech"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "communication_glossary"))
import skill_plan as sp  # noqa: E402


def _load_fixture():
    run = json.loads((FIXTURE_DIR / "checkpoint.json").read_text(encoding="utf-8"))
    glossary_md = (FIXTURE_DIR / "glossary.md").read_text(encoding="utf-8")
    expert_md = (FIXTURE_DIR / "kg_expert_layer.md").read_text(encoding="utf-8")
    return run, glossary_md, expert_md


# --- 1. extract_open_questions() heading matching ---------------------------


def test_extract_open_questions_exact_canonical_heading():
    run, glossary_md, expert_md = _load_fixture()
    result = sp.extract_open_questions(expert_md)
    assert "SOX/COSO-scoped" in result
    assert result.strip() != ""


def test_extract_open_questions_fallback_takes_last_match_not_first():
    # Earlier DECOY heading also starts with "Open questions" but is a
    # different, unrelated section; the real canonical-ish section comes
    # later. The exact canonical heading is deliberately NOT present here so
    # the loosened prefix-match fallback path is exercised.
    expert_md = (
        "# kg_expert_layer\n"
        "\n"
        "## Open questions for unrelated funding topic\n"
        "DECOY CONTENT — must not be returned.\n"
        "\n"
        "## Some other section\n"
        "irrelevant filler\n"
        "\n"
        "## Open questions where a human expert should weigh in\n"
        "REAL CONTENT — this is what must be returned.\n"
    )
    result = sp.extract_open_questions(expert_md)
    assert "REAL CONTENT" in result
    assert "DECOY CONTENT" not in result


def test_extract_open_questions_no_heading_returns_empty():
    assert sp.extract_open_questions("# no matching sections here\nsome text\n") == ""


# --- 2. _md_escape() ---------------------------------------------------------


def test_md_escape_neutralizes_backtick():
    assert sp._md_escape("H`1") == "H'1"
    assert "`" not in sp._md_escape("a`b`c")


def test_build_neutralizes_backtick_in_hypothesis_id_and_claim():
    run, glossary_md, expert_md = _load_fixture()
    run = copy.deepcopy(run)
    card = run["hypothesis_portfolio"]["hypothesis_cards"][0]
    card["hypothesis_id"] = "H`1"
    card["claim"] = "claim with a `backtick` inside it"
    out = sp.build(run, glossary_md, expert_md)
    # The bold+code-span wrapper is "**`{id}`**" — if the backtick inside the
    # id itself were NOT neutralized, it would prematurely close the code
    # span and corrupt the wrapper. Assert the wrapper is intact and no raw
    # backtick from the injected id/claim text survives.
    assert "**`H'1`**" in out
    assert "H`1" not in out
    assert "claim with a 'backtick' inside it" in out


# --- 3. review_mode handling --------------------------------------------------


def _run_with_review_mode(review_mode):
    run, glossary_md, expert_md = _load_fixture()
    run = copy.deepcopy(run)
    run["hypothesis_evidence_challenge"]["review_mode"] = review_mode
    return sp.build(run, glossary_md, expert_md)


def test_review_mode_targeted_search_note():
    out = _run_with_review_mode("TARGETED_SEARCH")
    assert "literature/published" in out


def test_review_mode_internal_data_audit_note():
    out = _run_with_review_mode("INTERNAL_DATA_AUDIT")
    assert "internal system-of-record data" in out


def test_review_mode_field_observation_log_note():
    out = _run_with_review_mode("FIELD_OBSERVATION_LOG")
    assert "fresh sensory/field observation" in out


def test_review_mode_unrecognized_value_gets_not_recognized_note():
    out = _run_with_review_mode("SOME_MADE_UP_MODE")
    assert "is not one of the 3 recognized values" in out
    assert "SOME_MADE_UP_MODE" in out


def test_review_mode_missing_evidence_dict_gets_entirely_missing_note():
    run, glossary_md, expert_md = _load_fixture()
    run = copy.deepcopy(run)
    del run["hypothesis_evidence_challenge"]
    out = sp.build(run, glossary_md, expert_md)
    assert "entirely missing from this checkpoint" in out


def test_unrecognized_and_missing_notes_are_different_messages():
    unrecognized_out = _run_with_review_mode("SOME_MADE_UP_MODE")

    run, glossary_md, expert_md = _load_fixture()
    run = copy.deepcopy(run)
    del run["hypothesis_evidence_challenge"]
    missing_out = sp.build(run, glossary_md, expert_md)

    def _note_line(text):
        for line in text.splitlines():
            if "หมายเหตุเฉพาะ checkpoint" in line:
                return line
        raise AssertionError("note line not found")

    assert _note_line(unrecognized_out) != _note_line(missing_out)
    assert "entirely missing" not in unrecognized_out
    assert "is not one of the 3 recognized values" not in missing_out


# --- 4. extract_human_checks() robustness ------------------------------------


def test_extract_human_checks_hypothesis_cards_as_dict_does_not_raise():
    run = {"hypothesis_portfolio": {"hypothesis_cards": {"H1": {"hypothesis_id": "H1"}}}}
    # as_list() on a dict wraps the whole dict as a single element (dict is
    # not a list), so extract_human_checks must not raise AttributeError —
    # it should simply treat that single non-dict-shaped-as-expected element
    # safely (isinstance(card, dict) guard covers the wrapped dict itself).
    checks = sp.extract_human_checks(run)
    assert isinstance(checks, list)


def test_extract_human_checks_skips_non_dict_card_in_list():
    run = {
        "hypothesis_portfolio": {
            "hypothesis_cards": [
                "not-a-dict-should-be-skipped",
                {"hypothesis_id": "H1", "lane": "primary", "claim": "a real claim"},
                42,
            ]
        }
    }
    checks = sp.extract_human_checks(run)
    assert len(checks) == 1
    assert checks[0]["hypothesis_id"] == "H1"


def test_extract_human_checks_real_fixture_matches_card_count():
    run, _, _ = _load_fixture()
    checks = sp.extract_human_checks(run)
    cards = run["hypothesis_portfolio"]["hypothesis_cards"]
    assert len(checks) == len(cards)
    assert {c["hypothesis_id"] for c in checks} == {c["hypothesis_id"] for c in cards}


# --- 5. checklist header fallback when zero hypothesis_cards -----------------


def test_checklist_shows_fallback_when_no_hypothesis_cards():
    run, glossary_md, expert_md = _load_fixture()
    run = copy.deepcopy(run)
    run["hypothesis_portfolio"]["hypothesis_cards"] = []
    out = sp.build(run, glossary_md, expert_md)
    assert "ไม่มี hypothesis_cards ที่อ่านได้" in out
    # The normal per-card bullet lines must not appear when there are no cards.
    assert "falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง" not in out


def test_checklist_shows_per_card_bullets_when_cards_present():
    run, glossary_md, expert_md = _load_fixture()
    out = sp.build(run, glossary_md, expert_md)
    assert "falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง" in out
    assert "ไม่มี hypothesis_cards ที่อ่านได้" not in out


# --- 6. main()/validate_checkpoint() refuses invalid checkpoints -------------


def test_validate_checkpoint_raises_systemexit_for_invalid_run():
    run, _, _ = _load_fixture()
    run = copy.deepcopy(run)
    # Corrupt structurally: drop hypothesis_portfolio entirely so the kernel
    # cannot possibly call this VALID_CHECKPOINT.
    del run["hypothesis_portfolio"]
    try:
        sp.validate_checkpoint(run)
    except SystemExit as e:
        assert "REFUSED" in str(e)
    else:
        raise AssertionError("expected SystemExit for invalid checkpoint")


def test_cli_refuses_invalid_checkpoint_before_writing_output(tmp_path):
    run, _, _ = _load_fixture()
    run = copy.deepcopy(run)
    del run["hypothesis_portfolio"]
    bad_checkpoint = tmp_path / "bad_checkpoint.json"
    bad_checkpoint.write_text(json.dumps(run), encoding="utf-8")
    out_path = tmp_path / "out_skill_plan.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SKILL_PLAN),
            str(bad_checkpoint),
            str(FIXTURE_DIR / "glossary.md"),
            str(FIXTURE_DIR / "kg_expert_layer.md"),
            str(out_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "REFUSED" in (result.stdout + result.stderr)
    assert not out_path.exists()


# --- 7. end-to-end sanity against the real fintech fixture -------------------


def test_end_to_end_build_against_real_fintech_fixture():
    run, glossary_md, expert_md = _load_fixture()
    out = sp.build(run, glossary_md, expert_md)
    assert "HYP-UIA-046-DEMO-001" in out
    assert "unknown-checkpoint" not in out
    for heading in (
        "## 1. Human",
        "## 2. AI-orchestrator",
        "## 3. AI-doer",
        "## 4. AI-auditor",
    ):
        assert heading in out
    hypothesis_ids = {c["hypothesis_id"] for c in run["hypothesis_portfolio"]["hypothesis_cards"]}
    assert any(hid in out for hid in hypothesis_ids)


def test_cli_end_to_end_against_real_fintech_fixture(tmp_path):
    out_path = tmp_path / "out_skill_plan.md"
    result = subprocess.run(
        [
            sys.executable,
            str(SKILL_PLAN),
            str(FIXTURE_DIR / "checkpoint.json"),
            str(FIXTURE_DIR / "glossary.md"),
            str(FIXTURE_DIR / "kg_expert_layer.md"),
            str(out_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")
    assert "HYP-UIA-046-DEMO-001" in content
    assert "unknown-checkpoint" not in content
    for heading in (
        "## 1. Human",
        "## 2. AI-orchestrator",
        "## 3. AI-doer",
        "## 4. AI-auditor",
    ):
        assert heading in content
