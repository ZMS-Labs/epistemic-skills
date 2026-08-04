#!/usr/bin/env python3
"""Cooperative-agent-grade PreToolUse gate (issue #42 reference).

Denies side-effecting tool calls while the active epistemic control is
hold/escalate. Fail-closed: malformed input or state denies. See README.md
for the honest trust boundary — the state file's writer is the boundary.
"""
import json
import os
import sys

SIDE_EFFECTING = {
    "Write", "Edit", "NotebookEdit", "Bash",
}
SIDE_EFFECTING_PREFIXES = (
    "mcp__github__merge", "mcp__github__push", "mcp__github__create",
    "mcp__github__update", "mcp__github__delete",
)
NON_ACTING = {"hold", "escalate"}


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        event = json.load(sys.stdin)
        tool = event["tool_name"]
    except Exception:
        deny("runtime gate: malformed hook event (fail closed)")
        return
    state_path = os.environ.get("EPISTEMIC_CONTROL_STATE", ".epistemic-control.json")
    if not os.path.exists(state_path):
        sys.exit(0)  # absent state: gate inactive by design
    try:
        control = json.load(open(state_path))["control"]
    except Exception:
        deny("runtime gate: malformed control state (fail closed)")
        return
    if control in NON_ACTING and (
        tool in SIDE_EFFECTING or tool.startswith(SIDE_EFFECTING_PREFIXES)
    ):
        deny(f"runtime gate: active control {control!r} forbids side-effecting"
             f" tool {tool!r} (cooperative-agent-grade; see reference/runtime-gate)")
        return
    sys.exit(0)


if __name__ == "__main__":
    main()
