from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "plugins" / "skillme" / "skills" / "system-engineering-dag"
PROFILE_PATH = DIR / "ux_attention_profile.json"
KERNEL_PATH = DIR / "ux_attention_kernel.py"
WIREFRAME = DIR / "WIREFRAME.md"
SKILL = DIR / "SKILL.md"


def _load_kernel():
    spec = importlib.util.spec_from_file_location("ux_attention_kernel", KERNEL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


K = _load_kernel()
PROFILE = K.load_profile(PROFILE_PATH)


def valid_record():
    return {
        "issue_visible_first_view": True,
        "status_visible_first_view": True,
        "unknowns_visually_distinct": True,
        "primary_action_visible_first_view": True,
        "owner_visible_first_view": True,
        "freshness_visible_first_view": True,
        "false_floor_absent": True,
        "mobile_horizontal_scroll_required_for_core_answer": False,
    }


def test_attention_profile_is_valid_and_explicitly_heuristic():
    result = K.validate_profile(PROFILE)
    assert result["status"] == "PASS"
    assert PROFILE["status"] == "research-informed-heuristic-not-universal-law"
    assert result["research_sources"] >= 4


def test_attention_bands_preserve_research_prior_and_long_tail_semantics():
    bands = PROFILE["attention_budget"]["bands"]
    assert [b["observed_viewing_time_share_percent"] for b in bands] == [57, 17, 7, 19]
    assert bands[1]["drop_from_previous_percent"] == pytest.approx(70.2)
    assert bands[2]["drop_from_previous_percent"] == pytest.approx(58.8)
    assert "aggregate" in bands[3]["share_semantics"]


def test_issue_screen_compiles_first_view_obligations():
    result = K.compile_issue_ui_obligations(PROFILE, "issue_analysis")
    assert result["applicable"] is True
    required = {
        "issue_first_wireframe",
        "first_view_issue_capsule",
        "attention_budget_review",
        "first_view_primary_action",
        "confirmed_unknown_visual_separation",
        "mobile_issue_visibility",
        "false_floor_check",
        "wireframe_comprehension_test",
        "first_view_performance_priority",
    }
    assert required.issubset(set(result["obligations"]))


def test_non_issue_homepage_does_not_inherit_issue_ui_ceremony():
    result = K.compile_issue_ui_obligations(PROFILE, "marketing_homepage")
    assert result["applicable"] is False
    assert result["obligations"] == []


def test_wireframe_requires_issue_status_action_owner_freshness_in_first_view():
    assert K.validate_wireframe_record(valid_record(), PROFILE)["status"] == "PASS"

    for field in [
        "issue_visible_first_view",
        "status_visible_first_view",
        "unknowns_visually_distinct",
        "primary_action_visible_first_view",
        "owner_visible_first_view",
        "freshness_visible_first_view",
        "false_floor_absent",
    ]:
        record = valid_record()
        record[field] = False
        with pytest.raises(K.AttentionProfileError):
            K.validate_wireframe_record(record, PROFILE)


def test_mobile_core_answer_must_not_require_horizontal_scroll():
    record = valid_record()
    record["mobile_horizontal_scroll_required_for_core_answer"] = True
    with pytest.raises(K.AttentionProfileError):
        K.validate_wireframe_record(record, PROFILE)


def test_wireframe_doc_exposes_attention_decay_and_issue_capsule():
    text = WIREFRAME.read_text(encoding="utf-8")
    for token in [
        "Issue Capsule",
        "Screen 1 | 57%",
        "Screen 2 | 17%",
        "Screen 3 | 7%",
        "19% **aggregate long tail**",
        "time_to_identify_issue",
        "scroll_before_issue_comprehension_rate",
        "No false floor",
    ]:
        assert token in text


def test_runtime_skill_makes_issue_first_wireframe_mandatory():
    text = SKILL.read_text(encoding="utf-8")
    assert "Issue-first wireframe is mandatory" in text
    assert "MUST load `WIREFRAME.md` and" in text
    assert "Issue-management UI must answer the Issue in the first viewport" in text
    assert "Attention percentages are research priors, not universal laws" in text
