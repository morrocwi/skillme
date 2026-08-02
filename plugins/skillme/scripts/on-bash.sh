#!/usr/bin/env bash
# PostToolUse(Bash): detects the two real, concrete signals the Stop gate
# cares about -- a checkpoint actually validating, and bridge.py actually
# running -- by matching on the commands the assistant really executes.
# Never blocks -- Stop enforces. Silently no-ops if state isn't active yet
# (this session never invoked the skillme skill), so it's a cheap no-op for
# every other Bash call in a session that isn't running skillme.
# tool_response shape confirmed via Claude Code docs: Bash returns an object
# with stdout/stderr/interrupted/isImage fields -- .stdout is the primary
# read; .stderr and a plain-string fallback are cheap defensive insurance.
set -uo pipefail

input="$(cat)"
session_id="$(jq -r '.session_id // "unknown"' <<<"$input" 2>/dev/null || echo unknown)"
command="$(jq -r '.tool_input.command // empty' <<<"$input" 2>/dev/null || echo "")"

state_dir="${TMPDIR:-/tmp}/skillme-hook-state"
state_file="$state_dir/$session_id.json"
[[ -f "$state_file" ]] || exit 0

active="$(jq -r '.skillme_active // false' "$state_file" 2>/dev/null || echo false)"
[[ "$active" == "true" ]] || exit 0

response_text="$(jq -r '
  if (.tool_response | type) == "string" then .tool_response
  else (.tool_response.stdout // "") + " " + (.tool_response.stderr // "") + " " + (.tool_response.output // "")
  end
' <<<"$input" 2>/dev/null || echo "")"

if [[ "$command" == *"skillme_protocol_kernel"* ]] && [[ "$response_text" == *"VALID_CHECKPOINT"* ]]; then
  tmp="$(mktemp)"
  jq '.checkpoint_reached = true' "$state_file" > "$tmp" && mv "$tmp" "$state_file"
fi

if [[ "$command" == *"doc_ecosystem_bridge/bridge.py"* ]] || [[ "$command" == *"doc_ecosystem_bridge"*"bridge.py"* ]]; then
  tmp="$(mktemp)"
  jq '.doc_eco_done = true' "$state_file" > "$tmp" && mv "$tmp" "$state_file"
fi

exit 0
