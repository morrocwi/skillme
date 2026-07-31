# universal-issue-analysis (Claude Code plugin)

This is the installable plugin subtree for **Universal Issue Analysis (UIA)** — a
philosophy-first protocol for analyzing any reported issue (software incident, complaint,
conflict, policy question, research anomaly, everyday decision) as a finite, auditable
retained difference instead of a guessed name, cause, or fix.

`git-subdir` plugin installs only pull this directory, so it carries its own `LICENSE` and this
short README. It does **not** carry the canonical spec (`UNIVERSAL_ISSUE_ANALYSIS_v0.4.6.md`)
or the standalone Python protocol kernel (`uia_protocol_kernel.py`) — those live in the repo
root at <https://github.com/morrocwi/universal-issue-analysis>. Clone the full repo if you need
the full spec text or want to run the kernel's self-test yourself.

What you get from installing this plugin: the `universal-issue-analysis` skill
([`skills/universal-issue-analysis/SKILL.md`](skills/universal-issue-analysis/SKILL.md)) — a
self-contained operational summary an AI assistant loads before analyzing a reported issue.

**Tier: `Dr` (design rationale)** — an architectural synthesis of established methods, not a
proven result. See the full repo's README for the complete tier-honesty statement.

Developed by Yaoharee Lahtee. MIT licensed — see [`LICENSE`](LICENSE).
