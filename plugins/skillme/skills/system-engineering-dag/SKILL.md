---
name: system-engineering-dag
description: >
  Risk-proportional, machine-verifiable companion skill for software/system engineering.
  For an issue, incident, anomaly, production failure, or architecture-affecting change,
  invoke SkillMe first, preserve its typed issue/hypothesis lineage, then use this skill to
  classify engineering risk, map affected system surfaces, derive mandatory test/recovery
  obligations, choose investigation vs intervention, and control branch/PR/release/learning.
  Use for software, web, API, data, database, cache, search, KG, AI, security, network,
  infrastructure, reliability, performance, deployment, backup/restore, DR, or operations.
---

# System Engineering DAG — operational router

**Status:** `Dr` engineering protocol.  
**Parent protocol:** `skillme`.  
**Machine source of truth:** `system_engineering_dag.json`.  
**Executable validator/compiler:** `system_engineering_dag_kernel.py`.  
**Issue-UI attention profile:** `ux_attention_profile.json` + `ux_attention_kernel.py`.  
**Issue-first wireframe contract:** `WIREFRAME.md`.  
**Detailed on-demand reference:** `REFERENCE.md`.

This file is intentionally short. Do not load the entire engineering reference unless the
impact map says a surface is affected or unknown. The JSON specs and kernels are authoritative
for graph shape, risk routing, typed handoff, obligations, waivers, decision rules, security
assurance, issue-first wireframe rules, and release invariants.

## 1. Mandatory SkillMe handshake

For a reported engineering **Issue**:

1. Invoke `skillme` first.
2. Reuse the same SkillMe run/checkpoint lineage.
3. Do not promote hypotheses to facts.
4. Create the typed handoff below.
5. Only then run engineering classification/impact/obligation logic.

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

If `issue_state == NO_ISSUE_UNDER_DECLARED_READOUT`, do not start an engineering intervention
unless a new/corrected SkillMe lineage admits one.

## 2. Work-item abstraction, GitHub adapter

The universal primitive is a **work item/change record**, not GitHub itself.

```yaml
work_item_adapter:
  canonical: WORK_ITEM
  github: Issue
  gitlab: Issue
  jira: Ticket
```

For this repository, GitHub is the active adapter:

`Issue → SkillMe → typed handoff → risk/impact → branch → change → verification → PR → review → release → production verification → outcome back to SkillMe`

Never edit `main` directly.

## 3. Risk-proportional routing

Do not run the full protocol for every typo.

```yaml
risk_tiers:
  L0_TRIVIAL:
    examples: [copy_typo, cosmetic_css]
    minimum: [issue_trace, targeted_test]

  L1_STANDARD:
    examples: [ordinary_bug, small_feature]
    minimum: [issue_trace, impact_map, targeted_test, rollback_plan]

  L2_HIGH:
    triggers:
      - database_change
      - auth_change
      - privacy_change
      - public_api_change
      - infrastructure_change
      - payment_change
      - multi_tenant_boundary_change
      - encryption_key_change
      - supply_chain_build_change
    requires:
      - typed_handoff
      - architecture_review
      - security_review
      - test_plan
      - migration_plan_if_applicable
      - recovery_plan
      - release_strategy
      - production_verification

  L3_CRITICAL:
    triggers:
      - irreversible_data_change
      - large_blast_radius
      - regulated_data
      - multi_region_change
      - safety_critical
      - active_data_corruption
    requires:
      - independent_review
      - full_test_obligation_matrix
      - restore_evidence
      - rollback_or_rollforward
      - progressive_release
      - post_change_review
```

The kernel is the source of truth for exact tier obligations.

## 4. Investigation != intervention

An engineering issue may require instrumentation before a fix hypothesis is justified.

```yaml
change_mode:
  INVESTIGATION:
    may:
      - temporary_logging
      - metrics
      - tracing
      - profiling
      - reproduction_test
      - diagnostic_endpoint
    may_claim_fix: false

  INTERVENTION:
    requires:
      - change_plan
      - test_obligations
      - recovery_plan
    may_claim_fix: true

  EMERGENCY_CHANGE:
    allowed_for:
      - active_customer_harm
      - active_security_incident
      - service_unavailable
      - active_data_corruption
    may_bypass:
      - normal_review_sequence
      - full_test_suite
    never_bypass:
      - traceability
      - owner
      - minimum_test
      - rollback_or_containment
      - evidence_preservation
      - post_hoc_review
```

## 5. Architecture impact compiler

Mark every relevant surface:

`AFFECTED | NOT_AFFECTED | UNKNOWN`

`UNKNOWN` is never silently converted to `NOT_AFFECTED`.

Core surfaces include product/domain/state, data/KG, DB/transactions/storage/cache, API/events,
search/vector/AI, frontend/UX, authn/authz/privacy/secrets, multi-tenancy, network/infra/config/
supply-chain, performance/reliability, external side effects, data integrity, backup/restore/DR,
CI/CD/release, observability, SLOs, incident runbooks, and — for issue-analysis/work-item
products — `issue_management_ui`.

For a critical surface, `UNKNOWN` creates an investigation obligation and blocks release unless
an explicit, time-bounded waiver is valid.

## 6. Obligations are derived, not checklist-selected

Use:

`Impact → Failure mode → Control → Test → Evidence → Recovery`

Examples:

- `database_schema=AFFECTED` ⇒ migration rehearsal, mixed-version compatibility, partial-failure
  test, rollback-or-roll-forward, restore path.
- `cache=AFFECTED` ⇒ key review, invalidation test, stale-data test, cache-down test, cache
  security review.
- `authorization=AFFECTED` ⇒ negative authorization and cross-tenant access tests.
- `multi_tenancy=AFFECTED` ⇒ tenant identity, data/cache isolation, noisy-neighbor, tenant restore.
- `data_integrity=AFFECTED` ⇒ stop/scope writes, repair/replay plan, reconciliation, restore path.
- `backup_restore=AFFECTED` ⇒ backup integrity, restore test, key-recovery test, business
  invariant reconciliation.
- `payment_or_external_side_effects=AFFECTED` ⇒ idempotency, side-effect ledger,
  reconciliation, replay/duplicate policy.
- `issue_management_ui=AFFECTED` ⇒ load `ux_attention_profile.json` and compile the issue-first
  wireframe obligations before approving the wireframe.

Use the kernels to compile exact obligations. Do not manually invent a “complete” checklist.

## 7. Issue-first wireframe is mandatory for Issue/Work-Item screens

If the primary screen task is `understand_issue`, `act_on_issue`, `incident_response`,
`work_item_triage`, or `issue_analysis`, **MUST load `WIREFRAME.md` and
`ux_attention_profile.json`**.

The first viewport must answer, without scrolling:

1. what the issue is;
2. current issue state;
3. risk/severity and affected scope;
4. confirmed vs unknown;
5. primary next action;
6. owner;
7. freshness / last evidence time.

This is the **Issue Capsule**. Decorative hero, branding-only blocks, generic KPI dashboards,
large nonessential images, and navigation chrome must not outrank it.

Research-informed vertical attention prior used by the profile:

```text
Screen 1: 57% of observed page-viewing time  → attention index 100
Screen 2: 17%                                → index ~30; ~70% drop vs Screen 1
Screen 3:  7%                                → index ~12; ~59% drop vs Screen 2
Below 3: 19% aggregate long tail             → NOT 19% per later screen
```

The figures are an aggregate research prior, **not a universal behavioral law**. The design
contract is therefore: prioritize Issue comprehension in the first viewport, then verify with
actual usability measures (`time_to_identify_issue`, `time_to_identify_status`,
`time_to_identify_next_action`, `scroll_before_issue_comprehension_rate`,
`critical_unknown_missed_rate`).

Hard fail if the Issue statement or required next action is hidden below the first viewport,
unknowns are visually collapsed into certainty, a false floor hides continuation, or mobile
requires horizontal scrolling to understand the core Issue.

## 8. Architecture decisions are evidence-gated

Listing a technology does not justify using it. The canonical spec defines `activate_if` and
`forbid_if` rules for high-complexity decisions including sharding, microservices, multi-region,
knowledge graphs, and vector retrieval.

Examples:

- do not shard without a measured capacity/partition limit and a partitionable access pattern;
- do not introduce microservices without real ownership/scaling/failure boundaries and an
  operational platform capable of carrying the complexity;
- do not add multi-region if a single region already satisfies declared SLO/RPO/RTO/residency;
- do not add KG/vector infrastructure when simpler relational/lexical retrieval meets the need.

World-class engineering includes knowing what **not** to build.

## 9. Security assurance is proportional

The canonical spec defines:

- `BASELINE` — ordinary low-sensitivity systems;
- `SENSITIVE` — personal/confidential data, multi-tenant boundaries, payments/identity;
- `HIGH_ASSURANCE` — regulated/high-impact data, large blast radius, safety/critical services.

Higher levels add independent review/adversarial testing, hardened build provenance, recovery
drills, and explicit residual-risk acceptance. Do not apply identical security ceremony to all
changes, and do not downgrade a high-impact surface merely to simplify delivery.

## 10. Cache security invariants

When cache is affected:

- permission/security context must participate in the cache key when responses are contextual;
- a cache hit must never bypass authorization;
- private tenant responses must not enter shared caches;
- secrets/credentials must not be cached;
- stale private data behavior must be explicit.

## 11. Multi-tenancy

If multi-tenancy is present, treat it as an explicit affected surface and cover tenant identity,
data isolation, cache isolation, quota/noisy-neighbor behavior, tenant-scoped audit,
tenant deletion, migration, and tenant-scoped restore.

## 12. Recovery is business correctness, not infrastructure boot

Hard invariants:

- backup without successful restore evidence is not recovery;
- schema rollback is not assumed safe;
- restore is incomplete until business invariants are reconciled;
- encrypted backup is useless without a key-recovery path;
- external side effects require ledger/reconciliation semantics;
- new-version writes may make roll-forward safer than binary rollback.

Never write merely `rollback available`. State what changes, target version/state, data
compatibility assumptions, validation, and failure-of-rollback behavior.

## 13. SLO/RPO/RTO precede architecture where relevant

Criticality targets feed architecture:

`Product criticality → SLI/SLO + RPO/RTO → architecture/redundancy/recovery design`

Do not invent expensive multi-region/redundancy patterns before targets justify them.

## 14. Observability is a design surface

Do not stop at “logs, metrics, traces”. For affected production paths define telemetry schema,
semantic naming, cardinality budget, sampling, PII redaction, ownership, retention/cost, trace
propagation, and actionable alerts.

## 15. Waivers, ownership, and freshness

A `MUST` may be waived only through an auditable exception:

```yaml
waiver:
  control: REQUIRED
  reason: REQUIRED
  risk: REQUIRED
  compensating_control: REQUIRED
  approver: REQUIRED
  expires_at: YYYY-MM-DD
  review_due_at: YYYY-MM-DD
```

Critical artifacts/nodes carry owner/evidence/status and verification freshness. A stale DR
test, threat model, capacity model, or dependency map is not silently treated as current.

## 16. Release contract

A production candidate records, as applicable:

- work item + SkillMe run
- branch + commit + artifact
- risk tier
- schema/migration/config/infra/search/ontology/model/prompt versions
- test evidence
- recovery decision
- observability readiness
- production verification plan

`deploy != release`. Select direct/rolling/canary/blue-green/shadow/progressive strategy by
risk/blast radius/reversibility, not ideology.

## 17. Machine verification

From this directory:

```bash
python3 system_engineering_dag_kernel.py
python3 system_engineering_dag_kernel.py --self-test
python3 ux_attention_kernel.py
python3 ux_attention_kernel.py --self-test
```

The engineering validator proves graph/protocol structure. The UX attention validator protects
the research labeling, vertical attention bands, Issue Capsule fields, first-view hard fails,
and conditional issue-UI obligations. Neither proves a causal/domain hypothesis is true.

## 18. On-demand reference loading

- Load `WIREFRAME.md` for issue/work-item/incident screens.
- Load `REFERENCE.md` only for affected/unknown engineering surfaces.

The deep reference covers domain/data/KG; DB/storage/cache; API/events/search/AI; security;
network/infra; UX/frontend/design; test/performance/resilience; backup/DR; release/recovery;
observability/SRE/incidents/governance/decommission.

## 19. Output order

For a qualifying Issue:

1. SkillMe lineage/status.
2. Risk tier and change mode.
3. Affected/unknown architecture surfaces.
4. Investigation obligations for unknowns.
5. Derived engineering obligations.
6. If UI is involved: Issue Capsule + attention-band wireframe placement.
7. Smallest justified change.
8. Migration/data/cache/security consequences.
9. Test evidence required.
10. Recovery: rollback vs roll-forward vs restore.
11. Work item → branch → PR traceability.
12. Release strategy and production verification.
13. Observability/SLO signals.
14. Waivers, residual risk, freshness.
15. Outcome/correction back to SkillMe.

## Hard invariants

- SkillMe first for Issues.
- Issue/work item is traceability, not root-cause proof.
- Test pass is not domain-truth proof.
- `UNKNOWN != NOT_AFFECTED`.
- Issue-management UI must answer the Issue in the first viewport.
- Attention percentages are research priors, not universal laws.
- No direct `main` edits.
- No destructive migration without compatibility and recovery design.
- No cache change without invalidation and security behavior.
- No production release without observability and verification.
- No backup claim without restore evidence.
- No recovery closure before business invariant reconciliation.
- No unbounded waiver.
- No complexity merely because the reference lists it.
