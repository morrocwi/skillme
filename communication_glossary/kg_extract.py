#!/usr/bin/env python3
"""PROTOTYPE — not committed to any repo yet.

Takes one UIA hypothesis checkpoint (a VALID_CHECKPOINT run record, same shape
`bridge.py` consumes) and emits `kg_raw_word.md`: a typed, deterministic,
fully-traceable word graph — the RAW material for a future knowledge graph, not
a semantic KG itself. No LLM, no NLP guessing, no invented relations — every
node and edge is a literal readout of "this word appeared in this exact
schema field of this exact hypothesis card", nothing more. This is a design
choice, not a limitation to hide: per this workspace's readout-not-truth stance,
inventing semantic edges (e.g. "X causes Y") from free text would be an
interpretive claim this script has no business making. If/when semantic edges
are wanted, that's a deliberate NEXT layer on top of this raw layer, not baked
in here.

Structure emitted is a DAG (a tree, in fact — trivially acyclic):

    checkpoint
      -> hypothesis card (H1, H2, H3, ...)
        -> type bucket (ROLE / CONCEPT / PROCESS / METRIC)
          -> word node (deduped, but keeps every source it came from)
      -> checkpoint-level type bucket (ROLE / TOOL / PROTOCOL / METRIC)
        -> word node

v0.2 (2026-08-01): each source field is now extracted in one of two modes,
chosen per-field, not guessed per-value:
  - "phrase" — the field is a list of short, name-like items (role names, tool
    names, protocol/method names). Kept as a WHOLE node each, not split into
    words — splitting "controls engineering lead" into `controls`/`engineering`
    /`lead` (v0.1's behavior) destroyed the name. This is what a v0.1 real run
    against both fixtures actually showed: "product owner" -> `product`+`owner`,
    "controls engineering lead" -> 3 separate generic words. Confirmed bug, not
    a hypothetical one.
  - "tokenize" — the field is free narrative text (a claim, a mechanism, a
    falsifier). Split into words as before; this is where "every word" genuinely
    means individual words, because the field IS prose, not a name list.

Known, stated limitation (Open, not solved here): "tokenize" mode is a plain
whitespace/punctuation split. This works for English and for informally-spaced
Thai, but NOT for unspaced formal Thai/Lao/Khmer running text — that needs a
real segmenter (e.g. pythainlp), which is out of scope for a stdlib-only
prototype. Confirmed against the v0.1 booking-fixture run: `registration.
success_rule`'s Thai clause came out as one oversized "word"
(`ต่ำกว่าเกณฑ์ที่`) instead of being segmented. Flagged, not hidden, not fixed
here — "phrase" mode sidesteps this for name-list fields, but any "tokenize"
field with unspaced Thai/CJK content still has this open limitation.

v0.3 (2026-08-01) — fixed 4 issues found by a 5-domain harsh-content ultracode
stress test (real checkpoints with embedded quotes/brackets/pipes/digits/
punctuation-heavy names, run through this script for real, output inspected as
a domain expert — see that run's synthesis report for full evidence):
  1. CRITICAL — Mermaid label injection (5/5 domains). See `mermaid_escape()`.
  2. MINOR — `WORD_RE` silently dropped digits/codes embedded in tokenize-mode
     text (asset ids like `GB-04A` -> `GB`, decline codes like `06` gone
     entirely, with no trace). Now includes `0-9` in the character class.
     Tradeoff, stated not hidden: bare numeric quantities (dates, counts) will
     now also surface as "words" — accepted, the alternative was silently
     losing meaningful identifiers.
  3. MINOR — `system_graph.nodes` is hard-mapped to TOOL regardless of content;
     an entity that's also a genuine ROLE elsewhere (e.g. "customer") was filed
     under both types for the same underlying entity. Now merged: an exact-
     phrase match already filed as ROLE absorbs the TOOL occurrence instead of
     duplicating the entity across two type buckets.
  4. MINOR — `hypothesis_evidence_challenge.hypotheses[*].citation_cards[*].
     title` was not covered by any field-mode mapping, so citation-title
     content (a natural place for the unicode/emoji stress case) was silently
     never extracted, not mis-extracted. Now included as CONCEPT/tokenize,
     sourced per the citation's own `hypothesis_id`.

Usage:
    python3 kg_extract.py <uia_checkpoint.json> <out_kg_raw_word.md>
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# Minimal, intentionally small stopword list — English only for now (see the
# Thai-tokenization limitation above). Extend deliberately, don't silently grow.
STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are",
    "be", "this", "that", "these", "those", "with", "by", "at", "from", "not",
    "no", "it", "its", "as", "than", "then", "so", "if", "but", "into", "onto",
    "over", "under", "per", "via", "vs", "which", "who", "whom", "what", "when",
}

WORD_RE = re.compile(r"[A-Za-zก-๙0-9]+(?:[-_][A-Za-zก-๙0-9]+)*")


def md_code_span(text: str) -> str:
    """Wrap `text` in a Markdown inline code span that's safe even if `text`
    itself contains backticks — uses a longer backtick fence than the longest
    backtick run inside the content (the standard CommonMark technique), with
    a padding space if the content starts/ends with a backtick.

    v0.4 fix: the word table previously used a fixed single-backtick fence
    (f"| `{word}` | ..."). A harsh word containing a literal backtick would
    terminate that code span early, silently misaligning or dropping table
    columns for that row — the same failure class as the Mermaid-label
    injection bug fixed in v0.3, just in the word-table section instead of
    the Mermaid section. Confirmed real by a full-pipeline ultracode review."""
    text = str(text)
    runs = re.findall(r"`+", text)
    fence = "`" * (max((len(r) for r in runs), default=0) + 1)
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def mermaid_escape(text: str) -> str:
    """Neutralize characters that break Mermaid label/shape-delimiter syntax.
    v0.3 (2026-08-01) — CRITICAL bug found by a 5-domain harsh-content stress
    test: phrase-mode text (role/tool/protocol names) was interpolated raw into
    `(["..."])` labels. A literal `"` in the source text (e.g. a role name like
    `Front-Desk "Triage" Lead`) unbalances the quoted string and corrupts the
    Mermaid node; `[`/`]` additionally collide with Mermaid's own shape
    delimiters. Confirmed broken in 5/5 domains before this fix. Uses Mermaid's
    HTML-entity label escaping (works inside quoted labels) rather than
    backslash-escaping, which Mermaid does not reliably support in this
    position. Applied to every label — phrase-mode AND tokenize-mode AND the
    checkpoint/card/type-bucket labels — even though tokenize-mode words are
    already regex-filtered to safe characters, so a future field/mode change
    can't silently reopen this hole."""
    return (
        str(text)
        .replace("&", "#amp;")  # must come first, or it would double-escape the entities below
        .replace('"', "#quot;")
        .replace("[", "#91;")
        .replace("]", "#93;")
    )


def tokenize(text) -> list[str]:
    if not text:
        return []
    words = WORD_RE.findall(str(text))
    return [w for w in words if w.lower() not in STOPWORDS and len(w) > 1]


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_phrase(value) -> str | None:
    # v0.4 fix: None must stay None, not become the literal string "None" — a
    # fabricated node contradicts this script's own no-invented-content promise.
    # Confirmed real by a full-pipeline ultracode review: as_list(None) can
    # legitimately reach here for a list field containing a null entry.
    if value is None:
        return None
    text = " ".join(str(value).split())  # collapse internal whitespace, keep as one node
    return text or None


# field -> (type, mode), per hypothesis card (source = the card itself)
# mode "tokenize": free narrative text, split into words.
# mode "phrase": a list of name-like items, kept whole (not split).
CARD_FIELD_MODES = {
    "claim": ("CONCEPT", "tokenize"),
    "alternative_explanations": ("CONCEPT", "tokenize"),
    "mechanism": ("PROCESS", "tokenize"),
    "predicted_readout": ("PROCESS", "tokenize"),
    "falsifier": ("METRIC", "tokenize"),
    "discriminating_information": ("METRIC", "tokenize"),
    "affected_agencies": ("ROLE", "phrase"),
}

# (object, field) -> (type, mode), checkpoint-level (source = the checkpoint, not one card)
CHECKPOINT_FIELD_MODES = {
    ("agency", "accountable_parties"): ("ROLE", "phrase"),
    ("agency", "decision_owners"): ("ROLE", "phrase"),
    ("agency", "affected"): ("ROLE", "phrase"),
    ("agency", "voice_holders"): ("ROLE", "phrase"),
    ("system_graph", "nodes"): ("TOOL", "phrase"),
    ("system_graph", "edges"): ("PROCESS", "phrase"),
    ("registration", "success_rule"): ("METRIC", "tokenize"),
    ("registration", "failure_rule"): ("METRIC", "tokenize"),
    ("translation", "adapter_cards"): ("PROTOCOL", "phrase"),
    ("causal_analysis", "controls"): ("PROTOCOL", "phrase"),
}


def extract(run: dict) -> tuple[dict, list]:
    """Returns (word_index, card_ids).
    word_index: {(word, type): {"sources": [source_label, ...]}}
    """
    word_index: dict[tuple[str, str], dict] = defaultdict(lambda: {"sources": []})
    portfolio = run.get("hypothesis_portfolio") or {}
    cards = portfolio.get("hypothesis_cards") or []
    card_ids = []

    for card in cards:
        cid = card.get("hypothesis_id", "?")
        card_ids.append(cid)
        # lane + causal_tier are single controlled-vocabulary values -> PROTOCOL, phrase (already atomic)
        for field, wtype in (("lane", "PROTOCOL"), ("causal_tier", "PROTOCOL")):
            value = card.get(field)
            if value:
                word_index[(str(value), wtype)]["sources"].append(f"{cid}:{field}")
        for field, (wtype, mode) in CARD_FIELD_MODES.items():
            for value in as_list(card.get(field)):
                if mode == "phrase":
                    phrase = as_phrase(value)
                    if phrase:
                        word_index[(phrase, wtype)]["sources"].append(f"{cid}:{field}")
                else:
                    for w in tokenize(value):
                        word_index[(w, wtype)]["sources"].append(f"{cid}:{field}")

    evidence = run.get("hypothesis_evidence_challenge") or {}
    review_mode = evidence.get("review_mode")
    if review_mode:
        word_index[(str(review_mode), "PROTOCOL")]["sources"].append("checkpoint:review_mode")

    for (obj_key, field), (wtype, mode) in CHECKPOINT_FIELD_MODES.items():
        obj = run.get(obj_key) or {}
        for value in as_list(obj.get(field)):
            if mode == "phrase":
                phrase = as_phrase(value)
                if phrase:
                    word_index[(phrase, wtype)]["sources"].append(f"checkpoint:{obj_key}.{field}")
            else:
                for w in tokenize(value):
                    word_index[(w, wtype)]["sources"].append(f"checkpoint:{obj_key}.{field}")

    for h in (evidence.get("hypotheses") or []):
        hid = h.get("hypothesis_id", "?")
        for citation in (h.get("citation_cards") or []):
            title = citation.get("title")
            for w in tokenize(title):
                word_index[(w, "CONCEPT")]["sources"].append(f"{hid}:citation_cards.title")

    # v0.3: system_graph.nodes is hard-mapped to TOOL regardless of content, but
    # the identical phrase can also be a genuine ROLE from a real role-source
    # field (e.g. "customer" in both agency.affected and system_graph.nodes).
    # Confirmed in the customer-support harsh-content run: "customer" got filed
    # as both W_ROLE_customer and W_TOOL_customer for the same entity. A role
    # designation from an actual role field is more specific than "this name
    # also appears as a graph node", so merge TOOL into ROLE when both exist for
    # the exact same phrase, keeping the TOOL occurrences as provenance under
    # the ROLE entry rather than filing the entity under two types.
    for key in list(word_index.keys()):
        word, wtype = key
        if wtype == "TOOL" and (word, "ROLE") in word_index:
            word_index[(word, "ROLE")]["sources"].extend(word_index[key]["sources"])
            del word_index[key]

    return word_index, card_ids


TYPE_ORDER = ["ROLE", "CONCEPT", "PROCESS", "TOOL", "PROTOCOL", "METRIC"]


def safe_node_id(prefix: str, text: str) -> str:
    """Stable, collision-safe Mermaid node id for ANY text, not just words.
    Plain ASCII sanitization alone can collide (e.g. two different Thai
    phrases both becoming all-underscore) or break Mermaid syntax outright
    (unsanitized text used directly as a node-id token), so a short content
    hash is always appended — the id need not be human-readable, the visible
    label (in the node's ["..."] text) is what a reader sees.

    v0.4 fix: this used to be `mermaid_id(wtype, word)`, applied only to word
    nodes — card/bucket nodes used a raw, unsanitized f"CARD_{cid}" instead.
    Confirmed real by a full-pipeline ultracode review: a harsh hypothesis_id
    (spaces, punctuation, or one id that's a prefix of another, e.g. "H1" vs
    "H1_ROLE") could break Mermaid node-id syntax or silently merge two
    distinct subtrees into one. Every node id in this file now goes through
    this one function."""
    safe = re.sub(r"[^A-Za-z0-9_]", "_", str(text))[:40]
    digest = hashlib.md5(str(text).encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{safe}_{digest}"


def mermaid_id(wtype: str, word: str) -> str:
    return safe_node_id(f"W_{wtype}", word)


def render_markdown(run: dict, word_index: dict, card_ids: list) -> str:
    checkpoint_ref = (run.get("hypothesis_portfolio") or {}).get(
        "checkpoint_certificate", "unknown-checkpoint"
    )
    lines = []
    lines.append(f"# kg_raw_word — {checkpoint_ref}")
    lines.append("")
    lines.append(
        "**PROTOTYPE output.** Raw, typed, fully-traceable word extraction — not a "
        "semantic KG yet. No relation was invented; every edge below reflects only "
        "\"this word literally appeared in this schema field of this source.\" "
        "See the script docstring for the stated tokenization limitation "
        "(unspaced formal Thai/CJK under-tokenizes)."
    )
    lines.append("")

    # per-card word buckets, grouped by type
    per_card_words: dict[str, dict[str, set]] = {cid: defaultdict(set) for cid in card_ids}
    checkpoint_words: dict[str, set] = defaultdict(set)
    for (word, wtype), meta in word_index.items():
        for source in meta["sources"]:
            if source.startswith("checkpoint:"):
                checkpoint_words[wtype].add(word)
            else:
                cid = source.split(":", 1)[0]
                if cid in per_card_words:
                    per_card_words[cid][wtype].add(word)

    # --- Mermaid DAG: checkpoint -> card -> type bucket -> word ---
    lines.append("## DAG (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    root_id = "CKPT"
    lines.append(f'  {root_id}["{mermaid_escape(checkpoint_ref)}"]')
    for cid in card_ids:
        card_node = safe_node_id("CARD", cid)
        lines.append(f'  {root_id} --> {card_node}["{mermaid_escape(cid)}"]')
        for wtype in TYPE_ORDER:
            words = per_card_words[cid].get(wtype)
            if not words:
                continue
            bucket_node = safe_node_id(f"{card_node}_BKT", wtype)
            lines.append(f'  {card_node} --> {bucket_node}["{wtype}"]')
            for w in sorted(words):
                word_node = mermaid_id(wtype, w)
                lines.append(f'  {bucket_node} --> {word_node}(["{mermaid_escape(w)}"])')
    for wtype in TYPE_ORDER:
        words = checkpoint_words.get(wtype)
        if not words:
            continue
        bucket_node = safe_node_id(f"{root_id}_BKT", wtype)
        lines.append(f'  {root_id} --> {bucket_node}["{wtype} (checkpoint-level)"]')
        for w in sorted(words):
            word_node = mermaid_id(wtype, w)
            lines.append(f'  {bucket_node} --> {word_node}(["{mermaid_escape(w)}"])')
    lines.append("```")
    lines.append("")

    # --- full word table, deduped, with every source ---
    lines.append("## Word table (deduped, every source kept)")
    lines.append("")
    lines.append("| word | type | occurrences | sources |")
    lines.append("|---|---|---|---|")
    for (word, wtype), meta in sorted(word_index.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        sources = sorted(set(meta["sources"]))
        lines.append(f"| {md_code_span(word)} | {wtype} | {len(meta['sources'])} | {', '.join(sources)} |")
    lines.append("")

    # --- summary stats ---
    lines.append("## Summary")
    lines.append("")
    by_type_count = defaultdict(set)
    for (word, wtype) in word_index:
        by_type_count[wtype].add(word)
    lines.append(f"- hypothesis cards: {len(card_ids)}")
    lines.append(f"- total distinct words: {len(word_index)}")
    for wtype in TYPE_ORDER:
        lines.append(f"- {wtype}: {len(by_type_count.get(wtype, set()))} distinct words")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <uia_checkpoint.json> <out_kg_raw_word.md>", file=sys.stderr)
        raise SystemExit(2)
    run = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    word_index, card_ids = extract(run)
    md = render_markdown(run, word_index, card_ids)
    Path(sys.argv[2]).write_text(md, encoding="utf-8")
    print(f"wrote {sys.argv[2]} — {len(word_index)} distinct words across {len(card_ids)} cards")


if __name__ == "__main__":
    main()
