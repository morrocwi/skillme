#!/usr/bin/env python3
"""PROTOTYPE — not committed to any repo yet.

Layer 3: a communication glossary tied to ONE ISSUE/DOMAIN, not to any single
stakeholder role. Founder's own correction (2026-08-01, verbatim intent): "ไม่ใช่
เอาทางใดทางหนึ่งคือต้องผูกกับ issue และโดเมน ไม่ใช่ agency ใด agency หนึ่ง" — the
glossary must be anchored to the issue itself so that ANYONE joining the
conversation (an engineer, a nurse, an ops manager — whoever) gets the same
shared vocabulary, not a vocabulary filtered through what one particular role
already knows or doesn't know.

Merges the two existing layers per domain, purely mechanically (no new LLM
calls, no new WebSearch — this reuses what Layer 1 and Layer 2 already
produced and verified):
  - Layer 1 (kg_raw_word_<domain>_v3.md) — deterministic readout: every term
    literally appeared in the checkpoint's own schema fields.
  - Layer 2 (kg_expert_layer_<domain>.md) — AI-interpretive, Open tier: named
    frameworks/methodologies a world-class expert would bring, verified where
    marked VERIFIED-VIA-SEARCH.

One deliberate curation choice, stated not hidden: SkillMe-protocol-internal
vocabulary (lane names like KNOWN_DIRECT, causal_tier names like
MECHANISM_HYPOTHESIS, review_mode like TARGETED_SEARCH) is EXCLUDED from the
domain-vocabulary section and listed separately — these are machinery of the
SkillMe analysis method itself, not vocabulary either an engineer or a nurse needs
to discuss gut health. Detected mechanically: any Layer-1 entry whose every
source ends in ":lane", ":causal_tier", or is exactly "checkpoint:review_mode".

Usage:
    python3 build_glossary.py <raw_word_md> <expert_layer_md> <out_glossary_md>
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# v0.2 fix: kg_extract.py v0.4 switched the word column from a fixed single
# backtick fence to a CommonMark-style variable-length fence (md_code_span())
# so a word containing a literal backtick doesn't break the code span. This
# regex must match that: capture the fence (one or more backticks), then any
# content up to that SAME fence again (backreference), with an optional single
# padding space kg_extract.py adds when content starts/ends with a backtick.
ROW_RE = re.compile(
    r"^\|\s*(`+)\s?(.*?)\s?\1\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|$", re.M
)
PROTOCOL_INTERNAL_SUFFIXES = (":lane", ":causal_tier")


def parse_raw_word_table(md_text: str) -> list[tuple[str, str, int, list[str]]]:
    rows = []
    for m in ROW_RE.finditer(md_text):
        _fence, word, wtype, count, sources_str = m.groups()
        sources = [s.strip() for s in sources_str.split(",")]
        rows.append((word, wtype, int(count), sources))
    return rows


def is_protocol_internal(sources: list[str]) -> bool:
    return all(
        s.endswith(PROTOCOL_INTERNAL_SUFFIXES) or s == "checkpoint:review_mode"
        for s in sources
    )


def parse_expert_layer(md_text: str) -> dict:
    def section(name: str) -> str:
        m = re.search(
            rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", md_text, re.M | re.S
        )
        return m.group(1).strip() if m else ""

    title_m = re.search(r"^# kg_expert_layer — (.+?) \(AI-INTERPRETIVE", md_text, re.M)
    title = title_m.group(1) if title_m else "unknown-checkpoint"

    frameworks_block = section("Relevant frameworks/methodologies per domain")
    # Bullets are Markdown paragraphs: "- **Name.** reasoning... Confidence: X."
    # often wrapped across multiple lines, with a bare "**Domain Heading**" line
    # between groups. Reassemble each bullet into one string before checking its
    # confidence tag — a naive line-by-line scan misses tags on continuation lines.
    bullets: list[str] = []
    current: str | None = None
    for raw_line in frameworks_block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        is_bare_heading = line.startswith("**") and line.endswith("**") and not line.startswith("- ")
        if line.startswith("- "):
            if current:
                bullets.append(current)
            current = line[2:]
        elif is_bare_heading:
            if current:
                bullets.append(current)
                current = None
        elif current is not None:
            current += " " + line
    if current:
        bullets.append(current)

    # pull only bullets that carry a confidence tag we trust for a glossary: HIGH
    # or VERIFIED-VIA-SEARCH (skip MEDIUM/uncertain ones here on purpose — a
    # communication glossary should lead with what's actually solid).
    strong_frameworks = [
        b for b in bullets
        if "VERIFIED-VIA-SEARCH" in b or "Confidence: HIGH" in b
    ]

    vocab_added = section("Vocabulary this adds beyond kg_raw_word.md's raw extraction")
    domains = section("Domain(s) identified")

    return {
        "title": title,
        "domains": domains,
        "strong_frameworks": strong_frameworks,
        "vocab_added": vocab_added,
    }


TYPE_LABEL_TH = {
    "ROLE": "ผู้เกี่ยวข้อง (ROLE)",
    "CONCEPT": "แนวคิด/สภาวะของปัญหา (CONCEPT)",
    "PROCESS": "กลไก/กระบวนการ (PROCESS)",
    "TOOL": "เครื่องมือ/ระบบ (TOOL)",
    "PROTOCOL": "วิธีวิเคราะห์/มาตรฐานที่อ้างถึง (PROTOCOL)",
    "METRIC": "ตัวชี้วัด/เงื่อนไขพิสูจน์ (METRIC)",
}
TYPE_ORDER = ["ROLE", "CONCEPT", "PROCESS", "TOOL", "PROTOCOL", "METRIC"]


def build(raw_md: str, expert_md: str) -> str:
    rows = parse_raw_word_table(raw_md)
    expert = parse_expert_layer(expert_md)

    domain_terms: dict[str, list[tuple[str, int]]] = defaultdict(list)
    protocol_internal_terms: list[str] = []
    for word, wtype, count, sources in rows:
        if wtype == "PROTOCOL" and is_protocol_internal(sources):
            protocol_internal_terms.append(word)
            continue
        domain_terms[wtype].append((word, count))

    lines = []
    lines.append(f"# Communication Glossary — {expert['title']}")
    lines.append("")
    lines.append(
        "**คำศัพท์นี้ผูกกับตัว *ประเด็น/โดเมน* ไม่ได้ผูกกับ role ใด role หนึ่ง** — "
        "ใครก็ตามที่เข้าร่วมคุยเรื่องนี้ (วิศวกร, พยาบาล, ผู้จัดการฝ่ายปฏิบัติการ, "
        "หรือใครก็ตาม) ต้องรู้คำชุดเดียวกันนี้ ไม่ว่าพื้นเดิมของแต่ละคนจะเป็นสายไหน "
        "รวมจาก 2 ชั้นที่มีอยู่แล้ว: ชั้น 1 (deterministic readout จาก checkpoint จริง) "
        "+ ชั้น 2 (AI-interpretive framework/องค์ความรู้ Open tier, เฉพาะที่ confidence "
        "HIGH หรือ VERIFIED-VIA-SEARCH เท่านั้น — ตัดรายการที่ยังไม่มั่นใจออกเพื่อไม่ให้ "
        "glossary นี้ชวนเข้าใจผิดว่าทุกคำแน่นอนเท่ากันหมด)."
    )
    lines.append("")

    lines.append("## 1. คำศัพท์แกนของประเด็นนี้ (readout จาก checkpoint จริง)")
    lines.append("")
    for wtype in TYPE_ORDER:
        terms = sorted(domain_terms.get(wtype, []), key=lambda t: (-t[1], t[0]))
        if not terms:
            continue
        lines.append(f"**{TYPE_LABEL_TH[wtype]}:**")
        lines.append(", ".join(f"`{w}`" for w, _ in terms))
        lines.append("")

    lines.append("## 2. องค์ความรู้ผู้เชี่ยวชาญที่ควรรู้เพิ่ม (AI-interpretive, Open tier — เฉพาะที่มั่นใจสูง)")
    lines.append("")
    if expert["strong_frameworks"]:
        for fw in expert["strong_frameworks"]:
            lines.append(f"- {fw}")
    else:
        lines.append("_(ไม่มีรายการที่ผ่านเกณฑ์ HIGH/VERIFIED-VIA-SEARCH ในรอบนี้)_")
    lines.append("")

    lines.append("## 3. คำที่ชั้น 2 เพิ่มเข้ามาจริง (ไม่ซ้ำกับคำดิบในชั้น 1)")
    lines.append("")
    lines.append(expert["vocab_added"] or "_(ไม่มีข้อมูล)_")
    lines.append("")

    if protocol_internal_terms:
        lines.append("## ภาคผนวก: คำเฉพาะของกลไกโปรโตคอล SkillMe เอง (ไม่ใช่คำศัพท์ของประเด็น — ตัดออกจาก glossary หลักโดยตั้งใจ)")
        lines.append("")
        lines.append(", ".join(f"`{w}`" for w in sorted(set(protocol_internal_terms))))
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} <raw_word_md> <expert_layer_md> <out_glossary_md>", file=sys.stderr)
        raise SystemExit(2)
    raw_md = Path(sys.argv[1]).read_text(encoding="utf-8")
    expert_md = Path(sys.argv[2]).read_text(encoding="utf-8")
    out = build(raw_md, expert_md)
    Path(sys.argv[3]).write_text(out, encoding="utf-8")
    print(f"wrote {sys.argv[3]}")


if __name__ == "__main__":
    main()
