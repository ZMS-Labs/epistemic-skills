#!/usr/bin/env python3
"""Stage-C PreToolUse hook: harness payload -> custody gate -> exit 0/2.

Fail-open by contract: ANY error (bad JSON, unknown harness, missing cwd,
no mission, evaluator exception) exits 0. Denial travels only via the
deliberate block path. Timeout is the harness's (configure <=10s); the inert
fast path is one directory stat per ancestor level.

Mission discovery walks UP from the payload's cwd (git-style) to the nearest
ancestor holding missions/. Residual, disclosed in SECURITY.md: a payload
cwd OUTSIDE the workspace tree (or a harness that reports no cwd) finds no
missions/ and stays inert -- the gate covers work done under the mission's
tree, not work reported from elsewhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from custody_mission import CustodyError


def _find_workspace(cwd: str) -> Path | None:
    current = Path(cwd or ".")
    while True:
        if (current / "missions").is_dir():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def _discover_workspace(call: dict) -> Path | None:
    """Find the mission workspace from whatever location the payload offers.

    The payload cwd is preferred and decides alone whenever present, so this
    cannot change behaviour for any harness that sends one. The fallback exists
    because Cursor's `beforeMCPExecution` documents NO cwd -- its event-specific
    fields are tool_name/tool_input plus url|command -- while every Cursor event
    carries the base field `workspace_roots`
    (https://cursor.com/docs/agent/hooks, 2026-08-12).

    Without the fallback that event resolved Path("") -> Path("."), i.e. it
    walked up from the HOOK PROCESS's own working directory, which Cursor leaves
    undocumented for plugin-shipped hooks. The failure was therefore not merely
    inert but nondeterministic, and its likely outcome -- discovering no mission
    -- is a silent ALLOW for exactly the actuator class (MCP calls to the arr
    APIs) the Stage-C ruling scoped the teeth to. A false allow is the error
    direction this contract treats as unrecoverable.

    Multi-root: roots are tried in order and the first holding a mission wins.
    Searching more places can only discover a mission where none was found
    before, so it can only add blocks, never remove one."""
    cwd = call.get("cwd") or ""
    if cwd:
        return _find_workspace(cwd)
    for root in call.get("workspace_roots") or []:
        if isinstance(root, str) and root:
            workspace = _find_workspace(root)
            if workspace is not None:
                return workspace
    return _find_workspace(".")


def _claude_kimi(payload: dict) -> dict | None:
    tool_input = payload.get("tool_input") or {}
    return {
        "tool_name": payload.get("tool_name", ""),
        "command": tool_input.get("command"),
        "file_path": tool_input.get("file_path"),
        "tool_input": tool_input or None,
        "session_id": payload.get("session_id", ""),
        "cwd": payload.get("cwd", ""),
    }


def _cursor(payload: dict) -> dict | None:
    # beforeShellExecution: {"command", "cwd"}; preToolUse carries tool fields.
    # beforeMCPExecution sends tool_input as a JSON STRING (verified against
    # https://cursor.com/docs/agent/hooks 2026-08-12) -- parse it so command
    # extraction still works; an unparseable string degrades to no match.
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except ValueError:
            tool_input = {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    return {
        "tool_name": payload.get("tool_name", "Shell"),
        "command": payload.get("command") or tool_input.get("command"),
        "file_path": tool_input.get("file_path"),
        "tool_input": tool_input or None,
        "session_id": payload.get("session_id", ""),
        "cwd": payload.get("cwd", ""),
        # beforeMCPExecution documents no cwd; workspace_roots is a BASE
        # field present on every Cursor event -- see _discover_workspace.
        "workspace_roots": payload.get("workspace_roots"),
    }


ADAPTERS = {
    "claude": _claude_kimi,
    "kimi": _claude_kimi,
    "codex": _claude_kimi,   # same PreToolUse shape; Task 6 docs-verify
    "cursor": _cursor,
    "gemini": _claude_kimi,  # BeforeTool shape (Gemini CLI only; agy REFUTED --
                             # own hooks.json, toolCall.name/args payload,
                             # JSON-decision blocking: needs its own adapter)
    "generic": _claude_kimi,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="custody_hook.py")
    parser.add_argument("--harness", default="generic")
    args = parser.parse_args(argv)
    try:
        adapter = ADAPTERS[args.harness]
        raw = sys.stdin.read()
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return 0
        call = adapter(payload)
        if not call or (not call.get("tool_name") and not call.get("command")):
            return 0
        workspace = _discover_workspace(call)
        if workspace is None:
            return 0  # inert fast path: no custody state at or above cwd
        from custody_gate import run_gate
        verdict = run_gate(
            workspace,
            {"tool_name": call["tool_name"], "command": call.get("command"),
             "file_path": call.get("file_path"),
             "tool_input": call.get("tool_input")},
            actor="hook:custody-gate",
            session_id=call.get("session_id", ""), harness=args.harness)
        if verdict["decision"] == "block":
            print(f"custody gate: BLOCKED -- {verdict['reason']}",
                  file=sys.stderr)
            return 2
        return 0
    except CustodyError as exc:
        # Fail-open posture stands, but a tamper/custody signal must not be
        # silent: name it on stderr so the session log carries it.
        print(f"custody gate: TAMPER/custody error detected, failing open: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 0
    except Exception:
        return 0  # fail open, always


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
