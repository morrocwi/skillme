#!/usr/bin/env bash
# TaskCreated: proof the assistant's own todolist was actually used this
# session. Only meaningful once skillme_active is set by on-skill-invoke.sh;
# a no-op state file (not skillme_active) still records it harmlessly.
set -euo pipefail

input="$(cat)"
session_id="$(jq -r '.session_id // "unknown"' <<<"$input")"

state_dir="${TMPDIR:-/tmp}/skillme-hook-state"
mkdir -p "$state_dir"
state_file="$state_dir/$session_id.json"
[[ -f "$state_file" ]] || echo '{}' > "$state_file"

tmp="$(mktemp)"
jq '.task_created = true' "$state_file" > "$tmp" && mv "$tmp" "$state_file"
exit 0
