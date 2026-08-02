# kg_expert_layer — HYP-SKILLME-BILLING-ACCT-DEMO-001 (AI-INTERPRETIVE, OPEN TIER)

**This is NOT a readout.** Unlike kg_raw_word.md (a deterministic extraction — every
node is a literal fact about what text appeared where), everything below is an AI's
judgment call about what expertise is relevant. Treat it as a starting point for a
human expert (a real accountant/controller, a real revenue-recognition specialist)
to confirm or correct, not as validated fact. Tier: Open (per this workspace's
readout-not-truth discipline) until reviewed by an actual domain expert.

## Domain(s) identified

- **US GAAP revenue recognition (ASC 606) / SaaS accounting** — the whole issue is
  literally a revenue-recognition-timing problem; H1's proration proposal and H3's
  "schedule reconstruction" framing both map directly onto this standard's own
  vocabulary and rules.
- **Fundamental accounting method (accrual vs. cash basis, matching principle)** —
  H2's core claim ("revenue field is really cash-collected, not accrual") is
  precisely the cash-vs-accrual distinction accounting theory names explicitly.
- **SaaS billing/contract-modification engineering practice** — the specific
  operational question of HOW a billing engine should represent a mid-cycle
  upgrade event has an established industry practice pattern, not just a general
  accounting rule.

## Relevant frameworks/methodologies per domain

- **ASC 606 ("Revenue from Contracts with Customers"), the FASB 5-step revenue
  recognition model** — the current, standard US GAAP framework (with IFRS 15 as
  the international equivalent, sharing the same 5-step model, so this reasoning
  is largely portable). Directly governs this exact issue: under ASC 606 a SaaS
  company recognizes revenue only as the service is delivered over the
  subscription period, never the full amount on day one — which is precisely what
  H1 says the billing engine is failing to do. Confidence: VERIFIED-VIA-SEARCH.
- **ASC 606 contract-modification treatment for mid-term upgrades, "prospective"
  accounting** — the specific, real, named rule for THIS checkpoint's exact
  scenario: an upgrade mid-billing-cycle is a "contract modification" event under
  ASC 606, generally accounted for prospectively (adjusting the remaining revenue
  schedule going forward), requiring a fresh assessment each time — this is not
  generic revenue-recognition theory, it is the specific sub-rule for exactly
  what H1/H3 describe. Confidence: VERIFIED-VIA-SEARCH.
- **Deferred revenue (a.k.a. unearned revenue) as a balance-sheet liability** —
  the standard accounting treatment for cash collected before the corresponding
  service is delivered: it sits on the balance sheet as a liability and is
  recognized into revenue gradually as service is delivered. This directly names
  the correct behavior H1's fix should produce (a decreasing deferred-revenue
  balance as the remaining service period elapses) rather than an immediate
  revenue hit. Confidence: VERIFIED-VIA-SEARCH.
- **The matching principle / accrual-basis accounting** — the fundamental GAAP
  concept H2 is describing informally ("cash collected" vs. "revenue earned"):
  accrual accounting recognizes revenue when earned, independent of when cash
  changes hands, and GAAP requires accrual (not cash) basis for reporting
  purposes. This is the textbook name for exactly the conflation H2 identifies in
  the engine's schema. Confidence: VERIFIED-VIA-SEARCH.

## What I verified via WebSearch vs. asserted from training knowledge

- **ASC 606's 5-step model, current status, and its application to SaaS
  subscription revenue timing** — SEARCHED. Sources:
  [SaaS Revenue Recognition Under ASC 606 — Maxio](https://www.maxio.com/blog/saas-revenue-recognition-asc-606),
  [ASC 606 Revenue Recognition: 5 Steps & Compliance Guide — DualEntry](https://www.dualentry.com/blog/asc-606-revenue-recognition)
- **ASC 606's specific contract-modification / prospective-treatment rule for
  mid-term SaaS upgrades** — SEARCHED. Sources:
  [Handling Mid-Contract Upgrades and Cross-Sells in SaaS Billing — Ordway](https://ordwaylabs.com/blog/handling-mid-contract-upgrades-and-cross-sells-in-saas-billing/),
  [SaaS revenue recognition: ASC 606 compliance — Orb](https://www.withorb.com/blog/saas-revenue-recognition-guide)
- **Deferred/unearned revenue as a balance-sheet liability, recognized gradually
  as service is delivered** — SEARCHED. Sources:
  [Deferred Revenue Explained: Why It's a Liability in SaaS — Baremetrics](https://baremetrics.com/blog/is-deferred-revenue-a-liability),
  [Deferred Revenue in SaaS: Examples & Best Practices — Maxio](https://www.maxio.com/saaspedia/deferred-revenue)
- **The matching principle and accrual-vs-cash-basis distinction, GAAP
  requirement of accrual basis** — SEARCHED. Sources:
  [Cash basis vs. accrual basis — AccountingTools](https://www.accountingtools.com/articles/cash-basis-vs-accrual-basis-accounting.html),
  [The Matching Principle — insightsoftware](https://insightsoftware.com/encyclopedia/the-matching-principle/)
- **Whether this specific company is a public company subject to SOX 404 internal-
  controls requirements, or subject to an external audit at all** — NOT knowable
  from the checkpoint (synthetic fixture, `metadata.simulation: true`) — not
  asserted either way, flagged as open below.
- **IFRS 15's exact degree of practical equivalence to ASC 606 for this specific
  scenario** (stated as "largely portable" above) — ASSERTED from the search
  summary's own framing, not independently cross-checked against the IFRS 15
  text directly this session.

## Vocabulary this adds beyond kg_raw_word.md's raw extraction

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

## Open questions / where a human expert should override this

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
