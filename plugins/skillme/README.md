# skillme (Claude Code plugin)

This is the installable plugin subtree for **SkillMe** — a
philosophy-first protocol for analyzing any reported issue (software incident, complaint,
conflict, policy question, research anomaly, everyday decision) as a finite, auditable
retained difference instead of a guessed name, cause, or fix.

`git-subdir` plugin installs only pull this directory, so it carries its own `LICENSE` and this
short README. It does **not** carry the canonical spec (`SKILLME.md`)
or the standalone Python protocol kernel (`skillme_protocol_kernel.py`) — those live in the repo
root at <https://github.com/morrocwi/skillme>. Clone the full repo if you need
the full spec text or want to run the kernel's self-test yourself.

What you get from installing this plugin: the `skillme` skill
([`skills/skillme/SKILL.md`](skills/skillme/SKILL.md)) — a
self-contained operational summary an AI assistant loads before analyzing a reported issue —
plus the companion `system-engineering-dag` skill
([`skills/system-engineering-dag/SKILL.md`](skills/system-engineering-dag/SKILL.md)) for
production-grade software/system engineering work. The plugin also includes a bundled
fail-closed `Stop` hook (`hooks/hooks.json` + `scripts/`) that activates automatically once
this plugin is installed, no per-project settings.json edit needed. It only fires for sessions
that actually invoke the `skillme` skill: it checks that `TaskCreate` was used to track the
run's phases and, if a checkpoint reached `VALID_CHECKPOINT`, that
`doc_ecosystem_bridge/bridge.py` was actually run against it, before letting the turn end.

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
3. The engineering skill maps the issue into architecture impact, data/DB/cache/security
   consequences, failure modes, test selection, migration/compatibility, backup/restore/DR,
   rollback versus roll-forward, CI/CD, progressive release, observability/SRE, incident
   response, and the learning loop back to SkillMe.
4. For Git work, preserve **Issue → branch → tests/checker → PR → required review → merge →
   progressive release → production verification**. Never edit `main` directly.

A GitHub Issue is a work/traceability container, not proof of root cause. Passing architecture
or test gates likewise does not promote a SkillMe hypothesis into fact.

**Tier: `Dr` (design rationale)** — an architectural synthesis of established methods, not a
proven result. See the full repo's README for the complete tier-honesty statement.

Developed by Yaoharee Lahtee. MIT licensed — see [`LICENSE`](LICENSE).