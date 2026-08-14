from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "skillme" / "skills" / "system-engineering-dag" / "SKILL.md"
PLUGIN_README = ROOT / "plugins" / "skillme" / "README.md"


def test_companion_skill_exists_and_has_valid_basic_frontmatter():
    assert SKILL.exists()
    text = SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "\nname: system-engineering-dag\n" in text
    assert "\ndescription: >\n" in text
    assert text.count("---") >= 2


def test_issue_routing_requires_skillme_then_engineering_dag():
    text = SKILL.read_text(encoding="utf-8")
    required = [
        "invoke: skillme",
        "first: true",
        "then_invoke: system-engineering-dag",
        "reuse that run/checkpoint",
        "GitHub Issue contract",
        "no_direct_main_edit: true",
        "no_test_no_merge: true",
        "no_review_no_release: true",
    ]
    for token in required:
        assert token in text, token


def test_engineering_dag_keeps_core_architecture_and_recovery_surfaces():
    text = SKILL.read_text(encoding="utf-8")
    required = [
        "database:",
        "cache:",
        "security:",
        "network:",
        "infrastructure:",
        "test_ecosystem:",
        "observability_sre:",
        "backup_restore_dr:",
        "release_recovery:",
        "rollback.architecture" if False else "rollback",
        "rollforward",
        "disaster_recovery_test",
        "backup_restore_test",
        "chaos_test",
        "migration_test",
        "ai.eval" if False else "ai_evaluation",
    ]
    for token in required:
        assert token in text, token


def test_backup_and_rollback_claims_are_not_naive():
    text = SKILL.read_text(encoding="utf-8")
    assert "backup_without_successful_restore_test_is_not_recovery" in text
    assert "database_schema_rollback_is_not_assumed_safe" in text
    assert "prefer_roll_forward_when_new_writes_make_old_version_unsafe" in text
    assert "No rollback claim without data/schema compatibility analysis" in text


def test_plugin_readme_exposes_mandatory_companion_routing():
    text = PLUGIN_README.read_text(encoding="utf-8")
    assert "system-engineering-dag" in text
    assert "MUST invoke `system-engineering-dag`" in text
    assert "Invoke `skillme` first" in text
    assert "Issue → branch → tests/checker → PR" in text
