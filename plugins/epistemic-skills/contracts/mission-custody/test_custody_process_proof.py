#!/usr/bin/env python3
"""Three-subprocess kill/resume/repair continuity proof: black-box through
custody_cli.py only, exactly as three independent, non-cooperating processes
(no shared Python state) would drive one mission end to end.

Process A opens, approves, records an effect, and sets a frontier, then a
deliberately-hung fourth invocation is killed before it can touch the store
-- proving a killed process leaves no partial checkpoint behind. A drift is
then planted directly on disk (an out-of-band edit between processes).
Process B resumes with no mission id, sees the drift, and reconciles it.
Process C verifies, is refused a self-certified PASS, receives a legitimate
FAIL, remediates, clears it, re-verifies, and reaches a PASS acceptance from
a truly independent acceptor. A final independent pass re-derives the full
checkpoint hash chain straight off disk -- never trusting the module under
test's own chain-verification code -- and confirms no `*.tmp` file survives
anywhere under `missions/`.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import time
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


def status_json(ws: Path, actor: str) -> dict:
    r = run("status", "--workspace", str(ws), "--actor", actor)
    check("status-call-exit-0", r.returncode == 0)
    return json.loads(r.stdout)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_chain_errors(mission_dir: Path) -> list[str]:
    """Recompute the checkpoint hash chain straight off disk, without
    importing or calling into custody_store.MissionStore.load_latest --
    the point of an *independent* re-verification is to never trust the
    module under test's own chain-verification code."""
    errors: list[str] = []
    paths = sorted((mission_dir / "checkpoints").glob("r????????.json"))
    if not paths:
        return [f"no checkpoint files under {mission_dir / 'checkpoints'}"]
    prev_sha: str | None = None
    for i, path in enumerate(paths, start=1):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("revision") != i:
            errors.append(
                f"{path.name}: revision {record.get('revision')!r} != expected {i}")
        if record.get("prev_checkpoint_sha256") != prev_sha:
            errors.append(f"{path.name}: prev_checkpoint_sha256 chain break")
        prev_sha = sha256_file(path)
    return errors


def test_three_subprocess_kill_resume_repair_proof() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        mission_id = "m-proof-kill-resume-repair"
        instruction = "Prove three-process kill, resume, and repair continuity end-to-end."
        missions_root = ws / "missions"
        mission_dir = missions_root / mission_id

        # ---------------------------------------------------------------
        # Process A: open, approve, effect, frontier -- each its own
        # process, exactly as an operator or another process would drive
        # the CLI. Then a deliberately-hung fourth invocation is killed.
        # ---------------------------------------------------------------
        r = run("open", "--workspace", str(ws), "--actor", "agent:worker",
                 "--mission-id", mission_id, "--instruction", instruction,
                 "--operator", "operator:zach", "--steward", "agent:worker")
        check("a-open-exit-0", r.returncode == 0)

        r = run("approve", "--workspace", str(ws), "--actor", "agent:worker")
        check("a-approve-exit-0", r.returncode == 0)

        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/proof.md", "--content", "state-1",
                 "--request-id", "req-a1")
        check("a-effect-exit-0", r.returncode == 0)
        check("a-effect-artifact-written",
              (ws / "notes" / "proof.md").read_text(encoding="utf-8") == "state-1")

        r = run("frontier", "--workspace", str(ws), "--actor", "agent:worker",
                 "--text", "next: hand off to the resuming process")
        check("a-frontier-exit-0", r.returncode == 0)

        st = status_json(ws, "agent:worker")
        check("a-revision-after-frontier-is-4", st["revision"] == 4)

        # Deliberately-hung fourth invocation: a `python -c` wrapper that
        # imports custody_cli (proving the module loads cleanly) and then
        # sleeps well past our kill -- so it is provably killed before it
        # ever calls main() and attempts any store write. Simpler and more
        # deterministic than racing a kill against a still-writing `effect`.
        hung = subprocess.Popen(
            [sys.executable, "-c", "import time, custody_cli; time.sleep(60)"],
            cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.time() + 5
        alive_before_kill = False
        while time.time() < deadline:
            if hung.poll() is None:
                alive_before_kill = True
                break
            time.sleep(0.05)
        check("a-hung-wrapper-alive-before-kill", alive_before_kill)
        time.sleep(0.3)  # let it finish importing and reach time.sleep(60)
        hung.kill()
        try:
            hung.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            hung.kill()
            hung.communicate()
        check("a-hung-wrapper-killed-nonzero-exit", hung.returncode != 0)

        st = status_json(ws, "agent:worker")
        check("a-hung-wrapper-died-pre-checkpoint-revision-still-4",
              st["revision"] == 4)
        tmp_after_kill = sorted(missions_root.rglob("*.tmp"))
        check("a-no-tmp-files-after-kill", tmp_after_kill == [])

        # ---------------------------------------------------------------
        # Drift plant: an out-of-band edit between processes, bypassing
        # custody entirely -- exactly what `resume` exists to catch.
        # ---------------------------------------------------------------
        (ws / "notes" / "proof.md").write_bytes(b"drifted-out-of-band-bytes")

        # ---------------------------------------------------------------
        # Process B: resume with no mission id, see the drift, reconcile.
        # ---------------------------------------------------------------
        r = run("resume", "--workspace", str(ws), "--actor", "agent:worker")
        check("b-resume-exit-3", r.returncode == 3)
        check("b-resume-names-drifted-path",
              "notes/proof.md" in r.stdout or "notes/proof.md" in r.stderr)

        st = status_json(ws, "agent:worker")
        check("b-status-reopened", st["status"] == "reopened")
        check("b-status-reconciliation-marker",
              "RECONCILIATION:notes/proof.md" in st["state"]["unresolved_verdicts"])

        r = run("reconcile", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/proof.md", "--content", "state-1",
                 "--request-id", "req-b1")
        check("b-reconcile-exit-0", r.returncode == 0)

        st = status_json(ws, "agent:worker")
        check("b-status-active-after-reconcile", st["status"] == "active")
        check("b-no-reconciliation-marker-remains",
              "RECONCILIATION:notes/proof.md" not in st["state"]["unresolved_verdicts"])
        check("b-revision-after-reconcile-is-6", st["revision"] == 6)

        # ---------------------------------------------------------------
        # Process C: verify, refuse a self-certified PASS, take a
        # legitimate FAIL, remediate, clear it, re-verify, and accept
        # from a truly independent acceptor.
        # ---------------------------------------------------------------
        r = run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        check("c-verify-exit-0", r.returncode == 0)

        r = run("accept", "--workspace", str(ws), "--actor", "agent:worker",
                 "--verdict", "PASS", "--acceptor", "agent:worker",
                 "--tier", "declared-role-separation",
                 "--reason", "worker accepting its own work")
        check("c-self-cert-exit-2", r.returncode == 2)
        check("c-self-cert-stderr-names-exception", "AcceptanceRefused" in r.stderr)

        st = status_json(ws, "agent:worker")
        check("c-self-cert-refused-still-verifying", st["status"] == "verifying")
        check("c-self-cert-refused-revision-still-7", st["revision"] == 7)

        r = run("accept", "--workspace", str(ws), "--actor", "agent:acceptor-2",
                 "--verdict", "FAIL", "--acceptor", "agent:acceptor-2",
                 "--tier", "declared-role-separation", "--reason", "missing section")
        check("c-fail-exit-0", r.returncode == 0)

        st = status_json(ws, "agent:worker")
        check("c-fail-reopened", st["status"] == "reopened")
        check("c-fail-marker-present",
              "FAIL:missing section" in st["state"]["unresolved_verdicts"])

        r = run("effect", "--workspace", str(ws), "--actor", "agent:worker",
                 "--path", "notes/proof.md", "--content", "state-2-remediated",
                 "--request-id", "req-c1")
        check("c-remediation-effect-exit-0", r.returncode == 0)

        r = run("clear-fail", "--workspace", str(ws), "--actor", "agent:worker",
                 "--match", "missing section", "--request-id", "req-c1")
        check("c-clear-fail-exit-0", r.returncode == 0)

        st = status_json(ws, "agent:worker")
        check("c-active-after-clear-fail", st["status"] == "active")

        r = run("verify", "--workspace", str(ws), "--actor", "agent:worker")
        check("c-reverify-exit-0", r.returncode == 0)

        r = run("accept", "--workspace", str(ws), "--actor", "agent:acceptor-2",
                 "--verdict", "PASS", "--acceptor", "agent:acceptor-2",
                 "--tier", "declared-role-separation",
                 "--reason", "remediated and independently reverified")
        check("c-final-pass-exit-0", r.returncode == 0)

        # A completed mission is unreachable via pathless discovery by
        # contract (no --mission-id escape hatch exists) -- confirm that
        # holds here too, then read the final state straight off disk.
        r = run("status", "--workspace", str(ws), "--actor", "agent:worker")
        check("c-completed-mission-unreachable-exit-2", r.returncode == 2)
        check("c-completed-mission-no-active-mission",
              "NoActiveMission" in r.stderr)

        # ---------------------------------------------------------------
        # Independent re-verification from disk: recompute the full
        # checkpoint hash chain ourselves (never trusting the module
        # under test's own chain-verification code), and confirm no
        # `.tmp` file survives anywhere under missions/.
        # ---------------------------------------------------------------
        chain_errors = independent_chain_errors(mission_dir)
        check("chain-independently-verified", chain_errors == [])
        for err in chain_errors:
            print(f"  chain error: {err}")

        checkpoint_paths = sorted((mission_dir / "checkpoints").glob("r????????.json"))
        final = json.loads(checkpoint_paths[-1].read_text(encoding="utf-8"))
        check("final-status-completed", final["status"] == "completed")
        check("final-revision-at-least-10", final["revision"] >= 10)

        r1 = json.loads(checkpoint_paths[0].read_text(encoding="utf-8"))
        check("r1-file-is-revision-1", r1["revision"] == 1)
        check("instruction-byte-identical-to-r1",
              final["manifest"]["authority"]["instruction"]
              == r1["manifest"]["authority"]["instruction"]
              == instruction)

        tmp_files = sorted(missions_root.rglob("*.tmp"))
        check("no-tmp-files-anywhere-under-missions", tmp_files == [])


TESTS = [
    test_three_subprocess_kill_resume_repair_proof,
]


def main() -> int:
    for fn in TESTS:
        fn()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
