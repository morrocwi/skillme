# communication_glossary

A 4-layer pipeline that sits downstream of a SkillMe `VALID_CHECKPOINT` (this repo's
own hypothesis-portfolio output) and produces a shared vocabulary for anyone who
needs to discuss the issue — **anchored to the issue/domain itself, not to any one
stakeholder role** (founder's explicit correction, 2026-08-01: "ไม่ใช่เอาทางใดทางหนึ่ง
คือต้องผูกกับ issue และโดเมน ไม่ใช่ agency ใด agency หนึ่ง"). Example worked case:
if an engineer needs to discuss a gut-health issue with a nurse, this pipeline
should surface the shared vocabulary both of them need — not a vocabulary split by
"what the engineer already knows" vs "what the nurse already knows."

## 🗂️ Kanban readout — as-of `54946b4`, 2026-08-03

> **Readout, not truth.** This board is a snapshot at the commit above, hand-updated —
> not a live scoreboard. Every card carries an evidence tier, same discipline as the
> prose sections below: `[verified]` (real execution / tests passing) · `[Dr]`
> (narrative judgment or known limitation, not yet tested) · `[Open]` (blocked or
> unresolved). **Blocked** is reserved for items waiting on a founder decision — same
> meaning as `cpg`'s own 🔴 OPEN HUMAN-GATES — never a loose label for "hard."

**Done**

| card | tier | witness |
|---|---|---|
| Layer 1 `kg_extract.py` — zero-interpretation word/phrase graph | `[verified]` | real checkpoints, full test suite |
| Layer 2 expert-framework reasoning contract | `[Dr]` (Open-tier by design) | deliberately not a script — LLM reasoning procedure, see below |
| Layer 3 `build_glossary.py` bridge | `[verified]` | real checkpoints |
| Layer 4 `skill_plan.py` hypothesis-card generation | `[verified]` | 20 pytest functions, PR #11/#12 regressions covered |
| `run_pipeline.py` one-command orchestrator | `[verified]` | 3/4 worked examples + end-to-end `doc_ecosystem_bridge` run |
| `kg_accumulate.py` cross-checkpoint accumulation | `[verified]` | 11/11 new tests, idempotency asserted byte-for-byte, 140/140 suite |

**Blocked — waiting on founder scope decision**

| card | tier | blocked-by |
|---|---|---|
| `registration.principal_id` → kernel schema | `[Open]` | scope not yet confirmed (see Layer 1 extension section below) |
| per-`(principal_id, topic_tag)` file storage vs. a real index | `[Open]` | scope not yet confirmed |

**Backlog — known, not started**

| card | tier | note |
|---|---|---|
| Thai/CJK tokenizer under-segmentation in `kg_extract.py` | `[Dr]` | needs a `pythainlp` dependency decision |
| Layer 2 → Layer 3 prose-heading/`"Confidence: X"` substring matching | `[Dr]` | not yet stress-tested against phrasing deviation |
| `TYPE_ORDER` fixed 6-value allowlist, no fallback bucket | `[Dr]` | not triggered by any fixture so far |
| `## Domain(s) identified` parsed by `build_glossary.py` but never rendered | `[Dr]` | wire it in or drop the parsing |
| `docs/FIELD_REFERENCE.md` missing `international_track`/`local_context_track.result_status` contract | `[Dr]` | |
| cross-process locking for concurrent `bridge.py` invocations | `[Dr]` | accepted, documented limit since v0.5 |
| no real human-entered issue has run the pipeline end-to-end yet | `[Open]` | every worked example so far is AI-constructed |

**Retained progress** (`Done[verified]` − `Blocked`, not raw card count): **5 − 2 = 3** net
forward since the pipeline existed. The Backlog items are named honestly, not silently
deferred, but don't count toward this line until moved.

## The four layers

### Layer 1 — `kg_extract.py` (deterministic readout)

Takes a SkillMe checkpoint JSON and extracts a typed word/phrase graph
(`kg_raw_word.md`: a Mermaid DAG + word table) with **zero interpretation**. Every
node is a literal fact: "this word/phrase appeared in this exact schema field of
this exact hypothesis card." No LLM, no invented relations, no invented content —
per this workspace's readout-not-truth discipline, this layer must never be
presented as anything other than what it is: a readout.

```bash
python3 kg_extract.py <uia_checkpoint.json> <out_kg_raw_word.md>
```

Fields are extracted in one of two modes, chosen per-field (not guessed per-value):
- **"phrase"** — name-like list fields (role names, tool names, protocol/method
  names, e.g. `agency.decision_owners`, `system_graph.nodes`) are kept as ONE whole
  node each, never split into words.
- **"tokenize"** — free narrative text fields (`claim`, `mechanism`, `falsifier`)
  are split into individual words.

### Layer 2 — expert-framework reasoning (AI-interpretive, Open tier — NOT a script)

There is deliberately no `kg_expert_layer.py`. This layer is an LLM reasoning
procedure: given a checkpoint + its Layer-1 output, identify what real, NAMED
frameworks/methodologies/vocabulary a world-class expert in that issue's domain(s)
would bring — e.g. "if the problem is a business problem, you need to know things
like the Business Model Canvas, SWOT analysis" (founder's own example). This is
fundamentally an **interpretive judgment**, not a readout, and must be tagged as
such, distinguishably, everywhere it's used.

Run it as an `Agent`/subagent call (or any LLM call with WebSearch access) using
this exact prompt shape — the heading structure below is load-bearing, because
Layer 3's parser matches on it:

```
Read <checkpoint.json> and <kg_raw_word.md>. Identify 2-4 real domains this issue
belongs to. For each, name 3-6 REAL, NAMED frameworks/methodologies a world-class
expert would bring — be specific and grounded in what THIS checkpoint's hypotheses
actually propose, not generic filler. Use WebSearch for at least 2-3 claims you're
not fully certain about (verify a named standard is still current/correctly named,
or search for a more specific framework than whatever you'd guess from memory) —
do not fabricate specificity to look thorough. Report which claims were verified
by search vs. asserted from training knowledge; do not blur the distinction.

Write output to kg_expert_layer.md with this exact structure:

# kg_expert_layer — <checkpoint_certificate> (AI-INTERPRETIVE, OPEN TIER)

**This is NOT a readout.** ...(disclaimer that everything below is a judgment call,
not validated fact; tier Open until reviewed by an actual domain expert)...

## Domain(s) identified
...

## Relevant frameworks/methodologies per domain
- **Framework name.** Why it applies to THIS checkpoint specifically. Confidence:
  HIGH (well-established) / MEDIUM / VERIFIED-VIA-SEARCH.
...

## What I verified via WebSearch vs. asserted from training knowledge
...(explicit ledger: claim -> SEARCHED (source link) or ASSERTED (unverified))...

## Vocabulary this adds beyond kg_raw_word.md's raw extraction
...(terms NOT already literal words in the source text)...

## Open questions / where a human expert should override this
...
```

See `examples/fintech/kg_expert_layer.md` for a real, WebSearch-verified worked
example (payments/reconciliation issue — verified Saga pattern, event sourcing/
CQRS, Stripe idempotency-key mechanics, COSO framework via real searches, all with
source links, with the weakest claim explicitly flagged as such).

Two more worked examples, added specifically to test the founder's own framing
("if an engineer wants to discuss X with a Y, what does the engineer need to
know?") — cross-discipline issues where NONE of Layer 2's contributed vocabulary
overlaps with Layer 1's raw extraction, confirming the glossary genuinely bridges
two different professional vocabularies around one shared issue, not just one
side's:
- `examples/gut-health-nurse-triage/` — a symptom-tracker app's single "stomach
  issue" label vs. what clinical nursing triage actually needs; Layer 2 verified
  Rome IV criteria, NICE red-flag/alarm-symptom referral criteria, the Emergency
  Severity Index, and SNOMED CT via real searches.
- `examples/billing-engineer-accountant/` — a SaaS billing engine's revenue-
  timing bug vs. what monthly-close accounting actually needs; Layer 2 verified
  ASC 606 (including its specific contract-modification sub-rule for mid-cycle
  upgrades), deferred revenue as a balance-sheet liability, and the matching
  principle via real searches.

### Layer 3 — `build_glossary.py` (mechanical merge, issue-anchored)

Purely mechanical — no new LLM calls, no new WebSearch. Merges Layer 1 + Layer 2's
output per issue into one glossary, filtering Layer 2 down to only `HIGH` /
`VERIFIED-VIA-SEARCH` confidence items (MEDIUM/uncertain items are deliberately
excluded from the glossary itself — a communication glossary should lead with
what's actually solid). Separately isolates SkillMe-protocol-internal vocabulary (lane
names like `KNOWN_DIRECT`, causal_tier names like `MECHANISM_HYPOTHESIS`,
`review_mode` values) into an appendix — that's machinery of the SkillMe method itself,
not vocabulary an engineer or a nurse needs to discuss the actual issue.

```bash
python3 build_glossary.py <kg_raw_word.md> <kg_expert_layer.md> <out_glossary.md>
```

### Layer 4 — `skill_plan.py` (role/skill plan, `Dr` tier)

Answers the founder's follow-up request directly ("มนุษย์ต้องรู้คำศัพท์อะไรบ้างเพื่อ
สั่งเอไอ ตรวจอะไรบ้าง ต้องมีสกิลอะไรบ้าง ... ai-orchestrator, ai-doer, ai-auditor
ต้องติดตั้งสกิลอะไรบ้าง"): one markdown doc, per checkpoint, split into 4 roles —
**Human**, **AI-orchestrator**, **AI-doer**, **AI-auditor**.

- The Human section's "what to check" is **mechanical, not invented** — pulled
  straight from that checkpoint's own already-kernel-validated hypothesis-card
  fields (`falsifier`, `discriminating_information`, `uncertainties`,
  `alternative_explanations`), plus `agency.decision_owners` for who actually
  holds authority, plus Layer 2's own "Open questions" section for what a human
  must override (AI cannot answer).
- The 3 AI-role sections are **curated from real, already-installed workspace
  skills** (not invented names), mapped to what each role actually does — the
  orchestrator/doer/auditor split mirrors the maker-checker pattern this session
  used for every PR (independent reviewer agent, never self-approving). Also
  emits a `review_mode`-driven note (`TARGETED_SEARCH` / `INTERNAL_DATA_AUDIT` /
  `FIELD_OBSERVATION_LOG`) telling the doer/auditor what kind of evidence this
  specific checkpoint actually rests on.
- Whole document is tagged **`Dr` tier** (declared recommendation, same as
  Layer 2) with an explicit "Open questions / limitations" section admitting the
  AI-role skill lists are curated, not auto-detected, and not proven sufficient
  or optimal — a starting point for the human to confirm or correct, never a
  science claim.

```bash
python3 skill_plan.py <uia_checkpoint.json> <glossary.md> <kg_expert_layer.md> <out_skill_plan.md>
```

Ran against all 3 existing worked examples (`examples/fintech/`,
`examples/gut-health-nurse-triage/`, `examples/billing-engineer-accountant/`) —
each produces a real `skill_plan.md` with exactly the hypothesis cards that
checkpoint actually has (3 each), confirming Layer 4 reads real checkpoint
content rather than templating generic advice.

### Layer 1 extension — `kg_accumulate.py` (cross-checkpoint accumulation, built 2026-08-02)

Built from the design registered the same day (git history has the design-only commit before this
one). Grew out of a founder requirement (recorded in `SKILLME.md` §14's "Expertise-typed roles +
user-growth loop" entry): the user's accumulated vocabulary should be a real, growing word map
anchored in Layer 1's own graph, not an invented flat list living somewhere else. `kg_extract.py`
only ever sees one checkpoint at a time; `kg_accumulate.py` merges its word/phrase graph across as
many checkpoints as have been ingested so far, scoped to one `(principal_id, topic_tag)` pair.

```bash
python3 kg_accumulate.py <checkpoint.json> --principal-id <id> --topic-tag <tag> \
    [--accumulated-dir <dir>]   # default: communication_glossary/accumulated/
```

- **`--principal-id`/`--topic-tag` are required CLI arguments in this version** — the design's
  proposed `registration.principal_id` checkpoint field was **not** added to the kernel schema in
  this pass (scope not yet confirmed); the script works today by taking both explicitly, which also
  keeps it usable against every existing example checkpoint (none of which declare that field).
  Wiring an automatic default read from the checkpoint itself, once/if that field is scoped and
  added, is a follow-up, not done here.
- **No new node-ID scheme was needed**, confirmed by two independent PR reviews reading
  `kg_extract.py` directly: `mermaid_id(wtype, word)` already hashes only `(wtype, word)`, never
  the checkpoint, so the same word/phrase from two different checkpoints already collides to the
  identical node id. Accumulation is a **union by key** over each checkpoint's `word_index`,
  extending each node's `sources` list with `<checkpoint_certificate>:<original_source>` entries.
- **Idempotent** — mirrors `doc_ecosystem_bridge/bridge.py`'s `already_ingested()` pattern exactly:
  a checkpoint whose `checkpoint_certificate` is already recorded in the accumulated state is
  skipped (printed as `SKIPPED`, state file untouched, verified byte-for-byte in tests), not
  re-merged, on a repeat run.
- **Storage**: one JSON state file (`kg_accumulated.json`, the merge source of truth — a list of
  `[word, type, sources]` triples plus `ingested_checkpoints`) and one regenerated Markdown file
  (`kg_accumulated.md`, same Mermaid-DAG-plus-word-table shape as `kg_raw_word.md`) per
  `(principal_id, topic_tag)`, under `communication_glossary/accumulated/<principal_id>/<topic_tag>/`.
  File-based and human-readable, matching Layer 1's own zero-interpretation-readout ethos — no
  database.
- **"New vocabulary this checkpoint" is returned as a mechanical, not guessed, computation** — the
  set of `(word, type)` keys absent from the accumulated state *before* this checkpoint was merged
  in. This is the concrete signal the vocabulary contract in `SKILLME.md` §14 needs; nothing in this
  script decides whether the user actually *learned* a term — that stays the orchestrator's own
  Open/Dr-tier judgment, feeding the already-registered `evidence_for_level` field.
- 11 new tests (`tests/test_kg_accumulate.py`), all real invocations against this repo's actual
  example checkpoints, no mocking or synthetic fixtures: first-ingest, idempotent re-run (byte-for-
  byte state equality asserted), cross-checkpoint merge growing the total, per-principal/per-topic
  scope isolation, blank-principal/blank-topic/missing-file/invalid-JSON refusals, checkpoint-
  qualified source labeling, and Markdown ingested-checkpoint listing. `pytest` 140/140 (was 129).
  `protocol_version` unaffected (`0.4.10`) — new sibling script, kernel/schema untouched.

**Still not decided**: whether `registration.principal_id` gets added to the kernel schema (and if
so, whether it carries the same declaration-only caveat as `maker_principal_id`/`checker_principal_id`
— no identity infrastructure verifies it, same as MC-02's existing scope note), and whether per-file
storage is sufficient long-term or should later be promoted into a real index. Scope for those two
questions must still be clarified with the founder before either lands.

## Status — 2026-08-01, v0.7 — one-command orchestrator + automated test coverage

Founder request: "เชื่อมเลยให้พร้อมเป็นสถาปัตสกิลระดับโลก ultracode" — close the two
readiness gaps named in an honest self-assessment given the same session: no single
command to run the pipeline, and zero automated test coverage for `skill_plan.py`
(two independent reviewer agents, PR #11 and PR #12, had each separately flagged
the missing-tests gap as a real risk).

- **`run_pipeline.py`** (repo root) — a thin one-command orchestrator. Shells out to
  `kg_extract.py` / `build_glossary.py` / `skill_plan.py` / `doc_ecosystem_bridge/bridge.py`
  as subprocesses; reimplements none of their logic (each script stays the single source
  of truth for its own layer). Layer 2 still cannot be scripted (Agent+WebSearch
  reasoning) — `--kg-expert-layer <file>` accepts an already-authored one, `--skip-layer2`
  writes an honestly-labeled stub (never silently treated as real enrichment), and giving
  neither refuses with a pointer to this README's Layer 2 prompt template. Validates the
  checkpoint itself first, before spawning any subprocess. Confirmed via real execution
  against 3 of the 4 worked examples plus an end-to-end run with `--doc-eco-target`
  against the real `human-ai-doc-ecosystem` sibling repo (README pointer, logbook, and
  DECISIONS.md rows all produced correctly in one command).
- **`tests/test_skill_plan.py`** — 20 real pytest functions, added because none existed.
  Covers every bug a prior ultracode scan + 2 independent reviews found and fixed (PR
  #11/#12) as a regression test, not just the happy path: the `extract_open_questions()`
  decoy-heading precedence fix, `_md_escape()`'s backtick neutralization, all 3
  `review_mode` values plus "unrecognized" vs. "entirely missing" (two textually distinct
  messages, asserted not to collapse), `hypothesis_cards`-as-dict / non-dict-element
  guards, the zero-hypothesis-cards fallback line, and the kernel-validation refusal path
  (both library-level and real CLI subprocess). An independent ultracode verify pass
  confirmed these aren't tautological by reverting 2 of the real fixes in a scratch copy
  and confirming the corresponding tests actually fail against the reverted code.
- **`tests/test_bridge.py`** — 23 real pytest functions covering `attach_communication()`
  (directory-at-filename skip, symlink-skip without following it, no stray temp files,
  target/dest_dir-symlink refusal, missing/empty source dir, overwrite-on-change),
  `link_communication_in_readme()` (idempotency, no-README no-op, empty-attached no-op,
  no corruption of existing content), `_escape_cell()`, `seed_docs()`'s backtick
  escaping, and `validate_checkpoint()`. Tests needing the real doc-eco sibling repo are
  `pytest.mark.skipif`-guarded on `node` + the repo actually being present, and ran for
  real (not skipped) in this environment. One MINOR gap the independent verify pass found
  — the directory-skip test didn't isolate the dedicated guard it was meant to
  regression-test, since a surrounding exception handler coincidentally produced a
  similar-looking message — was fixed (exact-string assertion instead of a loose
  substring match) and re-confirmed to actually fail against a reverted scratch copy.
- Full regression: `pytest tests/ -q` → 56 passed (43 new + 13 pre-existing);
  `uia_protocol_kernel.py --self-test` → 14/14. `README.md`/`llms.txt` updated (the "3-layer"
  wording left over from before Layer 4 existed is now fixed to "4-layer" everywhere it
  was found), and the plugin's `SKILL.md` gained a short section pointing an AI assistant
  at this downstream pipeline + `run_pipeline.py` after reaching `STOP_AT_HYPOTHESIS`.

Not fixed / explicitly out of scope for this pass (named honestly, not silently deferred):
Thai/CJK tokenizer under-segmentation in `kg_extract.py` (would need a new `pythainlp`
dependency — a real design decision for the founder, not something to add silently);
cross-process locking for concurrent `bridge.py` invocations (already an accepted,
documented limit from the v0.5 pass); every worked example so far, including this pass's
own test fixtures, is still AI-constructed — no real human-entered issue has run through
this system end-to-end yet.

## Status — 2026-08-01, v0.4, post-ultracode-review fixes

Built and iterated across this session via 3 ultracode Workflow runs (adversarial
harsh-content stress test on `kg_extract.py`, a 5-domain real-usage simulation for
the expert layer, and a full-pipeline cold-start review across 5 dimensions:
end-to-end execution on a brand-new issue, adversarial code review of both scripts,
architecture/tier-consistency review, and repo-state sanity check).

**Confirmed via real execution** (not assumed): full pipeline runs cold, end-to-end,
on a genuinely new issue on the first attempt (validated demonstrated with a retail
inventory/phantom-stockout checkpoint never seen by any of these scripts before).

**v0.4 fixes** (found by the full-pipeline review, each re-verified by constructing
an adversarial fixture and re-running for real):
1. **Mermaid card/bucket node-IDs were unsanitized** (`f"CARD_{cid}"` used the raw
   hypothesis_id directly, unlike word nodes which already went through a
   collision-safe hash). A harsh `hypothesis_id` (e.g. one that's a literal prefix
   of another node's name, like `H1_ROLE`) could silently merge two distinct DAG
   subtrees into one, or break Mermaid syntax outright. Fixed: every node id in
   `kg_extract.py` now goes through the same `safe_node_id()` hashing helper.
2. **The word table had no backtick-escaping** — a harsh word/phrase containing a
   literal backtick would terminate its Markdown code span early, silently
   misaligning the row (this is the same failure class `doc_ecosystem_bridge`'s
   `bridge.py` hit and fixed with `_escape_cell()` — the lesson hadn't carried over
   to this sibling script). Fixed with `md_code_span()` (CommonMark-correct
   variable-length backtick fence); `build_glossary.py`'s `ROW_RE` parser updated
   to match the new fence format.
3. **`as_phrase(None)` fabricated a literal `"None"` node** — a list field
   containing an explicit `null` entry (e.g. `affected_agencies: ["customer", null]`)
   produced a fake node, directly contradicting the script's own no-invented-content
   promise. Fixed: `None` now stays `None` and is skipped.

**Known limitations, stated not hidden** (from the same review, not yet fixed —
tracked here for the next iteration, not silently deferred):
- Thai/CJK unspaced running text under-tokenizes in "tokenize" mode fields (needs a
  real segmenter, e.g. `pythainlp` — out of scope for a stdlib-only script).
- The Layer 2 -> Layer 3 bridge is pure prose-heading + `"Confidence: X"`
  substring matching, with no structured format enforcing it — a phrasing
  deviation (e.g. `confidence: high` lowercase, or a missing colon) could silently
  drop a framework from the glossary with no error raised. Not yet stress-tested.
- The SkillMe checkpoint validator (`skillme_protocol_kernel.py`) checks structural
  completeness only, not factual accuracy — a `VALID_CHECKPOINT` can contain a
  wrong citation author/DOI (confirmed: happened for real during the
  full-pipeline test, caught only by the separate Layer-2 WebSearch step, not by
  validation).
- `TYPE_ORDER` in both scripts is a fixed 6-value allowlist (ROLE/CONCEPT/PROCESS/
  TOOL/PROTOCOL/METRIC) with no fallback bucket or warning for any other word type
  — not triggered by any real fixture tested so far, but silent if it ever is.
- `build_glossary.py` parses `## Domain(s) identified` from Layer 2 but never
  renders it into the output glossary — either wire it in or drop the parsing.
- No single orchestrating command runs all 3 layers — a user needs to know each
  script's CLI signature. `docs/FIELD_REFERENCE.md` (repo root) also doesn't yet
  document the `international_track`/`local_context_track.result_status` contract;
  a first-time user has to read `skillme_protocol_kernel.py` source directly for that.

**Cross-discipline confirmation (2026-08-01):** two more worked examples were run
end-to-end specifically to test the founder's original framing directly — "if an
engineer wants to discuss X with a Y, what does the engineer need to know?" — with
a genuinely different pair of disciplines each time, both reaching `VALID_CHECKPOINT`
on the first construction attempt and producing a glossary whose entire Layer-2
contribution had zero literal overlap with Layer 1's raw extraction (confirmed via
each example's own "Vocabulary this adds" section): `examples/gut-health-nurse-triage/`
(engineering ↔ clinical nursing) and `examples/billing-engineer-accountant/`
(engineering ↔ accounting). See the Layer 3 section above for what each verified.

## Status — 2026-08-01, v0.6 — ultracode weak-point scan + 9 fixes

A 5-scenario + 2-code-review ultracode Workflow (real execution, not
reasoning-only) stress-tested `skill_plan.py` and `bridge.py`'s
`attach_communication()`. 22 candidate findings were each independently
re-verified by a fresh agent (all 22 confirmed real). Fixed here, each
re-verified by actually re-running the scenario that found it:

1. **[CRITICAL, fixed]** `skill_plan.py` had no `uia_protocol_kernel.validate()`
   guard at all — unlike `bridge.py`, it would happily produce a confident-
   looking `skill_plan.md` from a checkpoint the kernel actually rejects.
   Ported `bridge.py`'s `validate_checkpoint()` pattern; `main()` now refuses
   with the same `REFUSED:` message shape.
2. **[CRITICAL, fixed]** `hypothesis_cards` was used raw, without the module's
   own `as_list()` guard — a dict (or any non-list) would raise `AttributeError`.
   Fixed with `as_list()` + a per-card `isinstance(card, dict)` skip.
3. **[MAJOR, fixed]** A literal backtick in `hypothesis_id`/`claim`/`falsifier`
   corrupted the bold+code-span markdown wrapping (in both `skill_plan.py` and
   `doc_ecosystem_bridge/bridge.py`'s `seed_docs()` — same defect class in two
   files). Fixed with a `_md_escape()` helper (backtick -> apostrophe);
   `bridge.py`'s existing `_escape_cell()` extended the same way and reused.
4. **[MAJOR, fixed]** `extract_open_questions()` matched an exact literal
   heading string — any real-world heading-wording drift silently dropped
   real open-questions content (silent-wrong, not a crash). Loosened to match
   any `## Open questions` prefix, case-insensitive.
5. **[MAJOR, fixed]** List-join calls (`"; ".join(...)`) assumed list-of-strings;
   a non-string element raised `TypeError`. Fixed by coercing every element
   through `_md_escape()` (which also `str()`-coerces) before joining.
6. **[MAJOR, fixed]** The "สิ่งที่ต้องตรวจ" header rendered unconditionally even
   with zero hypothesis cards, producing a misleadingly empty checklist. Now
   gated on `if checks:` with an explicit "no hypothesis_cards" fallback line.
7. **[MAJOR, fixed]** A checkpoint missing `hypothesis_evidence_challenge`
   entirely silently defaulted to `review_mode = TARGETED_SEARCH`'s confident
   note. Now routes through the same "not recognized, verify manually" branch,
   with a specific "field is entirely missing" message.
8. **[MAJOR, fixed]** `bridge.py`'s `attach_communication()` crashed with an
   unhandled `IsADirectoryError` if a source-dir entry was a directory rather
   than a file, aborting the whole run mid-loop. Now skips with a reported
   reason per artifact instead of crashing.
9. **[MAJOR, fixed]** A symlink at a known artifact filename (e.g.
   `glossary.md`) was silently dereferenced and copied through, regardless of
   where it pointed. Now refused per-artifact with a reported reason, nothing
   copied through.
10. **[MAJOR, fixed]** Non-atomic writes in `attach_communication()` could let
    a concurrent invocation observe a half-written file. Fixed with
    write-to-temp-then-`os.replace()` (atomic within `dest_dir`).
11. **[MAJOR, fixed]** `dest_dir`/`target` were used without checking for a
    symlink, which could resolve a write outside the intended target tree.
    Both now refuse (`SystemExit`) if either is a symlink.
12. **Doc bug (unrelated to the scan, self-caught while regenerating
    examples):** the README's own `skill_plan.py` usage line said
    `<kg_raw_word.md>` for argument 2, but the script's actual signature
    (and its own `usage:` string) takes `<glossary.md>` — the arg2 file is
    used to extract the glossary title via `extract_glossary_title()`. All 3
    committed example outputs had silently been generated with the wrong
    file and showed `unknown-checkpoint` as the title; regenerated with the
    correct arg, now showing each real `checkpoint_certificate` id.

Not fixed / explicitly out of scope: full cross-process locking for
concurrent `bridge.py` invocations against the same target (atomic per-file
writes close the corruption risk found; a lock file would additionally
serialize concurrent *invocations*, judged unnecessary complexity for a
local, single-operator CLI tool — revisit if that assumption stops holding).

## Status — 2026-08-01, v0.5 — Layer 4 (`skill_plan.py`) added

Added in direct response to the founder's follow-up request to build the
"expert declaration" role/skill plan now (registered as a roadmap pointer in
`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md` §14 the same day, then scoped and built
same-session). New file `skill_plan.py`; new outputs
`examples/*/skill_plan.md` (one per existing worked example). One self-caught
formatting bug fixed before commit: the `review_mode` note was originally
appended as a plain bullet under the AI-doer skill list, visually indistinguishable
from a real skill name — moved to its own labeled paragraph under both AI-doer
and AI-auditor sections. Also wired into `doc_ecosystem_bridge` via its new
`--attach-communication` flag (see that repo's README) so a full
`kg_raw_word.md` / `kg_expert_layer.md` / `glossary.md` / `skill_plan.md` set
can be attached to a `human-ai-doc-ecosystem` project as one step.

## Prior status — 2026-08-01, v0.1 -> v0.3 (kg_extract.py only, pre-repo)

Iterated in scratchpad across 2 earlier ultracode Workflow runs before this repo
commit: v0.1's naive per-word tokenization shredded role/tool/protocol names (e.g.
"product owner" -> `product` + `owner` separately) — fixed in v0.2 with the
phrase/tokenize mode split above. v0.3 fixed a CRITICAL Mermaid-label-injection
bug (unescaped `"`/`[`/`]` from harsh content corrupting the diagram) plus digit-
swallowing in the tokenizer, duplicate ROLE/TOOL entity filing, and missing
citation-title extraction — all found by a 5-domain harsh-content stress test and
re-verified against real adversarial checkpoints.
