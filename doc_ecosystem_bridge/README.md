# doc_ecosystem_bridge

Wires this repo (**universal-issue-analysis** / UIA) to Yaoharee Lahtee's
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

## What it deliberately does NOT do

- Does not touch `GOAL.md`, `PLAN.md`, `AGENTS.md`, or `INTAKE.md` — doc-eco's own README
  says these must be filled "from what THIS project has encountered," by whoever did the
  encountering, not copied in by a script.
- Does not write an `ADR` — an ADR records a settled structural choice; a hypothesis is
  provisional until UIA phase 16 picks a lane. Writing one now would overclaim.
- Does not run any UIA phase past 12, and does not run doc-eco's checkers automatically
  (`node tools/check_logbook.mjs` etc. — run those yourself after).

## Usage

```bash
cd universal-issue-analysis/doc_ecosystem_bridge
python3 bridge.py <uia_run.json> <target_project_dir>
# --uia-repo and --doc-eco-repo default to this repo and the sibling
# ANSE.ASIA/human-ai-doc-ecosystem respectively; pass them explicitly to override.
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
