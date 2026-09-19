#!/usr/bin/env python3
"""Stdlib-only validator/compiler for issue-first wireframe attention rules."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_PROFILE = HERE / "ux_attention_profile.json"


class AttentionProfileError(ValueError):
    pass


def load_profile(path: str | Path = DEFAULT_PROFILE) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _require_keys(obj: dict[str, Any], keys: list[str], where: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise AttentionProfileError(f"{where}: missing {missing}")


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    _require_keys(
        profile,
        ["spec_version", "status", "integration", "research_basis", "attention_budget", "issue_first_wireframe_contract", "wireframe_validation"],
        "profile",
    )
    if profile["status"] != "research-informed-heuristic-not-universal-law":
        raise AttentionProfileError("attention values must be labeled as heuristic, not universal law")

    integration = profile["integration"]
    _require_keys(integration, ["surface", "mandatory_when", "derived_obligations"], "integration")
    if integration["surface"] != "issue_management_ui":
        raise AttentionProfileError("integration surface must be issue_management_ui")

    bands = profile["attention_budget"]["bands"]
    if [b["id"] for b in bands] != ["SCREEN_1", "SCREEN_2", "SCREEN_3", "LONG_TAIL"]:
        raise AttentionProfileError("attention bands must preserve SCREEN_1/2/3/LONG_TAIL order")
    shares = [bands[0]["observed_viewing_time_share_percent"], bands[1]["observed_viewing_time_share_percent"], bands[2]["observed_viewing_time_share_percent"], bands[3]["observed_viewing_time_share_percent"]]
    if shares != [57, 17, 7, 19]:
        raise AttentionProfileError("research-prior shares changed without explicit source revision")
    if sum(shares) != 100:
        raise AttentionProfileError("attention bands must sum to 100 aggregate share")
    if "aggregate" not in bands[3].get("share_semantics", ""):
        raise AttentionProfileError("LONG_TAIL 19% must be explicitly aggregate, not per-screen")

    screen1 = bands[0]
    required_answers = {
        "what_is_the_issue",
        "issue_status",
        "severity_or_risk",
        "who_or_what_is_affected",
        "what_is_confirmed_vs_unknown",
        "primary_next_action",
        "owner_or_responsible_role",
    }
    if not required_answers.issubset(set(screen1.get("must_answer", []))):
        raise AttentionProfileError("SCREEN_1 no longer answers the core issue contract")

    capsule = profile["issue_first_wireframe_contract"]["issue_capsule"]
    capsule_fields = set(capsule["required_fields"])
    for field in ["issue_statement_one_sentence", "issue_state", "primary_next_action", "unknown_summary", "owner", "freshness_or_last_evidence_time"]:
        if field not in capsule_fields:
            raise AttentionProfileError(f"Issue Capsule missing {field}")
    if capsule["interaction"]["primary_action_count"] != 1:
        raise AttentionProfileError("Issue Capsule must expose exactly one primary action")

    hard_fail = set(profile["wireframe_validation"]["hard_fail"])
    for rule in [
        "issue_statement_not_visible_in_first_view",
        "primary_next_action_not_visible_in_first_view_for_actionable_issue",
        "unknown_present_but_hidden_as_if_resolved",
        "false_floor_hides_continuation",
        "mobile_core_answer_requires_horizontal_scroll",
    ]:
        if rule not in hard_fail:
            raise AttentionProfileError(f"wireframe hard-fail rule missing {rule}")

    if len(profile["research_basis"]) < 4:
        raise AttentionProfileError("attention profile needs multiple research anchors")
    return {"status": "PASS", "research_sources": len(profile["research_basis"]), "bands": len(bands)}


def compile_issue_ui_obligations(profile: dict[str, Any], screen_primary_task: str) -> dict[str, Any]:
    validate_profile(profile)
    applicable = screen_primary_task in {
        "understand_issue",
        "act_on_issue",
        "incident_response",
        "work_item_triage",
        "issue_analysis",
    }
    return {
        "status": "PASS",
        "surface": profile["integration"]["surface"],
        "applicable": applicable,
        "obligations": sorted(profile["integration"]["derived_obligations"]) if applicable else [],
    }


def validate_wireframe_record(record: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    validate_profile(profile)
    required = [
        "issue_visible_first_view",
        "status_visible_first_view",
        "unknowns_visually_distinct",
        "primary_action_visible_first_view",
        "owner_visible_first_view",
        "freshness_visible_first_view",
        "false_floor_absent",
        "mobile_horizontal_scroll_required_for_core_answer",
    ]
    _require_keys(record, required, "wireframe_record")
    if not record["issue_visible_first_view"]:
        raise AttentionProfileError("wireframe fails: issue not visible in first view")
    if not record["status_visible_first_view"]:
        raise AttentionProfileError("wireframe fails: issue status not visible in first view")
    if not record["unknowns_visually_distinct"]:
        raise AttentionProfileError("wireframe fails: unknowns are visually collapsed")
    if not record["primary_action_visible_first_view"]:
        raise AttentionProfileError("wireframe fails: primary action not visible in first view")
    if not record["owner_visible_first_view"] or not record["freshness_visible_first_view"]:
        raise AttentionProfileError("wireframe fails: owner/freshness missing from first view")
    if not record["false_floor_absent"]:
        raise AttentionProfileError("wireframe fails: false floor hides continuation")
    if record["mobile_horizontal_scroll_required_for_core_answer"]:
        raise AttentionProfileError("wireframe fails: mobile core answer requires horizontal scroll")
    return {"status": "PASS"}


def self_test() -> dict[str, Any]:
    profile = load_profile()
    tests: list[str] = []

    validate_profile(profile)
    tests.append("valid_profile")

    obligations = compile_issue_ui_obligations(profile, "issue_analysis")
    assert obligations["applicable"] is True
    assert "first_view_issue_capsule" in obligations["obligations"]
    assert "attention_budget_review" in obligations["obligations"]
    tests.append("issue_ui_compiles_obligations")

    non_issue = compile_issue_ui_obligations(profile, "marketing_homepage")
    assert non_issue["applicable"] is False
    assert non_issue["obligations"] == []
    tests.append("non_issue_ui_not_forced")

    valid_record = {
        "issue_visible_first_view": True,
        "status_visible_first_view": True,
        "unknowns_visually_distinct": True,
        "primary_action_visible_first_view": True,
        "owner_visible_first_view": True,
        "freshness_visible_first_view": True,
        "false_floor_absent": True,
        "mobile_horizontal_scroll_required_for_core_answer": False,
    }
    validate_wireframe_record(valid_record, profile)
    tests.append("valid_wireframe_record")

    bad = dict(valid_record)
    bad["issue_visible_first_view"] = False
    try:
        validate_wireframe_record(bad, profile)
    except AttentionProfileError:
        tests.append("issue_not_first_view_rejected")
    else:
        raise AssertionError("issue-not-first-view must fail")

    corrupted = copy.deepcopy(profile)
    corrupted["attention_budget"]["bands"][3]["share_semantics"] = "19 percent per screen"
    try:
        validate_profile(corrupted)
    except AttentionProfileError:
        tests.append("long_tail_misread_rejected")
    else:
        raise AssertionError("long-tail misinterpretation must fail")

    return {"status": "PASS", "passed": len(tests), "test_count": len(tests), "tests": tests}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        result = validate_profile(load_profile(args.profile))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
