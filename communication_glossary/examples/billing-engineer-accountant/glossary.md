# Communication Glossary — HYP-SKILLME-BILLING-ACCT-DEMO-001

**คำศัพท์นี้ผูกกับตัว *ประเด็น/โดเมน* ไม่ได้ผูกกับ role ใด role หนึ่ง** — ใครก็ตามที่เข้าร่วมคุยเรื่องนี้ (วิศวกร, พยาบาล, ผู้จัดการฝ่ายปฏิบัติการ, หรือใครก็ตาม) ต้องรู้คำชุดเดียวกันนี้ ไม่ว่าพื้นเดิมของแต่ละคนจะเป็นสายไหน รวมจาก 2 ชั้นที่มีอยู่แล้ว: ชั้น 1 (deterministic readout จาก checkpoint จริง) + ชั้น 2 (AI-interpretive framework/องค์ความรู้ Open tier, เฉพาะที่ confidence HIGH หรือ VERIFIED-VIA-SEARCH เท่านั้น — ตัดรายการที่ยังไม่มั่นใจออกเพื่อไม่ให้ glossary นี้ชวนเข้าใจผิดว่าทุกคำแน่นอนเท่ากันหมด).

## 1. คำศัพท์แกนของประเด็นนี้ (readout จาก checkpoint จริง)

**ผู้เกี่ยวข้อง (ROLE):**
`engineering`, `monthly close accounting team`, `controller`, `finance systems team`, `VP of Finance`

**แนวคิด/สภาวะของปัญหา (CONCEPT):**
`schedule`, `H1`, `SimulatedData`, `billing`, `engine`, `evidence`, `record`, `accounting`, `data`, `event`, `field`, `one`, `proration`, `revenue`, `H2`, `H3`, `MRR`, `accrual-based`, `across`, `actually`, `alone`, `ambiguity`, `amount`, `books`, `cash`, `cash-vs-accrual`, `close`, `collected`, `computed`, `computing`, `concepts`, `conflating`, `correct`, `cycle`, `dashboard`, `date`, `days`, `discarding`, `discards`, `distinct`, `distinction`, `entirely`, `every`, `forcing`, `full`, `hand`, `here`, `instead`, `internal`, `invoice`, `ledger`, `load-bearing`, `math`, `missing`, `model`, `name`, `needed`, `new-plan`, `originates`, `point-in-time`, `posting`, `proper`, `rather`, `rebuild`, `recognition`, `reconstruct`, `remaining`, `remaining-service-period`, `revenue-recognition`, `single`, `solely`, `spreading`, `sufficient`, `time`, `two`, `upgrade`, `upgrade-billed`, `wrong`

**กลไก/กระบวนการ (PROCESS):**
`event`, `invoice`, `question`, `upgrade`, `was`, `amount`, `charge`, `computed`, `date`, `designed`, `downstream`, `field`, `manual`, `period`, `remaining`, `removes`, `source`, `time`, `accounting`, `actually`, `adjustment`, `allocation`, `answer`, `anything`, `applied`, `around`, `before`, `billing`, `binary`, `cash-collection`, `cash_collected`, `change`, `close`, `close-month`, `collect-cash`, `conflation`, `customer-facing`, `dashboards`, `data`, `days`, `distinct`, `emitting`, `end`, `entire`, `exports`, `general`, `handler`, `ledger`, `lets`, `logic`, `manually`, `model`, `money`, `must`, `need`, `needed`, `new`, `nowhere`, `paid`, `per-period`, `post-to-gl`, `posting`, `posts`, `prorating`, `proration`, `reading`, `reads`, `received`, `recognition-period`, `recognition-schedule`, `recognized`, `recognized_revenue_schedule`, `reconstructed`, `reconstruction`, `revenue`, `schedule`, `schema`, `second`, `separating`, `service`, `should`, `simplest`, `single`, `start`, `timestamp`, `truth`, `upgrade-billed`, `without`

**เครื่องมือ/ระบบ (TOOL):**
`MRR-dashboard`, `accountant`, `billing-engine`, `general-ledger`, `invoice-service`

**วิธีวิเคราะห์/มาตรฐานที่อ้างถึง (PROTOCOL):**
`cash-vs-accrual data-model separation`, `proration-method redesign`, `revenue-recognition schedule reconstruction`, `synthetic full-cycle-signup replay`, `synthetic mid-cycle-upgrade replay`

**ตัวชี้วัด/เงื่อนไขพิสูจน์ (METRIC):**
`revenue`, `event`, `period`, `recognized`, `timing`, `already`, `amount`, `cash`, `collected`, `data`, `engine`, `manual`, `matches`, `proration`, `where`, `without`, `actually`, `adjustment`, `any`, `billing`, `carries`, `case`, `cash-vs-accrual`, `comparing`, `conflated`, `contains`, `days-remaining-prorated`, `depend`, `distinction`, `diverge`, `does`, `downstream`, `enough`, `entries`, `here`, `isn`, `ledger-posted`, `log`, `other`, `overstates`, `own`, `payload`, `raw`, `reasons`, `reconstruct`, `remaining-service-period`, `same`, `schedule`, `service`, `simply`, `surfaced`, `understates`, `upgrade`, `upgrade-related`, `way`, `whether`, `work`, `zero`

## 2. องค์ความรู้ผู้เชี่ยวชาญที่ควรรู้เพิ่ม (AI-interpretive, Open tier — เฉพาะที่มั่นใจสูง)

- **ASC 606 ("Revenue from Contracts with Customers"), the FASB 5-step revenue recognition model** — the current, standard US GAAP framework (with IFRS 15 as the international equivalent, sharing the same 5-step model, so this reasoning is largely portable). Directly governs this exact issue: under ASC 606 a SaaS company recognizes revenue only as the service is delivered over the subscription period, never the full amount on day one — which is precisely what H1 says the billing engine is failing to do. Confidence: VERIFIED-VIA-SEARCH.
- **ASC 606 contract-modification treatment for mid-term upgrades, "prospective" accounting** — the specific, real, named rule for THIS checkpoint's exact scenario: an upgrade mid-billing-cycle is a "contract modification" event under ASC 606, generally accounted for prospectively (adjusting the remaining revenue schedule going forward), requiring a fresh assessment each time — this is not generic revenue-recognition theory, it is the specific sub-rule for exactly what H1/H3 describe. Confidence: VERIFIED-VIA-SEARCH.
- **Deferred revenue (a.k.a. unearned revenue) as a balance-sheet liability** — the standard accounting treatment for cash collected before the corresponding service is delivered: it sits on the balance sheet as a liability and is recognized into revenue gradually as service is delivered. This directly names the correct behavior H1's fix should produce (a decreasing deferred-revenue balance as the remaining service period elapses) rather than an immediate revenue hit. Confidence: VERIFIED-VIA-SEARCH.
- **The matching principle / accrual-basis accounting** — the fundamental GAAP concept H2 is describing informally ("cash collected" vs. "revenue earned"): accrual accounting recognizes revenue when earned, independent of when cash changes hands, and GAAP requires accrual (not cash) basis for reporting purposes. This is the textbook name for exactly the conflation H2 identifies in the engine's schema. Confidence: VERIFIED-VIA-SEARCH.

## 3. คำที่ชั้น 2 เพิ่มเข้ามาจริง (ไม่ซ้ำกับคำดิบในชั้น 1)

None of the following appear as literal words/phrases in the checkpoint text
(checked against kg_raw_word.md's word table) — they are this layer's
interpretive contribution:

- ASC 606 / "Revenue from Contracts with Customers" (the checkpoint's own
  `adapter_cards` says "revenue-recognition schedule reconstruction" but never
  names the governing standard)
- The 5-step revenue recognition model (identify contract, identify performance
  obligations, determine transaction price, allocate price, recognize revenue)
- "Contract modification" / "prospective treatment" as the specific named ASC 606
  category this exact mid-cycle-upgrade scenario falls under
- Deferred revenue / unearned revenue (the checkpoint says "cash collected" and
  "recognized revenue" but never names the balance-sheet liability account that
  should sit between them)
- The matching principle (H2 describes the conflation mechanistically but never
  names the accounting principle it violates)
- IFRS 15 (the international-equivalent standard, relevant if this company or its
  auditors ever operate outside a pure US-GAAP context — not mentioned anywhere
  in the checkpoint)

## ภาคผนวก: คำเฉพาะของกลไกโปรโตคอล SkillMe เอง (ไม่ใช่คำศัพท์ของประเด็น — ตัดออกจาก glossary หลักโดยตั้งใจ)

`CROSS_ADAPTIVE`, `DESIGN_HYPOTHESIS`, `GENERATIVE_TRANSFORMATIVE`, `KNOWN_DIRECT`, `MECHANISM_HYPOTHESIS`, `STRUCTURAL_HYPOTHESIS`, `TARGETED_SEARCH`
