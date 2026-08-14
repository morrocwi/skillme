# skillme (Claude Code plugin)

This is the installable plugin subtree for **SkillMe** — a philosophy-first protocol for
analyzing any reported issue (software incident, complaint, conflict, policy question,
research anomaly, everyday decision) as a finite, auditable retained difference instead of a
guessed name, cause, or fix.

`git-subdir` plugin installs only pull this directory, so it carries its own `LICENSE` and this
short README. It does **not** carry the canonical root spec (`SKILLME.md`) or the standalone
root Python protocol kernel (`skillme_protocol_kernel.py`) — those live in the repo root at
<https://github.com/morrocwi/skillme>. Clone the full repo if you need the full root spec or
want to run its self-test.

What you get from installing this plugin:

- `skillme` — the issue-analysis protocol in
  [`skills/skillme/SKILL.md`](skills/skillme/SKILL.md).
- `system-engineering-dag` — the risk-proportional software/system engineering companion in
  [`skills/system-engineering-dag/SKILL.md`](skills/system-engineering-dag/SKILL.md).
- The engineering companion ships its own machine source of truth
  (`system_engineering_dag.json`), stdlib-only validator/obligation compiler
  (`system_engineering_dag_kernel.py`), and deep on-demand reference (`REFERENCE.md`).
- A bundled fail-closed `Stop` hook (`hooks/hooks.json` + `scripts/`) for the SkillMe run
  tracking rules already documented in the main skill.

## Mandatory routing for software/system Issues

When a reported Issue, bug, incident, anomaly, risk, or complaint concerns software, web,
application/API behavior, data/database/schema, cache, search, knowledge graph, AI,
security/privacy/IAM, network, infrastructure, reliability, performance, deployment,
backup/restore, disaster recovery, or production operations:

1. **Invoke `skillme` first.** Preserve its Q1/Q2 intake, retained-difference framing,
   stakeholder/agency mapping, issue-admission state, hypothesis/evidence challenge, rights
   gate, and `VALID_CHECKPOINT` semantics.
2. After domain/topology detection, **MUST invoke `system-engineering-dag` before proposing or
   implementing any architecture-impacting fix.** Reuse the same SkillMe lineage/checkpoint;
   do not silently restart the issue analysis.
3. The engineering adapter emits a typed handoff, classifies risk (`L0_TRIVIAL` →
   `L3_CRITICAL`), marks surfaces `AFFECTED | NOT_AFFECTED | UNKNOWN`, and derives tests,
   migration, security, recovery, and release obligations from actual impact. A typo does not
   run the same ceremony as a destructive database migration.
4. Investigation and intervention are separate modes: temporary instrumentation may gather
   evidence without claiming a fix; emergency changes may bypass normal sequence only while
   retaining traceability, owner, minimum test, containment/rollback, evidence preservation,
   and post-hoc review.
5. High-complexity architecture choices such as sharding, microservices, multi-region, KG, and
   vector retrieval have machine-readable `activate_if` and `forbid_if` conditions. Security
   assurance is likewise tiered (`BASELINE`, `SENSITIVE`, `HIGH_ASSURANCE`).
6. For Git work, preserve **Issue → branch → tests/checker → PR → required review → merge →
   release strategy → production verification**. Never edit `main` directly.

A GitHub Issue is the active work-item adapter for this repository, not proof of root cause.
Passing architecture or test gates likewise does not promote a SkillMe hypothesis into fact.

## Machine verification

From the repository root:

```bash
python3 plugins/skillme/skills/system-engineering-dag/system_engineering_dag_kernel.py
python3 plugins/skillme/skills/system-engineering-dag/system_engineering_dag_kernel.py --self-test
python3 -m pytest -q tests/test_system_engineering_dag_skill.py
```

The engineering kernel verifies graph structure and behavioral protocol invariants — node
uniqueness, dependency existence, acyclicity, required release ancestry, typed SkillMe handoff,
risk routing, impact-derived obligations, critical unknown blocking, time-bounded waivers,
destructive-change recovery paths, decision-rule shape, security-assurance tiers, and release
evidence requirements. It does **not** verify that a domain hypothesis or chosen engineering
intervention is true.

**Tier: `Dr` (design rationale)** — an architectural synthesis of established methods, not a
proven result. See the full repo's README for the complete tier-honesty statement.

Developed by Yaoharee Lahtee. MIT licensed — see [`LICENSE`](LICENSE).
