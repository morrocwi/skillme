#!/usr/bin/env bash
# Stop: the actual fail-closed gate. Only fires a block if this session
# invoked the skillme skill AND is missing one of the two concrete,
# hook-observed signals: TaskCreate usage, or bridge.py after a checkpoint.
# Blocking returns control to the assistant (not a hard session stop) with
# a reason string -- once it acts and the next Stop fires, the gate re-checks
# and passes through cleanly.
set -euo pipefail

input="$(cat)"
session_id="$(jq -r '.session_id // "unknown"' <<<"$input")"

state_dir="${TMPDIR:-/tmp}/skillme-hook-state"
state_file="$state_dir/$session_id.json"
[[ -f "$state_file" ]] || exit 0

active="$(jq -r '.skillme_active // false' "$state_file")"
[[ "$active" == "true" ]] || exit 0

task_created="$(jq -r '.task_created // false' "$state_file")"
checkpoint="$(jq -r '.checkpoint_reached // false' "$state_file")"
doc_eco="$(jq -r '.doc_eco_done // false' "$state_file")"

missing=""
if [[ "$task_created" != "true" ]]; then
  missing="${missing}TaskCreate was never called this session to track the UIA phases. "
fi
if [[ "$checkpoint" == "true" && "$doc_eco" != "true" ]]; then
  missing="${missing}A hypothesis portfolio reached VALID_CHECKPOINT but doc_ecosystem_bridge/bridge.py was never run against it. "
fi

if [[ -n "$missing" ]]; then
  reason="skillme session gate: ${missing}Address this before ending the turn -- see the skillme SKILL.md operational contract."
  jq -n --arg reason "$reason" '{"decision":"block","reason":$reason}'
  exit 0
fi

exit 0
