#!/usr/bin/env python3
"""Bridge: SkillMe phase-12 hypothesis checkpoint -> doc-ecosystem project scaffold.

See README.md in this folder for the design rationale and the test plan (already
run once as a smoke test against the SkillMe `--print-checkpoint-demo` fixture — see
README "Status"). Originally written and smoke-tested in a standalone
`uia-doc-ecosystem-bridge` repo, then absorbed into this repo (2026-08-01) so the
integration lives with the protocol it extends, under one name.

2026-08-01: an ultracode scenario-testing run found and this file then fixed 5
issues — see README "Status" for the full list (Markdown-cell escaping,
idempotency/dedup, DECISIONS.md row insertion order, write ordering, malformed-
JSON handling).

2026-08-01 (later): added --attach-communication to link this bridge's target
doc-ecosystem project to the communication_glossary pipeline's output
(Layers 1-4: raw word graph, expert-framework layer, issue-anchored glossary,
skill plan) — a straight file copy, not a new pipeline stage; see README.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

DECISIONS_OPEN_MARKER = "| # | Question | Blocks | Who decides | Since |\n|---|---|---|---|---|\n"


def load_kernel(uia_repo: Path):
    sys.path.insert(0, str(uia_repo))
    import skillme_protocol_kernel  # type: ignore

    return skillme_protocol_kernel


def validate_checkpoint(kernel, run: dict) -> dict:
    result = kernel.validate(run)
    if result.get("protocol_status") != "VALID_CHECKPOINT":
        raise SystemExit(
            "REFUSED: run is not a VALID_CHECKPOINT hypothesis portfolio "
            f"(protocol_status={result.get('protocol_status')!r}, "
            f"errors={result.get('errors')}). Fix the run record — a bridge that "
            "proceeds on invalid data would smuggle an unvalidated hypothesis into "
            "the doc ecosystem as if it had been checked."
        )
    return result


def ensure_scaffold(doc_eco_repo: Path, target: Path) -> bool:
    """Returns True iff this call actually scaffolded (False if already present)."""
    if (target / "AGENTS.md").exists():
        return False
    init_mjs = doc_eco_repo / "plugins/doc-ecosystem/skills/doc-ecosystem/tools/init.mjs"
    if not init_mjs.exists():
        raise SystemExit(f"REFUSED: init.mjs not found at {init_mjs} — wrong --doc-eco-repo?")
    subprocess.run(["node", str(init_mjs), str(target), "--all"], check=True)
    return True


def project_label(run: dict, target: Path) -> str:
    """A human-readable label for this checkpoint, preferring real checkpoint content
    over the target directory's basename (which is often a throwaway path)."""
    metadata = run.get("metadata", {})
    label = metadata.get("fixture_id")
    if not label:
        query = (run.get("registration", {}) or {}).get("query")
        if query:
            label = query.strip()
            if len(label) > 60:
                label = label[:57].rstrip() + "..."
    return label or target.name


def retitle_scaffold(target: Path, label: str) -> None:
    """Replace the scaffold's basename-derived title with `label`, only for the
    exact title line init.mjs wrote (never touches body text elsewhere)."""
    basename = target.name
    if label == basename:
        return
    for relpath, prefix in (("README.md", "# "), ("DECISIONS.md", "# DECISIONS — ")):
        p = target / relpath
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        old_line = f"{prefix}{basename}"
        if text.startswith(old_line):
            text = f"{prefix}{label}" + text[len(old_line):]
            p.write_text(text, encoding="utf-8")


SEED_DOCS_MARKER = "## AI-drafted starting point"


def seed_docs(target: Path, run: dict, checkpoint_ref: str) -> int:
    """Draft GOAL.md/SPEC.md/PLAN.md sections from checkpoint fields the kernel has
    already validated, so a human isn't re-typing what's already been checked.
    Idempotent (skips a file that already carries the marker) and clearly labeled
    as an AI draft, not a substitute for the human's own account of the project —
    per doc-eco's own README, AGENTS.md/GOAL.md must be filled by whoever did the
    encountering; this only saves re-typing already-validated checkpoint content."""
    registration = run.get("registration", {}) or {}
    issue = run.get("issue", {}) or {}
    retained_difference = run.get("retained_difference", {}) or {}
    disclaimer = (
        f"\n\n{SEED_DOCS_MARKER} (from SkillMe checkpoint {checkpoint_ref})\n\n"
        "> Draft only, pulled from a validated SkillMe checkpoint — not written by "
        "whoever did the encountering. Review and edit before treating as settled.\n\n"
    )

    sections = {
        "GOAL.md": (
            f"**Query:** {registration.get('query', '(not recorded)')}\n\n"
            f"**Success rule:** {registration.get('success_rule', '(not recorded)')}\n\n"
            f"**Failure rule:** {registration.get('failure_rule', '(not recorded)')}\n"
        ),
        "SPEC.md": (
            f"**Requested readout:** {issue.get('requested_readout', '(not recorded)')}\n\n"
            f"**Unresolved semantics:** {issue.get('unresolved_semantics', '(not recorded)')}\n\n"
            f"**Baseline (retained_difference):** {retained_difference.get('baseline', '(not recorded)')}\n\n"
            f"**Comparison:** {retained_difference.get('comparison', '(not recorded)')}\n"
        ),
        "PLAN.md": (
            f"**Checkpoint status:** {(run.get('hypothesis_portfolio') or {}).get('status', '(not recorded)')}\n\n"
            "**Candidate directions to evaluate before SkillMe phase 13** (from this "
            "checkpoint's hypothesis portfolio, not yet decided):\n\n"
            + "\n".join(
                f"- `{_escape_cell(c.get('hypothesis_id', '?'))}` "
                f"({_escape_cell(c.get('lane', '?'))}): {_escape_cell(c.get('claim', '?'))}"
                for c in (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards", [])
            )
            + "\n"
        ),
    }

    n_seeded = 0
    for relpath, body in sections.items():
        p = target / relpath
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if SEED_DOCS_MARKER in text:
            continue
        p.write_text(text + disclaimer + body, encoding="utf-8")
        n_seeded += 1
    return n_seeded


COMMUNICATION_ARTIFACTS = ("kg_raw_word.md", "kg_expert_layer.md", "glossary.md", "skill_plan.md")


def attach_communication(source_dir: Path, target: Path) -> dict:
    """Copy whichever communication_glossary artifacts exist for this checkpoint
    (kg_raw_word.md / kg_expert_layer.md / glossary.md / skill_plan.md — Layers
    1-4) into target/communication/. This does NOT run kg_extract.py/
    build_glossary.py/skill_plan.py itself — those are separate pipeline stages
    (Layer 2 needs an Agent+WebSearch reasoning step this script has no business
    doing) — it only attaches already-produced files to the doc-ecosystem
    project so they live alongside GOAL.md/DECISIONS.md/logbook.jsonl instead of
    staying in a separate, easy-to-lose location. A straight overwrite-copy, not
    an append — safe to re-run after any layer is regenerated, and naturally
    idempotent when nothing changed (same bytes back).

    Each artifact is copied via write-to-temp-then-os.replace() (atomic within
    dest_dir) so a reader never observes a half-written file; a directory or
    symlink where a real artifact file is expected is skipped with a reported
    reason instead of crashing the whole run (a 2026-08-01 ultracode scenario
    scan found the prior implementation would raise IsADirectoryError on the
    former and silently follow the latter outside source_dir on the latter).
    Returns {"attached": [name, ...], "skipped": [(name, reason), ...]}."""
    if not source_dir.is_dir():
        raise SystemExit(f"REFUSED: --attach-communication source {source_dir} is not a directory")
    if target.is_symlink():
        raise SystemExit(f"REFUSED: target {target} is a symlink — refusing to write through it")
    dest_dir = target / "communication"
    if dest_dir.is_symlink():
        raise SystemExit(f"REFUSED: {dest_dir} is a symlink — refusing to write through it")
    dest_dir.mkdir(parents=True, exist_ok=True)

    attached = []
    skipped = []
    for name in COMMUNICATION_ARTIFACTS:
        src = source_dir / name
        if src.is_symlink():
            skipped.append((name, "is a symlink — refusing to follow it (could point outside source_dir)"))
            continue
        if not src.exists():
            continue
        if not src.is_file():
            skipped.append((name, "exists but is not a regular file (e.g. a directory)"))
            continue
        try:
            data = src.read_text(encoding="utf-8")
        except OSError as e:
            skipped.append((name, f"read failed: {e}"))
            continue
        dest = dest_dir / name
        fd, tmp_path = tempfile.mkstemp(dir=dest_dir, prefix=f".{name}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(data)
            os.replace(tmp_path, dest)
        except OSError as e:
            Path(tmp_path).unlink(missing_ok=True)
            skipped.append((name, f"write failed: {e}"))
            continue
        attached.append(name)
    return {"attached": attached, "skipped": skipped}


COMMUNICATION_LINK_MARKER = "## communication_glossary output"

ARTIFACT_LABELS = {
    "kg_raw_word.md": "Layer 1 — deterministic word/phrase graph, zero interpretation",
    "kg_expert_layer.md": "Layer 2 — expert-framework vocabulary (AI-interpretive, Open tier)",
    "glossary.md": "Layer 3 — issue-anchored communication glossary (mechanical merge)",
    "skill_plan.md": "Layer 4 — Human / AI-orchestrator / AI-doer / AI-auditor role & skill plan",
}


def link_communication_in_readme(target: Path, attached: list[str]) -> bool:
    """attach_communication() puts files in target/communication/, but nothing
    in the scaffold's own docs points there — a human/AI reading README.md has
    no way to discover it exists short of already knowing to look (the seam
    was a file copy, not a real connection). This adds one discoverable,
    idempotent pointer to README.md so Layer 1's word graph and Layer 4's
    skill plan are actually surfaced where a reader would look first, not
    just physically present on disk. Returns True iff it wrote anything."""
    if not attached:
        return False
    readme = target / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8")
    if COMMUNICATION_LINK_MARKER in text:
        return False
    bullets = "\n".join(
        f"- `communication/{name}` — {ARTIFACT_LABELS.get(name, name)}" for name in attached
    )
    note = (
        f"\n\n{COMMUNICATION_LINK_MARKER}\n\n"
        "This project's checkpoint has a `communication_glossary` pipeline output "
        "attached (see `skillme/communication_glossary/`):\n\n"
        f"{bullets}\n\n"
        "Start with `skill_plan.md` if you're deciding who needs to know/do what; "
        "start with `kg_raw_word.md` if you need the literal vocabulary this "
        "checkpoint actually used, not an interpretation of it.\n"
    )
    readme.write_text(text + note, encoding="utf-8")
    return True


SOT_DOCS_MARKER = "<!-- sot-doc:v1 -->"

SOT_DOC_FILES = ("rag.md", "cite.md", "eq.md")

SOT_DOC_TITLES = {
    "rag.md": "Retrieval / Source Registry",
    "cite.md": "Citation Ledger",
    "eq.md": "Quantitative Claims & Mechanisms",
}


def _hyp_evidence_by_id(run: dict) -> dict:
    challenge = run.get("hypothesis_evidence_challenge") or {}
    return {h.get("hypothesis_id"): h for h in (challenge.get("hypotheses") or []) if isinstance(h, dict)}


def _render_rag_md(run: dict, checkpoint_ref: str) -> str:
    evidence_by_id = _hyp_evidence_by_id(run)
    cards = (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards") or []
    lines = [
        f"# {SOT_DOC_TITLES['rag.md']} — {checkpoint_ref}",
        "",
        SOT_DOCS_MARKER,
        "",
        "**Tier: readout** (mechanical extraction of `hypothesis_evidence_challenge` fields "
        "already validated by the kernel) **+ Dr** (the last section — human/AI must fill it "
        "in, it is never auto-generated).",
        "",
        "## Sources already searched per hypothesis (readout)",
        "",
    ]
    for card in cards:
        hid = card.get("hypothesis_id", "?")
        ev = evidence_by_id.get(hid, {})
        intl = ev.get("international_track") or {}
        local = ev.get("local_context_track") or {}
        lines.append(f"- `{_escape_cell(hid)}`")
        lines.append(f"  - international_track.sources_searched: {_escape_cell(intl.get('sources_searched') or '(none recorded)')}")
        lines.append(f"  - international_track.result_status: {_escape_cell(intl.get('result_status', '(not recorded)'))}")
        lines.append(f"  - local_context_track.sources_searched: {_escape_cell(local.get('sources_searched') or '(none recorded)')}")
        lines.append(f"  - local_context_track.result_status: {_escape_cell(local.get('result_status', '(not recorded)'))}")
    lines += [
        "",
        "## Evidence gaps declared (readout)",
        "",
    ]
    for card in cards:
        hid = card.get("hypothesis_id", "?")
        ev = evidence_by_id.get(hid, {})
        gaps = ev.get("evidence_gaps") or []
        lines.append(f"- `{_escape_cell(hid)}`: {_escape_cell(gaps if gaps else '(none declared)')}")
    lines += [
        "",
        "## Next discriminating test named per hypothesis (readout)",
        "",
    ]
    for card in cards:
        hid = card.get("hypothesis_id", "?")
        ev = evidence_by_id.get(hid, {})
        lines.append(f"- `{_escape_cell(hid)}`: {_escape_cell(ev.get('next_discriminating_test', '(none recorded)'))}")
    lines += [
        "",
        "## Source classes / RAG corpora to add (human/AI to fill in — NOT auto-generated)",
        "",
        "_(e.g. domain-specific databases, internal systems-of-record, named external "
        "knowledge bases a real search would use for each hypothesis above — same "
        "WebSearch-verification discipline as `communication_glossary`'s Layer 2. This "
        "script only reads what the checkpoint already recorded; it does not invent "
        "domain judgment about what sources SHOULD exist.)_",
        "",
    ]
    return "\n".join(lines)


def _render_cite_md(run: dict, checkpoint_ref: str) -> str:
    evidence_by_id = _hyp_evidence_by_id(run)
    cards = (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards") or []
    lines = [
        f"# {SOT_DOC_TITLES['cite.md']} — {checkpoint_ref}",
        "",
        SOT_DOCS_MARKER,
        "",
        "**Tier: readout** (mechanical extraction of `citation_cards` already validated by "
        "the kernel — `citation_audit == \"PASS\"` means the card is *structurally* complete, "
        "not that the citation is real evidence; check `metadata_verification`/"
        "`scope_verification` below for that) **+ Dr** (the last section — human/AI to fill in).",
        "",
        "## Citations per hypothesis (readout)",
        "",
    ]
    simulated = []
    for card in cards:
        hid = card.get("hypothesis_id", "?")
        ev = evidence_by_id.get(hid, {})
        lines.append(f"- `{_escape_cell(hid)}`")
        for cc in ev.get("citation_cards") or []:
            if not isinstance(cc, dict):
                continue
            title = cc.get("title", "(no title)")
            lines.append(
                f"  - **{_escape_cell(title)}** — {_escape_cell(cc.get('authors_or_issuer', '?'))}, "
                f"{_escape_cell(cc.get('year', '?'))}, {_escape_cell(cc.get('source_type', '?'))}"
            )
            lines.append(
                f"    - quality: {_escape_cell(cc.get('quality', '?'))}, "
                f"directness: {_escape_cell(cc.get('directness', '?'))}, "
                f"context_fit: {_escape_cell(cc.get('context_fit', '?'))}"
            )
            lines.append(
                f"    - metadata_verification: {_escape_cell(cc.get('metadata_verification', '?'))}, "
                f"scope_verification: {_escape_cell(cc.get('scope_verification', '?'))}"
            )
            lines.append(f"    - source: {_escape_cell(cc.get('persistent_id_or_official_url', '(none)'))}")
            if cc.get("metadata_verification") == "SIMULATED_ONLY" or cc.get("scope_verification") == "SIMULATED_ONLY":
                simulated.append((hid, title))
    lines += [
        "",
        "## Citation quality warning (readout — automatic flag, not a judgment call)",
        "",
    ]
    if simulated:
        for hid, title in simulated:
            lines.append(
                f"- `{_escape_cell(hid)}` / \"{_escape_cell(title)}\": `SIMULATED_ONLY` — this is a "
                "synthetic fixture citation, not real evidence. Do not cite it as a real source."
            )
    else:
        lines.append("_(no `SIMULATED_ONLY` citations found in this checkpoint)_")
    lines += [
        "",
        "## Real citations to add (human/AI to fill in — NOT auto-generated)",
        "",
        "_(add real, verified sources here per hypothesis — to replace or supplement any "
        "`SIMULATED_ONLY` fixture citations flagged above. This script only reads what the "
        "checkpoint already recorded; it does not invent or verify citations itself.)_",
        "",
    ]
    return "\n".join(lines)


def _render_eq_md(run: dict, checkpoint_ref: str) -> str:
    cards = (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards") or []
    registration = run.get("registration", {}) or {}
    lines = [
        f"# {SOT_DOC_TITLES['eq.md']} — {checkpoint_ref}",
        "",
        SOT_DOCS_MARKER,
        "",
        "**Tier: readout** (mechanical — the fields below, verbatim, are where a numeric "
        "threshold or quantitative claim would already be stated if this checkpoint has "
        "one) **+ Dr** (the last section — human/AI to fill in, and is very often correctly "
        "left empty: most SkillMe hypotheses are qualitative causal claims with no citable "
        "formula, and that is not a gap).",
        "",
        "## Readout: claim/mechanism/predicted_readout/falsifier per hypothesis",
        "",
        "_(read these yourself for any explicit numeric thresholds — this is a verbatim "
        "readout, not a verified extraction; no regex/NLP guess is applied)_",
        "",
    ]
    for card in cards:
        hid = card.get("hypothesis_id", "?")
        lines.append(f"- `{_escape_cell(hid)}`")
        lines.append(f"  - claim: {_escape_cell(card.get('claim', '?'))}")
        lines.append(f"  - mechanism: {_escape_cell(card.get('mechanism', '?'))}")
        lines.append(f"  - predicted_readout: {_escape_cell(card.get('predicted_readout', '?'))}")
        lines.append(f"  - falsifier: {_escape_cell(card.get('falsifier', '?'))}")
    lines += [
        "",
        "## Success/failure thresholds declared for this checkpoint (readout)",
        "",
        f"- success_rule: {_escape_cell(registration.get('success_rule', '(not recorded)'))}",
        f"- failure_rule: {_escape_cell(registration.get('failure_rule', '(not recorded)'))}",
        "",
        "## Formulas/equations that formalize this issue's mechanism (human/AI to add — NOT auto-generated)",
        "",
        "_(most SkillMe hypotheses are qualitative causal claims — this section correctly stays "
        "empty unless the domain genuinely has a citable quantitative relationship, e.g. a "
        "staging threshold, a percentage-of-completion formula, a validated scoring cut-off. "
        "Verify via WebSearch the same way `communication_glossary`'s Layer 2 does before "
        "adding anything here — do not fabricate a formula to fill this section.)_",
        "",
    ]
    return "\n".join(lines)


_SOT_RENDERERS = {"rag.md": _render_rag_md, "cite.md": _render_cite_md, "eq.md": _render_eq_md}


def seed_sot_docs(target: Path, run: dict, checkpoint_ref: str) -> list[str]:
    """Create target/sot/{rag,cite,eq}.md — a source-of-truth document set for a
    hypothesis, separate from both doc-eco's own template files (seed_docs()
    above only ever fills in a file that already exists) and from
    communication_glossary's pipeline output (attach_communication() above is a
    different, unrelated artifact set). Every section here is either a direct
    readout of already-kernel-validated checkpoint fields, or an explicit
    "human/AI to fill in — NOT auto-generated" placeholder — this script never
    fabricates a recommended source, citation, or equation itself, matching the
    same mechanical-vs-interpretive discipline used throughout this repo.
    Idempotent per file via SOT_DOCS_MARKER — a file that already carries it is
    left untouched (this is a starting draft, not something to silently
    overwrite a human's later edits to). Returns the list of filenames actually
    (re)written this call."""
    sot_dir = target / "sot"
    sot_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name in SOT_DOC_FILES:
        p = sot_dir / name
        if p.exists() and SOT_DOCS_MARKER in p.read_text(encoding="utf-8"):
            continue
        p.write_text(_SOT_RENDERERS[name](run, checkpoint_ref), encoding="utf-8")
        written.append(name)
    return written


SOT_LINK_MARKER = "## Source-of-truth docs (rag / cite / eq)"


def link_sot_docs_in_readme(target: Path, written: list[str]) -> bool:
    """Same discoverability gap as link_communication_in_readme() above, for
    target/sot/ instead of target/communication/ — a discoverable, idempotent
    pointer in README.md so rag.md/cite.md/eq.md aren't only found by someone
    who already knows to look under sot/."""
    if not written:
        return False
    readme = target / "README.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8")
    if SOT_LINK_MARKER in text:
        return False
    bullets = "\n".join(f"- `sot/{name}` — {SOT_DOC_TITLES[name]}" for name in written)
    note = (
        f"\n\n{SOT_LINK_MARKER}\n\n"
        "This project's checkpoint has a source-of-truth document set drafted (readout + "
        "Dr-tier placeholders for human/AI to fill in — see each file's own tier banner):\n\n"
        f"{bullets}\n"
    )
    readme.write_text(text + note, encoding="utf-8")
    return True


def _escape_cell(text: str) -> str:
    """Neutralize characters that would break a Markdown table row's column count,
    or corrupt an inline `code`/bold wrapper elsewhere in this file (backtick)."""
    return str(text).replace("`", "'").replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def already_ingested(target: Path) -> set[tuple[str, str]]:
    """(checkpoint_ref, hypothesis_id) pairs already logged, from prior bridge.py runs."""
    logbook = target / "logbook.jsonl"
    if not logbook.exists():
        return set()
    seen = set()
    for line in logbook.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("kind") == "hypothesis" and entry.get("checkpoint_ref") and entry.get("hypothesis_id"):
            seen.add((entry["checkpoint_ref"], entry["hypothesis_id"]))
    return seen


def append_logbook(target: Path, checkpoint_ref: str, cards: list[dict]) -> int:
    logbook = target / "logbook.jsonl"
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = []
    for card in cards:
        entry = {
            "ts": now,
            "by": "ai",
            "kind": "hypothesis",
            "what": card["claim"],
            "falsifier": card["falsifier"],
            "source": f"SkillMe checkpoint {checkpoint_ref} / hypothesis {card['hypothesis_id']} "
            f"/ lane {card['lane']}",
            "mechanism": card.get("mechanism"),
            "causal_tier": card.get("causal_tier"),
            "evidence_ledger_ref": card.get("evidence_ledger_ref"),
            "checkpoint_ref": checkpoint_ref,
            "hypothesis_id": card["hypothesis_id"],
        }
        lines.append(json.dumps(entry, ensure_ascii=False))
    with logbook.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return len(lines)


def append_decisions_open(
    target: Path, cards: list[dict], since: str, decision_owners: list[str] | None = None
) -> int:
    decisions_md = target / "DECISIONS.md"
    text = decisions_md.read_text(encoding="utf-8")
    idx = text.find(DECISIONS_OPEN_MARKER)
    if idx == -1:
        raise SystemExit(
            f"REFUSED: {decisions_md} does not contain the expected Open-table header — "
            "template drifted from what this script was written against. Fix by hand "
            "rather than guessing where to insert."
        )
    insert_at = idx + len(DECISIONS_OPEN_MARKER)
    next_heading = text.find("\n##", insert_at)
    if next_heading == -1:
        next_heading = len(text)
    table_body = text[insert_at:next_heading]

    # Insert after the LAST existing "|"-prefixed row, not right after the header —
    # otherwise each new batch of rows lands above the previous ones (out of order).
    existing_rows = 0
    last_row_end = 0
    consumed = 0
    for ln in table_body.splitlines(keepends=True):
        consumed += len(ln)
        if ln.strip().startswith("|"):
            existing_rows += 1
            last_row_end = consumed
    insertion_point = insert_at + last_row_end

    new_rows = []
    for i, card in enumerate(cards):
        n = existing_rows + i + 1
        mechanism = _escape_cell(card.get("mechanism", "?"))
        lane = _escape_cell(card.get("lane", "?"))
        question = f"Does `{mechanism}` (lane {lane}) explain the issue?"
        if decision_owners:
            who = _escape_cell(", ".join(decision_owners))
        else:
            who = "founder" if card.get("legal_relevance") != "NONE" else "AI + founder review"
        new_rows.append(f"| {n} | {question} | SkillMe phase 13 candidate generation | {who} | {since} |")
    text = text[:insertion_point] + "\n".join(new_rows) + "\n" + text[insertion_point:]
    decisions_md.write_text(text, encoding="utf-8")
    return len(new_rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run_json", type=Path, help="SkillMe run record JSON file")
    p.add_argument("target", type=Path, help="target project directory for doc-ecosystem")
    p.add_argument(
        "--uia-repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    p.add_argument(
        "--doc-eco-repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "human-ai-doc-ecosystem",
    )
    p.add_argument(
        "--seed-docs",
        action="store_true",
        help="draft GOAL.md/SPEC.md/PLAN.md sections from already-validated checkpoint "
        "fields (clearly labeled as an AI draft) instead of leaving them at the "
        "scaffold's placeholder text",
    )
    p.add_argument(
        "--attach-communication",
        type=Path,
        default=None,
        metavar="DIR",
        help="copy whichever of kg_raw_word.md/kg_expert_layer.md/glossary.md/"
        "skill_plan.md (communication_glossary's Layers 1-4) exist in DIR into "
        "target/communication/ — does not run those scripts itself, only "
        "attaches already-produced output",
    )
    p.add_argument(
        "--seed-sot-docs",
        action="store_true",
        help="create target/sot/{rag,cite,eq}.md — a source-of-truth document set "
        "(sources searched per hypothesis, citation ledger, quantitative-claims "
        "readout) drafted from already-validated checkpoint fields, with explicit "
        "human/AI-to-fill-in placeholders — separate from both doc-eco's own "
        "template and communication_glossary's output",
    )
    args = p.parse_args()

    try:
        run = json.loads(args.run_json.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {args.run_json} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {args.run_json} is not valid JSON: {e}")

    kernel = load_kernel(args.uia_repo)
    result = validate_checkpoint(kernel, run)

    hypothesis_portfolio = run["hypothesis_portfolio"]
    cards = hypothesis_portfolio["hypothesis_cards"]
    checkpoint_ref = hypothesis_portfolio.get("checkpoint_certificate", "unknown-checkpoint")
    since = datetime.date.today().isoformat()

    args.target.mkdir(parents=True, exist_ok=True)
    freshly_scaffolded = ensure_scaffold(args.doc_eco_repo, args.target)
    if freshly_scaffolded:
        retitle_scaffold(args.target, project_label(run, args.target))

    if args.seed_docs:
        n_seeded = seed_docs(args.target, run, checkpoint_ref)
        if n_seeded:
            print(f"SEEDED {n_seeded} doc(s) with a draft from checkpoint fields (marked AI-drafted)")

    if args.attach_communication:
        attach_result = attach_communication(args.attach_communication, args.target)
        attached = attach_result["attached"]
        skipped = attach_result["skipped"]
        if attached:
            print(f"ATTACHED {len(attached)} communication artifact(s) to target/communication/: {', '.join(attached)}")
            if link_communication_in_readme(args.target, attached):
                print("  LINKED target/README.md -> communication/ (discoverable pointer added)")
        else:
            print(f"ATTACHED 0 communication artifacts — none of {COMMUNICATION_ARTIFACTS} found in {args.attach_communication}")
        for name, reason in skipped:
            print(f"  SKIPPED {name}: {reason}")

    if args.seed_sot_docs:
        sot_written = seed_sot_docs(args.target, run, checkpoint_ref)
        if sot_written:
            print(f"SEEDED {len(sot_written)} SOT doc(s) in target/sot/: {', '.join(sot_written)}")
            if link_sot_docs_in_readme(args.target, sot_written):
                print("  LINKED target/README.md -> sot/ (discoverable pointer added)")
        else:
            print("SEEDED 0 SOT docs — target/sot/{rag,cite,eq}.md already exist and are marked (idempotent no-op)")

    decision_owners = (run.get("agency", {}) or {}).get("decision_owners") or []

    seen = already_ingested(args.target)
    new_cards = [c for c in cards if (checkpoint_ref, c["hypothesis_id"]) not in seen]
    skipped = len(cards) - len(new_cards)

    # DECISIONS.md written first: if its header has drifted and this raises SystemExit,
    # logbook.jsonl (append-only history) is never touched — no partial-failure state.
    n_rows = append_decisions_open(args.target, new_cards, since, decision_owners) if new_cards else 0
    n_logged = append_logbook(args.target, checkpoint_ref, new_cards) if new_cards else 0

    if skipped:
        print(f"SKIPPED {skipped} hypothesis card(s) already ingested for checkpoint {checkpoint_ref!r} (idempotent no-op)")
    print(f"OK — {n_logged} hypothesis card(s) logged, {n_rows} row(s) added to DECISIONS.md")
    print(f"  target: {args.target}")
    print(f"  checkpoint state: {result['state']}, claim_boundary: {result['claim_boundary']}")


if __name__ == "__main__":
    main()
