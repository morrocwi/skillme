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
plus a bundled fail-closed `Stop` hook (`hooks/hooks.json` + `scripts/`) that activates
automatically once this plugin is installed, no per-project settings.json edit needed. It only
fires for sessions that actually invoke this skill: it checks that `TaskCreate` was used to
track the run's phases and, if a checkpoint reached `VALID_CHECKPOINT`, that
`doc_ecosystem_bridge/bridge.py` was actually run against it, before letting the turn end.

**Tier: `Dr` (design rationale)** — an architectural synthesis of established methods, not a
proven result. See the full repo's README for the complete tier-honesty statement.

Developed by Yaoharee Lahtee. MIT licensed — see [`LICENSE`](LICENSE).
