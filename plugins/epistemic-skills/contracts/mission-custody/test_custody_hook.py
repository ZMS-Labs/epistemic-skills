#!/usr/bin/env python3
"""End-to-end tests for custody_hook.py: stdin payload -> exit code."""
from __future__ import annotations

import json
import os
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


def test_multi_root_order_cannot_decide_whether_a_guard_fires() -> None:
    """REPRODUCED FALSE ALLOW, now a regression test.

    _find_workspace only asks "does a missions/ dir exist here" -- it says
    nothing about whether a mission there is active, armed, or relevant. With
    first-wins, workspace_roots [A, B] where A holds a CANCELLED mission and B
    holds an ACTIVE enforce mission whose guard matches gated against A, hit
    NoActiveMission, and allowed the call SILENTLY -- while [B, A] blocked it.
    Root order is set by the IDE, not the mission author, so ordinary usage
    decided whether enforcement happened at all.

    Both orders must block."""
    guards = [{"name": "no-deploy", "tool_names": ["Bash"],
               "command_regexes": ["deploy-prod"], "path_globs": []}]
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "A", Path(tmp) / "B"
        a.mkdir(); b.mkdir()
        stale = Mission.open(a, "stale", "i", "operator:t", "agent:t",
                             actor="agent:t")
        stale.approve()
        stale.cancel("finished")          # missions/ exists, nothing active
        live = Mission.open(b, "live", "i", "operator:t", "agent:t",
                            actor="agent:t", guard_mode="enforce",
                            actuator_guards=guards)
        live.approve()

        payload = {"tool_name": "Bash",
                   "tool_input": {"command": "deploy-prod now"}}
        check("multi-root-stale-first-still-blocks",
              run_hook("cursor", dict(payload,
                                      workspace_roots=[str(a), str(b)])
                       ).returncode == 2)
        check("multi-root-armed-first-blocks",
              run_hook("cursor", dict(payload,
                                      workspace_roots=[str(b), str(a)])
                       ).returncode == 2)
        # a cwd that resolves to the stale mission must not MASK an armed root
        check("cwd-does-not-mask-an-armed-root",
              run_hook("cursor", dict(payload, cwd=str(a),
                                      workspace_roots=[str(b)])
                       ).returncode == 2)


def test_workspace_root_entry_shapes() -> None:
    """The entry shape comes from docs prose, not a captured payload, so the
    plausible editor conventions are all accepted rather than one being
    trusted. Guessing wrong would make the fallback a silent no-op in
    production while every test still passed."""
    guards = [{"name": "no-deploy", "tool_names": ["Bash"],
               "command_regexes": ["deploy-prod"], "path_globs": []}]
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        m = Mission.open(ws, "shapes", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=guards)
        m.approve()
        payload = {"tool_name": "Bash",
                   "tool_input": {"command": "deploy-prod now"}}
        uri = "file:///" + str(ws).replace(os.sep, "/")
        check("root-as-file-uri-blocks",
              run_hook("cursor", dict(payload, workspace_roots=[uri])
                       ).returncode == 2)
        check("root-as-uri-object-blocks",
              run_hook("cursor", dict(payload,
                                      workspace_roots=[{"uri": str(ws),
                                                        "name": "ws"}])
                       ).returncode == 2)
        check("root-as-path-object-blocks",
              run_hook("cursor", dict(payload,
                                      workspace_roots=[{"path": str(ws)}])
                       ).returncode == 2)


def test_root_location_uri_forms() -> None:
    """`_root_location` unit cases, including the RFC 8089 authority form.

    `file://server/share` carries the host in netloc, not path. Dropping it
    yields `/share`, which resolves to the WRONG local path -- and this fleet
    is UNC-heavy (Y: is a mapping of a UNC share), so the authority form is the
    one most likely to appear here."""
    import custody_hook
    unc = "\\" + "\\" + "server" + "\\" + "share" + "\\" + "project"
    cases = [
        ("file://server/share/project", unc),
        ("file:///C:/work/proj", "C:/work/proj"),
        ("file:///opt/u/proj", "/opt/u/proj"),
        ("file:///C:/a%20b/proj", "C:/a b/proj"),
        ("D:/dev/thing", "D:/dev/thing"),
        ({"uri": "D:/dev/thing"}, "D:/dev/thing"),
        ({"path": "D:/dev/thing"}, "D:/dev/thing"),
        (12345, ""),
        (None, ""),
        ({}, ""),
    ]
    for src, want in cases:
        check(f"root-location-{str(src)[:28]}",
              custody_hook._root_location(src) == want)


def test_missing_payload_cwd_is_inert_even_when_hook_process_runs_inside_armed_workspace() -> None:
    """No usable location means INERT, never a search from the hook process's
    own directory.

    Coercing an absent cwd to "." searches from wherever the hook happens to be
    running -- not where the agent is, and undocumented for plugin-shipped
    hooks. It can gate a call against a mission the caller has nothing to do
    with, or miss the armed one entirely; one of those directions is a false
    allow. The module's own contract already says a harness reporting no cwd
    stays inert, which the previous `or "."` quietly contradicted.

    Named to match the acceptance test in es#137, which owns this contract from
    the main() side; this covers the discovery function es#130 replaced that
    call site with."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-inert-cwd", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        # the hook subprocess runs with cwd INSIDE the armed workspace -- the
        # exact situation a "." fallback would silently exploit
        payload = {"tool_name": "Bash", "tool_input": {"command": "rm -rf x"}}
        r = subprocess.run(
            [sys.executable, str(HOOK), "--harness", "claude"],
            input=json.dumps(payload), capture_output=True, text=True,
            cwd=str(ws))
        check("no-cwd-no-roots-is-inert-not-process-relative",
              r.returncode == 0)
        check("inert-path-emits-no-block", "BLOCKED" not in r.stderr)


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
