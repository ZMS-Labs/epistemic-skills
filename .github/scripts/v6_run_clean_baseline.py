#!/usr/bin/env python3
"""Run clean-room baseline and write ES6-CLEAN-BASELINE evidence JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLEANROOM = REPO_ROOT / ".github/scripts/cleanroom_ci.sh"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref",
        default="HEAD",
        help="Git ref to test (default: HEAD)",
    )
    parser.add_argument(
        "--write",
        type=Path,
        required=True,
        help="Output evidence JSON path",
    )
    parser.add_argument(
        "--program",
        default="ES6-ZI-001",
        help="Program id stamped into the evidence JSON (default: ES6-ZI-001)",
    )
    parser.add_argument(
        "--packet",
        default="ES6-CLEAN-BASELINE",
        help="Packet id stamped into the evidence JSON",
    )
    args = parser.parse_args()

    sha = subprocess.check_output(
        ["git", "rev-parse", args.ref], cwd=REPO_ROOT, text=True
    ).strip()
    proc = subprocess.run(
        ["bash", str(CLEANROOM), sha],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    report = {
        "schema": "clean-baseline@1",
        "program": args.program,
        "packet": args.packet,
        "exact_start_sha": sha,
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "passed": proc.returncode == 0,
    }
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"clean baseline evidence: exit={proc.returncode} -> {args.write}")
    if proc.stdout:
        print(proc.stdout)
    if proc.returncode != 0 and proc.stderr:
        print(proc.stderr, file=__import__("sys").stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
