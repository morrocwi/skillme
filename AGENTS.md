# AGENTS.md - skillme

## What this repository is

SkillMe is a philosophy-first protocol for analyzing any reported issue - a software incident, a
customer complaint, an organizational conflict, a policy question, a research anomaly, or an
everyday decision - without smuggling in a name, a cause, or a fix before there is a finite,
auditable basis for one. This repository packages the standalone spec plus a stdlib-only Python
kernel that validates protocol structure, as an installable Claude Code skill.
Tier honesty, as the README and `llms.txt` state it: this project is `Dr` (design rationale), not `Th_coqc` or
`exact`; it has no proofs, no field trials, and no independent domain evaluation behind it yet. The
kernel checks that a record of a run is internally consistent and complete against the spec's schema
and gates; it does not verify that any issue, cause, or fix reported through the protocol is
actually true. Do not infer this project's maturity from the spec's length.

## Read first

The first three steps of the discovery order in `AI_START_HERE.md` (which continues with the kernel
self-test, `tests/`, `docs/FIELD_REFERENCE.md` and `CHANGELOG.md`), then the doc index:

1. `README.md` - framing, tier-honesty statement, quickstart, repo map.
2. `plugins/skillme/skills/skillme/SKILL.md` - the operational summary an AI assistant loads and follows.
3. `SKILLME.md` - the canonical, normative spec.
4. `llms.txt` - machine-readable doc index.

## Rules

These are rules the repository already states; this file adds none of its own.

- Every SkillMe run opens with exactly two questions, asked together, before any analysis starts
  (the two-question intake gate in `SKILL.md`). The only exception `SKILL.md` allows is an
  emergency containment bypass: minimal, reversible, recorded containment of ongoing harm, with no
  cause, fix or decision concluded under it. Never add a third mandatory intake question.
- Run `python3 skillme_protocol_kernel.py --self-test` yourself before repeating any pass/fail
  claim about the kernel.
- Treat `protocol_status: VALID` as "well-formed", not "correct".

## Programme map

This repository is one node of the Human-AI Readout Programme. Which repository answers which kind of
question, what to read first and which gate applies is kept in one place, the routing hub:
<https://github.com/morrocwi/main.hub> (start at its `AGENTS.md`, then `ROUTES.md`).
The hub holds pointers and pinned links only. It is a readout of one moment: when the hub and this
repository disagree, this repository wins.
