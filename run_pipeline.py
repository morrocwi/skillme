#!/usr/bin/env python3
"""Thin orchestrator for the communication_glossary pipeline.

Shells out to the repo's own scripts as subprocesses — it does NOT reimplement
any of their logic. Each script stays the single source of truth for its own
layer:

  kg_extract.py        -> Layer 1 (kg_raw_word.md)
  [Agent/WebSearch]     -> Layer 2 (kg_expert_layer.md) -- NOT scriptable, see below
  build_glossary.py    -> Layer 3 (glossary.md)
  skill_plan.py         -> Layer 4 (skill_plan.md)
  doc_ecosystem_bridge/bridge.py -> optional attach into a doc-ecosystem target

Usage:
    python3 run_pipeline.py <checkpoint.json> --out-dir <dir> \
        [--kg-expert-layer <existing_kg_expert_layer.md> | --skip-layer2] \
        [--doc-eco-target <dir> [--seed-docs] [--doc-eco-repo <path>]]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

STUB_KG_EXPERT_LAYER = """# kg_expert_layer — {checkpoint_ref} (AI-INTERPRETIVE, OPEN TIER)

**This is NOT a readout.** This file is a --skip-layer2 STUB, not a real Layer 2
enrichment. No Agent/WebSearch expert-framework reasoning was performed. Every
section below is an empty placeholder. Do not treat this as validated fact or
even as an AI's honest judgment call — re-run with --kg-expert-layer pointing at
a real Layer 2 output (see communication_glossary/README.md's Layer 2 prompt
template) before trusting downstream glossary/skill_plan output.

## Domain(s) identified

(none — stub, not populated)

## Relevant frameworks/methodologies per domain

(none — stub, not populated)

## What I verified via WebSearch vs. asserted from training knowledge

(none — stub, no WebSearch was performed)

## Vocabulary this adds beyond kg_raw_word.md's raw extraction

(none — stub, not populated)

## Open questions / where a human expert should override this

- This entire file is a --skip-layer2 stub. A human/Agent should author a real
  kg_expert_layer.md (see communication_glossary/README.md) and re-run this
  pipeline with --kg-expert-layer instead of --skip-layer2.
"""


def load_kernel(uia_repo: Path):
    sys.path.insert(0, str(uia_repo))
    import uia_protocol_kernel  # type: ignore

    return uia_protocol_kernel


def validate_checkpoint_or_refuse(checkpoint_path: Path) -> dict:
    try:
        run = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"REFUSED: {checkpoint_path} not found")
    except json.JSONDecodeError as e:
        raise SystemExit(f"REFUSED: {checkpoint_path} is not valid JSON: {e}")

    kernel = load_kernel(REPO_ROOT)
    result = kernel.validate(run)
    if result.get("protocol_status") != "VALID_CHECKPOINT":
        raise SystemExit(
            "REFUSED: checkpoint is not a VALID_CHECKPOINT hypothesis portfolio "
            f"(protocol_status={result.get('protocol_status')!r}, "
            f"errors={result.get('errors')}). Fix the checkpoint before running "
            "the pipeline — proceeding would spawn subprocesses on unvalidated data."
        )
    return run


def run_subprocess(cmd: list) -> None:
    # stdout streams live (each layer script's own "wrote ..." progress message
    # is real-time feedback, not noise to swallow) — only stderr is captured, so
    # a failure's error message can be re-raised verbatim without also hiding
    # every prior successful step's output until the whole pipeline finishes.
    try:
        subprocess.run([str(c) for c in cmd], check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.stderr) from None


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("checkpoint", type=Path, help="UIA hypothesis checkpoint JSON file")
    p.add_argument("--out-dir", type=Path, required=True, help="output directory for the 4 layer files")
    layer2 = p.add_mutually_exclusive_group()
    layer2.add_argument(
        "--kg-expert-layer",
        type=Path,
        default=None,
        help="path to an already-authored kg_expert_layer.md (Layer 2, Agent/WebSearch output)",
    )
    layer2.add_argument(
        "--skip-layer2",
        action="store_true",
        help="write a minimal, honestly-labeled stub instead of a real Layer 2 (not recommended)",
    )
    p.add_argument(
        "--doc-eco-target",
        type=Path,
        default=None,
        help="if given, also run doc_ecosystem_bridge/bridge.py against this target dir",
    )
    p.add_argument("--seed-docs", action="store_true", help="passed through to bridge.py")
    p.add_argument("--doc-eco-repo", type=Path, default=None, help="passed through to bridge.py")
    args = p.parse_args()

    # 1. Validate the checkpoint via the kernel directly, before spawning anything.
    run = validate_checkpoint_or_refuse(args.checkpoint)
    checkpoint_ref = (
        (run.get("hypothesis_portfolio") or {}).get("checkpoint_certificate", "unknown-checkpoint")
    )

    # Fail fast on a missing --kg-expert-layer file too, before Layer 1 even runs —
    # otherwise a nonexistent path crashes with a raw traceback *after* kg_raw_word.md
    # has already been written, leaving an undocumented partial-output state (an
    # independent PR review caught this: the old code only tried the read at Layer 2,
    # by which point Layer 1's subprocess had already succeeded).
    if args.kg_expert_layer is not None and not args.kg_expert_layer.is_file():
        raise SystemExit(f"REFUSED: --kg-expert-layer {args.kg_expert_layer} not found")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    kg_raw_word = args.out_dir / "kg_raw_word.md"
    kg_expert_layer = args.out_dir / "kg_expert_layer.md"
    glossary = args.out_dir / "glossary.md"
    skill_plan = args.out_dir / "skill_plan.md"

    # 2. Layer 1 — kg_extract.py
    run_subprocess([sys.executable, REPO_ROOT / "communication_glossary/kg_extract.py", args.checkpoint, kg_raw_word])

    # 3. Layer 2 — deliberately NOT scriptable (Agent+WebSearch reasoning; see
    #    communication_glossary/README.md "Layer 2 — expert-framework reasoning").
    if args.kg_expert_layer is not None:
        kg_expert_layer.write_text(args.kg_expert_layer.read_text(encoding="utf-8"), encoding="utf-8")
    elif args.skip_layer2:
        print(
            "WARNING: --skip-layer2 given — kg_expert_layer.md is a STUB, no real "
            "expert-framework enrichment (Agent/WebSearch reasoning) was performed.",
            file=sys.stderr,
        )
        kg_expert_layer.write_text(
            STUB_KG_EXPERT_LAYER.format(checkpoint_ref=checkpoint_ref), encoding="utf-8"
        )
    else:
        raise SystemExit(
            "REFUSED: Layer 2 (kg_expert_layer.md) cannot be produced by this script — it "
            "is deliberately an Agent/WebSearch reasoning step, not a Python script (see "
            "communication_glossary/README.md, 'Layer 2 — expert-framework reasoning' section, "
            "for the exact prompt template). Author kg_expert_layer.md yourself via an "
            "Agent/WebSearch call and re-run with --kg-expert-layer <path>, or pass "
            "--skip-layer2 to write an honestly-labeled stub instead."
        )

    # 4. Layer 3 — build_glossary.py
    run_subprocess(
        [sys.executable, REPO_ROOT / "communication_glossary/build_glossary.py", kg_raw_word, kg_expert_layer, glossary]
    )

    # 5. Layer 4 — skill_plan.py (glossary.md is arg2, NOT kg_raw_word.md)
    run_subprocess(
        [sys.executable, REPO_ROOT / "communication_glossary/skill_plan.py", args.checkpoint, glossary, kg_expert_layer, skill_plan]
    )

    produced = [f for f in (kg_raw_word, kg_expert_layer, glossary, skill_plan) if f.exists()]

    # 6. Optional doc-ecosystem bridge attach.
    if args.doc_eco_target is not None:
        bridge_cmd = [
            sys.executable,
            REPO_ROOT / "doc_ecosystem_bridge/bridge.py",
            args.checkpoint,
            args.doc_eco_target,
        ]
        if args.seed_docs:
            bridge_cmd.append("--seed-docs")
        if args.doc_eco_repo is not None:
            bridge_cmd += ["--doc-eco-repo", args.doc_eco_repo]
        bridge_cmd += ["--attach-communication", args.out_dir]
        run_subprocess(bridge_cmd)

    # 7. Summary.
    names = ", ".join(f.name for f in produced)
    print(f"DONE — produced in {args.out_dir}: {names}")


if __name__ == "__main__":
    main()
