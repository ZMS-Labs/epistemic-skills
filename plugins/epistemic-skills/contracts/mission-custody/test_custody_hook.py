#!/usr/bin/env python3
"""End-to-end tests for custody_hook.py: stdin payload -> exit code."""
from __future__ import annotations

import json
import os
import runpy
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOOK = ROOT / "custody_hook.py"
CURSOR_CLI_RENDERER = (
    ROOT.parents[1] / "hooks" / "render_cursor_cli_hooks.py"
)
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


def test_cursor_cli_installation_emits_plugin_root_hook_command() -> None:
    """es#136: render from an arbitrary workspace, then prove the installed
    absolute command blocks an armed actuator and stays inert without a
    mission.  The workspace deliberately has no local contracts tree."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "arbitrary workspace"
        ws.mkdir()
        destination = ws / ".cursor" / "hooks.json"
        rendered = subprocess.run(
            [sys.executable, str(CURSOR_CLI_RENDERER),
             "--output", str(destination)],
            cwd=ws, capture_output=True, text=True)
        check("cursor-cli-render-exit-0", rendered.returncode == 0)
        check("cursor-cli-config-written", destination.is_file())
        check("cursor-cli-workspace-has-no-local-contracts",
              not (ws / "contracts" / "mission-custody").exists())

        config = json.loads(destination.read_text(encoding="utf-8"))
        commands = [
            row["command"]
            for rows in config["hooks"].values()
            for row in rows
        ]
        expected_argv = [str(Path(sys.executable).resolve()),
                         str(HOOK.resolve()), "--harness", "cursor"]
        expected_command = (subprocess.list2cmdline(expected_argv)
                            if os.name == "nt" else shlex.join(expected_argv))
        check("cursor-cli-every-command-is-installed-hook",
              bool(commands) and all(c == expected_command for c in commands))
        check("cursor-cli-config-does-not-reference-dot-contracts-path",
              "./contracts/mission-custody/custody_hook.py"
              not in destination.read_text(encoding="utf-8"))

        mission = Mission.open(
            ws, "cursor-cli-install", "i", "operator:t", "agent:t",
            actor="agent:t", guard_mode="enforce", actuator_guards=GUARDS)
        mission.approve()
        blocked = subprocess.run(
            expected_argv,
            input=json.dumps({"command": "rm -rf x", "cwd": str(ws)}),
            cwd=ws, capture_output=True, text=True)
        check("cursor-cli-installed-hook-invoked", "no-rm" in blocked.stderr)
        check("cursor-cli-installed-hook-blocks", blocked.returncode == 2)

        inert = Path(tmp) / "inert workspace"
        inert.mkdir()
        allowed = subprocess.run(
            expected_argv,
            input=json.dumps({"command": "rm -rf x", "cwd": str(inert)}),
            cwd=inert, capture_output=True, text=True)
        check("cursor-cli-installed-hook-inert-without-mission",
              allowed.returncode == 0)

        before = destination.read_bytes()
        refused = subprocess.run(
            [sys.executable, str(CURSOR_CLI_RENDERER),
             "--output", str(destination)],
            cwd=ws, capture_output=True, text=True)
        check("cursor-cli-render-refuses-existing-config",
              refused.returncode == 2)
        check("cursor-cli-existing-config-unchanged",
              destination.read_bytes() == before)

        partial = ws / ".cursor" / "partial-hooks.json"
        real_open = Path.open

        class FailingWrite:
            def __init__(self) -> None:
                self.handle = real_open(
                    partial, "x", encoding="utf-8", newline="\n"
                )

            def __enter__(self):
                return self

            def write(self, value: str) -> int:
                self.handle.write(value[:1])
                self.handle.flush()
                raise OSError("simulated partial write")

            def __exit__(self, exc_type, exc, traceback) -> None:
                self.handle.close()

        renderer_globals = runpy.run_path(str(CURSOR_CLI_RENDERER))
        original_path_open = Path.open
        partial_write_raised = False
        try:
            Path.open = lambda *_args, **_kwargs: FailingWrite()
            try:
                renderer_globals["_write_new_config"](partial, "{}\n")
            except OSError:
                partial_write_raised = True
        finally:
            Path.open = original_path_open
        check("cursor-cli-partial-write-raises", partial_write_raised)
        check("cursor-cli-partial-write-removed", not partial.exists())
def test_env_bound_draft_self_arms() -> None:
    """OD-4 refined (operator ruling 2026-08-25: "Self-arm at open, union
    at approve"): a session whose harness env carries ZMS_MISSION_ID for a
    draft mission is gated by that draft's OWN guards pre-approve; without
    the binding the draft arms nothing (union at approve, unchanged)."""
    def run_with_env(binding: str | None) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        env.pop("ZMS_MISSION_ID", None)
        if binding is not None:
            env["ZMS_MISSION_ID"] = binding
        return subprocess.run(
            [sys.executable, str(HOOK), "--harness", "claude"],
            input=raw, capture_output=True, text=True, env=env)

    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        Mission.open(ws, "hook-draft", "i", "operator:t", "agent:t",
                     actor="agent:t", guard_mode="enforce",
                     actuator_guards=GUARDS)
        raw = json.dumps(payloads(tmp)["claude"])
        check("hook-unbound-draft-allows",
              run_with_env(None).returncode == 0)
        res = run_with_env("hook-draft")
        check("hook-env-bound-draft-blocks", res.returncode == 2)
        check("hook-env-bound-reason-names-rule",
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


def test_multiple_active_evaluates_the_union() -> None:
    # es#173: the decoy-disarm is dead -- a duplicated mission dir no longer
    # turns the gate inert; both copies' guards enforce and the hook blocks,
    # naming every matching (mission, rule) pair in the BLOCKED line.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-multi", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        shutil.copytree(ws / "missions" / "hook-multi",
                        ws / "missions" / "hook-multi-2")
        res = run_hook("claude", payloads(tmp)["claude"])
        check("hook-multi-active-blocks", res.returncode == 2)
        check("hook-multi-active-names-both",
              "hook-multi" in res.stderr and "hook-multi-2" in res.stderr)


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


def test_decoy_missions_ancestor_does_not_hide_armed_mission() -> None:
    """es#137: a shallow empty missions/ directory must not prevent discovery
    of an armed mission higher in the tree."""
    guards = [{"name": "no-deploy", "tool_names": ["Bash"],
               "command_regexes": ["deploy-prod"], "path_globs": []}]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "workspace"
        decoy = root / "subdir"
        decoy.mkdir(parents=True)
        (decoy / "missions").mkdir()
        live = Mission.open(root, "live", "i", "operator:t", "agent:t",
                            actor="agent:t", guard_mode="enforce",
                            actuator_guards=guards)
        live.approve()
        payload = {"tool_name": "Bash",
                   "tool_input": {"command": "deploy-prod now"},
                   "cwd": str(decoy / "deep")}
        (decoy / "deep").mkdir()
        check("decoy-missions-ancestor-still-blocks",
              run_hook("cursor", payload).returncode == 2)


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
        # BARE Windows form. Cursor's Windows workspace_roots use "/c:/...".
        # Returned unchanged it parses as a DRIVELESS "\\c:\\..." on Windows,
        # so the mission tree is never found and guarded MCP calls fail open --
        # exactly the hole the workspace_roots fallback exists to close.
        ("/c:/work/project", "c:/work/project"),
        ("/C:/work/project", "C:/work/project"),
        # RFC 8089: "localhost" is EQUIVALENT TO AN EMPTY AUTHORITY, i.e. a
        # LOCAL path. The UNC fix originally turned it into \\localhost\C:\...,
        # which resolves nowhere -- a hole that fix itself opened.
        ("file://localhost/C:/work/proj", "C:/work/proj"),
        ("file://localhost/opt/u/proj", "/opt/u/proj"),
        ("file://LOCALHOST/C:/work/proj", "C:/work/proj"),
        # a bare POSIX path must not be mangled by the drive-slash strip
        ("/opt/u/proj", "/opt/u/proj"),
        # the drive letter must be a LETTER: rewriting "/1:/x" would invent a
        # location out of a string nothing identified as a drive path
        ("/1:/work/project", "/1:/work/project"),
    ]
    for src, want in cases:
        check(f"root-location-{str(src)[:28]}",
              custody_hook._root_location(src) == want)


def test_relative_root_never_becomes_a_candidate() -> None:
    """A root the process cannot interpret must not resolve to the cwd.

    `_find_workspace` walks ancestors, and a RELATIVE path's chain terminates
    at `.`, so a `file://` URI fed through as a literal (Path("file:///c:/w")
    is relative on both platforms) made `Path(".")` -- "wherever the hook
    happens to be running" -- a candidate. Consequences measured: a block
    naming a rule from a mission the user is not in, and an entry written into
    that unrelated mission's guard log. The same shape hits the stripped
    bare-drive form on POSIX, where `c:/work` is relative."""
    import custody_hook
    asked: list[str] = []
    original = custody_hook._find_workspaces
    custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
    try:
        custody_hook._candidate_workspaces(
            {"workspace_roots": ["file:///c:/some/other/project"]})
    finally:
        custody_hook._find_workspaces = original
    check("uri-literal-not-probed",
          not any(a.startswith("file:") for a in asked))
    # NATIVE absoluteness, asserted the same way the gate decides it. An
    # earlier version of this check passed on Windows and FAILED on POSIX,
    # because the gate accepted "absolute under either flavour" while
    # _find_workspace parses natively -- so `c:/work/project` slipped through
    # on Linux and reached `.`. A platform-dependent assertion is how that got
    # past a green local run.
    check("no-relative-location-probed",
          all(Path(a).is_absolute() for a in asked))


def test_object_shaped_root_also_offers_both_readings() -> None:
    """An object root must get the dual reading a bare string gets.

    Gating the second reading on `isinstance(root, str)` skipped
    {"uri": "/c:/work/project"} entirely, so on POSIX only the stripped form
    -- relative there -- was offered, and a mission under the real absolute
    path was missed. A fail-open for exactly the editor shape this module set
    out to support."""
    import custody_hook
    for shape in ({"uri": "/c:/work/project"}, {"path": "/c:/work/project"}):
        asked: list[str] = []
        original = custody_hook._find_workspace
        custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
        try:
            custody_hook._candidate_workspaces({"workspace_roots": [shape]})
        finally:
            custody_hook._find_workspaces = original
        key = "uri" if "uri" in shape else "path"
        # exactly one reading is native-absolute per platform; the point is
        # that the object shape gets both OFFERED, not that both survive
        check(f"object-root-{key}-offers-a-reading", bool(asked))
        check(f"object-root-{key}-all-native-absolute",
              all(Path(a).is_absolute() for a in asked))


def test_drive_shaped_file_uri_offers_the_decoded_posix_reading() -> None:
    """`file:///c:/ok` decodes to `/c:/ok`, which is absolute on POSIX.

    The alternate reading used to be the RAW string. For a bare root that is
    the same thing, but for a URI it is not: the raw `file:///c:/ok` is
    relative to `Path` on both platforms, so on POSIX the stripped reading was
    rejected as relative AND the raw fallback was rejected too -- both readings
    discarded, workspace never evaluated, an armed mission there failing open.

    The alternate is now the unstripped DECODED path, so each platform still
    sees the reading that is absolute there."""
    import custody_hook
    check("uri-primary-is-the-windows-reading",
          custody_hook._root_location("file:///c:/ok") == "c:/ok")
    check("uri-alternate-is-the-posix-reading",
          custody_hook._root_location("file:///c:/ok", strip=False) == "/c:/ok")
    # UNC resolves before any stripping, so both readings agree
    unc = "\\" + "\\" + "server" + "\\" + "share" + "\\" + "p"
    check("uri-unc-unaffected-by-strip",
          custody_hook._root_location("file://server/share/p", strip=False) == unc)

    asked: list[str] = []
    original = custody_hook._find_workspaces
    custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
    try:
        custody_hook._candidate_workspaces({"workspace_roots": ["file:///c:/ok"]})
    finally:
        custody_hook._find_workspaces = original
    native = "c:/ok" if os.name == "nt" else "/c:/ok"
    check("uri-native-reading-probed", native in asked)
    check("uri-probes-nothing-relative",
          all(Path(a).is_absolute() for a in asked))


def test_malformed_root_does_not_disarm_the_others() -> None:
    """`urlparse` raises on a malformed authority; unhandled it returned ALLOW.

    "file://[oops" -> ValueError: Invalid IPv6 URL escaped discovery into the
    outer handler, so ONE malformed IDE-supplied root silently disarmed an
    armed guard with an empty stderr -- verbatim the fail-open the
    per-candidate handler downstream exists to close, left open one function
    earlier."""
    import custody_hook
    asked: list[str] = []
    original = custody_hook._find_workspaces
    custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
    try:
        custody_hook._candidate_workspaces(
            {"workspace_roots": ["file://[oops", "file:///c:/ok"]})
    except Exception as exc:                                  # noqa: BLE001
        check("malformed-root-does-not-raise", False)
        print(f"  raised {type(exc).__name__}")
    else:
        check("malformed-root-does-not-raise", True)
    finally:
        custody_hook._find_workspaces = original
    check("later-root-still-evaluated", any("ok" in a for a in asked))


def test_bare_drive_root_offers_both_readings() -> None:
    """'/c:/work/project' is a Windows drive path AND a legal POSIX path.

    On POSIX ':' is an ordinary filename character, so stripping the leading
    slash there yields a RELATIVE path: `_find_workspace` would search from
    wherever the hook process happens to run, find nothing, and silently allow
    the guarded call. Gating the rewrite on the platform only moves the
    fail-open to the other platform -- both wrong readings end the same way.

    So neither reading is chosen. Both are OFFERED; the native-absoluteness
    gate then keeps whichever one is real on this platform, `_find_workspace`
    drops whichever has no missions/ tree, and any-blocks-wins does the rest.

    The assertion is deliberately platform-aware. Asserting that BOTH readings
    are probed passed on Windows and would have failed on Linux, because only
    one of them is native-absolute on any given platform -- and a
    platform-dependent assertion that happens to hold locally is how a hole
    reaches CI green."""
    import custody_hook
    asked: list[str] = []
    original = custody_hook._find_workspaces
    custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
    try:
        custody_hook._candidate_workspaces(
            {"workspace_roots": ["/c:/work/project"]})
    finally:
        custody_hook._find_workspaces = original
    native = "c:/work/project" if os.name == "nt" else "/c:/work/project"
    other = "/c:/work/project" if os.name == "nt" else "c:/work/project"
    check("bare-drive-probes-the-native-reading", native in asked)
    check("bare-drive-drops-the-non-native-reading", other not in asked)
    check("bare-drive-probes-nothing-relative",
          all(Path(a).is_absolute() for a in asked))
    # a path with only ONE reading must not be probed twice
    asked.clear()
    custody_hook._find_workspaces = lambda loc: (asked.append(loc), [])[1]
    try:
        custody_hook._candidate_workspaces(
            {"workspace_roots": ["/opt/u/proj"]})
    finally:
        custody_hook._find_workspaces = original
    # A POSIX root has ONE reading. It is probed once where it is real, and
    # not probed at all on Windows, where "/opt/u/proj" is rooted-but-driveless
    # and `_find_workspace` would walk it to `.`.
    check("single-reading-probed-once",
          asked == ([] if os.name == "nt" else ["/opt/u/proj"]))


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

    # Residual hole: `_find_workspaces` itself used `cwd or "."` (and
    # `Path("")` is `.`). Probe in a fresh interpreter so earlier in-process
    # mocks of `_find_workspaces` cannot recurse into this assertion.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-inert-walk", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        probe = (
            "import os, sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import custody_hook\n"
            "os.chdir(sys.argv[2])\n"
            "print(repr([str(p) for p in custody_hook._find_workspaces('')]))\n"
        )
        r = subprocess.run(
            [sys.executable, "-c", probe, str(ROOT), str(ws)],
            capture_output=True, text=True)
        check("empty-cwd-walk-probe-ran", r.returncode == 0)
        check("empty-cwd-walk-does-not-use-process-dot",
              r.stdout.strip() == "[]")


def test_non_custody_error_on_one_root_does_not_suppress_a_later_block() -> None:
    """A non-CustodyError on an earlier candidate must not abort the loop.

    The loop originally caught only CustodyError, so anything else -- and
    Mission.load intentionally PROPAGATES environmental OSErrors such as
    PermissionError -- escaped to the outer `except Exception: return 0`. One
    unreadable root then silently suppressed every later root's block: root
    ORDER causing a false allow, the exact defect the loop was built to close.
    """
    guards = [{"name": "no-deploy", "tool_names": ["Bash"],
               "command_regexes": ["deploy-prod"], "path_globs": []}]
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "A", Path(tmp) / "B"
        a.mkdir(); b.mkdir()
        # structurally poisoned: a DIRECTORY where a checkpoint file must be,
        # which raises outside the CustodyError family
        (a / "missions" / "broken" / "checkpoints").mkdir(parents=True)
        (a / "missions" / "broken" / "checkpoints" / "r00000001.json").mkdir()
        live = Mission.open(b, "live", "i", "operator:t", "agent:t",
                            actor="agent:t", guard_mode="enforce",
                            actuator_guards=guards)
        live.approve()
        payload = {"tool_name": "Bash",
                   "tool_input": {"command": "deploy-prod now"},
                   "workspace_roots": [str(a), str(b)]}
        res = run_hook("cursor", payload)
        check("poisoned-earlier-root-does-not-suppress-later-block",
              res.returncode == 2)
        check("poisoned-root-failure-is-loud", "failing open" in res.stderr)


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
