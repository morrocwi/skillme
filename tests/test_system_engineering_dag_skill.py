from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins" / "skillme" / "skills" / "system-engineering-dag"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCE = SKILL_DIR / "REFERENCE.md"
SPEC = SKILL_DIR / "system_engineering_dag.json"
KERNEL = SKILL_DIR / "system_engineering_dag_kernel.py"
MAIN_SKILL = ROOT / "plugins" / "skillme" / "skills" / "skillme" / "SKILL.md"
PLUGIN_README = ROOT / "plugins" / "skillme" / "README.md"


def _load_kernel():
    spec = importlib.util.spec_from_file_location("system_engineering_dag_kernel", KERNEL)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


K = _load_kernel()
DAG = K.load_spec(SPEC)


def handoff():
    return {
        "skillme_run_id": "SM-TEST-1",
        "work_item_id": "ISSUE-38",
        "issue_state": "ISSUE_ADMITTED",
        "confirmed": ["observable symptom"],
        "hypotheses": ["candidate cause"],
        "unknowns": ["remaining uncertainty"],
        "affected_agencies": ["users"],
        "rights_constraints": [],
        "evidence_refs": ["trace:test"],
        "continuation_record": "CONT-1",
    }


def test_companion_skill_is_small_router_with_machine_sources():
    assert SKILL.exists()
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "\nname: system-engineering-dag\n" in text
    assert "system_engineering_dag.json" in text
    assert "system_engineering_dag_kernel.py" in text
    assert "REFERENCE.md" in text
    assert len(text.splitlines()) < 450, "runtime skill became a context bomb again"


def test_machine_graph_is_valid_acyclic_and_release_gated():
    result = K.validate_spec(DAG)
    assert result["status"] == "PASS"
    assert result["node_count"] >= 15
    order = result["topological_order"]
    assert order.index("skillme_handoff") < order.index("impact_map")
    assert order.index("verification") < order.index("release_candidate")
    assert order.index("production_verification") < order.index("learn_back_to_skillme")


def test_cycle_and_unknown_dependencies_are_rejected():
    mutated = json.loads(json.dumps(DAG))
    mutated["nodes"][0]["depends_on"] = ["learn_back_to_skillme"]
    with pytest.raises(K.ProtocolError):
        K.validate_spec(mutated)

    mutated = json.loads(json.dumps(DAG))
    mutated["nodes"][0]["depends_on"] = ["missing-node"]
    with pytest.raises(K.ProtocolError):
        K.validate_spec(mutated)


def test_skillme_handoff_is_typed_and_preserves_epistemic_boundary():
    assert K.validate_handoff(handoff(), DAG)["status"] == "PASS"

    bad = handoff()
    bad.pop("unknowns")
    with pytest.raises(K.ProtocolError):
        K.validate_handoff(bad, DAG)

    no_issue = handoff()
    no_issue["issue_state"] = "NO_ISSUE_UNDER_DECLARED_READOUT"
    assert K.validate_handoff(no_issue, DAG)["status"] == "NO_ENGINEERING_INTERVENTION"


def test_risk_routing_is_proportional_not_full_dag_for_typo():
    result = K.compile_obligations(
        {"frontend": "AFFECTED"},
        {"kind": "copy_typo", "mode": "INTERVENTION"},
        DAG,
    )
    assert result["risk_tier"] == "L0_TRIVIAL"
    assert "targeted_test" in result["obligations"]
    assert "restore_test" not in result["obligations"]
    assert "independent_review" not in result["obligations"]


def test_high_risk_database_change_derives_test_and_recovery_obligations():
    result = K.compile_obligations(
        {
            "database_schema": "AFFECTED",
            "backup_restore": "AFFECTED",
            "data_integrity": "AFFECTED",
        },
        {"triggers": ["database_change"], "mode": "INTERVENTION"},
        DAG,
    )
    assert result["risk_tier"] == "L2_HIGH"
    required = {
        "migration_rehearsal",
        "mixed_version_compatibility",
        "partial_failure_test",
        "rollback_or_rollforward",
        "restore_path",
        "backup_integrity_test",
        "restore_test",
        "key_recovery_test",
        "business_invariant_reconciliation",
    }
    assert required.issubset(set(result["obligations"]))


def test_unknown_critical_surface_blocks_and_generates_investigation():
    result = K.compile_obligations(
        {"data_integrity": "UNKNOWN"},
        {"triggers": ["active_data_corruption"], "mode": "INVESTIGATION"},
        DAG,
    )
    assert result["risk_tier"] == "L3_CRITICAL"
    assert result["status"] == "BLOCKED"
    assert "investigate:data_integrity" in result["investigation_obligations"]
    assert "evidence_preservation" in result["obligations"]


def test_explicit_time_bounded_waiver_can_unblock_unknown():
    waiver = {
        "control": "resolve-data-integrity",
        "reason": "emergency containment",
        "risk": "uncertain data integrity",
        "compensating_control": "writes disabled",
        "approver": "incident-commander",
        "expires_at": "2026-08-15",
        "review_due_at": "2026-08-15",
    }
    result = K.compile_obligations(
        {"data_integrity": "UNKNOWN"},
        {"triggers": ["active_data_corruption"], "mode": "EMERGENCY_CHANGE"},
        DAG,
        waiver=waiver,
    )
    assert result["status"] == "PASS"
    assert "waiver_record" in result["obligations"]
    assert "evidence_preservation" in result["obligations"]
    assert "post_hoc_review" in result["obligations"]


def test_cache_and_authorization_changes_derive_security_obligations():
    result = K.compile_obligations(
        {"cache": "AFFECTED", "authorization": "AFFECTED"},
        {"kind": "ordinary_bug", "mode": "INTERVENTION"},
        DAG,
    )
    required = {
        "cache_key_review",
        "cache_invalidation_test",
        "stale_data_test",
        "cache_failure_test",
        "cache_security_review",
        "authorization_negative_test",
        "cross_tenant_access_test",
    }
    assert required.issubset(set(result["obligations"]))


def test_external_side_effects_require_business_reconciliation():
    result = K.compile_obligations(
        {"payment_or_external_side_effects": "AFFECTED"},
        {"triggers": ["payment_change"], "mode": "INTERVENTION"},
        DAG,
    )
    assert {
        "idempotency_test",
        "external_side_effect_ledger",
        "reconciliation_test",
        "replay_duplicate_policy",
    }.issubset(set(result["obligations"]))


def test_release_record_requires_tests_observability_and_recovery_decision():
    valid = {
        "work_item_id": "ISSUE-38",
        "skillme_run_id": "SM-TEST-1",
        "branch": "feat/test",
        "commit_sha": "abc123",
        "artifact_id": "artifact-1",
        "risk_tier": "L2_HIGH",
        "test_evidence": ["pytest:test_system_engineering_dag_skill"],
        "recovery_decision": "ROLLFORWARD",
        "observability_ready": True,
        "production_verification_plan": ["error_rate", "data_integrity"],
    }
    assert K.validate_release(valid, DAG)["status"] == "PASS"

    invalid = dict(valid)
    invalid["observability_ready"] = False
    with pytest.raises(K.ProtocolError):
        K.validate_release(invalid, DAG)


def test_destructive_change_classes_cannot_lose_recovery_paths():
    mutated = json.loads(json.dumps(DAG))
    mutated["destructive_change_classes"]["database_destructive"] = ["write_a_document"]
    with pytest.raises(K.ProtocolError):
        K.validate_spec(mutated)


def test_multi_tenant_boundary_derives_isolation_and_restore_obligations():
    result = K.compile_obligations(
        {"multi_tenancy": "AFFECTED"},
        {"triggers": ["multi_tenant_boundary_change"], "mode": "INTERVENTION"},
        DAG,
    )
    assert result["risk_tier"] == "L2_HIGH"
    assert {
        "tenant_identity",
        "data_isolation_test",
        "cache_isolation_test",
        "quota_noisy_neighbor_test",
        "tenant_restore_test",
    }.issubset(set(result["obligations"]))


def test_affected_data_integrity_derives_business_recovery_obligations():
    result = K.compile_obligations(
        {"data_integrity": "AFFECTED"},
        {"triggers": ["active_data_corruption"], "mode": "EMERGENCY_CHANGE"},
        DAG,
    )
    assert result["risk_tier"] == "L3_CRITICAL"
    assert {
        "stop_or_scope_writes",
        "repair_or_replay_plan",
        "reconciliation_test",
        "restore_path",
    }.issubset(set(result["obligations"]))


def test_decision_rules_require_activation_and_forbid_conditions():
    assert {"sharding", "microservices", "multi_region", "knowledge_graph", "vector_retrieval"}.issubset(
        set(DAG["decision_rules"])
    )
    for rule in DAG["decision_rules"].values():
        assert rule["activate_if"]
        assert rule["forbid_if"]


def test_security_assurance_is_explicitly_tiered():
    assert {"BASELINE", "SENSITIVE", "HIGH_ASSURANCE"}.issubset(set(DAG["security_assurance_levels"]))
    for rule in DAG["security_assurance_levels"].values():
        assert rule["requires"]


def test_reference_keeps_deep_system_surfaces_without_forcing_runtime_context():
    text = REFERENCE.read_text(encoding="utf-8")
    for token in [
        "Knowledge / ontology / KG",
        "Database migration",
        "Cache security",
        "Multi-tenancy",
        "Test obligation catalog",
        "Backup / restore / disaster recovery",
        "Release / rollback / roll-forward",
        "Observability / SRE",
        "Emergency change",
        "Decommission",
    ]:
        assert token in text


def test_skillme_main_skill_routes_to_companion_and_reuses_lineage():
    text = MAIN_SKILL.read_text(encoding="utf-8")
    assert "Mandatory software/system engineering adapter" in text
    assert "MUST invoke the companion `system-engineering-dag` skill" in text
    assert "reuse the same lineage" in text


def test_plugin_readme_exposes_skillme_then_companion_route():
    text = PLUGIN_README.read_text(encoding="utf-8")
    assert "Invoke `skillme` first" in text
    assert "system-engineering-dag" in text
    assert "Issue → branch → tests/checker → PR" in text
