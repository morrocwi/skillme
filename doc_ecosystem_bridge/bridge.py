#!/usr/bin/env python3
"""Bridge: UIA phase-12 hypothesis checkpoint -> doc-ecosystem project scaffold.

See README.md in this folder for the design rationale and the test plan (already
run once as a smoke test against the UIA `--print-checkpoint-demo` fixture — see
README "Status"). Originally written and smoke-tested in a standalone
`uia-doc-ecosystem-bridge` repo, then absorbed into this repo (2026-08-01) so the
integration lives with the protocol it extends, under one name.

2026-08-01: an ultracode scenario-testing run found and this file then fixed 5
issues — see README "Status" for the full list (Markdown-cell escaping,
idempotency/dedup, DECISIONS.md row insertion order, write ordering, malformed-
JSON handling).
"""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

DECISIONS_OPEN_MARKER = "| # | Question | Blocks | Who decides | Since |\n|---|---|---|---|---|\n"


def load_kernel(uia_repo: Path):
    sys.path.insert(0, str(uia_repo))
    import uia_protocol_kernel  # type: ignore

    return uia_protocol_kernel


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
        f"\n\n{SEED_DOCS_MARKER} (from UIA checkpoint {checkpoint_ref})\n\n"
        "> Draft only, pulled from a validated UIA checkpoint — not written by "
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
            "**Candidate directions to evaluate before UIA phase 13** (from this "
            "checkpoint's hypothesis portfolio, not yet decided):\n\n"
            + "\n".join(
                f"- `{c.get('hypothesis_id', '?')}` ({c.get('lane', '?')}): {c.get('claim', '?')}"
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


def _escape_cell(text: str) -> str:
    """Neutralize characters that would break a Markdown table row's column count."""
    return str(text).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


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
            "source": f"UIA checkpoint {checkpoint_ref} / hypothesis {card['hypothesis_id']} "
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
        new_rows.append(f"| {n} | {question} | UIA phase 13 candidate generation | {who} | {since} |")
    text = text[:insertion_point] + "\n".join(new_rows) + "\n" + text[insertion_point:]
    decisions_md.write_text(text, encoding="utf-8")
    return len(new_rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run_json", type=Path, help="UIA run record JSON file")
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
