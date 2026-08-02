# Communication Glossary — HYP-SKILLME-GUT-NURSE-DEMO-001

**คำศัพท์นี้ผูกกับตัว *ประเด็น/โดเมน* ไม่ได้ผูกกับ role ใด role หนึ่ง** — ใครก็ตามที่เข้าร่วมคุยเรื่องนี้ (วิศวกร, พยาบาล, ผู้จัดการฝ่ายปฏิบัติการ, หรือใครก็ตาม) ต้องรู้คำชุดเดียวกันนี้ ไม่ว่าพื้นเดิมของแต่ละคนจะเป็นสายไหน รวมจาก 2 ชั้นที่มีอยู่แล้ว: ชั้น 1 (deterministic readout จาก checkpoint จริง) + ชั้น 2 (AI-interpretive framework/องค์ความรู้ Open tier, เฉพาะที่ confidence HIGH หรือ VERIFIED-VIA-SEARCH เท่านั้น — ตัดรายการที่ยังไม่มั่นใจออกเพื่อไม่ให้ glossary นี้ชวนเข้าใจผิดว่าทุกคำแน่นอนเท่ากันหมด).

## 1. คำศัพท์แกนของประเด็นนี้ (readout จาก checkpoint จริง)

**ผู้เกี่ยวข้อง (ROLE):**
`clinical nursing triage`, `patients`, `product engineering`, `clinical nursing triage lead`, `patient safety officer`

**แนวคิด/สภาวะของปัญหา (CONCEPT):**
`app`, `nurses`, `SimulatedData`, `evidence`, `record`, `symptom`, `H1`, `could`, `duration`, `event`, `field`, `model`, `one`, `picker`, `undifferentiated`, `GI`, `H2`, `H3`, `acute`, `alone`, `already-available`, `already-existing`, `ambiguity`, `apply`, `backend`, `binary`, `bleeding`, `bloating`, `cannot`, `checkbox`, `chronic`, `clinical`, `collapsing`, `compute`, `conflates`, `constipation`, `cramping`, `criteria`, `data`, `dedicated`, `detail`, `diarrhea`, `discarding`, `distinction`, `distinguishing`, `does`, `doesn`, `existing`, `exposes`, `free-text`, `frequency`, `generic`, `infer`, `issue`, `label`, `like`, `log`, `logged-symptom`, `only`, `originates`, `own`, `pattern`, `presentation`, `queue`, `reading`, `rectal`, `red-flag`, `red-flag-vs-benign`, `require`, `signal`, `single`, `solely`, `standard`, `stomach`, `submission`, `surface`, `symptoms`, `tier`, `timestamps`, `undertrained`, `uses`, `without`

**กลไก/กระบวนการ (PROCESS):**
`clinical`, `field`, `distinguishable`, `entry`, `event`, `lets`, `queue`, `adding`, `category`, `criteria`, `duration`, `free-text`, `frequency`, `model`, `render`, `rows`, `structured`, `symptom`, `without`, `GI`, `against`, `all`, `any`, `apply`, `captures`, `case`, `categories`, `categorize`, `change`, `computed`, `dashboard`, `data`, `designed`, `directly`, `display`, `emits`, `escalate`, `evaluate`, `even`, `fast`, `has`, `have`, `ingestion`, `keywords`, `label`, `log-symptom`, `map`, `note`, `open-case`, `opening`, `patient`, `patient-facing`, `pattern`, `pattern-based`, `picker`, `point-in-time`, `present`, `red-flag`, `regardless`, `render-queue-row`, `same`, `schema`, `severity`, `signal`, `single`, `standard`, `submission`, `subtype`, `subtypes`, `surfaced`, `symptom-entry`, `symptom-logged`, `taxonomy`, `though`, `time`, `triage`, `triage-queue`, `type`, `urgency-tier`, `value`, `was`

**เครื่องมือ/ระบบ (TOOL):**
`nurse`, `red-flag-escalation-line`, `symptom-entry-schema`, `symptom-tracker-app`, `triage-queue-dashboard`

**วิธีวิเคราะห์/มาตรฐานที่อ้างถึง (PROTOCOL):**
`GI symptom triage taxonomy`, `event-schema granularity redesign`, `red-flag symptom escalation protocol`, `synthetic benign-entry replay`, `synthetic red-flag-entry replay`

**ตัวชี้วัด/เงื่อนไขพิสูจน์ (METRIC):**
`red-flag`, `nurse`, `triage`, `already`, `benign`, `data`, `duration`, `label`, `present`, `render`, `urgency`, `90`, `GI`, `absent`, `accuracy`, `actually`, `alone`, `available`, `backend`, `can`, `comparison`, `depend`, `different`, `distinguish`, `does`, `entry`, `frequency`, `keyword`, `log`, `measured`, `nurses`, `pilot`, `positions`, `queue`, `queue-row`, `reliably`, `showing`, `single`, `structured`, `subtype`, `surfaced`, `symptom`, `symptoms`, `triage-time`, `visibly`, `was`, `whether`, `without`, `ผิดเป็น`, `มี`, `ลดลงต่ำกว่า`, `วินาทีต่อเคส`, `หรือ`, `ออกจากคิว`, `เคสใดถูก`, `เคสไหนถูกมองข้าม`, `เวลาเฉลี่ยที่`, `โดยไม่มี`, `ใช้เวลาแยกเคสนานขึ้นกว่าก่อน`, `ใช้แยก`

## 2. องค์ความรู้ผู้เชี่ยวชาญที่ควรรู้เพิ่ม (AI-interpretive, Open tier — เฉพาะที่มั่นใจสูง)

- **Rome IV criteria (Disorders of Gut-Brain Interaction, DGBI)** — the current, active diagnostic framework for functional GI disorders (IBS, functional bloating, etc.), and it explicitly requires duration/frequency data (e.g. IBS: recurrent abdominal pain ≥1 day/week over the last 3 months, onset ≥6 months prior) — exactly the structured field H2 proposes adding and the app currently lacks. A 2024 validation study found relaxing the frequency threshold to 3 days/month improved diagnostic performance (90.2% sensitivity, 85.1% specificity) without losing specificity, showing this is an actively-refined, current framework, not a static/outdated one. Confidence: VERIFIED-VIA-SEARCH.
- **NICE-guideline-style GI "red flag"/alarm symptoms (rectal bleeding, weight loss, altered bowel habit, anemia)** — the exact, real, named clinical concept H1 and H3 gesture at informally ("red-flag symptoms like rectal bleeding"). Confirmed current: NICE CG27 referral criteria (rectal bleeding + bowel-habit change, age-stratified two-week-wait referral) are still the reference alarm- symptom framework cited in current (2023-2024) clinical literature. Confidence: VERIFIED-VIA-SEARCH.
- **Emergency Severity Index (ESI)** — a real, current, 5-level nurse triage acuity framework (not specific to GI, but directly the class of tool H3's "compute an urgency tier the backend already has signal for" is reinventing ad hoc). Confirmed still in active use and under active validation research as of 2024-2025 (diagnostic-accuracy meta-analyses, reliability studies). Confidence: VERIFIED-VIA-SEARCH.
- **SNOMED CT** — the real, current, internationally-maintained structured clinical terminology standard that already has a dedicated "Gastrointestinal symptom (finding)" concept (ID 267045008) with subtype hierarchy via "is a" relationships. This is the named standard H1's proposed symptom-subtype taxonomy would be reinventing informally; adopting SNOMED CT GI-symptom codes instead of an app-specific enum would also solve H2's cross-system interoperability angle for free. Confidence: VERIFIED-VIA-SEARCH.

## 3. คำที่ชั้น 2 เพิ่มเข้ามาจริง (ไม่ซ้ำกับคำดิบในชั้น 1)

None of the following appear as literal words/phrases in the checkpoint text
(checked against kg_raw_word.md's word table) — they are this layer's
interpretive contribution:

- Rome IV criteria / disorders of gut-brain interaction (DGBI)
- NICE CG27 / two-week-wait referral criteria
- Emergency Severity Index (ESI) — the checkpoint never names any formal triage
  acuity framework, even though H3 is functionally proposing one
- SNOMED CT (concept 267045008, "Gastrointestinal symptom (finding)")
- The specific 6-month-onset / 3-month-active / ≥1-day-per-week diagnostic
  thresholds Rome IV actually uses (the checkpoint's H2 says "duration/frequency"
  generically, never these concrete numbers)
- "Alarm symptoms" / "red-flag features" as the formal clinical term-of-art
  (the checkpoint's H1/H3 use "red-flag" informally, without citing that this is
  itself established clinical vocabulary with a specific, named symptom list)

## ภาคผนวก: คำเฉพาะของกลไกโปรโตคอล SKILLME เอง (ไม่ใช่คำศัพท์ของประเด็น — ตัดออกจาก glossary หลักโดยตั้งใจ)

`CROSS_ADAPTIVE`, `DESIGN_HYPOTHESIS`, `GENERATIVE_TRANSFORMATIVE`, `KNOWN_DIRECT`, `MECHANISM_HYPOTHESIS`, `STRUCTURAL_HYPOTHESIS`, `TARGETED_SEARCH`
