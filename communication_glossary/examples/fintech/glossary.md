# Communication Glossary — HYP-UIA-046-DEMO-001

**คำศัพท์นี้ผูกกับตัว *ประเด็น/โดเมน* ไม่ได้ผูกกับ role ใด role หนึ่ง** — ใครก็ตามที่เข้าร่วมคุยเรื่องนี้ (วิศวกร, พยาบาล, ผู้จัดการฝ่ายปฏิบัติการ, หรือใครก็ตาม) ต้องรู้คำชุดเดียวกันนี้ ไม่ว่าพื้นเดิมของแต่ละคนจะเป็นสายไหน รวมจาก 2 ชั้นที่มีอยู่แล้ว: ชั้น 1 (deterministic readout จาก checkpoint จริง) + ชั้น 2 (AI-interpretive framework/องค์ความรู้ Open tier, เฉพาะที่ confidence HIGH หรือ VERIFIED-VIA-SEARCH เท่านั้น — ตัดรายการที่ยังไม่มั่นใจออกเพื่อไม่ให้ glossary นี้ชวนเข้าใจผิดว่าทุกคำแน่นอนเท่ากันหมด).

## 1. คำศัพท์แกนของประเด็นนี้ (readout จาก checkpoint จริง)

**ผู้เกี่ยวข้อง (ROLE):**
`Müller — QA lead 🔧`, `Payments Risk & Controls (PRC) — on-call`, `R&D / Ops (24x7)`, `merchant "north-cluster" (Tier-1)`, `Reconciliation & Ledger Integrity (R&LI) board`, `cardholder`, `merchant support desk`

**แนวคิด/สภาวะของปัญหา (CONCEPT):**
`same`, `status`, `SETTLED`, `SimulatedData`, `callback`, `evidence`, `ledger`, `queue-ack`, `record`, `H1`, `actual`, `append-only`, `attempt-id`, `behind`, `downstream`, `field`, `fix`, `label`, `log`, `never`, `pattern`, `payments`, `reconciliation-job`, `settlement`, `structurally`, `unrelated`, `write`, `202`, `Accepted`, `AcquirerX`, `FAILED`, `H2`, `H3`, `LI`, `PENDING`, `ack`, `acquirer-response-code`, `acquirer-timestamp`, `adapted`, `any`, `appointments`, `backend`, `because`, `before`, `being`, `benefit`, `binary`, `booking-service`, `bug`, `bugs`, `cached`, `cause`, `caused`, `class`, `client`, `condition`, `confirmed`, `consumer`, `corrupt`, `cost`, `cross-domain`, `dashboard`, `delivery`, `deriving`, `double-booked`, `double-reads`, `due`, `each`, `entire`, `entirely`, `every`, `existing`, `external-facing`, `extract`, `failure`, `final`, `fixture`, `flag`, `gate`, `gating`, `generative`, `has`, `instead`, `intermediate`, `join`, `key`, `keyed`, `later`, `layer`, `longer`, `merchant`, `merchant-facing`, `migration`, `mutable`, `nack`, `narrower`, `non-idempotent`, `observing`, `only`, `other`, `outweighs`, `overwrites`, `premature`, `premature-ack-as-success`, `premature-write`, `projection`, `pure`, `race`, `reached`, `read-time`, `reads`, `receiving`, `redesign`, `removes`, `replacing`, `report`, `resemble`, `retry-orchestrator`, `rewrite`, `root`, `row`, `scope`, `settlement-callback`, `settlement-event`, `simply`, `single`, `soft-decline`, `state`, `superficially`, `systems`, `tax-reporting`, `terminal`, `there`, `treated`, `truth`, `truth-state`, `two`, `variance`, `vendor`, `versus`, `waiting`, `without`, `writes`

**กลไก/กระบวนการ (PROCESS):**
`state`, `because`, `settlement`, `write-settled-flag`, `PENDING_CONFIRMATION`, `SETTLED`, `after`, `callback`, `class`, `confirmed`, `double-counted`, `explicit`, `rate`, `rather`, `request`, `202`, `HTTP`, `accepted`, `ack`, `ack/nack (soft-decline)`, `acknowledgement`, `acquirer-specific`, `already`, `already-emitted`, `ambiguous-SETTLED`, `becomes`, `between`, `booking-service`, `both`, `bug`, `bugs`, `business-layer`, `can`, `collapse`, `conflated`, `construction`, `consumer`, `cost`, `cycle`, `downstream`, `early`, `edge`, `eliminates`, `event`, `event-sourced`, `every`, `fire`, `fires`, `fix`, `fixture`, `intermediate`, `introducing`, `log`, `logic`, `machine`, `merely`, `migration`, `mirroring`, `models`, `moving`, `mutable-status`, `nack`, `needing`, `neither`, `one`, `only`, `overwrite`, `payment`, `projection`, `queue`, `races`, `read`, `receipt`, `reconcile`, `reconciliation`, `reduced`, `reduces`, `requiring`, `resolved`, `resolves`, `retroactively`, `retry-orchestrator`, `reverting`, `rewritten`, `row`, `settlement-event`, `single`, `soft-decline`, `sprint`, `structurally`, `submit-retry`, `success`, `systems`, `terminal`, `toward`, `transport-layer`, `trigger`, `undefined`, `validated`, `within`, `without`, `write`, `write-ordering`, `zero`

**เครื่องมือ/ระบบ (TOOL):**
`acquirer-gateway "AcquirerX" (prod)`, `ledger-writer (async/batch)`, `reconciliation-job (nightly, 02:00 ICT)`, `retry-orchestrator "north wing"`

**วิธีวิเคราะห์/มาตรฐานที่อ้างถึง (PROTOCOL):**
`ISO-8583 "field 39" mapping`, `Phase-2 (draft) review`, `canary gateway (5% traffic)`, `idempotency-key protocol v2`, `shadow-write "no-op" mode`

**ตัวชี้วัด/เงื่อนไขพิสูจน์ (METRIC):**
`SETTLED`, `ledger`, `acquirer`, `attempt-id`, `status`, `06`, `91`, `96`, `PENDING_CONFIRMATION`, `code`, `double-counted`, `rate`, `response`, `without`, `01`, `FAILED`, `absence`, `ack`, `adding`, `after`, `attempt`, `between`, `callback`, `can`, `change`, `coexist`, `confirms`, `conflicting`, `consistent`, `defined`, `does`, `even`, `event-sourced`, `every`, `explicit`, `field`, `historical`, `label`, `layer`, `level`, `machine`, `manual`, `migrating`, `model`, `permits`, `presence`, `projection`, `reconciliation`, `reconstruct`, `resolution`, `retry-state`, `row`, `rule`, `same`, `settlement`, `settlement-events`, `soft-decline`, `soft_decline`, `state`, `stays`, `still`, `two`, `whether`, `ต่อวัน`, `ต่ำกว่า`, `ยังถูกเขียนเป็น`, `วัดจาก`, `หรือ`, `หลังแก้`, `เทียบกับ`, `ใน`, `ไม่ลดลง`

## 2. องค์ความรู้ผู้เชี่ยวชาญที่ควรรู้เพิ่ม (AI-interpretive, Open tier — เฉพาะที่มั่นใจสูง)

- **ISO 8583 message-field semantics** — CONFIRMED-RELEVANT, already present in the source (`translation.adapter_cards` cites "ISO-8583 'field 39' mapping," field 39 being the response/action code). Confidence: HIGH (well-established knowledge; ISO 8583 is the decades-old standard for card-present/card-not-present authorization messaging and is still the dominant wire format acquirers use today).
- **Idempotency keys, in the Stripe/PayPal API-design convention sense** — applies because the whole bug class (H1, H2) is "an ack was treated as a terminal success," which is precisely what idempotency-key design exists to prevent on the *retry* side (safe re-submission) even though this bug is really on the *status-interpretation* side. Confidence: VERIFIED-VIA-SEARCH. Stripe's own idempotency docs confirm the current, correct framing: the API layer caches the *first* response for a given key and returns it on retry, with a documented key-lifecycle (e.g. auto-expiry) and strict parameter-match validation — this is the standard practitioners cite, and it is still current in 2026.
- **Acquirer/network response-code taxonomy (e.g. `06`, `91`, `96` soft-decline codes)** — CONFIRMED-RELEVANT, literally present in `registration.failure_rule` and `discriminating_information`. Confidence: HIGH (these are standard ISO 8583-family response codes; a payments engineer would recognize `91` as "issuer/switch inoperative" class and `96` as "system malfunction" class — worth a domain expert double-checking the exact code table version in use for AcquirerX specifically, since code meanings can be scheme- or acquirer-specific).
- **Saga pattern / eventual-consistency reconciliation with compensating transactions** — applies to the retry-orchestrator's multi-step flow (submit-retry → ack/nack → write-settled-flag → reconcile) as a long-running, multi-service transaction that needs either explicit compensation or a defined reconciliation sweep, which is exactly what the nightly reconciliation-job already is (an ad-hoc, undocumented compensation pass). Confidence: VERIFIED-VIA-SEARCH — current material (Microsoft Azure Architecture Center, Temporal docs) confirms Saga is still the standard named pattern for this, and explicitly states periodic reconciliation-with-compensating-transactions as a companion technique when eventual consistency is accepted — which matches this checkpoint's nightly job.
- **Event sourcing / CQRS (event-sourced settlement log)** — directly matches H3's proposal almost verbatim ("append-only settlement-event log... deriving the... label as a pure read-time projection"). Confidence: VERIFIED-VIA-SEARCH — current fintech architecture writeups (e.g. Formance, Iconsolutions) confirm event sourcing + CQRS is the named, current pattern for exactly this "single mutable status field is a race-condition target" problem in payment/ledger systems; H3 is independently re-deriving a known named pattern, not inventing something novel.
- **Double-entry bookkeeping reconciliation discipline** — applies as the conceptual reason "double-counted SETTLED volume" is a real financial-reporting defect and not just a UI bug: a settlement ledger that can silently overstate a balance without an offsetting entry violates the basic double-entry invariant reconciliation is built to catch. Confidence: HIGH (foundational accounting knowledge, not searched this session).
- **COSO Internal Control – Integrated Framework** — applies at the "why does an R&LI board exist and why does a nightly reconciliation-job matter" level: COSO's control-activities component explicitly names reconciliation as a standard detective control for financial accuracy. Confidence: VERIFIED-VIA-SEARCH — confirmed the 2013 COSO Integrated Framework (refreshed from the original 1992 version) is still the current, dominant internal-controls framework as of this search, and that "reconciliation" is explicitly named within it as a control activity. Whether this specific fintech org is actually COSO-scoped (e.g. SOX- reporting entity) is NOT knowable from the checkpoint and is flagged as an open question.
- **SRE-style blameless postmortem practice** — applies because the checkpoint already contains a verbatim postmortem quote from the on-call engineer and frames the fix search as cross-incident pattern transfer, which is the core practice blameless-postmortem methodology is designed to produce. Confidence: HIGH (well-established practice, not searched this session — Google SRE book naming is stable and I am confident in it).

## 3. คำที่ชั้น 2 เพิ่มเข้ามาจริง (ไม่ซ้ำกับคำดิบในชั้น 1)

None of the following literal terms appear in the checkpoint text (checked against the word
table in kg_raw_word_fintech_v3.md) — they are this layer's interpretive contribution:

- Saga pattern (compensating transactions)
- Event sourcing / CQRS (as the *named* pattern — the checkpoint describes the mechanism
  in H3 but never names it)
- Idempotency key (the checkpoint's own `translation.adapter_cards` says "idempotency-key
  protocol v2" as a *label*, but never explains or names the underlying Stripe/PayPal-style
  mechanics this layer is surfacing)
- COSO Internal Control – Integrated Framework
- Double-entry bookkeeping
- SRE blameless postmortem (as a named methodology, distinct from the checkpoint's own
  postmortem *quote*)
- The Five Whys
- Formal state machine / Petri-net terminology (the checkpoint describes states and
  transitions structurally but never uses FSM/Petri-net vocabulary)

## ภาคผนวก: คำเฉพาะของกลไกโปรโตคอล UIA เอง (ไม่ใช่คำศัพท์ของประเด็น — ตัดออกจาก glossary หลักโดยตั้งใจ)

`CROSS_ADAPTIVE`, `DESIGN_HYPOTHESIS`, `GENERATIVE_TRANSFORMATIVE`, `KNOWN_DIRECT`, `MECHANISM_HYPOTHESIS`, `STRUCTURAL_HYPOTHESIS`, `TARGETED_SEARCH "Phase-2 (draft)"`
