<div align="center">

# skillme

### SkillMe protocol

**A finite issue never gets named before it's found.** _by Yaoharee Lahtee_

[![tier](https://img.shields.io/badge/claim%20tier-Dr%20(design%20rationale)-orange)](#tier-honesty)
[![kernel](https://img.shields.io/badge/kernel-stdlib--only%2C%20run%20it%20yourself-brightgreen)](skillme_protocol_kernel.py)
[![self--test](https://img.shields.io/badge/self--test-14%2F14%20PASS-brightgreen)](tests/test_kernel_self_test.py)
[![pytest](https://img.shields.io/badge/pytest-13%2F13%20PASS-brightgreen)](tests/test_kernel_self_test.py)
[![version](https://img.shields.io/badge/protocol-v0.4.8-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

</div>

## What this is

SkillMe is a **philosophy-first protocol** for analyzing any reported issue — a software incident,
a customer complaint, an organizational conflict, a policy question, a research anomaly, or an
everyday decision — without smuggling in a name, a cause, or a fix before there's a finite,
auditable basis for one.

It does this with a small number of hard commitments:

- **Issue is not a name.** It's a *retained difference* that, under a declared agency, context,
  and query, changes what some agency can do, know, claim, or be responsible for.
- **Zero ≠ unresolved.** "No relevant difference found under this operator" and "the evidence
  cannot decide yet" are structurally different states — the protocol will not let you collapse
  one into the other.
- **Stakeholder ≠ agency.** Being affected by a decision and having power over it are tracked
  separately, on purpose, so the people who bear a cost but have no voice don't disappear from
  the analysis.
- **A cause needs a falsifier, not just a story.** Every hypothesis is put through a
  bidirectional (support **and** challenge) evidence search, split into a global track and a
  local-context track, before it's allowed anywhere near a candidate solution.
- **Three genuinely different candidates, or an honest partial.** Known-Direct,
  Cross-Adaptive, and Generative-Transformative — a search duty, not license to fabricate a
  third option to hit the count.

This repository packages the standalone spec plus a stdlib-only Python kernel that validates
**protocol structure** — as an installable Claude Code skill, so an AI assistant can load the
discipline before it analyzes your next incident.

## Tier honesty

> **This project is `Dr` — design rationale — not `Th_coqc` or `exact`.**

The spec is an original architectural synthesis of well-established methods (root-cause
analysis, FMEA/DMAIC, stakeholder mapping, GRADE-style evidence grading, PRISMA-style search
transparency, systems thinking, decision analysis) held together by one shared contract. It has
**no proofs, no field trials, and no independent domain evaluation** behind it yet. The kernel
in this repo checks that a *record of a run* is internally consistent and complete against the
spec's schema and gates — it does **not** verify that any issue, cause, or fix reported through
the protocol is actually true. See spec §0, §13 ("What is original in this synthesis") and §9
of this README for exactly what is and isn't checked. Do not cite this repo as proof that a SkillMe
run's conclusions are correct — only that the run followed the protocol's structure.

This stance is deliberate and matches the sibling projects
[`information-discrete-math`](https://github.com/morrocwi/information-discrete-math) and
`readout_genesis`: a claim is only as strong as its weakest load-bearing link, and it is
labeled honestly rather than rounded up.

## Quickstart — as a Claude Code skill

```
/plugin marketplace add morrocwi/skillme
/plugin install skillme@yaoharee-lahtee-skillme
```

Once installed, an AI assistant loads the `skillme` skill before analyzing a
reported issue — see
[`plugins/skillme/skills/skillme/SKILL.md`](plugins/skillme/skills/skillme/SKILL.md)
for the operational summary it follows (the two-question intake gate, the agency/stakeholder
map, the evidence-challenge protocol, the three-lane candidate generator, and the 48 hard
invariants it will not violate). **Note:** `git-subdir` plugin installs only pull
`plugins/skillme/` — the canonical spec and the standalone kernel below are
not installed with the skill; the SKILL.md is self-contained on its own, but running the
kernel or reading the full spec text requires cloning this repo.

## Quickstart — the kernel, standalone

Clone the full repo first — the kernel and spec are repo-root files, not part of the installed
plugin subtree above. No dependencies beyond the Python standard library.

```bash
python3 skillme_protocol_kernel.py --self-test          # 14 structural test cases, run them yourself
python3 skillme_protocol_kernel.py --print-demo          # a full, valid, [SimulatedData]-labeled run
python3 skillme_protocol_kernel.py --demo                # validate that demo run -> VALID
python3 skillme_protocol_kernel.py --print-checkpoint-demo  # the same run, stopped at hypothesis
python3 skillme_protocol_kernel.py --checkpoint-demo     # validate the checkpoint -> VALID_CHECKPOINT
python3 skillme_protocol_kernel.py my_run.json           # validate your own run record
python3 -m pytest tests/ -q                          # pytest wrapper around the above
```

Every fixture in the demo is explicitly labeled `[SimulatedData]` — the protocol forbids
reporting simulated evidence as field evidence (spec §0, invariant list §11).

## The protocol at a glance

| Phase | What happens | What the user sees |
|---|---|---|
| 0 | Two-question intake gate (mandatory, asked together) | "Issue คืออะไร?" + "มีข้อเสนอไหม?" |
| 1 | Protect — minimal, reversible containment only if there's ongoing harm | what must stop/be protected right now |
| 2–4 | Read philosophically, map agencies (10 discovery scans), compile perspectives | who's affected, involved, or missing a voice |
| 5–8 | Admit the issue, detect domain/topology, route adapters, execute, integrate | issue status in plain language |
| 9–10 | Compile the retained-difference model into a claim/warrant graph | mechanism vs. hypothesis vs. unknown |
| 11 | **Hypothesis Evidence Challenge** — global + local, support + challenge, citation-audited | evidence for/against each hypothesis |
| 12 | Certify the **three-lane hypothesis portfolio**; optional `STOP_AT_HYPOTHESIS` checkpoint | hypotheses + legal/representation status |
| 13–16 | Generate & audit **three-lane candidates**, decide | genuinely different options, with trade-offs |
| 17–19 | Act, verify, correct | what was tried, what it showed, what changes next |

Full phase-by-phase detail, all symbol definitions, and the 48 protocol invariants are in
[`SKILLME.md`](SKILLME.md) — this README is an
entry point, not a replacement for it.

## Repository map

```
skillme/
├── SKILLME.md   canonical spec — normative source of truth
├── skillme_protocol_kernel.py                stdlib-only protocol-structure validator + fixtures
├── docs/FIELD_REFERENCE.md               generated field-by-field reference (tools/generate_field_reference.py)
├── fixtures/checkpoint_demo_alt_domain.json  a second, non-booking-app checkpoint fixture
├── tools/generate_field_reference.py     regenerates docs/FIELD_REFERENCE.md from the kernel's own constants
├── tests/                                 pytest: kernel self-test + skill_plan.py/bridge.py coverage
├── run_pipeline.py                       one-command orchestrator over the 4-layer pipeline below
├── doc_ecosystem_bridge/                 bridges a VALID_CHECKPOINT into a human-ai-doc-ecosystem project
│   └── README.md                          bridge.py usage, design rationale, status history
├── communication_glossary/               4-layer pipeline: checkpoint -> issue-anchored shared vocabulary + skill plan
│   └── README.md                          Layer 1-4 design, worked examples in examples/
├── AI_START_HERE.md                      discovery order for AI assistants / reviewers
├── llms.txt                              machine-readable doc index
├── CHANGELOG.md                          version history through v0.4.8
├── plugins/skillme/                      the installable Claude Code plugin (self-contained subtree)
│   ├── README.md, LICENSE                 plugin-scoped copies (git-subdir installs pull only this dir)
│   ├── .claude-plugin/plugin.json         plugin manifest
│   └── skills/skillme/SKILL.md           operational summary the AI loads
└── .claude-plugin/marketplace.json       marketplace listing (yaoharee-lahtee-skillme)
```

## Downstream tooling built on a checkpoint

Two subsystems consume a `VALID_CHECKPOINT` run record and are not part of the core protocol
kernel — both are `Dr` tier or lighter, both link back to the spec, and neither is installed by
the Claude Code plugin above (clone the repo to use them):

- **[`doc_ecosystem_bridge/`](doc_ecosystem_bridge/)** — takes a checkpoint at Phase 12
  (`STOP_AT_HYPOTHESIS`) and scaffolds/updates a
  [`human-ai-doc-ecosystem`](https://github.com/morrocwi/human-ai-doc-ecosystem) project: logs
  each hypothesis card as a `logbook.jsonl` entry, adds an open question per hypothesis to
  `DECISIONS.md`, and (with `--seed-docs`) drafts `GOAL.md`/`SPEC.md`/`PLAN.md` sections from
  already-validated checkpoint fields, clearly labeled as an AI draft.
- **[`communication_glossary/`](communication_glossary/)** — a 4-layer pipeline that turns a
  checkpoint into a shared vocabulary for anyone discussing the issue, **anchored to the issue
  itself, not to any one stakeholder's background** (e.g. what does an engineer need to know to
  discuss a symptom-tracker bug with clinical nursing triage, or a billing bug with an
  accountant): Layer 1 (`kg_extract.py`) is a deterministic word/phrase graph; Layer 2 is an
  AI-interpretive, WebSearch-verified "what named expert frameworks apply" step (documented
  procedure, not a script); Layer 3 (`build_glossary.py`) mechanically merges both, keeping only
  high-confidence Layer 2 claims; Layer 4 (`skill_plan.py`) turns the checkpoint into a `Dr`-tier
  role/skill plan (Human / AI-orchestrator / AI-doer / AI-auditor). See its README for the full
  tier discipline and 3 worked examples (fintech, healthcare↔nursing, billing↔accounting).
- **[`run_pipeline.py`](run_pipeline.py)** — a one-command orchestrator over both subsystems
  above (it shells out to each script, reimplementing none of their logic): `python3
  run_pipeline.py <checkpoint.json> --out-dir <dir> --kg-expert-layer <file>
  [--doc-eco-target <dir>]`. Layer 2 still requires a real Agent/WebSearch call first (or pass
  `--skip-layer2` for an honestly-labeled stub) — this script cannot and does not fake it.

## What the kernel actually checks (and doesn't)

`skillme_protocol_kernel.py` (~2,100 lines, stdlib only) implements `validate(run: dict) -> dict`
against the schema and enums defined in the spec. It checks, among other things:

- the two-question intake gate was actually satisfied before analysis fields are trusted;
- emergency-containment bypasses stayed inside their scope (no cause/decision smuggled in);
- every hypothesis has a falsifier, an evidence-ledger reference, both an international and a
  local-context evidence track, and citation cards with independently-flagged
  `metadata_verification` / `scope_verification`;
- the three-lane hypothesis portfolio and candidate portfolio don't have duplicate mechanisms
  masquerading as "diverse" options;
- a run cannot close while its stakeholder map is still `OPEN`/`UNRESOLVED` or its translation
  lost information (`loss_audit != PASS`);
- old/renamed enum aliases (e.g. `HYBRID_BLIND`) are rejected, not silently accepted;
- citation cards adapt to 3 evidence vocabularies via `review_mode` — literature
  (`TARGETED_SEARCH`, the default), internal system-of-record data
  (`INTERNAL_DATA_AUDIT`, e.g. logs/tickets/sensor exports), or fresh field/sensory observation
  (`FIELD_OBSERVATION_LOG`, e.g. a baker's dough, a tagged tree at a census date) — same rigor
  (falsifier, source classes, `citation_audit`) in all three, only the citable-source vocabulary
  changes. See [`docs/FIELD_REFERENCE.md`](docs/FIELD_REFERENCE.md) for the exact field sets.
- only 5 of `agency`'s 13 list-type fields are actually required non-empty
  (`affected`/`observers`/`decision_owners`/`intervention_owners`/`accountable_parties`) — the
  other 8 (voice/veto/oversight/represented/resource/knowledge/future/power-gap roles) may stay
  `[]` for a small, direct-actor issue with no distinct party in that role. This was already true
  before it was documented — see `docs/FIELD_REFERENCE.md`'s agency section.

It does **not** check whether the reported issue is real, whether a cited source actually says
what it's claimed to say (only that a `scope_verification` flag was declared), whether a
proposed mechanism is the true cause, or whether an intervention will work. Structural validity
is necessary, not sufficient — see [Tier honesty](#tier-honesty) above.

## Attribution

SkillMe — the thesis, the entity definitions (retained difference, agency,
issue, problem, cause), the axioms, and the full 20-phase protocol — is Yaoharee Lahtee's work,
building on the Readout Genesis / Information Discrete Mathematics foundation from the same
author. This repository's packaging (marketplace listing, SKILL.md operational summary, README,
pytest wrapper) was assembled with AI assistance from the standalone spec and kernel the author
had already written; the AI did not originate the protocol's ideas.

## License

MIT — see [`LICENSE`](LICENSE).
