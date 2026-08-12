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
        # Shape deliberately widened: the envelope previously had NO read
        # surface anywhere -- _brief omitted it and resume printed no manifest
        # content -- so every "the steward should read scope/stop_rules"
        # argument was about text nothing ever displayed. Updated as an
        # intended change, not patched to chase a red.
        check("status-brief-shape",
              set(st) == {"mission_id", "status", "revision", "amendments_count",
                          "frontier", "unresolved_verdicts", "notes_count",
                          "receipt_ids_count", "written_utc", "written_by",
                          "checkpoints_since_last_amendment",
                          "envelope_advisory", "envelope_unset"})
        # acceptable_costs belongs here too: the ENFORCEMENT STATUS table names
        # it a declaration read by the steward AND the acceptor, so omitting it
        # let a resumed steward see the advisory header and every other field
        # while still missing the mission's cost boundary.
        # permissions belongs here for the same reason acceptable_costs does:
        # the manifest skill treats it as part of the envelope the operator
        # confirms, so a steward reading the newly-advertised envelope would
        # otherwise still miss the mission's allowed-action boundary.
        check("status-brief-envelope-keys",
              set(st["envelope_advisory"]) == {
                  "scope_in", "scope_out", "permissions", "protected_state",
                  "hold_if", "stop_if", "escalate_if", "acceptable_costs"})
        # this fixture opens with no envelope flags at all, so every field is
        # unset -- silence must not be allowed to imply boundedness
        check("status-brief-names-unset-envelope-fields",
              set(st["envelope_unset"]) == set(st["envelope_advisory"]))
        check("status-brief-amendment-latency-none-when-never-amended",
              st["checkpoints_since_last_amendment"] is None)
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


def test_gate_verb() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        # open an enforced mission guarding 'rm -rf'
        guards = [{"name": "no-rm", "tool_names": ["Bash"],
                   "command_regexes": ["rm -rf"], "path_globs": []}]
        gfile = tmp / "guards.json"
        gfile.write_text(json.dumps(guards), encoding="utf-8")
        run("open", "--workspace", str(tmp), "--actor", "agent:t",
            "--mission-id", "gate-cli", "--instruction", "i",
            "--operator", "operator:t", "--steward", "agent:t",
            "--guards-file", str(gfile), "--guard-mode", "enforce")
        run("approve", "--workspace", str(tmp), "--actor", "agent:t")
        blocked = subprocess.run(
            [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
             "--actor", "hook:custody-gate"],
            input=json.dumps({"tool_name": "Bash", "command": "rm -rf x",
                              "file_path": None}),
            capture_output=True, text=True)
        check("gate-blocks-enforced", blocked.returncode == 2)
        verdict = json.loads(blocked.stdout)
        check("gate-verdict-fields",
              verdict["decision"] == "block" and verdict["rule"] == "no-rm")
        allowed = subprocess.run(
            [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
             "--actor", "hook:custody-gate"],
            input=json.dumps({"tool_name": "Bash", "command": "ls",
                              "file_path": None}),
            capture_output=True, text=True)
        check("gate-allows-unmatched", allowed.returncode == 0)


def test_gate_no_mission_allows() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        res = subprocess.run(
            [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
             "--actor", "hook:custody-gate"],
            input=json.dumps({"tool_name": "Bash", "command": "rm -rf /"}),
            capture_output=True, text=True)
        check("gate-no-mission-exit-0", res.returncode == 0)


def test_open_guard_mode_without_guards_refused() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        res = run("open", "--workspace", str(tmp), "--actor", "agent:t",
                  "--mission-id", "bad-open", "--instruction", "i",
                  "--operator", "operator:t", "--steward", "agent:t",
                  "--guard-mode", "audit")
        check("open-mode-without-guards-refused", res.returncode == 2)


def test_amend_guard_mode_flag() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        run("open", "--workspace", str(tmp), "--actor", "agent:t",
            "--mission-id", "amend-cli", "--instruction", "i",
            "--operator", "operator:t", "--steward", "agent:t")
        run("approve", "--workspace", str(tmp), "--actor", "agent:t")
        guards = [{"name": "g", "tool_names": ["Bash"],
                   "command_regexes": ["x"], "path_globs": []}]
        gfile = tmp / "g.json"
        gfile.write_text(json.dumps(guards), encoding="utf-8")
        res = run("amend", "--workspace", str(tmp), "--actor", "agent:t",
                  "--text", "operator: arm audit mode",
                  "--guards-file", str(gfile), "--guard-mode", "audit")
        check("amend-guards-accepted", res.returncode == 0)


def test_text_file_preserves_bytes_exactly() -> None:
    """A verbatim grant must survive the CLI byte-for-byte.

    The inline flags travel argv, where a shell can rewrite the string before
    the contract ever sees it -- and the corruption is then hashed, chained and
    sealed as authoritative, so no downstream guarantee can catch it (es#133).
    The file path is the one that must be exact."""
    hostile = ('operator grants: run `amend` and $HOME cleanup; '
               '"quoted" \'single\' and $(date) stay literal; 100% & <>|;')
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        grant = Path(tmp) / "grant.txt"
        # a trailing newline is what a heredoc or editor leaves behind; it must
        # be stripped, not recorded as part of what the operator said
        grant.write_text(hostile + "\n", encoding="utf-8", newline="")

        r = run("open", "--workspace", str(ws), "--actor", "agent:w",
                "--mission-id", "textfile", "--instruction-file", str(grant),
                "--operator", "operator:zach", "--steward", "agent:w")
        check("open-instruction-file-exit-0", r.returncode == 0)
        run("approve", "--workspace", str(ws), "--actor", "agent:w")

        r = run("amend", "--workspace", str(ws), "--actor", "agent:w",
                "--text-file", str(grant))
        check("amend-text-file-exit-0", r.returncode == 0)

        auth = json.loads(run("status", "--workspace", str(ws),
                               "--actor", "agent:w").stdout)["manifest"]["authority"]
        check("instruction-byte-identical", auth["instruction"] == hostile)
        check("amendment-byte-identical", auth["amendments"][0]["text"] == hostile)

        check("note-text-file-exit-0",
              run("note", "--workspace", str(ws), "--actor", "agent:w",
                  "--text-file", str(grant)).returncode == 0)
        check("frontier-text-file-exit-0",
              run("frontier", "--workspace", str(ws), "--actor", "agent:w",
                  "--text-file", str(grant)).returncode == 0)
        st = json.loads(run("status", "--workspace", str(ws),
                             "--actor", "agent:w").stdout)
        check("note-byte-identical", st["state"]["notes"][-1] == hostile)
        check("frontier-byte-identical", st["state"]["frontier"] == hostile)


def test_text_file_artifact_stripping_is_exact() -> None:
    """Exactly two editor artifacts are removed, and nothing else.

    A greedy rstrip("\r\n") ate an operator's deliberate trailing blank line,
    and plain utf-8 decoding let a PowerShell-written BOM become the first
    character of a "verbatim" grant -- both silently, both producing a record
    that is intact and wrong."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        multi = Path(tmp) / "multi.txt"
        # deliberate blank line at the end, CRLF throughout: only the LAST
        # terminator is an artifact, the blank line is content
        multi.write_bytes(b"Line one.\r\nLine two.\r\n\r\n")
        r = run("open", "--workspace", str(ws), "--actor", "agent:w",
                "--mission-id", "artifacts", "--instruction-file", str(multi),
                "--operator", "operator:zach", "--steward", "agent:w")
        check("multiline-open-exit-0", r.returncode == 0)
        st = json.loads(run("status", "--workspace", str(ws),
                             "--actor", "agent:w").stdout)
        check("multiline-blank-line-preserved",
              st["manifest"]["authority"]["instruction"]
              == "Line one.\r\nLine two.\r\n")

        run("approve", "--workspace", str(ws), "--actor", "agent:w")
        bom = Path(tmp) / "bom.txt"
        bom.write_bytes(b"\xef\xbb\xbf" + b"operator grants: proceed\n")
        r = run("amend", "--workspace", str(ws), "--actor", "agent:w",
                "--text-file", str(bom))
        check("bom-amend-exit-0", r.returncode == 0)
        st = json.loads(run("status", "--workspace", str(ws),
                             "--actor", "agent:w").stdout)
        check("bom-stripped-from-verbatim-grant",
              st["manifest"]["authority"]["amendments"][0]["text"]
              == "operator grants: proceed")


def test_text_file_invalid_utf8_refuses_not_crashes() -> None:
    """PowerShell's bare Out-File writes UTF-16LE. Letting UnicodeDecodeError
    escape exits 1 with a traceback, breaking the documented 0/2/3 contract."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        bad = Path(tmp) / "utf16.txt"
        bad.write_bytes(b"\xff\xfeo\x00p\x00")
        r = run("open", "--workspace", str(ws), "--actor", "agent:w",
                "--mission-id", "badenc", "--instruction-file", str(bad),
                "--operator", "operator:zach", "--steward", "agent:w")
        check("invalid-utf8-exit-2", r.returncode == 2)
        check("invalid-utf8-names-custody-error", "CustodyError" in r.stderr)
        check("invalid-utf8-no-traceback", "Traceback" not in r.stderr)


def test_reason_file_on_accept_and_cancel() -> None:
    """accept's reason is hash-chained into the acceptance-verdict record --
    the same exactness stakes as an amendment, and previously untested."""
    reason = "accepted: `verified` end-to-end; $SCOPE unchanged; 100% green"
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        rf = Path(tmp) / "reason.txt"
        rf.write_text(reason + "\n", encoding="utf-8", newline="")
        open_cli(ws, "reasonfile", "instruction")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        r = run("accept", "--workspace", str(ws), "--actor", "agent:acceptor",
                "--verdict", "PASS", "--acceptor", "agent:acceptor",
                "--tier", "declared-role-separation", "--reason-file", str(rf))
        check("accept-reason-file-exit-0", r.returncode == 0)
        verdicts = list((ws / "missions" / "reasonfile" / "verdicts").glob("*.json"))
        check("accept-reason-byte-identical",
              bool(verdicts) and json.loads(
                  verdicts[0].read_text(encoding="utf-8"))["reason"] == reason)

    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        rf = Path(tmp) / "reason.txt"
        rf.write_text(reason + "\n", encoding="utf-8", newline="")
        open_cli(ws, "cancelfile", "instruction")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        r = run("cancel", "--workspace", str(ws), "--actor", "agent:worker",
                "--reason-file", str(rf))
        check("cancel-reason-file-exit-0", r.returncode == 0)


def test_text_file_mutual_exclusion_across_subcommands() -> None:
    """Mutual exclusion must hold on every verb that takes text, not only the
    one that happened to get a test."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        f = Path(tmp) / "t.txt"
        f.write_text("x", encoding="utf-8")
        r = run("open", "--workspace", str(ws), "--actor", "agent:w",
                "--mission-id", "excl2", "--instruction", "a",
                "--instruction-file", str(f),
                "--operator", "op", "--steward", "agent:w")
        check("open-both-instruction-flags-refused", r.returncode == 2)

        open_cli(ws, "excl2", "instruction")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        for verb in ("amend", "frontier"):
            r = run(verb, "--workspace", str(ws), "--actor", "agent:worker",
                    "--text", "a", "--text-file", str(f))
            check(f"{verb}-both-text-flags-refused", r.returncode == 2)


def test_text_and_text_file_are_mutually_exclusive() -> None:
    """Both flags is ambiguous about which is the record of truth; neither
    leaves the verb with nothing to record. Both refuse."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        grant = Path(tmp) / "g.txt"
        grant.write_text("hello", encoding="utf-8")
        open_cli(ws, "excl", "instruction")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")

        check("note-both-flags-refused",
              run("note", "--workspace", str(ws), "--actor", "agent:worker",
                  "--text", "a", "--text-file", str(grant)).returncode == 2)
        check("note-neither-flag-refused",
              run("note", "--workspace", str(ws),
                  "--actor", "agent:worker").returncode == 2)


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
    test_gate_verb,
    test_gate_no_mission_allows,
    test_open_guard_mode_without_guards_refused,
    test_amend_guard_mode_flag,
    test_text_file_preserves_bytes_exactly,
    test_text_and_text_file_are_mutually_exclusive,
    test_text_file_artifact_stripping_is_exact,
    test_text_file_invalid_utf8_refuses_not_crashes,
    test_reason_file_on_accept_and_cancel,
    test_text_file_mutual_exclusion_across_subcommands,
]


def main() -> int:
    for fn in TESTS:
        fn()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
