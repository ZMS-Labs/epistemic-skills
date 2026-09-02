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


def run(tool_name: str, state: object, *, write_state: bool = True,
        raw_event: str | None = None) -> dict:
    """Returns {"rc", "denied", "reason", "allow_ok"}.

    `allow_ok` is the STRICT allow: rc == 0, no deny decision, and stdout
    either empty (implicit allow) or a well-formed hook payload. Until this
    field existed the allow rows of the published table passed on a hook
    that had crashed, exited nonzero, or printed garbage -- `decision`
    stays "" in all three cases, so `denied` is False and the row reads as
    "allowed" without the hook having successfully allowed anything."""
    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "state.json"
        if write_state:
            state_path.write_text(json.dumps(state), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(HOOK)],
            input=(raw_event if raw_event is not None
                   else json.dumps({"tool_name": tool_name})),
            capture_output=True, text=True, encoding="utf-8",
            env={"EPISTEMIC_CONTROL_STATE": str(state_path),
                 "PYTHONIOENCODING": "utf-8",
                 "SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", ""),
                 "PATH": __import__("os").environ.get("PATH", "")},
        )
    decision = ""
    reason = ""
    shape_ok = True
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            out = payload.get("hookSpecificOutput", {})
            decision = out.get("permissionDecision", "")
            reason = out.get("permissionDecisionReason", "")
            shape_ok = (isinstance(out, dict)
                        and decision in ("", "allow", "ask", "deny"))
        except (ValueError, AttributeError):
            shape_ok = False
    denied = decision == "deny"
    return {"rc": proc.returncode, "denied": denied, "reason": reason,
            "allow_ok": proc.returncode == 0 and not denied and shape_ok}


def main() -> int:
    # ---- the published table: hold/escalate deny side effects -------------
    for control in ("hold", "escalate"):
        for tool in ("Write", "Edit", "NotebookEdit", "Bash"):
            check(f"{control}-denies-{tool}",
                  run(tool, {"control": control})["denied"])
        check(f"{control}-allows-a-read-only-tool",
              run("Read", {"control": control})["allow_ok"])
    for tool in ("Write", "Bash"):
        check(f"proceed-allows-{tool}",
              run(tool, {"control": "proceed"})["allow_ok"])
    check("absent-state-is-inactive",
          run("Bash", None, write_state=False)["allow_ok"])

    # ---- MultiEdit is a side-effecting built-in ---------------------------
    # The denial set listed Write/Edit/NotebookEdit/Bash and the MCP-prefix
    # check does not cover built-ins, so the standard MULTI-FILE edit path was
    # permitted under a non-acting control -- the gate advertising a denial it
    # did not perform.
    check("hold-denies-MultiEdit", run("MultiEdit", {"control": "hold"})["denied"])
    check("escalate-denies-MultiEdit",
          run("MultiEdit", {"control": "escalate"})["denied"])
    check("proceed-allows-MultiEdit",
          run("MultiEdit", {"control": "proceed"})["allow_ok"])

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
        check(f"hold-allows-{tool}", run(tool, {"control": "hold"})["allow_ok"])

    # ---- the repository's own `mutate` MCP verb is side-effecting --------
    # `mcp__arr__mutate` is this repository's existing, explicitly mutating
    # tool (contracts/mission-custody/test_custody_hook.py pairs it with an
    # `rm -rf` command), but `_WORD` extracts `mutate` and the verb
    # vocabulary did not carry it, so under hold/escalate the gate allowed a
    # KNOWN side-effecting call the classification exists to deny. This is
    # not the documented opaque-name residue: the verb was simply missing.
    for control in ("hold", "escalate"):
        check(f"{control}-denies-mcp__arr__mutate",
              run("mcp__arr__mutate", {"control": control})["denied"])
    check("proceed-allows-mcp__arr__mutate",
          run("mcp__arr__mutate", {"control": "proceed"})["allow_ok"])

    # ---- the built-in denial set was an allowlist too ---------------------
    # Closing the five `mcp__github__*` prefixes and leaving the five built-in
    # NAMES fixes one instance of a defect and leaves its sibling. Measured
    # against the shipped built-ins under `hold` before this change:
    #
    #     KillShell     allowed   <- terminates a running process
    #     Task          allowed   <- delegates arbitrary action to a subagent
    #     Agent         allowed
    #     SlashCommand  allowed   <- executes an arbitrary command file
    #     TodoWrite     allowed
    #
    # Every one is a side effect, and the published table says a side-effecting
    # tool is DENIED under `hold`. The table was false for five more rows than
    # the three this PR set out to close.
    for control in ("hold", "escalate"):
        for tool in ("KillShell", "TodoWrite"):
            check(f"{control}-denies-builtin-{tool}",
                  run(tool, {"control": control})["denied"])
        # Delegation is action. "The subagent has the same hook" is an
        # assumption about another process's configuration, not a property of
        # this one; a gate that denies the edit and permits ordering someone
        # else to make it has denied a spelling.
        for tool in ("Task", "Agent", "SlashCommand"):
            check(f"{control}-denies-delegation-{tool}",
                  run(tool, {"control": control})["denied"])
    for tool in ("KillShell", "Task", "SlashCommand"):
        check(f"proceed-allows-{tool}",
              run(tool, {"control": "proceed"})["allow_ok"])

    # ---- CONTROL: a held agent must still be able to LOOK ------------------
    # Widening the classification to built-in names is only safe if the
    # read-only built-ins still pass. A gate that denies everything under
    # `hold` has stopped distinguishing, and this is the assertion that fails
    # if the verb vocabulary is widened carelessly later.
    for tool in ("Read", "Grep", "Glob", "BashOutput", "WebFetch",
                 "WebSearch", "NotebookRead", "ExitPlanMode"):
        check(f"hold-allows-read-only-builtin-{tool}",
              run(tool, {"control": "hold"})["allow_ok"])

    # ---- the residue is still named, and still real ------------------------
    # An opaque name carrying no verb is allowed, built-in or MCP alike. This
    # is asserted rather than left implicit so the documented boundary is
    # executed instead of described.
    check("hold-allows-opaque-mcp-name",
          run("mcp__x__thing", {"control": "hold"})["allow_ok"])
    check("hold-allows-opaque-builtin-name",
          run("Frobnicate", {"control": "hold"})["allow_ok"])

    # ---- the malformed-event half of the fail-closed row ------------------
    # Every case above sends a valid object with a string `tool_name`, so
    # the advertised `malformed event -> deny` row was never EXECUTED:
    # deleting the hook's event validation would have left this suite green.
    for label, raw in (("invalid-json", "{not json"),
                       ("missing-key", json.dumps({"tool": "Bash"})),
                       ("non-string-tool", json.dumps({"tool_name": ["Bash"]})),
                       ("null-tool", json.dumps({"tool_name": None})),
                       ("empty-stdin", "")):
        result = run("Bash", {"control": "proceed"}, raw_event=raw)
        check(f"malformed-event-{label}-denies", result["denied"])
        check(f"malformed-event-{label}-exits-0", result["rc"] == 0)

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
