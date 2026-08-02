# Changelog

All notable changes to Universal Issue Analysis (UIA) are recorded here. This repo starts its
public history at v0.4.6; the version history from v0.4.6 down through v0.3 is carried over
from the standalone spec document's own §14 Development roadmap for continuity. Current
protocol version: **v0.4.8**.

## v0.4.8 — 10-domain fit-test refinements

- Ran issue→hypothesis across 10 new domains (astronomy, agriculture, music, law, sports, urban
  planning, ecology, culinary science, linguistics, military logistics) to test whether §6.9.1's
  domain-mapping method (v0.4.7) genuinely connects to the root grammar, not just passes schema.
  Result: `VALID_CHECKPOINT` 10/10, genuine (non-forced) fit 9/10, `Dr`-tier ceiling flawless in
  all 10 — see spec §6.9.4 for the full findings and what was and wasn't changed as a result.
- Added a third `hypothesis_evidence_challenge.review_mode` value, `FIELD_OBSERVATION_LOG`, for
  domains whose real evidence is a fresh sensory/field observation, not a citable document or
  system log — `observer`/`observation_method`/`observed_at`/`location_or_context` in place of
  literature or internal-system fields, same rigor otherwise.
- Documented (kernel behavior unchanged) that only 5 of `agency`'s 13 list-type fields were ever
  enforced non-empty — the other 8 may stay `[]` for small, direct-actor issues; locked in with a
  permanent regression test so this doesn't silently change later.
- Added a false-precision caveat to spec §2: "retained difference" can sound more measurable than
  it is when the reader is a human sense (a conductor's ear, a baker's palate) rather than a
  sensor — the readout is still valid by definition, but its reproducibility is lower than the
  vocabulary might suggest.
- `pytest` 13/13 (was 9), kernel `--self-test` 14/14 unaffected (demo/checkpoint-demo fixtures
  untouched).

## v0.4.8 patch — protocol_version drift fix (2026-08-02)

The commit above changed `uia_protocol_kernel.py`'s validation logic (new `review_mode`) but
left `VERSION = "0.4.6"` unbumped, so every run the kernel produced kept declaring
`protocol_version: "0.4.6"` — a real spec/runtime drift, not a docs typo. Found while verifying
local state against GitHub before tagging this release. Fixed: `VERSION` constant, schema
`$id`/`title`, CLI description, the spec doc's header `Version:` field and §10 example, and
every fixture/example `checkpoint.json` that hardcoded `"protocol_version": "0.4.6"`
(`fixtures/checkpoint_demo_alt_domain.json` + 3 files under `communication_glossary/examples/`)
now consistently read `0.4.8`. `pytest` 67/67, kernel `--self-test` 14/14 after the fix.

## v0.4.7 — External lineage consolidation (Philosophy-Logic-Mapping core)

Documentation-only — no change to `uia_protocol_kernel.py`, schema, or `protocol_version`.
Connected UIA's philosophy/logic core to 4 sibling repos in the same author's lineage
(`readout_genesis`, `research_universal_solver`, `readout_universe`,
`information-discrete-math`) that were never actually linked to this repo before, after
independently reading each one's real current content (not assumed from memory):

- Fixed spec §3's root-grammar equation to restore tier tags (`⊢[Th_coqc]`, `⊢[Dr]`) that a
  prior version had silently dropped — verified byte-for-byte against
  `readout_genesis/READOUT_GENESIS_CORE.md`'s actual current definition.
- Added §6.9.1 "Domain mapping method" — a quotient-declaration + tier-ceiling discipline
  borrowed (structure only, not authority/tier) from `readout_genesis`'s proven
  domain-registration standard, explicitly capped at `Dr` tier and terminating at the
  hypothesis-portfolio checkpoint — never a science claim, usable for hypothesis generation in
  any domain precisely because it doesn't require machine-checked proof.
- Added §6.9.2 (a pointer to `information-discrete-math`'s contaminated-concept table, for
  hypotheses touching continuum-math concepts) and §6.9.3 (an informative-only reference to
  `readout_universe`'s Lens Law translation loop).

## v0.4.6 — Claim-Preserving Resumable Hypothesis Checkpoint

- Repo-ized the standalone spec (`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`) and its executable
  companion (`uia_protocol_kernel.py`) as an installable Claude Code skill/marketplace plugin.
- No protocol changes from the spec's own v0.4.6: adds a machine-checkable
  `STOP_AT_HYPOTHESIS` / `RUN_FULL` checkpoint after Phase 12 (§0.1, §6.17.11) that lets a run
  pause at a certified three-lane hypothesis portfolio without making a decision, intervention,
  or field-truth claim, and resume later from the same `continuation_record` without silently
  starting a new lineage.

## Repository additions (downstream tooling, not protocol version changes)

These sit on top of a `VALID_CHECKPOINT` run record rather than changing the protocol/kernel
itself, so they're tracked here separately from the vX.Y.Z entries above. See each subsystem's
own README for its own status history.

- **`doc_ecosystem_bridge/`** — bridges a checkpoint into a
  [`human-ai-doc-ecosystem`](https://github.com/morrocwi/human-ai-doc-ecosystem) project
  (`logbook.jsonl` entries, `DECISIONS.md` open questions, optional `--seed-docs` drafting).
  Absorbed from a standalone repo, then fixed across 3 rounds of adversarial + real-usage
  ultracode testing (Mermaid/Markdown-injection escaping, idempotency, decision-owner lookup,
  scaffold retitling, `INTERNAL_DATA_AUDIT` review_mode, relaxed `authority_assumptions`
  carve-out).
- **`communication_glossary/`** — a 3-layer pipeline (deterministic word graph → AI-interpretive
  expert-framework layer → issue-anchored glossary) that produces the shared vocabulary two
  people from different fields need to discuss the same issue. Iterated across a harsh-content
  stress test (Mermaid node-id/backtick escaping, `None`-node fabrication) and a full-pipeline
  cold-start review, with 3 worked examples (fintech; healthcare↔nursing; billing↔accounting)
  each independently WebSearch-verified.

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
done. Same section also registers a founder-stated next direction (an expert-declaration system
and a skill-registration system) as of 2026-08-01 — not yet scoped, not yet started, logged as a
pointer for the next session rather than a commitment.
