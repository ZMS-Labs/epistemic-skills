#!/usr/bin/env python3
"""Stage-C gate: evaluate a harness tool call against the active mission's
operator-approved actuator guards (mission-manifest@1 optional fields).

Read-only by contract: the only write anywhere in this module is an append to
missions/<id>/guard-log.jsonl on a MATCH -- the checkpoint chain is never
touched (verified by test: run-gate-chain-byte-identical). The checkpoint read
goes through MissionStore.load_latest, so the manifest evaluated is the
chain-verified latest.

Matching is deliberately over-broad (handoff error-direction lesson): a false
block names its rule and is discharged by an amend; a false allow silently
retires custody of the actuator class the tracer retro named.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from custody_mission import (
    Mission,
    MultipleActiveMissions,
    NoActiveMission,
    _ascii_case_fold,
    _normalize_relpath,
    now_utc,
)

GUARD_LOG_NAME = "guard-log.jsonl"
_PREVIEW = 120


def _glob_regex(glob: str) -> "re.Pattern[str]":
    """Translate a path glob: '**' crosses separators ('**/' matches ZERO or
    more segments; a trailing '/**' also matches the base path itself),
    '*'/'?' stay in-segment. Paths are normalized ('\\' -> '/', no './', no
    trailing '/') before match; on NT both sides fold A-Z only
    (_ascii_case_fold -- never str.casefold)."""
    trailing_base = glob.endswith("/**")
    if trailing_base:
        glob = glob[:-3]
    out: list[str] = []
    i = 0
    while i < len(glob):
        if glob[i] == "*":
            if glob[i:i + 3] == "**/":
                out.append("(?:.*/)?")
                i += 3
            elif glob[i:i + 2] == "**":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    if trailing_base:
        out.append("(?:/.*)?")
    return re.compile("".join(out) + "$", re.DOTALL)


def _fold(text: str) -> str:
    return _ascii_case_fold(text) if os.name == "nt" else text


def _norm_path(path: str) -> str:
    return _fold(_normalize_relpath(path.replace("\\", "/")))


def _tool_in(rule: dict, tool_name: str) -> bool:
    return tool_name in rule["tool_names"]


def _patterns_match(rule: dict, tool_call: dict) -> bool:
    command = tool_call.get("command")
    if not command:
        # MCP and other non-shell tools carry their payload as structured
        # arguments, not a command string. Serializing (sorted keys, so the
        # haystack is deterministic) lets command_regexes cover URLs, paths,
        # and flags inside those arguments. Deliberately crude: over-matching
        # is the safe direction, and a false block names its rule.
        tool_input = tool_call.get("tool_input")
        if tool_input is not None:
            command = json.dumps(tool_input, sort_keys=True)
    if command:
        for pattern in rule["command_regexes"]:
            if re.search(pattern, command):
                return True
    file_path = tool_call.get("file_path")
    if file_path:
        target = _norm_path(file_path)
        for glob in rule["path_globs"]:
            if _glob_regex(_fold(_normalize_relpath(glob))).match(target):
                return True
    return False


def evaluate(authority: dict, tool_call: dict) -> dict:
    mode = authority.get("guard_mode")
    guards = authority.get("actuator_guards")
    if not mode or not guards:
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": mode or "inert", "reason": "no guards armed"}
    for rule in guards:
        if _tool_in(rule, tool_call.get("tool_name", "")) \
                and _patterns_match(rule, tool_call):
            if mode == "enforce":
                return {"decision": "block", "matched": True,
                        "rule": rule["name"], "mode": mode,
                        "reason": (
                            f"custody guard '{rule['name']}' matched this call; "
                            "the mission envelope does not discharge it -- record "
                            "an operator grant via `amend` or stop")}
            return {"decision": "allow", "matched": True, "rule": rule["name"],
                    "mode": mode,
                    "reason": f"custody guard '{rule['name']}' matched (audit mode)"}
    return {"decision": "allow", "matched": False, "rule": None,
            "mode": mode, "reason": "no guard matched"}


def _append_guard_log(mission_dir: Path, entry: dict) -> None:
    path = mission_dir / GUARD_LOG_NAME
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def run_gate(workspace: Path, tool_call: dict, *, actor: str,
             session_id: str = "", harness: str = "") -> dict:
    workspace = Path(workspace)
    try:
        mission = Mission.load(workspace, actor=actor)
    except NoActiveMission as exc:
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert", "reason": f"gate inert: {type(exc).__name__}"}
    except MultipleActiveMissions as exc:
        # Fail-open posture stands (a hook must never brick the tool loop on
        # discovery ambiguity), but a decoy second mission silently disarming
        # the gate must not pass quietly.
        print(f"custody gate: MULTIPLE ACTIVE MISSIONS under {workspace} -- "
              "gate inert, enforcement degraded to convention-held; resolve "
              "the duplicate mission dirs before relying on guards",
              file=sys.stderr)
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert", "reason": f"gate inert: {type(exc).__name__}"}
    latest = mission.status()
    verdict = evaluate(latest["manifest"]["authority"], tool_call)
    if verdict["matched"]:
        command = tool_call.get("command") or ""
        entry = {
            "utc": now_utc(),
            "actor": actor,
            "session_id": session_id,
            "harness": harness,
            "mode": verdict["mode"],
            "decision": verdict["decision"],
            "rule": verdict["rule"],
            "tool_name": tool_call.get("tool_name", ""),
            "command_preview": command[:_PREVIEW],
            "file_path": tool_call.get("file_path"),
        }
        try:
            _append_guard_log(mission.store.mission_dir, entry)
        except Exception as exc:
            # The audit append is best-effort; the VERDICT is not. A log
            # failure must never flip a block into an allow.
            print(f"custody gate: guard-log append failed "
                  f"({type(exc).__name__}: {exc}); verdict "
                  f"{verdict['decision']} stands but was not logged",
                  file=sys.stderr)
    return verdict
