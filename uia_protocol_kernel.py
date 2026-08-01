#!/usr/bin/env python3
"""UIA v0.4.6 standalone protocol kernel.

This standard-library-only reference implementation validates protocol
structure and state transitions. It does not establish the truth, causal
validity, legality, legitimacy, or efficacy of domain claims.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


VERSION = "0.4.6"
ABSENT_PROPOSAL_TERMS = {
    "ไม่มี",
    "ไม่มีข้อเสนอ",
    "ข้าม",
    "none",
    "no",
    "no proposal",
    "skip",
}

ENUMS = {
    "continuation_policy": {
        "STOP_AT_HYPOTHESIS",
        "RUN_FULL",
    },
    "proposal_mode": {
        "AUTO",
        "USER_PROPOSAL_INTEGRATED",
        "AI_INDEPENDENT",
        "HYBRID_BLIND_COMPARE",
    },
    "intake_status": {
        "WAITING_FOR_ISSUE",
        "WAITING_FOR_PROPOSAL_RESPONSE",
        "INTAKE_COMPLETE",
        "INTAKE_PROTOCOL_FAIL",
    },
    "emergency_status": {
        "NOT_TRIGGERED",
        "CONTAINMENT_ACTIVE",
        "CONTAINMENT_ENDED",
        "CONTAINMENT_PROTOCOL_FAIL",
    },
    "stakeholder_map_status": {"CLOSED", "OPEN", "UNRESOLVED"},
    "issue_status": {
        "ISSUE_ADMITTED",
        "NO_ISSUE_UNDER_DECLARED_READOUT",
        "UNRESOLVED",
        "PROTOCOL_FAIL",
        "DRIFT",
    },
    "candidate_status": {
        "CANDIDATE_SET_COMPLETE",
        "CANDIDATE_SET_PARTIAL_2",
        "CANDIDATE_SET_PARTIAL_1",
        "INFORMATION_ONLY",
        "NO_ADMISSIBLE_SOLUTION",
    },
    "proposal_outcome": {
        "ADMITTED_AS_HYPOTHESIS",
        "REFRAMED_AS_HYPOTHESIS",
        "CHALLENGED_BY_HYPOTHESIS_PORTFOLIO",
        "ADMITTED_AS_CANDIDATE",
        "ADMITTED_AS_INFORMATION",
        "MERGED_DUPLICATE",
        "COMPLEMENTARY_COMPONENT",
        "NEEDS_REVISION",
        "BLOCKED_BY_RIGHTS",
        "OUT_OF_SCOPE",
        "HELD_OUT_BY_MODE",
        "UNRESOLVED",
        "NOT_APPLICABLE",
    },
    "result_status": {
        "PASS_EXACT",
        "PASS_TOLERANCED",
        "FAIL",
        "UNRESOLVED",
        "PROTOCOL_FAIL",
        "DRIFT",
    },
    "action_status": {
        "INTERVENE",
        "MONITOR",
        "HOLD",
        "BLOCK",
        "NO_ACTION_UNDER_SCOPE",
    },
    "claim_tier": {"Th_coqc", "exact", "finite_diagnostic", "Dr", "Open"},
    "evidence_challenge_status": {
        "EVIDENCE_CHALLENGE_COMPLETE",
        "EVIDENCE_CHALLENGE_PARTIAL",
        "LOCAL_EVIDENCE_NOT_FOUND",
        "CITATION_VERIFICATION_FAIL",
        "SEARCH_PROTOCOL_FAIL",
        "EVIDENCE_INSUFFICIENT",
    },
    "evidence_balance": {
        "SUPPORTS",
        "LEAN_SUPPORTS",
        "MIXED",
        "LEAN_CHALLENGES",
        "CHALLENGES",
        "INSUFFICIENT",
    },
    "global_certainty": {
        "HIGH",
        "MODERATE",
        "LOW",
        "VERY_LOW",
        "INSUFFICIENT",
    },
    "local_applicability": {
        "HIGH",
        "MODERATE",
        "LOW",
        "UNRESOLVED",
        "NO_ELIGIBLE_EVIDENCE_FOUND",
    },
    "transfer_status": {
        "DIRECTLY_APPLICABLE_WITH_DECLARED_SCOPE",
        "ADAPT_WITH_CONDITIONS",
        "TRANSFER_UNCERTAIN",
        "LOCALLY_INFORMATIVE_GLOBAL_MIXED",
        "LOCAL_SIGNAL_REQUIRES_TEST",
        "LOCALLY_CONTRADICTED",
        "NOT_TRANSFERABLE",
        "INSUFFICIENT_EVIDENCE",
    },
    "hypothesis_portfolio_status": {
        "HYPOTHESIS_PORTFOLIO_READY",
        "HYPOTHESIS_PORTFOLIO_PARTIAL",
        "HYPOTHESIS_PORTFOLIO_BLOCKED",
    },
    "legal_relevance": {
        "NONE",
        "CONTEXTUAL",
        "LOAD_BEARING",
    },
    "legal_status": {
        "NOT_REQUIRED",
        "NOT_REVIEWED",
        "PRELIMINARY",
        "VERIFIED_FOR_DECLARED_SCOPE",
        "UNRESOLVED",
    },
    "hypothesis_causal_tier": {
        "MECHANISM_HYPOTHESIS",
        "ASSOCIATIONAL_HYPOTHESIS",
        "STRUCTURAL_HYPOTHESIS",
        "NORMATIVE_HYPOTHESIS",
        "DESIGN_HYPOTHESIS",
        "UNRESOLVED",
    },
    "legitimacy_status": {
        "DIRECTLY_GROUNDED",
        "MIXED_GROUNDING",
        "INFERRED_NOT_FIELD_CONFIRMED",
        "BLOCKED_PENDING_REPRESENTATION",
    },
    "proposal_relation": {
        "INDEPENDENT",
        "SUPPORTS_USER_PROPOSAL",
        "CHALLENGES_USER_PROPOSAL",
        "REFRAMES_USER_PROPOSAL",
        "NOT_APPLICABLE",
    },
}

LANES = {
    "KNOWN_DIRECT",
    "CROSS_ADAPTIVE",
    "GENERATIVE_TRANSFORMATIVE",
}

CANONICAL_PHASES = [
    "0_TWO_QUESTION_INTAKE",
    "1_PROTECT",
    "2_READ_PHILOSOPHICALLY",
    "3_MAP_AGENCIES",
    "4_COMPILE_PERSPECTIVES",
    "5_ADMIT_ISSUE",
    "6_DETECT_DOMAIN",
    "7_DETECT_TOPOLOGY",
    "8_ROUTE_ADAPTERS",
    "9_EXECUTE",
    "10_INTEGRATE",
    "11_CHALLENGE_HYPOTHESES_WITH_EVIDENCE",
    "12_ROUTE_PROPOSAL",
    "13_GENERATE_CANDIDATES",
    "14_AUDIT_CANDIDATES",
    "15_AUDIT_TRANSLATION",
    "16_DECIDE",
    "17_ACT",
    "18_VERIFY",
    "19_CORRECT",
]

EMERGENCY_REQUIRED = {
    "reason",
    "scope",
    "rights_check",
    "owner",
    "stop_rule",
    "rollback_rule",
    "evidence_preservation",
    "review_due_at",
}

CANDIDATE_REQUIRED = {
    "candidate_id",
    "lane",
    "knowledge_basis",
    "mechanism_id",
    "hypothesis",
    "intervention",
    "expected_readout",
    "falsifier",
    "smallest_reversible_test",
    "rights_gate",
    "feasibility",
    "agency_effects",
    "hypothesis_ids",
    "evidence_ledger_refs",
}

HYPOTHESIS_REQUIRED = {
    "hypothesis_id",
    "lane",
    "claim",
    "mechanism",
    "boundary",
    "conditions",
    "affected_agencies",
    "predicted_readout",
    "alternative_explanations",
    "falsifier",
    "discriminating_information",
    "evidence_ledger_ref",
    "causal_tier",
    "legal_relevance",
    "legal_status",
    "authority_assumptions",
    "representation_status",
    "legitimacy_status",
    "proposal_relation",
    "uncertainties",
}

REPRESENTATION_REQUIRED = {
    "direct_voice",
    "authorized_proxy",
    "inferred_only",
    "absent_or_unreached",
}


def nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def get_path(data: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def proposal_presence(answer: Any) -> str:
    if not nonblank(answer):
        return "UNANSWERED"
    normalized = " ".join(str(answer).strip().lower().split())
    if normalized in ABSENT_PROPOSAL_TERMS:
        return "PROPOSAL_ABSENT_DECLARED"
    return "PROPOSAL_PRESENT"


def expected_mode(requested: str, presence: str) -> str | None:
    if requested not in ENUMS["proposal_mode"]:
        return None
    if requested == "AUTO":
        return (
            "AI_INDEPENDENT"
            if presence == "PROPOSAL_ABSENT_DECLARED"
            else "HYBRID_BLIND_COMPARE"
        )
    return requested


def candidate_status_for_count(count: int) -> str:
    if count >= 3:
        return "CANDIDATE_SET_COMPLETE"
    if count == 2:
        return "CANDIDATE_SET_PARTIAL_2"
    if count == 1:
        return "CANDIDATE_SET_PARTIAL_1"
    return "INFORMATION_ONLY"


def require_nonblank(
    data: dict[str, Any], paths: list[str], errors: list[str]
) -> None:
    for path in paths:
        if not nonblank(get_path(data, path)):
            errors.append(f"MISSING_OR_BLANK:{path}")


def validate_emergency(
    emergency: Any, errors: list[str], warnings: list[str]
) -> str:
    if emergency is None:
        return "NOT_TRIGGERED"
    if not isinstance(emergency, dict):
        errors.append("EMERGENCY_RECORD_NOT_OBJECT")
        return "CONTAINMENT_PROTOCOL_FAIL"
    status = emergency.get("status", "NOT_TRIGGERED")
    if status not in ENUMS["emergency_status"]:
        errors.append(f"INVALID_EMERGENCY_STATUS:{status}")
        return "CONTAINMENT_PROTOCOL_FAIL"
    if status == "NOT_TRIGGERED":
        return status
    missing = sorted(
        field for field in EMERGENCY_REQUIRED if not emergency.get(field)
    )
    if missing:
        errors.append("EMERGENCY_CONTRACT_MISSING:" + ",".join(missing))
    prohibited = {
        "cause",
        "causal_verdict",
        "selected_solution",
        "candidate_winner",
        "issue_verdict",
    }
    present = sorted(field for field in prohibited if emergency.get(field))
    if present:
        errors.append("EMERGENCY_BYPASS_EXCEEDED_SCOPE:" + ",".join(present))
    if emergency.get("analysis_allowed") is True:
        errors.append("EMERGENCY_BYPASS_ANALYSIS_NOT_ALLOWED")
    if emergency.get("reversible") is False:
        errors.append("EMERGENCY_CONTAINMENT_NOT_REVERSIBLE")
    if emergency.get("evidence_preservation") not in {
        "PRESERVED",
        "NOT_APPLICABLE",
        True,
    }:
        warnings.append("EMERGENCY_EVIDENCE_PRESERVATION_UNCLEAR")
    return status


def validate(run: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    trace: list[str] = ["0_TWO_QUESTION_INTAKE"]

    if not isinstance(run, dict):
        return {
            "protocol_version": VERSION,
            "protocol_status": "PROTOCOL_FAIL",
            "state": "INPUT_NOT_OBJECT",
            "errors": ["INPUT_NOT_OBJECT"],
            "warnings": [],
            "phase_trace": trace,
            "claim_boundary": "STRUCTURE_ONLY",
        }

    supplied_version = run.get("protocol_version")
    if supplied_version != VERSION:
        return {
            "protocol_version": VERSION,
            "protocol_status": "DRIFT",
            "state": "SPEC_RUNTIME_DRIFT",
            "errors": [
                f"VERSION_MISMATCH:expected={VERSION},received={supplied_version}"
            ],
            "warnings": [],
            "phase_trace": trace,
            "claim_boundary": "STRUCTURE_ONLY",
        }

    run_control = run.get("run_control")
    if not isinstance(run_control, dict):
        errors.append("MISSING_OBJECT:run_control")
        run_control = {}
    continuation_policy = run_control.get("continuation_policy")
    if continuation_policy not in ENUMS["continuation_policy"]:
        errors.append(
            f"INVALID_CONTINUATION_POLICY:{continuation_policy}"
        )
    if not nonblank(run_control.get("requested_by")):
        errors.append("MISSING_OR_BLANK:run_control.requested_by")
    if not nonblank(run_control.get("continuation_record")):
        errors.append("MISSING_OR_BLANK:run_control.continuation_record")

    emergency_status = validate_emergency(
        run.get("emergency_containment"), errors, warnings
    )
    trace.append("1_PROTECT")

    intake = run.get("two_question_intake")
    if not isinstance(intake, dict):
        errors.append("MISSING_OBJECT:two_question_intake")
        intake = {}
    q1 = intake.get("q1_answer_verbatim")
    q2_supplied = "q2_answer_verbatim" in intake
    q2 = intake.get("q2_answer_verbatim")

    if not nonblank(q1):
        state = "WAITING_FOR_ISSUE"
    elif not q2_supplied or not nonblank(q2):
        state = "WAITING_FOR_PROPOSAL_RESPONSE"
    else:
        state = "INTAKE_COMPLETE"

    declared_entry = intake.get("entry_status")
    if declared_entry is not None and declared_entry not in ENUMS["intake_status"]:
        errors.append(f"INVALID_INTAKE_STATUS:{declared_entry}")
    if declared_entry is not None and declared_entry != state:
        errors.append(
            f"INTAKE_STATUS_MISMATCH:declared={declared_entry},derived={state}"
        )

    if state != "INTAKE_COMPLETE":
        if emergency_status != "NOT_TRIGGERED" and errors:
            status = "PROTOCOL_FAIL"
            state = "CONTAINMENT_PROTOCOL_FAIL"
        elif errors:
            status = "PROTOCOL_FAIL"
        else:
            status = "WAITING"
        return {
            "protocol_version": VERSION,
            "protocol_status": status,
            "state": state,
            "proposal_presence": (
                proposal_presence(q2) if q2_supplied else "UNANSWERED"
            ),
            "emergency_status": emergency_status,
            "errors": errors,
            "warnings": warnings,
            "phase_trace": trace,
            "analysis_entry_allowed": False,
            "claim_boundary": "STRUCTURE_ONLY",
        }

    presence = proposal_presence(q2)
    declared_presence = intake.get("q2_presence")
    if declared_presence is not None and declared_presence != presence:
        errors.append(
            "PROPOSAL_PRESENCE_MISMATCH:"
            f"declared={declared_presence},derived={presence}"
        )
    if not nonblank(intake.get("certificate")):
        errors.append("MISSING_OR_BLANK:two_question_intake.certificate")

    proposal = run.get("proposal_input")
    if not isinstance(proposal, dict):
        errors.append("MISSING_OBJECT:proposal_input")
        proposal = {}
    requested_mode = proposal.get("requested_mode", "AUTO")
    if requested_mode not in ENUMS["proposal_mode"]:
        errors.append(f"INVALID_PROPOSAL_MODE:{requested_mode}")
    resolved_mode = expected_mode(str(requested_mode), presence)
    if proposal.get("resolved_mode") != resolved_mode:
        errors.append(
            "PROPOSAL_MODE_MISMATCH:"
            f"declared={proposal.get('resolved_mode')},derived={resolved_mode}"
        )
    if presence == "PROPOSAL_PRESENT" and not nonblank(
        proposal.get("proposal_verbatim")
    ):
        errors.append("MISSING_OR_BLANK:proposal_input.proposal_verbatim")
    if presence == "PROPOSAL_ABSENT_DECLARED" and proposal.get(
        "outcome"
    ) not in {None, "NOT_APPLICABLE"}:
        errors.append("ABSENT_PROPOSAL_MUST_BE_NOT_APPLICABLE")
    outcome = proposal.get("outcome", "NOT_APPLICABLE")
    if outcome not in ENUMS["proposal_outcome"]:
        errors.append(f"INVALID_PROPOSAL_OUTCOME:{outcome}")

    require_nonblank(
        run,
        [
            "registration.query",
            "registration.decision_to_support",
            "registration.requester",
            "registration.success_rule",
            "registration.failure_rule",
            "registration.abstention_rule",
            "context.time_index",
            "context.location_or_domain",
            "context.boundary",
            "context.horizon",
            "context.resolution",
            "translation.raw_user_expression",
            "translation.selected_domain_projection",
            "translation.user_facing_issue_statement",
            "retained_difference.baseline",
            "retained_difference.comparison",
            "retained_difference.lineage",
        ],
        errors,
    )
    trace.extend(
        [
            "2_READ_PHILOSOPHICALLY",
            "3_MAP_AGENCIES",
            "4_COMPILE_PERSPECTIVES",
        ]
    )

    agency = run.get("agency")
    if not isinstance(agency, dict):
        errors.append("MISSING_OBJECT:agency")
        agency = {}
    for field in {
        "affected",
        "observers",
        "decision_owners",
        "intervention_owners",
        "accountable_parties",
    }:
        value = agency.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"AGENCY_ROLE_EMPTY:{field}")
    stakeholder_status = agency.get("stakeholder_map_status")
    if stakeholder_status not in ENUMS["stakeholder_map_status"]:
        errors.append(f"INVALID_STAKEHOLDER_MAP_STATUS:{stakeholder_status}")

    loss_audit = get_path(run, "translation.loss_audit")
    if loss_audit not in {"PASS", "REVISE", "BLOCK"}:
        errors.append(f"INVALID_TRANSLATION_LOSS_AUDIT:{loss_audit}")

    final = run.get("final")
    if continuation_policy == "RUN_FULL":
        if not isinstance(final, dict):
            errors.append("MISSING_OBJECT:final")
            final = {}
        issue_status = final.get("issue_status")
    else:
        if final is None:
            final = {}
        elif not isinstance(final, dict):
            errors.append("FINAL_RECORD_NOT_OBJECT")
            final = {}
        issue_status = get_path(run, "issue.candidate_state")
    if issue_status not in ENUMS["issue_status"]:
        errors.append(f"INVALID_ISSUE_STATUS:{issue_status}")
    trace.extend(
        [
            "5_ADMIT_ISSUE",
            "6_DETECT_DOMAIN",
            "7_DETECT_TOPOLOGY",
            "8_ROUTE_ADAPTERS",
            "9_EXECUTE",
            "10_INTEGRATE",
        ]
    )

    causal = run.get("causal_analysis")
    if not isinstance(causal, dict):
        errors.append("MISSING_OBJECT:causal_analysis")
        causal = {}
    if not isinstance(causal.get("candidates"), list):
        errors.append("CAUSAL_CANDIDATES_NOT_LIST")
    if not isinstance(causal.get("alternatives"), list):
        errors.append("CAUSAL_ALTERNATIVES_NOT_LIST")
    if not nonblank(causal.get("causal_tier")):
        errors.append("MISSING_OR_BLANK:causal_analysis.causal_tier")

    evidence = run.get("hypothesis_evidence_challenge")
    if not isinstance(evidence, dict):
        errors.append("MISSING_OBJECT:hypothesis_evidence_challenge")
        evidence = {}
    for field in {"search_protocol_id", "frozen_at", "review_mode"}:
        if not evidence.get(field):
            errors.append(f"EVIDENCE_CHALLENGE_MISSING:{field}")
    if evidence.get("synthesis_method") != (
        "QUALITY_DIRECTNESS_CONTEXT_NOT_VOTE_COUNT"
    ):
        errors.append("EVIDENCE_SYNTHESIS_MUST_NOT_USE_VOTE_COUNT")
    evidence_status = evidence.get("status")
    if evidence_status not in ENUMS["evidence_challenge_status"]:
        errors.append(f"INVALID_EVIDENCE_CHALLENGE_STATUS:{evidence_status}")
    target_context = evidence.get("target_context")
    if not isinstance(target_context, dict):
        errors.append("EVIDENCE_TARGET_CONTEXT_NOT_OBJECT")
        target_context = {}
    for field in {"country", "institutions_and_population"}:
        if not target_context.get(field):
            errors.append(f"EVIDENCE_TARGET_CONTEXT_MISSING:{field}")
    languages = target_context.get("languages")
    if not isinstance(languages, list) or not languages:
        errors.append("EVIDENCE_LOCAL_LANGUAGES_EMPTY")

    hypothesis_ledgers = evidence.get("hypotheses")
    if not isinstance(hypothesis_ledgers, list) or not hypothesis_ledgers:
        errors.append("HYPOTHESIS_EVIDENCE_LEDGERS_EMPTY")
        hypothesis_ledgers = []
    ledger_ids: set[str] = set()
    hypothesis_ids: set[str] = set()
    simulated = bool(get_path(run, "metadata.simulation", False))
    # review_mode INTERNAL_DATA_AUDIT: same rigor (falsifier, source classes,
    # result_status, citation_audit, the certainty/applicability enums below all
    # still apply unconditionally) but the per-citation fields swap the
    # literature-index vocabulary (authors_or_issuer, journal_or_repository,
    # persistent_id_or_official_url) for an internal-system-of-record vocabulary,
    # since the realistic evidence base for many operational issues is EHR/
    # payment-ledger/sensor/ticketing logs, not published sources. Any other
    # review_mode value (including the pre-existing TARGETED_SEARCH) keeps the
    # original literature schema unchanged — fully backward compatible.
    if evidence.get("review_mode") == "INTERNAL_DATA_AUDIT":
        citation_required = {
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
    elif evidence.get("review_mode") == "FIELD_OBSERVATION_LOG":
        # Same rigor as the other two modes (falsifier, source classes,
        # result_status, citation_audit, the certainty/applicability enums
        # below all still apply unconditionally) but the per-citation fields
        # swap literature/internal-system vocabulary for a fresh-field-
        # observation vocabulary — a 10-domain fit test found citation_cards'
        # literature framing was dead weight in domains whose real evidence is
        # a sensory/field readout at the moment of observation (a baker's
        # dough, a tagged tree at a census date, a coach's session notes), not
        # a citable document. `observed_at` replaces `retrieved_at` since
        # there is no separate "retrieval" step from a "publication."
        citation_required = {
            "citation_id",
            "title",
            "observer",
            "observation_method",
            "observed_at",
            "location_or_context",
            "context_country_or_region",
            "claim_supported_or_challenged",
            "direction",
            "quality",
            "directness",
            "context_fit",
            "metadata_verification",
            "scope_verification",
        }
    else:
        citation_required = {
            "citation_id",
            "title",
            "authors_or_issuer",
            "year",
            "source_type",
            "journal_or_repository",
            "persistent_id_or_official_url",
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
    for index, ledger in enumerate(hypothesis_ledgers):
        if not isinstance(ledger, dict):
            errors.append(f"HYPOTHESIS_EVIDENCE_NOT_OBJECT:{index}")
            continue
        for field in {
            "hypothesis_id",
            "hypothesis",
            "falsifier",
            "ledger_id",
            "next_discriminating_test",
        }:
            if not ledger.get(field):
                errors.append(
                    f"HYPOTHESIS_EVIDENCE_MISSING:{index}:{field}"
                )
        hypothesis_id = str(ledger.get("hypothesis_id", ""))
        ledger_id = str(ledger.get("ledger_id", ""))
        if hypothesis_id in hypothesis_ids:
            errors.append(f"DUPLICATE_HYPOTHESIS_ID:{hypothesis_id}")
        if ledger_id in ledger_ids:
            errors.append(f"DUPLICATE_EVIDENCE_LEDGER_ID:{ledger_id}")
        hypothesis_ids.add(hypothesis_id)
        ledger_ids.add(ledger_id)

        for track_name in {"international_track", "local_context_track"}:
            track = ledger.get(track_name)
            if not isinstance(track, dict):
                errors.append(
                    f"EVIDENCE_TRACK_NOT_OBJECT:{index}:{track_name}"
                )
                continue
            for query_field in {"support_queries", "challenge_queries"}:
                queries = track.get(query_field)
                if not isinstance(queries, list) or not queries:
                    errors.append(
                        f"EVIDENCE_QUERIES_EMPTY:{index}:{track_name}:"
                        f"{query_field}"
                    )
            sources = track.get("sources_searched")
            if not isinstance(sources, list) or not sources:
                errors.append(
                    f"EVIDENCE_SOURCES_EMPTY:{index}:{track_name}"
                )
            if not track.get("result_status"):
                errors.append(
                    f"EVIDENCE_RESULT_STATUS_MISSING:{index}:{track_name}"
                )
        local_track = ledger.get("local_context_track", {})
        local_status = (
            local_track.get("result_status")
            if isinstance(local_track, dict)
            else None
        )
        if local_status == "NO_LOCAL_EVIDENCE_EXISTS":
            errors.append("FORBIDDEN_LOCAL_ABSENCE_CLAIM")
        if local_status not in {
            "LOCAL_EVIDENCE_FOUND",
            "LOCAL_EVIDENCE_NOT_FOUND",
        }:
            errors.append(
                f"INVALID_LOCAL_EVIDENCE_RESULT_STATUS:{local_status}"
            )
        source_classes = (
            local_track.get("source_classes_searched")
            if isinstance(local_track, dict)
            else None
        )
        if not isinstance(source_classes, list) or len(source_classes) < 2:
            errors.append(
                f"LOCAL_SOURCE_CLASSES_INSUFFICIENT:{index}"
            )

        for list_field in {
            "supporting_evidence",
            "challenging_evidence",
            "citation_cards",
            "evidence_gaps",
        }:
            if not isinstance(ledger.get(list_field), list):
                errors.append(
                    f"HYPOTHESIS_EVIDENCE_LIST_REQUIRED:{index}:{list_field}"
                )
        cards_for_hypothesis = ledger.get("citation_cards")
        if not isinstance(cards_for_hypothesis, list):
            cards_for_hypothesis = []
        for card_index, citation in enumerate(cards_for_hypothesis):
            if not isinstance(citation, dict):
                errors.append(
                    f"CITATION_CARD_NOT_OBJECT:{index}:{card_index}"
                )
                continue
            missing = sorted(
                field for field in citation_required if not citation.get(field)
            )
            if missing:
                errors.append(
                    f"CITATION_CARD_MISSING:{index}:{card_index}:"
                    + ",".join(missing)
                )
            allowed_verification = (
                {"VERIFIED", "SIMULATED_ONLY"}
                if simulated
                else {"VERIFIED"}
            )
            if citation.get("metadata_verification") not in (
                allowed_verification
            ):
                errors.append(
                    f"CITATION_METADATA_NOT_VERIFIED:{index}:{card_index}"
                )
            if citation.get("scope_verification") not in (
                allowed_verification
            ):
                errors.append(
                    f"CITATION_SCOPE_NOT_VERIFIED:{index}:{card_index}"
                )
        if ledger.get("citation_audit") != "PASS":
            errors.append(f"CITATION_AUDIT_NOT_PASS:{index}")
        for enum_name in {
            "global_certainty",
            "local_applicability",
            "evidence_balance",
            "transfer_status",
        }:
            value = ledger.get(enum_name)
            if value not in ENUMS[enum_name]:
                errors.append(
                    f"INVALID_{enum_name.upper()}:{index}:{value}"
                )

    trace.extend(
        [
            "11_CHALLENGE_HYPOTHESES_WITH_EVIDENCE",
            "12_ROUTE_PROPOSAL",
        ]
    )

    hypothesis_portfolio = run.get("hypothesis_portfolio")
    if not isinstance(hypothesis_portfolio, dict):
        errors.append("MISSING_OBJECT:hypothesis_portfolio")
        hypothesis_portfolio = {}
    hypothesis_cards = hypothesis_portfolio.get("hypothesis_cards")
    if not isinstance(hypothesis_cards, list) or not hypothesis_cards:
        errors.append("HYPOTHESIS_PORTFOLIO_CARDS_EMPTY")
        hypothesis_cards = []
    portfolio_hypothesis_ids: set[str] = set()
    hypothesis_lanes: set[str] = set()
    hypothesis_mechanisms: list[str] = []
    proposal_relations: set[str] = set()
    for index, card in enumerate(hypothesis_cards):
        if not isinstance(card, dict):
            errors.append(f"HYPOTHESIS_CARD_NOT_OBJECT:{index}")
            continue
        # authority_assumptions is checked separately below: it may be genuinely
        # empty when a hypothesis has no legal/authority dimension at all
        # (legal_relevance=NONE, legal_status=NOT_REQUIRED) — forcing filler
        # content there for e.g. a purely mechanical/signal-processing hypothesis
        # would just add noise, not a real authority consideration.
        missing = sorted(
            field
            for field in HYPOTHESIS_REQUIRED - {"authority_assumptions"}
            if not card.get(field)
        )
        authority_assumptions = card.get("authority_assumptions")
        no_authority_dimension = (
            card.get("legal_relevance") == "NONE"
            and card.get("legal_status") == "NOT_REQUIRED"
        )
        if not isinstance(authority_assumptions, list):
            missing.append("authority_assumptions")
        elif not authority_assumptions and not no_authority_dimension:
            missing.append("authority_assumptions")
        missing = sorted(missing)
        if missing:
            errors.append(
                f"HYPOTHESIS_CARD_MISSING:{index}:" + ",".join(missing)
            )
        hypothesis_id = str(card.get("hypothesis_id", ""))
        if hypothesis_id in portfolio_hypothesis_ids:
            errors.append(
                f"DUPLICATE_PORTFOLIO_HYPOTHESIS_ID:{hypothesis_id}"
            )
        portfolio_hypothesis_ids.add(hypothesis_id)
        if hypothesis_id not in hypothesis_ids:
            errors.append(
                f"PORTFOLIO_HYPOTHESIS_ID_NOT_IN_EVIDENCE:{hypothesis_id}"
            )
        ledger_ref = card.get("evidence_ledger_ref")
        if ledger_ref not in ledger_ids:
            errors.append(
                f"PORTFOLIO_EVIDENCE_REF_UNKNOWN:{hypothesis_id}:{ledger_ref}"
            )
        lane = card.get("lane")
        if lane not in LANES:
            errors.append(
                f"INVALID_HYPOTHESIS_LANE:{hypothesis_id}:{lane}"
            )
        else:
            hypothesis_lanes.add(str(lane))
        mechanism = " ".join(
            str(card.get("mechanism", "")).lower().split()
        )
        if mechanism:
            hypothesis_mechanisms.append(mechanism)
        no_authority_dimension = (
            card.get("legal_relevance") == "NONE"
            and card.get("legal_status") == "NOT_REQUIRED"
        )
        for list_field in {
            "conditions",
            "affected_agencies",
            "alternative_explanations",
            "discriminating_information",
            "authority_assumptions",
            "uncertainties",
        }:
            value = card.get(list_field)
            if not isinstance(value, list):
                errors.append(
                    f"HYPOTHESIS_CARD_LIST_EMPTY:{hypothesis_id}:{list_field}"
                )
            elif not value and not (
                list_field == "authority_assumptions" and no_authority_dimension
            ):
                errors.append(
                    f"HYPOTHESIS_CARD_LIST_EMPTY:{hypothesis_id}:{list_field}"
                )
        causal_tier = card.get("causal_tier")
        if causal_tier not in ENUMS["hypothesis_causal_tier"]:
            errors.append(
                f"INVALID_HYPOTHESIS_CAUSAL_TIER:"
                f"{hypothesis_id}:{causal_tier}"
            )
        legal_relevance = card.get("legal_relevance")
        legal_status = card.get("legal_status")
        if legal_relevance not in ENUMS["legal_relevance"]:
            errors.append(
                f"INVALID_LEGAL_RELEVANCE:{hypothesis_id}:{legal_relevance}"
            )
        if legal_status not in ENUMS["legal_status"]:
            errors.append(
                f"INVALID_LEGAL_STATUS:{hypothesis_id}:{legal_status}"
            )
        if legal_relevance == "NONE" and legal_status != "NOT_REQUIRED":
            errors.append(
                f"LEGAL_NONE_REQUIRES_NOT_REQUIRED:{hypothesis_id}"
            )
        if (
            legal_relevance == "LOAD_BEARING"
            and legal_status == "NOT_REQUIRED"
        ):
            errors.append(
                f"LOAD_BEARING_LEGAL_CLAIM_NOT_REVIEWED:{hypothesis_id}"
            )
        representation = card.get("representation_status")
        if not isinstance(representation, dict):
            errors.append(
                f"REPRESENTATION_STATUS_NOT_OBJECT:{hypothesis_id}"
            )
            representation = {}
        represented_count = 0
        for representation_field in REPRESENTATION_REQUIRED:
            value = representation.get(representation_field)
            if not isinstance(value, list):
                errors.append(
                    f"REPRESENTATION_FIELD_NOT_LIST:"
                    f"{hypothesis_id}:{representation_field}"
                )
            else:
                represented_count += len(value)
        if represented_count == 0:
            errors.append(
                f"REPRESENTATION_STATUS_EMPTY:{hypothesis_id}"
            )
        legitimacy_status = card.get("legitimacy_status")
        if legitimacy_status not in ENUMS["legitimacy_status"]:
            errors.append(
                f"INVALID_LEGITIMACY_STATUS:"
                f"{hypothesis_id}:{legitimacy_status}"
            )
        relation = card.get("proposal_relation")
        if relation not in ENUMS["proposal_relation"]:
            errors.append(
                f"INVALID_PROPOSAL_RELATION:{hypothesis_id}:{relation}"
            )
        else:
            proposal_relations.add(str(relation))

    if len(hypothesis_mechanisms) != len(set(hypothesis_mechanisms)):
        errors.append("HYPOTHESIS_DIVERSITY_FAIL:DUPLICATE_MECHANISM")
    hypothesis_portfolio_status = hypothesis_portfolio.get("status")
    if hypothesis_portfolio_status not in ENUMS[
        "hypothesis_portfolio_status"
    ]:
        errors.append(
            f"INVALID_HYPOTHESIS_PORTFOLIO_STATUS:"
            f"{hypothesis_portfolio_status}"
        )
    if hypothesis_portfolio_status == "HYPOTHESIS_PORTFOLIO_READY":
        if len(hypothesis_cards) < 3 or hypothesis_lanes != LANES:
            errors.append(
                "HYPOTHESIS_READY_REQUIRES_ALL_THREE_LANES"
            )
        if any(
            card.get("legitimacy_status")
            == "BLOCKED_PENDING_REPRESENTATION"
            for card in hypothesis_cards
            if isinstance(card, dict)
        ):
            errors.append(
                "HYPOTHESIS_READY_BLOCKED_BY_REPRESENTATION"
            )
    if hypothesis_portfolio.get("diversity_test") != "PASS":
        errors.append("HYPOTHESIS_DIVERSITY_GATE_NOT_PASS")
    if hypothesis_portfolio.get("evidence_linkage_test") != "PASS":
        errors.append("HYPOTHESIS_EVIDENCE_LINKAGE_NOT_PASS")
    if not nonblank(hypothesis_portfolio.get("checkpoint_certificate")):
        errors.append(
            "MISSING_OR_BLANK:hypothesis_portfolio.checkpoint_certificate"
        )
    if presence == "PROPOSAL_PRESENT" and not (
        proposal_relations
        - {"INDEPENDENT", "NOT_APPLICABLE"}
    ):
        errors.append("USER_PROPOSAL_NOT_COMPARED_IN_HYPOTHESIS_PORTFOLIO")

    if continuation_policy == "STOP_AT_HYPOTHESIS":
        downstream = {
            "candidate_portfolio",
            "intervention",
            "checker",
            "final",
        }
        if any(name in run for name in downstream):
            warnings.append(
                "DOWNSTREAM_RECORDS_PRESENT_BUT_NOT_EVALUATED_AT_CHECKPOINT"
            )
        if errors:
            checkpoint_protocol_status = "PROTOCOL_FAIL"
            checkpoint_state = "PROTOCOL_FAIL"
        else:
            checkpoint_protocol_status = "VALID_CHECKPOINT"
            checkpoint_state = "HYPOTHESIS_PORTFOLIO_READY"
        return {
            "protocol_version": VERSION,
            "protocol_status": checkpoint_protocol_status,
            "state": checkpoint_state,
            "continuation_policy": continuation_policy,
            "continuation_available": True,
            "next_phase": "13_GENERATE_CANDIDATES",
            "continuation_record": run_control.get("continuation_record"),
            "proposal_presence": presence,
            "resolved_mode": resolved_mode,
            "emergency_status": emergency_status,
            "evidence_challenge_status": evidence_status,
            "hypothesis_portfolio_status": hypothesis_portfolio_status,
            "issue_status": issue_status,
            "errors": errors,
            "warnings": warnings,
            "phase_trace": trace,
            "analysis_entry_allowed": True,
            "claim_boundary": (
                "HYPOTHESIS_PORTFOLIO_ONLY;"
                "NO_DECISION_INTERVENTION_OR_FIELD_TRUTH_CLAIM"
            ),
        }

    portfolio = run.get("candidate_portfolio")
    if not isinstance(portfolio, dict):
        errors.append("MISSING_OBJECT:candidate_portfolio")
        portfolio = {}
    cards = portfolio.get("candidate_cards")
    if not isinstance(cards, list):
        errors.append("CANDIDATE_CARDS_NOT_LIST")
        cards = []
    seen_ids: set[str] = set()
    seen_lanes: set[str] = set()
    mechanisms: list[str] = []
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            errors.append(f"CANDIDATE_NOT_OBJECT:{index}")
            continue
        missing = sorted(
            field for field in CANDIDATE_REQUIRED if not card.get(field)
        )
        if missing:
            errors.append(
                f"CANDIDATE_MISSING:{index}:" + ",".join(missing)
            )
        candidate_id = str(card.get("candidate_id", ""))
        if candidate_id in seen_ids:
            errors.append(f"DUPLICATE_CANDIDATE_ID:{candidate_id}")
        seen_ids.add(candidate_id)
        lane = card.get("lane")
        if lane not in LANES:
            errors.append(f"INVALID_CANDIDATE_LANE:{lane}")
        else:
            seen_lanes.add(lane)
        mechanism = " ".join(str(card.get("mechanism_id", "")).lower().split())
        if mechanism:
            mechanisms.append(mechanism)
        if card.get("rights_gate") != "PASS":
            warnings.append(f"CANDIDATE_RIGHTS_NOT_PASS:{candidate_id}")
        card_hypotheses = card.get("hypothesis_ids")
        card_ledgers = card.get("evidence_ledger_refs")
        if not isinstance(card_hypotheses, list) or not card_hypotheses:
            errors.append(f"CANDIDATE_HYPOTHESIS_REFS_EMPTY:{candidate_id}")
        elif any(ref not in hypothesis_ids for ref in card_hypotheses):
            errors.append(f"CANDIDATE_HYPOTHESIS_REF_UNKNOWN:{candidate_id}")
        if not isinstance(card_ledgers, list) or not card_ledgers:
            errors.append(f"CANDIDATE_EVIDENCE_REFS_EMPTY:{candidate_id}")
        elif any(ref not in ledger_ids for ref in card_ledgers):
            errors.append(f"CANDIDATE_EVIDENCE_REF_UNKNOWN:{candidate_id}")
    if len(mechanisms) != len(set(mechanisms)):
        errors.append("CANDIDATE_DIVERSITY_FAIL:DUPLICATE_MECHANISM")
    declared_candidate_status = portfolio.get("status")
    if declared_candidate_status not in ENUMS["candidate_status"]:
        errors.append(f"INVALID_CANDIDATE_STATUS:{declared_candidate_status}")
    derived_candidate_status = candidate_status_for_count(len(cards))
    if declared_candidate_status == "CANDIDATE_SET_COMPLETE":
        if len(cards) < 3 or seen_lanes != LANES:
            errors.append("COMPLETE_SET_REQUIRES_ALL_THREE_LANES")
    elif declared_candidate_status not in {
        "INFORMATION_ONLY",
        "NO_ADMISSIBLE_SOLUTION",
    } and declared_candidate_status != derived_candidate_status:
        errors.append(
            "CANDIDATE_STATUS_MISMATCH:"
            f"declared={declared_candidate_status},derived={derived_candidate_status}"
        )
    if portfolio.get("diversity_test") != "PASS" and len(cards) > 1:
        errors.append("CANDIDATE_DIVERSITY_GATE_NOT_PASS")
    if portfolio.get("rights_and_feasibility_gate") != "PASS":
        warnings.append("PORTFOLIO_RIGHTS_OR_FEASIBILITY_NOT_PASS")

    trace.extend(
        [
            "13_GENERATE_CANDIDATES",
            "14_AUDIT_CANDIDATES",
            "15_AUDIT_TRANSLATION",
            "16_DECIDE",
        ]
    )

    intervention = run.get("intervention")
    if not isinstance(intervention, dict):
        errors.append("MISSING_OBJECT:intervention")
        intervention = {}
    action_status = final.get("action_status")
    if action_status not in ENUMS["action_status"]:
        errors.append(f"INVALID_ACTION_STATUS:{action_status}")
    if action_status == "INTERVENE":
        for field in {
            "selected",
            "owner",
            "rights_check",
            "stop_rule",
            "rollback_rule",
            "expected_readout",
        }:
            if not intervention.get(field):
                errors.append(f"INTERVENTION_MISSING:{field}")
    trace.append("17_ACT")

    checker = run.get("checker")
    if not isinstance(checker, dict):
        errors.append("MISSING_OBJECT:checker")
        checker = {}
    result_status = final.get("result_status")
    if result_status not in ENUMS["result_status"]:
        errors.append(f"INVALID_RESULT_STATUS:{result_status}")
    if result_status in {"PASS_EXACT", "PASS_TOLERANCED", "FAIL"}:
        require_nonblank(
            run,
            [
                "checker.baseline_readout",
                "checker.post_readout",
                "checker.frozen_target",
            ],
            errors,
        )
    trace.extend(["18_VERIFY", "19_CORRECT"])

    closure = final.get("closure_status")
    if closure not in {"CLOSED", "MONITOR", "REOPEN"}:
        errors.append(f"INVALID_CLOSURE_STATUS:{closure}")
    if closure == "CLOSED" and stakeholder_status != "CLOSED":
        errors.append("CANNOT_CLOSE_WITH_OPEN_OR_UNRESOLVED_STAKEHOLDER_MAP")
    if closure == "CLOSED" and loss_audit != "PASS":
        errors.append("CANNOT_CLOSE_WITH_TRANSLATION_LOSS_DEFECT")
    require_nonblank(
        run,
        [
            "final.claim_scope",
            "final.uncertainty",
            "final.reproducibility_or_audit_path",
            "final.correction_path",
            "final.weakest_claim_tier",
        ],
        errors,
    )
    tier = final.get("weakest_claim_tier")
    if tier not in ENUMS["claim_tier"]:
        errors.append(f"INVALID_CLAIM_TIER:{tier}")

    if errors:
        protocol_status = "PROTOCOL_FAIL"
        state = "PROTOCOL_FAIL"
    else:
        protocol_status = "VALID"
        state = closure or "MONITOR"

    return {
        "protocol_version": VERSION,
        "protocol_status": protocol_status,
        "state": state,
        "continuation_policy": continuation_policy,
        "continuation_available": False,
        "continuation_record": run_control.get("continuation_record"),
        "proposal_presence": presence,
        "resolved_mode": resolved_mode,
        "emergency_status": emergency_status,
        "evidence_challenge_status": evidence_status,
        "hypothesis_portfolio_status": hypothesis_portfolio_status,
        "candidate_status": declared_candidate_status,
        "issue_status": issue_status,
        "result_status": result_status,
        "errors": errors,
        "warnings": warnings,
        "phase_trace": trace,
        "analysis_entry_allowed": True,
        "claim_boundary": (
            "PROTOCOL_STRUCTURE_ONLY;DOMAIN_TRUTH_AND_EFFICACY_NOT_CONFIRMED"
        ),
    }


def demo_run() -> dict[str, Any]:
    return {
        "protocol_version": VERSION,
        "run_control": {
            "continuation_policy": "RUN_FULL",
            "requested_by": "built-in demo",
            "continuation_record": "CONT-UIA-046-DEMO-001",
        },
        "metadata": {
            "label": "[SimulatedData]",
            "simulation": True,
            "fixture_id": "UIA-046-E2E-WEB-BOOKING-001",
        },
        "two_question_intake": {
            "q1_prompt": "Issue คืออะไร?",
            "q1_answer_verbatim": (
                "ผู้ใช้บางรายกดยืนยันการจองแล้วหน้าเว็บแสดงว่ากำลังประมวลผล"
                "นานเกินเกณฑ์และไม่ทราบว่าจองสำเร็จหรือไม่"
            ),
            "q2_prompt": "มีข้อเสนออะไรเกี่ยวกับประเด็นนี้ไหม?",
            "q2_answer_verbatim": (
                "เสนอให้เพิ่มปุ่มกดซ้ำและส่งอีเมลยืนยันเมื่อการจองเสร็จ"
            ),
            "q2_presence": "PROPOSAL_PRESENT",
            "entry_status": "INTAKE_COMPLETE",
            "certificate": "J2-UIA-046-DEMO",
        },
        "emergency_containment": {"status": "NOT_TRIGGERED"},
        "registration": {
            "query": (
                "อะไรทำให้สถานะการจองไม่ชัด และควรทดลองแนวทางใดก่อน"
            ),
            "decision_to_support": "เลือก reversible test ลด ambiguous bookings",
            "requester": "product team",
            "authorized_users": ["product", "engineering", "support"],
            "forbidden_uses": ["ใช้ fixture แทนหลักฐาน production"],
            "success_rule": "ambiguous-state rate ต่ำกว่าเกณฑ์ที่ freeze",
            "failure_rule": "ไม่ลดหรือเพิ่ม duplicate booking",
            "abstention_rule": "UNRESOLVED หาก lineage ข้ามระบบไม่พอ",
        },
        "proposal_input": {
            "presence": "PROPOSAL_PRESENT",
            "requested_mode": "AUTO",
            "resolved_mode": "HYBRID_BLIND_COMPARE",
            "proposal_verbatim": (
                "เพิ่มปุ่มกดซ้ำและส่งอีเมลยืนยันเมื่อการจองเสร็จ"
            ),
            "anchoring_control": "BLIND_FREEZE_VERIFIED",
            "outcome": "COMPLEMENTARY_COMPONENT",
            "attribution_lineage": "proposal-tape/demo/1",
        },
        "context": {
            "time_index": "synthetic observation window T0-T1",
            "location_or_domain": "mobile web booking",
            "boundary": "confirm click through final booking readout",
            "horizon": "same session plus 24-hour reconciliation",
            "resolution": "one booking attempt per correlation id",
            "constraints": ["no production mutation in fixture"],
            "values": ["clarity", "reversibility", "non-duplication"],
            "rights": ["minimum necessary personal data"],
            "permissions": ["synthetic trace only"],
        },
        "agency": {
            "affected": ["customer", "support"],
            "observers": ["client telemetry", "booking service"],
            "knowledge_holders": ["customer", "support", "engineering"],
            "voice_holders": ["customer representative", "support"],
            "decision_owners": ["product owner"],
            "intervention_owners": ["engineering owner"],
            "resource_holders": ["platform operations"],
            "veto_or_consent_holders": ["privacy reviewer"],
            "accountable_parties": ["service owner"],
            "oversight_parties": ["quality reviewer"],
            "represented_or_absent_parties": ["customers without telemetry"],
            "future_or_indirect_parties": ["operations"],
            "stakeholder_map_status": "CLOSED",
            "power_exposure_voice_gaps": [
                "customers receive impact but cannot inspect backend state"
            ],
        },
        "translation": {
            "raw_user_expression": (
                "กดยืนยันแล้วค้าง ไม่รู้ว่าจองสำเร็จหรือไม่"
            ),
            "selected_domain_projection": "booking state/readout mismatch",
            "canonical_uia_mapping": (
                "retained difference between customer readout and booking state"
            ),
            "topology": "NETWORK",
            "adapter_cards": [
                "state-machine",
                "end-to-end tracing",
                "service recovery",
            ],
            "loss_audit": "PASS",
            "user_facing_issue_statement": (
                "สถานะที่ลูกค้าเห็นไม่แยกผลสำเร็จ กำลังรอ และล้มเหลว"
            ),
        },
        "retained_difference": {
            "baseline": "customer readout becomes final within frozen limit",
            "comparison": "some synthetic attempts remain ambiguous",
            "raw_records": ["client-event", "booking-state", "notification-event"],
            "missing_records": [],
            "lineage": "trace/demo/correlation-id",
        },
        "issue": {
            "type": "UNCERTAINTY",
            "requested_readout": "final booking status per attempt",
            "candidate_state": "ISSUE_ADMITTED",
            "minimal_quotient": "attempt-state-transition-notification",
            "zero_semantics": "no ambiguous attempt under frozen readout",
            "unresolved_semantics": "trace cannot correlate attempt to final state",
        },
        "system_graph": {
            "nodes": [
                "customer",
                "client",
                "booking-api",
                "booking-store",
                "notification",
            ],
            "edges": [
                "confirm",
                "create",
                "persist",
                "return-status",
                "notify",
            ],
            "feedback_loops": ["manual retry"],
            "delays": ["asynchronous confirmation"],
            "invariants": ["one attempt id maps to at most one booking"],
        },
        "causal_analysis": {
            "candidates": [
                "client timeout before final backend state",
                "missing transition between pending and confirmed",
            ],
            "alternatives": ["notification delay without booking-state delay"],
            "controls": ["synthetic success", "synthetic forced timeout"],
            "counterexamples": ["confirmed booking with late email"],
            "intervention_evidence": [],
            "causal_tier": "MECHANISM_CANDIDATE",
        },
        "hypothesis_evidence_challenge": {
            "search_protocol_id": "SEARCH-UIA-046-DEMO",
            "frozen_at": "2026-07-31T00:00:00+07:00",
            "target_context": {
                "country": "Thailand",
                "languages": ["th", "en"],
                "institutions_and_population": (
                    "synthetic Thai mobile-web booking context"
                ),
            },
            "review_mode": "TARGETED_SEARCH",
            "synthesis_method": (
                "QUALITY_DIRECTNESS_CONTEXT_NOT_VOTE_COUNT"
            ),
            "status": "EVIDENCE_CHALLENGE_COMPLETE",
            "hypotheses": [
                {
                    "ledger_id": "EL-H1",
                    "hypothesis_id": "H1",
                    "hypothesis": "client stops observing before final state",
                    "falsifier": "backend lacks a final state for the attempt",
                    "international_track": {
                        "support_queries": ["async client final-state refresh"],
                        "challenge_queries": [
                            "polling fails despite final backend state"
                        ],
                        "sources_searched": [
                            "simulated international engineering index"
                        ],
                        "inclusion_rules": ["state-observation mechanism"],
                        "exclusion_rules": ["unrelated interface latency"],
                        "result_status": "SIMULATED_EVIDENCE_FOUND",
                    },
                    "local_context_track": {
                        "support_queries": [
                            "สถานะธุรกรรมเว็บไทยกำลังประมวลผล"
                        ],
                        "challenge_queries": [
                            "ระบบจองไทยสถานะค้างสาเหตุอื่น"
                        ],
                        "source_classes_searched": [
                            "local_journals",
                            "practice_records",
                        ],
                        "sources_searched": [
                            "simulated Thai source",
                            "simulated local incident record",
                        ],
                        "result_status": "LOCAL_EVIDENCE_FOUND",
                    },
                    "supporting_evidence": ["SIM-CIT-H1"],
                    "challenging_evidence": ["SIM-CIT-H1"],
                    "citation_cards": [
                        {
                            "citation_id": "SIM-CIT-H1",
                            "title": "[SimulatedData] H1 evidence record",
                            "authors_or_issuer": "UIA fixture",
                            "year": 2026,
                            "source_type": "synthetic_fixture",
                            "journal_or_repository": "built-in fixture",
                            "persistent_id_or_official_url": "fixture://H1",
                            "context_country_or_region": "Thailand/synthetic",
                            "claim_supported_or_challenged": "H1 boundary",
                            "direction": "MIXED",
                            "quality": "LOW",
                            "directness": "PARTIAL",
                            "context_fit": "LOW",
                            "metadata_verification": "SIMULATED_ONLY",
                            "scope_verification": "SIMULATED_ONLY",
                            "retrieved_at": "2026-07-31",
                        }
                    ],
                    "global_certainty": "LOW",
                    "local_applicability": "LOW",
                    "evidence_balance": "MIXED",
                    "transfer_status": "ADAPT_WITH_CONDITIONS",
                    "evidence_gaps": ["no field evidence in fixture"],
                    "next_discriminating_test": "shadow refresh by attempt id",
                    "citation_audit": "PASS",
                },
                {
                    "ledger_id": "EL-H2",
                    "hypothesis_id": "H2",
                    "hypothesis": "state fragments cannot correlate end-to-end",
                    "falsifier": "complete lineage exists while ambiguity persists",
                    "international_track": {
                        "support_queries": ["distributed event lineage ambiguity"],
                        "challenge_queries": [
                            "complete tracing does not resolve ambiguous state"
                        ],
                        "sources_searched": [
                            "simulated international engineering index"
                        ],
                        "inclusion_rules": ["end-to-end state lineage"],
                        "exclusion_rules": ["single-node-only failures"],
                        "result_status": "SIMULATED_EVIDENCE_FOUND",
                    },
                    "local_context_track": {
                        "support_queries": ["การติดตามธุรกรรมระบบไทย"],
                        "challenge_queries": [
                            "มี trace ครบแต่สถานะธุรกรรมไทยยังไม่ชัด"
                        ],
                        "source_classes_searched": [
                            "local_journals",
                            "official_or_practice_records",
                        ],
                        "sources_searched": [
                            "simulated Thai source",
                            "simulated local incident record",
                        ],
                        "result_status": "LOCAL_EVIDENCE_FOUND",
                    },
                    "supporting_evidence": ["SIM-CIT-H2"],
                    "challenging_evidence": ["SIM-CIT-H2"],
                    "citation_cards": [
                        {
                            "citation_id": "SIM-CIT-H2",
                            "title": "[SimulatedData] H2 evidence record",
                            "authors_or_issuer": "UIA fixture",
                            "year": 2026,
                            "source_type": "synthetic_fixture",
                            "journal_or_repository": "built-in fixture",
                            "persistent_id_or_official_url": "fixture://H2",
                            "context_country_or_region": "Thailand/synthetic",
                            "claim_supported_or_challenged": "H2 boundary",
                            "direction": "MIXED",
                            "quality": "LOW",
                            "directness": "PARTIAL",
                            "context_fit": "LOW",
                            "metadata_verification": "SIMULATED_ONLY",
                            "scope_verification": "SIMULATED_ONLY",
                            "retrieved_at": "2026-07-31",
                        }
                    ],
                    "global_certainty": "LOW",
                    "local_applicability": "LOW",
                    "evidence_balance": "MIXED",
                    "transfer_status": "ADAPT_WITH_CONDITIONS",
                    "evidence_gaps": ["no field evidence in fixture"],
                    "next_discriminating_test": "one-route event mirror",
                    "citation_audit": "PASS",
                },
                {
                    "ledger_id": "EL-H3",
                    "hypothesis_id": "H3",
                    "hypothesis": "binary UI collapses recoverable states",
                    "falsifier": "ambiguity remains with all states observable",
                    "international_track": {
                        "support_queries": ["finite recovery state user interface"],
                        "challenge_queries": [
                            "explicit recovery states do not reduce ambiguity"
                        ],
                        "sources_searched": [
                            "simulated international design index"
                        ],
                        "inclusion_rules": ["observable recovery states"],
                        "exclusion_rules": ["pure visual redesign"],
                        "result_status": "SIMULATED_EVIDENCE_FOUND",
                    },
                    "local_context_track": {
                        "support_queries": ["สถานะกู้คืนระบบจองภาษาไทย"],
                        "challenge_queries": [
                            "เพิ่มสถานะแล้วผู้ใช้ไทยยังสับสน"
                        ],
                        "source_classes_searched": [
                            "local_journals",
                            "stakeholder_or_practice_records",
                        ],
                        "sources_searched": [
                            "simulated Thai source",
                            "simulated usability record",
                        ],
                        "result_status": "LOCAL_EVIDENCE_FOUND",
                    },
                    "supporting_evidence": ["SIM-CIT-H3"],
                    "challenging_evidence": ["SIM-CIT-H3"],
                    "citation_cards": [
                        {
                            "citation_id": "SIM-CIT-H3",
                            "title": "[SimulatedData] H3 evidence record",
                            "authors_or_issuer": "UIA fixture",
                            "year": 2026,
                            "source_type": "synthetic_fixture",
                            "journal_or_repository": "built-in fixture",
                            "persistent_id_or_official_url": "fixture://H3",
                            "context_country_or_region": "Thailand/synthetic",
                            "claim_supported_or_challenged": "H3 boundary",
                            "direction": "MIXED",
                            "quality": "LOW",
                            "directness": "PARTIAL",
                            "context_fit": "LOW",
                            "metadata_verification": "SIMULATED_ONLY",
                            "scope_verification": "SIMULATED_ONLY",
                            "retrieved_at": "2026-07-31",
                        }
                    ],
                    "global_certainty": "LOW",
                    "local_applicability": "LOW",
                    "evidence_balance": "MIXED",
                    "transfer_status": "ADAPT_WITH_CONDITIONS",
                    "evidence_gaps": ["no field evidence in fixture"],
                    "next_discriminating_test": "shadow recovery-state prototype",
                    "citation_audit": "PASS",
                },
            ],
        },
        "hypothesis_portfolio": {
            "hypothesis_cards": [
                {
                    "hypothesis_id": "H1",
                    "lane": "KNOWN_DIRECT",
                    "claim": "client stops observing before final backend state",
                    "mechanism": "observation terminates before state convergence",
                    "boundary": "confirm click through final booking readout",
                    "conditions": [
                        "backend reaches a final state after client timeout"
                    ],
                    "affected_agencies": ["customer", "support"],
                    "predicted_readout": (
                        "bounded refresh resolves some ambiguous attempts"
                    ),
                    "alternative_explanations": [
                        "backend never reaches a final state"
                    ],
                    "falsifier": "backend lacks a final state for the attempt",
                    "discriminating_information": [
                        "attempt-id state after client timeout"
                    ],
                    "evidence_ledger_ref": "EL-H1",
                    "causal_tier": "MECHANISM_HYPOTHESIS",
                    "legal_relevance": "NONE",
                    "legal_status": "NOT_REQUIRED",
                    "authority_assumptions": [
                        "system owner may authorize synthetic observation"
                    ],
                    "representation_status": {
                        "direct_voice": ["synthetic customer report"],
                        "authorized_proxy": ["support record"],
                        "inferred_only": [],
                        "absent_or_unreached": ["customers without telemetry"],
                    },
                    "legitimacy_status": "INFERRED_NOT_FIELD_CONFIRMED",
                    "proposal_relation": "INDEPENDENT",
                    "uncertainties": ["no production evidence"],
                },
                {
                    "hypothesis_id": "H2",
                    "lane": "CROSS_ADAPTIVE",
                    "claim": (
                        "fragmented event lineage prevents end-to-end "
                        "state reconstruction"
                    ),
                    "mechanism": "state transitions lose correlating lineage",
                    "boundary": "client, booking service and notification",
                    "conditions": [
                        "events exist but lack a shared attempt identifier"
                    ],
                    "affected_agencies": [
                        "customer",
                        "support",
                        "engineering",
                    ],
                    "predicted_readout": (
                        "event mirror reveals the missing transition"
                    ),
                    "alternative_explanations": [
                        "lineage is complete but UI collapses states"
                    ],
                    "falsifier": (
                        "complete lineage exists while ambiguity persists"
                    ),
                    "discriminating_information": [
                        "cross-service transition trace"
                    ],
                    "evidence_ledger_ref": "EL-H2",
                    "causal_tier": "STRUCTURAL_HYPOTHESIS",
                    "legal_relevance": "CONTEXTUAL",
                    "legal_status": "PRELIMINARY",
                    "authority_assumptions": [
                        "data minimization permits synthetic event mirroring"
                    ],
                    "representation_status": {
                        "direct_voice": ["support record"],
                        "authorized_proxy": ["engineering owner"],
                        "inferred_only": ["customer interpretation"],
                        "absent_or_unreached": [
                            "customers without correlated records"
                        ],
                    },
                    "legitimacy_status": "MIXED_GROUNDING",
                    "proposal_relation": "INDEPENDENT",
                    "uncertainties": ["privacy review not field-confirmed"],
                },
                {
                    "hypothesis_id": "H3",
                    "lane": "GENERATIVE_TRANSFORMATIVE",
                    "claim": (
                        "binary customer UI collapses distinct recoverable "
                        "booking states"
                    ),
                    "mechanism": "readout quotient merges actionable states",
                    "boundary": "customer-visible booking state machine",
                    "conditions": [
                        "distinct backend states require distinct safe actions"
                    ],
                    "affected_agencies": ["customer", "support"],
                    "predicted_readout": (
                        "explicit recovery states expose a safe next action"
                    ),
                    "alternative_explanations": [
                        "ambiguity originates solely in missing backend state"
                    ],
                    "falsifier": (
                        "ambiguity remains when all recoverable states "
                        "are observable"
                    ),
                    "discriminating_information": [
                        "usability readout by recovery-state prototype"
                    ],
                    "evidence_ledger_ref": "EL-H3",
                    "causal_tier": "DESIGN_HYPOTHESIS",
                    "legal_relevance": "CONTEXTUAL",
                    "legal_status": "PRELIMINARY",
                    "authority_assumptions": [
                        "product owner may authorize a shadow prototype"
                    ],
                    "representation_status": {
                        "direct_voice": ["synthetic customer report"],
                        "authorized_proxy": ["support representative"],
                        "inferred_only": ["unobserved customer expectations"],
                        "absent_or_unreached": ["customers without telemetry"],
                    },
                    "legitimacy_status": "INFERRED_NOT_FIELD_CONFIRMED",
                    "proposal_relation": "REFRAMES_USER_PROPOSAL",
                    "uncertainties": [
                        "field comprehension and efficacy not confirmed"
                    ],
                },
            ],
            "diversity_test": "PASS",
            "evidence_linkage_test": "PASS",
            "proposal_comparison_status": "COMPLETE",
            "checkpoint_certificate": "HYP-UIA-046-DEMO-001",
            "status": "HYPOTHESIS_PORTFOLIO_READY",
        },
        "candidate_portfolio": {
            "candidate_cards": [
                {
                    "candidate_id": "C-KD",
                    "lane": "KNOWN_DIRECT",
                    "knowledge_basis": "state-aware polling and idempotency",
                    "mechanism_id": "readout_refresh",
                    "hypothesis": "client stops observing before final state",
                    "intervention": "bounded status refresh by attempt id",
                    "expected_readout": "pending becomes a final explicit state",
                    "falsifier": "backend lacks a final state for the attempt",
                    "smallest_reversible_test": "shadow refresh on synthetic attempts",
                    "rights_gate": "PASS",
                    "feasibility": "PASS",
                    "agency_effects": ["customer clarity", "small read load"],
                    "hypothesis_ids": ["H1"],
                    "evidence_ledger_refs": ["EL-H1"],
                },
                {
                    "candidate_id": "C-XA",
                    "lane": "CROSS_ADAPTIVE",
                    "knowledge_basis": "parcel-tracking event lineage",
                    "mechanism_id": "event_lineage",
                    "hypothesis": "state fragments cannot be correlated end-to-end",
                    "intervention": "append-only transition events per attempt",
                    "expected_readout": "missing transition becomes locatable",
                    "falsifier": "complete lineage exists while ambiguity persists",
                    "smallest_reversible_test": "one synthetic route with event mirror",
                    "rights_gate": "PASS",
                    "feasibility": "PASS",
                    "agency_effects": ["engineering observability", "data minimization"],
                    "hypothesis_ids": ["H2"],
                    "evidence_ledger_refs": ["EL-H2"],
                },
                {
                    "candidate_id": "C-GT",
                    "lane": "GENERATIVE_TRANSFORMATIVE",
                    "knowledge_basis": "UIA finite readout design",
                    "mechanism_id": "recovery_state",
                    "hypothesis": "binary success/fail UI collapses recoverable states",
                    "intervention": "finite customer-visible recovery state machine",
                    "expected_readout": "every attempt exposes next safe action",
                    "falsifier": "ambiguity remains with all states observable",
                    "smallest_reversible_test": "prototype state machine in shadow mode",
                    "rights_gate": "PASS",
                    "feasibility": "PASS",
                    "agency_effects": ["customer agency", "support consistency"],
                    "hypothesis_ids": ["H3"],
                    "evidence_ledger_refs": ["EL-H3"],
                },
            ],
            "diversity_test": "PASS",
            "rights_and_feasibility_gate": "PASS",
            "pareto_nondominated": ["C-KD", "C-XA", "C-GT"],
            "recommended_first_test": "C-KD",
            "user_proposal_candidate_id": "C-GT",
            "user_proposal_outcome": "COMPLEMENTARY_COMPONENT",
            "status": "CANDIDATE_SET_COMPLETE",
        },
        "intervention": {
            "selected": "C-KD",
            "predicted_mechanism": "restore observation of final state",
            "expected_readout": "explicit final state within frozen limit",
            "owner": "engineering owner",
            "rights_check": "PASS",
            "stop_rule": "stop if duplicate or excess-load indicator rises",
            "rollback_rule": "disable shadow refresh flag",
        },
        "checker": {
            "independent": True,
            "baseline_readout": "12 simulated ambiguous attempts of 100",
            "post_readout": "2 simulated ambiguous attempts of 100",
            "frozen_target": "at most 3 ambiguous attempts of 100",
            "positive_control": "forced pending becomes confirmed",
            "negative_control": "unknown attempt remains unresolved",
            "deviations": [],
        },
        "final": {
            "issue_status": "ISSUE_ADMITTED",
            "action_status": "INTERVENE",
            "result_status": "PASS_TOLERANCED",
            "candidate_status": "CANDIDATE_SET_COMPLETE",
            "closure_status": "MONITOR",
            "defects": [],
            "claim_scope": "synthetic fixture only",
            "uncertainty": "field efficacy cannot be confirmed",
            "weakest_claim_tier": "finite_diagnostic",
            "reproducibility_or_audit_path": "built-in --demo fixture",
            "correction_path": "revise candidates if field readout differs",
        },
    }


def checkpoint_demo_run() -> dict[str, Any]:
    run = copy.deepcopy(demo_run())
    run["run_control"]["continuation_policy"] = "STOP_AT_HYPOTHESIS"
    run["run_control"]["requested_by"] = "built-in checkpoint demo"
    run["run_control"]["continuation_record"] = (
        "CONT-UIA-046-HYP-DEMO-001"
    )
    for field in {
        "candidate_portfolio",
        "intervention",
        "checker",
        "final",
    }:
        run.pop(field, None)
    return run


def checkpoint_demo_run_alt_domain() -> dict[str, Any]:
    """A second, deliberately non-booking-app checkpoint fixture (industrial
    vibration-sensor false-alarm rate), added 2026-08-01 after a 5-domain
    real-usage simulation found `--print-checkpoint-demo` was the only reference
    shape available and raised ambiguity about which of its content was a
    structural requirement (e.g. Thai-language fields) versus example-locale
    color. Genuinely validated end-to-end, not hand-waved — see
    fixtures/checkpoint_demo_alt_domain.json (the actual source of truth this
    loads) and docs/FIELD_REFERENCE.md's "A note on 'local'" section."""
    path = Path(__file__).resolve().parent / "fixtures" / "checkpoint_demo_alt_domain.json"
    return json.loads(path.read_text(encoding="utf-8"))


def schema_summary() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.invalid/uia/0.4.6/run.schema.json",
        "title": "UIA v0.4.6 finite issue protocol with resumable checkpoint",
        "type": "object",
        "required": [
            "protocol_version",
            "run_control",
            "two_question_intake",
            "emergency_containment",
            "hypothesis_portfolio",
        ],
        "properties": {
            "protocol_version": {"const": VERSION},
            "run_control": {"type": "object"},
            "two_question_intake": {"type": "object"},
            "emergency_containment": {"type": "object"},
            "registration": {"type": "object"},
            "proposal_input": {"type": "object"},
            "context": {"type": "object"},
            "agency": {"type": "object"},
            "translation": {"type": "object"},
            "retained_difference": {"type": "object"},
            "issue": {"type": "object"},
            "system_graph": {"type": "object"},
            "causal_analysis": {"type": "object"},
            "hypothesis_evidence_challenge": {"type": "object"},
            "hypothesis_portfolio": {"type": "object"},
            "candidate_portfolio": {"type": "object"},
            "intervention": {"type": "object"},
            "checker": {"type": "object"},
            "final": {"type": "object"},
        },
        "x-uia-note": (
            "Use this script's validate() for cross-field semantic invariants."
        ),
    }


def self_test() -> dict[str, Any]:
    cases: list[tuple[str, bool, str]] = []

    valid = validate(demo_run())
    cases.append(
        (
            "complete_demo",
            valid["protocol_status"] == "VALID"
            and valid["state"] == "MONITOR"
            and len(valid["phase_trace"]) == len(CANONICAL_PHASES),
            json.dumps(valid, ensure_ascii=False),
        )
    )

    checkpoint = validate(checkpoint_demo_run())
    cases.append(
        (
            "hypothesis_checkpoint_is_valid_and_resumable",
            checkpoint["protocol_status"] == "VALID_CHECKPOINT"
            and checkpoint["state"] == "HYPOTHESIS_PORTFOLIO_READY"
            and checkpoint["continuation_available"] is True
            and checkpoint["next_phase"] == "13_GENERATE_CANDIDATES"
            and len(checkpoint["phase_trace"]) == 13,
            json.dumps(checkpoint, ensure_ascii=False),
        )
    )

    missing_legal_annotation = checkpoint_demo_run()
    del missing_legal_annotation["hypothesis_portfolio"][
        "hypothesis_cards"
    ][0]["legal_status"]
    report = validate(missing_legal_annotation)
    cases.append(
        (
            "hypothesis_missing_legal_annotation_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "HYPOTHESIS_CARD_MISSING:0:legal_status" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    empty_representation = checkpoint_demo_run()
    empty_representation["hypothesis_portfolio"]["hypothesis_cards"][0][
        "representation_status"
    ] = {
        "direct_voice": [],
        "authorized_proxy": [],
        "inferred_only": [],
        "absent_or_unreached": [],
    }
    report = validate(empty_representation)
    cases.append(
        (
            "hypothesis_empty_representation_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "REPRESENTATION_STATUS_EMPTY:H1" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    duplicate_hypothesis_mechanism = checkpoint_demo_run()
    duplicate_hypothesis_mechanism["hypothesis_portfolio"][
        "hypothesis_cards"
    ][1]["mechanism"] = (
        duplicate_hypothesis_mechanism["hypothesis_portfolio"][
            "hypothesis_cards"
        ][0]["mechanism"]
    )
    report = validate(duplicate_hypothesis_mechanism)
    cases.append(
        (
            "duplicate_hypothesis_mechanism_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "HYPOTHESIS_DIVERSITY_FAIL:DUPLICATE_MECHANISM" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    missing_q2 = demo_run()
    del missing_q2["two_question_intake"]["q2_answer_verbatim"]
    missing_q2["two_question_intake"].pop("q2_presence", None)
    missing_q2["two_question_intake"].pop("entry_status", None)
    report = validate(missing_q2)
    cases.append(
        (
            "missing_q2_waits",
            report["protocol_status"] == "WAITING"
            and report["state"] == "WAITING_FOR_PROPOSAL_RESPONSE"
            and report["proposal_presence"] == "UNANSWERED",
            json.dumps(report, ensure_ascii=False),
        )
    )

    alias = demo_run()
    alias["proposal_input"]["requested_mode"] = "HYBRID_BLIND"
    report = validate(alias)
    cases.append(
        (
            "reject_old_alias",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any("INVALID_PROPOSAL_MODE" in e for e in report["errors"]),
            json.dumps(report, ensure_ascii=False),
        )
    )

    emergency_overreach = {
        "protocol_version": VERSION,
        "two_question_intake": {
            "q1_answer_verbatim": "ระบบกำลังผิดปกติ",
        },
        "emergency_containment": {
            "status": "CONTAINMENT_ACTIVE",
            "reason": "continuing service impact",
            "scope": "pause new requests",
            "rights_check": "PASS",
            "owner": "service owner",
            "stop_rule": "stop after stable readout",
            "rollback_rule": "restore route",
            "evidence_preservation": "PRESERVED",
            "review_due_at": "T+15m",
            "causal_verdict": "database is the root cause",
        },
    }
    report = validate(emergency_overreach)
    cases.append(
        (
            "emergency_cannot_decide_cause",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "EMERGENCY_BYPASS_EXCEEDED_SCOPE" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    open_map = demo_run()
    open_map["agency"]["stakeholder_map_status"] = "OPEN"
    open_map["final"]["closure_status"] = "CLOSED"
    report = validate(open_map)
    cases.append(
        (
            "open_stakeholder_map_cannot_close",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "CANNOT_CLOSE_WITH_OPEN_OR_UNRESOLVED_STAKEHOLDER_MAP" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    duplicate_mechanism = demo_run()
    duplicate_mechanism["candidate_portfolio"]["candidate_cards"][1][
        "mechanism_id"
    ] = "readout_refresh"
    report = validate(duplicate_mechanism)
    cases.append(
        (
            "duplicate_mechanism_fails_diversity",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "CANDIDATE_DIVERSITY_FAIL" in e for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    missing_local_track = demo_run()
    del missing_local_track["hypothesis_evidence_challenge"]["hypotheses"][0][
        "local_context_track"
    ]
    report = validate(missing_local_track)
    cases.append(
        (
            "missing_local_track_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "EVIDENCE_TRACK_NOT_OBJECT:0:local_context_track" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    unverified_citation = demo_run()
    unverified_citation["metadata"]["simulation"] = False
    unverified_citation["hypothesis_evidence_challenge"]["hypotheses"][0][
        "citation_cards"
    ][0]["metadata_verification"] = "UNVERIFIED"
    report = validate(unverified_citation)
    cases.append(
        (
            "unverified_citation_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "CITATION_METADATA_NOT_VERIFIED:0:0" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    false_local_absence = demo_run()
    false_local_absence["hypothesis_evidence_challenge"]["hypotheses"][0][
        "local_context_track"
    ]["result_status"] = "NO_LOCAL_EVIDENCE_EXISTS"
    report = validate(false_local_absence)
    cases.append(
        (
            "false_local_absence_claim_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "FORBIDDEN_LOCAL_ABSENCE_CLAIM" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    missing_candidate_evidence_ref = demo_run()
    del missing_candidate_evidence_ref["candidate_portfolio"][
        "candidate_cards"
    ][0]["evidence_ledger_refs"]
    report = validate(missing_candidate_evidence_ref)
    cases.append(
        (
            "candidate_without_evidence_ref_fails",
            report["protocol_status"] == "PROTOCOL_FAIL"
            and any(
                "CANDIDATE_EVIDENCE_REFS_EMPTY:C-KD" in e
                for e in report["errors"]
            ),
            json.dumps(report, ensure_ascii=False),
        )
    )

    failed = [
        {"name": name, "diagnostic": diagnostic}
        for name, passed, diagnostic in cases
        if not passed
    ]
    return {
        "protocol_version": VERSION,
        "test_count": len(cases),
        "passed": len(cases) - len(failed),
        "failed": len(failed),
        "status": "PASS" if not failed else "FAIL",
        "cases": [
            {"name": name, "passed": passed}
            for name, passed, _ in cases
        ],
        "failures": failed,
        "claim_boundary": "FINITE_DIAGNOSTIC_ONLY",
    }


def emit(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate UIA v0.4.6 resumable protocol records."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--demo", action="store_true")
    group.add_argument("--print-demo", action="store_true")
    group.add_argument("--checkpoint-demo", action="store_true")
    group.add_argument("--print-checkpoint-demo", action="store_true")
    group.add_argument(
        "--print-checkpoint-demo-2",
        action="store_true",
        help="a second, non-booking-app checkpoint fixture (industrial vibration-"
        "sensor false-alarm rate) — a starting template for a different domain, "
        "see docs/FIELD_REFERENCE.md",
    )
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--schema", action="store_true")
    group.add_argument("json_file", nargs="?")
    args = parser.parse_args(argv)

    if args.self_test:
        report = self_test()
        emit(report)
        return 0 if report["status"] == "PASS" else 3
    if args.print_demo:
        emit(demo_run())
        return 0
    if args.print_checkpoint_demo:
        emit(checkpoint_demo_run())
        return 0
    if args.print_checkpoint_demo_2:
        emit(checkpoint_demo_run_alt_domain())
        return 0
    if args.demo:
        report = validate(demo_run())
        emit(report)
        return 0 if report["protocol_status"] == "VALID" else 3
    if args.checkpoint_demo:
        report = validate(checkpoint_demo_run())
        emit(report)
        return (
            0
            if report["protocol_status"] == "VALID_CHECKPOINT"
            else 3
        )
    if args.schema:
        emit(schema_summary())
        return 0
    if not args.json_file:
        parser.print_help(sys.stderr)
        return 2

    try:
        with Path(args.json_file).open("r", encoding="utf-8") as handle:
            run = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        emit({"protocol_status": "INPUT_ERROR", "error": str(exc)})
        return 2

    report = validate(run)
    emit(report)
    if report["protocol_status"] == "DRIFT":
        return 4
    if report["protocol_status"] == "PROTOCOL_FAIL":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
