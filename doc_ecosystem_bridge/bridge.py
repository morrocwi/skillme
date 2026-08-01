#!/usr/bin/env python3
"""Bridge: UIA phase-12 hypothesis checkpoint -> doc-ecosystem project scaffold.

See README.md in this folder for the design rationale and the test plan (already
run once as a smoke test against the UIA `--print-checkpoint-demo` fixture — see
README "Status"). Originally written and smoke-tested in a standalone
`uia-doc-ecosystem-bridge` repo, then absorbed into this repo (2026-08-01) so the
integration lives with the protocol it extends, under one name.
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


def ensure_scaffold(doc_eco_repo: Path, target: Path) -> None:
    if (target / "AGENTS.md").exists():
        return
    init_mjs = doc_eco_repo / "plugins/doc-ecosystem/skills/doc-ecosystem/tools/init.mjs"
    if not init_mjs.exists():
        raise SystemExit(f"REFUSED: init.mjs not found at {init_mjs} — wrong --doc-eco-repo?")
    subprocess.run(["node", str(init_mjs), str(target), "--all"], check=True)


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
        }
        lines.append(json.dumps(entry, ensure_ascii=False))
    with logbook.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return len(lines)


def append_decisions_open(target: Path, cards: list[dict], since: str) -> int:
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
    existing_rows = len([ln for ln in table_body.splitlines() if ln.strip().startswith("|")])

    new_rows = []
    for i, card in enumerate(cards):
        n = existing_rows + i + 1
        question = f"Does `{card.get('mechanism', '?')}` (lane {card.get('lane', '?')}) explain the issue?"
        who = "founder" if card.get("legal_relevance") != "NONE" else "AI + founder review"
        new_rows.append(f"| {n} | {question} | UIA phase 13 candidate generation | {who} | {since} |")
    text = text[:insert_at] + "\n".join(new_rows) + "\n" + text[insert_at:]
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
    args = p.parse_args()

    run = json.loads(args.run_json.read_text(encoding="utf-8"))
    kernel = load_kernel(args.uia_repo)
    result = validate_checkpoint(kernel, run)

    hypothesis_portfolio = run["hypothesis_portfolio"]
    cards = hypothesis_portfolio["hypothesis_cards"]
    checkpoint_ref = hypothesis_portfolio.get("checkpoint_certificate", "unknown-checkpoint")
    since = datetime.date.today().isoformat()

    args.target.mkdir(parents=True, exist_ok=True)
    ensure_scaffold(args.doc_eco_repo, args.target)
    n_logged = append_logbook(args.target, checkpoint_ref, cards)
    n_rows = append_decisions_open(args.target, cards, since)

    print(f"OK — {n_logged} hypothesis card(s) logged, {n_rows} row(s) added to DECISIONS.md")
    print(f"  target: {args.target}")
    print(f"  checkpoint state: {result['state']}, claim_boundary: {result['claim_boundary']}")


if __name__ == "__main__":
    main()
