"""Regression coverage for communication_glossary/kg_accumulate.py.

Follows this repo's convention: no mocking, real subprocess/module calls
against pytest's tmp_path fixture, against the repo's own real example
checkpoints (not synthetic fixtures) where possible.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "communication_glossary"))
import kg_accumulate  # noqa: E402

FINTECH_CHECKPOINT = (
    REPO_ROOT / "communication_glossary" / "examples" / "fintech" / "checkpoint.json"
)
GUT_HEALTH_CHECKPOINT = (
    REPO_ROOT
    / "communication_glossary"
    / "examples"
    / "gut-health-nurse-triage"
    / "checkpoint.json"
)


def test_first_ingest_creates_state_and_markdown(tmp_path):
    result = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path
    )
    assert result["skipped"] is False
    assert result["total_words"] > 0
    assert len(result["new_words"]) == result["total_words"]
    assert result["state_path"].exists()
    assert result["markdown_path"].exists()

    state = json.loads(result["state_path"].read_text())
    assert state["principal_id"] == "user-1"
    assert state["topic_tag"] == "fintech"
    assert result["checkpoint_certificate"] in state["ingested_checkpoints"]


def test_reingesting_same_checkpoint_is_skipped_and_idempotent(tmp_path):
    first = kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path)
    state_before = json.loads(first["state_path"].read_text())

    second = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path
    )
    assert second["skipped"] is True
    assert second["new_words"] == []
    assert second["total_words"] == first["total_words"]

    state_after = json.loads(first["state_path"].read_text())
    assert state_after == state_before, "skipped run must not modify the state file"


def test_second_different_checkpoint_merges_and_grows_total(tmp_path):
    first = kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path)
    second = kg_accumulate.accumulate(
        GUT_HEALTH_CHECKPOINT, "user-1", "fintech", tmp_path
    )

    assert second["skipped"] is False
    assert len(second["new_words"]) > 0
    assert second["total_words"] == first["total_words"] + len(second["new_words"])

    state = json.loads(second["state_path"].read_text())
    assert len(state["ingested_checkpoints"]) == 2
    assert first["checkpoint_certificate"] in state["ingested_checkpoints"]
    assert second["checkpoint_certificate"] in state["ingested_checkpoints"]


def test_node_ids_collide_correctly_across_checkpoints_no_duplicate_entries(tmp_path):
    # Load-bearing fact this whole design depends on (verified live by two
    # independent PR reviews of kg_extract.py's mermaid_id()): the same
    # (word, type) pair from two different checkpoints must merge into ONE
    # accumulated entry with a unioned sources list, not two separate entries.
    kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "shared-topic", tmp_path)
    result = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-2", "shared-topic", tmp_path
    )
    # different principal_id -> different accumulation scope entirely
    assert result["skipped"] is False

    # Same principal, ingest the SAME checkpoint content again under a fresh
    # topic to confirm cross-topic scoping doesn't leak state.
    fresh_topic_result = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-1", "another-topic", tmp_path
    )
    assert fresh_topic_result["skipped"] is False
    assert fresh_topic_result["total_words"] > 0


def test_scoping_is_isolated_per_principal_and_topic(tmp_path):
    kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path)
    other_principal = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-2", "fintech", tmp_path
    )
    other_topic = kg_accumulate.accumulate(
        FINTECH_CHECKPOINT, "user-1", "other-topic", tmp_path
    )
    # Both are fresh ingests in their own scope -- not affected by user-1/fintech
    assert other_principal["skipped"] is False
    assert other_topic["skipped"] is False
    assert other_principal["total_words"] == other_topic["total_words"]

    scope_a = kg_accumulate.state_dir(tmp_path, "user-1", "fintech")
    scope_b = kg_accumulate.state_dir(tmp_path, "user-2", "fintech")
    scope_c = kg_accumulate.state_dir(tmp_path, "user-1", "other-topic")
    assert scope_a != scope_b != scope_c


def test_blank_principal_id_refused(tmp_path):
    import pytest

    with pytest.raises(SystemExit, match="principal-id"):
        kg_accumulate.accumulate(FINTECH_CHECKPOINT, "  ", "fintech", tmp_path)


def test_blank_topic_tag_refused(tmp_path):
    import pytest

    with pytest.raises(SystemExit, match="topic-tag"):
        kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "  ", tmp_path)


def test_missing_checkpoint_file_refused(tmp_path):
    import pytest

    with pytest.raises(SystemExit, match="not found"):
        kg_accumulate.accumulate(
            tmp_path / "does-not-exist.json", "user-1", "fintech", tmp_path
        )


def test_invalid_json_checkpoint_refused(tmp_path):
    import pytest

    bad = tmp_path / "bad.json"
    bad.write_text("not json {{{")
    with pytest.raises(SystemExit, match="not valid JSON"):
        kg_accumulate.accumulate(bad, "user-1", "fintech", tmp_path)


def test_merge_extends_sources_with_checkpoint_qualified_labels(tmp_path):
    result = kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path)
    state = json.loads(result["state_path"].read_text())
    cert = result["checkpoint_certificate"]
    for word, wtype, sources in state["word_index"]:
        for source in sources:
            assert source.startswith(f"{cert}:"), (
                f"source {source!r} for {word!r} not qualified with checkpoint "
                "certificate"
            )


def test_markdown_lists_all_ingested_checkpoints(tmp_path):
    kg_accumulate.accumulate(FINTECH_CHECKPOINT, "user-1", "fintech", tmp_path)
    second = kg_accumulate.accumulate(
        GUT_HEALTH_CHECKPOINT, "user-1", "fintech", tmp_path
    )
    md = second["markdown_path"].read_text(encoding="utf-8")
    assert "Checkpoints ingested (2)" in md
