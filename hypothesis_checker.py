#!/usr/bin/env python3
"""Phase 2: the CHECKER side of MC-01/MC-02 -- the counterpart to
hypothesis_runner.py's maker side.

hypothesis_runner.py never writes "status: APPROVED" -- by construction,
there is no code path in it that does. This script is where that verdict
gets written, and it is a SEPARATE program, invoked separately, on purpose:
the same script cannot both generate a raw_result and check it. There is no
"--i-am-also-the-checker" flag.

Scope, stated honestly (same discipline as hypothesis_runner.py):

- `--checker-principal-id` is REQUIRED and is refused if it matches the
  raw_result's own `maker_principal_id` (MC-02, structural). This is a
  DECLARATION check, not identity verification -- this repo has no identity
  infrastructure wired to it (the workspace's anse-principals-and-db system
  is a separate, unconnected repo; see hypothesis_runner.py's own module
  docstring for the same caveat about the OS-subuser substrate). Anyone can
  declare any principal_id string. What this script guarantees is only that
  the DECLARED maker and DECLARED checker differ -- a structural floor, not
  a cryptographic one.
- `--tier` (L0-L5, MIMCG, cpg/AGENTS.md step 6.5, ratified 2026-08-02) is
  REQUIRED. L3+ REQUIRES `--checker-type HUMAN` -- refused otherwise, by the
  kernel's own validate() when this script writes the result back into the
  checkpoint, not just by this script's own logic (defense in depth: both
  layers enforce it independently).
- This script re-runs the mechanical check itself where it can (re-reads
  the raw_result and re-verifies exit_code == expected_exit_status) rather
  than trusting the raw_result's own "passed" field -- per this workspace's
  standing MC-04 discipline ("don't trust a log you could have fabricated").
  It does NOT re-execute the payload in a fresh container -- that would
  require re-resolving payload_ref and re-invoking hypothesis_runner.py,
  which is a legitimate stronger check a human reviewer can still choose to
  do manually; this script only re-derives from the raw_result's own
  recorded fields.
- Writing the checker_result back into the checkpoint JSON (so the kernel's
  validate() sees and structurally enforces it) is this script's actual
  job -- it edits the hypothesis card in place and re-validates the whole
  checkpoint before writing, refusing to write a result that would make the
  checkpoint invalid.

Usage:
    python3 hypothesis_checker.py <checkpoint.json> <hypothesis_id> \
        <raw_result.json> --checker-principal-id <id> --checker-type AI|HUMAN \
        --tier L0..L5 --verdict APPROVED|REJECTED --rationale "..."
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def load_kernel():
    sys.path.insert(0, str(REPO_ROOT))
    import skillme_protocol_kernel  # type: ignore

    return skillme_protocol_kernel


def load_checkpoint_or_refuse(checkpoint_path: Path) -> dict:
    try:
        return json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {checkpoint_path} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {checkpoint_path} is not valid JSON: {e}")


def find_hypothesis_card(run: dict, hypothesis_id: str) -> dict:
    cards = (run.get("hypothesis_portfolio") or {}).get("hypothesis_cards") or []
    for card in cards:
        if isinstance(card, dict) and card.get("hypothesis_id") == hypothesis_id:
            return card
    raise SystemExit(
        f"REFUSED: hypothesis_id {hypothesis_id!r} not found in this checkpoint's "
        "hypothesis_portfolio.hypothesis_cards"
    )


def load_raw_result_or_refuse(raw_result_path: Path, hypothesis_id: str) -> dict:
    try:
        record = json.loads(raw_result_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {raw_result_path} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {raw_result_path} is not valid JSON: {e}")
    if record.get("schema") != "skillme_verification_raw_result_v1":
        raise SystemExit(
            f"REFUSED: {raw_result_path} is not a "
            "skillme_verification_raw_result_v1 record (unexpected 'schema' "
            f"field: {record.get('schema')!r})"
        )
    if record.get("hypothesis_id") != hypothesis_id:
        raise SystemExit(
            f"REFUSED: raw_result is for hypothesis_id {record.get('hypothesis_id')!r}, "
            f"not {hypothesis_id!r} -- wrong file for this checker invocation"
        )
    if not record.get("maker_principal_id"):
        raise SystemExit(
            "REFUSED: raw_result has no maker_principal_id -- was this "
            "produced by an old hypothesis_runner.py before Phase 2? "
            "Re-run the maker step first."
        )
    return record


def re_derive_mechanical_result(raw_result: dict) -> bool:
    # MC-04: don't trust a log you could have fabricated -- re-derive the
    # pass/fail from the raw_result's own recorded exit_code/expected fields
    # rather than trusting its own "passed" boolean at face value.
    exit_code = raw_result.get("exit_code")
    expected = raw_result.get("expected_exit_status")
    return exit_code is not None and exit_code == expected


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("checkpoint", type=Path, help="SkillMe checkpoint JSON file")
    p.add_argument("hypothesis_id", help="hypothesis_id of the card to check")
    p.add_argument("raw_result", type=Path, help="raw_result_<id>.json from hypothesis_runner.py")
    p.add_argument(
        "--checker-principal-id", required=True,
        help="identifier for the checker (MC-02: must differ from the raw_result's maker_principal_id)",
    )
    p.add_argument("--checker-type", required=True, choices=["AI", "HUMAN"])
    p.add_argument("--tier", required=True, choices=["L0", "L1", "L2", "L3", "L4", "L5"])
    p.add_argument("--verdict", required=True, choices=["APPROVED", "REJECTED"])
    p.add_argument("--rationale", required=True, help="why this verdict -- required, non-blank")
    p.add_argument(
        "--out", type=Path, default=None,
        help="write the updated checkpoint here instead of overwriting the input (default: overwrite in place)",
    )
    args = p.parse_args()

    kernel = load_kernel()
    run = load_checkpoint_or_refuse(args.checkpoint)
    card = find_hypothesis_card(run, args.hypothesis_id)
    raw_result = load_raw_result_or_refuse(args.raw_result, args.hypothesis_id)

    if kernel.normalize_principal_id(
        args.checker_principal_id
    ) == kernel.normalize_principal_id(raw_result["maker_principal_id"]):
        raise SystemExit(
            "REFUSED: --checker-principal-id matches the raw_result's own "
            f"maker_principal_id ({raw_result['maker_principal_id']!r}) -- "
            "MC-02: the same principal cannot be both maker and checker. "
            "This script structurally refuses it; the kernel's validate() "
            "would refuse it again even if this check were somehow bypassed."
        )

    if args.tier in {"L3", "L4", "L5"} and args.checker_type == "AI":
        raise SystemExit(
            f"REFUSED: tier {args.tier} requires --checker-type HUMAN "
            "(MIMCG, cpg/AGENTS.md step 6.5, ratified 2026-08-02) -- an AI "
            "checker is only eligible for L0-L2."
        )

    mechanically_passed = re_derive_mechanical_result(raw_result)
    if args.verdict == "APPROVED" and not mechanically_passed:
        print(
            "WARNING: approving a hypothesis whose raw_result did NOT pass "
            f"mechanically (exit_code={raw_result.get('exit_code')!r}, "
            f"expected={raw_result.get('expected_exit_status')!r}). This is "
            "allowed -- a human checker may approve for reasons the exit "
            "code doesn't capture -- but it is not the common case. "
            "Rationale should explain why.",
            file=sys.stderr,
        )

    card["checker_result"] = {
        "maker_principal_id": raw_result["maker_principal_id"],
        "checker_principal_id": args.checker_principal_id,
        "checker_type": args.checker_type,
        "tier": args.tier,
        "verdict": args.verdict,
        "rationale": args.rationale,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "raw_result_ref": str(args.raw_result),
        "mechanically_passed": mechanically_passed,
    }

    result = kernel.validate(run)
    if result.get("protocol_status") not in ("VALID", "VALID_CHECKPOINT"):
        # writing checker_result must never itself invalidate the checkpoint
        raise SystemExit(
            "REFUSED: writing this checker_result would make the checkpoint "
            f"invalid (protocol_status={result.get('protocol_status')!r}, "
            f"errors={result.get('errors')}). Not writing anything."
        )

    out_path = args.out or args.checkpoint
    out_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    print(
        f"wrote {out_path} (hypothesis_id={args.hypothesis_id}, "
        f"verdict={args.verdict}, tier={args.tier}, "
        f"mechanically_passed={mechanically_passed})"
    )


if __name__ == "__main__":
    main()
