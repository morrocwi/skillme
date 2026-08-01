# kg_expert_layer — HYP-UIA-046-DEMO-001 (AI-INTERPRETIVE, OPEN TIER)

**This is NOT a readout.** Unlike kg_raw_word.md (a deterministic extraction — every
node is a literal fact about what text appeared where), everything below is an AI's
judgment call about what expertise is relevant. Treat it as a starting point for a
human expert to confirm or correct, not as validated fact. Tier: Open (per this
workspace's readout-not-truth discipline) until reviewed by an actual domain expert.

## Domain(s) identified

- **Payments engineering / card-scheme protocol handling** — the checkpoint's `system_graph`
  nodes (`retry-orchestrator`, `ledger-writer`, `acquirer-gateway "AcquirerX"`) and the
  H1 mechanism (`202 Accepted` queue-ack conflated with settlement) are a textbook
  acquirer-integration bug, not a generic web bug.
- **Distributed-systems consistency / state-machine design** — H2 and H3 both explicitly
  frame the fix as a state-machine problem: H2 proposes an explicit `PENDING_CONFIRMATION`
  state between ack and terminal state; H3 proposes replacing a mutable `ledger.status`
  field with an append-only event log to remove write-ordering races "by construction."
- **Financial reconciliation / accounting controls** — the `registration.query` ("ทำไม
  soft-decline retry ถึงถูกบันทึกเป็น settled ใน ledger"), the `Reconciliation & Ledger
  Integrity (R&LI) board` oversight party, and `reconciliation-job (nightly, 02:00 ICT)`
  as a system node all point to a books-and-records / financial-controls angle, not just
  an engineering one — this is a case where a software bug produces a materially wrong
  financial report (overstated settled volume).
- **Incident analysis / postmortem methodology** — the checkpoint itself already quotes
  an on-call engineer's postmortem language ("we assumed the queue accepting the retry
  meant the payment cleared...") and frames H2 as cross-domain transfer from a prior
  incident (the booking-service double-booking postmortem) — this is exactly the shape of
  postmortem-driven pattern recognition ("we've seen this failure shape before").

## Relevant frameworks/methodologies per domain

**Payments engineering:**
- **ISO 8583 message-field semantics** — CONFIRMED-RELEVANT, already present in the source
  (`translation.adapter_cards` cites "ISO-8583 'field 39' mapping," field 39 being the
  response/action code). Confidence: HIGH (well-established knowledge; ISO 8583 is the
  decades-old standard for card-present/card-not-present authorization messaging and is
  still the dominant wire format acquirers use today).
- **Idempotency keys, in the Stripe/PayPal API-design convention sense** — applies because
  the whole bug class (H1, H2) is "an ack was treated as a terminal success," which is
  precisely what idempotency-key design exists to prevent on the *retry* side (safe
  re-submission) even though this bug is really on the *status-interpretation* side.
  Confidence: VERIFIED-VIA-SEARCH. Stripe's own idempotency docs confirm the current,
  correct framing: the API layer caches the *first* response for a given key and returns
  it on retry, with a documented key-lifecycle (e.g. auto-expiry) and strict parameter-match
  validation — this is the standard practitioners cite, and it is still current in 2026.
- **Acquirer/network response-code taxonomy (e.g. `06`, `91`, `96` soft-decline codes)** —
  CONFIRMED-RELEVANT, literally present in `registration.failure_rule` and
  `discriminating_information`. Confidence: HIGH (these are standard ISO 8583-family
  response codes; a payments engineer would recognize `91` as "issuer/switch inoperative"
  class and `96` as "system malfunction" class — worth a domain expert double-checking the
  exact code table version in use for AcquirerX specifically, since code meanings can be
  scheme- or acquirer-specific).

**Distributed-systems consistency:**
- **Saga pattern / eventual-consistency reconciliation with compensating transactions** —
  applies to the retry-orchestrator's multi-step flow (submit-retry → ack/nack →
  write-settled-flag → reconcile) as a long-running, multi-service transaction that needs
  either explicit compensation or a defined reconciliation sweep, which is exactly what
  the nightly reconciliation-job already is (an ad-hoc, undocumented compensation pass).
  Confidence: VERIFIED-VIA-SEARCH — current material (Microsoft Azure Architecture Center,
  Temporal docs) confirms Saga is still the standard named pattern for this, and explicitly
  states periodic reconciliation-with-compensating-transactions as a companion technique
  when eventual consistency is accepted — which matches this checkpoint's nightly job.
- **Event sourcing / CQRS (event-sourced settlement log)** — directly matches H3's proposal
  almost verbatim ("append-only settlement-event log... deriving the... label as a
  pure read-time projection"). Confidence: VERIFIED-VIA-SEARCH — current fintech
  architecture writeups (e.g. Formance, Iconsolutions) confirm event sourcing + CQRS is the
  named, current pattern for exactly this "single mutable status field is a race-condition
  target" problem in payment/ledger systems; H3 is independently re-deriving a known
  named pattern, not inventing something novel.
- **Formal state machine (explicit terminal vs. non-terminal states) / Petri-net-style
  modeling of the payment lifecycle** — applies because both H1's root cause (missing a
  terminal-vs-non-terminal distinction) and H2's proposed fix (add an explicit
  `PENDING_CONFIRMATION` state) are literally "this state machine has an implicit, wrong
  state model." Confidence: MEDIUM (well-established software-engineering technique;
  I did not search for a more specific named variant beyond generic FSM/Petri-net framing,
  and did not verify whether payments-specific literature has a more specific named model
  than generic FSM design — flagged as open below).

**Financial reconciliation / accounting controls:**
- **Double-entry bookkeeping reconciliation discipline** — applies as the conceptual reason
  "double-counted SETTLED volume" is a real financial-reporting defect and not just a UI
  bug: a settlement ledger that can silently overstate a balance without an offsetting
  entry violates the basic double-entry invariant reconciliation is built to catch.
  Confidence: HIGH (foundational accounting knowledge, not searched this session).
- **COSO Internal Control – Integrated Framework** — applies at the "why does an R&LI board
  exist and why does a nightly reconciliation-job matter" level: COSO's control-activities
  component explicitly names reconciliation as a standard detective control for financial
  accuracy. Confidence: VERIFIED-VIA-SEARCH — confirmed the 2013 COSO Integrated Framework
  (refreshed from the original 1992 version) is still the current, dominant internal-controls
  framework as of this search, and that "reconciliation" is explicitly named within it as a
  control activity. Whether this specific fintech org is actually COSO-scoped (e.g. SOX-
  reporting entity) is NOT knowable from the checkpoint and is flagged as an open question.

**Incident analysis / postmortem methodology:**
- **SRE-style blameless postmortem practice** — applies because the checkpoint already
  contains a verbatim postmortem quote from the on-call engineer and frames the fix search
  as cross-incident pattern transfer, which is the core practice blameless-postmortem
  methodology is designed to produce. Confidence: HIGH (well-established practice,
  not searched this session — Google SRE book naming is stable and I am confident in it).
- **The Five Whys** — applies as a plausible root-cause-drilling technique that would arrive
  at the same H1 mechanism ("why is SETTLED written early?" → "on ack, not callback" →
  "why?" → "early sprint conflated 202 with success") but this is my inference about a
  technique that *could* produce this analysis, not a technique named anywhere in the
  checkpoint. Confidence: MEDIUM (well-established technique; not specific to this
  checkpoint beyond general applicability).

## What I verified via WebSearch vs. asserted from training knowledge

- **Idempotency keys (Stripe convention, current mechanics/key-lifecycle)** — SEARCHED.
  Sources: [Idempotent requests | Stripe API Reference](https://docs.stripe.com/api/idempotent_requests),
  [Designing robust and predictable APIs with idempotency (Stripe blog)](https://stripe.com/blog/idempotency),
  [How Stripe Prevents Double Payment Using Idempotent API](https://newsletter.systemdesign.one/p/idempotent-api)
- **Whether a more specific/current named framework exists for "payment settlement state
  reconciliation" than event sourcing/CQRS** — SEARCHED. Sources:
  [Formance — Account Reconciliation Patterns for High-Volume Fintech](https://www.formance.com/blog/financial-operations/account-reconciliation-patterns-for-high-volume-fintech),
  [CQRS & Event Sourcing in Financial Services (Iconsolutions)](https://iconsolutions.com/blog/cqrs-event-sourcing),
  [Microservices Pattern: Event sourcing](https://microservices.io/patterns/data/event-sourcing.html).
  Result: no more-specific named standard than event sourcing/CQRS turned up; that remains
  the best-fit named framework as of this search.
- **Saga pattern still current/correctly-named for this class of multi-step payment
  transaction with reconciliation-as-compensation** — SEARCHED. Sources:
  [Saga Design Pattern — Azure Architecture Center (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga),
  [Saga Pattern in Microservices: A Mastery Guide (Temporal)](https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices)
- **COSO Internal Control–Integrated Framework, current version and its explicit naming of
  reconciliation as a control activity** — SEARCHED. Sources:
  [Internal Control | COSO](https://www.coso.org/guidance-on-ic),
  [COSO Framework | Definition, Pillars, Principles (Pathlock)](https://pathlock.com/blog/internal-controls/coso-framework/)
- **ISO 8583 "field 39" as the response/action-code field** — ASSERTED (own training
  knowledge, unverified this session — this is long-stable card-industry knowledge and the
  field name/number is also independently corroborated by the checkpoint's own
  `translation.adapter_cards` entry, but I did not run a fresh search on it).
- **Double-entry bookkeeping as the conceptual basis for reconciliation controls** —
  ASSERTED (foundational accounting knowledge, unverified this session).
- **SRE-style blameless postmortem practice (Google SRE book framing)** — ASSERTED
  (well-established practice knowledge, unverified this session).
- **The Five Whys as a plausible-but-not-checkpoint-named technique** — ASSERTED, and
  explicitly flagged above as my own inference rather than anything in the source text.
- **Specific meaning of response codes `06`/`91`/`96` for AcquirerX** — NOT verified either
  way; I gave a generic ISO 8583-family reading (HIGH confidence on the general code-family
  behavior, explicitly flagged as needing acquirer-specific confirmation) but did not search
  for AcquirerX-specific code tables because AcquirerX is a fictional/synthetic vendor name
  in this fixture (see `metadata.simulation: true`) — there is nothing real to look up.

## Vocabulary this adds beyond kg_raw_word.md's raw extraction

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

## Open questions / where a human expert should override this

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
