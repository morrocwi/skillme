---
name: skillme
description: >
  Load before analyzing any reported issue, incident, complaint, conflict, risk, anomaly,
  policy question, or "what should we do about X" decision — software bugs, customer
  complaints, organizational conflicts, research anomalies, social/policy issues, and
  everyday decisions all qualify. Gives the SkillMe protocol: a
  mandatory two-question intake gate before any analysis starts, retained-difference issue
  framing (an issue is not a name, it is a difference that survives under a declared
  agency/context/query), a stakeholder-agency map that separates who is affected from who
  holds power, a bidirectional global+local evidence-challenge for every causal hypothesis,
  and a three-lane (Known-Direct / Cross-Adaptive / Generative-Transformative) solution
  candidate generator with rights and diversity gates. Use it whenever you are about to say
  "the root cause is X", "the fix is Y", jump straight to a solution, or aggregate
  stakeholder opinions into one verdict.
---

# SkillMe — readout-first issue analysis protocol

**Developed by Yaoharee Lahtee.** SkillMe is a philosophy-first protocol for turning a reported
issue into a finite, auditable analysis instead of a guessed answer. It is built on the same
readout-first foundation as `information-discrete-math` and `readout_genesis`: everything you
can act on is a **finite retained difference**, not the world itself.

**Tier: `Dr` (design rationale)** — this is an architectural synthesis of established methods
(RCA, FMEA, stakeholder mapping, GRADE, PRISMA, systems thinking, decision analysis), not a
proven theorem. The bundled kernel (`skillme_protocol_kernel.py`) only verifies **protocol
structure** (required fields, enum validity, cross-references, gate order) — it does **not**
verify that any domain claim, cause, or fix is actually true. Say so when you report results.

This file is a self-contained operational summary shipped with the plugin. The canonical spec
(`SKILLME.md`) and the standalone protocol kernel
(`skillme_protocol_kernel.py`) live in the full repo root — they are **not** installed with this
plugin (a plugin install only pulls this `plugins/skillme/` subtree). Clone
the whole repo if you need the full spec text or want to run the kernel yourself:
`https://github.com/morrocwi/skillme`. Read the full spec before disputing an
edge case or extending the protocol — this summary is not a substitute for it.

## The one commitment

> Issue = a **retained difference** that, under a declared agency, context, and query,
> changes what some agency can do, know, claim, be responsible for, or redirect.

Not "issue = what's wrong" and not "issue = what the loudest stakeholder feels". Zero and
unresolved are different things: **`0` = no relevant difference found under this operator;
`⊥` = the tool/evidence/resolution cannot decide yet.** Never report one as the other.

## Before you start analyzing anything: the Two-Question Intake Gate

Every SkillMe run opens with exactly two questions, asked together, before any translation,
stakeholder mapping, causal analysis, or candidate generation happens:

1. **Q1 — Issue:** "Issue คืออะไร? กรุณาอธิบายสิ่งที่เกิดขึ้นหรือประเด็นที่ต้องการให้วิเคราะห์" /
   "What is the issue? Describe what happened or what needs analysis."
2. **Q2 — User proposal:** "คุณมีข้อเสนอหรือแนวคิดเกี่ยวกับประเด็นนี้ไหม? หากไม่มี ตอบว่า 'ไม่มี' ได้" /
   "Do you have a proposal or idea about this? If not, you can answer 'none'."

Rules:
- Q1 must be non-blank. Q2 **must be answered**, but "none" / "ไม่มี" / "skip" is a complete,
  valid answer (`PROPOSAL_ABSENT_DECLARED`) — never a missing value, never silently inferred
  from silence.
- The only exception is an **emergency containment bypass**: if there's ongoing harm, you may
  do the minimum reversible containment action (stop, isolate, preserve evidence) with a
  recorded `reason/scope/rights_check/owner/stop_rule/rollback_rule/evidence_preservation/
  review_due_at` — but you may NOT conclude a cause, pick a fix, or make a decision under this
  bypass. After containment, go back to waiting for Q1/Q2.
- Never add a third mandatory intake question before analysis is allowed to start.

Once both are answered: if Q2 has content, mode defaults to `HYBRID_BLIND_COMPARE` (AI
generates candidates blind, then compares against the user's proposal); if Q2 declares
absence, mode is `AI_INDEPENDENT`.

## Core moves, in order

1. **Protect** — only if there's ongoing harm; minimal, reversible, no causal claims.
2. **Read philosophically** — separate: what difference is retained, from what state, under
   what context/query/resolution. Ask only for what's missing.
3. **Map agencies** — don't start from the meeting attendee list. Run all 10 discovery scans
   (named / impact / dependency / rights / power / knowledge / representation / horizon /
   adversarial / boundary) and stop expanding only when new agencies stop changing the query,
   rights gate, graph, or intervention. Distinguish 12 agency roles (affected, observing,
   knowledge, voice, decision, intervention, resource, veto, accountable, oversight,
   represented, future/latent) — **stakeholder ≠ agency**: someone can be affected with zero
   voice, or have decision power with zero exposure.
4. **Compile perspectives** — keep a dissent ledger; never silently pick the powerful party's
   framing as "the overview".
5. **Admit the issue** — `ISSUE_ADMITTED` / `NO_ISSUE_UNDER_DECLARED_READOUT` / `UNRESOLVED`,
   never fudge zero vs. unresolved.
6. **Detect domain + topology**, route to adapters (RCA/FMEA/DMAIC/stakeholder-map/DAG/
   systems-dynamics/MCDA/etc. — see full spec §6.10 for the registry) without letting an
   adapter promote its own evidence tier.
7. **Generate competing hypotheses**, then run the **Hypothesis Evidence Challenge**: for
   every load-bearing hypothesis, search *and* record both support and challenge queries, in
   both an international track and a local-context track (for Thailand: ThaiJO, TNRR,
   government open data, Thai + English terms). Citations need separate
   `metadata_verification` and `scope_verification` — matching metadata is not the same as the
   source actually supporting the claim. Never write `LOCAL_EVIDENCE_NOT_FOUND` as
   `NO_LOCAL_EVIDENCE_EXISTS`. Never count citations as a vote — quality, directness, and
   context-fit decide, not `#support − #challenge`.
8. **Certify the hypothesis portfolio** (checkpoint) — three lanes
   (Known-Direct / Cross-Adaptive / Generative-Transformative), each with a mechanism,
   falsifier, legal-relevance annotation, and representation-lineage record (direct voice /
   authorized proxy / inferred-only / absent-or-unreached — never let power speak for an
   absent party without flagging it). You may **stop here** (`STOP_AT_HYPOTHESIS`) without
   having made any decision, intervention, or field-truth claim — this is a valid, resumable
   checkpoint, not an incomplete run.
9. **Generate candidates** — three lanes again, genuinely different (not the same fix under
   three names): Known-Direct (proven method in-domain), Cross-Adaptive (borrowed mechanism
   from another domain), Generative-Transformative (new hypothesis / redesign). If you can
   only find one or two admissible lanes, say `CANDIDATE_SET_PARTIAL_1/2` — do not fabricate
   a third to hit the count.
10. **Decide / Act / Verify / Correct** — freeze the decision criteria before you see the
    outcome (maker-checker firewall), state stop/rollback rules, and treat correction/
    withdrawal as a sign of reliability, not failure.

## Hard invariants (do not violate — see full spec §11 for all 48)

- Never let authority substitute for evidence, or correlation substitute for
  intervention-supported cause.
- Never let a stakeholder-utility score override a rights gate.
- Never call consultation "co-decision" when participants can't actually change the outcome.
- Never resume a `STOP_AT_HYPOTHESIS` checkpoint by silently starting a new lineage — reuse
  `continuation_record`, open a correction record if anything changed.
- Never treat `VALID_CHECKPOINT` as a decision, success, or closure — it's a resumable pause.

## Output shape (what the human should see, plain language, in this order)

Intake confirmation → issue in plain language → who's affected/involved (including the
voiceless) → immediate containment if any → what's confirmed vs. hypothesis vs. unknown →
evidence for/against each hypothesis (global + local) → the user's proposal and what happened
to it → three-lane candidates with trade-offs → recommended first (smallest reversible) test →
who decides/acts/checks → how you'll know it worked → what would make you revise this.

Internal SkillMe vocabulary (`retained difference`, `agency readout`, `quotient`) stays in the
technical/audit trail — don't force the user to learn it unless they ask.

## Downstream: turning a checkpoint into shared vocabulary + a project doc trail

Reaching `STOP_AT_HYPOTHESIS` (a `VALID_CHECKPOINT`) is not the end of what this repo can do
with it. Two downstream tools (full repo only, not in this plugin subtree — clone the repo)
turn a checkpoint into artifacts the people in step 3's agency map actually need:

- **`communication_glossary/`** — a 4-layer pipeline that turns one checkpoint into a shared
  vocabulary for anyone discussing the issue, anchored to the issue/domain itself, not to any
  one stakeholder's prior knowledge. Layer 1 (`kg_extract.py`) is a deterministic word-graph
  readout; Layer 2 is an AI-interpretive expert-framework reasoning step (Agent + WebSearch,
  deliberately not a script — see that folder's README for the exact prompt template); Layer 3
  (`build_glossary.py`) mechanically merges the two into an issue-anchored glossary; Layer 4
  (`skill_plan.py`) turns the checkpoint into a `Dr`-tier role/skill plan split into Human /
  AI-orchestrator / AI-doer / AI-auditor — what vocabulary the human needs to command the work,
  what to verify before trusting AI output, and what skills each AI role needs.
- **`doc_ecosystem_bridge/bridge.py`** — bridges the checkpoint (and, optionally, the
  `communication_glossary` output above) into a `human-ai-doc-ecosystem` project: one
  `hypothesis`-kind logbook entry and one open `DECISIONS.md` row per hypothesis card — never
  an `ADR`, because a hypothesis isn't settled until phase 16 (`DECIDE`) picks a lane.
- **`run_pipeline.py`** (repo root) — a thin one-command orchestrator over all of the above. It
  shells out to each script rather than reimplementing any of their logic:
  ```
  python3 run_pipeline.py <checkpoint.json> --out-dir <dir> \
      --kg-expert-layer <already-authored kg_expert_layer.md> \
      [--doc-eco-target <dir> [--seed-docs]]
  ```
  Layer 2 still can't be scripted (it needs an actual Agent/WebSearch call) — author
  `kg_expert_layer.md` yourself first and pass it in, or pass `--skip-layer2` to get an
  honestly-labeled stub (clearly marked as unenriched, never silently treated as real Layer 2
  output) so you can still exercise Layers 1/3/4 without it.

## Verify before you claim

The kernel is not part of this plugin subtree — clone the full repo (see above) to run it.
`python3 skillme_protocol_kernel.py --self-test` runs 14 structural test cases (happy path +
violation cases) against the bundled reference implementation — stdlib-only, no network. Run
it yourself before repeating any pass/fail claim about the kernel; do not take this file's
prose on trust.
```
$ python3 skillme_protocol_kernel.py --self-test
{"status": "PASS", "passed": 14, "test_count": 14, ...}
```

## Session-tracking contract (enforced by a bundled hook, not just this prose)

Installing this plugin also installs a fail-closed `Stop` hook (`hooks/hooks.json`) that
checks, at the end of every turn where this skill was loaded:

1. **TaskCreate was actually called** to track the run's phases (intake, agency/stakeholder
   map, hypothesis evidence challenge, hypothesis portfolio) — not just this file's prose
   telling you to.
2. **If a run reached `VALID_CHECKPOINT`, `doc_ecosystem_bridge/bridge.py` was actually run**
   against it before the turn ends.

If either is missing, the hook blocks the turn end with a `reason` naming exactly what's
missing — act on it (call `TaskCreate`, run `bridge.py`) and the next `Stop` check passes
cleanly; it does not hard-stop the session. This is deliberate: the two soft instructions
above (use `TaskCreate`, run `bridge.py` at checkpoint) are advisory and can silently get
skipped under time pressure — the hook makes them structural instead. It only activates for
sessions that actually invoked this skill; it is a silent no-op for every other Bash/Skill/Stop
event in a project where the plugin happens to be installed.
