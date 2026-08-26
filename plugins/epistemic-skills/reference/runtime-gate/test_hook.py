#!/usr/bin/env python3
"""Black-box tests for the reference runtime gate (issue #42).

Run the hook as a subprocess, exactly as a harness does, and read the decision
it prints. The README publishes a behaviour table; until this file existed
nothing executed it, and three of its rows were false.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "hook.py"

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def run(tool_name: str, state: object, *, write_state: bool = True) -> dict:
    """Returns {"rc": int, "denied": bool, "reason": str}."""
    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "state.json"
        if write_state:
            state_path.write_text(json.dumps(state), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps({"tool_name": tool_name}),
            capture_output=True, text=True, encoding="utf-8",
            env={"EPISTEMIC_CONTROL_STATE": str(state_path),
                 "PYTHONIOENCODING": "utf-8",
                 "SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", ""),
                 "PATH": __import__("os").environ.get("PATH", "")},
        )
    decision = ""
    reason = ""
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            out = payload.get("hookSpecificOutput", {})
            decision = out.get("permissionDecision", "")
            reason = out.get("permissionDecisionReason", "")
        except ValueError:
            pass
    return {"rc": proc.returncode, "denied": decision == "deny",
            "reason": reason}


def main() -> int:
    # ---- the published table: hold/escalate deny side effects -------------
    for control in ("hold", "escalate"):
        for tool in ("Write", "Edit", "NotebookEdit", "Bash"):
            check(f"{control}-denies-{tool}",
                  run(tool, {"control": control})["denied"])
        check(f"{control}-allows-a-read-only-tool",
              not run("Read", {"control": control})["denied"])
    for tool in ("Write", "Bash"):
        check(f"proceed-allows-{tool}",
              not run(tool, {"control": "proceed"})["denied"])
    check("absent-state-is-inactive",
          not run("Bash", None, write_state=False)["denied"])

    # ---- MultiEdit is a side-effecting built-in ---------------------------
    # The denial set listed Write/Edit/NotebookEdit/Bash and the MCP-prefix
    # check does not cover built-ins, so the standard MULTI-FILE edit path was
    # permitted under a non-acting control -- the gate advertising a denial it
    # did not perform.
    check("hold-denies-MultiEdit", run("MultiEdit", {"control": "hold"})["denied"])
    check("escalate-denies-MultiEdit",
          run("MultiEdit", {"control": "escalate"})["denied"])
    check("proceed-allows-MultiEdit",
          not run("MultiEdit", {"control": "proceed"})["denied"])

    # ---- side effects outside the GitHub MCP namespace --------------------
    # The prefix list named five `mcp__github__*` verbs, so a mutating tool in
    # ANY other MCP namespace was silently allowed. This repository itself
    # references `mcp__plugin_playwright_playwright__browser_click`.
    for tool in (
        "mcp__plugin_playwright_playwright__browser_click",
        "mcp__plugin_playwright_playwright__browser_type",
        "mcp__filesystem__write_file",
        "mcp__notion__API-patch-page",
        "mcp__slack__slack_send_message",
        "mcp__sonarr__post",
    ):
        check(f"hold-denies-{tool}", run(tool, {"control": "hold"})["denied"])
    # ... and a read-only MCP call is still allowed: a gate that denies every
    # MCP call under `hold` would stop the agent from LOOKING, which is the
    # one thing a held agent must still be able to do.
    for tool in ("mcp__github__get_issue", "mcp__notion__API-retrieve-a-page",
                 "mcp__filesystem__read_file"):
        check(f"hold-allows-{tool}", not run(tool, {"control": "hold"})["denied"])

    # ---- an out-of-vocabulary control is malformed state ------------------
    # The README's own table says malformed state DENIES. `control in
    # NON_ACTING` treated "typo", 0, and an unhashable value as "not hold, not
    # escalate" -- i.e. as PROCEED -- so a typo or a corrupted writer disabled
    # the gate silently, and an unhashable value raised TypeError from set
    # membership.
    for label, state in (("typo", {"control": "typo"}),
                         ("number", {"control": 0}),
                         ("list", {"control": []}),
                         ("missing-key", {}),
                         ("not-an-object", ["hold"])):
        result = run("Bash", state)
        check(f"malformed-control-{label}-denies", result["denied"])
        check(f"malformed-control-{label}-exits-0", result["rc"] == 0)

    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
