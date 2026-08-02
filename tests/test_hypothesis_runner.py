"""Regression coverage for hypothesis_runner.py (Phase 1b).

Follows this repo's convention: no mocking, real subprocess calls, real
Docker containers actually run. Guarded with skipif when docker isn't
available. Every case here was manually verified against a live run before
being locked in as a test (see CHANGELOG.md v0.4.10 entry) -- including the
world-readable permission bug, which a mocked test would never have caught.
"""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
import skillme_protocol_kernel as k  # noqa: E402

RUNNER = REPO_ROOT / "hypothesis_runner.py"
PAYLOADS_DIR = REPO_ROOT / "fixtures" / "hyp_payloads"

needs_docker = pytest.mark.skipif(
    shutil.which("docker") is None, reason="requires docker"
)


def _checkpoint_with_payload(payload: dict) -> dict:
    run = copy.deepcopy(k.checkpoint_demo_run())
    run["hypothesis_portfolio"]["hypothesis_cards"][0]["verification_payload"] = payload
    assert k.validate(run)["protocol_status"] == "VALID_CHECKPOINT"
    return run


def _passing_payload() -> dict:
    return {
        "payload_ref": "fixtures/hyp_payloads/passing_python",
        "entrypoint": "verify.py",
        "language": "PYTHON3",
        "declared_inputs": [],
        "network_required": False,
        "resource_class": "LIGHT",
        "expected_exit_status": 0,
    }


def _run_runner(checkpoint: dict, hypothesis_id: str, out_dir: Path):
    cp_path = out_dir / "checkpoint.json"
    cp_path.write_text(json.dumps(checkpoint), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(RUNNER), str(cp_path), hypothesis_id, "--out-dir", str(out_dir)],
        capture_output=True, text=True, timeout=120,
    )


@needs_docker
def test_passing_payload_produces_pending_independent_check(tmp_path):
    result = _run_runner(_checkpoint_with_payload(_passing_payload()), "H1", tmp_path)
    assert result.returncode == 0, result.stderr
    record = json.loads((tmp_path / "raw_result_H1.json").read_text())
    assert record["status"] == "PENDING_INDEPENDENT_CHECK"
    assert record["tier"] == "finite_diagnostic"
    assert record["exit_code"] == 0
    assert record["passed"] is True
    assert "hello from sandbox" in record["stdout"]
    # structural guarantee: this record must never claim APPROVED
    assert "APPROVED" != record["status"]
    assert "APPROVED" not in json.dumps(record).replace(
        record["claim_boundary"], ""
    )


@needs_docker
def test_failing_payload_records_failure_not_error(tmp_path):
    payload = {
        "payload_ref": "fixtures/hyp_payloads/failing_python",
        "entrypoint": "verify.py",
        "language": "PYTHON3",
        "declared_inputs": [],
        "network_required": False,
        "resource_class": "LIGHT",
        "expected_exit_status": 0,
    }
    result = _run_runner(_checkpoint_with_payload(payload), "H1", tmp_path)
    assert result.returncode == 0, result.stderr  # the runner itself succeeds
    record = json.loads((tmp_path / "raw_result_H1.json").read_text())
    assert record["exit_code"] == 1
    assert record["passed"] is False
    assert "this hypothesis fails" in record["stdout"]


def test_missing_verification_payload_refuses_cleanly(tmp_path):
    run = copy.deepcopy(k.checkpoint_demo_run())
    assert "verification_payload" not in run["hypothesis_portfolio"]["hypothesis_cards"][0]
    result = _run_runner(run, "H1", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "no verification_payload declared" in result.stderr


def test_invalid_checkpoint_refuses_before_docker(tmp_path):
    run = copy.deepcopy(k.checkpoint_demo_run())
    del run["hypothesis_portfolio"]["hypothesis_cards"][0]["falsifier"]  # break structure
    result = _run_runner(run, "H1", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "VALID_CHECKPOINT" in result.stderr


def test_unknown_hypothesis_id_refuses(tmp_path):
    result = _run_runner(_checkpoint_with_payload(_passing_payload()), "NOT_A_REAL_ID", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "not found" in result.stderr


def test_unsupported_language_refuses_cleanly(tmp_path):
    payload = _passing_payload()
    payload["language"] = "COQC"
    result = _run_runner(_checkpoint_with_payload(payload), "H1", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "no image wired" in result.stderr


def test_payload_ref_path_escape_refused(tmp_path):
    payload = _passing_payload()
    payload["payload_ref"] = "../../../etc"
    result = _run_runner(_checkpoint_with_payload(payload), "H1", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "outside the repo" in result.stderr


def test_missing_declared_input_refused(tmp_path):
    payload = _passing_payload()
    payload["declared_inputs"] = ["does_not_exist.txt"]
    result = _run_runner(_checkpoint_with_payload(payload), "H1", tmp_path)
    assert result.returncode != 0
    assert "REFUSED" in result.stderr
    assert "declares an input it doesn't ship" in result.stderr


def test_non_world_readable_payload_refuses_with_clear_message(tmp_path):
    # Real bug found by actually running this against a mode-660 fixture file
    # during Phase 1b development: the sandbox UID (65534) can't read it, and
    # without this preflight check that surfaces as a cryptic docker stderr
    # ("Permission denied") in the raw_result instead of a clean refusal.
    # payload_ref must resolve inside REPO_ROOT (the runner refuses escapes),
    # so this scratch dir has to live under the repo, not pytest's tmp_path.
    scratch_payload = PAYLOADS_DIR / f"_test_scratch_{tmp_path.name}"
    scratch_payload.mkdir(parents=True, exist_ok=True)
    try:
        verify = scratch_payload / "verify.py"
        verify.write_text("print('should not run')\n", encoding="utf-8")
        verify.chmod(0o600)  # not world-readable
        payload = {
            "payload_ref": str(scratch_payload.relative_to(REPO_ROOT)),
            "entrypoint": "verify.py",
            "language": "PYTHON3",
            "declared_inputs": [],
            "network_required": False,
            "resource_class": "LIGHT",
            "expected_exit_status": 0,
        }
        result = _run_runner(_checkpoint_with_payload(payload), "H1", tmp_path)
        assert result.returncode != 0
        assert "REFUSED" in result.stderr
        assert "world-readable" in result.stderr
    finally:
        shutil.rmtree(scratch_payload, ignore_errors=True)


def test_concurrency_lock_refuses_second_invocation(tmp_path):
    import fcntl

    lock_path = Path("/tmp/skillme_hypothesis_runner.lock")
    lock_path.touch(exist_ok=True)
    held = open(lock_path, "w")
    try:
        fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = _run_runner(_checkpoint_with_payload(_passing_payload()), "H1", tmp_path)
        assert result.returncode != 0
        assert "REFUSED" in result.stderr
        assert "already running" in result.stderr
    finally:
        fcntl.flock(held, fcntl.LOCK_UN)
        held.close()
