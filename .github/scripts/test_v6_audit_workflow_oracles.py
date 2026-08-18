#!/usr/bin/env python3
"""Self-test for v6_audit_workflow_oracles.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT = REPO_ROOT / ".github/scripts/v6_audit_workflow_oracles.py"


def main() -> int:
    # Report mode must run without crashing.
    proc = subprocess.run(
        [sys.executable, str(AUDIT), "--allow-findings"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    if "finding_count" not in proc.stdout:
        raise AssertionError("audit output missing finding_count")
    print("v6 workflow oracle audit self-test: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
