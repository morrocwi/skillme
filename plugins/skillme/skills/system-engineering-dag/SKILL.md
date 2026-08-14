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
**Detailed on-demand reference:** `REFERENCE.md`.

This file is intentionally short. Do not load the entire engineering reference unless the
impact map says a surface is affected or unknown. The JSON spec and kernel are authoritative
for graph shape, risk routing, typed handoff, obligations, waivers, and release invariants.

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
search/vector/AI, frontend/UX, authn/authz/privacy/secrets, network/infra/config/supply-chain,
performance/reliability, external side effects, backup/restore/DR, CI/CD/release, observability,
SLOs, and incident runbooks.

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
- `backup_restore=AFFECTED` ⇒ backup integrity, restore test, key-recovery test, business
  invariant reconciliation.
- `payment_or_external_side_effects=AFFECTED` ⇒ idempotency, side-effect ledger,
  reconciliation, replay/duplicate policy.

Use the kernel to compile exact obligations. Do not manually invent a “complete” checklist.

## 7. Optional complexity is opt-in

KG, vector search, dedicated search infrastructure, sharding, multi-region, microservices, and
similar complexity are **not universal requirements**. Activate them only when evidence and
requirements justify them.

World-class engineering includes knowing what **not** to build.

## 8. Cache security invariants

When cache is affected:

- permission/security context must participate in the cache key when responses are contextual;
- a cache hit must never bypass authorization;
- private tenant responses must not enter shared caches;
- secrets/credentials must not be cached;
- stale private data behavior must be explicit.

## 9. Multi-tenancy

If multi-tenancy is present, treat it as an explicit affected surface and cover tenant identity,
data isolation, cache isolation, quota/noisy-neighbor behavior, tenant-scoped audit,
tenant deletion, migration, and tenant-scoped restore.

## 10. Recovery is business correctness, not infrastructure boot

Hard invariants:

- backup without successful restore evidence is not recovery;
- schema rollback is not assumed safe;
- restore is incomplete until business invariants are reconciled;
- encrypted backup is useless without a key-recovery path;
- external side effects require ledger/reconciliation semantics;
- new-version writes may make roll-forward safer than binary rollback.

Never write merely `rollback available`. State what changes, target version/state, data
compatibility assumptions, validation, and failure-of-rollback behavior.

## 11. SLO/RPO/RTO precede architecture where relevant

Criticality targets feed architecture:

`Product criticality → SLI/SLO + RPO/RTO → architecture/redundancy/recovery design`

Do not invent expensive multi-region/redundancy patterns before targets justify them.

## 12. Observability is a design surface

Do not stop at “logs, metrics, traces”. For affected production paths define telemetry schema,
semantic naming, cardinality budget, sampling, PII redaction, ownership, retention/cost, trace
propagation, and actionable alerts.

## 13. Waivers and freshness

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

Critical artifacts must carry owner/evidence/status and verification freshness. A stale DR test,
threat model, capacity model, or dependency map is not silently treated as current.

## 14. Release contract

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

## 15. Machine verification

From this directory:

```bash
python3 system_engineering_dag_kernel.py
python3 system_engineering_dag_kernel.py --self-test
```

The validator proves protocol structure such as node uniqueness, dependency existence,
acyclicity, release-gate ancestry, destructive-change recovery paths, typed handoff, risk
routing, impact-derived obligations, waiver shape, and release-record requirements.

It does **not** prove that the user's causal hypothesis or engineering decision is true.

## 16. On-demand reference loading

Read `REFERENCE.md` only for affected/unknown surfaces. Use its sections for:

- domain/data/KG
- DB/storage/cache
- API/events/search/AI
- security/privacy/IAM/supply-chain
- network/infrastructure
- UX/frontend/design
- test ecosystem/performance/resilience
- backup/restore/DR
- release/rollback/roll-forward
- observability/SRE/incidents/governance/decommission

## 17. Output order

For a qualifying Issue:

1. SkillMe lineage/status.
2. Risk tier and change mode.
3. Affected/unknown architecture surfaces.
4. Investigation obligations for unknowns.
5. Derived engineering obligations.
6. Smallest justified change.
7. Migration/data/cache/security consequences.
8. Test evidence required.
9. Recovery: rollback vs roll-forward vs restore.
10. Work item → branch → PR traceability.
11. Release strategy and production verification.
12. Observability/SLO signals.
13. Waivers, residual risk, freshness.
14. Outcome/correction back to SkillMe.

## Hard invariants

- SkillMe first for Issues.
- Issue/work item is traceability, not root-cause proof.
- Test pass is not domain-truth proof.
- `UNKNOWN != NOT_AFFECTED`.
- No direct `main` edits.
- No destructive migration without compatibility and recovery design.
- No cache change without invalidation and security behavior.
- No production release without observability and verification.
- No backup claim without restore evidence.
- No recovery closure before business invariant reconciliation.
- No unbounded waiver.
- No complexity merely because the reference lists it.
