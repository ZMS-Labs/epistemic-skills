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
`resume`. On a clean resume the drift list on stdout is empty by contract;
a one-line summary goes to stderr so vacuous cleanliness (zero receipts on
record) is visible instead of indistinguishable from verified cleanliness.
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


def build_parser() -> argparse.ArgumentParser:
    common = _common_parser()
    parser = argparse.ArgumentParser(prog="custody_cli.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_open = sub.add_parser("open", parents=[common])
    p_open.add_argument("--mission-id", required=True)
    p_open.add_argument("--instruction", required=True)
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

    sub.add_parser("approve", parents=[common])

    p_status = sub.add_parser("status", parents=[common])
    p_status.add_argument("--brief", action="store_true")

    p_amend = sub.add_parser("amend", parents=[common])
    p_amend.add_argument("--text", required=True)

    p_note = sub.add_parser("note", parents=[common])
    p_note.add_argument("--text", required=True)

    p_frontier = sub.add_parser("frontier", parents=[common])
    p_frontier.add_argument("--text", required=True)

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
    p_accept.add_argument("--reason", required=True)

    p_clear = sub.add_parser("clear-fail", parents=[common])
    p_clear.add_argument("--match", required=True)
    p_clear.add_argument("--request-id", required=True)

    p_cancel = sub.add_parser("cancel", parents=[common])
    p_cancel.add_argument("--reason", required=True)

    return parser


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
        Mission.open(
            workspace, mission_id=args.mission_id, instruction=args.instruction,
            operator_ref=args.operator, steward_ref=args.steward,
            required_tier=args.tier, actor=args.actor,
            scope_in=args.scope_in, scope_out=args.scope_out,
            permissions=args.permission, protected_state=args.protected,
            hold_if=args.hold_if, stop_if=args.stop_if, escalate_if=args.escalate_if,
            acceptable_costs=args.acceptable_costs)
        print(1)  # Mission.open always writes revision 1
        return 0

    mission = Mission.load(workspace, actor=args.actor)

    if args.command == "approve":
        print(mission.approve())
    elif args.command == "status":
        latest = mission.status()
        _print_status(_brief(latest) if args.brief else latest)
    elif args.command == "amend":
        print(mission.amend_authority(args.text))
    elif args.command == "note":
        print(mission.note(args.text))
    elif args.command == "frontier":
        print(mission.set_frontier(args.text))
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
                                      assurance_tier=args.tier, reason=args.reason))
    elif args.command == "clear-fail":
        print(mission.clear_fail(args.match, args.request_id))
    elif args.command == "cancel":
        print(mission.cancel(args.reason))
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
