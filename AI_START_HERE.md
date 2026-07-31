# AI_START_HERE.md — read this before touching any single file

> [!WARNING]
> Do not infer this project's maturity from its size. The spec (`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`,
> ~3,700 lines) is large and detailed, but the whole project self-declares tier `Dr`
> (design rationale) — an architectural synthesis of established methods, not a proven result.
> The kernel validates *protocol structure*, not domain truth. Read
> [Tier honesty](README.md#tier-honesty) in the README before making any claim about what this
> project proves.

## What this project is

**Universal Issue Analysis (UIA)** — a philosophy-first protocol for analyzing any reported
issue (software incident, complaint, conflict, policy question, research anomaly, everyday
decision) as a finite, auditable retained difference instead of a guessed name/cause/fix. It
shares its readout-first foundation with `information-discrete-math` and `readout_genesis`
(same author, Yaoharee Lahtee): everything an agency can act on is a finite retained difference,
not the world itself.

## Discovery order — do these in sequence, don't skip ahead

1. **`README.md`** — framing, tier-honesty statement, quickstart, repo map.
2. **`plugins/universal-issue-analysis/skills/universal-issue-analysis/SKILL.md`** — the
   operational summary an AI assistant actually loads and follows: the two-question intake
   gate, the core protocol moves in order, the hard invariants, the output shape. This is the
   file to read if you're about to *use* the protocol, not just describe it.
3. **`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`** — the canonical, normative spec. §0 states the
   authority order (protocol invariants §11 > canonical 20-phase workflow §6.14 >
   machine-readable contract §10 > glossary/enums §3 > everything else is a view/checklist).
   Read this in full before disputing an edge case, extending the protocol, or claiming a
   section contradicts another.
4. **`python3 uia_protocol_kernel.py --self-test`** — run this yourself (stdlib only, no
   network, no install) before repeating any pass/fail claim about the kernel. At the time this
   file was written it reported `14/14 PASS`; re-run it on your checkout rather than trusting
   this number.
5. **`tests/test_kernel_self_test.py`** (`python3 -m pytest tests/ -q`) — pytest wrapper around
   the same self-test plus the demo/checkpoint-demo fixtures.
6. **`CHANGELOG.md`** — version history through v0.4.6; states plainly which later milestones
   (v0.5–v0.7: formal semantics, adversarial fixtures, cross-domain field evaluation) are *not*
   done yet.

## The one thing not to do

Do not summarize UIA as "just root-cause analysis" or "just a chatbot intake form" — both miss
what's actually load-bearing: the zero/unresolved separation (spec §UIA-A6), the
stakeholder-vs-agency split with 12 distinct agency roles (spec §4.3), the mandatory
bidirectional global+local evidence challenge before any hypothesis reaches a candidate (spec
§6.17), and the resumable `STOP_AT_HYPOTHESIS` checkpoint that lets a run pause without
smuggling in a decision (spec §6.17.11). Read §13 of the spec ("What is original in this
synthesis") for the author's own claim of what's new versus inherited from prior art.
