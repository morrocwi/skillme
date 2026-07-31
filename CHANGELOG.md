# Changelog

All notable changes to Universal Issue Analysis (UIA) are recorded here. This repo starts its
public history at v0.4.6; the version history below through v0.4.6 is carried over from the
standalone spec document's own §14 Development roadmap for continuity.

## v0.4.6 — Claim-Preserving Resumable Hypothesis Checkpoint (this release)

- Repo-ized the standalone spec (`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`) and its executable
  companion (`uia_protocol_kernel.py`) as an installable Claude Code skill/marketplace plugin.
- No protocol changes from the spec's own v0.4.6: adds a machine-checkable
  `STOP_AT_HYPOTHESIS` / `RUN_FULL` checkpoint after Phase 12 (§0.1, §6.17.11) that lets a run
  pause at a certified three-lane hypothesis portfolio without making a decision, intervention,
  or field-truth claim, and resume later from the same `continuation_record` without silently
  starting a new lineage.

## v0.4.5 — Global–Local Hypothesis Evidence Challenge

- Added the bidirectional (support + challenge) evidence-search protocol per hypothesis,
  split into an international track and a local-context track (§6.17).
- Added the Citation Card with separate `metadata_verification` and `scope_verification`.
- Added the global–local transfer matrix and forbade collapsing "not found locally" into
  "does not exist locally".

## v0.4.4 — Standalone consolidation and executable protocol kernel

- Consolidated the spec into a document readable without the conversation that produced it.
- Shipped the first version of the stdlib-only Python protocol-structure validator.

## v0.4.3 — Two-Question Intake Gate

- Made the Q1 (issue) + Q2 (proposal) intake gate mandatory before any analysis, with an
  explicit `PROPOSAL_ABSENT_DECLARED` state distinct from "unanswered", and a scoped
  emergency-containment-only bypass that cannot reach a causal or solution verdict.

## v0.4.2 — Optional User Proposal Input

- Added the dual-tape rule separating raw issue observation from user-proposed solutions,
  `AUTO` / `USER_PROPOSAL_INTEGRATED` / `AI_INDEPENDENT` / `HYBRID_BLIND_COMPARE` modes, and
  non-privileged proposal outcomes (proposals get no extra credit for being the reporter's).

## v0.4.1 — Three-Lane Candidate Production

- Required every run that reaches a decision to search for three structurally distinct
  candidate lanes (Known-Direct / Cross-Adaptive / Generative-Transformative) as a search
  duty, with honest partial/information-only statuses when fewer than three are admissible.

## v0.4 — Philosophy-First Domain Translation Protocol

- Separated stakeholder from agency and expanded the agency-role/asymmetry matrix.
- Added the bidirectional user-language ↔ canonical-UIA translation contract with loss audit.
- Added the Universal Adapter Card contract so domain methods (RCA, FMEA, DMAIC, stakeholder
  mapping, DAGs, systems dynamics, MCDA, etc.) plug in without silently promoting their own
  evidence tier.

## v0.3 — Retained Graph–Matrix Protocol

- Added the Issue Topology Ladder and the `CHAIN/PATTERN/NETWORK/NONLINEAR/SCALE/GENERATIVE/
  HYBRID` adapter router.
- Added the graph–matrix kernel and query-relative minimal-quotient gate.
- Status at this stage: `finite_diagnostic`/`Dr` only, not field-validated.

See [`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`](UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md) §14 for the
full roadmap prose, including the planned v0.5–v0.7 formal-semantics, adversarial-fixture, and
cross-domain field-evaluation milestones — none of those are complete yet; do not cite them as
done.
