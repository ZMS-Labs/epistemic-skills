#!/usr/bin/env python3
"""Thin argparse CLI over the Mission lifecycle API (custody_mission.Mission).
No logic beyond translation: every subcommand parses flags, calls exactly one
Mission method, and prints exactly what that method returns.

Discovery is pathless by contract: no subcommand other than `open` accepts a
--mission-path or --mission-id flag. `Mission.load()` finds the single active
mission under --workspace on every other command.

Exit codes: 0 success; 2 usage/refusal (a CustodyError subclass prints its
class name + message to stderr); 3 drift detected on `resume`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from custody_mission import CustodyError, Mission


def _print_status(checkpoint: dict) -> None:
    print(json.dumps(checkpoint, indent=2, sort_keys=True, ensure_ascii=True))


def _common_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", required=True)
    common.add_argument("--actor", required=True)
    return common


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

    sub.add_parser("approve", parents=[common])
    sub.add_parser("status", parents=[common])

    p_note = sub.add_parser("note", parents=[common])
    p_note.add_argument("--text", required=True)

    p_frontier = sub.add_parser("frontier", parents=[common])
    p_frontier.add_argument("--text", required=True)

    p_effect = sub.add_parser("effect", parents=[common])
    p_effect.add_argument("--path", required=True)
    p_effect.add_argument("--content", required=True)
    p_effect.add_argument("--request-id", required=True)

    sub.add_parser("resume", parents=[common])

    p_reconcile = sub.add_parser("reconcile", parents=[common])
    p_reconcile.add_argument("--path", required=True)
    p_reconcile.add_argument("--content", required=True)
    p_reconcile.add_argument("--request-id", required=True)

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


def dispatch(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace)

    if args.command == "open":
        Mission.open(
            workspace, mission_id=args.mission_id, instruction=args.instruction,
            operator_ref=args.operator, steward_ref=args.steward,
            required_tier=args.tier, actor=args.actor,
            scope_in=args.scope_in, scope_out=args.scope_out,
            permissions=args.permission, protected_state=args.protected)
        return 0

    mission = Mission.load(workspace, actor=args.actor)

    if args.command == "approve":
        mission.approve()
    elif args.command == "status":
        _print_status(mission.status())
    elif args.command == "note":
        mission.note(args.text)
    elif args.command == "frontier":
        mission.set_frontier(args.text)
    elif args.command == "effect":
        mission.record_effect(args.path, args.content, args.request_id)
    elif args.command == "resume":
        drift = mission.resume()
        for relpath in drift:
            print(relpath)
        return 3 if drift else 0
    elif args.command == "reconcile":
        mission.reconcile(args.path, args.content, args.request_id)
    elif args.command == "verify":
        mission.begin_verification()
    elif args.command == "accept":
        mission.record_verdict(args.verdict, acceptor_id=args.acceptor,
                                assurance_tier=args.tier, reason=args.reason)
    elif args.command == "clear-fail":
        mission.clear_fail(args.match, args.request_id)
    elif args.command == "cancel":
        mission.cancel(args.reason)
    else:
        raise AssertionError(f"unhandled command {args.command!r}")
    return 0


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args)
    except CustodyError as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
