#!/usr/bin/env python3
"""Stage-C PreToolUse hook: harness payload -> custody gate -> exit 0/2.

Fail-open by contract: ANY error (bad JSON, unknown harness, missing cwd,
no mission, evaluator exception) exits 0. Denial travels only via the
deliberate block path. Timeout is the harness's (configure <=10s); the inert
fast path is one directory stat.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _claude_kimi(payload: dict) -> dict | None:
    tool_input = payload.get("tool_input") or {}
    return {
        "tool_name": payload.get("tool_name", ""),
        "command": tool_input.get("command"),
        "file_path": tool_input.get("file_path"),
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
        "session_id": payload.get("session_id", ""),
        "cwd": payload.get("cwd", ""),
    }


ADAPTERS = {
    "claude": _claude_kimi,
    "kimi": _claude_kimi,
    "codex": _claude_kimi,   # same PreToolUse shape; Task 6 docs-verify
    "cursor": _cursor,
    "gemini": _claude_kimi,  # BeforeTool shape; Task 6 docs-verify (agy shares it)
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
        if not call or not call.get("tool_name") and not call.get("command"):
            return 0
        cwd = call.get("cwd") or "."
        workspace = Path(cwd)
        if not (workspace / "missions").is_dir():
            return 0  # inert fast path: no custody state here at all
        from custody_gate import run_gate
        verdict = run_gate(
            workspace,
            {"tool_name": call["tool_name"], "command": call.get("command"),
             "file_path": call.get("file_path")},
            actor="hook:custody-gate",
            session_id=call.get("session_id", ""), harness=args.harness)
        if verdict["decision"] == "block":
            print(f"custody gate: BLOCKED -- {verdict['reason']}",
                  file=sys.stderr)
            return 2
        return 0
    except Exception:
        return 0  # fail open, always


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
