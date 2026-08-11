#!/usr/bin/env python3
"""Black-box tests for custody_cli.py: drive it via subprocess, exactly as an
operator or another process would. No import of custody_cli internals except
for the AST structural check on --mission-path/--mission-id placement."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLI = ROOT / "custody_cli.py"

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), *args], capture_output=True, text=True)


def open_cli(ws: Path, mission_id: str, instruction: str, actor: str = "agent:worker",
             steward: str = "agent:worker") -> subprocess.CompletedProcess:
    return run("open", "--workspace", str(ws), "--actor", actor,
               "--mission-id", mission_id, "--instruction", instruction,
               "--operator", "operator:zach", "--steward", steward)


def test_open_approve_effect_status_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        r = open_cli(ws, "m-cli-open", "Ship the CLI.")
        check("open-exit-0", r.returncode == 0)

        r = run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        check("approve-exit-0", r.returncode == 0)

        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/a.md", "--content", "hello",
                 "--request-id", "req-1")
        check("effect-exit-0", r.returncode == 0)
        check("effect-artifact-written",
              (ws / "notes" / "a.md").read_text(encoding="utf-8") == "hello")

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        check("status-exit-0", r.returncode == 0)
        st = json.loads(r.stdout)
        check("status-record-checkpoint", st["record"] == "checkpoint@1")
        check("status-revision-3", st["revision"] == 3)
        check("status-status-active", st["status"] == "active")


def test_resume_detects_drift_exit_3() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-drift", "Track drift.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "notes/a.md", "--content", "hello", "--request-id", "req-1")
        (ws / "notes" / "a.md").write_text("tampered", encoding="utf-8")

        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("resume-exit-3", r.returncode == 3)
        check("resume-names-path", "notes/a.md" in r.stdout)

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        st = json.loads(r.stdout)
        check("resume-status-reopened", st["status"] == "reopened")
        check("resume-marker-present",
              "RECONCILIATION:notes/a.md" in st["state"]["unresolved_verdicts"])

        # reconcile the drift, then resume again: no drift, exit 0, empty stdout
        run("reconcile", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "notes/a.md", "--content", "hello", "--request-id", "req-2")
        r = run("resume", "--workspace", str(ws), "--actor", "agent:third")
        check("resume-clean-exit-0", r.returncode == 0)
        check("resume-clean-empty-stdout", r.stdout.strip() == "")


def test_accept_self_cert_refused_exit_2() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-selfcert", "Finish task.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("verify", "--workspace", str(ws), "--actor", "agent:worker")

        r = run("accept", "--workspace", str(ws), "--actor", "agent:worker",
                 "--verdict", "PASS", "--acceptor", "agent:worker",
                 "--tier", "declared-role-separation", "--reason", "self says done")
        check("accept-self-cert-exit-2", r.returncode == 2)
        check("accept-self-cert-stderr-names-exception",
              "AcceptanceRefused" in r.stderr)

        # confirm the mission is still 'verifying', not silently completed
        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        st = json.loads(r.stdout)
        check("accept-self-cert-no-completion", st["status"] == "verifying")


def test_full_lifecycle_via_cli() -> None:
    """note/frontier/clear-fail/cancel wiring, exercised once each."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-full", "Exercise every subcommand.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("note", "--workspace", str(ws), "--actor", "agent:worker",
            "--text", "checking in")
        run("frontier", "--workspace", str(ws), "--actor", "agent:worker",
            "--text", "next: write the fix")

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        st = json.loads(r.stdout)
        check("full-notes-recorded", "checking in" in st["state"]["notes"])
        check("full-frontier-set", st["state"]["frontier"] == "next: write the fix")

        run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        r = run("accept", "--workspace", str(ws), "--actor", "agent:worker",
                 "--verdict", "FAIL", "--acceptor", "agent:acceptor",
                 "--tier", "declared-role-separation", "--reason", "missing case")
        check("full-fail-exit-0", r.returncode == 0)

        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "notes/fix.md", "--content", "patched",
            "--request-id", "req-fix-1")
        r = run("clear-fail", "--workspace", str(ws), "--actor", "agent:worker",
                 "--match", "missing case", "--request-id", "req-fix-1")
        check("full-clear-fail-exit-0", r.returncode == 0)

        run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        r = run("accept", "--workspace", str(ws), "--actor", "agent:worker",
                 "--verdict", "PASS", "--acceptor", "agent:acceptor",
                 "--tier", "declared-role-separation", "--reason", "fix verified")
        check("full-accept-pass-exit-0", r.returncode == 0)

        # pathless discovery correctly excludes a completed mission: no
        # --mission-id escape hatch exists to reach it, by contract.
        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        check("full-completed-mission-unreachable-status", r.returncode == 2)
        check("full-completed-mission-no-active-mission",
              "NoActiveMission" in r.stderr)

        r = run("cancel", "--workspace", str(ws), "--actor", "agent:worker",
                 "--reason", "already completed, should refuse")
        check("full-cancel-refused-exit-2", r.returncode == 2)


def test_no_mission_flags_outside_open() -> None:
    tree = ast.parse(CLI.read_text(encoding="utf-8"))

    def _str_const(node: ast.AST) -> str | None:
        return node.value if isinstance(node, ast.Constant) and isinstance(
            node.value, str) else None

    open_vars: set[str] = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and node.value.func.attr == "add_parser"
                and node.value.args and _str_const(node.value.args[0]) == "open"
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            open_vars.add(node.targets[0].id)
    check("ast-found-open-subparser-var", bool(open_vars))

    violations: list[str] = []
    saw_mission_id_in_open = False
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument" and node.args):
            continue
        flag = _str_const(node.args[0])
        if flag not in ("--mission-path", "--mission-id"):
            continue
        recv = node.func.value
        recv_name = recv.id if isinstance(recv, ast.Name) else None
        if recv_name in open_vars:
            if flag == "--mission-id":
                saw_mission_id_in_open = True
        else:
            violations.append(f"{flag} on {recv_name!r}")
    check("no-mission-flags-outside-open", not violations)
    check("open-declares-mission-id", saw_mission_id_in_open)


TESTS = [
    test_open_approve_effect_status_roundtrip,
    test_resume_detects_drift_exit_3,
    test_accept_self_cert_refused_exit_2,
    test_full_lifecycle_via_cli,
    test_no_mission_flags_outside_open,
]


def main() -> int:
    for fn in TESTS:
        fn()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
