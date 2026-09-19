#!/usr/bin/env python3
"""Validator and obligation compiler for the System Engineering DAG.

Stdlib-only. It validates the canonical graph, typed SkillMe handoff, risk routing,
impact maps, waivers, and derived engineering obligations. It does not prove domain
or causal truth.
"""
from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC = HERE / "system_engineering_dag.json"


class ProtocolError(ValueError):
    pass


def load_spec(path: str | Path = DEFAULT_SPEC) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _require_keys(obj: dict[str, Any], keys: list[str], where: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ProtocolError(f"{where}: missing required keys {missing}")


def _toposort(nodes: list[dict[str, Any]]) -> list[str]:
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        raise ProtocolError("duplicate node id")
    node_ids = set(ids)
    deps = {n["id"]: set(n.get("depends_on", [])) for n in nodes}
    for node_id, ds in deps.items():
        missing = ds - node_ids
        if missing:
            raise ProtocolError(f"{node_id}: unknown dependencies {sorted(missing)}")
    incoming = {k: set(v) for k, v in deps.items()}
    ready = sorted(k for k, v in incoming.items() if not v)
    order: list[str] = []
    while ready:
        cur = ready.pop(0)
        order.append(cur)
        for other in sorted(incoming):
            if cur in incoming[other]:
                incoming[other].remove(cur)
                if not incoming[other] and other not in order and other not in ready:
                    ready.append(other)
                    ready.sort()
    if len(order) != len(nodes):
        cycle_nodes = sorted(k for k, v in incoming.items() if v)
        raise ProtocolError(f"graph contains cycle or unresolved dependency among {cycle_nodes}")
    return order


def _ancestors(nodes: list[dict[str, Any]], node_id: str) -> set[str]:
    deps = {n["id"]: set(n.get("depends_on", [])) for n in nodes}
    if node_id not in deps:
        raise ProtocolError(f"unknown node {node_id}")
    seen: set[str] = set()
    stack = list(deps[node_id])
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(deps[cur])
    return seen


def validate_spec(spec: dict[str, Any]) -> dict[str, Any]:
    _require_keys(
        spec,
        [
            "spec_version", "nodes", "risk_tiers", "handoff_schema", "impact_status",
            "surfaces", "critical_surfaces", "obligation_rules", "waiver_schema",
            "artifact_metadata_schema", "release_schema", "required_release_path",
            "destructive_change_classes", "recovery_invariants", "decision_rules",
            "security_assurance_levels"
        ],
        "spec",
    )
    node_required = spec["node_schema"]["required"]
    allowed_kinds = set(spec["node_schema"]["kinds"])
    for i, node in enumerate(spec["nodes"]):
        _require_keys(node, node_required, f"nodes[{i}]")
        if node["kind"] not in allowed_kinds:
            raise ProtocolError(f"{node['id']}: invalid kind {node['kind']}")
    order = _toposort(spec["nodes"])
    node_ids = {n["id"] for n in spec["nodes"]}

    for required in spec["required_release_path"]:
        if required not in node_ids:
            raise ProtocolError(f"required release path references missing node {required}")

    prod_ancestors = _ancestors(spec["nodes"], "production_verification")
    for must_precede in [
        "work_item", "skillme_handoff", "risk_classification", "impact_map",
        "obligation_compile", "change_plan_gate", "implementation", "verification",
        "pull_request", "release_candidate"
    ]:
        if must_precede not in prod_ancestors:
            raise ProtocolError(f"production path bypasses {must_precede}")

    learn_ancestors = _ancestors(spec["nodes"], "learn_back_to_skillme")
    if "production_verification" not in learn_ancestors:
        raise ProtocolError("learning path does not depend on production verification")

    allowed_status = set(spec["impact_status"])
    if allowed_status != {"AFFECTED", "NOT_AFFECTED", "UNKNOWN"}:
        raise ProtocolError("impact_status must preserve AFFECTED/NOT_AFFECTED/UNKNOWN")

    surfaces = set(spec["surfaces"])
    for rule in spec["obligation_rules"]:
        if rule["when_surface"] not in surfaces:
            raise ProtocolError(f"obligation rule references unknown surface {rule['when_surface']}")
        if not rule.get("require"):
            raise ProtocolError(f"obligation rule for {rule['when_surface']} has no obligations")

    for change_class, obligations in spec["destructive_change_classes"].items():
        if not obligations:
            raise ProtocolError(f"{change_class} lacks recovery obligations")
        if not any(("rollback" in x or "rollforward" in x or "restore" in x or "failover" in x or "revert" in x) for x in obligations):
            raise ProtocolError(f"{change_class} lacks rollback/rollforward/restore/failover path")

    required_recovery_invariants = {
        "backup_without_restore_test_is_not_recovery",
        "database_schema_rollback_is_not_assumed_safe",
        "recovery_complete_requires_business_invariant_reconciliation",
        "encrypted_backup_requires_key_recovery_path",
    }
    if not required_recovery_invariants.issubset(set(spec["recovery_invariants"])):
        raise ProtocolError("missing required recovery invariants")

    for decision, rule in spec["decision_rules"].items():
        if not rule.get("activate_if") or not rule.get("forbid_if"):
            raise ProtocolError(f"decision rule {decision} must define activate_if and forbid_if")

    required_assurance = {"BASELINE", "SENSITIVE", "HIGH_ASSURANCE"}
    if not required_assurance.issubset(set(spec["security_assurance_levels"])):
        raise ProtocolError("security assurance levels must include BASELINE/SENSITIVE/HIGH_ASSURANCE")
    for level, rule in spec["security_assurance_levels"].items():
        if not rule.get("requires"):
            raise ProtocolError(f"security assurance level {level} has no requirements")

    return {"status": "PASS", "node_count": len(spec["nodes"]), "topological_order": order}


def validate_handoff(handoff: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    required = spec["handoff_schema"]["required"]
    _require_keys(handoff, required, "handoff")
    if handoff["issue_state"] not in spec["handoff_schema"]["issue_states"]:
        raise ProtocolError(f"handoff: invalid issue_state {handoff['issue_state']}")
    for key in ["confirmed", "hypotheses", "unknowns", "affected_agencies", "rights_constraints", "evidence_refs"]:
        if not isinstance(handoff[key], list):
            raise ProtocolError(f"handoff.{key} must be a list")
    if handoff["issue_state"] == "NO_ISSUE_UNDER_DECLARED_READOUT":
        return {"status": "NO_ENGINEERING_INTERVENTION", "reason": "SkillMe did not admit an issue"}
    return {"status": "PASS"}


def classify_risk(change: dict[str, Any], spec: dict[str, Any]) -> str:
    triggers = set(change.get("triggers", []))
    if triggers & set(spec["risk_tiers"]["L3_CRITICAL"].get("triggers", [])):
        return "L3_CRITICAL"
    if triggers & set(spec["risk_tiers"]["L2_HIGH"].get("triggers", [])):
        return "L2_HIGH"
    if change.get("kind") in spec["risk_tiers"]["L0_TRIVIAL"].get("examples", []):
        return "L0_TRIVIAL"
    return "L1_STANDARD"


def validate_waiver(waiver: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    _require_keys(waiver, spec["waiver_schema"]["required"], "waiver")
    for key in ["expires_at", "review_due_at"]:
        try:
            _dt.date.fromisoformat(waiver[key])
        except Exception as exc:
            raise ProtocolError(f"waiver.{key} must be YYYY-MM-DD") from exc
    return {"status": "PASS"}


def compile_obligations(
    impact: dict[str, str],
    change: dict[str, Any],
    spec: dict[str, Any],
    waiver: dict[str, Any] | None = None,
) -> dict[str, Any]:
    unknown_surfaces = set(impact) - set(spec["surfaces"])
    if unknown_surfaces:
        raise ProtocolError(f"impact contains unknown surfaces {sorted(unknown_surfaces)}")
    invalid = {k: v for k, v in impact.items() if v not in spec["impact_status"]}
    if invalid:
        raise ProtocolError(f"invalid impact statuses {invalid}")

    risk_tier = classify_risk(change, spec)
    obligations = set(spec["risk_tiers"][risk_tier]["required_obligations"])
    investigation = set()
    blockers = []

    for surface, status in impact.items():
        if status == "AFFECTED":
            for rule in spec["obligation_rules"]:
                if rule["when_surface"] == surface and rule["when_status"] == status:
                    obligations.update(rule["require"])
        elif status == "UNKNOWN":
            investigation.add(f"investigate:{surface}")
            if surface in spec["critical_surfaces"]:
                blockers.append(f"critical_surface_unknown:{surface}")

    if change.get("mode") == "INVESTIGATION":
        obligations.add("evidence_preservation")
        obligations.add("investigation_exit_criteria")
    elif change.get("mode") == "EMERGENCY_CHANGE":
        obligations.update(spec["change_modes"]["EMERGENCY_CHANGE"]["must_not_bypass"])
    else:
        obligations.update(spec["change_modes"]["INTERVENTION"]["requires"])

    if blockers and waiver is not None:
        validate_waiver(waiver, spec)
        obligations.add("waiver_record")
        blockers = []

    return {
        "status": "BLOCKED" if blockers else "PASS",
        "risk_tier": risk_tier,
        "obligations": sorted(obligations),
        "investigation_obligations": sorted(investigation),
        "blockers": blockers,
    }


def validate_release(record: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    _require_keys(record, spec["release_schema"]["required"], "release")
    if record["risk_tier"] not in spec["risk_tiers"]:
        raise ProtocolError("release: invalid risk_tier")
    if record["recovery_decision"] not in spec["release_schema"]["recovery_decisions"]:
        raise ProtocolError("release: invalid recovery_decision")
    if not record["test_evidence"]:
        raise ProtocolError("release: test_evidence must be non-empty")
    if not record["observability_ready"]:
        raise ProtocolError("release: observability must be ready")
    if not record["production_verification_plan"]:
        raise ProtocolError("release: production verification plan required")
    return {"status": "PASS"}


def _fixture_handoff() -> dict[str, Any]:
    return {
        "skillme_run_id": "SM-1",
        "work_item_id": "ISSUE-38",
        "issue_state": "ISSUE_ADMITTED",
        "confirmed": ["cache serves stale response"],
        "hypotheses": ["invalidation event missing"],
        "unknowns": [],
        "affected_agencies": ["users"],
        "rights_constraints": [],
        "evidence_refs": ["trace-1"],
        "continuation_record": "CONT-1",
    }


def self_test() -> dict[str, Any]:
    spec = load_spec()
    tests = []

    def ok(name, fn):
        fn()
        tests.append((name, True))

    def must_fail(name, fn):
        try:
            fn()
        except ProtocolError:
            tests.append((name, True))
            return
        raise AssertionError(f"{name}: expected ProtocolError")

    ok("valid_spec", lambda: validate_spec(spec))

    cyc = copy.deepcopy(spec)
    for n in cyc["nodes"]:
        if n["id"] == "work_item":
            n["depends_on"] = ["learn_back_to_skillme"]
    must_fail("cycle_detected", lambda: validate_spec(cyc))

    bad_dep = copy.deepcopy(spec)
    bad_dep["nodes"][0]["depends_on"] = ["does_not_exist"]
    must_fail("unknown_dependency", lambda: validate_spec(bad_dep))

    destructive = copy.deepcopy(spec)
    destructive["destructive_change_classes"]["database_destructive"] = ["document_it"]
    must_fail("destructive_change_requires_recovery", lambda: validate_spec(destructive))

    ok("valid_handoff", lambda: validate_handoff(_fixture_handoff(), spec))

    bad_handoff = _fixture_handoff()
    bad_handoff.pop("unknowns")
    must_fail("handoff_is_typed", lambda: validate_handoff(bad_handoff, spec))

    trivial = compile_obligations({"frontend": "AFFECTED"}, {"kind": "copy_typo", "mode": "INTERVENTION"}, spec)
    assert trivial["risk_tier"] == "L0_TRIVIAL"
    assert "restore_test" not in trivial["obligations"]
    tests.append(("risk_proportional_trivial", True))

    db = compile_obligations(
        {"database_schema": "AFFECTED", "backup_restore": "AFFECTED"},
        {"triggers": ["database_change"], "mode": "INTERVENTION"},
        spec,
    )
    assert db["risk_tier"] == "L2_HIGH"
    for item in ["migration_rehearsal", "mixed_version_compatibility", "restore_test", "key_recovery_test", "business_invariant_reconciliation"]:
        assert item in db["obligations"], item
    tests.append(("db_change_derives_recovery_obligations", True))

    critical_unknown = compile_obligations(
        {"data_integrity": "UNKNOWN"},
        {"triggers": ["active_data_corruption"], "mode": "INVESTIGATION"},
        spec,
    )
    assert critical_unknown["status"] == "BLOCKED"
    assert "investigate:data_integrity" in critical_unknown["investigation_obligations"]
    tests.append(("critical_unknown_blocks", True))

    waiver = {
        "control": "data_integrity_resolution",
        "reason": "emergency containment",
        "risk": "possible stale data",
        "compensating_control": "writes disabled",
        "approver": "incident_commander",
        "expires_at": "2026-08-15",
        "review_due_at": "2026-08-15",
    }
    waived = compile_obligations(
        {"data_integrity": "UNKNOWN"},
        {"triggers": ["active_data_corruption"], "mode": "EMERGENCY_CHANGE"},
        spec,
        waiver=waiver,
    )
    assert waived["status"] == "PASS"
    assert "waiver_record" in waived["obligations"]
    tests.append(("explicit_waiver_can_unblock", True))

    cache = compile_obligations(
        {"cache": "AFFECTED", "authorization": "AFFECTED"},
        {"kind": "ordinary_bug", "mode": "INTERVENTION"},
        spec,
    )
    for item in ["cache_invalidation_test", "cache_security_review", "authorization_negative_test", "cross_tenant_access_test"]:
        assert item in cache["obligations"], item
    tests.append(("cache_auth_derives_security_obligations", True))

    payment = compile_obligations(
        {"payment_or_external_side_effects": "AFFECTED"},
        {"triggers": ["payment_change"], "mode": "INTERVENTION"},
        spec,
    )
    for item in ["external_side_effect_ledger", "reconciliation_test", "idempotency_test"]:
        assert item in payment["obligations"], item
    tests.append(("external_side_effects_require_reconciliation", True))

    tenancy = compile_obligations(
        {"multi_tenancy": "AFFECTED"},
        {"triggers": ["multi_tenant_boundary_change"], "mode": "INTERVENTION"},
        spec,
    )
    assert tenancy["risk_tier"] == "L2_HIGH"
    for item in ["data_isolation_test", "cache_isolation_test", "tenant_restore_test"]:
        assert item in tenancy["obligations"], item
    tests.append(("multi_tenant_boundary_requires_isolation", True))

    integrity = compile_obligations(
        {"data_integrity": "AFFECTED"},
        {"triggers": ["active_data_corruption"], "mode": "EMERGENCY_CHANGE"},
        spec,
    )
    for item in ["stop_or_scope_writes", "repair_or_replay_plan", "reconciliation_test", "restore_path"]:
        assert item in integrity["obligations"], item
    tests.append(("data_integrity_derives_business_recovery", True))

    release = {
        "work_item_id": "ISSUE-38",
        "skillme_run_id": "SM-1",
        "branch": "feat/x",
        "commit_sha": "abc",
        "artifact_id": "artifact-1",
        "risk_tier": "L2_HIGH",
        "test_evidence": ["pytest"],
        "recovery_decision": "ROLLFORWARD",
        "observability_ready": True,
        "production_verification_plan": ["error_rate", "data_integrity"],
    }
    ok("release_record_valid", lambda: validate_release(release, spec))

    bad_release = dict(release)
    bad_release["observability_ready"] = False
    must_fail("release_requires_observability", lambda: validate_release(bad_release, spec))

    passed = sum(1 for _, p in tests if p)
    return {"status": "PASS", "passed": passed, "test_count": len(tests), "tests": [n for n, _ in tests]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=str(DEFAULT_SPEC))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        result = validate_spec(load_spec(args.spec))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
