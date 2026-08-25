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

from custody_store import StoreError
from custody_mission import (
    CustodyError,
    Mission,
    _approved_by_chain,
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
    the raw spelling allowed a false allow (es#137).

    INHERITED REASONING (from test_glob_overmatch_still_held, deleted by the
    es#137 fix): "'..' is not collapsed by normalization, so it over-matches --
    the safe direction (a false block names its rule; a false allow retires
    custody)". Collapsing retired that OVER-match protection for guard matching
    and replaced it with textual resolution. The residual, in the false-allow
    direction: this collapse is LEXICAL, while the kernel resolves ``..`` only
    AFTER following symlinks -- a write spelled through a symlinked parent can
    land inside a guarded tree without matching an armed guard (recorded as
    KL-GUARD-LEXICAL / CLM-MC-GUARD-LEXICAL; pinned by
    test_guard_match_is_lexical_symlinked_parent_diverges). Do not "fix" this
    by resolving symlinks here without a fresh custody review: realpath calls
    inside the gate change its failure modes on broken links and network
    filesystems."""
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


def _union_entries(workspace: Path, actor: str) -> tuple[list[dict], list[dict]]:
    """Assemble the guard union (es#173 section 2): every ACTIVE mission,
    chain-verified and manifest-verified, carrying the OD-4 approval flag
    (`_approved_by_chain` -- the chain test, so a never-approved mission
    wedged in `reopened` arms nothing).

    A mission that fails to load or verify joins `degraded` instead: its
    guards CANNOT be trusted, so they are not enforced -- and every caller
    must SAY so, because a silently shrunken union is the old
    MultipleActiveMissions fail-open decoy rebuilt one layer down."""
    active, skipped = Mission._discover(workspace)
    degraded = [dict(s) for s in skipped]
    entries: list[dict] = []
    for e in active:
        mission = Mission(e["store"], workspace, actor)
        try:
            # status() re-reads the chain and verifies the manifest, so the
            # authority evaluated is the chain-verified latest -- and a
            # tampered manifest degrades instead of arming. This also covers
            # the mid-evaluation epoch flip the old two-read gate special-
            # cased: a writer publishing the first @2 between discovery and
            # this read surfaces HERE, as a degraded entry.
            latest = mission.status()
        except (StoreError, ValueError, CustodyError) as exc:
            reason = f"{e['name']}: {type(exc).__name__}: {exc}"
            # Tamper keeps its own distinct, greppable stderr signal: a
            # session log must be searchable for TAMPER (the hook's contract
            # since before the union), and the union fold must not silently
            # retire that marker.
            print(("custody gate: TAMPER/custody error reading mission "
                   + e["name"] + " -- its guards are NOT enforced (union "
                   "degraded): " + reason)
                  .encode("ascii", "backslashreplace").decode("ascii"),
                  file=sys.stderr)
            degraded.append({
                "name": e["name"], "kind": type(exc).__name__,
                "reason": reason})
            continue
        entries.append({"name": e["name"], "mission": mission,
                        "latest": latest,
                        "approved": _approved_by_chain(e["store"])})
    return entries, degraded


def evaluate_union(entries: list[dict], tool_call: dict,
                   own_mission: str | None = None) -> list[dict]:
    """Every matching (mission, rule) pair across the union of APPROVED
    missions' armed guards, plus the bound mission's OWN guards -- ALL
    matches, not first: the operator discharging a block needs the full
    bill (es#173 section 2).

    OD-1 UNION-ALWAYS: callers pass every entry; binding routes authority
    and never REMOVES exposure. OD-4 REFINED (operator ruling 2026-08-25:
    "Self-arm at open, union at approve"): a mission's armed guards bind
    its OWN session -- a call bound to it via `own_mission` -- from the
    moment open arms them, exactly as the pre-union core behaved; they
    join the fleet-wide union only once the mission is chain-approved.
    Unbound calls see only the approved union, so an unblessed draft
    still cannot block OTHER sessions -- membership is decided here, in
    the one place, and binding can only ADD the bound mission's own
    guards (the safe direction: a false block names its rule and is
    discharged by amend)."""
    matches: list[dict] = []
    for entry in entries:
        if not entry.get("approved") and entry["name"] != own_mission:
            continue
        authority = entry["latest"]["manifest"]["authority"]
        mode = authority.get("guard_mode")
        guards = authority.get("actuator_guards")
        if not mode or not guards:
            continue
        for rule in guards:
            if _tool_in(rule, tool_call.get("tool_name", "")) \
                    and _patterns_match(rule, tool_call):
                matches.append({"mission": entry["name"],
                                "rule": rule["name"], "mode": mode,
                                "decision": ("block" if mode == "enforce"
                                             else "allow")})
    return matches


def effect_rule_matches(rule: dict, artifact_relpath: str) -> bool:
    """Does an armed guard bind the `effect` verb's write to this path?
    (es#173, OD-2: effect IS the file write.)

    `tool_names` -- a harness concept -- deliberately does NOT filter here:
    the effect verb is not a harness tool, and a guard that binds a path
    must bind the path however the write is spelled, or the custody CLI
    itself remains the one unmediated writer (the FATAL-2 hole restated).
    Over-matching is this module's documented safe direction: a false block
    names its rule and is discharged per-mission by amend. Rules carrying
    only command_regexes never match an effect -- there is no command."""
    target = _guard_norm_path(artifact_relpath)
    return any(_guard_glob_regex(glob).match(target)
               for glob in rule["path_globs"])


def evaluate_effect_union(entries: list[dict], artifact_relpath: str,
                          own_mission: str | None = None) -> list[dict]:
    """Every matching (mission, rule) pair for an `effect` write, across
    the union of APPROVED missions' armed guards plus the acting
    mission's OWN guards -- the OD-2 surface, sharing OD-4 REFINED
    membership with `evaluate_union` ("Self-arm at open, union at
    approve", operator ruling 2026-08-25): a draft mission's own effect
    is checked against its own guards from open, and against the
    approved union; its guards bind no OTHER mission pre-approve.
    Entries carry {"name", "authority", "approved"}."""
    matches: list[dict] = []
    for entry in entries:
        if not entry.get("approved") and entry["name"] != own_mission:
            continue
        authority = entry["authority"]
        mode = authority.get("guard_mode")
        guards = authority.get("actuator_guards")
        if not mode or not guards:
            continue
        for rule in guards:
            if effect_rule_matches(rule, artifact_relpath):
                matches.append({"mission": entry["name"],
                                "rule": rule["name"], "mode": mode,
                                "decision": ("block" if mode == "enforce"
                                             else "allow")})
    return matches


def _degraded_disclosure(degraded: list[dict]) -> str:
    names = ", ".join(sorted(d["name"] for d in degraded))
    return (f" UNION DEGRADED: mission dir(s) {names} unreadable -- their "
            "guards are NOT enforced; repair or resolve them before "
            "relying on the union.")


def _log_matches(workspace: Path, matches: list[dict], tool_call: dict, *,
                 actor: str, session_id: str, harness: str) -> None:
    """One guard-log append per MATCHING (mission, rule) pair, into that
    mission's own dir: each mission's audit trail must be complete from its
    own dir (es#173 section 2). Best-effort exactly as before -- the append
    is audit, the VERDICT is not, and a log failure must never flip a block
    into an allow."""
    command = tool_call.get("command") or ""
    for row in matches:
        entry = {
            "utc": now_utc(),
            "actor": actor,
            "session_id": session_id,
            "harness": harness,
            "mode": row["mode"],
            "decision": row["decision"],
            "rule": row["rule"],
            "tool_name": tool_call.get("tool_name", ""),
            "command_preview": command[:_PREVIEW],
            "file_path": tool_call.get("file_path"),
        }
        try:
            _append_guard_log(workspace / "missions" / row["mission"], entry)
        except Exception as exc:
            print(f"custody gate: guard-log append failed for "
                  f"{row['mission']} ({type(exc).__name__}: {exc}); verdict "
                  f"{row['decision']} stands but was not logged",
                  file=sys.stderr)


def run_gate(workspace: Path, tool_call: dict, *, actor: str,
             session_id: str = "", harness: str = "",
             bound_mission: str | None = None) -> dict:
    """Evaluate a harness tool call against the UNION of all approved
    missions' armed guards (es#173, OD-1 UNION-ALWAYS): bound or not, every
    gate-routed call sees every approved mission's guards -- if binding to
    mission A exempted a call from mission B's guards, every guard would be
    voluntary the moment two missions coexist. Under OD-4 REFINED
    ("Self-arm at open, union at approve", operator ruling 2026-08-25)
    `bound_mission` additionally SELF-ARMS: a call bound to mission M is
    also checked against M's own guards even before M is approved, so a
    binding can ADD exposure but never remove any (case row 16 keeps its
    teeth: a bad binding is loud on stderr, names no active mission, and
    the approved union is evaluated regardless).

    Plurality is legal, so MultipleActiveMissions is gone as an inert
    cause -- the fail-open decoy is removed not by handling the error
    better but by making the state legal. The hook path stays fail-open for
    corrupt or epoch-skewed stores (a hook must never brick the tool loop),
    but an allow that dropped a mission's guards must SAY so, in the
    verdict reason and on stderr (case rows 22, B22)."""
    workspace = Path(workspace)
    if bound_mission:
        try:
            Mission.load(workspace, actor=actor, mission_id=bound_mission)
        except (CustodyError, StoreError) as exc:
            print(f"custody gate: session binding invalid "
                  f"({type(exc).__name__}: {exc}) -- exposure unaffected: "
                  "the union is evaluated regardless of binding",
                  file=sys.stderr)
    entries, degraded = _union_entries(workspace, actor)
    if not entries:
        skew = [d for d in degraded if d["kind"] == "EpochSkew"]
        if skew:
            # VERSION SKEW IS NOT AN EMPTY WORKSPACE. A store from a newer
            # contract epoch fails validation, gets skipped, and leaves the
            # workspace looking missionless -- so an armed mission that
            # BLOCKED reports `allow` the moment its epoch moves ahead of
            # this reader. Named on the verdict and on stderr; the posture
            # stays allow/inert because inverting it would strand the
            # workspace with no verb to resolve it. CLAIMS, not "is": this
            # reader cannot tell a genuine newer store from a corrupt or
            # relabelled one.
            detail = "; ".join(d["reason"] for d in skew)
            print(f"custody gate: MISSION STORE CLAIMS A NEWER EPOCH THAN "
                  f"THIS READER under {workspace} -- gate inert and guards "
                  f"NOT enforced. Read it with an updated custody "
                  f"plugin/CLI to find out whether the store is genuinely "
                  f"newer or corrupt; this reader cannot tell. "
                  f"Detail: {detail}", file=sys.stderr)
            return {"decision": "allow", "matched": False, "rule": None,
                    "mode": "inert",
                    "reason": ("gate inert: mission store CLAIMS a contract "
                               "epoch newer than this reader -- guards are "
                               "NOT enforced here, and this reader cannot "
                               "tell a genuine newer store from a corrupt "
                               f"or relabelled one ({detail})")}
        reason = "gate inert: NoActiveMission"
        if degraded:
            # BOTH CHANNELS, like the entries-present path below and the
            # EpochSkew branch above. This branch composed the disclosure into
            # `reason` and printed nothing, so a workspace whose ONLY missions
            # were unreadable produced an `allow` whose sole stderr line
            # ("skipping unreadable mission dir") never says guards are not
            # enforced -- the worst case wearing the quietest signal.
            reason += _degraded_disclosure(degraded)
            print("custody gate:" + _degraded_disclosure(degraded),
                  file=sys.stderr)
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert", "reason": reason}
    matches = evaluate_union(entries, tool_call, own_mission=bound_mission)
    disclosure = ""
    if degraded:
        # An allow that silently dropped a mission's guards would be the
        # section-0 decoy rebuilt one layer down: disclose in BOTH channels.
        disclosure = _degraded_disclosure(degraded)
        print("custody gate:" + disclosure, file=sys.stderr)
    if matches:
        _log_matches(workspace, matches, tool_call, actor=actor,
                     session_id=session_id, harness=harness)
    blocking = [m for m in matches if m["decision"] == "block"]
    if blocking:
        pairs = "; ".join(f"mission={m['mission']} rule={m['rule']}"
                          for m in blocking)
        return {
            "decision": "block", "matched": True,
            "rule": blocking[0]["rule"], "mode": "enforce",
            "matches": matches,
            "reason": (
                f"custody guard(s) matched this call: {pairs}. No mission "
                "envelope discharges them. This gate reads ONLY guard_mode "
                "and actuator_guards -- recording amendment TEXT does not "
                "discharge a block, however clearly it grants the work. "
                "Discharge is PER-MISSION: an amend recorded in one "
                "mission discharges that mission's rule only, so a call "
                "blocked by several missions needs each one's amend. The "
                "exits, per matching mission (bind with --mission <id>): "
                "change the rule that matched via `amend --guards-file`, "
                "or `amend --guard-mode audit` to retire that mission's "
                "guard set, or stop. Both amend forms are recorded, "
                "chained and comparable; narrating a grant is not. NOTE: "
                "if a rule covers the shell itself, the amend command is "
                "blocked by the same rule -- run it OUT OF BAND (a session "
                "or terminal this hook does not gate). The gate "
                "deliberately has no self-repair exemption: a rule that "
                "exempted its own discharge command would be a hole shaped "
                "exactly like the thing it guards." + disclosure)}
    if matches:
        pairs = "; ".join(f"mission={m['mission']} rule={m['rule']}"
                          for m in matches)
        return {"decision": "allow", "matched": True,
                "rule": matches[0]["rule"], "mode": matches[0]["mode"],
                "matches": matches,
                "reason": (f"custody guard(s) matched (audit mode): {pairs}"
                           + disclosure)}
    armed = [e for e in entries
             if (e.get("approved") or e["name"] == bound_mission)
             and e["latest"]["manifest"]["authority"].get("guard_mode")
             and e["latest"]["manifest"]["authority"].get("actuator_guards")]
    if not armed:
        # Case row 7: a lone unapproved draft (or unguarded missions only)
        # contributes nothing to an UNBOUND call -- allow, disclosed as
        # such. Its own bound session is self-armed above (OD-4 refined),
        # so this branch is reached only when no evaluated source exists.
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert",
                "reason": "no approved mission guards armed" + disclosure}
    # The reported POSTURE of a mixed union must not depend on directory
    # names: `armed[0]` is the alphabetically first armed mission, so
    # `a-audit` + `z-enforce` reported "audit" while the workspace was
    # genuinely enforcing. Report the strongest posture present, and say so
    # when the union is mixed. (Reporting only -- the decision here is
    # allow/unmatched either way.)
    modes = sorted({e["latest"]["manifest"]["authority"]["guard_mode"]
                    for e in armed})
    mode = "enforce" if "enforce" in modes else modes[0]
    mixed = ""
    if len(modes) > 1:
        mixed = (" (union is MIXED: "
                 + ", ".join(
                     f"{e['name']}="
                     f"{e['latest']['manifest']['authority']['guard_mode']}"
                     for e in sorted(armed, key=lambda e: e["name"]))
                 + ")")
    return {"decision": "allow", "matched": False, "rule": None,
            "mode": mode,
            "reason": "no guard matched" + mixed + disclosure}
