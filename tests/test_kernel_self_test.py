import copy
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL = REPO_ROOT / "skillme_protocol_kernel.py"

sys.path.insert(0, str(REPO_ROOT))
import skillme_protocol_kernel as k  # noqa: E402


def test_self_test_passes():
    result = subprocess.run(
        [sys.executable, str(KERNEL), "--self-test"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["failed"] == 0
    assert report["passed"] == report["test_count"]


def test_demo_run_is_valid():
    result = subprocess.run(
        [sys.executable, str(KERNEL), "--demo"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["protocol_status"] == "VALID"


def test_checkpoint_demo_run_is_valid_checkpoint():
    result = subprocess.run(
        [sys.executable, str(KERNEL), "--checkpoint-demo"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["protocol_status"] == "VALID_CHECKPOINT"
    assert report["continuation_available"] is True


def test_checkpoint_demo_alt_domain_is_valid_and_not_thai():
    result = subprocess.run(
        [sys.executable, str(KERNEL), "--print-checkpoint-demo-2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    run = json.loads(result.stdout)
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]
    assert report["errors"] == []
    raw = json.dumps(run, ensure_ascii=False)
    assert "Thailand" not in raw
    assert "ไทย" not in raw
    assert "th" not in run["hypothesis_evidence_challenge"]["target_context"]["languages"]


def _demo_checkpoint() -> dict:
    result = subprocess.run(
        [sys.executable, str(KERNEL), "--print-checkpoint-demo"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_authority_assumptions_may_be_empty_with_no_authority_dimension():
    run = copy.deepcopy(_demo_checkpoint())
    card = run["hypothesis_portfolio"]["hypothesis_cards"][0]
    card["authority_assumptions"] = []
    card["legal_relevance"] = "NONE"
    card["legal_status"] = "NOT_REQUIRED"
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_authority_assumptions_still_required_when_legally_relevant():
    run = copy.deepcopy(_demo_checkpoint())
    card = run["hypothesis_portfolio"]["hypothesis_cards"][1]
    card["authority_assumptions"] = []
    # demo's H2 already has legal_relevance != "NONE" — carve-out must not apply
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("authority_assumptions" in e for e in report["errors"])


def test_authority_assumptions_still_required_when_legal_status_not_not_required():
    run = copy.deepcopy(_demo_checkpoint())
    card = run["hypothesis_portfolio"]["hypothesis_cards"][0]
    card["authority_assumptions"] = []
    card["legal_relevance"] = "NONE"
    card["legal_status"] = "PRELIMINARY"  # not NOT_REQUIRED -> carve-out must not apply
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("authority_assumptions" in e for e in report["errors"])


_INTERNAL_DATA_AUDIT_FIELDS = {
    "citation_id",
    "title",
    "source_system",
    "query_or_filter",
    "record_id_or_url",
    "context_country_or_region",
    "claim_supported_or_challenged",
    "direction",
    "quality",
    "directness",
    "context_fit",
    "metadata_verification",
    "scope_verification",
    "retrieved_at",
}


def _to_internal_data_audit_card(citation: dict) -> dict:
    citation = dict(citation)
    for field in ("authors_or_issuer", "year", "source_type", "journal_or_repository", "persistent_id_or_official_url"):
        citation.pop(field, None)
    citation["source_system"] = "internal audit log"
    citation["query_or_filter"] = "attempt_id=TEST"
    citation["record_id_or_url"] = "internal://audit/TEST"
    return citation


def test_internal_data_audit_review_mode_accepts_internal_source_citations():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_evidence_challenge"]["review_mode"] = "INTERNAL_DATA_AUDIT"
    for h in run["hypothesis_evidence_challenge"]["hypotheses"]:
        h["citation_cards"] = [_to_internal_data_audit_card(c) for c in h["citation_cards"]]
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_targeted_search_review_mode_still_requires_literature_citations():
    run = copy.deepcopy(_demo_checkpoint())
    # review_mode left as the demo's default (TARGETED_SEARCH) — internal-data
    # fields must NOT be accepted as a substitute for the literature fields.
    for h in run["hypothesis_evidence_challenge"]["hypotheses"]:
        h["citation_cards"] = [_to_internal_data_audit_card(c) for c in h["citation_cards"]]
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("CITATION_CARD_MISSING" in e for e in report["errors"])


def _to_field_observation_card(citation: dict) -> dict:
    citation = dict(citation)
    for field in ("authors_or_issuer", "year", "source_type", "journal_or_repository", "persistent_id_or_official_url", "retrieved_at"):
        citation.pop(field, None)
    citation["observer"] = "test observer"
    citation["observation_method"] = "direct visual inspection"
    citation["observed_at"] = "2026-08-01T09:00:00+07:00"
    citation["location_or_context"] = "test site"
    return citation


def test_field_observation_log_review_mode_accepts_field_observation_citations():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_evidence_challenge"]["review_mode"] = "FIELD_OBSERVATION_LOG"
    for h in run["hypothesis_evidence_challenge"]["hypotheses"]:
        h["citation_cards"] = [_to_field_observation_card(c) for c in h["citation_cards"]]
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_targeted_search_review_mode_rejects_field_observation_citations():
    run = copy.deepcopy(_demo_checkpoint())
    for h in run["hypothesis_evidence_challenge"]["hypotheses"]:
        h["citation_cards"] = [_to_field_observation_card(c) for c in h["citation_cards"]]
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("CITATION_CARD_MISSING" in e for e in report["errors"])


def test_internal_data_audit_review_mode_rejects_field_observation_citations():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_evidence_challenge"]["review_mode"] = "INTERNAL_DATA_AUDIT"
    for h in run["hypothesis_evidence_challenge"]["hypotheses"]:
        h["citation_cards"] = [_to_field_observation_card(c) for c in h["citation_cards"]]
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("CITATION_CARD_MISSING" in e for e in report["errors"])


def test_small_direct_agency_may_leave_non_enforced_roles_empty():
    # 10-domain fit test (2026-08-01) found agents manufacturing filler content
    # for voice_holders/veto_or_consent_holders/represented_or_absent_parties/
    # power_exposure_voice_gaps/oversight_parties/resource_holders/
    # knowledge_holders/future_or_indirect_parties, assuming they were kernel-
    # required — the kernel only ever enforced 5 agency fields
    # (AGENCY_ROLE_EMPTY: affected, observers, decision_owners,
    # intervention_owners, accountable_parties). This test locks in that this
    # was already true, so it doesn't silently regress, and so the doc
    # clarification (FIELD_REFERENCE.md) stays accurate.
    run = copy.deepcopy(_demo_checkpoint())
    for field in (
        "voice_holders", "veto_or_consent_holders", "represented_or_absent_parties",
        "power_exposure_voice_gaps", "oversight_parties", "resource_holders",
        "knowledge_holders", "future_or_indirect_parties",
    ):
        if field in run["agency"]:
            run["agency"][field] = []
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]
