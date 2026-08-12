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

        # a verdict is recorded by its acceptor: the worker session naming a
        # different acceptor is refused
        r = run("accept", "--workspace", str(ws), "--actor", "agent:worker",
                 "--verdict", "FAIL", "--acceptor", "agent:acceptor",
                 "--tier", "declared-role-separation", "--reason", "missing case")
        check("full-fabricated-acceptor-exit-2", r.returncode == 2)
        check("full-fabricated-acceptor-refused", "AcceptanceRefused" in r.stderr)

        r = run("accept", "--workspace", str(ws), "--actor", "agent:acceptor",
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
        r = run("accept", "--workspace", str(ws), "--actor", "agent:acceptor",
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


def test_ascii_safe_drift_and_error_output() -> None:
    """Non-ASCII content in a drifted relpath or a CustodyError message must
    render as an ASCII-only escape on stdout/stderr -- never a raw non-ASCII
    byte, and never a crash regardless of the console codepage (brief Step 3:
    "PYTHONIOENCODING-safe (ASCII-only output)"). Covers both raw-str print
    sites: the `resume` drift list and the top-level CustodyError handler."""
    # Built via a \uXXXX escape (not a literal character) so this source
    # file itself stays pure ASCII (isascii() true).
    e_acute = "\u00e9"  # 'e' with acute accent, U+00E9
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-ascii", "Exercise ASCII-safe output.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")

        non_ascii_path = f"notes/r{e_acute}sum{e_acute}.md"
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", non_ascii_path, "--content", "hello",
            "--request-id", "req-ascii-1")
        (ws / "notes" / f"r{e_acute}sum{e_acute}.md").write_text(
            "tampered", encoding="utf-8")

        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("resume-ascii-exit-3", r.returncode == 3)
        check("resume-ascii-stdout-is-ascii", r.stdout.isascii())
        check("resume-ascii-stdout-escapes-non-ascii", "\\xe9" in r.stdout)

        # Drive the mission to 'reopened' via a legitimate (non-self-cert)
        # FAIL verdict, then trigger a CustodyError whose message embeds a
        # non-ASCII value supplied verbatim by the operator: clear-fail's
        # "no FAIL marker matching {fragment!r}" with a non-matching,
        # non-ASCII --match fragment.
        run("reconcile", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", non_ascii_path, "--content", "hello",
            "--request-id", "req-ascii-2")
        run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        run("accept", "--workspace", str(ws), "--actor", "agent:acceptor",
            "--verdict", "FAIL", "--acceptor", "agent:acceptor",
            "--tier", "declared-role-separation", "--reason", "needs review")

        r = run("clear-fail", "--workspace", str(ws), "--actor", "agent:worker",
                 "--match", f"caf{e_acute}-does-not-match",
                 "--request-id", "req-ascii-2")
        check("clear-fail-ascii-exit-2", r.returncode == 2)
        check("clear-fail-ascii-stderr-is-ascii", r.stderr.isascii())
        check("clear-fail-ascii-stderr-names-exception", "CustodyError" in r.stderr)
        check("clear-fail-ascii-stderr-escapes-non-ascii", "\\xe9" in r.stderr)


def test_open_stop_rules_and_acceptable_costs() -> None:
    """open's --hold-if/--stop-if/--escalate-if/--cost flags land verbatim,
    in order, in the manifest's stop_rules and acceptable_costs."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        r = run("open", "--workspace", str(ws), "--actor", "agent:worker",
                 "--mission-id", "m-cli-stoprules", "--instruction", "Guard the stop rules.",
                 "--operator", "operator:zach", "--steward", "agent:worker",
                 "--hold-if", "clientA re-grabs", "--hold-if", "second hold",
                 "--stop-if", "operator revokes",
                 "--escalate-if", "protected state touched",
                 "--cost", "one session per stage")
        check("open-stop-rules-exit-0", r.returncode == 0)

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        check("open-stop-rules-status-exit-0", r.returncode == 0)
        st = json.loads(r.stdout)
        manifest = st["manifest"]
        check("open-stop-rules-hold-if",
              manifest["stop_rules"]["hold_if"] == ["clientA re-grabs", "second hold"])
        check("open-stop-rules-stop-if",
              manifest["stop_rules"]["stop_if"] == ["operator revokes"])
        check("open-stop-rules-escalate-if",
              manifest["stop_rules"]["escalate_if"] == ["protected state touched"])
        check("open-stop-rules-acceptable-costs",
              manifest["authority"]["acceptable_costs"] == ["one session per stage"])


def test_open_without_stop_rules_yields_empty_lists() -> None:
    """Existing behavior unchanged: omitting the new flags still yields
    empty stop_rules/acceptable_costs lists."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-nostoprules", "No stop rules given.")

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        st = json.loads(r.stdout)
        manifest = st["manifest"]
        check("open-no-stop-rules-hold-if-empty", manifest["stop_rules"]["hold_if"] == [])
        check("open-no-stop-rules-stop-if-empty", manifest["stop_rules"]["stop_if"] == [])
        check("open-no-stop-rules-escalate-if-empty",
              manifest["stop_rules"]["escalate_if"] == [])
        check("open-no-stop-rules-costs-empty",
              manifest["authority"]["acceptable_costs"] == [])


def test_success_output_confirms_the_write() -> None:
    """Every mutating command prints its landed revision (or receipt): a mute
    success path is what got resume misread as broken (efficacy evaluation
    2026-08-12). Also covers --brief and --content-file."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        r = open_cli(ws, "m-cli-output", "Confirm every write.")
        check("open-prints-r1", r.stdout.strip() == "1")

        r = run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        check("approve-prints-r2", r.stdout.strip() == "2")

        r = run("note", "--workspace", str(ws), "--actor", "agent:worker",
                 "--text", "landed?")
        check("note-prints-r3", r.stdout.strip() == "3")

        r = run("frontier", "--workspace", str(ws), "--actor", "agent:worker",
                 "--text", "next step")
        check("frontier-prints-r4", r.stdout.strip() == "4")

        # --content-file carries bodies argv cannot: quoting-hostile text
        body = 'a "quoted" $body with `backticks` and\nnewlines\n'
        src = ws / "body-src.md"
        src.write_text(body, encoding="utf-8")
        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/from-file.md", "--content-file", str(src),
                 "--request-id", "req-file-1")
        check("effect-content-file-exit-0", r.returncode == 0)
        check("effect-content-file-written",
              (ws / "notes" / "from-file.md").read_text(encoding="utf-8") == body)
        receipt = json.loads(r.stdout)
        check("effect-prints-receipt",
              receipt["record"] == "receipt@1"
              and receipt["request_id"] == "req-file-1")

        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/x.md", "--content", "inline",
                 "--content-file", str(src), "--request-id", "req-both")
        check("effect-content-flags-exclusive", r.returncode == 2)

        r = run("status", "--workspace", str(ws), "--actor", "agent:worker",
                 "--brief")
        st = json.loads(r.stdout)
        check("status-brief-shape",
              set(st) == {"mission_id", "status", "revision", "amendments_count",
                          "frontier", "unresolved_verdicts", "notes_count",
                          "receipt_ids_count", "written_utc", "written_by"})
        check("status-brief-revision", st["revision"] == 5)

        # clean resume: stdout stays empty by contract; the summary (with the
        # vacuous-clean distinction) goes to stderr
        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("resume-clean-summary-on-stderr", "resume: clean" in r.stderr)
        check("resume-clean-not-vacuous", "vacuously" not in r.stderr)
        check("resume-clean-stdout-still-empty", r.stdout.strip() == "")


def test_resume_vacuous_clean_is_labelled() -> None:
    """Zero receipts means the drift check verified nothing -- the prior
    session read exactly this silence as tool breakage, three times."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-vacuous", "No effects yet.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("resume-vacuous-exit-0", r.returncode == 0)
        check("resume-vacuous-stdout-empty", r.stdout.strip() == "")
        check("resume-vacuous-labelled", "vacuously" in r.stderr)


def test_resume_missing_receipt_via_cli() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-lostrec", "Guard receipts.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "notes/a.md", "--content", "hello", "--request-id", "req-1")
        mission_dir = ws / "missions" / "m-cli-lostrec"
        for p in (mission_dir / "receipts").glob("*.json"):
            p.unlink()

        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("lostrec-exit-3", r.returncode == 3)
        check("lostrec-names-request-id", "RECEIPT-MISSING:req-1" in r.stdout)

        # the forgery channel is closed at the CLI: a decoy path cannot claim
        # the lost id (round-2 finding A ran this exact sequence and won)
        r = run("reconcile", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/decoy.md", "--content", "harmless decoy",
                 "--request-id", "req-1")
        check("lostrec-forgery-exit-2", r.returncode == 2)
        check("lostrec-decoy-not-written", not (ws / "notes" / "decoy.md").exists())

        r = run("acknowledge-loss", "--workspace", str(ws),
                 "--actor", "agent:worker", "--request-id", "req-1")
        check("lostrec-ack-exit-0", r.returncode == 0)
        check("lostrec-ack-prints-revision", r.stdout.strip().isdigit())
        r = run("resume", "--workspace", str(ws), "--actor", "agent:third")
        check("lostrec-clean-after-ack", r.returncode == 0)
        check("lostrec-clean-is-vacuous-again", "vacuously" in r.stderr)


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
    test_ascii_safe_drift_and_error_output,
    test_open_stop_rules_and_acceptable_costs,
    test_open_without_stop_rules_yields_empty_lists,
    test_success_output_confirms_the_write,
    test_resume_vacuous_clean_is_labelled,
    test_resume_missing_receipt_via_cli,
    test_no_mission_flags_outside_open,
]


def main() -> int:
    for fn in TESTS:
        fn()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
