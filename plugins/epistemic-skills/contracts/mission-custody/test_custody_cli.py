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
        run("begin-verification", "--workspace", str(ws), "--actor", "agent:worker")

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

        run("begin-verification", "--workspace", str(ws), "--actor", "agent:worker")

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

        run("begin-verification", "--workspace", str(ws), "--actor", "agent:worker")
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


def test_content_file_read_failures_are_refusals() -> None:
    """`--content-file` naming a missing or non-UTF-8 file must be the
    documented exit-2 refusal, not a traceback and exit 1.

    `_read_text` (instruction/text/reason) was hardened for exactly this and
    `_read_content` (effect/reconcile bodies) was not, so an ordinary input
    error on the ONE flag an operator uses most was indistinguishable from an
    internal crash. Measured before the fix:
    `effect --content-file <missing>` -> FileNotFoundError traceback, rc 1."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-cfile", "Exercise content-file refusals.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")

        missing = ws / "nope.txt"
        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                "--path", "a.md", "--content-file", str(missing),
                "--request-id", "req-missing")
        check("content-file-missing-exit-2", r.returncode == 2)
        check("content-file-missing-no-traceback",
              "Traceback" not in r.stderr)
        check("content-file-missing-names-the-flag",
              "content" in r.stderr.casefold())

        # PowerShell's bare `Out-File` writes UTF-16LE; the same class the
        # instruction/text readers already refuse.
        utf16 = ws / "utf16.txt"
        # WITH the BOM: bare UTF-16LE ASCII is NUL-padded and decodes as valid
        # (garbage) UTF-8, so it would not exercise the decode refusal at all.
        # The BOM's leading 0xFF is invalid UTF-8 in any position -- the shape
        # PowerShell's `Out-File` actually writes.
        utf16.write_bytes("hello".encode("utf-16"))
        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                "--path", "b.md", "--content-file", str(utf16),
                "--request-id", "req-utf16")
        check("content-file-utf16-exit-2", r.returncode == 2)
        check("content-file-utf16-no-traceback", "Traceback" not in r.stderr)

        # ... and reconcile reads the same helper.
        r = run("reconcile", "--workspace", str(ws), "--actor", "agent:worker",
                "--path", "a.md", "--content-file", str(missing),
                "--request-id", "req-missing-2")
        check("reconcile-content-file-missing-exit-2", r.returncode == 2)
        check("reconcile-content-file-missing-no-traceback",
              "Traceback" not in r.stderr)


def test_continuity_warning_is_ascii_safe() -> None:
    """The unreconciled-continuity warning interpolates an artifact path
    straight into stderr, bypassing `_ascii_safe`.

    Every other path-bearing output in this CLI is escaped; this one was
    added later and was not. Measured before the fix: a break on
    `notes/r\u00e9sum\u00e9.md` put a raw non-ASCII byte on stderr, which is
    what the ASCII-only output contract exists to prevent (a console codepage
    that cannot encode it turns a warning into a UnicodeEncodeError)."""
    e_acute = "\u00e9"
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        rel = f"notes/r{e_acute}sum{e_acute}.md"
        open_cli(ws, "m-cli-cont", "Exercise continuity warning output.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", rel, "--content", "x", "--request-id", "cont-1")
        # An unreceipted write BETWEEN two receipted events is the break.
        (ws / "notes" / f"r{e_acute}sum{e_acute}.md").write_text(
            "y", encoding="utf-8")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", rel, "--content", "z", "--request-id", "cont-2")

        r = run("resume", "--workspace", str(ws), "--actor", "agent:worker")
        check("continuity-warning-present",
              "unreconciled continuity break" in r.stderr)
        check("continuity-warning-stderr-is-ascii", r.stderr.isascii())
        check("continuity-warning-escapes-non-ascii",
              "\\xe9" in r.stderr)


def test_audit_report_kind_is_validatable() -> None:
    """`audit` labels its JSON `record: continuity-report@1`. A record label
    is a promise that the repository's own validator can read it -- and
    `validate_record` answered `unknown kind 'continuity-report@1'`, so the
    command's output was incompatible with the contract it claims membership
    in."""
    sys.path.insert(0, str(ROOT))
    from verify_mission_custody import validate_record  # noqa: E402

    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-audit", "Exercise audit record validity.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "a.md", "--content", "x", "--request-id", "aud-1")
        r = run("audit", "--workspace", str(ws), "--actor", "agent:worker")
        check("audit-exit-0-clean", r.returncode == 0)
        report = json.loads(r.stdout)
        check("audit-record-kind", report["record"] == "continuity-report@1")
        check("audit-report-validates", validate_record(report) == [])

        # A malformed report must still be REFUSED -- a validator that accepts
        # everything is not a validator (planted negative control).
        bad = dict(report)
        bad["continuity_breaks"] = "not-a-list"
        check("audit-report-negative-control", validate_record(bad) != [])


def test_audit_report_with_orphaned_receipt_validates() -> None:
    """`orphaned_retired_receipts()` supplies OBJECTS (request_id,
    receipt_path, note), but continuity-report@1's validator required a list
    of STRINGS -- so the report validated only while the orphan list was
    empty and was rejected precisely when an orphan was reported: the
    command's real output refused by the contract it claims membership in."""
    sys.path.insert(0, str(ROOT))
    from verify_mission_custody import validate_record  # noqa: E402

    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-cli-orphan", "Exercise orphan report validity.")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "a.md", "--content", "x", "--request-id", "orph-1")

        # An orphan is a receipt PRESENT for an id the chain RETIRED: lose
        # the file, acknowledge the loss (retires the id), restore the file.
        receipts = ws / "missions" / "m-cli-orphan" / "receipts"
        held = None
        for c in receipts.glob("*.json"):
            held = c.read_bytes()
            c.unlink()
        check("orphan-fixture-receipt-removed", held is not None)
        # acknowledge_receipt_loss is legal only from 'reopened': a
        # drift-detecting resume moves the mission there first.
        r = run("resume", "--workspace", str(ws), "--actor", "agent:second")
        check("orphan-fixture-resume-sees-the-loss", r.returncode == 3)
        r = run("acknowledge-loss", "--workspace", str(ws),
                "--actor", "agent:worker", "--request-id", "orph-1")
        check("orphan-fixture-loss-acknowledged", r.returncode == 0)
        import hashlib
        (receipts / (hashlib.sha256(b"orph-1").hexdigest() + ".json")
         ).write_bytes(held)

        # audit exits 3 when it has something to report -- the finding is
        # the fixture, not a failure of the command.
        r = run("audit", "--workspace", str(ws), "--actor", "agent:worker")
        check("orphan-audit-exit-3-reports-the-orphan", r.returncode == 3)
        report = json.loads(r.stdout)
        check("orphan-audit-lists-the-orphan",
              len(report["orphaned_retired_receipts"]) == 1)
        check("orphan-report-validates", validate_record(report) == [])

        # Negative control: the STRING shape the first validator demanded is
        # now the malformed input -- the check enforces the object shape,
        # it does not wave everything through.
        bad = dict(report)
        bad["orphaned_retired_receipts"] = ["orph-1"]
        check("orphan-report-negative-control", validate_record(bad) != [])


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
        run("begin-verification", "--workspace", str(ws), "--actor", "agent:worker")
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


def test_malformed_guards_json_returns_exit_2_without_traceback() -> None:
    """es#137 P2: malformed --guards-file JSON is a custody refusal (exit 2),
    not a traceback / exit 1. Named to match the issue acceptance test; covers
    both `open` and `amend`."""
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        bad = tmp / "guards.json"
        bad.write_text("{not-json", encoding="utf-8")
        opened = run("open", "--workspace", str(tmp), "--actor", "agent:t",
                     "--mission-id", "bad-json-open", "--instruction", "i",
                     "--operator", "operator:t", "--steward", "agent:t",
                     "--guards-file", str(bad), "--guard-mode", "enforce")
        check("open-malformed-guards-exit-2", opened.returncode == 2)
        check("open-malformed-guards-no-traceback",
              "Traceback" not in opened.stderr)
        check("open-malformed-guards-names-refusal",
              "CustodyError" in opened.stderr)

        ok_open = open_cli(tmp, "bad-json-amend", "i")
        check("amend-malformed-setup-open", ok_open.returncode == 0)
        run("approve", "--workspace", str(tmp), "--actor", "agent:worker")
        amended = run("amend", "--workspace", str(tmp),
                      "--actor", "agent:worker",
                      "--text", "operator: arm with bad json",
                      "--guards-file", str(bad), "--guard-mode", "enforce")
        check("amend-malformed-guards-exit-2", amended.returncode == 2)
        check("amend-malformed-guards-no-traceback",
              "Traceback" not in amended.stderr)
        check("amend-malformed-guards-names-refusal",
              "CustodyError" in amended.stderr)


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
        run("begin-verification", "--workspace", str(ws), "--actor", "agent:worker")
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


def test_scope_ack_has_a_cli_door() -> None:
    """A gate with no door is not a gate, it is a wedge.

    `scope_ack` shipped as a Python parameter only: `accept` had no
    --scope-ack and never passed one, so through the ONLY supported surface a
    legitimate, operator-granted piece of drift was permanently un-PASSable --
    and the refusal message named a remedy that did not exist. Writing a
    control without installing it, in the refusal text of the control itself."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        run("open", "--mission-id", "m-door", "--instruction", "w",
            "--operator", "op", "--steward", "agent:worker",
            "--actor", "agent:worker", "--scope-out", "secrets.env",
            "--workspace", str(ws))
        run("approve", "--actor", "agent:worker", "--workspace", str(ws))
        run("effect", "--path", "secrets.env", "--content", "TOKEN=x",
            "--request-id", "r1", "--actor", "agent:worker",
            "--workspace", str(ws))
        run("begin-verification", "--actor", "agent:worker", "--workspace", str(ws))

        accept = ["accept", "--verdict", "PASS", "--actor", "agent:acceptor",
                  "--acceptor", "agent:acceptor",
                  "--tier", "declared-role-separation", "--reason", "done",
                  "--workspace", str(ws)]
        refused = run(*accept)
        check("cli-accept-refuses-unacknowledged-drift", refused.returncode == 2)
        # the refusal must name the flag an acceptor can actually type
        check("cli-refusal-names-the-real-flag",
              "--scope-ack secrets.env" in (refused.stdout + refused.stderr))

        ok = run(*accept, "--scope-ack", "secrets.env")
        check("cli-scope-ack-discharges", ok.returncode == 0)


def test_verify_is_read_only_and_reports_chain() -> None:
    """es#138 oracle 1: `verify` mutates NOTHING -- no checkpoint appended,
    status unchanged -- and reports chain_ok on a healthy chain."""
    import shutil
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-ro", "instruction text", actor="agent:worker")
        run("approve", "--workspace", str(ws), "--actor", "operator:SternOne")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "a.txt", "--content", "x", "--request-id", "r1")
        cps = ws / "missions" / "m-ro" / "checkpoints"
        before = sorted(cps.iterdir())
        st_before = json.loads(run("status", "--workspace", str(ws),
                                   "--actor", "agent:worker").stdout)
        r = run("verify", "--workspace", str(ws), "--actor", "agent:auditor")
        audit = json.loads(r.stdout)
        after = sorted(cps.iterdir())
        st_after = json.loads(run("status", "--workspace", str(ws),
                                  "--actor", "agent:worker").stdout)
        check("verify-exit-0", r.returncode == 0)
        check("verify-read-only-flag", audit["read_only"] is True)
        check("verify-chain-ok", audit["chain_ok"] is True)
        check("verify-no-checkpoint-appended", before == after)
        check("verify-status-unchanged",
              st_before["status"] == st_after["status"] == "active")
        shutil.rmtree(ws, ignore_errors=True)


def test_verify_detects_tampered_chain() -> None:
    """es#138 oracle 2: a tampered checkpoint is REFUSED loudly at load
    (nonzero exit, stderr names the checkpoint) -- and verify still writes
    nothing. The store's load-time schema/hash validation is the detection;
    the read-only requirement holds even on a broken chain."""
    import shutil
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-tamper", "instruction text", actor="agent:worker")
        run("approve", "--workspace", str(ws), "--actor", "operator:SternOne")
        run("effect", "--workspace", str(ws), "--actor", "agent:worker",
            "--path", "a.txt", "--content", "x", "--request-id", "r1")
        cps = ws / "missions" / "m-tamper" / "checkpoints"
        target = sorted(cps.glob("*.json"))[0]
        rec = json.loads(target.read_text(encoding="utf-8"))
        rec["note"] = "tampered: field altered after the fact"
        target.write_text(json.dumps(rec, indent=2), encoding="utf-8")
        before = sorted(cps.iterdir())
        r = run("verify", "--workspace", str(ws), "--actor", "agent:auditor")
        after = sorted(cps.iterdir())
        check("tamper-nonzero-exit", r.returncode != 0)
        check("tamper-names-checkpoint",
              "r00000001.json" in (r.stdout + r.stderr))
        check("tamper-still-no-writes", before == after)
        shutil.rmtree(ws, ignore_errors=True)



# --- Codex MODERATE/MINOR triage, 2026-08-25 ------------------------------


def run_env(env_extra: dict, *args: str) -> subprocess.CompletedProcess:
    """`run`, plus environment: the session binding's second channel lives
    there, and its precedence against the flag is the thing under test."""
    import os
    env = {**os.environ, **env_extra}
    return subprocess.run(
        [sys.executable, str(CLI), *args], capture_output=True, text=True,
        env=env)


def test_empty_mission_flag_never_defers_to_the_environment() -> None:
    """`custody effect --mission "$MISSION_ID"` with an unset variable passes
    an EMPTY flag. Treating that as absent handed the session back to a stale
    ZMS_MISSION_ID, so the effect landed under a different mission's
    authority -- against the documented flag-over-environment precedence."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        for name in ("m-stale", "m-real"):
            open_cli(ws, name, "two missions")
            run("approve", "--workspace", str(ws), "--actor", "agent:worker",
                "--mission", name)
        r = run_env({"ZMS_MISSION_ID": "m-stale"},
                    "effect", "--workspace", str(ws), "--actor", "agent:worker",
                    "--mission", "", "--path", "notes/a.md",
                    "--content", "x", "--request-id", "req-1")
        check("empty-mission-flag-refuses", r.returncode == 2)
        check("empty-mission-flag-names-the-binding-rule",
              "BindingInvalid" in r.stderr)
        check("empty-mission-flag-wrote-nothing",
              not (ws / "notes" / "a.md").exists())
        check("empty-mission-flag-did-not-use-the-environment",
              not list((ws / "missions" / "m-stale" / "receipts").glob("*")))


def test_missions_validates_its_own_session_binding() -> None:
    """Case rows 4/9/15: a present binding is validated on EVERY verb.
    `missions` was the one verb that silently accepted a stale
    ZMS_MISSION_ID. Read-only, so nothing was misrouted -- but "the binding
    you are holding is dead" is what an operator running it wants to know."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-live", "the live one")
        r = run_env({"ZMS_MISSION_ID": "m-gone"},
                    "missions", "--workspace", str(ws), "--actor",
                    "agent:worker")
        check("missions-refuses-a-stale-binding", r.returncode == 2)
        check("missions-names-the-stale-binding", "m-gone" in r.stderr)
        r = run_env({"ZMS_MISSION_ID": "m-live"},
                    "missions", "--workspace", str(ws), "--actor",
                    "agent:worker")
        check("missions-accepts-a-valid-binding", r.returncode == 0)


def test_missions_survives_an_unreadable_mission_dir() -> None:
    """The per-row handler caught only (StoreError, ValueError) while
    `load_latest` can raise OSError, and `main()` catches neither -- so one
    unreadable mission dir killed the listing with a traceback instead of
    emitting an `unreadable` row and continuing."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "m-live", "the live one")
        # A DIRECTORY where the checkpoint file belongs: reading it raises
        # IsADirectoryError (POSIX) / PermissionError (NT) -- both OSError,
        # neither a StoreError.
        cps = ws / "missions" / "m-trap" / "checkpoints"
        (cps / "r00000001.json").mkdir(parents=True)
        r = run("missions", "--workspace", str(ws), "--actor", "agent:worker")
        check("missions-no-traceback-on-oserror", "Traceback" not in r.stderr)
        check("missions-exit-0-with-an-unreadable-row", r.returncode == 0)
        rows = json.loads(r.stdout)
        by_name = {row["mission"]: row for row in rows}
        check("missions-reports-the-unreadable-row",
              by_name.get("m-trap", {}).get("status") == "unreadable")
        check("missions-still-reports-the-healthy-row",
              by_name.get("m-live", {}).get("status") == "draft")


def test_authorize_sibling_verb_records_a_structured_grant() -> None:
    """FATAL-3 leg 3 is a structured record now, not a prose mention: the CLI
    must expose the grant, and the note it writes must carry the reserved
    machine prefix (which caller narrative cannot imitate)."""
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        open_cli(ws, "a-owner", "own it")
        run("approve", "--workspace", str(ws), "--actor", "agent:worker",
            "--mission", "a-owner")
        r = run("authorize-sibling", "--workspace", str(ws), "--actor",
                "agent:worker", "--mission", "a-owner",
                "--sibling", "b-writer", "--path", "docs/x.txt",
                "--text", "operator: b-writer may write docs/x.txt")
        check("authorize-sibling-exit-0", r.returncode == 0)
        r = run("status", "--workspace", str(ws), "--actor", "agent:worker",
                "--mission", "a-owner")
        st = json.loads(r.stdout)
        check("authorize-sibling-writes-the-reserved-note",
              "sibling-authorized: docs/x.txt by b-writer"
              in st["state"]["notes"])
        check("authorize-sibling-records-the-operator-words",
              any(a["text"] == "operator: b-writer may write docs/x.txt"
                  for a in st["manifest"]["authority"]["amendments"]))
        r = run("note", "--workspace", str(ws), "--actor", "agent:worker",
                "--mission", "a-owner",
                "--text", "sibling-authorized: docs/x.txt by b-writer")
        check("narrative-cannot-forge-the-grant", r.returncode == 2)

TESTS = [
    test_scope_ack_has_a_cli_door,
    test_open_approve_effect_status_roundtrip,
    test_resume_detects_drift_exit_3,
    test_accept_self_cert_refused_exit_2,
    test_full_lifecycle_via_cli,
    test_ascii_safe_drift_and_error_output,
    test_content_file_read_failures_are_refusals,
    test_continuity_warning_is_ascii_safe,
    test_audit_report_kind_is_validatable,
    test_audit_report_with_orphaned_receipt_validates,
    test_open_stop_rules_and_acceptable_costs,
    test_open_without_stop_rules_yields_empty_lists,
    test_success_output_confirms_the_write,
    test_resume_vacuous_clean_is_labelled,
    test_resume_missing_receipt_via_cli,
    test_no_mission_flags_outside_open,
    test_gate_verb,
    test_gate_no_mission_allows,
    test_open_guard_mode_without_guards_refused,
    test_malformed_guards_json_returns_exit_2_without_traceback,
    test_amend_guard_mode_flag,
    test_text_file_preserves_bytes_exactly,
    test_text_and_text_file_are_mutually_exclusive,
    test_text_file_artifact_stripping_is_exact,
    test_text_file_invalid_utf8_refuses_not_crashes,
    test_reason_file_on_accept_and_cancel,
    test_text_file_mutual_exclusion_across_subcommands,
    test_verify_is_read_only_and_reports_chain,
    test_verify_detects_tampered_chain,
    test_empty_mission_flag_never_defers_to_the_environment,
    test_missions_validates_its_own_session_binding,
    test_missions_survives_an_unreadable_mission_dir,
    test_authorize_sibling_verb_records_a_structured_grant,
]


def main() -> int:
    for fn in TESTS:
        fn()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0



if __name__ == "__main__":
    raise SystemExit(main())
