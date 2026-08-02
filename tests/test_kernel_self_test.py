import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

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


def _valid_verification_payload() -> dict:
    return {
        "payload_ref": "sha256:deadbeef",
        "entrypoint": "verify.py",
        "language": "PYTHON3",
        "declared_inputs": ["evidence.json"],
        "network_required": False,
        "resource_class": "LIGHT",
        "expected_exit_status": 0,
    }


def test_hypothesis_card_has_no_verification_payload_by_default():
    # Phase 1a (2026-08-02): most hypotheses are qualitative causal claims with
    # no executable payload at all -- the demo fixture must stay VALID_CHECKPOINT
    # with the field entirely absent, proving it's genuinely optional.
    run = copy.deepcopy(_demo_checkpoint())
    for card in run["hypothesis_portfolio"]["hypothesis_cards"]:
        assert "verification_payload" not in card
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_verification_payload_valid_shape_accepted():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = (
        _valid_verification_payload()
    )
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_verification_payload_not_object_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = "not-an-object"
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("VERIFICATION_PAYLOAD_NOT_OBJECT" in e for e in report["errors"])


def test_verification_payload_missing_field_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    del payload["expected_exit_status"]
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "VERIFICATION_PAYLOAD_MISSING" in e and "expected_exit_status" in e
        for e in report["errors"]
    )


def test_verification_payload_invalid_language_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["language"] = "PERL"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("INVALID_VERIFICATION_LANGUAGE" in e for e in report["errors"])


def test_verification_payload_invalid_resource_class_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["resource_class"] = "MEDIUM"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("INVALID_VERIFICATION_RESOURCE_CLASS" in e for e in report["errors"])


def test_verification_payload_declared_inputs_must_be_string_list():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["declared_inputs"] = "evidence.json"  # not a list
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "VERIFICATION_PAYLOAD_DECLARED_INPUTS_INVALID" in e for e in report["errors"]
    )


def test_verification_payload_network_required_must_be_bool():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["network_required"] = "false"  # string, not bool
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "VERIFICATION_PAYLOAD_NETWORK_REQUIRED_NOT_BOOL" in e for e in report["errors"]
    )


def test_verification_payload_expected_exit_status_must_be_int_not_bool():
    # bool is a subclass of int in Python -- must be explicitly excluded so
    # True/False can't silently pass as 1/0.
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["expected_exit_status"] = True
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "VERIFICATION_PAYLOAD_EXPECTED_EXIT_STATUS_NOT_INT" in e
        for e in report["errors"]
    )


def test_verification_payload_blank_payload_ref_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    payload = _valid_verification_payload()
    payload["payload_ref"] = "   "
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "VERIFICATION_PAYLOAD_BLANK" in e and "payload_ref" in e
        for e in report["errors"]
    )


# --- Phase 2 (2026-08-02): checker_result / MC-02 principal separation ---

def _valid_checker_result() -> dict:
    return {
        "maker_principal_id": "agent-session-abc",
        "checker_principal_id": "agent-session-xyz",
        "checker_type": "AI",
        "tier": "L0",
        "verdict": "APPROVED",
        "rationale": "Re-ran the raw_result mechanically, exit code matched.",
        "checked_at": "2026-08-02T12:00:00+07:00",
    }


def test_hypothesis_card_has_no_checker_result_by_default():
    run = copy.deepcopy(_demo_checkpoint())
    for card in run["hypothesis_portfolio"]["hypothesis_cards"]:
        assert "checker_result" not in card
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_checker_result_valid_distinct_principals_accepted():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = (
        _valid_checker_result()
    )
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_checker_result_can_exist_without_verification_payload():
    # A purely analytical hypothesis (no mechanical payload at all) can still
    # be human-reviewed and approved by judgment -- checker_result doesn't
    # require verification_payload to be present.
    run = copy.deepcopy(_demo_checkpoint())
    card = run["hypothesis_portfolio"]["hypothesis_cards"][0]
    assert "verification_payload" not in card
    card["checker_result"] = _valid_checker_result()
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_checker_result_same_principal_rejected():
    # This is the core MC-02 guarantee: the same principal cannot be both
    # maker and checker.
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["checker_principal_id"] = checker["maker_principal_id"]
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("CHECKER_RESULT_SAME_PRINCIPAL" in e for e in report["errors"])


def test_checker_result_not_object_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = "nope"
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("CHECKER_RESULT_NOT_OBJECT" in e for e in report["errors"])


def test_checker_result_missing_field_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    del checker["rationale"]
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "CHECKER_RESULT_MISSING" in e and "rationale" in e for e in report["errors"]
    )


def test_checker_result_invalid_checker_type_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["checker_type"] = "ROBOT"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("INVALID_CHECKER_TYPE" in e for e in report["errors"])


def test_checker_result_invalid_tier_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["tier"] = "L9"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("INVALID_CHECKER_TIER" in e for e in report["errors"])


def test_checker_result_invalid_verdict_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["verdict"] = "MAYBE"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any("INVALID_CHECKER_VERDICT" in e for e in report["errors"])


@pytest.mark.parametrize("tier", ["L3", "L4", "L5"])
def test_checker_tier_l3_plus_requires_human_not_ai(tier):
    # MIMCG L3+ requires a human final owner (cpg/AGENTS.md step 6.5,
    # ratified 2026-08-02) -- structurally enforced, not just documented.
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["tier"] = tier
    checker["checker_type"] = "AI"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "CHECKER_TIER_REQUIRES_HUMAN" in e and tier in e for e in report["errors"]
    )


@pytest.mark.parametrize("tier", ["L3", "L4", "L5"])
def test_checker_tier_l3_plus_accepts_human(tier):
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["tier"] = tier
    checker["checker_type"] = "HUMAN"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


@pytest.mark.parametrize("tier", ["L0", "L1", "L2"])
def test_checker_tier_below_l3_accepts_ai(tier):
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["tier"] = tier
    checker["checker_type"] = "AI"
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] == "VALID_CHECKPOINT", report["errors"]


def test_checker_result_blank_principal_ids_rejected():
    run = copy.deepcopy(_demo_checkpoint())
    checker = _valid_checker_result()
    checker["maker_principal_id"] = "   "
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"] = checker
    report = k.validate(run)
    assert report["protocol_status"] != "VALID_CHECKPOINT"
    assert any(
        "CHECKER_RESULT_BLANK" in e and "maker_principal_id" in e
        for e in report["errors"]
    )
