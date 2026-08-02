#!/usr/bin/env bash
# PostToolUse(Skill): marks this session as a skillme run and reminds the
# assistant of the todolist/doc-eco contract. Never blocks -- Stop enforces.
set -euo pipefail

input="$(cat)"
session_id="$(jq -r '.session_id // "unknown"' <<<"$input")"
skill_name="$(jq -r '.tool_input.skill // empty' <<<"$input")"

[[ "$skill_name" == "skillme" ]] || exit 0

state_dir="${TMPDIR:-/tmp}/skillme-hook-state"
mkdir -p "$state_dir"
state_file="$state_dir/$session_id.json"
[[ -f "$state_file" ]] || echo '{}' > "$state_file"

tmp="$(mktemp)"
jq '.skillme_active = true | .checkpoint_reached = false | .doc_eco_done = false' \
  "$state_file" > "$tmp" && mv "$tmp" "$state_file"

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "skillme was just loaded. Its operational contract for this session: (1) use TaskCreate to track each UIA phase (intake, agency/stakeholder map, hypothesis evidence challenge, hypothesis portfolio) as you go through it, not after the fact; (2) once a run reaches STOP_AT_HYPOTHESIS / VALID_CHECKPOINT, run doc_ecosystem_bridge/bridge.py against that checkpoint before ending the turn, so the analysis is bridged into the target project's doc ecosystem. A Stop hook will block the turn end and tell you exactly what's missing if either of these was skipped."
  }
}
EOF
exit 0
