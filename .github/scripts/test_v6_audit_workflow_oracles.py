#!/usr/bin/env python3
"""Self-test for v6_audit_workflow_oracles.py.

Planted RED controls per rule (a control must fail against a build that
treats absence as success), plus the original does-not-crash report run.
Requires PyYAML, same as the audit itself; the CI step installs it.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT = REPO_ROOT / ".github/scripts/v6_audit_workflow_oracles.py"

SPEC = importlib.util.spec_from_file_location("v6_audit_workflow_oracles", AUDIT)
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD  # dataclass processing resolves cls.__module__
SPEC.loader.exec_module(MOD)


def _write(tmp: Path, name: str, text: str) -> Path:
    path = tmp / name
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    failures = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # RED: whole-tree reader behind a paths: filter must be a finding.
        planted = _write(tmp, "reader-behind-filter.yml", """\
name: planted
"on":
  pull_request:
    paths: ["docs/**"]
jobs:
  gate:
    runs-on: ubuntu-24.04
    steps:
      - name: whole-tree scan
        run: python .github/scripts/check_public_content.py
""")
        findings = MOD.audit_workflow(planted)
        if any(f.kind == "path_filtered_whole_tree_reader" for f in findings):
            print("[PASS] planted whole-tree reader behind paths: filter fails closed")
        else:
            failures += 1
            print(f"[FAIL] reader-behind-filter not flagged: {findings}")

        # GREEN: same reader with no paths: filter must be clean.
        clean = _write(tmp, "reader-no-filter.yml", """\
name: planted
"on":
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
jobs:
  gate:
    runs-on: ubuntu-24.04
    steps:
      - name: whole-tree scan
        run: python .github/scripts/check_public_content.py
""")
        findings = MOD.audit_workflow(clean)
        if not findings:
            print("[PASS] unfiltered whole-tree reader passes")
        else:
            failures += 1
            print(f"[FAIL] unfiltered reader wrongly flagged: {findings}")

        # RED: step input path not covered by the filter must be a finding.
        uncovered = _write(tmp, "uncovered-input.yml", """\
name: planted
"on":
  pull_request:
    paths: ["docs/**"]
jobs:
  gate:
    runs-on: ubuntu-24.04
    steps:
      - name: scoped check
        run: python plugins/epistemic-skills/tests/check_thing.py
""")
        findings = MOD.audit_workflow(uncovered)
        if any(f.kind == "uncovered_pr_path" for f in findings):
            print("[PASS] planted uncovered step input fails closed")
        else:
            failures += 1
            print(f"[FAIL] uncovered input not flagged: {findings}")

    # Live tree: the audit must currently report zero findings (R7 removed the
    # epistemic-flexibility filters; other workflows must stay consistent).
    live = MOD.run_audit()
    if live:
        failures += 1
        print(f"[FAIL] live tree has findings: {[ (f.workflow, f.kind, f.path) for f in live ]}")
    else:
        print("[PASS] live workflow tree is clean")

    # Report mode must run without crashing (original check).
    proc = subprocess.run(
        [sys.executable, str(AUDIT), "--allow-findings"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or "finding_count" not in proc.stdout:
        failures += 1
        print(f"[FAIL] report mode: rc={proc.returncode}\n{proc.stderr}")
    else:
        print("[PASS] report mode emits finding_count and exits 0")

    print(f"v6 workflow oracle audit self-test: {'PASS' if not failures else 'FAIL'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
