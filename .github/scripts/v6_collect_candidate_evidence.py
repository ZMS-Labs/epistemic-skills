#!/usr/bin/env python3
"""Collect ES6-V6-CANDIDATE requalification evidence (public-content + custody).

Does not run clean-room CI; that must target a committed SHA via
v6_run_clean_baseline.py after the freeze files are committed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CUSTODY_WF = REPO_ROOT / ".github/workflows/mission-custody-contract.yml"
PUBLIC_CONTENT = REPO_ROOT / ".github/scripts/check_public_content.py"


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def custody_test_commands() -> list[str]:
    """Unique `python …/test_*.py` commands from the Linux contract job."""
    text = CUSTODY_WF.read_text(encoding="utf-8")
    commands: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("run: python plugins/epistemic-skills/contracts/mission-custody/test_"):
            continue
        cmd = line[len("run: ") :]
        if cmd in seen:
            continue
        seen.add(cmd)
        commands.append(cmd)
    return commands


def _portable(cmd: str) -> str:
    """Record a command a READER can re-run from the repo root.

    Recording ``sys.executable`` and absolute script paths stamped the build
    host's interpreter and checkout -- including a scratch directory carrying a
    session id -- into committed evidence. The public-content pattern set was
    structurally blind to that class (publication-gate finding PG-24). The
    normalized form is equivalent, portable, and reviewable; the command
    actually executed is unchanged.
    """
    return cmd.replace(sys.executable, "python").replace(f"{REPO_ROOT}/", "")


def run_cmd(cmd: str) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        shell=True,
        capture_output=True,
        text=True,
    )
    return {
        "command": _portable(cmd),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "passed": proc.returncode == 0,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def collect_public_content(sha: str, dest: Path) -> dict:
    self_test = run_cmd(f"{sys.executable} {PUBLIC_CONTENT} --self-test")
    live = run_cmd(f"{sys.executable} {PUBLIC_CONTENT}")
    payload = {
        "schema": "public-content-evidence@1",
        "program": "ES6-V6-CANDIDATE",
        "exact_start_sha": sha,
        "generated_at": _now(),
        "self_test": self_test,
        "live": live,
        "passed": bool(self_test["passed"] and live["passed"]),
    }
    write_json(dest, payload)
    return payload


def collect_custody(sha: str, dest: Path) -> dict:
    commands = custody_test_commands()
    steps = [run_cmd(f"{sys.executable} {cmd[len('python '):]}") for cmd in commands]
    payload = {
        "schema": "custody-suite-evidence@1",
        "program": "ES6-V6-CANDIDATE",
        "exact_start_sha": sha,
        "generated_at": _now(),
        "steps": steps,
        "passed": all(step["passed"] for step in steps) if steps else False,
        "step_count": len(steps),
    }
    write_json(dest, payload)
    return payload


def run_self_test() -> int:
    commands = custody_test_commands()
    required = {
        "python plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py",
        "python plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py",
        "python plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py",
    }
    missing = required - set(commands)
    if missing:
        raise AssertionError(f"custody command extraction missed: {missing}")
    if len(commands) < 6:
        raise AssertionError(f"expected full Linux custody suite, got {commands}")
    print(f"v6 candidate evidence collector self-test: ok ({len(commands)} custody commands)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--public-content",
        type=Path,
        help="Write public-content evidence JSON here",
    )
    parser.add_argument(
        "--custody",
        type=Path,
        help="Write custody-suite evidence JSON here",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    if not args.public_content and not args.custody:
        parser.error("provide --self-test, --public-content, and/or --custody")
    # R11c: evidence stamped with HEAD's SHA must describe HEAD's tree. A
    # dirty working tree (outside the packet output directory, which this
    # collector is in the business of writing) makes the stamp a lie — the
    # predecessor's public-content evidence was stamped at one SHA while the
    # scanned tree matched another. Refuse instead.
    status = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True
    )
    dirt = [
        line for line in status.splitlines()
        if line.strip() and "docs/v6/ES6-V6-CANDIDATE/" not in line
    ]
    if dirt:
        print(
            "DIRTY_TREE_REFUSED: evidence must be collected on a clean tree "
            f"({len(dirt)} entries differ from HEAD, e.g. {dirt[0]!r}). Commit "
            "or stash first; stamped-SHA/tree divergence is the R5/R11c class.",
            file=sys.stderr,
        )
        return 2
    sha = git_head()
    failed = False
    if args.public_content:
        payload = collect_public_content(sha, args.public_content)
        print(f"public-content evidence: passed={payload['passed']} -> {args.public_content}")
        failed = failed or not payload["passed"]
    if args.custody:
        payload = collect_custody(sha, args.custody)
        print(f"custody-suite evidence: passed={payload['passed']} steps={payload['step_count']} -> {args.custody}")
        failed = failed or not payload["passed"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
