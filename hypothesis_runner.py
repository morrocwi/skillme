#!/usr/bin/env python3
"""Phase 1b: execute a hypothesis card's declared verification_payload in a
hardened Docker container and record a bounded, finite_diagnostic-tier raw
result.

Scope, stated honestly (per the ultracode team-meeting adversarial review that
named this exact scope split -- see CHANGELOG.md / SKILLME.md §14):

- This script is the MAKER side only. It never writes a "status: APPROVED"
  field anywhere -- there is no code path in this file that does that, on
  purpose. Its output is a raw_result record tagged PENDING_INDEPENDENT_CHECK,
  finite_diagnostic tier: a bounded, this-environment, this-input observation.
  It proves nothing about whether the hypothesis is true.
- It does NOT implement principal-level (Phase 2) maker/checker separation --
  the OS-subuser substrate this workspace has scripted
  (cpg/tools/agent_office/setup_agent_users.sh) has never actually been
  provisioned on this machine (verified live: no anse-* OS users exist, and
  provisioning requires an interactive sudo run this script cannot perform).
  So this script uses Docker UID/mount separation instead, scoped to this
  repo only: the hypothesis container gets NO writable bind mount anywhere
  (no docker.sock, no host network by default, --read-only root, only an
  in-memory --tmpfs with an enforced size cap for scratch space) and runs as
  a fixed non-root UID. The *raw_result* file is written by this script's own
  process AFTER the container exits, from the container's captured
  stdout/stderr/exit code only -- the container itself cannot touch the host
  filesystem at all, let alone the result file. This closes the *filesystem*
  self-certification loophole the review named; it does not yet close the
  *actor* loophole (the same session that ran this script could also be the
  one that later marks something "checked") -- that still needs Phase 2's
  principal_id separation, not built here.
- COQC payload language is declared in the schema (skillme_protocol_kernel.py
  VERIFICATION_LANGUAGES) but this runner has no Coq image wired -- it
  refuses cleanly rather than silently no-op or fake success.
- payload_ref is resolved as a LOCAL DIRECTORY PATH only. No remote fetch, no
  signature/hash verification of payload_ref's contents against anything --
  that is a real, named supply-chain gap (the adversarial security review's
  finding #9), not fixed by this script.
- --storage-opt size=... is NOT used for the disk-quota flag: verified live on
  this host (overlay2 storage driver) that it silently no-ops (wrote 50MB
  through a --storage-opt size=10m container with no error). --tmpfs's size=
  option was verified live to actually enforce (dd hit "No space left on
  device" at the declared limit) -- that is what this script uses instead.

Usage:
    python3 hypothesis_runner.py <checkpoint.json> <hypothesis_id> --out-dir <dir>
"""
from __future__ import annotations

import argparse
import fcntl
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
LOCK_PATH = Path("/tmp/skillme_hypothesis_runner.lock")

# Not a supply-chain-vetted registry -- these are the images this runner
# has actually been exercised against. Pinned by tag, not digest (a real,
# named gap: no provenance/signature verification, see module docstring).
LANGUAGE_IMAGES = {
    "PYTHON3": "python:3.12-slim",
    "BASH": "bash:5",
}

RESOURCE_LIMITS = {
    "LIGHT": {"memory": "256m", "pids": "32", "tmpfs_mb": 16},
    "HEAVY": {"memory": "2g", "pids": "128", "tmpfs_mb": 128},
}

TIMEOUT_SECONDS = 300


def load_kernel():
    sys.path.insert(0, str(REPO_ROOT))
    import skillme_protocol_kernel  # type: ignore

    return skillme_protocol_kernel


def validate_checkpoint_or_refuse(checkpoint_path: Path) -> dict:
    try:
        run = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {checkpoint_path} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {checkpoint_path} is not valid JSON: {e}")

    kernel = load_kernel()
    result = kernel.validate(run)
    if result.get("protocol_status") != "VALID_CHECKPOINT":
        raise SystemExit(
            "REFUSED: checkpoint is not a VALID_CHECKPOINT hypothesis portfolio "
            f"(protocol_status={result.get('protocol_status')!r}, "
            f"errors={result.get('errors')}). Fix the checkpoint before running "
            "the runner -- proceeding would execute code from unvalidated data."
        )
    return run


def find_hypothesis_card(run: dict, hypothesis_id: str) -> dict:
    cards = (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards") or []
    for card in cards:
        if isinstance(card, dict) and card.get("hypothesis_id") == hypothesis_id:
            return card
    raise SystemExit(
        f"REFUSED: hypothesis_id {hypothesis_id!r} not found in this checkpoint's "
        "hypothesis_portfolio.hypothesis_cards"
    )


def resolve_payload_or_refuse(card: dict, hypothesis_id: str) -> dict:
    payload = card.get("verification_payload")
    if not isinstance(payload, dict):
        raise SystemExit(
            f"REFUSED: hypothesis {hypothesis_id!r} has no verification_payload "
            "declared -- nothing for this runner to execute. Most hypotheses in "
            "this protocol are qualitative causal claims with no executable "
            "payload at all; that is expected and not an error in the "
            "checkpoint, just not something this runner applies to."
        )
    language = payload.get("language")
    if language not in LANGUAGE_IMAGES:
        supported = ", ".join(sorted(LANGUAGE_IMAGES))
        raise SystemExit(
            f"REFUSED: language {language!r} is declared in the schema but this "
            f"runner has no image wired for it yet (supported: {supported}). "
            "Refusing cleanly rather than silently no-op or fake a result."
        )
    payload_dir = (REPO_ROOT / str(payload.get("payload_ref"))).resolve()
    if REPO_ROOT not in payload_dir.parents and payload_dir != REPO_ROOT:
        raise SystemExit(
            f"REFUSED: payload_ref {payload.get('payload_ref')!r} resolves "
            f"outside the repo ({payload_dir}) -- refusing to mount an "
            "arbitrary host path into the sandbox."
        )
    if not payload_dir.is_dir():
        raise SystemExit(
            f"REFUSED: payload_ref directory not found: {payload_dir}"
        )
    entrypoint = payload_dir / str(payload.get("entrypoint"))
    if not entrypoint.is_file():
        raise SystemExit(
            f"REFUSED: entrypoint not found inside payload_ref: {entrypoint}"
        )
    for declared in payload.get("declared_inputs") or []:
        if not (payload_dir / str(declared)).exists():
            raise SystemExit(
                f"REFUSED: declared_inputs entry {declared!r} not found under "
                f"{payload_dir} -- payload declares an input it doesn't ship."
            )
    check_payload_world_readable_or_refuse(payload_dir)
    return payload


def check_payload_world_readable_or_refuse(payload_dir: Path) -> None:
    # The sandbox runs as a fixed non-root UID (65534, "nobody") that has no
    # group membership matching the host user who owns payload_dir -- caught
    # live during Phase 1b testing: a real mode-660 fixture file produced
    # "Permission denied" inside the container with a cryptic docker stderr,
    # not a clean refusal. Preflight-check instead of letting that leak
    # through as the "raw result".
    bad = []
    for path in [payload_dir, *payload_dir.rglob("*")]:
        mode = path.stat().st_mode
        needs_exec = path.is_dir()
        other_ok = (mode & 0o004) and (not needs_exec or (mode & 0o001))
        if not other_ok:
            bad.append(path)
    if bad:
        listed = "\n  ".join(str(p) for p in bad[:10])
        more = f"\n  ... and {len(bad) - 10} more" if len(bad) > 10 else ""
        raise SystemExit(
            "REFUSED: payload_ref is not world-readable, so the sandbox UID "
            "(65534, non-root, no shared group with the host owner) cannot "
            f"read it. Fix with chmod o+rX on:\n  {listed}{more}"
        )


def acquire_global_lock():
    # Global concurrency cap (adversarial security review finding #2: per-
    # container limits alone don't prevent fleet-scale OOM if N sandboxes run
    # simultaneously). One hypothesis_runner.py invocation at a time on this
    # host -- refuses immediately rather than silently queueing.
    LOCK_PATH.touch(exist_ok=True)
    lock_file = open(LOCK_PATH, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit(
            "REFUSED: another hypothesis_runner.py is already running on this "
            f"host ({LOCK_PATH} is locked) -- global concurrency cap is 1. "
            "Wait for it to finish or investigate a stuck/orphaned run."
        )
    return lock_file


def run_in_container(payload_dir: Path, payload: dict) -> dict:
    language = payload["language"]
    image = LANGUAGE_IMAGES[language]
    resource_class = payload.get("resource_class", "LIGHT")
    limits = RESOURCE_LIMITS.get(resource_class, RESOURCE_LIMITS["LIGHT"])
    entrypoint = payload["entrypoint"]
    network_required = bool(payload.get("network_required"))

    interpreter = {"PYTHON3": "python3", "BASH": "bash"}[language]

    cmd = [
        "docker", "run", "--rm",
        "--network", "none" if not network_required else "bridge",
        "--read-only",
        "--cap-drop", "ALL",
        "--pids-limit", limits["pids"],
        "--memory", limits["memory"],
        "--tmpfs", f"/tmp:size={limits['tmpfs_mb']}m,rw,noexec",
        "--user", "65534:65534",
        "-v", f"{payload_dir}:/payload:ro",
        "--workdir", "/payload",
        image,
        interpreter, f"/payload/{entrypoint}",
    ]

    started_at = time.time()
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
        timed_out = False
        exit_code = proc.returncode
        stdout, stderr = proc.stdout, proc.stderr
    except FileNotFoundError:
        raise SystemExit(
            "REFUSED: 'docker' is not installed or not on PATH -- "
            "hypothesis_runner.py requires Docker to sandbox execution."
        )
    except subprocess.TimeoutExpired as e:
        timed_out = True
        exit_code = None
        stdout = e.stdout or ""
        stderr = (e.stderr or "") + f"\n[hypothesis_runner] TIMEOUT after {TIMEOUT_SECONDS}s"
    duration_s = round(time.time() - started_at, 3)

    # Bound raw output -- an adversarial payload could try to exhaust the
    # host by printing gigabytes to stdout even inside the resource limits.
    max_chars = 200_000
    truncated = len(stdout) > max_chars or len(stderr) > max_chars
    stdout = stdout[:max_chars]
    stderr = stderr[:max_chars]

    return {
        "exit_code": exit_code,
        "expected_exit_status": payload.get("expected_exit_status"),
        "passed": (
            exit_code is not None and exit_code == payload.get("expected_exit_status")
        ),
        "timed_out": timed_out,
        "duration_s": duration_s,
        "stdout": stdout,
        "stderr": stderr,
        "output_truncated": truncated,
        "image": image,
        "language": language,
        "resource_class": resource_class,
        "network_required": network_required,
        "docker_command": cmd,
    }


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("checkpoint", type=Path, help="SkillMe checkpoint JSON file")
    p.add_argument("hypothesis_id", help="hypothesis_id of the card to verify")
    p.add_argument("--out-dir", type=Path, required=True, help="where to write raw_result JSON")
    p.add_argument(
        "--maker-principal-id",
        required=True,
        help=(
            "identifier for whoever/whatever is running this (Phase 2, MC-02): "
            "a session id, agent id, or human identifier. Stamped into the "
            "raw_result so hypothesis_checker.py can structurally refuse a "
            "checker_principal_id that matches this one. Declared, not "
            "cryptographically verified -- see module docstring."
        ),
    )
    args = p.parse_args()

    run = validate_checkpoint_or_refuse(args.checkpoint)
    card = find_hypothesis_card(run, args.hypothesis_id)
    payload = resolve_payload_or_refuse(card, args.hypothesis_id)
    payload_dir = (REPO_ROOT / str(payload["payload_ref"])).resolve()

    lock_file = acquire_global_lock()
    try:
        execution = run_in_container(payload_dir, payload)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"raw_result_{args.hypothesis_id}.json"
    # Structural guarantee (independent review finding, extended to
    # maker_principal_id in Phase 2 since hypothesis_checker.py's MC-02
    # enforcement now depends on it): status/tier/claim_boundary/
    # maker_principal_id are placed AFTER **execution in this dict literal,
    # so they always win Python's last-key-wins merge semantics even if a
    # future edit adds a same-named key to run_in_container()'s return
    # value. Asserted explicitly too, so that scenario fails loudly instead
    # of silently overriding a guarantee this design rests on.
    _protected_keys = {"status", "tier", "claim_boundary", "maker_principal_id"}
    assert not _protected_keys & set(execution), (
        f"run_in_container() must never return any of {sorted(_protected_keys)} "
        "-- those are hardcoded below and must not be payload-influenceable"
    )
    record = {
        "schema": "skillme_verification_raw_result_v1",
        "hypothesis_id": args.hypothesis_id,
        "checkpoint_certificate": (
            (run.get("hypothesis_portfolio") or {}).get("checkpoint_certificate")
        ),
        **execution,
        "maker_principal_id": args.maker_principal_id,
        "tier": "finite_diagnostic",
        "status": "PENDING_INDEPENDENT_CHECK",
        "claim_boundary": (
            "This record proves only that the declared payload ran, once, in "
            "this sandboxed environment, and produced this exit code/output. "
            "It does NOT prove the hypothesis is true, does NOT constitute an "
            "independent check (MC-01/MC-02: the same process that ran this "
            "also authored this record), and is NOT self-promotable to "
            "APPROVED by anything in this codebase."
        ),
    }
    out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"wrote {out_path} (status={record['status']}, exit_code={execution['exit_code']})")


if __name__ == "__main__":
    main()
