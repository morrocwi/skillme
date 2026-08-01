# Skill Plan — HYP-UIA-GUT-NURSE-DEMO-001

**Tier: `Dr`** (declared recommendation, same as Layer 2 — a judgment call, not a proven-optimal staffing plan). Who needs to know/do what to actually work this checkpoint, split into 4 roles. The Human section's "what to check" is mechanical (pulled straight from this checkpoint's own already-validated `falsifier`/`discriminating_information`/`uncertainties` fields, per §11 invariants ~39-41 — nothing invented). The AI role sections are curated: real skills installed in this workspace, mapped to what each role actually does, not benchmarked against alternatives — treat as a starting point to confirm or correct, same discipline as Layer 2's expert-framework suggestions.

## 1. Human

**คำศัพท์ที่ต้องรู้เพื่อสั่งงาน AI** — ดูที่ `HYP-UIA-GUT-NURSE-DEMO-001`'s communication glossary (Section 1-2) ทั้งหมด — ผูกกับ *ประเด็นนี้โดยเฉพาะ* ไม่ใช่รายการทั่วไป: ต้องรู้คำศัพท์แกน (raw vocabulary จาก checkpoint จริง) บวกกับ framework ผู้เชี่ยวชาญที่ verified แล้ว (ถ้ามี) ก่อนจะสั่งงาน AI ให้ทำอะไรต่อได้อย่างแม่นยำ

**ผู้มีอำนาจตัดสินใจตาม checkpoint นี้:** patient safety officer

**สิ่งที่ต้องตรวจ/verify ก่อนเชื่อผลลัพธ์ AI** (ดึงจาก field จริงที่ kernel validate แล้ว ต่อ hypothesis card — ไม่ใช่รายการทั่วไป):

- **`H1`** (KNOWN_DIRECT) — claim: the app's symptom picker uses one generic 'stomach issue' checkbox that conflates bloating, cramping, diarrhea, constipation, and red-flag symptoms like rectal bleeding into a single undifferentiated label
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: nurses can already reliably distinguish urgency from the single label alone
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: nurse triage-time measured with subtype label present vs. absent
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): no production evidence
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: nurses are undertrained on reading the existing free-text detail field
- **`H2`** (CROSS_ADAPTIVE) — claim: the app does not log symptom duration or frequency, so nurses cannot apply standard clinical pattern criteria (e.g. distinguishing acute vs. chronic GI symptom presentation) that require that data
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: urgency triage does not actually depend on duration/frequency data
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: comparison of triage accuracy with vs. without structured duration data available
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): structured-field patient-compliance rate not field-confirmed
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: nurses could infer duration from submission timestamps alone without a dedicated field
- **`H3`** (GENERATIVE_TRANSFORMATIVE) — claim: the app's binary logged-symptom event model exposes only one undifferentiated queue tier to nurses, collapsing an already-existing red-flag-vs-benign distinction the app's own backend could compute but doesn't surface
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: red-flag and benign symptoms already render at visibly different queue positions
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: backend log showing whether a red-flag keyword was present but not surfaced in the queue-row render
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): free-text red-flag keyword detection accuracy not field-confirmed
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: ambiguity originates solely from the picker (H1), not from the event model discarding an already-available signal

**คำถามเปิดจาก Layer 2 ที่ human ต้อง override/ตัดสินเอง (AI ตอบไม่ได้):**

- **Is SNOMED CT actually licensed/available to this org?** SNOMED CT requires a
  national/regional license in many jurisdictions — adopting it isn't free even
  though it's the technically correct named standard. The checkpoint gives no
  evidence either way (synthetic fixture).
- **Would ESI (an emergency-department-specific tool) actually transfer to an
  outpatient app-based triage context**, or does outpatient/telehealth GI triage
  have its own more specific named acuity framework this session didn't surface?
  Flagged as the weakest domain-fit claim among the VERIFIED-VIA-SEARCH items.
- **The Rome IV frequency-threshold modification (3 days/month) is from a single
  2024 validation study**, not yet necessarily adopted into mainstream clinical
  practice guidelines — a domain expert should confirm current guideline status
  rather than treating this as settled.
- **Whether the app's free-text field genuinely contains a detectable "red-flag
  keyword" signal (H3's premise)** is itself unverified — this layer can name the
  clinical vocabulary red-flag detection would need to match against, but cannot
  confirm the NLP/keyword-detection engineering claim H3 makes.

**สกิลที่ต้องมีเพื่อสั่งงานสำเร็จ** (ทั่วไป ไม่ผูกกับ checkpoint นี้โดยเฉพาะ แต่จำเป็นเสมอ):

- อ่าน tier ออก: `Th_coqc` (พิสูจน์แล้ว) ≠ `finite_diagnostic` (วัด/รันจริง) ≠ `Dr` (narrative ที่มนุษย์ประกาศ) ≠ `Open` (ยังไม่รู้) — ต้องรู้ว่า output จาก AI ชิ้นไหนอยู่ tier ไหน
- รู้ว่า `VALID_CHECKPOINT` **ไม่ใช่** decision/intervention/field-confirmation/success/closure (Invariant #46) — ห้ามสั่งงานต่อราวกับว่า checkpoint นี้ตัดสินใจแทนได้แล้ว
- รู้วิธีขอ maker-checker: ทุกงานที่ AI ผลิตแล้วจะ merge/ship/ตัดสินใจต่อ ต้องมี independent check ก่อนเสมอ (คนละ context/agent จากคนที่ผลิต) — อย่าเชื่อ AI ที่ตรวจงานตัวเอง
- อ่าน glossary.md Section 3 ("คำที่ชั้น 2 เพิ่มเข้ามาจริง") เพื่อรู้ว่าคำไหนเป็นการตีความของ AI (Open tier) ไม่ใช่ข้อเท็จจริงจาก checkpoint (readout)

## 2. AI-orchestrator

หน้าที่: แตกงานเป็นขั้นตอนตาม §6.9.1's domain-mapping discipline, สั่งงาน AI-doer, เรียก AI-auditor ก่อน merge/ship ทุกครั้ง (maker-checker firewall, Axiom A10), และห้ามให้ผลของ auditor ไหลย้อนกลับเข้า doer ก่อน freeze (Invariant #7)

**สกิลที่ควรติดตั้ง (จาก skill จริงใน workspace นี้):**

- `project-onboard` — ก่อนเริ่มงานใน repo ใดๆ ที่ยังไม่เคย onboard
- `subteam-structure` — โครงทีมย่อยมาตรฐาน (orchestrator + system + design + coding)
- `maker-checker-gate` — รู้ว่า artifact ระดับไหนต้องการ independent check ก่อน release/merge/ship (นี่คือกฎที่บังคับ AI-auditor ให้มีอยู่จริง ไม่ใช่ optional)
- `grr-epistemic-foundation` — โครงสร้าง Claim/Evidence/Warrant/Status สำหรับ finding ที่ไม่ใช่ Coq theorem

## 3. AI-doer

หน้าที่: สร้าง/แก้ checkpoint จริง, รัน kg_extract.py/build_glossary.py, ทำ Layer 2 reasoning (WebSearch-verified), เขียนโค้ด — งานที่ AI-auditor จะมาตรวจทีหลัง

**สกิลที่ควรติดตั้ง:**

- `information-discrete-math` — บังคับโหลดก่อนแตะคณิตศาสตร์/ฟิสิกส์ใดๆ (มุม/ระยะทาง/อนันต์/ศูนย์) ตาม §6.9.2's contaminated-concept guard
- `toon-format` — บังคับโหลดก่อนส่งข้อมูลมีโครงสร้าง (JSON/ตาราง) เข้า prompt LLM ใดๆ
- `rigorous-diagnosis` — วินัยการวินิจฉัย/debug ก่อนสรุป root cause หรือบอกว่า "แก้แล้ว"
- `doc-ecosystem` — ถ้างานนี้ต้องส่งต่อเข้า doc-ecosystem project (bridge.py's target)

**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** review_mode = TARGETED_SEARCH — evidence for this checkpoint is literature/published sources; the doer needs real WebSearch discipline (verify claims, don't assert from training knowledge alone), the auditor needs to spot-check source links actually support the claim, not just exist.

## 4. AI-auditor

หน้าที่: ตรวจ output ของ AI-doer แบบ **อิสระ** (fresh context, ไม่ใช่ agent เดียวกับที่ผลิตงาน) ก่อน orchestrator จะ merge/ship อะไรก็ตาม — ตรงกับ pattern ที่ session นี้ใช้จริงทุก PR (spawn independent reviewer agent, verify claim ต่อ source จริง ไม่ใช่แค่อ่าน diff)

**สกิลที่ควรติดตั้ง:**

- `maker-checker-gate` — กฎเดียวกับ orchestrator แต่ฝั่งนี้คือผู้ปฏิบัติจริง: ห้าม self-approve งานที่ตัวเองก็ผลิต
- `rigorous-diagnosis` — ก่อนเชื่อผลวัด/error message/พฤติกรรมที่สังเกตได้ครั้งเดียว
- `verified-live-fix` — ถ้างานนี้แตะ live deployment (web/production) — verify แบบ curl+browser dual-check
- `security-review` / `web-secure-fast-audit` — ถ้า checkpoint นี้แตะ web/security surface
- `grr-epistemic-foundation` — เพื่อตรวจว่า Claim/Evidence/Warrant ของงานที่ตรวจ ครบและไม่ overclaim

**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** review_mode = TARGETED_SEARCH — evidence for this checkpoint is literature/published sources; the doer needs real WebSearch discipline (verify claims, don't assert from training knowledge alone), the auditor needs to spot-check source links actually support the claim, not just exist.

## Open questions / limitations of this skill plan itself

- AI role skill lists เป็น curated ไม่ใช่ auto-detected จากเนื้อหา checkpoint ทั้งหมด (ยกเว้น review_mode ด้านบน) — ถ้า checkpoint แตะ domain เฉพาะทางอื่น (เช่น กฎหมาย, การเงิน) อาจต้องเพิ่มสกิลที่ไม่ได้อยู่ในรายการนี้ ให้ human ตัดสินใจเพิ่มเอง
- ไม่มีการยืนยันว่า skill list นี้ "เพียงพอ" หรือ "ที่สุด" — เป็นจุดเริ่มต้นที่สมเหตุสมผล (Dr tier) ให้ human ปรับตามบริบทจริง
