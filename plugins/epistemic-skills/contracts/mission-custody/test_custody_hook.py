#!/usr/bin/env python3
"""End-to-end tests for custody_hook.py: stdin payload -> exit code."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOOK = ROOT / "custody_hook.py"
sys.path.insert(0, str(ROOT))
from custody_mission import Mission  # noqa: E402
from custody_store import sha256_file  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


GUARDS = [{"name": "no-rm", "tool_names": ["Bash", "shell", "Shell"],
           "command_regexes": ["rm -rf"], "path_globs": []}]


def run_hook(harness: str, payload: dict | str) -> subprocess.CompletedProcess:
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(HOOK), "--harness", harness],
        input=raw, capture_output=True, text=True)


def payloads(cwd: str) -> dict:
    return {
        "claude": {"hook_event_name": "PreToolUse", "session_id": "s1",
                   "cwd": cwd,
                   "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "kimi": {"hook_event_name": "PreToolUse", "session_id": "s2",
                 "cwd": cwd,
                 "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "codex": {"session_id": "s3", "cwd": cwd,
                  "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "cursor": {"command": "rm -rf x", "cwd": cwd},  # beforeShellExecution
        "gemini": {"tool_name": "Bash",
                   "tool_input": {"command": "rm -rf x"}, "cwd": cwd},
        "generic": {"tool_name": "Bash",
                    "tool_input": {"command": "rm -rf x"}, "cwd": cwd},
    }


def test_block_per_harness() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-e2e", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        for harness, payload in payloads(tmp).items():
            res = run_hook(harness, payload)
            check(f"hook-{harness}-blocks", res.returncode == 2)
            check(f"hook-{harness}-reason-names-rule",
                  "no-rm" in (res.stderr + res.stdout))


def test_allow_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-allow", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        ok = payloads(tmp)["claude"]
        ok["tool_input"] = {"command": "ls"}
        check("hook-unmatched-allows", run_hook("claude", ok).returncode == 0)
    with tempfile.TemporaryDirectory() as tmp:
        # no missions dir at all -> inert fast path
        p = payloads(tmp)["claude"]
        check("hook-no-missions-dir-allows",
              run_hook("claude", p).returncode == 0)


def test_log_write_failure_still_blocks() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-logfail", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        (ws / "missions" / "hook-logfail" / "guard-log.jsonl").mkdir()
        res = run_hook("claude", payloads(tmp)["claude"])
        check("hook-log-failure-still-blocks", res.returncode == 2)


def test_subdirectory_cwd_still_gates() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-subdir", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        sub = ws / "deep" / "nest"
        sub.mkdir(parents=True)
        p = payloads(str(sub))["claude"]
        check("hook-subdir-cwd-blocks", run_hook("claude", p).returncode == 2)


def test_tampered_mission_fails_open_loudly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-tamper", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        # forge a tail checkpoint rewriting the instruction
        latest, path = m.store.load_latest()
        forged = json.loads(json.dumps(latest))
        forged["revision"] = latest["revision"] + 1
        forged["prev_checkpoint_sha256"] = sha256_file(path)
        forged["manifest"]["authority"]["instruction"] = "rewritten"
        m.store.write_checkpoint(forged)
        res = run_hook("claude", payloads(tmp)["claude"])
        check("hook-tamper-fails-open", res.returncode == 0)
        check("hook-tamper-stderr-loud",
              "CustodyError" in res.stderr and "TAMPER" in res.stderr)


def test_completed_mission_allows() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-done", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        m.cancel("done")  # completed/cancelled missions are out of scope
        check("hook-completed-mission-allows",
              run_hook("claude", payloads(tmp)["claude"]).returncode == 0)


def test_cursor_string_tool_input_mcp() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        guards = [{"name": "no-rm-mcp", "tool_names": ["mcp__arr__mutate"],
                   "command_regexes": ["rm -rf"], "path_globs": []}]
        m = Mission.open(ws, "hook-mcp-str", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=guards)
        m.approve()
        # beforeMCPExecution sends tool_input as a JSON STRING
        payload = {"tool_name": "mcp__arr__mutate",
                   "tool_input": json.dumps({"command": "rm -rf x"}),
                   "cwd": tmp}
        check("hook-cursor-string-tool-input-blocks",
              run_hook("cursor", payload).returncode == 2)


def test_multiple_active_allows_with_warning() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-multi", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        shutil.copytree(ws / "missions" / "hook-multi",
                        ws / "missions" / "hook-multi-2")
        res = run_hook("claude", payloads(tmp)["claude"])
        check("hook-multi-active-allows", res.returncode == 0)
        check("hook-multi-active-warns",
              "multiple active" in res.stderr.lower())


def test_fail_open() -> None:
    check("hook-garbage-stdin-allows", run_hook("claude", "not json{{").returncode == 0)
    check("hook-empty-stdin-allows", run_hook("claude", "").returncode == 0)
    check("hook-unknown-harness-allows",
          subprocess.run([sys.executable, str(HOOK), "--harness", "nope"],
                         input="{}", capture_output=True,
                         text=True).returncode == 0)


def test_cursor_mcp_without_cwd_discovers_via_workspace_roots() -> None:
    """Cursor's beforeMCPExecution documents NO cwd -- only the base field
    workspace_roots. Before this fallback the payload resolved Path("") ->
    Path("."), walking up from the HOOK PROCESS's cwd (undocumented for
    plugin-shipped hooks), so the gate silently ALLOWED guarded MCP calls --
    a false allow, the direction this contract treats as unrecoverable."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        guards = [{"name": "no-arr-mutate", "tool_names": ["mcp__arr__mutate"],
                   "command_regexes": [":8989/api"], "path_globs": []}]
        m = Mission.open(ws, "hook-mcp-roots", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=guards)
        m.approve()
        nested = ws / "src" / "deep"
        nested.mkdir(parents=True)

        # NO cwd key at all -- exactly what beforeMCPExecution documents
        payload = {"tool_name": "mcp__arr__mutate",
                   "tool_input": json.dumps({"url": "http://h:8989/api/v3/cmd"}),
                   "workspace_roots": [str(nested)]}
        check("hook-cursor-mcp-no-cwd-blocks-via-roots",
              run_hook("cursor", payload).returncode == 2)

        # a root holding no mission must not invent one: stays inert (allow)
        outside = Path(tempfile.mkdtemp())
        try:
            check("hook-cursor-roots-without-mission-inert",
                  run_hook("cursor", dict(payload,
                                          workspace_roots=[str(outside)])
                           ).returncode == 0)
        finally:
            shutil.rmtree(outside, ignore_errors=True)

        # malformed roots must fail open, never raise
        for bad in ([None], [123], [""], "notalist", []):
            check(f"hook-cursor-malformed-roots-{type(bad).__name__}-{bad!r:.12}",
                  run_hook("cursor", dict(payload, workspace_roots=bad)
                           ).returncode in (0, 2))


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
