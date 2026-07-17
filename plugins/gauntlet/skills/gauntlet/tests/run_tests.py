#!/usr/bin/env python3
"""Gauntlet roster/selector test runner. Stdlib only. Exit 0 = all pass.

Layers:
  1. validate_roster.py        — schema, roles, collisions, freshness (mechanical)
  2. select_lenses.py --self-test — 1000 deterministic constraint fixtures
  3. targeted regression cases below — must-include / must-exclude behavior

NOT covered here (honest gap): the behavioral admission battery (paired blind
lens-vs-neighbor evaluation on real dossiers) — see evals/README.md.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def sh(*args):
    r = subprocess.run([PY, *args], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    failures = []

    rc, out = sh(str(ROOT / "scripts" / "validate_roster.py"))
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] validate_roster: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("validate_roster")

    rc, out = sh(str(ROOT / "scripts" / "select_lenses.py"), "--self-test")
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] selector self-test: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("selector-self-test")

    # targeted regressions
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("sel", ROOT / "scripts" / "select_lenses.py")
    sel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sel)

    cases = [
        ("security subject seats a security evaluator",
         {"subject": "internet-exposed admin panel with default credentials on new service", "axis": "fixed",
          "depth": "standard", "domains": ["security", "internet-exposure"], "risk_classes": ["security"],
          "domain_confidence": "high"},
         lambda r: any(e["capability"] == "security" for e in r["selection"]["evaluators"])),
        ("open question gets generators incl. null option",
         {"subject": "should we migrate to k8s operators", "axis": "open", "depth": "standard",
          "domains": ["strategy", "infra"], "risk_classes": []},
         lambda r: "null-hypothesis-advocate" in r["selection"]["generators"]),
        ("fixed artifact gets NO generators",
         {"subject": "review this firewall change", "axis": "fixed", "depth": "quick",
          "domains": ["infra"], "risk_classes": ["irreversible"]},
         lambda r: r["selection"]["generators"] == []),
        ("irreversible risk attaches red-lines gate",
         {"subject": "wipe and rebuild the pool", "axis": "fixed", "depth": "standard",
          "domains": ["infra"], "risk_classes": ["irreversible"]},
         lambda r: "red-lines-arbitrator" in r["selection"]["gates"]),
        ("defensible priors flips judge to bayesian",
         {"subject": "which cache eviction wins on measured hit rates", "axis": "open", "depth": "standard",
          "domains": ["performance"], "risk_classes": [], "defensible_priors": True},
         lambda r: r["selection"]["judge"] == "bayesian-adjudicator"),
        ("default judge is pragmatic-judge",
         {"subject": "anything", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: r["selection"]["judge"] == "pragmatic-judge"),
        ("mutex pair never co-selected without contrast",
         {"subject": "cloud sovereignty tradeoff for self-hosted services", "axis": "open", "depth": "max",
          "domains": ["cloud", "sovereignty", "self-hosting", "infra"], "risk_classes": []},
         lambda r: sum(1 for e in r["selection"]["evaluators"]
                       if e["id"] in ("cloud-native-purist", "local-first-survivalist")) <= 1),
        ("retired ids never selected",
         {"subject": "first principles constraint relaxation premortem epistemics", "axis": "open", "depth": "max",
          "domains": ["strategy", "constraints", "assumptions"], "risk_classes": []},
         lambda r: not {e["id"] for e in r["selection"]["evaluators"]} &
                   {"first-principles-engineer", "constraint-relaxer", "constraint-inverter",
                    "meta-epistemic-auditor", "premortem-facilitator"}),
        ("candidates never seated even on their home domain",
         {"subject": "backup restore drill RPO RTO integrity", "axis": "fixed", "depth": "deep",
          "domains": ["backups", "restore", "dr"], "risk_classes": [], "domain_confidence": "high"},
         lambda r: all(e["status"] != "candidate" for e in r["selection"]["evaluators"])),
        ("replay record carries registry hash + scores + exclusions",
         {"subject": "x", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: len(r["replay"]["registry_sha256"]) == 64 and r["replay"]["scores"] and r["replay"]["exclusions"]),
        ("exploration seat auto-seats a probation lens at standard depth",
         {"subject": "payment ledger cutover", "axis": "fixed", "depth": "standard", "domains": ["infra"], "risk_classes": ["irreversible"]},
         lambda r: r["selection"]["exploration"] is not None
                   and r["selection"]["exploration"]["status"] == "probation"
                   and r["selection"]["exploration"]["id"] not in {s["id"] for s in r["selection"]["evaluators"]}
                   and all(s["status"] == "active" for s in r["selection"]["evaluators"])),
        ("exploration seat absent at quick depth",
         {"subject": "x", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: r["selection"]["exploration"] is None),
        ("exploration seat honors explicit opt-out",
         {"subject": "x", "axis": "fixed", "depth": "deep", "domains": ["infra"], "risk_classes": [],
          "allow_probation_seat": False},
         lambda r: r["selection"]["exploration"] is None),
        ("retired verification-oracle-auditor never seated anywhere",
         {"subject": "mocked test oracle verification adequacy", "axis": "fixed", "depth": "max",
          "domains": ["data-ml", "product"], "risk_classes": []},
         lambda r: "verification-oracle-auditor" not in {s["id"] for s in r["selection"]["evaluators"]}
                   and (r["selection"]["exploration"] or {}).get("id") != "verification-oracle-auditor"),
    ]
    for name, subj, check in cases:
        r = sel.run(subj)
        ok = check(r) and not r["constraint_violations"]
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            failures.append(name)

    try:
        test_lens_stats_aggregation()
    except AssertionError as e:
        print(f"[FAIL] lens_stats aggregation: {e}")
        failures.append("lens_stats")

    try:
        test_consult_packet()
    except AssertionError as e:
        print(f"[FAIL] consult_packet: {e}")
        failures.append("consult_packet")

    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
    return 0 if not failures else 1



def test_consult_packet():
    """Step 7b helper: packet builds, secret-screen blocks, dissent escalates + validates."""
    import json as _json, subprocess, sys as _sys, tempfile, os
    script = str(ROOT / "scripts" / "consult_packet.py")

    def write_tmp(obj):
        fd, p = tempfile.mkstemp(suffix=".json"); os.close(fd)
        with open(p, "w", encoding="utf-8") as f:
            f.write(_json.dumps(obj))
        return p

    def sh(*a):
        return subprocess.run([_sys.executable, script, *a], capture_output=True, text=True)

    clean = {"subject": "s", "verdict": "CONDITIONAL", "decisive_tensions": ["t1"], "dossier_text": "d"}
    p = write_tmp(clean)
    try:
        out = sh("build", "--input", p)
        assert out.returncode == 0 and "GAUNTLET-CONSULT" in out.stdout, out.stderr
    finally:
        os.unlink(p)

    # fake AWS-shaped token assembled from fragments so the SOURCE has no contiguous
    # key literal (keeps gitleaks/CodeQL quiet) while the runtime value still trips the regex
    fake_key = "AK" + "IA" + "1234567890" + "ABCD00"
    p = write_tmp(dict(clean, dossier_text=f"key {fake_key} here"))
    try:
        out = sh("build", "--input", p)
        assert out.returncode == 3 and "secret-screen" in out.stderr.lower(), "secret-screen must block"
    finally:
        os.unlink(p)

    fd, ledger = tempfile.mkstemp(suffix=".jsonl"); os.close(fd)
    p1 = write_tmp({"reading": "DISSENT", "strongest_reason_verdict_wrong": "r", "confidence": "low"})
    p2 = write_tmp({"reading": "DISSENT", "confidence": "low"})
    try:
        out = sh("record", "--run", "t1", "--ledger", ledger, "--response", p1)
        assert out.returncode == 0 and "ESCALATE-TO-SOVEREIGN" in out.stdout, out.stderr
        rec = _json.loads(open(ledger, encoding="utf-8").read().strip())
        assert rec["disposition"] == "ESCALATE-TO-SOVEREIGN"
        out = sh("record", "--run", "t2", "--ledger", ledger, "--response", p2)
        assert out.returncode == 2, "DISSENT without reason must fail"
    finally:
        os.unlink(ledger); os.unlink(p1); os.unlink(p2)
    print("[PASS] consult_packet build/secret-screen/record/validation")


def test_lens_stats_aggregation():
    """lens_stats aggregates the ledger and fires the lifecycle threshold flags."""
    import json as _json, subprocess, sys as _sys, tempfile, os
    recs = []
    # probation lens seated in 20 eligible runs -> ACTIVATION-REVIEW-DUE
    for i in range(20):
        recs.append({"ts": f"t{i}", "subject": "s", "depth": "deep", "verdict": "NO-GO",
                     "eligible": True, "lenses": [
            {"id": "prob-lens", "lifecycle": "probation", "upheld_unique": 1, "upheld_dup": 0},
            {"id": "dup-lens", "lifecycle": "active", "upheld_unique": 0, "upheld_dup": 3,
             "false_high": 1 if i == 0 else 0},
        ]})
    fd, path = tempfile.mkstemp(suffix=".jsonl"); os.close(fd)
    try:
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(_json.dumps(r) + "\n")
        out = subprocess.run([_sys.executable, str(ROOT / "scripts" / "lens_stats.py"),
                              "--ledger", path, "--json"], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        data = _json.loads(out.stdout)
        assert data["runs"] == 20
        assert "ACTIVATION-REVIEW-DUE" in data["lenses"]["prob-lens"]["flags"]
        assert "DEPRECATE-MERGE-CANDIDATE" in data["lenses"]["dup-lens"]["flags"]
        assert data["lenses"]["dup-lens"]["dup_rate"] == 1.0
        assert any(fl.startswith("FALSE-HIGH") for fl in data["lenses"]["dup-lens"]["flags"])
        assert data["lenses"]["prob-lens"]["flags"] == ["ACTIVATION-REVIEW-DUE"]
    finally:
        os.unlink(path)
    print("[PASS] lens_stats aggregation + lifecycle threshold flags")

if __name__ == "__main__":
    raise SystemExit(main())
