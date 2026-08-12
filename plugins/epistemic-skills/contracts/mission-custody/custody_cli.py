#!/usr/bin/env python3
"""Thin argparse CLI over the Mission lifecycle API (custody_mission.Mission).
No logic beyond translation: every subcommand parses flags, calls exactly one
Mission method, and prints exactly what that method returns -- the new
revision number for lifecycle mutations, the receipt JSON for effect and
reconcile, the checkpoint JSON for status.

Discovery is pathless by contract: no subcommand other than `open` accepts a
--mission-path or --mission-id flag. `Mission.load()` finds the single active
mission under --workspace on every other command.

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
import sys
from pathlib import Path

from custody_mission import CustodyError, Mission
from custody_store import StoreError


def _print_status(checkpoint: dict) -> None:
    print(json.dumps(checkpoint, indent=2, sort_keys=True, ensure_ascii=True))


def _ascii_safe(text: str) -> str:
    """Render text as ASCII-only, escaping any non-ASCII characters so a
    print to stdout/stderr never raises UnicodeEncodeError regardless of
    PYTHONIOENCODING or the console codepage. Mirrors the ensure_ascii=True
    guarantee _print_status already gets from json.dumps, for the two
    output paths that print a raw str instead of a JSON document."""
    return text.encode("ascii", "backslashreplace").decode("ascii")


def _read_content(args: argparse.Namespace) -> str:
    if args.content_file is not None:
        # newline='' disables universal-newline translation: the receipt
        # hashes exactly the bytes the file carries, CRLF preserved -- silent
        # normalization here would make every cross-store hash compare lie.
        with open(args.content_file, encoding="utf-8", newline="") as handle:
            return handle.read()
    return args.content


def _common_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", required=True)
    common.add_argument("--actor", required=True)
    return common


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

    sub.add_parser("resume", parents=[common])

    p_reconcile = sub.add_parser("reconcile", parents=[common])
    p_reconcile.add_argument("--path", required=True)
    _add_content_flags(p_reconcile)
    p_reconcile.add_argument("--request-id", required=True)

    p_ack = sub.add_parser("acknowledge-loss", parents=[common])
    p_ack.add_argument("--request-id", required=True)

    sub.add_parser("verify", parents=[common])

    p_accept = sub.add_parser("accept", parents=[common])
    p_accept.add_argument("--verdict", required=True)
    p_accept.add_argument("--acceptor", required=True)
    p_accept.add_argument("--tier", required=True)
    _add_text_flags(p_accept, "reason")

    p_clear = sub.add_parser("clear-fail", parents=[common])
    p_clear.add_argument("--match", required=True)
    p_clear.add_argument("--request-id", required=True)

    p_cancel = sub.add_parser("cancel", parents=[common])
    _add_text_flags(p_cancel, "reason")

    return parser


def _read_guards_file(path: str) -> list:
    with open(path, encoding="utf-8") as handle:
        guards = json.load(handle)
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


def _brief(checkpoint: dict) -> dict:
    return {
        "mission_id": checkpoint["mission_id"],
        "status": checkpoint["status"],
        "revision": checkpoint["revision"],
        "amendments_count": len(
            checkpoint["manifest"]["authority"]["amendments"]),
        "frontier": checkpoint["state"]["frontier"],
        "unresolved_verdicts": checkpoint["state"]["unresolved_verdicts"],
        "notes_count": len(checkpoint["state"]["notes"]),
        "receipt_ids_count": len(checkpoint["receipt_ids"]),
        "written_utc": checkpoint["written_utc"],
        "written_by": checkpoint["written_by"],
    }


def dispatch(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)

    if args.command == "open":
        if args.guard_mode and not args.guards_file:
            raise CustodyError("--guard-mode requires --guards-file")
        guards = (_read_guards_file(args.guards_file)
                  if args.guards_file else None)
        Mission.open(
            workspace, mission_id=args.mission_id,
            instruction=_read_text(args, "instruction"),
            operator_ref=args.operator, steward_ref=args.steward,
            required_tier=args.tier, actor=args.actor,
            scope_in=args.scope_in, scope_out=args.scope_out,
            permissions=args.permission, protected_state=args.protected,
            hold_if=args.hold_if, stop_if=args.stop_if, escalate_if=args.escalate_if,
            acceptable_costs=args.acceptable_costs,
            guard_mode=args.guard_mode, actuator_guards=guards)
        print(1)  # Mission.open always writes revision 1
        return 0

    if args.command == "gate":
        from custody_gate import run_gate
        verdict = run_gate(workspace, _read_tool_call(args), actor=args.actor,
                           session_id="", harness="cli")
        _print_status(verdict)
        return 2 if verdict["decision"] == "block" else 0

    mission = Mission.load(workspace, actor=args.actor)

    if args.command == "approve":
        print(mission.approve())
    elif args.command == "status":
        latest = mission.status()
        _print_status(_brief(latest) if args.brief else latest)
    elif args.command == "audit":
        breaks = mission.continuity_breaks()
        _print_status({"record": "continuity-report@1",
                        "continuity_breaks": breaks})
        return 3 if breaks else 0
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
        receipt = mission.record_effect(args.path, _read_content(args),
                                         args.request_id)
        _print_status(receipt)
    elif args.command == "resume":
        drift = mission.resume()
        for relpath in drift:
            print(_ascii_safe(relpath))
        if not drift:
            n = len(set(mission.status()["receipt_ids"]))
            vacuous = " -- vacuously (no effects recorded)" if n == 0 else ""
            print(f"resume: clean; {n} receipt id(s) on record{vacuous}",
                  file=sys.stderr)
        # A continuity break is not drift and raises no obligation, but a
        # clean resume is exactly where its absence would be misread as
        # "nothing happened here" -- so it rides alongside the verdict.
        unanswered = [b for b in mission.continuity_breaks()
                      if not b["already_reconciled"]]
        if unanswered:
            paths = ", ".join(sorted({b["artifact_path"] for b in unanswered}))
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
    elif args.command == "verify":
        print(mission.begin_verification())
    elif args.command == "accept":
        print(mission.record_verdict(args.verdict, acceptor_id=args.acceptor,
                                      assurance_tier=args.tier,
                                      reason=_read_text(args, "reason")))
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
        print(_ascii_safe(f"{type(exc).__name__}: {exc}"), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
