# Skill Plan — HYP-UIA-046-DEMO-001

**Tier: `Dr`** (declared recommendation, same as Layer 2 — a judgment call, not a proven-optimal staffing plan). Who needs to know/do what to actually work this checkpoint, split into 4 roles. The Human section's "what to check" is mechanical (pulled straight from this checkpoint's own already-validated `falsifier`/`discriminating_information`/`uncertainties` fields, per §11 invariants ~39-41 — nothing invented). The AI role sections are curated: real skills installed in this workspace, mapped to what each role actually does, not benchmarked against alternatives — treat as a starting point to confirm or correct, same discipline as Layer 2's expert-framework suggestions.

## 1. Human

**คำศัพท์ที่ต้องรู้เพื่อสั่งงาน AI** — ดูที่ `HYP-UIA-046-DEMO-001`'s communication glossary (Section 1-2) ทั้งหมด — ผูกกับ *ประเด็นนี้โดยเฉพาะ* ไม่ใช่รายการทั่วไป: ต้องรู้คำศัพท์แกน (raw vocabulary จาก checkpoint จริง) บวกกับ framework ผู้เชี่ยวชาญที่ verified แล้ว (ถ้ามี) ก่อนจะสั่งงาน AI ให้ทำอะไรต่อได้อย่างแม่นยำ

**ผู้มีอำนาจตัดสินใจตาม checkpoint นี้:** Payments Risk & Controls (PRC) — on-call

**สิ่งที่ต้องตรวจ/verify ก่อนเชื่อผลลัพธ์ AI** (ดึงจาก field จริงที่ kernel validate แล้ว ต่อ hypothesis card — ไม่ใช่รายการทั่วไป):

- **`H1`** (KNOWN_DIRECT) — claim: retry-orchestrator writes ledger.status="SETTLED" on receiving a '202 Accepted' queue-ack from vendor "AcquirerX", without waiting for the actual settlement callback, so a later soft-decline on the same attempt-id never overwrites the premature SETTLED flag
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: ledger.status stays SETTLED even after acquirer confirms 'soft_decline' on attempt #2
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: acquirer response code ('06'|'91'|'96') vs ledger.status at attempt-id level
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): no production evidence
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: reconciliation-job double-reads the same ledger row due to a non-idempotent join key
- **`H2`** (CROSS_ADAPTIVE) — claim: the same premature-ack-as-success pattern that caused double-booked appointments in the unrelated booking-service fixture (client observing a queue-ack before the backend reached a final state) is structurally the same failure adapted to payments: a queue-ack is being treated as a settlement truth-state — cross-domain the fix pattern is "gate any external-facing status write behind the actual terminal callback, never behind an intermediate ack/nack"
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: adding PENDING_CONFIRMATION state does not change the double-counted SETTLED rate
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: presence/absence of an explicit PENDING_CONFIRMATION row between ack and settlement callback
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): no production evidence
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: the two systems only superficially resemble each other and the payments bug has an unrelated root cause in the settlement-callback delivery layer
- **`H3`** (GENERATIVE_TRANSFORMATIVE) — claim: a generative redesign — replacing the binary ledger.status field entirely with an append-only settlement-event log keyed by (attempt-id, acquirer-response-code, acquirer-timestamp), and deriving the merchant-facing SETTLED/PENDING/FAILED label as a pure read-time projection over that log — removes the entire class of premature-write bugs structurally, because there is no longer a single mutable status field for a race condition to corrupt; every downstream consumer (reconciliation-job, tax-reporting extract, merchant dashboard, R&LI variance report) reads the same append-only truth instead of a cached label 🔧
  - falsifier ที่ต้องเช็คว่ายัง falsify ไม่ได้จริง: migrating to an event-sourced model still permits two conflicting settlement-events to coexist for the same attempt-id without a defined resolution rule
  - ข้อมูลที่ต้องหาเพิ่มเพื่อแยกสมมติฐานนี้จากอันอื่น: whether the projection layer can reconstruct a consistent SETTLED/FAILED label for every historical attempt-id without manual reconciliation
  - ความไม่แน่นอนที่ประกาศไว้แล้ว (ต้องรู้ว่ายังไม่ปิด): no production evidence
  - คำอธิบายทางเลือกที่ AI พิจารณาแล้วแต่ยังไม่ตัด: the migration cost and downstream rewrite scope outweighs the benefit versus simply gating the existing write on a confirmed callback (H1's narrower fix)

**คำถามเปิดจาก Layer 2 ที่ human ต้อง override/ตัดสินเอง (AI ตอบไม่ได้):**

- **Is this org actually SOX/COSO-scoped?** The checkpoint gives no evidence either way
  (it's a synthetic fixture — `metadata.simulation: true`). COSO relevance is asserted
  from the *shape* of the problem (financial misstatement via reconciliation-board
  oversight), not from any explicit regulatory-scope field in the checkpoint.
- **Whether Saga/event-sourcing is proportionate for H1's narrower fix.** The checkpoint's
  own H3 card explicitly raises this tension ("migration cost and downstream rewrite scope
  outweighs the benefit versus simply gating the existing write on a confirmed callback") —
  a domain expert should weigh event sourcing's real migration cost against H1's much
  cheaper fix, which this layer cannot adjudicate from text alone.
- **AcquirerX-specific response-code semantics for `06`/`91`/`96`.** These are read here as
  generic ISO 8583-family soft-decline codes; the checkpoint's `AcquirerX` is itself
  synthetic, so there is no real specification to check them against. A production
  engagement would need the actual acquirer's code table.
- **Whether a more specific payments-industry-named pattern exists for "explicit
  intermediate confirmation state between ack and terminal outcome"** beyond generic
  FSM/Petri-net vocabulary — I did not find one via search and flagged this as MEDIUM
  confidence; a payments-domain expert may know a more specific named pattern (e.g. from
  card-network settlement-cycle documentation) that this session didn't surface.
- **The Five Whys entry is the weakest claim in this document** — it's a plausible-fit
  technique, not anything referenced or implied by the checkpoint itself; treat it as the
  lowest-confidence item here.

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

**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** review_mode = 'TARGETED_SEARCH "Phase-2 (draft)"' is not one of the 3 recognized values (TARGETED_SEARCH / INTERNAL_DATA_AUDIT / FIELD_OBSERVATION_LOG) — do NOT assume TARGETED_SEARCH's evidence discipline applies; the doer/auditor must read the raw hypothesis_evidence_challenge field themselves and confirm what kind of evidence this checkpoint actually rests on.

## 4. AI-auditor

หน้าที่: ตรวจ output ของ AI-doer แบบ **อิสระ** (fresh context, ไม่ใช่ agent เดียวกับที่ผลิตงาน) ก่อน orchestrator จะ merge/ship อะไรก็ตาม — ตรงกับ pattern ที่ session นี้ใช้จริงทุก PR (spawn independent reviewer agent, verify claim ต่อ source จริง ไม่ใช่แค่อ่าน diff)

**สกิลที่ควรติดตั้ง:**

- `maker-checker-gate` — กฎเดียวกับ orchestrator แต่ฝั่งนี้คือผู้ปฏิบัติจริง: ห้าม self-approve งานที่ตัวเองก็ผลิต
- `rigorous-diagnosis` — ก่อนเชื่อผลวัด/error message/พฤติกรรมที่สังเกตได้ครั้งเดียว
- `verified-live-fix` — ถ้างานนี้แตะ live deployment (web/production) — verify แบบ curl+browser dual-check
- `security-review` / `web-secure-fast-audit` — ถ้า checkpoint นี้แตะ web/security surface
- `grr-epistemic-foundation` — เพื่อตรวจว่า Claim/Evidence/Warrant ของงานที่ตรวจ ครบและไม่ overclaim

**หมายเหตุเฉพาะ checkpoint นี้ (จาก `review_mode` จริง):** review_mode = 'TARGETED_SEARCH "Phase-2 (draft)"' is not one of the 3 recognized values (TARGETED_SEARCH / INTERNAL_DATA_AUDIT / FIELD_OBSERVATION_LOG) — do NOT assume TARGETED_SEARCH's evidence discipline applies; the doer/auditor must read the raw hypothesis_evidence_challenge field themselves and confirm what kind of evidence this checkpoint actually rests on.

## Open questions / limitations of this skill plan itself

- AI role skill lists เป็น curated ไม่ใช่ auto-detected จากเนื้อหา checkpoint ทั้งหมด (ยกเว้น review_mode ด้านบน) — ถ้า checkpoint แตะ domain เฉพาะทางอื่น (เช่น กฎหมาย, การเงิน) อาจต้องเพิ่มสกิลที่ไม่ได้อยู่ในรายการนี้ ให้ human ตัดสินใจเพิ่มเอง
- ไม่มีการยืนยันว่า skill list นี้ "เพียงพอ" หรือ "ที่สุด" — เป็นจุดเริ่มต้นที่สมเหตุสมผล (Dr tier) ให้ human ปรับตามบริบทจริง
