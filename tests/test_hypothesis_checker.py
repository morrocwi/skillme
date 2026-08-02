"""Regression coverage for hypothesis_checker.py (Phase 2).

Follows this repo's convention: no mocking, real subprocess calls. Every
case here was manually verified against a live run before being locked in
as a test.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
import skillme_protocol_kernel as k  # noqa: E402

CHECKER = REPO_ROOT / "hypothesis_checker.py"


def _checkpoint_with_verification_payload() -> dict:
    run = copy.deepcopy(k.checkpoint_demo_run())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = {
        "payload_ref": "fixtures/hyp_payloads/passing_python",
        "entrypoint": "verify.py",
        "language": "PYTHON3",
        "declared_inputs": [],
        "network_required": False,
        "resource_class": "LIGHT",
        "expected_exit_status": 0,
    }
    assert k.validate(run)["protocol_status"] == "VALID_CHECKPOINT"
    return run


def _raw_result(tmp_path: Path, maker_principal_id="maker-session-1", exit_code=0) -> Path:
    record = {
        "schema": "skillme_verification_raw_result_v1",
        "hypothesis_id": "H1",
        "checkpoint_certificate": "TEST-CERT",
        "exit_code": exit_code,
        "expected_exit_status": 0,
        "passed": exit_code == 0,
        "timed_out": False,
        "duration_s": 1.0,
        "stdout": "test output",
        "stderr": "",
        "output_truncated": False,
        "image": "python:3.12-slim",
        "language": "PYTHON3",
        "resource_class": "LIGHT",
        "network_required": False,
        "docker_command": ["docker", "run"],
        "maker_principal_id": maker_principal_id,
        "tier": "finite_diagnostic",
        "status": "PENDING_INDEPENDENT_CHECK",
        "claim_boundary": "test claim boundary",
    }
    path = tmp_path / "raw_result_H1.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


def _run_checker(checkpoint_path: Path, raw_result_path: Path, **kwargs):
    args = {
        "checker_principal_id": "checker-session-2",
        "checker_type": "AI",
        "tier": "L0",
        "verdict": "APPROVED",
        "rationale": "test rationale",
    }
    args.update(kwargs)
    cmd = [
        sys.executable, str(CHECKER), str(checkpoint_path), "H1", str(raw_result_path),
        "--checker-principal-id", args["checker_principal_id"],
        "--checker-type", args["checker_type"],
        "--tier", args["tier"],
        "--verdict", args["verdict"],
        "--rationale", args["rationale"],
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30)


def test_valid_check_writes_checker_result(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path)

    result = _run_checker(checkpoint_path, raw_result_path)
    assert result.returncode == 0, result.stderr

    updated = json.loads(checkpoint_path.read_text())
    checker_result = updated["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"]
    assert checker_result["maker_principal_id"] == "maker-session-1"
    assert checker_result["checker_principal_id"] == "checker-session-2"
    assert checker_result["verdict"] == "APPROVED"
    assert checker_result["mechanically_passed"] is True
    # the resulting checkpoint must still validate
    assert k.validate(updated)["protocol_status"] == "VALID_CHECKPOINT"


def test_same_principal_as_maker_refused(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, maker_principal_id="same-session")

    result = _run_checker(
        checkpoint_path, raw_result_path, checker_principal_id="same-session"
    )
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "MC-02" in result.stderr
    # checkpoint must be untouched
    untouched = json.loads(checkpoint_path.read_text())
    assert "checker_result" not in untouched["hypothesis_portfolio"]["hypothesis_cards"][0]


def test_same_principal_with_trailing_whitespace_refused(tmp_path):
    # Real bug found by independent review of this PR: the original MC-02
    # comparison was a raw string equality, so "same-session" vs
    # "same-session " (trailing space) silently passed as different
    # principals. Now normalized (strip + casefold) before comparing.
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, maker_principal_id="same-session")

    result = _run_checker(
        checkpoint_path, raw_result_path, checker_principal_id="same-session "
    )
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "MC-02" in result.stderr
    untouched = json.loads(checkpoint_path.read_text())
    assert "checker_result" not in untouched["hypothesis_portfolio"]["hypothesis_cards"][0]


def test_same_principal_with_different_case_refused(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, maker_principal_id="Same-Session")

    result = _run_checker(
        checkpoint_path, raw_result_path, checker_principal_id="same-session"
    )
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "MC-02" in result.stderr
    untouched = json.loads(checkpoint_path.read_text())
    assert "checker_result" not in untouched["hypothesis_portfolio"]["hypothesis_cards"][0]


def test_genuinely_different_principals_still_accepted(tmp_path):
    # Guard against over-normalizing into false refusals.
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, maker_principal_id="maker-session-1")

    result = _run_checker(
        checkpoint_path, raw_result_path, checker_principal_id="checker-session-2"
    )
    assert result.returncode == 0, result.stderr


def test_l3_with_ai_checker_refused(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path)

    result = _run_checker(checkpoint_path, raw_result_path, tier="L3", checker_type="AI")
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "HUMAN" in result.stderr


@pytest.mark.parametrize("tier", ["L3", "L4", "L5"])
def test_l3_plus_with_human_checker_accepted(tmp_path, tier):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path)

    result = _run_checker(checkpoint_path, raw_result_path, tier=tier, checker_type="HUMAN")
    assert result.returncode == 0, result.stderr
    updated = json.loads(checkpoint_path.read_text())
    assert (
        updated["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"]["tier"]
        == tier
    )


def test_wrong_hypothesis_id_in_raw_result_refused(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path)
    raw_result_path.write_text(
        raw_result_path.read_text().replace('"hypothesis_id": "H1"', '"hypothesis_id": "H2"')
    )

    result = _run_checker(checkpoint_path, raw_result_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "wrong file" in result.stderr


def test_raw_result_missing_maker_principal_id_refused(tmp_path):
    # Simulates a raw_result from a pre-Phase-2 hypothesis_runner.py.
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path)
    record = json.loads(raw_result_path.read_text())
    del record["maker_principal_id"]
    raw_result_path.write_text(json.dumps(record))

    result = _run_checker(checkpoint_path, raw_result_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "no maker_principal_id" in result.stderr


def test_mechanically_failed_but_approved_warns(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, exit_code=1)  # mechanically failed

    result = _run_checker(checkpoint_path, raw_result_path, verdict="APPROVED")
    assert result.returncode == 0, result.stderr
    assert "WARNING" in result.stderr
    updated = json.loads(checkpoint_path.read_text())
    checker_result = updated["hypothesis_portfolio"]["hypothesis_cards"][0]["checker_result"]
    assert checker_result["mechanically_passed"] is False
    assert checker_result["verdict"] == "APPROVED"


def test_rejected_verdict_does_not_warn(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint_path.write_text(json.dumps(_checkpoint_with_verification_payload()))
    raw_result_path = _raw_result(tmp_path, exit_code=1)

    result = _run_checker(checkpoint_path, raw_result_path, verdict="REJECTED")
    assert result.returncode == 0, result.stderr
    assert "WARNING" not in result.stderr


def test_out_flag_writes_separate_file_leaves_input_untouched(tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    original = _checkpoint_with_verification_payload()
    checkpoint_path.write_text(json.dumps(original))
    raw_result_path = _raw_result(tmp_path)
    out_path = tmp_path / "checked_checkpoint.json"

    cmd = [
        sys.executable, str(CHECKER), str(checkpoint_path), "H1", str(raw_result_path),
        "--checker-principal-id", "checker-session-2", "--checker-type", "AI",
        "--tier", "L0", "--verdict", "APPROVED", "--rationale", "test",
        "--out", str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert "checker_result" not in json.loads(checkpoint_path.read_text())[
        "hypothesis_portfolio"
    ]["hypothesis_cards"][0]
    assert "checker_result" in json.loads(out_path.read_text())[
        "hypothesis_portfolio"
    ]["hypothesis_cards"][0]
