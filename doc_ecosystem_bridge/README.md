# doc_ecosystem_bridge

Wires this repo (**skillme**, protocol codename UIA / Universal Issue Analysis) to Yaoharee Lahtee's
`human-ai-doc-ecosystem` (doc-eco) repo, per founder request (2026-08-01). Originally
built and smoke-tested as a standalone `uia-doc-ecosystem-bridge` repo, then absorbed
into UIA itself (same day, founder request: "ดูดกลืนเข้าไปเป็นงานเดียวกัน") so the
integration lives with the protocol it extends, under one repo name.

- **UIA** (this repo) — a 20-phase issue-analysis protocol. Phase 12 certifies a
  **hypothesis portfolio** and can stop there (`STOP_AT_HYPOTHESIS`), instead of
  continuing to candidate generation / decision / action.
- **`human-ai-doc-ecosystem`** (doc-eco) — a blank starter documentation structure
  (20 templates, 4 checkers) that a project scaffolds via `init.mjs` and then fills in
  by hand as it goes.

**The integration:** doc-eco becomes the *next phase* after UIA's hypothesis checkpoint,
not a separate workflow. When a UIA run reaches `VALID_CHECKPOINT` at phase 12, this
bridge scaffolds (or reuses) the target project's doc-eco structure and records each
hypothesis card as a `hypothesis`-kind logbook entry plus an open question in
`DECISIONS.md` — never as a settled `ADR`, because a hypothesis isn't settled until UIA's
own phase 16 (`DECIDE`) picks a lane.

## Status — 2026-08-01, `--seed-sot-docs` added (rag.md / cite.md / eq.md)

Founder request (verbatim): "ให้ rag.md สำหรับ sot ของ hypo ที่ควรมีควรเพิ่ม ควรหา ควรใช้อื่นๆ.
cite.md. eq.md. หรือควรมีอะไรอีกที่ตัดระเบียบ data และ sot ของ issue" — a source-of-truth
document set for a hypothesis's data discipline: what sources exist/should be added
(rag.md), what's actually cited and how solid it is (cite.md), and what quantitative
claims/thresholds the checkpoint already states (eq.md). Founder confirmed via a
clarifying question that this is a **separate document set attached to doc-eco only**
— not a new `communication_glossary` pipeline layer, not a checkpoint schema change.

- `seed_sot_docs()`: creates `target/sot/rag.md`, `cite.md`, `eq.md`. Every section is
  either a direct readout of already-kernel-validated `hypothesis_evidence_challenge`/
  `hypothesis_portfolio`/`registration` fields, or an explicit, empty "human/AI to fill
  in — NOT auto-generated" placeholder — this function never fabricates a recommended
  source, a real citation, or a formula itself (same discipline as `attach_communication()`
  and `communication_glossary`'s own Layer 1/3-vs-Layer-2 split). `cite.md` automatically
  flags any citation with `metadata_verification`/`scope_verification == SIMULATED_ONLY`
  as a synthetic fixture, not real evidence — tested directly: a real-looking citation
  next to a `SIMULATED_ONLY` one only flags the latter.
- Idempotent per file via a `<!-- sot-doc:v1 -->` marker; links itself from
  `target/README.md` via `link_sot_docs_in_readme()`, same pattern as
  `link_communication_in_readme()`.
- Wired into `run_pipeline.py` too (`--seed-sot-docs` passes through to `bridge.py`).
- 10 new pytest tests (`tests/test_bridge.py`) cover creation, idempotency, per-file
  readout correctness, the `SIMULATED_ONLY` flagging, graceful degradation when
  `hypothesis_evidence_challenge` is entirely absent, and — the load-bearing check — that
  the placeholder sections genuinely never contain fabricated content. Spot-verified not
  tautological: reverted the `SIMULATED_ONLY` flagging guard in a scratch copy and
  confirmed the flag disappears without it.
- Confirmed via real execution against the real `human-ai-doc-ecosystem` sibling repo
  (fintech and gut-health-nurse-triage examples): `eq.md` correctly surfaces the
  fintech example's real numeric threshold ("double-counted SETTLED rate ต่ำกว่า 0.01%
  ต่อวัน") verbatim from `registration.failure_rule`.
- **Independent review found one real MUST-FIX**, fixed same pass: `_escape_cell()` was
  applied inconsistently across the 3 new render functions — free-text fields
  (`claim`/`mechanism`/`predicted_readout`/`falsifier`/`next_discriminating_test`/
  `success_rule`/`failure_rule` and several citation-card fields) were interpolated raw,
  so an embedded backtick or newline (realistic for LLM-generated checkpoint content)
  corrupted the markdown list structure — the exact bug class already fixed twice
  elsewhere in this file (`skill_plan.py`, `seed_docs()`'s `PLAN.md` section). Fixed by
  wrapping every checkpoint-derived interpolation with `_escape_cell()`; added a
  regression test, confirmed to fail against a scratch copy with the fix reverted.
- `pytest tests/ -q` → 67 passed in this environment (11 new + 56 pre-existing; node +
  the sibling repo are both present here, so no tests skip — the exact pass/skip split
  depends on whether the doc-eco sibling repo is reachable from wherever the suite is
  run from, since a few tests are `skipif`-guarded on that).
  `uia_protocol_kernel.py --self-test` → 14/14.

## Status — 2026-08-01, orchestrator + automated test coverage added

Same pass as `communication_glossary/README.md`'s "one-command orchestrator + automated
test coverage" entry — see that README for the full write-up. What lands in this repo:
`run_pipeline.py` (repo root) can drive this script's `--seed-docs --attach-communication`
path as one step of a single command instead of a separate manual invocation, and
`tests/test_bridge.py` (23 real pytest functions, new — none existed before) locks in
every `attach_communication()`/`link_communication_in_readme()`/`seed_docs()`/
`_escape_cell()` fix from the two prior ultracode passes as a regression test, not just a
one-time manual re-verification. Tests needing the real `human-ai-doc-ecosystem` sibling
repo are `pytest.mark.skipif`-guarded on `node` + the repo's presence, and ran for real
(not skipped) in this environment. `pytest tests/ -q` → 56 passed;
`uia_protocol_kernel.py --self-test` → 14/14.

## Status — 2026-08-01, communication_glossary <-> doc-eco seam closed (README pointer)

Founder request (verbatim): "เชื่อมเรื่อง word และ skill_plan ให้เข้ากันกับ รอยต่อกับ doc eco"
— connect Layer 1's word graph and Layer 4's skill plan so they're actually
joined at the seam with doc-eco, not just physically present. Until now,
`--attach-communication` copied the 4 files into `target/communication/` but
nothing in the scaffold's own docs pointed there — a human/AI opening
`README.md` (the doc-eco scaffold's own stated front door) had no way to
discover `communication/` existed short of already knowing to look. Added
`link_communication_in_readme()`: whenever `--attach-communication` actually
attaches at least one file, it appends one idempotent `## communication_glossary
output` section to `target/README.md` naming each attached file with what it
is, ending with an explicit "start with `skill_plan.md` ... / start with
`kg_raw_word.md` ..." pointer.

Confirmed via real execution against the **real** `human-ai-doc-ecosystem` repo
(not a scratch fixture) — `bridge.py <fintech checkpoint> <scratch target>
--seed-docs --attach-communication communication_glossary/examples/fintech`
against the actual `ANSE.ASIA/human-ai-doc-ecosystem` `init.mjs`:
- `target/README.md` gained the new section with all 4 real filenames.
- Re-running the identical command a second time: `grep -c` for the section
  marker stays at 1 (idempotent, no duplicate section), and no `LINKED`
  message prints on the second run (nothing to add).
- `node tools/check_logbook.mjs` on the resulting real scaffold: `OK — every
  entry is well formed`.
- Edge cases tested directly (not just reasoned about): a target missing
  `README.md` and an empty `attached` list both return `False` / no-op rather
  than crashing.

`pytest tests/ -q` (13/13) and `uia_protocol_kernel.py --self-test` (14/14)
both re-confirmed unaffected.

## Status — 2026-08-01, SMOKE-TESTED (steps 1-4 of the test plan below)

Written and reviewed against the real source of both repos (kernel schema, `init.mjs`,
template files, `check_logbook.mjs`'s `KINDS`/`REQUIRED_BY_KIND`) — not guessed. Smoke
test run for real (not assumed) in the standalone repo before the absorption:

- `--print-checkpoint-demo` fixture generated and validated as `VALID_CHECKPOINT`.
- `bridge.py` ran against it: scaffolded a fresh doc-eco target (`--all`, 21 files),
  appended 3 `kind:"hypothesis"` lines to `logbook.jsonl`, appended 3 rows to
  `DECISIONS.md`'s `## Open` table — one per hypothesis card in the demo fixture.
- `check_logbook.mjs` reported `OK — every entry is well formed` for the result.
- Real output was inspected directly (not just exit codes) before trusting this.

Re-ran steps 1-4 from this new in-repo location with no `--uia-repo`/`--doc-eco-repo`
flags — the corrected default paths (see "What changed on absorption" below) resolve
correctly and produced the same result (3 hypothesis entries, 3 Open rows, `check_logbook.mjs`
clean).

**Not yet done:** step 5 (a real, non-demo UIA run).

## Status — 2026-08-01, ultracode scenario-testing + 5 fixes

An 11-agent ultracode Workflow ran 10 scenarios against `bridge.py` for real (crafted
mutations of the demo fixture, actual execution, not reasoning-only). Found and this
repo then fixed 5 issues, each re-verified by actually re-running the scenario that
found it:

1. **[MAJOR, fixed]** `append_decisions_open()` wrote hypothesis-card `mechanism`/`lane`
   text into a Markdown table cell without escaping `|` — a schema-valid card
   containing `|` corrupted the `DECISIONS.md` table's column count. Fixed with a
   `_escape_cell()` helper (`\|` and newline neutralization). Re-verified: an injected
   `|`/backtick mechanism string now produces a row with exactly 6 unescaped pipes
   (5 columns), matching the header, in every row.
2. **[MAJOR, fixed]** No idempotency/dedup guard — re-running the same UIA checkpoint
   against a target that already ingested it silently duplicated every logbook entry
   and DECISIONS.md row. Fixed by tracking `(checkpoint_ref, hypothesis_id)` pairs
   already present in `logbook.jsonl` (`already_ingested()`) and skipping cards already
   seen, with a `SKIPPED n hypothesis card(s) already ingested ...` message. Re-verified:
   running the same checkpoint twice against the same target now stays at 4 logbook
   lines / 3 DECISIONS.md rows (was 7/6 before the fix).
3. **[MAJOR, fixed]** `append_decisions_open()` inserted new rows immediately after the
   table header instead of after the last existing row, so a second batch's higher row
   numbers ended up listed above the first batch's — non-ascending order. Fixed by
   inserting after the last `|`-prefixed line in the table body instead of right after
   the header marker. Re-verified: two distinct 5-card checkpoints run sequentially
   against the same target now produce rows numbered 1-10 in strict ascending file
   order (was 6-10 above 1-5 before the fix, confirmed non-ascending at 60+60-card
   scale during the original scenario run).
4. **[MINOR, fixed]** `append_logbook()` ran before `append_decisions_open()` with no
   transaction, so a `DECISIONS.md` header-drift failure left `logbook.jsonl` already
   written — an inconsistent partial-failure state. Fixed by swapping the order
   (`DECISIONS.md` written first). Re-verified: against a target with a deliberately
   corrupted `DECISIONS.md` header, a failed run now leaves both `logbook.jsonl`
   (line count) and `DECISIONS.md` (md5) byte-for-byte unchanged.
5. **[MINOR, fixed]** `json.loads()` on the run-record file had no error handling, so
   malformed JSON surfaced as a raw 5-frame Python traceback. Fixed with a
   `try/except json.JSONDecodeError`/`FileNotFoundError` around the load, producing a
   `REFUSED: <path> is not valid JSON: <reason>` message instead. Re-verified: a
   non-JSON input file now produces that one-line message, exit code 1, no traceback,
   no target directory created.

All 5 fixes re-verified together against the unmodified baseline scenario too (still
22-file scaffold, 3 hypothesis entries, 3 DECISIONS.md rows, `check_logbook.mjs` clean)
— no regression from the fixes.

## Status — 2026-08-01, 5-domain real-usage simulation + 6 development items

A second ultracode Workflow (not adversarial this time — genuine real-usage
simulation) built and validated a REAL, non-demo UIA checkpoint from scratch for
each of 5 domains (healthcare, fintech, manufacturing/IoT, edtech, customer-support
SaaS), ran each through `bridge.py`, and reported friction points. All 5 domains
reached `VALID_CHECKPOINT` (avg. 0.8 validate-fix iterations) and all 5 `bridge.py`
runs succeeded — this also finally executes test-plan step 5 ("a real, non-demo UIA
run"). Findings led to 6 development items, all implemented and re-verified here
(positive AND negative-control tests, plus the repo's own `pytest tests/`, all
passing):

1. **`bridge.py`** — "Who decides" in `DECISIONS.md` now prefers the run's
   `agency.decision_owners` (real, checkpoint-validated data) over the previous
   binary `legal_relevance` switch. **Correction (independent review, 2026-08-01):**
   the kernel's own `validate()` already requires `agency.decision_owners` to be a
   non-empty list for any `VALID_CHECKPOINT` (`AGENCY_ROLE_EMPTY:decision_owners`
   otherwise) — so through the real CLI path (`main()` refuses anything but
   `VALID_CHECKPOINT` before `append_decisions_open()` ever runs), the old
   `legal_relevance` switch is dead code, not a live fallback. It only remains
   reachable if `append_decisions_open()` is called directly as a library
   function, bypassing `main()`'s validation gate.
2. **`bridge.py`** — new `--seed-docs` flag drafts `GOAL.md`/`SPEC.md`/`PLAN.md`
   sections from already-validated checkpoint fields (`registration.query`,
   `issue.requested_readout`, `retained_difference.baseline`, the hypothesis
   portfolio), clearly labeled `## AI-drafted starting point`, idempotent (skips a
   file that already carries the marker).
3. **`bridge.py`** — a freshly-scaffolded target's `README.md`/`DECISIONS.md`
   title now uses `metadata.fixture_id` or `registration.query` instead of the
   raw target-directory basename, via exact-line-match replacement (never touches
   an already-scaffolded target or unrelated body text).
4. **`uia_protocol_kernel.py`** — a new `hypothesis_evidence_challenge.review_mode`
   value `"INTERNAL_DATA_AUDIT"` swaps each citation card's required fields from
   the literature-citation vocabulary (`authors_or_issuer`, `journal_or_repository`,
   `persistent_id_or_official_url`) to an internal-system vocabulary
   (`source_system`, `query_or_filter`, `record_id_or_url`) for domains whose real
   evidence is operational logs, not published sources. All other rigor
   (falsifier, `source_classes_searched` >= 2, `result_status`,
   `citation_audit == "PASS"`, the certainty/applicability enums) is unchanged.
   Any other `review_mode` value, including the pre-existing `"TARGETED_SEARCH"`,
   keeps the original literature schema — fully backward compatible (verified with
   a negative-control test: the same missing-literature-fields record still fails
   validation under `"TARGETED_SEARCH"`).
5. **`uia_protocol_kernel.py`** — a hypothesis card's `authority_assumptions` list
   may now be empty, but *only* when that same card has `legal_relevance: "NONE"`
   AND `legal_status: "NOT_REQUIRED"` (i.e. genuinely no authority/legal dimension,
   e.g. a purely mechanical hypothesis) — verified with a negative-control test:
   an empty list on a card with `legal_relevance != "NONE"` still fails validation.
   Every other hypothesis-card field is unaffected.
6. **`docs/FIELD_REFERENCE.md`** — generated by `tools/generate_field_reference.py`
   directly from the kernel's own `ENUMS`/`LANES`/`*_REQUIRED` constants (re-run
   the generator after any schema change; never hand-edit the doc), including an
   explicit note that `local_context_track`/`target_context` describe the real
   locale of the issue at hand, not a requirement for Thai language — the demo
   fixture's use of Thailand was locale color, not schema. A second built-in
   fixture, `--print-checkpoint-demo-2` (`fixtures/checkpoint_demo_alt_domain.json`,
   an industrial vibration-sensor false-alarm-rate issue), gives a non-booking,
   non-Thai starting template; genuinely validated (`VALID_CHECKPOINT`, zero
   errors), not hand-waved, and confirmed to flow end-to-end through `bridge.py`
   (including `--seed-docs` and the new "Who decides" lookup) in the same way the
   original demo fixture does.

## Status — 2026-08-01, ultracode weak-point scan + `attach_communication()` hardening

An ultracode scenario-testing run adversarially tested `attach_communication()`
(added earlier the same day) for real, alongside `communication_glossary/skill_plan.py`
— see that repo's README for the full 12-item fix list. The 5 findings that landed
in this file, each re-verified by actually re-running the scenario that found it:

- A directory at a known artifact filename (e.g. a folder literally named
  `skill_plan.md`) crashed with an unhandled `IsADirectoryError`, aborting the
  whole run mid-loop with no report of what had already been copied. Now
  skipped per-artifact with a reported reason; the run continues.
- A symlink at a known artifact filename was silently dereferenced and copied
  through regardless of where it pointed (could read outside `source_dir`).
  Now refused per-artifact with a reported reason, nothing copied through.
- Writes were non-atomic — a concurrent reader/writer against the same target
  could observe a half-written file. Fixed with write-to-temp-then-`os.replace()`.
- Neither `target` nor `target/communication` was checked for being a symlink
  before writing — could silently resolve a write outside the intended target
  tree. Both now refuse (`SystemExit`) if either is a symlink.
- `seed_docs()`'s `PLAN.md` section had the same unescaped-backtick markdown
  corruption bug found in `skill_plan.py` (a backtick in `hypothesis_id`/
  `claim` split the intended code span). `_escape_cell()` extended to also
  neutralize backticks and applied to the `PLAN.md` bullet line.

`attach_communication()` now returns `{"attached": [...], "skipped": [(name,
reason), ...]}` instead of a bare list — `main()`'s call site updated to print
each skip reason. Re-verified end-to-end via the real CLI (`--seed-docs
--attach-communication` together against a harsh, deliberately backtick/pipe-
laden but still-`VALID_CHECKPOINT` fixture): all 4 artifacts attached, `PLAN.md`
renders clean escaped markdown, `pytest tests/ -q` (13/13) and
`uia_protocol_kernel.py --self-test` (14/14) both re-confirmed unaffected.

Not fixed / explicitly out of scope: full cross-process locking for concurrent
`bridge.py` invocations against the same target — atomic per-file writes close
the file-corruption risk found; a lock file would additionally serialize
concurrent *invocations* of the whole script, judged unnecessary complexity
for a local, single-operator CLI tool.

## Status — 2026-08-01, `--attach-communication` added

Added to connect `communication_glossary`'s full output (all 4 layers, once
`skill_plan.py` — see that repo's README — exists) into a doc-eco target as one
step, per the founder's explicit request to wire the two systems together.
Confirmed via real execution: content-identical copy into
`communication/`, idempotent re-run (no duplicate/corrupted files),
clean `REFUSED` message on a missing source directory, graceful 0-file no-op
on an empty/unrelated source directory. `pytest tests/ -q` (13/13) and
`uia_protocol_kernel.py --self-test` (14/14) both re-confirmed unaffected,
since this flag doesn't touch kernel/schema code.

## What changed on absorption

Moving `bridge.py` from a sibling folder (`ANSE.ASIA/uia-doc-ecosystem-bridge/`) to
`ANSE.ASIA/universal-issue-analysis/doc_ecosystem_bridge/` shifted its own directory
by one level, so the default path arguments were corrected:

- `--uia-repo` default: now `Path(__file__).resolve().parent.parent` (this repo's root,
  since the script itself lives one level inside it) — was previously
  `parent.parent / "universal-issue-analysis"` (a sibling-folder assumption that no
  longer holds).
- `--doc-eco-repo` default: now `Path(__file__).resolve().parent.parent.parent /
  "human-ai-doc-ecosystem"` (up to `ANSE.ASIA/`, then into the sibling doc-eco repo) —
  was previously `parent.parent / "human-ai-doc-ecosystem"`.

Everything else (`ensure_scaffold`, `append_logbook`, `append_decisions_open`,
`validate_checkpoint`) is unchanged from the smoke-tested version.

## What it does

1. Loads a UIA run record (JSON) and validates it with the real
   `uia_protocol_kernel.validate()` from this repo — refuses to proceed unless
   `protocol_status == "VALID_CHECKPOINT"`.
2. Scaffolds the target project with doc-eco's `init.mjs --all` if it isn't scaffolded
   yet (`init.mjs` itself never overwrites existing files, and neither does this script).
3. Appends one `{"kind":"hypothesis", ...}` line per hypothesis card to `logbook.jsonl`
   (append-only, per doc-eco's own axiom: written while working, not after).
4. Appends one row per hypothesis card to `DECISIONS.md`'s `## Open` table (append-only).
5. **Optionally** (`--attach-communication <dir>`), copies an already-built
   `communication_glossary` output set (`kg_raw_word.md`, `kg_expert_layer.md`,
   `glossary.md`, `skill_plan.md` — whichever of those 4 exist in the given
   directory) into the target project's `communication/` folder, unchanged,
   content-identical. Pure file copy — idempotent (re-running with the same
   source is a no-op if content is unchanged), refuses cleanly if the given
   directory doesn't exist, and is a graceful no-op (0 files attached) if none
   of the 4 known artifact filenames are present.
6. Whenever step 5 actually attaches at least one file, also appends one
   discoverable, idempotent pointer section (`## communication_glossary
   output`) to the target's `README.md` naming each attached file with what
   it is, so a human/AI opening the scaffold's own front door finds Layer 1's
   word graph and Layer 4's skill plan instead of only finding them by
   already knowing `communication/` exists — closing the gap where the two
   systems were connected by a file copy but not by any actual cross-reference.
7. **Optionally** (`--seed-sot-docs`), creates `target/sot/{rag,cite,eq}.md` —
   a source-of-truth document set for the hypothesis portfolio, separate from
   both doc-eco's own template (step 2, only ever fills in a file that
   already exists) and from `communication_glossary`'s output (steps 5-6):
   - `rag.md` — per-hypothesis readout of `sources_searched`/`result_status`
     (international + local tracks), declared `evidence_gaps`, and the named
     `next_discriminating_test`.
   - `cite.md` — per-hypothesis readout of `citation_cards` (title, issuer,
     year, quality/directness/context_fit, verification status), with an
     automatic warning section flagging any `SIMULATED_ONLY` citation as a
     synthetic fixture, not real evidence.
   - `eq.md` — verbatim readout of `claim`/`mechanism`/`predicted_readout`/
     `falsifier` per hypothesis plus the checkpoint's declared
     `success_rule`/`failure_rule`, for spotting explicit numeric thresholds.
   Every file ends with an explicit "human/AI to fill in — NOT auto-generated"
   placeholder section for real source/citation/equation recommendations —
   this script only ever reads what the checkpoint already recorded, the
   same mechanical-vs-interpretive discipline as `attach_communication()`
   above and `communication_glossary`'s own Layer 1/3 vs. Layer 2 split.
   Idempotent per file (a file already carrying its marker is left alone),
   and links itself from `target/README.md` the same way step 6 does.

## What it deliberately does NOT do

- Does not touch `GOAL.md`, `PLAN.md`, `AGENTS.md`, or `INTAKE.md` — doc-eco's own README
  says these must be filled "from what THIS project has encountered," by whoever did the
  encountering, not copied in by a script.
- Does not write an `ADR` — an ADR records a settled structural choice; a hypothesis is
  provisional until UIA phase 16 picks a lane. Writing one now would overclaim.
- Does not run any UIA phase past 12, and does not run doc-eco's checkers automatically
  (`node tools/check_logbook.mjs` etc. — run those yourself after).
- `--attach-communication` does not invoke `kg_extract.py` / `build_glossary.py` /
  `skill_plan.py` itself — it only copies files that already exist. Layer 2 of
  `communication_glossary` requires an `Agent`/WebSearch reasoning step this
  stdlib-only bridge script has no business performing; run the pipeline first,
  then attach its output.
- `--seed-sot-docs` never invents a recommended source, a real citation, or a
  formula — every non-readout section in `rag.md`/`cite.md`/`eq.md` is an
  explicit, empty "human/AI to fill in" placeholder. A stdlib-only script has
  no business fabricating domain judgment, same reasoning as `attach_communication()`
  above and `communication_glossary`'s Layer 1/3-vs-Layer-2 split.

## Usage

```bash
cd skillme/doc_ecosystem_bridge
python3 bridge.py <uia_run.json> <target_project_dir>
# --uia-repo and --doc-eco-repo default to this repo and the sibling
# ANSE.ASIA/human-ai-doc-ecosystem respectively; pass them explicitly to override.

# optionally, also attach a built communication_glossary output set:
python3 bridge.py <uia_run.json> <target_project_dir> \
  --attach-communication ../communication_glossary/examples/fintech

# optionally, also draft a source-of-truth doc set (rag.md/cite.md/eq.md):
python3 bridge.py <uia_run.json> <target_project_dir> --seed-sot-docs
```

## Test plan (re-run after absorption, before trusting the moved defaults)

1. `python3 ../uia_protocol_kernel.py --print-checkpoint-demo > <scratch>/demo_checkpoint.json`
   — the repo's own `[SimulatedData]`-labeled fixture, already known to validate as
   `VALID_CHECKPOINT` (per the repo's `--checkpoint-demo` self-test).
2. `python3 bridge.py <scratch>/demo_checkpoint.json <scratch>/bridge-smoke-test`
   (no `--uia-repo`/`--doc-eco-repo` flags — confirms the corrected defaults resolve).
3. Confirm: `<scratch>/bridge-smoke-test/AGENTS.md` etc. exist (full `--all` set),
   `logbook.jsonl` has one new `hypothesis` line per card in the demo fixture,
   `DECISIONS.md`'s Open table has one new row per card.
4. `node <scratch>/bridge-smoke-test/tools/check_logbook.mjs <scratch>/bridge-smoke-test/logbook.jsonl`
   — must report `OK — every entry is well formed` for the new lines (existing seed line
   from `init.mjs` is unrelated and may show as open loop, that's expected on a fresh scaffold).
5. Only after 1–4 pass with real (not assumed) output: try a real, non-demo UIA run.
