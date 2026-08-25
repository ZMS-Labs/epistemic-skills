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
import os
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

sys.path.insert(0, str(Path(__file__).resolve().parent))

from custody_mission import CustodyError


def _find_workspace(cwd: str) -> Path | None:
    """Nearest ancestor holding missions/ (legacy single answer)."""
    workspaces = _find_workspaces(cwd)
    return workspaces[0] if workspaces else None


def _find_workspaces(cwd: str) -> list[Path]:
    """Every ancestor holding missions/, nearest first.

    Stopping at the first missions/ directory was a reproduced false allow
    (es#137): a decoy empty ``<workspace>/subdir/missions/`` hid an armed
    mission higher in the tree. The hook gates against every candidate, so
    every ancestor with a missions/ store must be offered.

    An empty or missing location must not fall back to ``.``: ``Path("")``
    is ``.``, so ``cwd or "."`` searched from the hook process directory
    (es#137)."""
    if not cwd:
        return []
    current = Path(cwd)
    found: list[Path] = []
    while True:
        if (current / "missions").is_dir():
            if current not in found:
                found.append(current)
        parent = current.parent
        if parent == current:
            break
        current = parent
    return found


def _strip_leading_drive_slash(path: str) -> str:
    """'/C:/x' -> 'C:/x'. A URI path and Cursor's bare Windows roots both carry
    the leading slash; Windows reads the un-stripped form as a driveless path.

    The drive letter must be a LETTER. '/1:/x' is not a drive path, and
    rewriting it would invent a location out of an unrecognised string."""
    if len(path) > 2 and path[0] == "/" and path[1].isalpha() and path[2] == ":":
        return path[1:]
    return path


def _root_location(root: object, *, strip: bool = True) -> str:
    """Best-effort path string from one workspace_roots entry.

    The entry shape is taken from Cursor's docs prose, NOT from a captured
    payload -- so this accepts the shapes editors actually use rather than
    trusting one: a bare path, a `file://` URI (the LSP/VS Code convention),
    or an object carrying `uri`/`path`. An unrecognised shape yields "" and is
    skipped. Guessing wrong here would make the whole fallback a silent no-op
    in production while every test passed."""
    if isinstance(root, dict):
        root = root.get("uri") or root.get("path") or ""
    if not isinstance(root, str) or not root:
        return ""
    if root.startswith("file://"):
        from urllib.parse import unquote, urlparse
        parsed = urlparse(root)
        path = unquote(parsed.path)
        # RFC 8089 defines "localhost" as EQUIVALENT TO AN EMPTY AUTHORITY, so
        # file://localhost/C:/work is a LOCAL path. Treating it as a UNC
        # authority produced \\localhost\C:\work, which resolves nowhere -- a
        # hole the UNC fix itself opened, caught in review.
        if parsed.netloc and parsed.netloc.lower() != "localhost":
            # Authority form: file://server/share -> \\server\share. Dropping
            # the host silently resolves to the WRONG local path, and this
            # fleet is UNC-heavy (a mapped drive over a UNC share).
            return "\\\\" + parsed.netloc + path.replace("/", "\\")
        return _strip_leading_drive_slash(path) if strip else path
    # Bare (non-URI) roots need the same treatment: Cursor's Windows
    # workspace_roots use the form "/c:/work/project". Returned unchanged, a
    # Windows path parse reads that as "\c:\work\project" with NO DRIVE, so
    # _find_workspace never sees the real missions/ tree and the gate takes the
    # inert path -- silently allowing exactly the guarded MCP calls this
    # fallback exists to catch.
    return _strip_leading_drive_slash(root) if strip else root


def _candidate_workspaces(call: dict) -> list[Path]:
    """EVERY workspace this payload could belong to, in priority order.

    Deliberately a list, not a single answer. An earlier version returned the
    first location holding a `missions/` directory, and that was a REPRODUCED
    FALSE ALLOW: `_find_workspace` only asks "does a missions/ dir exist here",
    which says nothing about whether a mission there is active, armed, or
    relevant. With workspace_roots [A, B] where A holds a CANCELLED mission and
    B holds an ACTIVE enforce mission whose guard matches, first-wins gated
    against A, hit NoActiveMission, and allowed the call SILENTLY -- while the
    reverse order blocked it. Root order is set by the IDE, not the mission
    author, so ordinary usage decided whether enforcement happened.

    That also falsified the claim this function used to carry ("searching more
    places can only add blocks"): true only if "found" means "found an
    actionable decision", whereas the code meant "found a directory".

    The caller therefore gates against EVERY candidate and blocks if ANY of
    them blocks. A false block names its rule and is discharged by an amend; a
    false allow silently retires custody. cwd is placed first so its verdict is
    reported first, but it no longer masks the others.

    No usable location yields an EMPTY list -- inert, never `Path(".")`, which
    would search from wherever the hook process happens to be running."""
    candidates: list[Path] = []

    def consider(location: str) -> None:
        if not location:
            return
        # A RELATIVE location is not a usable root. `_find_workspace` walks
        # ancestors, and a relative path's chain terminates at `.` -- so a
        # root the process cannot interpret would resolve to "wherever the
        # hook happens to be running", which this function's own docstring
        # promises never happens. Observed with a `file://` URI fed through as
        # a literal (`Path("file:///c:/w")` is relative on both platforms) and
        # with the stripped bare-drive form on POSIX, where `c:/work` is
        # relative. Both produced `Path(".")` as a candidate: a block naming a
        # rule from a mission the user is not in, and an entry written into
        # that unrelated mission's guard log.
        # NATIVE absoluteness, because `_find_workspace` parses with the
        # native `Path`. An earlier attempt accepted "absolute under either
        # flavour", which let `c:/work/project` through on POSIX -- absolute
        # to PureWindowsPath, relative to the `Path` that actually consumes it,
        # so the ancestor walk still reached `.`. A gate whose notion of valid
        # differs from its consumer's is not a gate.
        #
        # This is also what makes the two readings correct per platform rather
        # than by luck: on POSIX the UNSTRIPPED "/c:/work" is native-absolute
        # and the stripped form is not; on Windows the reverse. Each platform
        # accepts exactly the reading that is real there.
        try:
            if not Path(location).is_absolute():
                return
        except (OSError, ValueError):
            return
        for workspace in _find_workspaces(location):
            if workspace not in candidates:
                candidates.append(workspace)

    consider(call.get("cwd") or "")
    roots = call.get("workspace_roots")
    if isinstance(roots, list):  # a bare string would iterate per-character
        for root in roots:
            try:
                location = _root_location(root)
            except Exception as exc:                      # noqa: BLE001
                # `urlparse` raises ValueError on a malformed authority
                # ("file://[oops" -> Invalid IPv6 URL). Unhandled, it escaped
                # discovery into the outer handler and returned ALLOW with an
                # empty stderr -- one malformed IDE-supplied root silently
                # disarming an armed guard, which is verbatim the fail-open
                # the per-candidate handler downstream was added to close.
                print(f"custody-gate: unreadable workspace root, skipping: "
                      f"{type(exc).__name__}", file=sys.stderr)
                continue
            consider(location)
            # '/c:/work/project' has TWO readings: a Windows drive path (which
            # _root_location resolves) and, on POSIX, a perfectly legal
            # absolute path, because ':' is an ordinary filename character
            # there. Choosing one platform's reading gets the other wrong, and
            # both wrong answers end identically: no workspace found, no
            # mission consulted, the guarded call SILENTLY ALLOWED.
            #
            # So neither is chosen. Both are offered, _find_workspace discards
            # whichever has no missions/ tree, and any-blocks-wins covers the
            # rest -- the same reasoning that made this function return a list
            # instead of a first-wins answer.
            # The alternate reading is the UNSTRIPPED, DECODED path -- never
            # the raw string. For a bare root those are the same thing, but for
            # a URI they are not: on POSIX `file:///c:/ok` decodes to the valid
            # absolute path `/c:/ok`, while the raw URI is relative to `Path`
            # and gets rejected. Offering the raw form meant BOTH readings were
            # discarded there and an armed mission under that root failed open.
            #
            # This also covers object-shaped roots, which an `isinstance(root,
            # str)` guard previously skipped entirely.
            alternate = _root_location(root, strip=False)
            if alternate and alternate != location:
                consider(alternate)
    return candidates


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
        workspaces = _candidate_workspaces(call)
        if not workspaces:
            return 0  # inert fast path: no custody state at any reported location
        from custody_gate import run_gate
        tool_call = {"tool_name": call["tool_name"],
                     "command": call.get("command"),
                     "file_path": call.get("file_path"),
                     "tool_input": call.get("tool_input")}
        # The session's binding channel, best-effort: the harness process
        # env is what this hook inherits. Under OD-4 refined ("Self-arm at
        # open, union at approve") the binding SELF-ARMS the named
        # mission's own guards; it can only ADD exposure (a name matching
        # no mission dir changes nothing), so the lower-provenance env
        # never widens what a session may do -- only what it may not.
        bound = os.environ.get("ZMS_MISSION_ID", "").strip() or None
        # ANY candidate blocking blocks the call. A custody error on one
        # candidate must not skip the rest: an unreadable mission in the first
        # workspace would otherwise suppress a real block from the second,
        # turning a tamper signal into a silent allow.
        for workspace in workspaces:
            try:
                verdict = run_gate(
                    workspace, tool_call, actor="hook:custody-gate",
                    session_id=call.get("session_id", ""),
                    harness=args.harness, bound_mission=bound)
            except CustodyError as exc:
                # Tamper keeps its own distinct, greppable signal: a session log
                # must be searchable for TAMPER, and folding it into the generic
                # branch below silently retired that marker.
                print(f"custody gate: TAMPER/custody error detected at "
                      f"{workspace}, failing open for that mission: "
                      f"{type(exc).__name__}: {exc}", file=sys.stderr)
                continue
            except Exception as exc:
                # Deliberately broad, and per-candidate. Catching ONLY
                # CustodyError let every other exception -- Mission.load
                # intentionally propagates environmental OSErrors such as
                # PermissionError -- escape to the outer handler, which returns
                # 0 immediately. One unreadable root then silently suppressed
                # every later root's block: root ORDER causing a false allow,
                # the exact defect this loop was built to close. Fail open for
                # the candidate that failed, never for the rest.
                print(f"custody gate: error evaluating {workspace}, failing "
                      f"open for that mission only: "
                      f"{type(exc).__name__}: {exc}", file=sys.stderr)
                continue
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
