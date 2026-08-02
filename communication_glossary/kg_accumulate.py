#!/usr/bin/env python3
"""Layer 1 extension — cross-checkpoint accumulation of `kg_extract.py`'s word/
phrase graph, scoped to one (principal_id, topic_tag) pair over time.

`kg_extract.py`'s `extract(run)` only ever sees a single checkpoint. This script
merges that single-checkpoint word_index into a persistent, growing graph for a
given person and topic, across as many checkpoints as have been ingested so far.

Design registered in `communication_glossary/README.md` ("Planned — Layer 1
cross-checkpoint accumulation", 2026-08-02) before this script was written; that
entry's reasoning is not repeated here in full.

No new node-ID scheme: `kg_extract.py`'s `mermaid_id(wtype, word)` already hashes
only `(wtype, word)`, never the checkpoint, so the identical (word, type) pair
from two different checkpoints already collides to the same node id today.
Accumulation is therefore a union by `(word, type)` key over each checkpoint's
word_index, extending each node's `sources` list with checkpoint-qualified
labels.

Idempotency: mirrors `doc_ecosystem_bridge/bridge.py`'s `already_ingested()`
pattern -- a checkpoint whose `checkpoint_certificate` is already recorded in
the accumulated state is skipped, not re-merged, on a repeat run.

`registration.principal_id` is NOT read from the checkpoint automatically in
this version -- `--principal-id`/`--topic-tag` are required CLI arguments. This
keeps the script usable today even though no checkpoint in this repo's fixtures
declares that (still-optional, not-yet-added-to-the-kernel-schema) field; wiring
it to read from the checkpoint itself is a follow-up, not done here.

Storage: one JSON state file (the merge source of truth) plus one regenerated
Markdown file (human-readable, same Mermaid-DAG-plus-table shape as
`kg_raw_word.md`) per (principal_id, topic_tag), under
`communication_glossary/accumulated/<principal_id>/<topic_tag>/`.

Usage:
    python3 kg_accumulate.py <checkpoint.json> --principal-id <id> \
        --topic-tag <tag> --accumulated-dir <dir>
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
import kg_extract  # noqa: E402

STATE_FILENAME = "kg_accumulated.json"
MARKDOWN_FILENAME = "kg_accumulated.md"


def state_dir(accumulated_dir: Path, principal_id: str, topic_tag: str) -> Path:
    return accumulated_dir / principal_id / topic_tag


def load_state(accumulated_dir: Path, principal_id: str, topic_tag: str) -> dict:
    path = state_dir(accumulated_dir, principal_id, topic_tag) / STATE_FILENAME
    if not path.exists():
        return {
            "principal_id": principal_id,
            "topic_tag": topic_tag,
            "ingested_checkpoints": [],
            # word_index stored as a list of [word, type, sources] triples --
            # JSON object keys can't be tuples, and this keeps the file diffable.
            "word_index": [],
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {path} is not valid JSON: {e}")


def word_index_from_state(state: dict) -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for word, wtype, sources in state["word_index"]:
        index[(word, wtype)] = {"sources": list(sources)}
    return index


def state_from_word_index(
    principal_id: str, topic_tag: str, ingested: list, word_index: dict
) -> dict:
    return {
        "principal_id": principal_id,
        "topic_tag": topic_tag,
        "ingested_checkpoints": ingested,
        "word_index": [
            [word, wtype, meta["sources"]]
            for (word, wtype), meta in sorted(word_index.items())
        ],
    }


def checkpoint_certificate_of(run: dict) -> str:
    return (run.get("hypothesis_portfolio") or {}).get(
        "checkpoint_certificate", "unknown-checkpoint"
    )


def merge(
    accumulated: dict[tuple[str, str], dict],
    new_index: dict[tuple[str, str], dict],
    checkpoint_certificate: str,
) -> set[tuple[str, str]]:
    """Merges new_index into accumulated in place. Returns the set of
    (word, type) keys that were NOT already present in accumulated before
    this merge -- the mechanical "new vocabulary this checkpoint introduced"
    signal the vocabulary contract (SKILLME.md SS14) needs."""
    newly_seen: set[tuple[str, str]] = set()
    for key, meta in new_index.items():
        if key not in accumulated:
            accumulated[key] = {"sources": []}
            newly_seen.add(key)
        for source in meta["sources"]:
            accumulated[key]["sources"].append(f"{checkpoint_certificate}:{source}")
    return newly_seen


def render_markdown(
    principal_id: str,
    topic_tag: str,
    ingested_checkpoints: list[str],
    word_index: dict[tuple[str, str], dict],
) -> str:
    lines = []
    lines.append(f"# kg_accumulated — {principal_id} / {topic_tag}")
    lines.append("")
    lines.append(
        "**Accumulated readout, not a semantic KG.** Same zero-interpretation "
        "discipline as `kg_raw_word.md` -- every node below is a literal "
        "\"this word appeared in this checkpoint's schema field\" fact, merged "
        "across every checkpoint listed below for this principal and topic. No "
        "relation is invented across checkpoints; merging only unions "
        "identical (word, type) pairs and keeps every source."
    )
    lines.append("")
    lines.append(f"**Checkpoints ingested ({len(ingested_checkpoints)}):**")
    for cert in ingested_checkpoints:
        lines.append(f"- `{cert}`")
    lines.append("")

    words_by_type: dict[str, set[str]] = defaultdict(set)
    for word, wtype in word_index:
        words_by_type[wtype].add(word)

    lines.append("## DAG (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    root_id = kg_extract.safe_node_id("ACCUM", f"{principal_id}/{topic_tag}")
    lines.append(
        f'  {root_id}["{kg_extract.mermaid_escape(principal_id)} / '
        f'{kg_extract.mermaid_escape(topic_tag)}"]'
    )
    for wtype in kg_extract.TYPE_ORDER:
        words = words_by_type.get(wtype)
        if not words:
            continue
        bucket_node = kg_extract.safe_node_id(f"{root_id}_BKT", wtype)
        lines.append(f'  {root_id} --> {bucket_node}["{wtype}"]')
        for w in sorted(words):
            word_node = kg_extract.mermaid_id(wtype, w)
            lines.append(
                f'  {bucket_node} --> {word_node}(["{kg_extract.mermaid_escape(w)}"])'
            )
    lines.append("```")
    lines.append("")

    lines.append("## Word table (deduped, every source kept)")
    lines.append("")
    lines.append("| Type | Word/Phrase | Sources |")
    lines.append("|---|---|---|")
    for (word, wtype), meta in sorted(word_index.items()):
        sources = ", ".join(f"`{s}`" for s in meta["sources"])
        lines.append(
            f"| {wtype} | {kg_extract.md_code_span(word)} | {sources} |"
        )
    lines.append("")

    return "\n".join(lines)


def accumulate(
    checkpoint_path: Path,
    principal_id: str,
    topic_tag: str,
    accumulated_dir: Path,
) -> dict:
    """Returns a summary dict: {skipped, checkpoint_certificate, new_words,
    total_words, state_path, markdown_path}."""
    if not principal_id.strip():
        raise SystemExit("REFUSED: --principal-id must be non-blank")
    if not topic_tag.strip():
        raise SystemExit("REFUSED: --topic-tag must be non-blank")

    try:
        run = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {checkpoint_path} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {checkpoint_path} is not valid JSON: {e}")

    checkpoint_certificate = checkpoint_certificate_of(run)
    state = load_state(accumulated_dir, principal_id, topic_tag)

    if checkpoint_certificate in state["ingested_checkpoints"]:
        return {
            "skipped": True,
            "checkpoint_certificate": checkpoint_certificate,
            "new_words": [],
            "total_words": len(state["word_index"]),
            "state_path": state_dir(accumulated_dir, principal_id, topic_tag)
            / STATE_FILENAME,
            "markdown_path": state_dir(accumulated_dir, principal_id, topic_tag)
            / MARKDOWN_FILENAME,
        }

    accumulated_index = word_index_from_state(state)
    new_index, _card_ids = kg_extract.extract(run)
    newly_seen = merge(accumulated_index, new_index, checkpoint_certificate)

    ingested = state["ingested_checkpoints"] + [checkpoint_certificate]
    updated_state = state_from_word_index(
        principal_id, topic_tag, ingested, accumulated_index
    )

    out_dir = state_dir(accumulated_dir, principal_id, topic_tag)
    out_dir.mkdir(parents=True, exist_ok=True)
    state_path = out_dir / STATE_FILENAME
    markdown_path = out_dir / MARKDOWN_FILENAME
    state_path.write_text(
        json.dumps(updated_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    markdown_path.write_text(
        render_markdown(principal_id, topic_tag, ingested, accumulated_index),
        encoding="utf-8",
    )

    return {
        "skipped": False,
        "checkpoint_certificate": checkpoint_certificate,
        "new_words": sorted(newly_seen),
        "total_words": len(accumulated_index),
        "state_path": state_path,
        "markdown_path": markdown_path,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("checkpoint", type=Path, help="SkillMe checkpoint JSON file")
    p.add_argument("--principal-id", required=True)
    p.add_argument("--topic-tag", required=True)
    p.add_argument(
        "--accumulated-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "accumulated",
        help="root directory for per-(principal,topic) accumulated state "
        "(default: communication_glossary/accumulated/)",
    )
    args = p.parse_args()

    result = accumulate(
        args.checkpoint, args.principal_id, args.topic_tag, args.accumulated_dir
    )
    if result["skipped"]:
        print(
            f"SKIPPED — checkpoint {result['checkpoint_certificate']!r} already "
            f"ingested for this principal/topic. {result['total_words']} words "
            "accumulated so far."
        )
    else:
        print(
            f"wrote {result['state_path']} and {result['markdown_path']} — "
            f"{len(result['new_words'])} new word(s) this checkpoint, "
            f"{result['total_words']} total distinct words accumulated."
        )


if __name__ == "__main__":
    main()
