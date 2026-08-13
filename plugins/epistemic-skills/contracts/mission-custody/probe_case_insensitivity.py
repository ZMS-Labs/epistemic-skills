#!/usr/bin/env python3
"""es#162 probe: does the scope comparison agree with THIS filesystem about
case?

Custody folds case only under os.name == 'nt' (`_ascii_case_fold` via
`_fold`), so the comparison assumes every non-NT filesystem is
case-sensitive. macOS's default APFS is not. The round-2 disposition ruled
this UNDECIDABLE from a Linux host -- "one macOS CI run settles it" -- and
this probe is that run's instrument.

DIAGNOSTIC, NOT A GATE. It prints a labelled verdict block and exits 0 on
any measured outcome (including CONFIRMED): es#162 is a filed, open issue,
and a diagnostic that fails CI would block merges on a defect the estate has
already recorded. Nonzero exit means the probe itself broke, nothing else.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_mission import Mission, _same_artifact  # noqa: E402


def main() -> int:
    print(f"host: os.name={os.name!r} platform={sys.platform!r}")

    # Half 1: what does the FILESYSTEM say about a case-differing pair?
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        (ws / "Case.txt").write_text("x", encoding="utf-8")
        fs_folds = (ws / "case.txt").exists()
    print(f"filesystem-folds-case: {fs_folds}")

    # Half 2: what does the COMPARISON say about the same pair?
    comparison_folds = _same_artifact("Case.txt", "case.txt")
    print(f"comparison-folds-case: {comparison_folds}")

    if fs_folds == comparison_folds:
        print("VERDICT: comparison AGREES with this filesystem -- "
              "es#162 not exercisable / refuted on this host")
        return 0

    # The halves disagree. Demonstrate the consequence end-to-end: a
    # respelled write dodging a declared exclusion.
    with tempfile.TemporaryDirectory() as td:
        ws = Path(td)
        m = Mission.open(
            ws, mission_id="probe-es162", instruction="case probe",
            operator_ref="operator:probe", steward_ref="agent:probe",
            required_tier="declared-role-separation", actor="agent:probe",
            scope_out=["secrets.env"])
        m.approve()
        m.record_effect("SECRETS.env", "leak", "probe-1")
        same_file = (ws / "secrets.env").exists()
        findings = [(f["artifact_path"], f["reason"])
                    for f in m.scope_consistency()]
    print(f"fs-says-SECRETS.env-is-secrets.env: {same_file}")
    print(f"scope-consistency-findings: {findings}")

    if same_file and not findings:
        print("VERDICT: CONFIRMED -- this filesystem folds case, the "
              "comparison does not, and a respelled write dodges the "
              "declared exclusion (es#162). Evidence above.")
    elif not same_file:
        print("VERDICT: INCONCLUSIVE -- the pair probe and the mission "
              "probe disagree about this filesystem; read the evidence "
              "above before concluding anything")
    else:
        print("VERDICT: comparison caught the respelled write -- "
              "es#162 refuted on this host despite the pair disagreement; "
              "read the evidence above")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
