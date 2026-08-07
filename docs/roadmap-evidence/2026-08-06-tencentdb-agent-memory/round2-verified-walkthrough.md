# TencentDB-Agent-Memory synthesis — real-attachment-point walkthrough (round 2, text-only simulation)

## Item 1 — Defensive LLM-call parsing discipline

**Attachment point:** Conceptual seam only, no code today. Layer 2 ("expert layer") is a fixed prompt template in `communication_glossary/README.md` lines 87–124, run by a human/AI conversation — not by any script. `kg_expert_layer.py` does not exist. Confirmed by grep: zero `openai.*`/`anthropic.*`/`.messages.create`/model-endpoint calls anywhere in the repo.

**Before → after:** Before: a human/AI reads `checkpoint.json` + `kg_raw_word.md`, follows the prompt template, hand-writes `kg_expert_layer.md` (e.g. `communication_glossary/examples/fintech/kg_expert_layer.md`); `build_glossary.py` then mechanically parses that finished file (fence-strip + heading/bullet regex, lines 40–54 and 78–111, already tolerant of multi-line-wrapped bullets). After (if ever built): a new `kg_expert_layer.py` would need, on top of what exists nowhere today — (a) a pre-call injection/quality gate on untrusted checkpoint free-text, (b) an explicit context-size cap policy, (c) a hard post-hoc cap on domain/framework counts rather than trusting the prompt's self-limit, (d) the same fence-strip → regex-extract → sanitize → single-repair-retry discipline `build_glossary.py` already applies to Layer 1 output, and (e) an explicit `extraction_failed` vs `zero_found` status split grounded in the existing `SKILLME-A6` axiom (`SKILLME.md:504`, `0 ≠ ⊥`).

**Correction to draft_section.md item 1:** The "deliberately no `kg_expert_layer.py`" quote lives at `communication_glossary/README.md:79`, not the repo-root `README.md:79` (that line is unrelated, about plugin-install scope). Any draft citing the repo-root file for this quote is wrong.

**Still nothing built, still docs-only.** No wrapper script, no API call, no parser for Layer 2 exists anywhere in the repo.

---

## Item 2 — L1 pipeline instrumentation

**Attachment point:** `communication_glossary/kg_extract.py` (`main()` 369–381, `extract()` 190–255) and `communication_glossary/kg_accumulate.py` (`accumulate()` 186–249, `merge()` 103–119, `main()` 269–280) — both live-verified by re-running against the fintech fixture.

**Before → after:** Before: `kg_extract.py` emits a usage message + exit code 2 on bad args, and on success prints "wrote … 342 distinct words across 3 cards" plus a per-type breakdown (PROTOCOL:12 CONCEPT:143 PROCESS:104 METRIC:72 ROLE:7 TOOL:4) — all confirmed by live run. After (proposed, not implemented): new counters and a `telemetry_status` field emitted at the same print boundaries — a design proposal only, correctly framed as such in the source walkthrough.

**Correction to draft_section.md item 2:** None needed — every cited line number, field name, and runtime number was independently re-derived and matched exactly on re-verification.

**Still nothing built, still docs-only.** The instrumentation fields are proposed additions; current code has no `telemetry_status` or extended counters.

---

## Item 4 — Uniform response envelope reframe

**Attachment point:** `hypothesis_runner.py`, `main()` lines 318–336 (builds the 20-field `raw_result` record) and `hypothesis_checker.py` (`load_raw_result_or_refuse`, `re_derive_mechanical_result` lines 112–118, `main()`).

**Before → after:**
| Field | Before | After (proposed) |
|---|---|---|
| `scope` | absent | new structured field (`payload_ref`, `entrypoint`, `declared_inputs`, `sandbox{...}`) surfacing what `docker_command` (#16) already carries buried in an argv list |
| `status` | hardcoded literal `"PENDING_INDEPENDENT_CHECK"` (write-only; `hypothesis_checker.py` never reads it) | three-way enum `checked_found` / `checked_absent` / `not_yet_checked` |
| `tier` | hardcoded literal `"finite_diagnostic"` | same literal, but typed against the closed enum `{Th_coqc, exact, finite_diagnostic, Dr, Open}` (`SKILLME-A12`, `SKILLME.md:541` — verbatim match) |

Renaming `status` breaks nothing structurally — `hypothesis_checker.py`'s verdict logic runs entirely off `exit_code`/`expected_exit_status`, never off `record["status"]`. It does require updating `hypothesis_runner.py`'s own docstring (line 11, which names the old literal) and four test assertions (`test_hypothesis_runner.py:85,91,247`, `test_hypothesis_checker.py:57`).

**Correction to draft_section.md item 4:** Field count is **20, not 21** (13 `execution` keys + 7 record-literal keys — count against the code, table only lists 20). Also, `hypothesis_checker.py`'s docstring (lines 5–9) does **not** assert the record is tagged `PENDING_INDEPENDENT_CHECK` — it only says the runner never writes `status: APPROVED`; only `hypothesis_runner.py`'s own docstring (line 11) names that literal, so only that file's docstring goes stale on rename.

**New risk this walkthrough surfaced (not present in the original proposal):** naming the new values `checked_found`/`checked_absent` is itself an axiom risk — both are produced by the maker (`hypothesis_runner.py`) alone, before any independent check runs, so a name containing "checked" reads as an audited verdict when structurally it is not. This collides with `SKILLME-A4` (efficacy ≠ truth) and the maker-checker firewall `SKILLME-A10`. **Recommend the enum be renamed to avoid implying independent verification** (e.g. `maker_found`/`maker_absent`/`not_yet_run`) before this is registered — do not adopt `checked_found`/`checked_absent` as worded.

**Still nothing built, still docs-only.** The `scope` field and the status/tier enum retyping are proposals; current code emits only the hardcoded literals.

---

## Item 6 — Async job idempotent-create + status enum

**Attachment point:** `communication_glossary/kg_accumulate.py`, `checkpoint_certificate_of()` (lines 97–100) and the skip-check inside `accumulate()` (`if`/return at lines 209–219, preceded by extraction/state-load setup at lines 206–207).

**Before → after:** Before: `checkpoint_certificate_of()` pulls a bare string (`hypothesis_portfolio.checkpoint_certificate`) with no hash/format validation — confirmed non-hash-derived: `skillme_protocol_kernel.py:1222-1225` only checks non-blank, and real fixtures use human-assigned labels (`HYP-SKILLME-ALT-DEMO-001`, `HYP-SKILLME-046-DEMO-001`), not hash output. The skip-check is a synchronous Python list-membership test against `state["ingested_checkpoints"]`; on hit it returns `{"skipped": True, ...}` without calling `merge()` or writing any file — there is no "in-flight" state representable today, since the function call itself is the entire unit of work. After (proposed): a separate job-status record keyed by `(principal_id, topic_tag, checkpoint_certificate)`, living beside (not inside) `kg_accumulated.json`, cycling `pending → processing → ready/failed`, written by a job runner before/after calling `accumulate()`. `ready` maps onto today's existing `ingested_checkpoints` membership; `processing` is the state the current code has no vocabulary for at all; `failed` must not leave partial state misread as `ready`.

**Correction to draft_section.md item 6:** The claim that `checkpoint_certificate` "is presumed to already be a stable content-hash-derived certificate produced upstream" is unsupported and should be replaced with: *it is a non-blank identity string of unverified provenance/uniqueness — no code in the repo computes it via a hash function.*

**Still nothing built, still docs-only.** No job-status record, no queue, no worker exists; `accumulate()` remains fully synchronous.

---

## Item 10 — Discrete visibility enum on principal_id+topic_tag partition

**Attachment point:** `communication_glossary/kg_accumulate.py`, `state_dir()` (lines 55–56) plus `load_state()`'s default-state dict (lines 62–69) and `state_from_word_index()`'s constructed dict (lines 86–94).

**Before → after:** Before: `--principal-id`/`--topic-tag` are unvalidated `argparse` strings concatenated directly into a filesystem path (`accumulated/<principal_id>/<topic_tag>/`); no identity/ACL check exists anywhere in the file or in any file that touches this path — confirmed by grep across `build_glossary.py`, `skill_plan.py`, `hypothesis_runner.py`, `hypothesis_checker.py` (zero references) and `tests/test_kg_accumulate.py` (which does call `state_dir()` directly, at lines 108–110, but only to assert storage-scope isolation across three `(principal_id, topic_tag)` pairs, never to test access control). After (proposed): a `"visibility"` field (`"private" | "team" | "restricted_acl" | "agent_targeted"`) inserted into both dicts, plus a companion `visibility_acl`/`visibility_agents` list for the two ACL-bearing cases, threaded through via a new `--visibility` CLI arg. As pure JSON this is mechanically trivial to add — but it would be **inert data only**, exactly like `principal_id`/`topic_tag` are inert data today. No code path anywhere in this repo reads a field back and makes an allow/deny decision on it; enforcement would require a caller-identity concept (which does not exist in this repo at all) plus new gating code at every read/write/downstream-consumer point — none of which exists in any not-yet-wired-up form.

**Correction to draft_section.md item 10:** The claim "no other file in the repo references `kg_accumulate.py`, `state_dir`, or the `accumulated/` tree at all" is false — `tests/test_kg_accumulate.py` references all three extensively (10 tests calling `accumulate()`, one calling `state_dir()` directly). This does not change the substantive conclusion (storage-scope isolation is tested; access control is not), but the "zero references" sentence must be struck.

**This walkthrough surfaced a reason to flag, not reject, but register cautiously:** adding the enum without also building the enforcement layer would create a field that *looks* like a security control while doing nothing — a namer/reader mismatch risk similar to Item 4's. If registered, it should be registered explicitly as schema-only with a companion note that enforcement is unbuilt, per `SKILLME-A4`/`A6` (absence of readout ≠ absence of state; 0 ≠ ⊥) — not as a completed access-control feature.

**Still nothing built, still docs-only.** No `visibility` field, no identity/ACL check, no enforcement code exists anywhere in this repo today.