#!/usr/bin/env bash
# Stop: the actual fail-closed gate. Only fires a block if this session
# invoked the skillme skill AND is missing one of the two concrete,
# hook-observed signals: TaskCreate usage, or bridge.py after a checkpoint.
# Blocking returns control to the assistant (not a hard session stop) with
# a reason string -- once it acts and the next Stop fires, the gate re-checks
# and passes through cleanly.
set -uo pipefail

input="$(cat)"
session_id="$(jq -r '.session_id // "unknown"' <<<"$input" 2>/dev/null || echo unknown)"

state_dir="${TMPDIR:-/tmp}/skillme-hook-state"
state_file="$state_dir/$session_id.json"
[[ -f "$state_file" ]] || exit 0

active="$(jq -r '.skillme_active // false' "$state_file" 2>/dev/null || echo false)"
[[ "$active" == "true" ]] || exit 0

# The TaskCreated hook event was live-tested and never fires in this Claude
# Code version (2.1.220) -- so .task_created from state is unreliable and
# only kept as a secondary OR. Primary signal: Claude Code's own real task
# storage at ~/.claude/tasks/<session_id>/*.json (reverse-engineered by
# inspecting a live session, not officially documented -- if this path ever
# changes, this check silently stops finding tasks and falls back to state).
real_tasks_dir="${HOME:-/root}/.claude/tasks/$session_id"
real_task_count=0
if [[ -d "$real_tasks_dir" ]]; then
  real_task_count="$(find "$real_tasks_dir" -maxdepth 1 -name '*.json' 2>/dev/null | wc -l)"
fi

task_created_flag="$(jq -r '.task_created // false' "$state_file" 2>/dev/null || echo false)"
task_created="false"
if [[ "$real_task_count" -gt 0 || "$task_created_flag" == "true" ]]; then
  task_created="true"
fi

checkpoint="$(jq -r '.checkpoint_reached // false' "$state_file" 2>/dev/null || echo false)"
doc_eco="$(jq -r '.doc_eco_done // false' "$state_file" 2>/dev/null || echo false)"

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
