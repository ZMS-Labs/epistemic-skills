#!/usr/bin/env python3
"""Thin argparse CLI over the Mission lifecycle API (custody_mission.Mission).
No logic beyond translation: every subcommand parses flags, calls exactly one
Mission method, and prints exactly what that method returns -- the new
revision number for lifecycle mutations, the receipt JSON for effect and
reconcile, the checkpoint JSON for status.

Discovery is pathless by contract: no subcommand other than `open` accepts a
--mission-path or --mission-id flag. Under es#173 concurrent missions a
session declares which mission it acts under through exactly two channels --
`--mission <id>` (per-call, wins) and the `ZMS_MISSION_ID` environment
variable (session default); flag > env > unbound. Unbound, `Mission.load()`
resolves the single active mission (unchanged), refuses `BindingRequired`
when several are active, and a stale binding refuses `BindingInvalid` --
it never falls through to discovery.

Exit codes: 0 success; 2 usage/refusal (argparse prints usage; a CustodyError
subclass prints its class name + message to stderr); 3 drift detected on
`resume`. `gate` adds: exit 2 = block (a guarded actuator fired outside the
armed envelope), exit 0 = allow. Exit 2 is deliberately uniform across
usage/refusal/block: a `gate` block is distinguishable by the verdict JSON
on stdout ("decision": "block"), not by a dedicated exit code. On a clean
resume the drift list on stdout is empty by contract; a one-line summary
goes to stderr so vacuous cleanliness (zero receipts on record) is visible
instead of indistinguishable from verified cleanliness.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from custody_mission import CustodyError, Mission, uncompared_scope_entries
from custody_store import StoreError


def _print_status(checkpoint: dict) -> None:
    print(json.dumps(checkpoint, indent=2, sort_keys=True, ensure_ascii=True))


def _display_safe(text: str, *, preserve_printable_syntax: bool = False) -> str:
    """Render terminal text without allowing control-character execution.

    Raw fields use full JSON string escaping (minus the surrounding quotes).
    A completed refusal message can also contain trusted printable syntax --
    notably the JSON-quoted ``--scope-ack`` token that the acceptor must copy
    exactly.  In that mode preserve printable ASCII quotes and backslashes,
    while still JSON-escaping every control and non-ASCII code point.  Both
    modes therefore prevent forged rows and ANSI execution and remain safe
    on an ASCII-only console.  JSON document surfaces get the same guarantees
    from ``_print_status``'s ``ensure_ascii=True``.
    """
    if preserve_printable_syntax:
        return "".join(
            char if " " <= char <= "~"
            else json.dumps(char, ensure_ascii=True)[1:-1]
            for char in text
        )
    return json.dumps(text, ensure_ascii=True)[1:-1]


def _read_content(args: argparse.Namespace) -> str:
    """Artifact bodies, with the SAME refusal contract `_read_text` carries.

    `_read_text` was hardened for missing and non-UTF-8 files and this reader
    was not, so the ONE flag an operator uses most (`--content-file`) answered
    an ordinary input error with a traceback and exit 1 -- indistinguishable
    from an internal crash, and outside this module's documented 0/2/3
    contract. Measured: `effect --content-file <missing>` -> FileNotFoundError,
    rc 1.

    Deliberately NOT sharing `_read_text`'s body: that reader strips a BOM and
    ONE trailing terminator, and an artifact body must be hashed as the exact
    bytes the file carries. Only the refusal behaviour is shared, and the
    difference is the point."""
    if args.content_file is not None:
        # newline='' disables universal-newline translation: the receipt
        # hashes exactly the bytes the file carries, CRLF preserved -- silent
        # normalization here would make every cross-store hash compare lie.
        try:
            with open(args.content_file, encoding="utf-8", newline="") as handle:
                return handle.read()
        except UnicodeDecodeError as exc:
            raise CustodyError(
                f"content file is not valid UTF-8 ({exc.reason}); the receipt "
                "hashes these bytes, and a file this cannot decode would be "
                "recorded wrong or not at all -- re-save it as UTF-8") from None
        except OSError as exc:
            raise CustodyError(f"cannot read content file: {exc}") from None
    return args.content


def _common_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", required=True)
    common.add_argument("--actor", required=True)
    # es#173 session->mission binding, channel 1 of 2 (channel 2 is the
    # ZMS_MISSION_ID environment variable; the flag wins). Deliberately
    # named --mission, NOT --mission-id/--mission-path: those flags remain
    # banned outside `open` (pathless-discovery contract) -- this one names
    # which mission's AUTHORITY the verb acts under, never a path.
    common.add_argument("--mission", default=None)
    return common


def _session_binding(args: argparse.Namespace) -> str | None:
    """flag > env > unbound. An empty or whitespace env value is unset --
    `export ZMS_MISSION_ID=` must not manufacture a binding."""
    flag = getattr(args, "mission", None)
    if flag is not None:
        # PRESENT, not truthy. `custody effect --mission "$MISSION_ID"` with an
        # unset variable passes an EMPTY flag; treating that as absent handed
        # the session back to a stale `ZMS_MISSION_ID`, so effects and notes
        # landed under a different mission's authority -- silently, and against
        # the documented flag-over-environment precedence. An empty flag is now
        # a binding that `_ID_RE` refuses in `Mission.load` (BindingInvalid),
        # which is the loud outcome.
        return flag
    env = os.environ.get("ZMS_MISSION_ID", "").strip()
    return env or None


def _add_content_flags(parser: argparse.ArgumentParser) -> None:
    # Artifact bodies do not belong on a command line: argv caps out near
    # 32K chars on Windows and every shell metacharacter must survive
    # quoting -- --content-file reads the bytes directly instead.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content")
    group.add_argument("--content-file", dest="content_file")


def _add_text_flags(parser: argparse.ArgumentParser, name: str) -> None:
    """A `--<name>` / `--<name>-file` pair, for the SAME reason artifact
    bodies got one: argv caps near 32K chars on Windows and every shell
    metacharacter must survive quoting.

    The reason is strictest for `amend`, whose text is the operator's
    VERBATIM grant -- the one string in the contract whose exactness is the
    whole point. Corruption here happens BEFORE the contract sees the string,
    so every downstream guarantee (validation, hash chain, drift detection,
    tail anchor) is intact and irrelevant: the mangled text is sealed as
    authoritative. Observed live -- backticks in a double-quoted shell string
    were executed as command substitution and silently deleted a word from a
    recorded note, exit 0 (es#133)."""
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(f"--{name}")
    group.add_argument(f"--{name}-file", dest=f"{name}_file")


def _read_text(args: argparse.Namespace, name: str) -> str:
    """Read a text argument from its inline flag or its file.

    Exactly two editor/shell artifacts are removed, and nothing else:

    - a leading UTF-8 BOM (`utf-8-sig`). PowerShell 5.1's `Out-File` and
      `Set-Content -Encoding utf8` write one by default on this fleet, and
      plain `utf-8` decoding keeps it as U+FEFF -- which is NOT whitespace, so
      it survives the empty-text checks and lands as the first character of a
      "verbatim" operator grant.
    - ONE trailing line terminator (\\r\\n, \\n, or \\r), because a file
      practically always ends with one and it is not part of what the operator
      said. Deliberately not `rstrip("\\r\\n")`: that eats an entire trailing
      RUN, silently deleting a blank line the operator meant to keep.

    Interior bytes are untouched -- newline='' keeps CRLF exactly as supplied.

    A file that is not valid UTF-8 is a REFUSAL, not a crash: PowerShell's
    bare `Out-File` writes UTF-16LE, and letting UnicodeDecodeError escape
    exits 1 with a traceback, violating this module's documented 0/2/3
    contract."""
    path = getattr(args, f"{name}_file", None)
    if path is None:
        return getattr(args, name)
    try:
        with open(path, encoding="utf-8-sig", newline="") as handle:
            text = handle.read()
    except UnicodeDecodeError as exc:
        raise CustodyError(
            f"{name} file is not valid UTF-8 ({exc.reason}); custody records "
            "text, and a file this cannot decode would be recorded wrong or "
            "not at all -- re-save it as UTF-8") from None
    except OSError as exc:
        raise CustodyError(f"cannot read {name} file: {exc}") from None
    for terminator in ("\r\n", "\n", "\r"):
        if text.endswith(terminator):
            return text[:-len(terminator)]
    return text


def build_parser() -> argparse.ArgumentParser:
    common = _common_parser()
    parser = argparse.ArgumentParser(prog="custody_cli.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_open = sub.add_parser("open", parents=[common])
    p_open.add_argument("--mission-id", required=True)
    _add_text_flags(p_open, "instruction")
    p_open.add_argument("--operator", required=True)
    p_open.add_argument("--steward", required=True)
    p_open.add_argument("--tier", default="declared-role-separation")
    p_open.add_argument("--scope-in", action="append", default=[])
    p_open.add_argument("--scope-out", action="append", default=[])
    p_open.add_argument("--permission", action="append", default=[])
    p_open.add_argument("--protected", action="append", default=[])
    p_open.add_argument("--hold-if", action="append", default=[], dest="hold_if")
    p_open.add_argument("--stop-if", action="append", default=[], dest="stop_if")
    p_open.add_argument("--escalate-if", action="append", default=[], dest="escalate_if")
    p_open.add_argument("--cost", action="append", default=[], dest="acceptable_costs")
    p_open.add_argument("--guards-file", dest="guards_file")
    p_open.add_argument("--guard-mode", dest="guard_mode",
                        choices=["audit", "enforce"])
    # es#173: quarantine an unreadable sibling mission dir, recorded in the
    # opening checkpoint; open refuses otherwise (case row B17).
    p_open.add_argument("--acknowledge-unreadable", action="append",
                        default=[], dest="acknowledge_unreadable",
                        metavar="DIR")

    sub.add_parser("approve", parents=[common])

    p_status = sub.add_parser("status", parents=[common])
    p_status.add_argument("--brief", action="store_true")

    sub.add_parser("audit", parents=[common])

    p_amend = sub.add_parser("amend", parents=[common])
    _add_text_flags(p_amend, "text")
    p_amend.add_argument("--guards-file", dest="guards_file")
    p_amend.add_argument("--guard-mode", dest="guard_mode",
                         choices=["audit", "enforce"])

    p_gate = sub.add_parser("gate", parents=[common])
    p_gate.add_argument("--input-file", dest="input_file")

    p_note = sub.add_parser("note", parents=[common])
    _add_text_flags(p_note, "text")

    p_frontier = sub.add_parser("frontier", parents=[common])
    _add_text_flags(p_frontier, "text")

    p_effect = sub.add_parser("effect", parents=[common])
    p_effect.add_argument("--path", required=True)
    _add_content_flags(p_effect)
    p_effect.add_argument("--request-id", required=True)
    # es#173 case row B23: effect under an unreadable active sibling refuses
    # UnionDegraded until repaired or explicitly acknowledged (the
    # acknowledgement is recorded in the acting mission's chain and
    # persists).
    p_effect.add_argument("--acknowledge-unreadable", action="append",
                          default=[], dest="acknowledge_unreadable",
                          metavar="DIR")

    # es#173: plurality needs an enumeration verb.
    sub.add_parser("missions", parents=[common],
                   help="READ-ONLY list of every mission dir: id, status, "
                        "approved?, steward, frontier")

    p_ack_sib = sub.add_parser("acknowledge-sibling", parents=[common])
    p_ack_sib.add_argument("--path", required=True)

    # es#173 section 4b leg 3: the STRUCTURED grant. `--sibling`, not
    # `--mission`: `--mission` names the acting session's binding on every
    # verb and must keep meaning exactly that.
    p_auth_sib = sub.add_parser(
        "authorize-sibling", parents=[common],
        help="record an operator grant that mission <sibling> may write "
             "<path>, so a drift matching its receipt can be acknowledged "
             "rather than reconciled")
    p_auth_sib.add_argument("--sibling", required=True)
    p_auth_sib.add_argument("--path", required=True)
    _add_text_flags(p_auth_sib, "text")

    sub.add_parser("resume", parents=[common])

    p_reconcile = sub.add_parser("reconcile", parents=[common])
    p_reconcile.add_argument("--path", required=True)
    _add_content_flags(p_reconcile)
    p_reconcile.add_argument("--request-id", required=True)

    p_ack = sub.add_parser("acknowledge-loss", parents=[common])
    p_ack.add_argument("--request-id", required=True)

    # es#138: `verify` was a lifecycle WRITE wearing a read verb's name -- a
    # read-only auditor moved a live mission to 'verifying' through it. The
    # name now belongs to the read-only chain audit; the transition is
    # `begin-verification`. There is deliberately NO mutating alias: a hard
    # error on old muscle memory is the loud warning; silent mutation was the
    # failure mode being fixed.
    sub.add_parser("verify", parents=[common],
                   help="READ-ONLY chain integrity audit; mutates nothing")
    sub.add_parser("begin-verification", parents=[common],
                   help="lifecycle transition into 'verifying' (writes a checkpoint)")

    p_accept = sub.add_parser("accept", parents=[common])
    p_accept.add_argument("--verdict", required=True)
    p_accept.add_argument("--acceptor", required=True)
    p_accept.add_argument("--tier", required=True)
    # The gate this feeds refuses a PASS over undischarged scope drift and its
    # refusal message names this flag. Shipping the gate without the flag left
    # a legitimate, operator-granted drift permanently un-PASSable on the only
    # supported surface, while telling the acceptor to use a remedy that did
    # not exist -- writing a control without installing it, in the refusal text
    # of the control itself.
    p_accept.add_argument("--scope-ack", action="append", default=[],
                          metavar="PATH",
                          help="acknowledge one finding that crossed the "
                               "declared scope; repeatable. Each token in the "
                               "refusal message needs its own --scope-ack: a "
                               "bare PATH acknowledges a boundary crossing, "
                               "linked:PATH acknowledges a multiply-linked "
                               "disclosure (they are different judgements and "
                               "neither discharges the other).")
    _add_text_flags(p_accept, "reason")

    p_clear = sub.add_parser("clear-fail", parents=[common])
    p_clear.add_argument("--match", required=True)
    p_clear.add_argument("--request-id", required=True)

    p_cancel = sub.add_parser("cancel", parents=[common])
    _add_text_flags(p_cancel, "reason")

    return parser


def _read_guards_file(path: str) -> list:
    try:
        with open(path, encoding="utf-8") as handle:
            guards = json.load(handle)
    except json.JSONDecodeError as exc:
        raise CustodyError(
            f"guards file is not valid JSON: {exc}") from None
    if not isinstance(guards, list):
        raise CustodyError("guards file must contain a JSON list of rules")
    return guards


def _read_tool_call(args: argparse.Namespace) -> dict:
    # stdin carries the tool-call JSON by default -- argv has a ~32KB ceiling
    # on Windows and every shell metachar must survive, same reason
    # --content-file exists. --input-file is the explicit-file escape hatch.
    raw = (Path(args.input_file).read_text(encoding="utf-8")
           if args.input_file else sys.stdin.read())
    try:
        call = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CustodyError(f"gate: tool-call JSON unreadable: {exc}") from None
    if not isinstance(call, dict) or not isinstance(call.get("tool_name"), str):
        raise CustodyError("gate: tool-call JSON needs a string 'tool_name'")
    call.setdefault("command", None)
    call.setdefault("file_path", None)
    return call


def _print_envelope(checkpoint: dict, file=sys.stdout) -> None:
    """Show the advisory envelope, marked advisory.

    Every "the steward should have read scope" argument was about a field no
    surface displayed. This is the display. It refuses nothing and says so --
    a boundary a reader could mistake for a control is the estate's keystone
    failure (writing a control is not installing one) in labelling form."""
    manifest = checkpoint["manifest"]
    rows = [
        ("scope.in", manifest["scope"]["in"]),
        ("scope.out", manifest["scope"]["out"]),
        ("permissions", manifest["authority"]["permissions"]),
        ("protected_state", manifest["authority"]["protected_state"]),
        ("hold_if", manifest["stop_rules"]["hold_if"]),
        ("stop_if", manifest["stop_rules"]["stop_if"]),
        ("escalate_if", manifest["stop_rules"]["escalate_if"]),
        ("acceptable_costs", manifest["authority"]["acceptable_costs"]),
    ]
    # This header used to read "enforced by nothing", which stopped being true
    # in the same change that added the comparison: scope path patterns are
    # machine-compared at acceptance and can refuse a PASS. A display whose
    # own honesty label is stale is the failure this display exists to fix.
    print("envelope (ADVISORY at run time -- nothing blocks a tool call on "
          "it. Pre-tool enforcement lives in authority.actuator_guards; "
          "scope path patterns ARE compared at acceptance and can refuse a "
          "PASS):", file=file)
    for name, values in rows:
        if values:
            for value in values:
                print(f"  {name}: {_display_safe(value)}", file=file)
        else:
            print(f"  {name}: (unset -- UNBOUNDED, not safely defaulted)",
                  file=file)
    uncompared = uncompared_scope_entries(manifest)
    if uncompared.get("in_comparison_disabled"):
        print("  scope.in: COMPARISON DISABLED -- the declaration mixes prose "
              "with path patterns, so NOTHING in scope.in is compared",
              file=file)
    for direction in ("in", "out"):
        for entry in uncompared[direction]:
            # Naming what is NOT compared, so "scope is checked now" never
            # gets read as "all of scope is checked".
            print(f"  scope.{direction}: {_display_safe(entry)} "
                  "(prose -- NOT machine-compared)", file=file)


def _checkpoints_since_last_amendment(mission, latest: dict) -> int | None:
    """How many revisions have passed since authority last changed.

    The measured failure on the reference mission was not an unenforced
    boundary field -- it was AMENDMENT LATENCY. An operator reframed a mission
    at r52; the `amend` verb existed from r59; the grant was not recorded until
    r85. Seventeen hours and twenty-seven checkpoints of work ran under
    authority the record did not carry, and nothing counted.

    This counts. It is objective, needs no field to be populated, and cannot be
    gamed without recording a real amendment. None when the mission has never
    been amended -- distinct from 0, which means "amended at this revision"."""
    amendments = latest["manifest"]["authority"]["amendments"]
    if not amendments:
        return None
    for path in mission.store.checkpoint_paths():
        record = json.loads(path.read_text(encoding="utf-8"))
        if len(record["manifest"]["authority"]["amendments"]) == len(amendments):
            return latest["revision"] - record["revision"]
    return None


def _brief(checkpoint: dict, mission=None) -> dict:
    manifest = checkpoint["manifest"]
    brief = {
        "mission_id": checkpoint["mission_id"],
        "status": checkpoint["status"],
        "revision": checkpoint["revision"],
        "amendments_count": len(manifest["authority"]["amendments"]),
        "frontier": checkpoint["state"]["frontier"],
        "unresolved_verdicts": checkpoint["state"]["unresolved_verdicts"],
        "notes_count": len(checkpoint["state"]["notes"]),
        "receipt_ids_count": len(checkpoint["receipt_ids"]),
        "written_utc": checkpoint["written_utc"],
        "written_by": checkpoint["written_by"],
    }
    if mission is not None:
        brief["checkpoints_since_last_amendment"] = \
            _checkpoints_since_last_amendment(mission, checkpoint)
    # The envelope had NO read surface at all: _brief omitted it and `resume`
    # printed no manifest content, so every "the steward should read it"
    # argument was about text that nothing ever displayed. Advisory fields are
    # labelled as such right here, so a reader never has to infer their class
    # from the company they keep -- see README.md's ENFORCEMENT STATUS table.
    brief["envelope_advisory"] = {
        "scope_in": manifest["scope"]["in"],
        "scope_out": manifest["scope"]["out"],
        "permissions": manifest["authority"]["permissions"],
        "protected_state": manifest["authority"]["protected_state"],
        "hold_if": manifest["stop_rules"]["hold_if"],
        "stop_if": manifest["stop_rules"]["stop_if"],
        "escalate_if": manifest["stop_rules"]["escalate_if"],
        "acceptable_costs": manifest["authority"]["acceptable_costs"],
    }
    empty = sorted(name for name, value in brief["envelope_advisory"].items()
                   if not value)
    if empty:
        # An empty envelope field is UNBOUNDED, not safely defaulted, and
        # `_str_list` accepts [] forever with no surface ever saying so.
        brief["envelope_unset"] = empty
    uncompared = uncompared_scope_entries(manifest)
    if uncompared["in"] or uncompared["out"]:
        # Which scope entries the acceptance comparison does NOT range over.
        # Reporting the comparison without reporting its blind spot would let
        # "scope is checked" be read as "all of scope is checked".
        brief["scope_not_compared"] = uncompared
    return brief


def dispatch(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)

    if args.command == "open":
        if args.guard_mode and not args.guards_file:
            raise CustodyError("--guard-mode requires --guards-file")
        guards = (_read_guards_file(args.guards_file)
                  if args.guards_file else None)
        binding = _session_binding(args)
        if binding is not None:
            # Case row B4/B9: a present binding is validated on EVERY verb --
            # a stale ZMS_MISSION_ID must refuse loudly, never be silently
            # ignored. A valid binding does not otherwise affect `open`.
            Mission.load(workspace, actor=args.actor, mission_id=binding)
        Mission.open(
            workspace, mission_id=args.mission_id,
            instruction=_read_text(args, "instruction"),
            operator_ref=args.operator, steward_ref=args.steward,
            required_tier=args.tier, actor=args.actor,
            scope_in=args.scope_in, scope_out=args.scope_out,
            permissions=args.permission, protected_state=args.protected,
            hold_if=args.hold_if, stop_if=args.stop_if, escalate_if=args.escalate_if,
            acceptable_costs=args.acceptable_costs,
            guard_mode=args.guard_mode, actuator_guards=guards,
            acknowledge_unreadable=args.acknowledge_unreadable)
        print(1)  # Mission.open always writes revision 1
        # The binding line for the shell: printed, NOT set -- a child
        # process cannot set its parent's environment, and pretending
        # otherwise would manufacture the "bound, actually unbound" decoy
        # (es#173 section 1). stderr, so stdout keeps its one-value contract.
        print(f"bind: export ZMS_MISSION_ID={_display_safe(args.mission_id)}",
              file=sys.stderr)
        return 0

    if args.command == "missions":
        # Case rows 4/9/15: a present binding is validated on EVERY verb. This
        # was the one verb that silently accepted a stale ZMS_MISSION_ID.
        # Read-only, so nothing was misrouted -- but "the binding you are
        # holding is dead" is exactly what an operator running `missions` is
        # trying to find out.
        binding = _session_binding(args)
        if binding is not None:
            Mission.load(workspace, actor=args.actor, mission_id=binding)
        rows = []
        missions_root = workspace / "missions"
        if missions_root.is_dir():
            from custody_mission import _approved_by_chain
            from custody_store import MissionStore
            for mission_dir in sorted(missions_root.iterdir()):
                if not mission_dir.is_dir():
                    continue
                store = MissionStore(mission_dir)
                if not store.checkpoint_paths():
                    continue
                row = {"mission": mission_dir.name}
                try:
                    latest, _ = store.load_latest()
                except (StoreError, ValueError, OSError) as exc:
                    # OSError too: `load_latest` can raise PermissionError or
                    # FileNotFoundError, and `main()` catches only
                    # CustodyError/StoreError -- so one locked mission dir
                    # killed the whole listing with a traceback instead of
                    # emitting an `unreadable` row and continuing.
                    row.update({"status": "unreadable",
                                "error": f"{type(exc).__name__}: {exc}",
                                "approved": None, "steward_ref": None,
                                "frontier": None})
                else:
                    row.update({
                        "status": latest["status"],
                        "approved": _approved_by_chain(store),
                        "steward_ref": latest["manifest"]["steward_ref"],
                        "frontier": latest["state"]["frontier"],
                        "revision": latest["revision"],
                    })
                rows.append(row)
        _print_status(rows)
        return 0

    if args.command == "gate":
        from custody_gate import run_gate
        # OD-4 refined ("Self-arm at open, union at approve", operator
        # ruling 2026-08-25): the session binding self-arms the bound
        # mission's own guards. Exposure only grows -- the union of
        # approved missions is evaluated with or without a binding.
        verdict = run_gate(workspace, _read_tool_call(args), actor=args.actor,
                           session_id="", harness="cli",
                           bound_mission=_session_binding(args))
        _print_status(verdict)
        return 2 if verdict["decision"] == "block" else 0

    mission = Mission.load(workspace, actor=args.actor,
                           mission_id=_session_binding(args))

    if args.command == "approve":
        print(mission.approve())
    elif args.command == "status":
        latest = mission.status()
        _print_status(_brief(latest, mission) if args.brief else latest)
    elif args.command == "audit":
        # ORPHANS FIRST. The orphan check is existence-based and cheap; the
        # continuity scan READS every historical receipt. Running the scan
        # first meant one unreadable receipt took the whole command down
        # before the orphan report -- the thing this path exists to make
        # findable -- ever printed. The read failure is handled at its source
        # now, but the ordering stays: a report about files EXISTING should
        # not depend on a pass that opens them.
        orphans = mission.orphaned_retired_receipts()
        breaks = mission.continuity_breaks()
        _print_status({"record": "continuity-report@1",
                        "continuity_breaks": breaks,
                        "orphaned_retired_receipts": orphans})
        return 3 if (breaks or orphans) else 0
    elif args.command == "amend":
        kwargs: dict = {}
        if args.guards_file:
            kwargs["actuator_guards"] = _read_guards_file(args.guards_file)
        if args.guard_mode:
            kwargs["guard_mode"] = args.guard_mode
        print(mission.amend_authority(_read_text(args, "text"), **kwargs))
    elif args.command == "note":
        print(mission.note(_read_text(args, "text")))
    elif args.command == "frontier":
        print(mission.set_frontier(_read_text(args, "text")))
    elif args.command == "effect":
        receipt = mission.record_effect(
            args.path, _read_content(args), args.request_id,
            acknowledge_unreadable=args.acknowledge_unreadable)
        _print_status(receipt)
    elif args.command == "resume":
        findings = mission.resume()
        for marker in findings:
            print(_display_safe(marker))
        # SIBLING-DISCHARGED is finding-grade but non-blocking (operator
        # ruling 2026-08-25, loud auto-discharge): it rides stdout like
        # every finding -- a resume that discharged a transient sibling
        # crossing must NEVER print "clean" -- but it leaves nothing
        # unresolved, so it does not contribute to the drift exit code.
        drift = [m for m in findings
                 if not m.startswith("SIBLING-DISCHARGED:")]
        if not findings:
            n = len(set(mission.status()["receipt_ids"]))
            vacuous = " -- vacuously (no effects recorded)" if n == 0 else ""
            print(f"resume: clean; {n} receipt id(s) on record{vacuous}",
                  file=sys.stderr)
        # Resume is the ONE moment a steward reliably reads before acting, and
        # it printed no manifest content at all -- so the envelope was never in
        # front of anyone at the moment it was supposed to inform. Advisory:
        # nothing here refuses anything; that is stated so it cannot be misread.
        _print_envelope(mission.status(), file=sys.stderr)
        # A continuity break is not drift and raises no obligation, but a
        # clean resume is exactly where its absence would be misread as
        # "nothing happened here" -- so it rides alongside the verdict.
        unanswered = [b for b in mission.continuity_breaks()
                      if not b["already_reconciled"]]
        if unanswered:
            paths = ", ".join(sorted({
                _display_safe(b["artifact_path"]) for b in unanswered
            }))
            print(f"resume: {len(unanswered)} unreconciled continuity "
                  f"break(s) -- the artifact changed between receipted events "
                  f"with no reconciliation answering for it: {paths}; run "
                  "`audit` for detail", file=sys.stderr)
        return 3 if drift else 0
    elif args.command == "reconcile":
        receipt = mission.reconcile(args.path, _read_content(args),
                                     args.request_id)
        _print_status(receipt)
    elif args.command == "acknowledge-loss":
        print(mission.acknowledge_receipt_loss(args.request_id))
    elif args.command == "acknowledge-sibling":
        print(mission.acknowledge_sibling(args.path))
    elif args.command == "authorize-sibling":
        print(mission.authorize_sibling(args.sibling, args.path,
                                        _read_text(args, "text")))
    elif args.command == "verify":
        # READ-ONLY (es#138): never a lifecycle write. Exit 0 = chain intact,
        # exit 4 = chain break reported. Either way nothing was written.
        audit = mission.verify_chain()
        print(json.dumps(audit, indent=2, sort_keys=True))
        return 0 if audit["chain_ok"] else 4
    elif args.command == "begin-verification":
        print(mission.begin_verification())
    elif args.command == "accept":
        print(mission.record_verdict(args.verdict, acceptor_id=args.acceptor,
                                      assurance_tier=args.tier,
                                      reason=_read_text(args, "reason"),
                                      scope_ack=args.scope_ack))
    elif args.command == "clear-fail":
        print(mission.clear_fail(args.match, args.request_id))
    elif args.command == "cancel":
        print(mission.cancel(_read_text(args, "reason")))
    else:
        raise AssertionError(f"unhandled command {args.command!r}")
    return 0


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args)
    except (CustodyError, StoreError) as exc:
        # StoreError refusals (concurrent writer, duplicate receipt, invalid
        # record) honor the same exit-2 contract as custody refusals instead
        # of escaping as a traceback with exit 1.
        print(_display_safe(
            f"{type(exc).__name__}: {exc}", preserve_printable_syntax=True
        ), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
