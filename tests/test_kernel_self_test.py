import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KERNEL = REPO_ROOT / "uia_protocol_kernel.py"


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
