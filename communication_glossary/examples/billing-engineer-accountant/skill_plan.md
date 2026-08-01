# Skill Plan — HYP-UIA-BILLING-ACCT-DEMO-001

**Tier: `Dr`** (declared recommendation, same as Layer 2 — a judgment call, not a proven-optimal staffing plan). Who needs to know/do what to actually work this checkpoint, split into 4 roles. The Human section's "what to check" is mechanical (pulled straight from this checkpoint's own already-validated `falsifier`/`discriminating_information`/`uncertainties` fields, per §11 invariants ~39-41 — nothing invented). The AI role sections are curated: real skills installed in this workspace, mapped to what each role actually does, not benchmarked against alternatives — treat as a starting point to confirm or correct, same discipline as Layer 2's expert-framework suggestions.

## 1. Human

**คำศัพท์ที่ต้องรู้เพื่อสั่งงาน AI** — ดูที่ `HYP-UIA-BILLING-ACCT-DEMO-001`'s communication glossary (Section 1-2) ทั้งหมด — ผูกกับ *ประเด็นนี้โดยเฉพาะ* ไม่ใช่รายการทั่วไป: ต้องรู้คำศัพท์แกน (raw vocabulary จาก checkpoint จริง) บวกกับ framework ผู้เชี่ยวชาญที่ verified แล้ว (ถ้ามี) ก่อนจะสั่งงาน AI ให้ทำอะไรต่อได้อย่างแม่นยำ

**ผู้มีอำนาจตัดสินใจตาม checkpoint นี้:** VP of Finance

**สิ่งที่ต้องตรวจ/verify ก่อนเชื่อผลลัพธ์ AI** (ดึงจาก field จริงที่ kernel validate แล้ว ต่อ hypothesis card — ไม่ใช่รายการทั่วไป):

- **`H1`** (KNOWN_DIRECT) — claim: the billing engine books the full new-plan amount as revenue on the upgrade date instead of spreading it across the remaining days of the billing cycle
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: recognized revenue already matches service period without proration
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: comparing ledger-posted amount vs. days-remaining-prorated amount for the same upgrade event
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): no production evidence
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: the ledger posting is correct and the MRR dashboard is the one computing it wrong
- **`H2`** (CROSS_ADAPTIVE) — claim: the billing engine's internal 'revenue' field is computed as cash collected at invoice time rather than as an accrual-based recognition schedule, conflating two distinct accounting concepts under one field name
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: revenue timing does not actually depend on cash-vs-accrual distinction here
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: a case where cash collected and recognized revenue diverge for reasons other than proration timing
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): schema-migration cost not field-confirmed
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: proration alone (H1) is sufficient and the cash-vs-accrual distinction is not actually load-bearing here
- **`H3`** (GENERATIVE_TRANSFORMATIVE) — claim: the engine's single point-in-time 'upgrade-billed' event discards the remaining-service-period data needed to reconstruct a proper revenue-recognition schedule, forcing accounting to rebuild that schedule by hand every close
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: the event already carries enough data to reconstruct a schedule without manual work
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: whether the engine's raw event payload contains remaining-service-period data that simply isn't surfaced downstream
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): whether a schedule-event redesign is proportionate given migration cost
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: ambiguity originates solely from missing proration math (H1), not from the event model discarding schedule data entirely

**คำถามเปิดจาก Layer 2 ที่ human ต้อง override/ตัดสินเอง (AI ตอบไม่ได้):**

- **Is this company actually SOX-scoped or independently audited?** The
  checkpoint gives no evidence either way. If it is, the manual-reconciliation
  burden this issue describes is itself a potential internal-control weakness
  worth flagging to the controller/auditors, not just an engineering annoyance —
  this layer cannot make that call from text alone.
- **H1's "just prorate by days remaining" proposal vs. ASC 606's actual
  contract-modification rule**: proration is necessary but the search results
  suggest ASC 606 modification accounting may require more than simple
  day-proration in some cases (a fresh performance-obligation assessment) — a
  real accountant should confirm whether this specific company's contracts are
  simple enough that day-proration alone is GAAP-compliant, or whether H3's
  fuller schedule-reconstruction approach is actually required for compliance,
  not just convenience.
- **H2's proposed schema change (separate `cash_collected` from
  `recognized_revenue_schedule` fields) is architecturally sound accounting-
  theory-wise, but this layer cannot assess the engineering migration cost** —
  that tradeoff (named explicitly as unresolved in H2's own `uncertainties`
  field) needs an engineer's estimate, not an accounting framework.
- **IFRS 15 portability was asserted, not independently verified this session**
  — if this company has any international reporting obligation, a human expert
  should confirm the specific points of divergence rather than trusting the
  "largely portable" summary above.

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
