---
name: system-engineering-dag
description: >
  Production-grade companion skill for software, web, application, API, data, database,
  cache, search, knowledge-graph, AI, security, network, infrastructure, reliability,
  deployment, backup, disaster-recovery, incident, performance, or architecture work.
  When the work is framed as an issue/bug/incident/risk/anomaly, invoke SkillMe first and
  preserve its intake, evidence, hypothesis, rights, and checkpoint semantics; then use this
  skill to map the admitted or still-qualified issue into architecture impact, failure modes,
  tests, migration, recovery, rollback/roll-forward, release, observability, and learning.
  Use before proposing an architecture-impacting fix, schema migration, cache strategy,
  security change, deployment plan, recovery plan, or production release.
---

# System Engineering DAG — production-grade companion to SkillMe

**Status:** architectural/engineering protocol (`Dr` tier unless independently verified).  
**Parent issue-analysis protocol:** `skillme`.  
**Primary contract:** an engineering issue must not jump directly from symptom to fix.

This skill is a system-engineering projection of SkillMe. SkillMe decides **what issue is
actually admitted, what remains hypothesis, what evidence supports/challenges it, who is
affected, and what claim boundary is justified**. This skill decides **which system surfaces
are affected, what architecture and operational consequences follow, what must be tested,
and how a change can be released and recovered safely**.

It does **not** replace SkillMe, and passing engineering gates does not prove a causal/domain
claim is true.

## Mandatory invocation contract with SkillMe

For any reported software/system **Issue**, incident, complaint, anomaly, production failure,
security concern, performance regression, data-quality failure, schema problem, cache problem,
AI-quality regression, deployment failure, or architecture risk:

```yaml
issue_routing:
  MUST:
    - invoke: skillme
      first: true
    - preserve:
        - Q1_issue
        - Q2_user_proposal
        - retained_difference
        - agency_context_query
        - stakeholder_agency_map
        - issue_admission_state
        - hypothesis_evidence_challenge
        - rights_gate
        - VALID_CHECKPOINT_semantics
    - then_invoke: system-engineering-dag
      when:
        - domain_or_topology_includes_software_or_system_engineering
        - proposed_action_changes_architecture_data_code_config_infra_or_operations
        - production_or_recovery_risk_exists
  MUST_NOT:
    - bypass_skillme_intake
    - promote_hypothesis_to_fact
    - treat_VALID_CHECKPOINT_as_solution_or_closure
    - jump_from_symptom_to_fix
    - edit_main_directly
```

If SkillMe has already been run in the same lineage, **reuse that run/checkpoint**. Do not
silently create a fresh issue analysis merely to invoke this skill.

## GitHub Issue contract

For repositories using GitHub, the engineering lineage is:

```yaml
git_issue_workflow:
  policy:
    no_issue_no_work: true
    no_direct_main_edit: true
    no_test_no_merge: true
    no_review_no_release: true
  dag:
    - GitHub_Issue
    - SkillMe_Intake
    - SkillMe_Issue_Admission_or_Qualified_Unresolved
    - SkillMe_Hypothesis_Evidence_Checkpoint
    - System_Engineering_Impact_Map
    - Branch_or_Isolated_Workspace
    - Architecture_and_Change_Design
    - Implementation
    - Verification
    - Pull_Request
    - Human_or_Required_Review
    - Merge
    - Progressive_Release
    - Production_Verification
    - Observe_and_Learn
  traceability:
    issue_must_link_to:
      - branch
      - commits
      - tests
      - pull_request
      - release_if_any
      - incident_or_postmortem_if_any
```

The GitHub Issue is **not** itself proof of root cause. It is a work/traceability container.
SkillMe remains authoritative for issue/hypothesis epistemics.

# Master engineering DAG

```yaml
engineering_dag:

  foundation:
    depends_on: [skillme_issue_lineage]
    nodes:
      - philosophy_and_system_principles
      - product_problem_and_requirements
      - non_functional_requirements
      - glossary_and_ubiquitous_language
      - constraints_and_risk_posture
    outputs:
      - philosophy
      - requirements
      - acceptance_criteria
      - nfr

  domain:
    depends_on: [foundation]
    nodes:
      - domain_discovery
      - entities_value_objects_aggregates
      - business_rules
      - invariants
      - bounded_contexts
      - state_machines
      - domain_events
    gate:
      - domain_boundary_explicit
      - state_transitions_explicit
      - invariants_testable

  information:
    depends_on: [domain]
    parallel_with: [data, knowledge, ux]
    nodes:
      - content_inventory
      - content_model
      - information_architecture
      - taxonomy
      - controlled_vocabulary
      - sitemap
      - navigation
      - search_facets

  data:
    depends_on: [domain]
    parallel_with: [information, knowledge]
    nodes:
      - data_typology
      - data_classification
      - data_ownership
      - source_of_truth
      - data_lineage
      - data_quality
      - data_lifecycle
      - retention
      - deletion
    typology:
      - master
      - reference
      - transactional
      - operational
      - event
      - content
      - observational
      - claim
      - evidence
      - provenance
      - temporal
      - geospatial
      - analytical
      - telemetry
      - derived
      - ai_derived
      - vector
      - knowledge_graph

  knowledge:
    depends_on: [domain, data]
    nodes:
      - vocabulary
      - taxonomy
      - thesaurus_or_concept_scheme
      - ontology
      - knowledge_graph
      - entity_resolution
      - canonical_identity
      - aliases_and_external_ids
      - evidence_and_provenance
      - temporal_validity
      - graph_constraints
      - graph_validation

  system_architecture:
    depends_on: [domain, data]
    nodes:
      - system_context
      - containers
      - components
      - runtime
      - sequence_flows
      - dependency_map
      - data_flow
      - trust_boundaries
      - deployment_view
      - network_view
      - failure_domains
      - degraded_modes
      - capacity_model
    decisions:
      - modular_monolith_vs_services
      - sync_vs_async
      - consistency_model
      - availability_model
      - multi_region_or_single_region

  database:
    depends_on: [data, system_architecture]
    nodes:
      - conceptual_data_model
      - logical_schema
      - physical_schema
      - table_and_type_design
      - pk_fk_unique_check_constraints
      - index_design
      - partitioning
      - transaction_boundaries
      - isolation_and_locking
      - concurrency_control
      - query_and_workload_model
      - read_replicas
      - replication
      - failover
      - connection_pooling
      - sharding_if_justified
      - archive_and_cold_storage
      - migration_architecture
    migration_pattern:
      - expand
      - mixed_version_compatibility
      - migrate
      - validate
      - switch
      - contract
    warning:
      - database_schema_rollback_is_not_assumed_safe
      - data_written_by_new_version_may_require_roll_forward_or_restore

  storage:
    depends_on: [data, database]
    nodes:
      - relational_store
      - document_store_if_needed
      - object_storage
      - blob_storage
      - graph_store
      - vector_store
      - search_index
      - warehouse
      - lake_if_needed
      - archive
    invariant:
      - source_of_truth_for_every_store

  cache:
    depends_on: [system_architecture, database]
    nodes:
      - cache_requirements
      - browser_cache
      - cdn_edge_cache
      - reverse_proxy_cache
      - api_cache
      - application_cache
      - distributed_cache
      - search_graph_vector_cache
      - cache_key_design
      - ttl
      - invalidation
      - cache_warming
      - stale_policy
    strategies:
      - cache_aside
      - read_through
      - write_through
      - write_behind
      - refresh_ahead
    failure_modes:
      - cache_unavailable
      - stale_cache
      - hot_key
      - stampede
      - penetration
      - eviction_storm
      - cold_start
    mitigations:
      - bypass_or_source_fallback
      - coalescing
      - jitter
      - negative_cache
      - rate_limit

  integration:
    depends_on: [domain, security]
    nodes:
      - api_contract
      - api_schema
      - validation
      - errors
      - pagination
      - filtering_sorting
      - versioning
      - deprecation
      - idempotency
      - timeout
      - retry
      - rate_limit
      - external_dependency_contract
      - event_contract
      - queues
      - streams
      - pubsub
      - ordering
      - delivery_semantics
      - replay
      - dead_letter_queue
      - event_schema_evolution

  search_retrieval_ai:
    depends_on: [data, knowledge, storage]
    nodes:
      - lexical_search
      - full_text
      - autocomplete
      - synonym
      - fuzzy
      - faceted
      - geo
      - semantic
      - hybrid_search
      - ranking
      - index_schema
      - zero_downtime_reindex
      - vector_embedding_pipeline
      - sql_retrieval
      - kg_retrieval
      - reranking
      - evidence_assembly
      - llm_generation
      - model_prompt_tool_versioning
      - ai_guardrails
      - ai_evaluation
    invariant:
      - llm_is_not_the_database_or_source_of_truth

  security:
    parallel_with: [system_architecture, infrastructure, implementation]
    nodes:
      - asset_inventory
      - threat_model
      - abuse_cases
      - trust_boundaries
      - authentication
      - authorization
      - rbac_abac_policy
      - least_privilege
      - service_identity
      - session_and_revocation
      - secrets_management
      - key_management
      - encryption_in_transit
      - encryption_at_rest
      - certificate_lifecycle
      - audit
      - privacy
      - data_minimization
      - retention_and_deletion
      - supply_chain_security
      - dependency_scanning
      - secret_scanning
      - sbom
      - artifact_provenance
      - artifact_signing

  network:
    depends_on: [system_architecture, security]
    nodes:
      - dns
      - cdn
      - waf
      - load_balancer
      - ingress
      - public_private_networks
      - segmentation
      - firewall_rules
      - egress_policy
      - service_to_service_policy
      - ddos_protection

  infrastructure:
    depends_on: [system_architecture, network, security]
    nodes:
      - infrastructure_as_code
      - compute
      - containers_or_serverless
      - load_balancing
      - database_infra
      - cache_infra
      - queue_infra
      - search_infra
      - object_storage
      - secrets
      - environments
      - environment_parity
      - runtime_configuration
      - configuration_versioning
      - config_validation
      - config_rollback
      - feature_flags
      - kill_switches

  ux_design_frontend:
    depends_on: [domain, information, security, system_architecture]
    nodes:
      - user_journey
      - user_flow
      - task_flow
      - permission_states
      - loading_empty_error_offline_stale_states
      - wireframe
      - interactive_prototype
      - usability_test
      - design_system
      - design_tokens
      - responsive_rules
      - accessibility
      - frontend_architecture
      - routing
      - rendering_strategy
      - server_client_form_state
      - error_boundaries
      - bundle_and_asset_strategy
      - Design_md

  implementation:
    depends_on: [architecture_ready, issue_branch_created]
    nodes:
      - repository_structure
      - module_boundaries
      - ownership
      - ADRs
      - code
      - architecture_fitness_rules

  test_ecosystem:
    parallel_with: [implementation]
    nodes:
      - static_analysis
      - lint_format_typecheck
      - unit_test
      - property_based_test
      - fuzz_test
      - component_test
      - integration_test
      - contract_test
      - api_test
      - database_test
      - transaction_and_deadlock_test
      - migration_test
      - data_quality_test
      - ontology_and_kg_validation
      - cache_test
      - search_relevance_test
      - event_queue_replay_test
      - ui_component_test
      - visual_regression
      - end_to_end
      - cross_browser_device
      - accessibility_test
      - internationalization_test
      - security_test
      - authorization_negative_test
      - performance_benchmark
      - load_test
      - stress_test
      - spike_test
      - soak_test
      - volume_test
      - scalability_test
      - concurrency_test
      - resilience_test
      - fault_injection
      - chaos_test
      - failover_test
      - backup_restore_test
      - disaster_recovery_test
      - deployment_smoke_test
      - canary_verification
      - production_verification

  reliability:
    depends_on: [system_architecture, test_ecosystem]
    nodes:
      - timeouts
      - retries
      - exponential_backoff
      - jitter
      - circuit_breaker
      - bulkhead
      - backpressure
      - rate_limiting
      - load_shedding
      - idempotency
      - saga
      - outbox
      - degraded_modes
      - overload_strategy
      - autoscaling
      - capacity_forecast

  observability_sre:
    parallel_with: [implementation, release]
    nodes:
      - structured_logs
      - metrics
      - distributed_traces
      - events
      - profiles_if_needed
      - request_correlation_trace_ids
      - golden_signals
      - business_metrics
      - sli
      - slo
      - error_budget
      - actionable_alerting
      - synthetic_monitoring

  backup_restore_dr:
    depends_on: [data, storage, infrastructure]
    nodes:
      - rpo
      - rto
      - backup_scope
      - full_incremental_snapshot_log_backup
      - point_in_time_recovery
      - encrypted_backups
      - immutable_backup
      - independent_backup_location
      - offsite_or_offregion_copy
      - backup_retention
      - restore_architecture
      - granular_restore
      - restore_validation
      - automated_or_rehearsed_restore
      - dr_strategy
      - failover
      - failback
      - dr_drill
      - business_continuity
    invariant:
      - backup_without_successful_restore_test_is_not_recovery

  release_recovery:
    depends_on: [test_ecosystem, backup_restore_dr, observability_sre]
    nodes:
      - build_once_promote_many
      - immutable_artifact
      - sbom_and_attestation
      - release_manifest
      - schema_config_infra_model_prompt_index_versions
      - deployment_strategy
      - rolling_or_blue_green_or_canary
      - startup_liveness_readiness
      - application_rollback
      - config_rollback
      - infrastructure_rollback
      - feature_rollback
      - model_rollback
      - search_index_rollback
      - cache_flush_or_rebuild
      - database_recovery_strategy
      - roll_forward
      - progressive_rollout
      - production_verification
    rule:
      - deploy_is_not_release
      - prefer_roll_forward_when_new_writes_make_old_version_unsafe

  cicd:
    depends_on: [implementation, test_ecosystem, security]
    nodes:
      - checkout
      - dependency_validation
      - lint
      - typecheck
      - build
      - unit_test
      - security_scan
      - integration_gate
      - contract_gate
      - staging_gate
      - migration_rehearsal
      - recovery_gate
      - signed_artifact
      - production_candidate
      - canary
      - progressive_rollout

  incident_operations:
    depends_on: [observability_sre, backup_restore_dr, release_recovery]
    nodes:
      - severity_model
      - incident_commander
      - communication
      - escalation
      - containment
      - evidence_preservation
      - runbooks
      - kill_switch
      - rollback_or_rollforward_or_restore
      - post_recovery_validation
      - blameless_postmortem
      - corrective_actions

  governance_lifecycle:
    nodes:
      - dependency_lifecycle
      - end_of_life_tracking
      - cost_architecture
      - capacity_cost_forecast
      - audit_model
      - architecture_decision_records
      - deprecation
      - data_retention
      - decommission
      - credential_revocation
      - archive_and_evidence_preservation

  learning_loop:
    depends_on: [production, incident_operations]
    inputs:
      - telemetry
      - user_feedback
      - issue_outcome
      - incident_postmortem
      - data_quality
      - security_findings
      - ai_evaluation
      - cost_and_capacity
    loops_back_to:
      - skillme_issue_lineage
      - product_requirements
      - domain_model
      - data_architecture
      - ontology
      - system_architecture
      - ux
      - test_strategy
      - recovery_strategy
```

# Issue → engineering impact compiler

After SkillMe's issue state/hypotheses are available, compile the engineering projection:

```yaml
issue_engineering_projection:
  input:
    - skillme_run_id_or_checkpoint
    - admitted_issue_or_qualified_unresolved
    - confirmed_facts
    - hypotheses
    - unknowns
    - affected_agencies
    - user_proposal
  produce:
    - architecture_impact_map
    - affected_sources_of_truth
    - affected_bounded_contexts
    - affected_data_and_schema
    - affected_runtime_dependencies
    - affected_security_and_privacy_controls
    - failure_mode_map
    - observability_gap_map
    - test_plan
    - migration_plan
    - backup_restore_impact
    - rollback_rollforward_plan
    - release_plan
    - acceptance_and_stop_rules
  forbidden:
    - architecture_change_without_issue_trace
    - destructive_migration_without_recovery_plan
    - cache_change_without_invalidation_and_failure_model
    - production_change_without_observability
    - release_without_test_evidence
```

## Architecture impact map

For every Issue/hypothesis, mark each surface `AFFECTED | NOT_AFFECTED | UNKNOWN`:

```yaml
impact_surfaces:
  - product_requirement
  - domain_rule
  - state_machine
  - information_architecture
  - data_model
  - data_quality
  - ontology_or_kg
  - database_schema
  - transaction_model
  - storage
  - cache
  - api
  - events_queue_stream
  - search
  - vector_retrieval
  - ai_model_prompt_tool
  - frontend
  - ux
  - authentication
  - authorization
  - privacy
  - secrets_crypto
  - network
  - infrastructure
  - configuration
  - dependencies_supply_chain
  - performance_capacity
  - reliability
  - backup_restore
  - disaster_recovery
  - cicd
  - release
  - observability
  - sre_slo
  - incident_runbook
```

`UNKNOWN` is not equivalent to `NOT_AFFECTED`.

# Required failure model

Before an architecture-impacting fix is accepted, ask what happens for at least:

```yaml
failure_catalog:
  - process_crash
  - node_failure
  - region_failure
  - database_unavailable
  - database_corruption
  - bad_schema_migration
  - replica_lag
  - cache_unavailable
  - stale_cache
  - queue_backlog
  - duplicate_event
  - lost_or_delayed_event
  - search_index_corruption
  - external_api_timeout
  - dns_failure
  - certificate_or_secret_expiry
  - credential_compromise
  - disk_or_memory_exhaustion
  - traffic_spike
  - retry_storm
  - partial_network_partition
  - deployment_regression
  - configuration_regression
  - backup_failure
  - restore_failure
  - ai_quality_regression
  - ai_prompt_or_tool_injection
```

Not every issue requires every failure simulation, but every **affected** critical failure mode
must have a test, prevention/control, detection signal, and recovery action or an explicit
accepted-risk record.

# Recovery matrix

```yaml
recovery_classes:
  code:
    options: [rollback, rollforward, traffic_shift]
  configuration:
    options: [version_revert, kill_switch]
  infrastructure:
    options: [iac_revert, replace, failover]
  database_schema:
    options: [compatibility_mode, forward_fix, carefully_verified_reverse_migration, restore]
  data:
    options: [repair, replay, point_in_time_restore, reconciliation]
  cache:
    options: [bypass, flush, rebuild, warm]
  search:
    options: [previous_index, alias_switch, rebuild]
  ai:
    options: [model_rollback, prompt_rollback, retrieval_rollback, disable_feature]
  region:
    options: [failover, traffic_shift, dr_environment]
```

Never write merely `rollback available`. State **what** rolls back, **to which version/state**,
what data compatibility is assumed, how it is validated, and what happens if rollback fails.

# Release manifest

Every production candidate should be traceable as far as applicable:

```yaml
release_manifest:
  issue: REQUIRED
  skillme_lineage: REQUIRED_FOR_ISSUE_WORK
  branch: REQUIRED
  commit_sha: REQUIRED
  artifact_id: REQUIRED
  application_version: REQUIRED
  schema_version: OPTIONAL_IF_UNCHANGED
  migration_version: OPTIONAL_IF_UNCHANGED
  config_version: REQUIRED_IF_CONFIGURED
  infrastructure_version: REQUIRED_IF_INFRA_MANAGED
  feature_flags: RECORD
  dependency_lock: RECORD
  search_index_version: OPTIONAL_IF_USED
  ontology_version: OPTIONAL_IF_USED
  ai_model_version: OPTIONAL_IF_USED
  prompt_version: OPTIONAL_IF_USED
  embedding_version: OPTIONAL_IF_USED
  test_evidence: REQUIRED
  restore_evidence: REQUIRED_IF_RECOVERY_CRITICAL
  rollback_or_rollforward_plan: REQUIRED
```

# Quality gates

```yaml
gates:
  G0_issue:
    requires:
      - skillme_intake_complete
      - issue_state_recorded
      - facts_hypotheses_unknowns_separated

  G1_domain:
    requires:
      - affected_domain_identified
      - business_rules_and_states_understood

  G2_architecture:
    requires:
      - architecture_impact_map
      - dependency_map
      - failure_model
      - security_impact
      - data_impact

  G3_change_design:
    requires:
      - change_plan
      - compatibility_plan
      - migration_plan_if_needed
      - cache_invalidation_plan_if_needed
      - recovery_plan

  G4_verification:
    requires:
      - relevant_test_layers_green
      - security_checks_green_or_explicitly_blocked
      - migration_rehearsal_if_needed
      - recovery_test_if_needed

  G5_pr:
    requires:
      - issue_linked
      - branch_not_main
      - test_evidence
      - review

  G6_release:
    requires:
      - immutable_or_identified_artifact
      - release_manifest
      - observability_ready
      - rollback_or_rollforward_ready
      - canary_or_justified_release_strategy

  G7_production:
    requires:
      - production_verification
      - business_and_technical_signals_healthy
      - no_unaccepted_data_integrity_regression

  G8_learning:
    requires:
      - result_written_back_to_issue_or_incident_lineage
      - unexpected_outcomes_feed_SkillMe_correction_loop
```

# Test selection rule

Do not run tests merely to fill a checklist. Derive tests from the Issue impact/failure map.
At minimum, select from:

- static / lint / type / architecture fitness
- unit / property-based / fuzz
- component / integration / contract / API
- DB constraint / transaction / isolation / deadlock / migration
- data-quality / lineage / provenance
- ontology / KG shape and consistency
- cache hit/miss/expiry/invalidation/stampede/failure
- search relevance/freshness/reindex
- queue duplicate/retry/order/replay/DLQ
- frontend component / visual regression / E2E
- accessibility / browser / device / i18n
- SAST / DAST / SCA / secrets / container / IaC / authn/authz / penetration
- benchmark / load / stress / spike / soak / volume / concurrency
- fault injection / resilience / chaos / failover
- backup integrity / restore / PITR / DR drill
- deployment smoke / health / readiness / canary / production verification
- AI golden-set / groundedness / retrieval / citation / injection / tool-misuse / latency / cost

# Git execution protocol

```yaml
git_execution:
  1_issue:
    action: create_or_link_issue
  2_branch:
    action: create_branch_from_current_default_branch
    forbid: direct_main_edit
  3_plan:
    action:
      - record_skillme_lineage
      - architecture_impact_map
      - test_plan
      - recovery_plan
  4_change:
    action: implement_small_reviewable_change
  5_verify:
    action: run_relevant_tests_and_checkers
  6_pr:
    action: open_pull_request
    body_must_include:
      - closes_or_relates_issue
      - why
      - architecture_impact
      - tests
      - migration
      - security
      - rollback_or_rollforward
      - residual_risk
  7_review:
    action: human_or_required_checker_review
  8_merge:
    precondition: required_gates_green
  9_release:
    action: progressive_release_and_verify
  10_learn:
    action: write_result_back_to_issue_and_SkillMe_lineage
```

# Output contract

For an Issue, report in this order:

1. `SkillMe lineage/status` — admitted / unresolved / checkpoint; confirmed vs hypothesis.
2. `Architecture impact` — affected system surfaces and unknowns.
3. `Failure model` — what can fail because of the issue or proposed change.
4. `Change design` — smallest justified/reversible change first.
5. `Data/schema/cache/security consequences`.
6. `Test ecosystem selection` — exact tests derived from impact.
7. `Migration + compatibility`.
8. `Backup/restore/DR impact`.
9. `Rollback vs roll-forward` with concrete conditions.
10. `Git Issue → branch → PR traceability`.
11. `Release strategy + canary/verification`.
12. `Observability/SLO signals`.
13. `Residual unknowns / accepted risks`.
14. `Learning/correction path back into SkillMe`.

# Hard invariants

- **SkillMe first for Issues.** This skill is not a symptom-to-fix shortcut.
- **Issue != root cause.** A GitHub Issue is a work container, not epistemic proof.
- **No issue, no architecture-changing work** unless an emergency containment exception is
  explicitly recorded under SkillMe.
- **No direct edits to `main`.** Use Issue → branch → verification → PR.
- **No destructive DB migration without compatibility + recovery design.**
- **No cache design without invalidation + stale/failure behavior.**
- **No production release without observability.**
- **No backup claim without restore evidence.**
- **No rollback claim without data/schema compatibility analysis.**
- **No test claim without naming the executed evidence.**
- **No `UNKNOWN` silently rewritten as `NOT_AFFECTED`.**
- **No AI-generated data promoted to ground truth without provenance/verification.**
- **No architecture decision without an owner, consequence, and reversal/deprecation path.**
- **No release closure until production verification and issue/result feedback are recorded.**
