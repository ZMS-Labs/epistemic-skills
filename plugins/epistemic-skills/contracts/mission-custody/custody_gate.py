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

from custody_store import EpochSkew
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
    (_ascii_case_fold -- never str.casefold).

    Anchored with \\Z, never '$': '$' also matches just before a TRAILING
    NEWLINE, so the glob 'safe.txt' matched the distinct file 'safe.txt\\n'
    -- a false CLEAN on the scope.in side, where a path one byte outside the
    declaration read as inside it. re.DOTALL stays: '*' and '**' must still
    span a newline INSIDE a name; only the one-character terminal tolerance
    dies. (re.fullmatch at every call site was measured observably identical
    in every grid cell -- it buys nothing while moving the guarantee from one
    compiler to four call sites.) The same '$' tolerance survives verbatim in
    operator-authored `command_regexes`, whose semantics belong to the
    author, not this compiler -- disclosed in SECURITY.md."""
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
    return re.compile("".join(out) + r"\Z", re.DOTALL)


def _fold(text: str) -> str:
    return _ascii_case_fold(text) if os.name == "nt" else text


def _collapse_parent_segments(path: str) -> str:
    """Collapse ``..`` segments for guard path matching only.

    Scope comparison keeps ``..`` lexical (disclosed). Harness ``file_path``
    values may carry parent segments that resolve inside a guarded tree; matching
    the raw spelling allowed a false allow (es#137)."""
    norm = path.replace("\\", "/")
    parts = norm.split("/")
    out: list[str] = []
    for part in parts:
        if part == "..":
            if out and out[-1] != ".." and not (len(out) == 1 and out[0].endswith(":")):
                out.pop()
            else:
                out.append("..")
        elif part != ".":
            out.append(part)
    return "/".join(out)


def _norm_path(path: str) -> str:
    return _fold(_normalize_relpath(path.replace("\\", "/")))


def _guard_norm_path(path: str) -> str:
    """Normalize a harness file_path for guard glob matching (es#137).

    Scope comparison keeps ``..`` lexical via ``_norm_path``; only guard
    matching collapses parent segments so a resolved path cannot bypass an
    armed rule."""
    return _fold(_collapse_parent_segments(_normalize_relpath(path.replace("\\", "/"))))


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
        target = _guard_norm_path(file_path)
        for glob in rule["path_globs"]:
            if _guard_glob_regex(glob).match(target):
                return True
    return False


def _guard_glob_regex(glob: str) -> "re.Pattern[str]":
    """Compile a guard path glob, honouring the trailing-separator
    directory marker (es#155, gate half).

    'M:/Media/' normalized to an exact 'M:/Media' and bound NOTHING under
    the directory -- for an ARMED guard that is a silent false-allow on the
    entire subtree the operator evidently meant. Expanded to the compiler's
    trailing-base form, the same directory-marker reading scope entries and
    amendment tokens already use; forward and Windows separators alike.

    OPERATOR NOTICE (mandatory, per the es#150 adjudication): an armed
    guard whose path_globs carry a trailing separator becomes MORE
    RESTRICTIVE on upgrade -- it now matches the directory and everything
    under it where it previously matched almost nothing. That is the
    over-match direction (a false block names its rule and is discharged
    by an amend), but it is a behavior change on an enforcement surface,
    disclosed in SECURITY.md rather than slipped in."""
    norm = _fold(_normalize_relpath(glob))
    if not norm:
        # '.', './', '.\', './.': normalization yields the EMPTY path --
        # the workspace itself -- and compiling '' produces a regex
        # matching nothing, silently: an ARMED guard the operator believes
        # covers everything, covering nothing at all. The DOT spellings
        # express that intent, so they compile to match every target --
        # the over-match direction (a false block names its rule and
        # discharges by amend), and the one that also catches absolute
        # respellings of workspace files.
        #
        # The literal EMPTY STRING is not one of them: it expresses no
        # directory intent (a placeholder, most plausibly), it passes the
        # manifest validator today, and it has always been inert --
        # flipping it to block-everything would be an enforcement change
        # on armed fleets that the SECURITY.md notice (scoped to
        # trailing-separator markers) never disclosed. It keeps its
        # historical behavior: matches nothing real.
        segments = glob.replace("\\", "/").split("/")
        if any(seg == "." for seg in segments) \
                and all(seg in ("", ".") for seg in segments):
            return _glob_regex("**")
        return _glob_regex(norm)
    if glob.replace("\\", "/").endswith("/"):
        # The FILESYSTEM ROOT is the one spelling normalization leaves with
        # its separator attached ('/' stays '/'), so appending the marker
        # built '//**' -- which compiles to a regex matching the root and
        # NOTHING under it: a guard of '/' (block all absolute writes)
        # silently allowed every descendant. Drive roots are unaffected
        # ('C:/' normalizes to 'C:'). Compile the root as the bare-subtree
        # form instead, which matches every absolute target and no
        # relative one.
        if norm == "/":
            return _glob_regex("/**")
        if norm == "**" or norm.endswith("/**"):
            # 'foo/**/' already carries subtree semantics INCLUDING the
            # base; appending another '/**' compiled to 'foo/.*(?:/.*)?',
            # which requires a separator after 'foo' -- a write to the
            # base itself was silently allowed where the plain 'foo/**'
            # spelling matches it.
            return _glob_regex(norm)
        return _glob_regex(norm + "/**")
    return _glob_regex(norm)


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
                            "the mission envelope does not discharge it. This "
                            "gate reads ONLY guard_mode and actuator_guards -- "
                            "recording amendment TEXT does not discharge a "
                            "block, however clearly it grants the work. The "
                            "exits are: change the rule that matched "
                            f"('{rule['name']}') via `amend --guards-file`, or "
                            "`amend --guard-mode audit` to retire the whole "
                            "guard set, or stop. Both amend forms are "
                            "recorded, chained and comparable; narrating a "
                            "grant is not. NOTE: if this rule covers the "
                            "shell itself, the amend command is blocked by "
                            "the same rule -- run it OUT OF BAND (a session "
                            "or terminal this hook does not gate). The gate "
                            "deliberately has no self-repair exemption: a "
                            "rule that exempted its own discharge command "
                            "would be a hole shaped exactly like the thing "
                            "it guards.")}
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
        # VERSION SKEW IS NOT AN EMPTY WORKSPACE. A store from a newer contract
        # epoch fails validation, gets skipped, and leaves the workspace looking
        # missionless -- so an armed mission that BLOCKED reports `allow` with
        # reason `NoActiveMission` the moment its epoch moves ahead of this
        # reader (measured). That reason is false and points the operator at the
        # wrong repair: the mission is fine, the READER is old.
        #
        # This is the failure mode the first contract@2 write would hit fleet-
        # wide (es#118), so it is named on the verdict itself and on stderr,
        # where the MultipleActiveMissions decoy warning already lives. The
        # posture is unchanged -- still allow, still inert -- because inverting
        # it would strand the workspace with no verb to resolve it.
        detail = str(exc)
        if "EpochSkew" in getattr(exc, "skipped_kinds", ()):
            print(f"custody gate: MISSION STORE CLAIMS A NEWER EPOCH THAN "
                  f"THIS READER under {workspace} -- gate inert and guards NOT "
                  f"enforced. Read it with an updated custody plugin/CLI to "
                  f"find out whether the store is genuinely newer or corrupt; "
                  f"this reader cannot tell. Detail: {detail}", file=sys.stderr)
            # CLAIMS, matching epoch_skew(). A categorical "is from a newer
            # epoch" sends the operator to upgrade when the store may in fact
            # be tampered -- the same over-claim corrected in the helper and
            # SECURITY.md, left standing in the one string a consumer actually
            # branches on.
            return {"decision": "allow", "matched": False, "rule": None,
                    "mode": "inert",
                    "reason": ("gate inert: mission store CLAIMS a contract "
                               "epoch newer than this reader -- guards are NOT "
                               "enforced here, and this reader cannot tell a "
                               "genuine newer store from a corrupt or "
                               f"relabelled one ({detail})")}
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
    try:
        latest = mission.status()
    except EpochSkew as exc:
        # THE CHAIN IS READ TWICE. `Mission.load` resolves the mission, then
        # status() re-reads it -- so a writer publishing the first @2 between
        # those two reads makes the skew surface HERE, where the handler above
        # never sees it. Before this, a direct caller got a raw exception and
        # the hook fell through to its generic error path, both of them missing
        # the stale-reader verdict this change exists to deliver. That window is
        # narrow but it is exactly the contract@2 rollout moment.
        print(f"custody gate: MISSION STORE BEGAN CLAIMING A NEWER EPOCH "
              f"mid-evaluation under {workspace} -- gate inert and guards NOT "
              f"enforced. Read it with an updated custody plugin/CLI; this "
              f"reader cannot tell a genuine newer store from a corrupt one. "
              f"Detail: {exc}", file=sys.stderr)
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert",
                "reason": ("gate inert: mission store CLAIMS a contract epoch "
                           "newer than this reader -- guards are NOT enforced "
                           "here, and this reader cannot tell a genuine newer "
                           f"store from a corrupt or relabelled one ({exc})")}
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
