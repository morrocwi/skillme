#!/usr/bin/env python3
"""Layer 4 — skill_plan.md: who needs to know/do what to actually work this
checkpoint, split into 4 roles: **Human**, **AI-orchestrator**, **AI-doer**,
**AI-auditor**. Founder's own framing (2026-08-01): the human side must state
what vocabulary is needed to command the AI, what to check/verify to actually
solve the issue per this hypothesis, and what skills are needed to command the
work successfully; the three AI roles each need their own skill list.

Tier: `Dr` (declared recommendation), same as Layer 2 — this is a judgment
call about what's needed, not a proven-optimal staffing plan. It is mechanical
where the source data allows (Human's "what to check" comes straight from the
checkpoint's own falsifier/discriminating_information/uncertainties fields —
already-validated, not invented) and declared/curated where it can't be
(the AI role skill lists reference real skills installed in this workspace,
chosen by reasoned mapping to what each role actually does in §6.9.1's
domain-mapping discipline and the maker-checker pattern this repo's own PRs
were built with — not benchmarked against alternatives).

Inputs:
  - <checkpoint.json>  — the real UIA run record (Layer 0)
  - <glossary.md>       — Layer 3's issue-anchored vocabulary (for Human's
                          "what vocabulary" section — referenced, not copied)
  - <kg_expert_layer.md> — Layer 2's Open-questions section, if useful context

Usage:
    python3 skill_plan.py <checkpoint.json> <glossary.md> <kg_expert_layer.md> <out_skill_plan.md>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def extract_human_checks(run: dict) -> list[dict]:
    """One check-item per hypothesis card, straight from already-validated
    schema fields — nothing invented. This IS the checklist a human needs to
    verify before trusting the AI's output on this checkpoint, because these
    are exactly the fields the protocol itself uses to keep a hypothesis
    falsifiable (Invariant list §11, items ~39-41)."""
    cards = ((run.get("hypothesis_portfolio") or {}).get("hypothesis_cards")) or []
    checks = []
    for card in cards:
        checks.append(
            {
                "hypothesis_id": card.get("hypothesis_id", "?"),
                "lane": card.get("lane", "?"),
                "claim": card.get("claim", "?"),
                "falsifier": card.get("falsifier", "?"),
                "discriminating_information": as_list(card.get("discriminating_information")),
                "uncertainties": as_list(card.get("uncertainties")),
                "alternative_explanations": as_list(card.get("alternative_explanations")),
            }
        )
    return checks


def extract_open_questions(expert_md: str) -> str:
    m = re.search(
        r"^## Open questions / where a human expert should override this\n(.*?)(?=^## |\Z)",
        expert_md,
        re.M | re.S,
    )
    return m.group(1).strip() if m else ""


def extract_glossary_title(glossary_md: str) -> str:
    m = re.search(r"^# Communication Glossary — (.+)$", glossary_md, re.M)
    return m.group(1) if m else "unknown-checkpoint"


REVIEW_MODE_NOTE = {
    "TARGETED_SEARCH": (
        "review_mode = TARGETED_SEARCH — evidence for this checkpoint is literature/published "
        "sources; the doer needs real WebSearch discipline (verify claims, don't assert from "
        "training knowledge alone), the auditor needs to spot-check source links actually "
        "support the claim, not just exist."
    ),
    "INTERNAL_DATA_AUDIT": (
        "review_mode = INTERNAL_DATA_AUDIT — evidence is internal system-of-record data (logs, "
        "tickets, sensor exports); the doer needs access-appropriate query discipline over "
        "those systems (not literature search), the auditor needs to confirm the cited "
        "system/query/record actually exists and says what's claimed."
    ),
    "FIELD_OBSERVATION_LOG": (
        "review_mode = FIELD_OBSERVATION_LOG — evidence is a fresh sensory/field observation "
        "(dough, a tagged tree, a session note); the doer needs domain-specific observational "
        "rigor (not a literature or system-log skill), the auditor needs to confirm the "
        "observer/method/location are named specifically enough to be checkable, not vague."
    ),
}


def build(run: dict, glossary_md: str, expert_md: str) -> str:
    checkpoint_ref = (run.get("hypothesis_portfolio") or {}).get(
        "checkpoint_certificate", "unknown-checkpoint"
    )
    glossary_title = extract_glossary_title(glossary_md)
    checks = extract_human_checks(run)
    open_questions = extract_open_questions(expert_md)
    decision_owners = (run.get("agency", {}) or {}).get("decision_owners") or []
    review_mode = (run.get("hypothesis_evidence_challenge") or {}).get("review_mode", "TARGETED_SEARCH")
    review_note = REVIEW_MODE_NOTE.get(review_mode, REVIEW_MODE_NOTE["TARGETED_SEARCH"])

    lines: list[str] = []
    lines.append(f"# Skill Plan — {checkpoint_ref}")
    lines.append("")
    lines.append(
        "**Tier: `Dr`** (declared recommendation, same as Layer 2 — a judgment call, not a "
        "proven-optimal staffing plan). Who needs to know/do what to actually work this "
        "checkpoint, split into 4 roles. The Human section's \"what to check\" is mechanical "
        "(pulled straight from this checkpoint's own already-validated `falsifier`/"
        "`discriminating_information`/`uncertainties` fields, per §11 invariants ~39-41 — "
        "nothing invented). The AI role sections are curated: real skills installed in this "
        "workspace, mapped to what each role actually does, not benchmarked against "
        "alternatives — treat as a starting point to confirm or correct, same discipline as "
        "Layer 2's expert-framework suggestions."
    )
    lines.append("")

    # --- 1. Human ---
    lines.append("## 1. Human")
    lines.append("")
    lines.append(
        f"**คำศัพท์ที่ต้องรู้เพื่อสั่งงาน AI** — ดูที่ `{glossary_title}`'s "
        "communication glossary (Section 1-2) ทั้งหมด — ผูกกับ *ประเด็นนี้โดยเฉพาะ* "
        "ไม่ใช่รายการทั่วไป: ต้องรู้คำศัพท์แกน (raw vocabulary จาก checkpoint จริง) "
        "บวกกับ framework ผู้เชี่ยวชาญที่ verified แล้ว (ถ้ามี) ก่อนจะสั่งงาน AI ให้ทำอะไรต่อได้อย่างแม่นยำ"
    )
    lines.append("")
    if decision_owners:
        lines.append(f"**ผู้มีอำนาจตัดสินใจตาม checkpoint นี้:** {', '.join(decision_owners)}")
        lines.append("")
    lines.append(
        "**สิ่งที่ต้องตรวจ/verify ก่อนเชื่อผลลัพธ์ AI** (ดึงจาก field จริงที่ kernel validate แล้ว "
        "ต่อ hypothesis card — ไม่ใช่รายการทั่วไป):"
    )
    lines.append("")
    for c in checks:
        lines.append(
            f"- **`{c['hypothesis_id']}`** ({c['lane']}) — claim: {c['claim']}"
        )
        lines.append(f"  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: {c['falsifier']}")
        if c["discriminating_information"]:
            lines.append(
                "  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: "
                + "; ".join(c["discriminating_information"])
            )
        if c["uncertainties"]:
            lines.append("  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): " + "; ".join(c["uncertainties"]))
        if c["alternative_explanations"]:
            lines.append(
                "  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: "
                + "; ".join(c["alternative_explanations"])
            )
    lines.append("")
    if open_questions:
        lines.append("**คำถามเปิดจาก Layer 2 ที่ human ต้อง override/ตัดสินเอง (AI ตอบไม่ได้):**")
        lines.append("")
        lines.append(open_questions)
        lines.append("")
    lines.append(
        "**สกิลที่ต้องมีเพื่อสั่งงานสำเร็จ** (ทั่วไป ไม่ผูกกับ checkpoint นี้โดยเฉพาะ แต่จำเป็นเสมอ):"
    )
    lines.append("")
    lines.append(
        "- อ่าน tier ออก: `Th_coqc` (พิสูจน์แล้ว) ≠ `finite_diagnostic` (วัด/รันจริง) ≠ `Dr` "
        "(narrative ที่มนุษย์ประกาศ) ≠ `Open` (ยังไม่รู้) — ต้องรู้ว่า output จาก AI ชิ้นไหนอยู่ tier ไหน"
    )
    lines.append(
        "- รู้ว่า `VALID_CHECKPOINT` **ไม่ใช่** decision/intervention/field-confirmation/success/"
        "closure (Invariant #46) — ห้ามสั่งงานต่อราวกับว่า checkpoint นี้ตัดสินใจแทนได้แล้ว"
    )
    lines.append(
        "- รู้วิธีขอ maker-checker: ทุกงานที่ AI ผลิตแล้วจะ merge/ship/ตัดสินใจต่อ ต้องมี independent "
        "check ก่อนเสมอ (คนละ context/agent จากคนที่ผลิต) — อย่าเชื่อ AI ที่ตรวจงานตัวเอง"
    )
    lines.append(
        "- อ่าน glossary.md Section 3 (\"คำที่ชั้น 2 เพิ่มเข้ามาจริง\") เพื่อรู้ว่าคำไหนเป็นการตีความของ AI "
        "(Open tier) ไม่ใช่ข้อเท็จจริงจาก checkpoint (readout)"
    )
    lines.append("")

    # --- 2/3/4. AI roles ---
    lines.append("## 2. AI-orchestrator")
    lines.append("")
    lines.append(
        "หน้าที่: แตกงานเป็นขั้นตอนตาม §6.9.1's domain-mapping discipline, สั่งงาน AI-doer, "
        "เรียก AI-auditor ก่อน merge/ship ทุกครั้ง (maker-checker firewall, Axiom A10), "
        "และห้ามให้ผลของ auditor ไหลย้อนกลับเข้า doer ก่อน freeze (Invariant #7)"
    )
    lines.append("")
    lines.append("**สกิลที่ควรติดตั้ง (จาก skill จริงใน workspace นี้):**")
    lines.append("")
    lines.append("- `project-onboard` — ก่อนเริ่มงานใน repo ใดๆ ที่ยังไม่เคย onboard")
    lines.append("- `subteam-structure` — โครงทีมย่อยมาตรฐาน (orchestrator + system + design + coding)")
    lines.append(
        "- `maker-checker-gate` — รู้ว่า artifact ระดับไหนต้องการ independent check "
        "ก่อน release/merge/ship (นี่คือกฎที่บังคับ AI-auditor ให้มีอยู่จริง ไม่ใช่ optional)"
    )
    lines.append("- `grr-epistemic-foundation` — โครงสร้าง Claim/Evidence/Warrant/Status สำหรับ finding ที่ไม่ใช่ Coq theorem")
    lines.append("")

    lines.append("## 3. AI-doer")
    lines.append("")
    lines.append(
        "หน้าที่: สร้าง/แก้ checkpoint จริง, รัน kg_extract.py/build_glossary.py, ทำ Layer 2 "
        "reasoning (WebSearch-verified), เขียนโค้ด — งานที่ AI-auditor จะมาตรวจทีหลัง"
    )
    lines.append("")
    lines.append("**สกิลที่ควรติดตั้ง:**")
    lines.append("")
    lines.append(
        "- `information-discrete-math` — บังคับโหลดก่อนแตะคณิตศาสตร์/ฟิสิกส์ใดๆ "
        "(มุม/ระยะทาง/อนันต์/ศูนย์) ตาม §6.9.2's contaminated-concept guard"
    )
    lines.append(
        "- `toon-format` — บังคับโหลดก่อนส่งข้อมูลมีโครงสร้าง (JSON/ตาราง) เข้า prompt LLM ใดๆ"
    )
    lines.append("- `rigorous-diagnosis` — วินัยการวินิจฉัย/debug ก่อนสรุป root cause หรือบอกว่า \"แก้แล้ว\"")
    lines.append(f"- `doc-ecosystem` — ถ้างานนี้ต้องส่งต่อเข้า doc-ecosystem project (bridge.py's target)")
    lines.append("")
    lines.append(f"**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** {review_note}")
    lines.append("")

    lines.append("## 4. AI-auditor")
    lines.append("")
    lines.append(
        "หน้าที่: ตรวจ output ของ AI-doer แบบ **อิสระ** (fresh context, ไม่ใช่ agent เดียวกับที่ผลิตงาน) "
        "ก่อน orchestrator จะ merge/ship อะไรก็ตาม — ตรงกับ pattern ที่ session นี้ใช้จริงทุก PR "
        "(spawn independent reviewer agent, verify claim ต่อ source จริง ไม่ใช่แค่อ่าน diff)"
    )
    lines.append("")
    lines.append("**สกิลที่ควรติดตั้ง:**")
    lines.append("")
    lines.append(
        "- `maker-checker-gate` — กฎเดียวกับ orchestrator แต่ฝั่งนี้คือผู้ปฏิบัติจริง: "
        "ห้าม self-approve งานที่ตัวเองก็ผลิต"
    )
    lines.append("- `rigorous-diagnosis` — ก่อนเชื่อผลวัด/error message/พฤติกรรมที่สังเกตได้ครั้งเดียว")
    lines.append(
        "- `verified-live-fix` — ถ้างานนี้แตะ live deployment (web/production) — verify แบบ curl+browser dual-check"
    )
    lines.append(
        "- `security-review` / `web-secure-fast-audit` — ถ้า checkpoint นี้แตะ web/security surface"
    )
    lines.append("- `grr-epistemic-foundation` — เพื่อตรวจว่า Claim/Evidence/Warrant ของงานที่ตรวจ ครบและไม่ overclaim")
    lines.append("")
    lines.append(f"**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** {review_note}")
    lines.append("")

    lines.append("## Open questions / limitations of this skill plan itself")
    lines.append("")
    lines.append(
        "- AI role skill lists เป็น curated ไม่ใช่ auto-detected จากเนื้อหา checkpoint ทั้งหมด "
        "(ยกเว้น review_mode ด้านบน) — ถ้า checkpoint แตะ domain เฉพาะทางอื่น (เช่น กฎหมาย, การเงิน) "
        "อาจต้องเพิ่มสกิลที่ไม่ได้อยู่ในรายการนี้ ให้ human ตัดสินใจเพิ่มเอง"
    )
    lines.append(
        "- ไม่มีการยืนยันว่า skill list นี้ \"เพียงพอ\" หรือ \"ที่สุด\" — เป็นจุดเริ่มต้นที่สมเหตุสมผล "
        "(Dr tier) ให้ human ปรับตามบริบทจริง"
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} <checkpoint.json> <glossary.md> <kg_expert_layer.md> <out_skill_plan.md>",
            file=sys.stderr,
        )
        raise SystemExit(2)
    run = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    glossary_md = Path(sys.argv[2]).read_text(encoding="utf-8")
    expert_md = Path(sys.argv[3]).read_text(encoding="utf-8")
    out = build(run, glossary_md, expert_md)
    Path(sys.argv[4]).write_text(out, encoding="utf-8")
    print(f"wrote {sys.argv[4]}")


if __name__ == "__main__":
    main()
