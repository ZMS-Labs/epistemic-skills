#!/usr/bin/env python3
"""Cooperative-agent-grade PreToolUse gate (issue #42 reference).

Denies side-effecting tool calls while the active epistemic control is
hold/escalate. Fail-closed: malformed input or state denies. See README.md
for the honest trust boundary — the state file's writer is the boundary.
"""
import json
import os
import re
import sys

SIDE_EFFECTING = {
    # MultiEdit is the standard MULTI-FILE edit path. Omitting it left the
    # gate advertising a denial it did not perform: under `hold`, edits routed
    # through MultiEdit were permitted while the identical edit through `Edit`
    # was denied.
    "Write", "Edit", "MultiEdit", "NotebookEdit", "Bash",
}

# DELEGATION IS ACTION. These built-ins do not themselves write anything; they
# hand the work to another executor. Under `hold` that is the evasion the
# control exists to prevent, and "the subagent has the same hook" is an
# assumption about another process's configuration, not a property of this one.
# A gate that denies the edit and permits ordering someone else to make it has
# denied a spelling, not an action.
DELEGATING = {"Task", "Agent", "SlashCommand"}
SIDE_EFFECTING_PREFIXES = (
    "mcp__github__merge", "mcp__github__push", "mcp__github__create",
    "mcp__github__update", "mcp__github__delete",
)

# Every prefix above is a GitHub verb, so a mutating tool in ANY OTHER MCP
# namespace was silently allowed under a non-acting control -- this repository
# itself references `mcp__plugin_playwright_playwright__browser_click`, and
# filesystem, database and messaging servers have the same shape. An allowlist
# of five prefixes encodes its author's enumeration, and its blind spot IS the
# namespace nobody enumerated.
#
# So the namespace no longer decides. The tool name is split into words and
# tested against a verb vocabulary. DELIBERATELY OVER-BROAD in the safe
# direction: under `hold` a false deny costs a retry, a false allow costs the
# action the control exists to prevent. Read-only calls stay allowed, because
# a held agent must still be able to LOOK.
#
# NAMED RESIDUE, because a heuristic that hides its edges is worse than none:
# a mutating tool whose name carries no verb from this list (`mcp__x__thing`)
# is still allowed. This is the measured vocabulary, not a proof of
# completeness.
MCP_MUTATING_VERBS = {
    "add", "append", "apply", "approve", "archive", "cancel", "clear",
    "click", "close", "commit", "copy", "create", "delete", "deploy",
    "destroy", "drag", "drop", "edit", "exec", "execute", "fill", "import",
    "insert", "install", "invite", "kill", "merge", "move", "mutate",
    "navigate",
    "patch", "post", "press", "publish", "purge", "push", "put", "remove",
    "rename", "reset", "restart", "revoke", "run", "save", "schedule",
    "send", "set", "share", "start", "stop", "submit", "sync", "trash",
    "type", "unlink", "update", "upload", "upsert", "write",
    # `mutate` is not aspirational: this repository's own `mcp__arr__mutate`
    # (paired with `rm -rf` in contracts/mission-custody/test_custody_hook.py)
    # was ALLOWED under hold/escalate because the word was absent here -- a
    # known side-effecting call the classification exists to deny.
}
_WORD = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+|\d+")

# The DOCUMENTED state vocabulary. `control in NON_ACTING` treated everything
# else -- a typo, a number, a corrupted writer's output -- as if it were
# `proceed`, so the gate disabled itself silently on malformed state that the
# README's own table says must DENY. An unhashable value did worse: `[] in
# {...}` raises TypeError, so the hook exited nonzero with a traceback instead
# of deciding anything.
NON_ACTING = {"hold", "escalate"}
CONTROLS = NON_ACTING | {"proceed"}


def name_mutates(tool: str) -> bool:
    """Does this tool name carry a mutating verb?

    Applied to BUILT-INS as well as MCP names. The five-name built-in set above
    is an enumeration exactly like the five `mcp__github__*` prefixes were, and
    it has the same blind spot: measured against the shipped built-ins under
    `hold`, `KillShell` -- which terminates a running process -- was allowed,
    because nothing tested a built-in name it did not already list. Closing the
    MCP allowlist and leaving the built-in allowlist open fixes one instance of
    a defect and leaves its sibling.

    Read-only built-ins keep passing because their names carry no verb from the
    vocabulary: Read, Grep, Glob, BashOutput, WebFetch, WebSearch,
    NotebookRead, ExitPlanMode. A held agent must still be able to LOOK.
    """
    return bool({w.lower() for w in _WORD.findall(tool)} & MCP_MUTATING_VERBS)


def mcp_mutates(tool: str) -> bool:
    """Does this MCP tool name carry a mutating verb, in any namespace?"""
    if not tool.startswith("mcp__"):
        return False
    return name_mutates(tool)


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
        if not isinstance(tool, str):
            raise TypeError("tool_name must be a string")
    except Exception:
        deny("runtime gate: malformed hook event (fail closed)")
        return
    state_path = os.environ.get("EPISTEMIC_CONTROL_STATE", ".epistemic-control.json")
    if not os.path.exists(state_path):
        sys.exit(0)  # absent state: gate inactive by design
    try:
        with open(state_path, encoding="utf-8") as handle:
            control = json.load(handle)["control"]
    except Exception:
        deny("runtime gate: malformed control state (fail closed)")
        return
    # OUT OF VOCABULARY IS MALFORMED, not "proceed". The documented state is
    # {"control": "hold|escalate|proceed"}, and the README's table says
    # malformed state denies.
    if not isinstance(control, str) or control not in CONTROLS:
        deny(f"runtime gate: control state {control!r} is outside the "
             f"documented vocabulary {sorted(CONTROLS)} (fail closed)")
        return
    if control in NON_ACTING and (
        tool in SIDE_EFFECTING
        or tool in DELEGATING
        or tool.startswith(SIDE_EFFECTING_PREFIXES)
        or name_mutates(tool)
    ):
        deny(f"runtime gate: active control {control!r} forbids side-effecting"
             f" tool {tool!r} (cooperative-agent-grade; see reference/runtime-gate)")
        return
    sys.exit(0)


if __name__ == "__main__":
    main()
