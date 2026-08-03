# Changelog

All notable changes to SkillMe are recorded here. This repo starts its
public history at v0.4.6; the version history from v0.4.6 down through v0.3 is carried over
from the standalone spec document's own §14 Development roadmap for continuity. Current
protocol version: **v0.4.10**.

## 🗂️ Kanban readout — as-of `54946b4`, 2026-08-03

> **Readout, not truth** — a snapshot at the commit above, not a live scoreboard.
> Full board (Done/Backlog cards, evidence tiers) lives in
> `communication_glossary/README.md`'s own Kanban section — kept there as the single
> source so this summary never drifts out of sync with it. Only **Blocked** items
> (waiting on a founder decision, same meaning as `cpg`'s 🔴 OPEN HUMAN-GATES) are
> mirrored here for quick scanning:

| card | tier | blocked-by |
|---|---|---|
| `registration.principal_id` → kernel schema | `[Open]` | scope not yet confirmed |
| per-`(principal_id, topic_tag)` file storage vs. a real index | `[Open]` | scope not yet confirmed |

## communication_glossary Layer 1 — `kg_accumulate.py`: cross-checkpoint word-graph accumulation (2026-08-02, no protocol_version bump)

Founder read Collins & Evans (2002) with this session, then asked to design and build the one
genuinely new gap that reading surfaced (registered in `SKILLME.md` §14's "Expertise-typed roles +
user-growth loop" entry): `kg_extract.py`'s word/phrase graph only ever sees one checkpoint at a
time, with no mechanism to merge it across checkpoints for the same person and topic over time —
the "growing word map" the founder's user-growth requirement needs. Design registered first
(`communication_glossary/README.md`), reviewed independently, then built the same day.

- New `kg_accumulate.py`: merges `kg_extract.py`'s per-checkpoint `word_index` into a persistent,
  growing graph scoped to `(--principal-id, --topic-tag)`. No new node-ID scheme needed —
  `mermaid_id(wtype, word)` already hashes only `(wtype, word)`, confirmed by two independent
  reviews reading the code directly, so cross-checkpoint node collisions already work correctly.
  Idempotent (mirrors `bridge.py`'s `already_ingested()` pattern) and returns the mechanical
  "new vocabulary this checkpoint" set the vocabulary contract needs, without judging whether the
  user actually learned anything — that stays an orchestrator judgment call, out of scope here.
- Storage: `communication_glossary/accumulated/<principal_id>/<topic_tag>/` (JSON state + rendered
  Markdown), gitignored — real per-user runtime state, not a source file.
- `--principal-id`/`--topic-tag` are required CLI args in this pass; the design's proposed
  `registration.principal_id` checkpoint field was not added to the kernel schema — not yet scoped.
- 11 new tests (`tests/test_kg_accumulate.py`), all real invocations against this repo's actual
  example checkpoints, no mocking. `pytest` 140/140 (was 129). `protocol_version` stays `0.4.10` —
  new sibling script, kernel/schema untouched.

## v0.4.10 — Phase 2: checker_result (MC-02 principal separation + MIMCG tier enforcement, 2026-08-02)

Founder ratified `DEC-mimcg-umbrella-skill` into `cpg/AGENTS.md` (step 6.5, cpg PR #113) as an
explicit `human_pi` act -- an AI ratifying its own governance escalation would have defeated the
principle being enforced. With a real MIMCG gate now in force, this builds the actual "check"
step Phase 1b's `raw_result` explicitly refused to be.

- New optional `checker_result` on hypothesis cards (§10). Kernel enforces MC-02
  (`maker_principal_id != checker_principal_id`, hard reject on match) and MIMCG's
  L3+-requires-`HUMAN` rule, both live-verified in both directions. Declaration checks, not
  identity verification -- no identity infrastructure is wired to this repo.
- New `hypothesis_checker.py`: a genuinely separate program from `hypothesis_runner.py`, invoked
  separately -- no flag lets one invocation both generate and check a result. Re-derives
  pass/fail from `raw_result`'s own fields (MC-04), refuses invalid/mismatched/pre-Phase-2
  inputs, warns on mechanically-failed-but-approved.
- `hypothesis_runner.py` gained required `--maker-principal-id`; fixed the same dict-ordering
  bug class the Phase 1b review caught (moved after `**execution`, assert extended).
- 30 new tests (19 kernel + 11 checker), all real invocations, no mocking. `pytest` 119/119 (was
  89). `protocol_version` `0.4.9` -> `0.4.10`.
- **Fixed after independent PR review** (2026-08-02): the MC-02 same-principal comparison in both
  the kernel's `validate()` and `hypothesis_checker.py`'s own preflight check was raw string
  equality, so `"agent-x"` vs `"agent-x "` (trailing whitespace) or `"AGENT-X"` (different case)
  silently passed as two different principals, defeating the guarantee this entry's own text
  above claims. Added `normalize_principal_id()` (strip + casefold) to `skillme_protocol_kernel.py`
  and applied it in both enforcement points -- still a DECLARATION check, not identity
  verification, per the existing scope note above; normalizing closes the trivial bypass, it does
  not add cryptographic identity. 6 new regression tests (2 kernel MC-02 case/whitespace, 1 kernel
  unit test for the normalizer itself, 2 checker-script case/whitespace, 1 checker
  genuinely-different-principals guard against over-normalizing). `pytest` 129/129.

## v0.5.2 — on-stop.sh: fix plugin-only install permanent-block gap (2026-08-02, no protocol_version bump)

Founder handed over two external AI-authored review documents of the live repo
(`skillmenote.md`, `SKILLME.md` snapshot) for extraction. Each of the three claimed P0 bugs was
independently verified against the actual repo before trusting it (readout-not-truth discipline),
not applied on the reviewer's say-so:

- **Confirmed real** — `on-stop.sh`'s fail-closed Stop gate unconditionally required
  `doc_ecosystem_bridge/bridge.py` to have run after a `VALID_CHECKPOINT`. But
  `marketplace.json`'s git-subdir install only fetches `plugins/skillme/` -- `doc_ecosystem_bridge/`
  lives at the repo root and is never present in a plugin-only install. That combination meant a
  plugin-only-install user could never satisfy this gate and would be blocked forever with no way
  out. Fixed: only enforce the bridge requirement when `doc_ecosystem_bridge/bridge.py` is actually
  reachable on disk (checked across `CLAUDE_PROJECT_DIR`, `$(pwd)`, and the plugin root's repo-root
  sibling). Live-verified in three scenarios (isolated plugin-only tree -> no block; full-repo
  checkout -> still blocks, no regression; `doc_eco_done` already true -> no block) plus new
  `tests/test_on_stop_hook.py` regression coverage (4 tests, real `bash` subprocess calls against
  `tmp_path` trees, no mocking).
- **Rejected after verification** — the review's claim that `review_mode` needed strict enum
  validation was checked against the actual fintech fixture
  (`communication_glossary/examples/fintech/checkpoint.json`) and the kernel's own inline comment:
  a non-enum `review_mode` value (`'TARGETED_SEARCH "Phase-2 (draft)"'`) is explicitly documented as
  an intentional, backward-compatible fallback path, with `skill_plan.py` surfacing a graceful note
  about it rather than refusing. An initial attempt to "fix" this as a hard `PROTOCOL_FAIL` broke
  `test_cli_end_to_end_against_real_fintech_fixture` -- confirming it was not a bug, and the change
  was reverted before commit.
- **Deferred, not conclusively verified** — the review's third claim (semantic lineage / narrative
  consistency across the fintech fixture's Q1 vs domain projection) was investigated but not
  conclusively confirmed as a cleanly fixable bug distinct from the kernel's already-disclosed
  structural-only-validation limit; not acted on this round.

## Phase 1b — hypothesis_runner.py: real sandboxed execution (2026-08-02, no protocol_version bump)

Founder confirmed the workspace's `anse-multi-agent-subuser` OS-identity substrate has never
actually been provisioned on this machine (verified live: zero `anse-*` OS users exist,
provisioning needs an interactive `sudo` run) and chose Docker UID/mount separation instead,
scoped to this repo. Every hardening flag was verified live against real Docker on this host
before being relied on -- including catching that `--storage-opt size=...` silently no-ops on
this host's overlay2 driver (a `--storage-opt size=10m` container wrote 50MB with zero error);
`--tmpfs size=Nm` is used instead, confirmed to genuinely enforce.

- New `hypothesis_runner.py`: executes a hypothesis card's `verification_payload` (v0.4.9) in a
  hardened container (`--network=none` by default, `--read-only`, `--cap-drop=ALL`, non-root UID
  65534, no writable bind mount anywhere, `--tmpfs` disk cap, global concurrency lock).
- Every `raw_result` record is hardcoded `status: PENDING_INDEPENDENT_CHECK` /
  `tier: finite_diagnostic` -- there is no code path that writes `APPROVED`, by construction.
  Closes the *filesystem* self-certification loophole; does NOT close the *actor*-level loophole
  (Phase 2, `principal_id` separation, not built here).
- `COQC` (declared in v0.4.9's schema) has no image wired -- refuses cleanly rather than fake it.
- Real bug found by actually running this against a mode-660 fixture file: the sandbox's fixed
  UID can't read files it doesn't own/share a group with -- was a cryptic Docker permission
  error, now a clean preflight refusal with a `chmod` fix in the message.
- **Fixed after independent review** (reviewer actually ran real Docker commands, not just read
  code): (1) `docker` missing from `PATH` raised a raw unhandled `FileNotFoundError` traceback
  instead of a clean refusal -- now caught and refused; (2) `record = {..., "status": ...,
  **execution}` placed the hardcoded `status`/`tier` fields *before* `**execution` in the dict
  literal, so a future field added to `run_in_container()`'s return value named `status` or
  `tier` would silently win Python's last-key-wins merge and defeat the "never writes APPROVED"
  guarantee -- reordered (`**execution` first, hardcoded fields last) plus an explicit `assert`
  that fails loudly if this is ever violated. Both fixes have dedicated regression tests.
- 12 new tests against real Docker (no mocking; 2 of the 12 are the review-driven fixes above).
  `pytest` 89/89 (was 77). `protocol_version` stays `0.4.9` -- new sibling script, kernel/schema
  untouched.

## v0.4.9 — Phase 1a: hypothesis verification-payload schema (2026-08-02)

Founder-driven ultracode team meeting (5 position papers → chair synthesis → 3-lens adversarial
review) proposed connecting a docker hypothesis-verification sandbox + maker-checker gate +
expert-registration into skillme. Review found the design's core premise had no attachment
point in the real repo: `HYPOTHESIS_REQUIRED` had zero fields able to hold executable code.
This is Phase 1a of the review's fixed build order -- schema first, container work later.

- Added `verification_payload` (OPTIONAL, spec §10) to hypothesis cards: `payload_ref`,
  `entrypoint`, `language` (`PYTHON3`/`BASH`/`COQC`), `declared_inputs`, `network_required`,
  `resource_class` (`LIGHT`/`HEAVY`), `expected_exit_status`. Kernel validates shape only --
  never resolves/executes anything; `claim_boundary` unchanged (`STRUCTURE_ONLY`).
- Fully backward-compatible: absent on every existing fixture, all stay `VALID_CHECKPOINT`.
- Phase 1b (the actual sandbox runner + separate-identity status writer) and Phase 2
  (`principal_id`-level maker/checker separation) are explicitly NOT part of this entry -- see
  spec §14 for the full review findings on why those can't be claimed "closed" yet.
- 10 new kernel tests (1 positive shape-valid, 1 absent-by-default, 8 negative cases covering
  every validated sub-field). `pytest` 77/77 (was 67), kernel `--self-test` 14/14 unaffected.

## Plugin v0.5.1 — Live-tested and fixed two real hook bugs (2026-08-02)

Founder asked to actually test the v0.5.0 hooks in a fresh session rather than trust static
review. Spun up genuinely separate `claude -p ... --plugin-dir plugins/skillme` subprocesses
(a real new process, not this session) and inspected `~/.claude/debug/<session>.txt` for ground
truth. Found two real bugs neither static review nor pipe-testing could have caught:

1. **Hook loading failed entirely.** `plugin.json`'s `"hooks": "./hooks/hooks.json"` field
   (added "for clarity" in v0.5.0) duplicated the same path Claude Code auto-discovers by
   default, and the loader treats that as an error: `Duplicate hooks file detected... Hook
   load failed`. Every skillme hook was silently registered as zero hooks. Fixed by removing
   the redundant declaration.
2. **The `TaskCreated` hook event never fires** in Claude Code 2.1.220 despite being in the
   documented event list — confirmed by calling `TaskCreate` 4 times in a live session and
   finding zero `TaskCreated` log lines. `on-stop.sh`'s `task_created` check was silently
   always false via that path. Fixed by checking Claude Code's own real task storage
   (`~/.claude/tasks/<session_id>/*.json`, found by inspecting a live session -- not
   officially documented, kept as the primary signal with the old state-file flag as a
   fallback OR in case a future version does fire `TaskCreated`).

After both fixes, re-tested live end-to-end: a session instructed to invoke skillme then
explicitly refuse to call TaskCreate under any circumstances was blocked by the `Stop` hook
**9 consecutive times** (`"decision":"block"` in the debug log each time, matching the model's
own "Fourth repetition... still holding" text) until the CLI's own unrelated turn budget ended
the process -- the hook itself never gave up. A second session (compliant, not told to refuse)
was blocked twice, called `TaskCreate` in response, and passed cleanly. `on-skill-invoke.sh`'s
`additionalContext` injection was also confirmed firing (555 chars logged) exactly once per
skill load.

## Plugin v0.5.0 — Bundled fail-closed Stop hook (2026-08-02)

Founder request: connect the plugin's own operational contract (use `TaskCreate` to track
phases; run `doc_ecosystem_bridge/bridge.py` at `VALID_CHECKPOINT`) to something structural,
not just SKILL.md prose that can be skipped under pressure. Added
`plugins/skillme/hooks/hooks.json` + `plugins/skillme/scripts/*.sh`, auto-discovered and
activated by Claude Code for every project the plugin is installed in — no per-project
settings.json edit required (`${CLAUDE_PLUGIN_ROOT}` resolves the bundled scripts wherever the
plugin lands).

- `PostToolUse` on the `Skill` tool: when this skill loads, marks the session active and
  injects a reminder of the contract as `additionalContext`.
- `PostToolUse` on `Bash`: detects the two real signals from the commands actually run —
  `skillme_protocol_kernel.py` returning `VALID_CHECKPOINT`, and `doc_ecosystem_bridge/bridge.py`
  actually executing — rather than guessing from conversation text.
- `TaskCreated`: records that the assistant's own todolist was actually used.
- `Stop`: the enforcement point. Blocks turn-end with a `reason` naming exactly what's missing
  (untracked phases, or a checkpoint that was never bridged into doc-eco) if this session
  invoked the skill; a silent no-op for every other session. Blocking returns control to the
  assistant to act, not a hard session stop — the next `Stop` re-checks and passes once
  satisfied.

State lives in a per-session temp file (`$TMPDIR/skillme-hook-state/<session_id>.json`), not
committed to any project. Pipe-tested all 4 scripts end-to-end with synthetic hook JSON (no-op
on non-skillme skill, active-marking, block-then-clear on TaskCreate, block-then-clear on
checkpoint+bridge.py, and the unrelated-session no-op) before merging. Plugin version bumped
0.4.8 -> 0.5.0 (a real plugin capability change); `protocol_version` untouched at 0.4.8 since
no kernel validation logic changed.

## v0.4.8-rebrand-internal — Protocol's internal identity renamed UIA -> SkillMe (2026-08-02)

Follow-up founder decision to the entry below: the UIA internal identity that the prior rebrand
deliberately left untouched is now renamed too. Scope:

- `uia_protocol_kernel.py` -> `skillme_protocol_kernel.py` (module rename; every import/
  subprocess call across `tests/`, `run_pipeline.py`, `communication_glossary/*.py`,
  `doc_ecosystem_bridge/bridge.py`, `tools/generate_field_reference.py` updated in lockstep).
- `UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md` -> `SKILLME.md` (canonical spec filename; chosen with no
  version number embedded, on purpose, to stop this exact class of stale-filename drift from
  recurring — the old frozen-filename convention this reverses is itself why the file said
  "v0.4.6" in its name while its own content had already moved to v0.4.8).
- Every `UIA` acronym, `Universal Issue Analysis` phrase, and `UIA-*` formal ID (axioms `UIA-A0`
  .. `UIA-A12`, `UIA-CORE`, `UIA-RGM`) renamed to `SkillMe`/`SKILLME-*` throughout the kernel,
  the spec, and every subsystem README/docstring — live/current text only, historical dated
  status entries describing what a past commit did are left untouched on purpose (they're
  accurate history, not stale current claims).
- One schema-adjacent field, `canonical_uia_mapping` (documented in spec §6.9, present in the
  alt-domain fixture and 3 communication_glossary examples, but confirmed **not** actually
  read/enforced by `validate()`), renamed to `canonical_skillme_mapping`. Called out separately
  from pure branding because it's a documented contract field name, even though inert today.
  Several other spec-only illustrative field names in the same family
  (`uia_input_mapping`/`uia_output_mapping`/`uia_entry_gate`/`uia_exit_mapping`/
  `uia_analysis_sheet`, the `uia_run`/`uia_rgm` YAML example keys) were confirmed the same way
  (grepped for real fixture usage and kernel `.get()`/subscript access — none found) before
  renaming.
- Also fixed, while in the area: the spec's own "Standalone execution contract" section
  (§ near the end) had referenced a companion filename `uia_protocol_kernel_v0_4_6.py` that
  never actually matched the real file in this repo (`uia_protocol_kernel.py`, no version
  suffix) even before this rename — a pre-existing bug, now corrected to the real filename.

`protocol_version` stays `0.4.8` — no kernel validation logic changed, only names.
pytest 67/67, kernel `--self-test` 14/14 after the rename.

## v0.4.8-rebrand — Repo/plugin/marketplace renamed to `skillme` (2026-08-02)

Founder rebrand decision (no protocol/kernel change, `protocol_version` stays `0.4.8`): GitHub
repo `morrocwi/universal-issue-analysis` -> `morrocwi/skillme`, plugin subtree
`plugins/universal-issue-analysis/` -> `plugins/skillme/` (including the installable skill's
own invocation name), `plugin.json`/`marketplace.json` name fields, git-subdir `source.url`,
and every outward-facing install command/path reference in README.md/llms.txt/AI_START_HERE.md.
This tag exists so `marketplace.json`'s git-subdir `ref` has a real commit to resolve against
that actually contains `plugins/skillme/` — the prior `v0.4.8` tag predates the rename and only
has `plugins/universal-issue-analysis/` at that commit, which would make a fresh
`/plugin install` fail to resolve the path. The protocol's own internal identity (`UIA` inside
`uia_protocol_kernel.py`, the canonical spec's title) is intentionally untouched — a separate,
higher-risk follow-up decision, not done here.

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

See [`SKILLME.md`](SKILLME.md) §14 for the
full roadmap prose, including the planned v0.5–v0.7 formal-semantics, adversarial-fixture, and
cross-domain field-evaluation milestones — none of those are complete yet; do not cite them as
done. Same section also registers a founder-stated next direction (an expert-declaration system
and a skill-registration system) as of 2026-08-01 — not yet scoped, not yet started, logged as a
pointer for the next session rather than a commitment.
