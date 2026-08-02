"""Regression coverage for plugins/skillme/scripts/on-stop.sh.

Covers a real bug found by external review (2026-08-02): marketplace.json's
git-subdir install pulls ONLY plugins/skillme/ -- doc_ecosystem_bridge/ lives
at the repo root and is never fetched by a plugin-only install. The hook
used to demand bridge.py unconditionally after a checkpoint, which would
block a plugin-only-install session forever with no way to satisfy the gate.
Fixed by only requiring it when it's actually reachable on disk.

Runs the real bash script via subprocess against isolated tmp_path trees --
no mocking, matches the manual live-verification already done for this fix.
"""
import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ON_STOP = REPO_ROOT / "plugins" / "skillme" / "scripts" / "on-stop.sh"

needs_bash_jq = pytest.mark.skipif(
    not ON_STOP.exists(),
    reason="on-stop.sh not found",
)


def _run_hook(tmp_path, session_id, state, plugin_root, cwd=None, project_dir=None):
    state_dir = tmp_path / "skillme-hook-state"
    state_dir.mkdir(exist_ok=True)
    (state_dir / f"{session_id}.json").write_text(json.dumps(state))

    env = dict(os.environ)
    env["TMPDIR"] = str(tmp_path)
    env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
    env.pop("CLAUDE_PROJECT_DIR", None)
    if project_dir is not None:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)

    result = subprocess.run(
        ["bash", str(ON_STOP)],
        input=json.dumps({"session_id": session_id}),
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd is not None else str(tmp_path),
        env=env,
    )
    return result


@needs_bash_jq
def test_checkpoint_without_doc_eco_but_bridge_unreachable_does_not_block(tmp_path):
    """Plugin-only install: doc_ecosystem_bridge/ genuinely absent -> no block."""
    isolated_root = tmp_path / "isolated-plugin-root" / "plugins" / "skillme"
    (isolated_root / "scripts").mkdir(parents=True)

    state = {
        "skillme_active": True,
        "task_created": True,
        "checkpoint_reached": True,
        "doc_eco_done": False,
    }
    result = _run_hook(
        tmp_path, "sess-isolated", state, plugin_root=isolated_root, cwd=tmp_path
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "", (
        "must not block when doc_ecosystem_bridge/bridge.py is unreachable: "
        + result.stdout
    )


@needs_bash_jq
def test_checkpoint_without_doc_eco_and_bridge_reachable_still_blocks(tmp_path):
    """Full repo checkout: doc_ecosystem_bridge/bridge.py exists -> still blocks (no regression)."""
    repo_root = tmp_path / "full-repo"
    plugin_root = repo_root / "plugins" / "skillme"
    (plugin_root / "scripts").mkdir(parents=True)
    bridge_dir = repo_root / "doc_ecosystem_bridge"
    bridge_dir.mkdir(parents=True)
    (bridge_dir / "bridge.py").write_text("# stub\n")

    state = {
        "skillme_active": True,
        "task_created": True,
        "checkpoint_reached": True,
        "doc_eco_done": False,
    }
    result = _run_hook(
        tmp_path, "sess-full-repo", state, plugin_root=plugin_root, cwd=repo_root
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["decision"] == "block"
    assert "doc_ecosystem_bridge/bridge.py" in payload["reason"]


@needs_bash_jq
def test_checkpoint_with_doc_eco_done_does_not_block(tmp_path):
    isolated_root = tmp_path / "isolated-plugin-root" / "plugins" / "skillme"
    (isolated_root / "scripts").mkdir(parents=True)

    state = {
        "skillme_active": True,
        "task_created": True,
        "checkpoint_reached": True,
        "doc_eco_done": True,
    }
    result = _run_hook(
        tmp_path, "sess-done", state, plugin_root=isolated_root, cwd=tmp_path
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == ""


@needs_bash_jq
def test_missing_task_created_blocks_regardless_of_bridge_reachability(tmp_path):
    isolated_root = tmp_path / "isolated-plugin-root" / "plugins" / "skillme"
    (isolated_root / "scripts").mkdir(parents=True)

    state = {
        "skillme_active": True,
        "task_created": False,
        "checkpoint_reached": False,
        "doc_eco_done": False,
    }
    result = _run_hook(
        tmp_path, "sess-no-task", state, plugin_root=isolated_root, cwd=tmp_path
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["decision"] == "block"
    assert "TaskCreate was never called" in payload["reason"]
