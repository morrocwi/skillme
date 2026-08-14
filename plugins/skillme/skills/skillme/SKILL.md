---
name: skillme
description: >
  Load before analyzing any reported issue, incident, complaint, conflict, risk, anomaly,
  policy question, or "what should we do about X" decision — software bugs, customer
  complaints, organizational conflicts, research anomalies, social/policy issues, and
  everyday decisions all qualify. Gives the SkillMe protocol: a mandatory two-question intake
  gate, retained-difference issue framing, stakeholder-agency mapping, bidirectional evidence
  challenge, and three-lane solution generation. For software/system engineering issues,
  preserve this SkillMe lineage and invoke the companion `system-engineering-dag` skill before
  an architecture-impacting fix.
---

# SkillMe — readout-first issue analysis protocol

**Developed by Yaoharee Lahtee.** SkillMe is a philosophy-first protocol for turning a reported
issue into a finite, auditable analysis instead of a guessed answer. It is built on the same
readout-first foundation as `information-discrete-math` and `readout_genesis`: everything you
can act on is a **finite retained difference**, not the world itself.

**Tier: `Dr` (design rationale)** — this is an architectural synthesis of established methods
(RCA, FMEA, stakeholder mapping, GRADE, PRISMA, systems thinking, decision analysis), not a
proven theorem. The bundled kernel (`skillme_protocol_kernel.py`) only verifies **protocol
structure** (required fields, enum validity, cross-references, gate order) — it does **not**
verify that any domain claim, cause, or fix is actually true. Say so when you report results.

This file is a self-contained operational summary shipped with the plugin. The canonical spec
(`SKILLME.md`) and the standalone protocol kernel (`skillme_protocol_kernel.py`) live in the
full repo root — they are **not** installed with this plugin. Clone the whole repo if you need
the full spec or want to run the root kernel yourself: `https://github.com/morrocwi/skillme`.

## The one commitment

> Issue = a **retained difference** that, under a declared agency, context, and query,
> changes what some agency can do, know, claim, be responsible for, or redirect.

Not "issue = what's wrong" and not "issue = what the loudest stakeholder feels". Zero and
unresolved are different things: **`0` = no relevant difference found under this operator;
`⊥` = the tool/evidence/resolution cannot decide yet.** Never report one as the other.

## Before you start analyzing anything: the Two-Question Intake Gate

Every SkillMe run opens with exactly two questions, asked together, before any translation,
stakeholder mapping, causal analysis, or candidate generation happens:

1. **Q1 — Issue:** "Issue คืออะไร? กรุณาอธิบายสิ่งที่เกิดขึ้นหรือประเด็นที่ต้องการให้วิเคราะห์" /
   "What is the issue? Describe what happened or what needs analysis."
2. **Q2 — User proposal:** "คุณมีข้อเสนอหรือแนวคิดเกี่ยวกับประเด็นนี้ไหม? หากไม่มี ตอบว่า 'ไม่มี' ได้" /
   "Do you have a proposal or idea about this? If not, you can answer 'none'."

Rules:
- Q1 must be non-blank. Q2 **must be answered**, but "none" / "ไม่มี" / "skip" is a complete,
  valid answer (`PROPOSAL_ABSENT_DECLARED`) — never a missing value, never silently inferred.
- The only exception is an **emergency containment bypass**: if there's ongoing harm, you may
  do the minimum reversible containment action (stop, isolate, preserve evidence) with a
  recorded `reason/scope/rights_check/owner/stop_rule/rollback_rule/evidence_preservation/
  review_due_at` — but you may NOT conclude a cause, pick a fix, or make a decision under this
  bypass. After containment, go back to waiting for Q1/Q2.
- Never add a third mandatory intake question before analysis is allowed to start.

Once both are answered: if Q2 has content, mode defaults to `HYBRID_BLIND_COMPARE`; if Q2
declares absence, mode is `AI_INDEPENDENT`.

## Core moves, in order

1. **Protect** — only if there's ongoing harm; minimal, reversible, no causal claims.
2. **Read philosophically** — separate the retained difference, prior state, context/query, and
   readout resolution. Ask only for what's missing.
3. **Map agencies** — run named / impact / dependency / rights / power / knowledge /
   representation / horizon / adversarial / boundary scans. Distinguish affected, observing,
   knowledge, voice, decision, intervention, resource, veto, accountable, oversight,
   represented, future/latent roles. **Stakeholder ≠ agency**.
4. **Compile perspectives** — keep a dissent ledger; never silently choose the powerful party's
   framing as the overview.
5. **Admit the issue** — `ISSUE_ADMITTED` / `NO_ISSUE_UNDER_DECLARED_READOUT` / `UNRESOLVED`.
6. **Detect domain + topology**, route to adapters without letting an adapter promote its own
   evidence tier.

### Mandatory software/system engineering adapter

If step 6 detects a software, web, application, API, data, database/schema, cache, search,
knowledge-graph, AI, security/privacy/IAM, network, infrastructure, reliability, performance,
deployment, backup/restore, disaster-recovery, incident-response, or production-operations
Issue, **MUST invoke the companion `system-engineering-dag` skill** before proposing or
implementing an architecture-impacting fix.

Do not pass prose loosely. Compile this typed handoff from the **same SkillMe lineage**:

```yaml
skillme_engineering_handoff:
  skillme_run_id: REQUIRED
  work_item_id: REQUIRED
  issue_state: ISSUE_ADMITTED | UNRESOLVED | NO_ISSUE_UNDER_DECLARED_READOUT
  confirmed: []
  hypotheses: []
  unknowns: []
  affected_agencies: []
  rights_constraints: []
  evidence_refs: []
  continuation_record: REQUIRED
```

Routing rules:

```yaml
system_engineering_issue_route:
  first: skillme
  then:
    typed_handoff: skillme_engineering_handoff
    invoke: system-engineering-dag
    before:
      - architecture_fix
      - schema_migration
      - cache_strategy_change
      - security_change
      - infrastructure_change
      - production_release
  work_item_adapter:
    canonical: WORK_ITEM
    github: Issue
  git_lineage:
    - GitHub_Issue
    - branch
    - tests_checker
    - Pull_Request
    - required_review
    - merge
    - release_strategy
    - production_verification
  forbid:
    - direct_main_edit
    - symptom_to_fix_jump
    - treating_issue_as_root_cause_proof
    - treating_test_pass_as_domain_truth_proof
```

If the current run already has a SkillMe checkpoint, **reuse the same lineage**. Do not create a
second intake/hypothesis lineage merely to call the engineering adapter. The companion's
architecture/test/recovery gates cannot promote a SkillMe hypothesis into fact. If SkillMe's
state is `NO_ISSUE_UNDER_DECLARED_READOUT`, the engineering companion must not silently turn
that into an intervention.

7. **Generate competing hypotheses**, then run the **Hypothesis Evidence Challenge**: for every
   load-bearing hypothesis, record support and challenge searches in both international and
   local-context tracks. Separate metadata verification from scope verification. Never write
   `LOCAL_EVIDENCE_NOT_FOUND` as `NO_LOCAL_EVIDENCE_EXISTS`. Never count citations as votes.
8. **Certify the hypothesis portfolio** — three lanes (Known-Direct / Cross-Adaptive /
   Generative-Transformative), each with mechanism, falsifier, legal relevance, and
   representation lineage. `STOP_AT_HYPOTHESIS` creates a valid resumable checkpoint, not a
   decision or closure.
9. **Generate candidates** — genuinely different three-lane candidates. If only one or two
   admissible lanes exist, report `CANDIDATE_SET_PARTIAL_1/2`; do not fabricate a third.
10. **Decide / Act / Verify / Correct** — freeze decision criteria before outcome, state
    stop/rollback rules, and treat correction/withdrawal as reliability rather than failure.

## Hard invariants

- Never let authority substitute for evidence, or correlation substitute for intervention-
  supported cause.
- Never let stakeholder utility override a rights gate.
- Never call consultation co-decision when participants cannot change the outcome.
- Never resume `STOP_AT_HYPOTHESIS` by silently starting a new lineage; reuse
  `continuation_record`, opening a correction record when information changed.
- Never treat `VALID_CHECKPOINT` as a decision, success, or closure.
- For qualifying software/system Issues, never bypass `system-engineering-dag` before an
  architecture-impacting fix, migration, recovery plan, or production release.
- Never let the engineering companion collapse `UNKNOWN` into `NOT_AFFECTED`.

## Output shape

Intake confirmation → issue in plain language → affected/involved agencies (including the
voiceless) → immediate containment if any → confirmed vs hypothesis vs unknown → evidence
for/against hypotheses (global + local) → user's proposal and its treatment → three-lane
candidates → smallest reversible test → who decides/acts/checks → success/falsification rule →
what would make you revise this.

For qualifying software/system Issues, append the companion projection: typed handoff → risk
level/change mode → architecture impact → investigation/test obligations → migration/
compatibility → backup/restore/DR → rollback/roll-forward → work-item/branch/PR traceability →
release/production verification → observability/SLO → waiver/freshness/residual risk →
correction back into SkillMe.

Internal SkillMe vocabulary stays in the technical/audit trail; do not force the user to learn
it unless they ask.

## Downstream checkpoint tooling

Reaching `STOP_AT_HYPOTHESIS` is not closure. In the full repo:

- `communication_glossary/` turns the checkpoint into shared vocabulary and Human/AI role/skill
  plans.
- `doc_ecosystem_bridge/bridge.py` bridges the checkpoint into project hypothesis/decision
  artifacts without falsely turning a hypothesis into an ADR.
- `run_pipeline.py` orchestrates those repo-root tools while preserving lineage.

## Verify before you claim

The root kernel is not part of this plugin subtree. In a full clone:

```bash
python3 skillme_protocol_kernel.py --self-test
```

For the engineering companion, its own machine source of truth and kernel **are** shipped in
the plugin subtree; see `../system-engineering-dag/SKILL.md`.

## Session-tracking contract

Installing this plugin also installs a fail-closed `Stop` hook that, for turns where SkillMe
was loaded, checks that run phases were structurally tracked and, when the full repo's bridge is
actually available and a `VALID_CHECKPOINT` was reached, that the checkpoint bridge was run.
If a required action is missing, the hook names what is missing; it does not silently claim the
run is complete.
