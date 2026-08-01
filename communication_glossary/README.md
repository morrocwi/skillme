# communication_glossary

A 3-layer pipeline that sits downstream of a UIA `VALID_CHECKPOINT` (this repo's
own hypothesis-portfolio output) and produces a shared vocabulary for anyone who
needs to discuss the issue — **anchored to the issue/domain itself, not to any one
stakeholder role** (founder's explicit correction, 2026-08-01: "ไม่ใช่เอาทางใดทางหนึ่ง
คือต้องผูกกับ issue และโดเมน ไม่ใช่ agency ใด agency หนึ่ง"). Example worked case:
if an engineer needs to discuss a gut-health issue with a nurse, this pipeline
should surface the shared vocabulary both of them need — not a vocabulary split by
"what the engineer already knows" vs "what the nurse already knows."

## The three layers

### Layer 1 — `kg_extract.py` (deterministic readout)

Takes a UIA checkpoint JSON and extracts a typed word/phrase graph
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

### Layer 3 — `build_glossary.py` (mechanical merge, issue-anchored)

Purely mechanical — no new LLM calls, no new WebSearch. Merges Layer 1 + Layer 2's
output per issue into one glossary, filtering Layer 2 down to only `HIGH` /
`VERIFIED-VIA-SEARCH` confidence items (MEDIUM/uncertain items are deliberately
excluded from the glossary itself — a communication glossary should lead with
what's actually solid). Separately isolates UIA-protocol-internal vocabulary (lane
names like `KNOWN_DIRECT`, causal_tier names like `MECHANISM_HYPOTHESIS`,
`review_mode` values) into an appendix — that's machinery of the UIA method itself,
not vocabulary an engineer or a nurse needs to discuss the actual issue.

```bash
python3 build_glossary.py <kg_raw_word.md> <kg_expert_layer.md> <out_glossary.md>
```

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
- The UIA checkpoint validator (`uia_protocol_kernel.py`) checks structural
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
  a first-time user has to read `uia_protocol_kernel.py` source directly for that.

## Prior status — 2026-08-01, v0.1 -> v0.3 (kg_extract.py only, pre-repo)

Iterated in scratchpad across 2 earlier ultracode Workflow runs before this repo
commit: v0.1's naive per-word tokenization shredded role/tool/protocol names (e.g.
"product owner" -> `product` + `owner` separately) — fixed in v0.2 with the
phrase/tokenize mode split above. v0.3 fixed a CRITICAL Mermaid-label-injection
bug (unescaped `"`/`[`/`]` from harsh content corrupting the diagram) plus digit-
swallowing in the tokenizer, duplicate ROLE/TOOL entity filing, and missing
citation-title extraction — all found by a 5-domain harsh-content stress test and
re-verified against real adversarial checkpoints.
