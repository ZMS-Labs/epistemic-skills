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

    try:
        test_collapsed_lifecycle()
    except AssertionError as e:
        print(f"[FAIL] collapsed lifecycle: {e}")
        failures.append("collapsed-lifecycle")

    rc, out = sh(str(ROOT / "scripts" / "validate_roster.py"))
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] validate_roster: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("validate_roster")

    rc, out = sh(str(ROOT / "scripts" / "select_lenses.py"), "--self-test")
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] selector self-test: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("selector-self-test")

    # run-record machinery: finalize + verify self-tests, and the shipped synthetic
    # example must verify clean (selector output + verdict re-derived, hash chain intact)
    rc, out = sh(str(ROOT / "scripts" / "finalize_run.py"), "--self-test")
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] finalize_run self-test: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("finalize-run-self-test")

    rc, out = sh(str(ROOT / "scripts" / "verify_run.py"), "--self-test")
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] verify_run self-test: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("verify-run-self-test")

    rc, out = sh(str(ROOT / "scripts" / "verify_run.py"), "--run-dir",
                 str(ROOT / "examples" / "example-run"))
    print(f"[{'PASS' if rc == 0 else 'FAIL'}] example run verifies: {out.splitlines()[-1] if out else ''}")
    if rc != 0:
        failures.append("example-run-verification")

    try:
        test_shipped_example_ledger_line()
    except AssertionError as e:
        print(f"[FAIL] shipped example ledger line: {e}")
        failures.append("example-ledger-line")

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
         {"subject": "cloud sovereignty tradeoff for homelab services", "axis": "open", "depth": "max",
          "domains": ["cloud", "sovereignty", "self-hosting", "infra"], "risk_classes": []},
         lambda r: sum(1 for e in r["selection"]["evaluators"]
                       if e["id"] in ("cloud-native-purist", "local-first-survivalist")) <= 1),
        ("retired ids never selected",
         {"subject": "first principles constraint relaxation premortem epistemics", "axis": "open", "depth": "max",
          "domains": ["strategy", "constraints", "assumptions"], "risk_classes": []},
         lambda r: not {e["id"] for e in r["selection"]["evaluators"]} &
                   {"first-principles-engineer", "constraint-relaxer", "constraint-inverter",
                    "meta-epistemic-auditor", "premortem-facilitator"}),
        ("former candidates are available to the ordinary evaluator pool",
         {"subject": "backup restore drill RPO RTO integrity", "axis": "fixed", "depth": "deep",
          "domains": ["backups", "restore", "dr"], "risk_classes": [], "domain_confidence": "high"},
         lambda r: all(e["status"] == "available" for e in r["selection"]["evaluators"])),
        ("replay record carries registry hash + scores + exclusions",
         {"subject": "x", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: len(r["replay"]["registry_sha256"]) == 64 and r["replay"]["scores"] and r["replay"]["exclusions"]),
        ("standard panel records exactly one subject-seeded wildcard",
         {"subject": "payment ledger cutover", "subject_sha256": "1" * 64,
          "axis": "fixed", "depth": "standard", "domains": ["infra"], "risk_classes": ["irreversible"]},
         lambda r: len(r["selection"]["wildcards"]) == 1
                   and r["selection"]["wildcards"][0] in {s["id"] for s in r["selection"]["evaluators"]}
                   and "exploration" not in r["selection"]),
        ("quick panel has no wildcard seat",
         {"subject": "x", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: r["selection"]["wildcards"] == []),
        ("max panel records exactly two subject-seeded wildcards",
         {"subject": "x", "subject_sha256": "2" * 64,
          "axis": "fixed", "depth": "max", "domains": ["infra"], "risk_classes": []},
         lambda r: len(r["selection"]["wildcards"]) == 2),
        ("retired verification-oracle-auditor never seated anywhere",
         {"subject": "mocked test oracle verification adequacy", "axis": "fixed", "depth": "max",
          "domains": ["data-ml", "product"], "risk_classes": []},
         lambda r: "verification-oracle-auditor" not in {s["id"] for s in r["selection"]["evaluators"]}),
        # Fit-sensitive alias fixtures (audit 08 Part 2c failure cases): these assert a
        # seating DIRECTION the aliased vocabulary produces — the constraint battery
        # cannot validate fit, so both must fail if DOMAIN_ALIASES is reverted.
        ("domain aliases: $120k spend decision seats an economics lens",
         {"subject": "approve a $120k/year reserved capacity commitment", "axis": "fixed",
          "depth": "standard", "domains": ["finance", "spend"], "risk_classes": ["spend"],
          "domain_confidence": "high"},
         lambda r: any(e["capability"] == "economics" for e in r["selection"]["evaluators"])),
        ("domain aliases: UX change seats wcag-accessibility-expert",
         {"subject": "redesign account settings page for screen-reader users", "axis": "fixed",
          "depth": "standard", "domains": ["ux"], "risk_classes": [],
          "domain_confidence": "high"},
         lambda r: "wcag-accessibility-expert" in {s["id"] for s in r["selection"]["evaluators"]}),
        ("domain aliases canonicalize both sides of the match",
         {"subject": "x", "axis": "fixed", "depth": "quick", "domains": ["infra"], "risk_classes": []},
         lambda r: sel.canon_domains(["finance", "cost", "spend"]) == {"economics"}
                   and sel.canon_domains(["ux", "wcag", "inclusive-design"]) == {"ux-accessibility"}
                   and sel.canon_domains(["infra", "operations", "ops"]) == {"infra-ops"}
                   and sel.canon_domains(["unmapped-term"]) == {"unmapped-term"}),
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
        test_subject_seeded_wildcards(sel)
    except AssertionError as e:
        print(f"[FAIL] subject-seeded wildcards: {e}")
        failures.append("subject-seeded-wildcards")

    try:
        test_arbitrator_seat_provenance_neutrality()
    except AssertionError as e:
        print(f"[FAIL] arbitrator seat-provenance neutrality: {e}")
        failures.append("arbitrator-seat-provenance")

    try:
        test_consult_packet()
    except AssertionError as e:
        print(f"[FAIL] consult_packet: {e}")
        failures.append("consult_packet")

    try:
        test_verify_evidence_fails_closed_on_binary()
    except AssertionError as e:
        print(f"[FAIL] verify_evidence fail-closed: {e}")
        failures.append("verify_evidence-fail-closed")

    try:
        test_materialized_role_binding()
    except AssertionError as e:
        print(f"[FAIL] materialized role binding: {e}")
        failures.append("materialized-role-binding")

    try:
        test_role_frontmatter_is_cross_runtime_portable()
    except AssertionError as e:
        print(f"[FAIL] role frontmatter portability: {e}")
        failures.append("role-frontmatter-portability")

    try:
        test_codex_agent_renderer()
    except AssertionError as e:
        print(f"[FAIL] Codex agent renderer: {e}")
        failures.append("codex-agent-renderer")

    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
    return 0 if not failures else 1


def test_collapsed_lifecycle():
    registry = json.loads((ROOT / "roster" / "registry.json").read_text(encoding="utf-8"))
    statuses = {entry["status"] for entry in registry["entries"]}
    assert statuses <= {"available", "retired"}, statuses
    assert statuses == {"available", "retired"}, statuses
    schema = json.loads((ROOT / "roster" / "lens.schema.json").read_text(encoding="utf-8"))
    assert set(schema["properties"]["status"]["enum"]) == {"available", "retired"}
    arbitrator = (ROOT / "bases" / "base-arbitrator.md").read_text(encoding="utf-8")
    assert "Seat provenance and historical telemetry carry zero evidentiary weight" in arbitrator
    print("[PASS] roster lifecycle is available -> retired")



def test_shipped_example_ledger_line():
    """runs/ledger.jsonl ships exactly one line: the example projection, marked
    example:true, schema ledger@2, ineligible, family-granular models only."""
    ledger = ROOT / "runs" / "ledger.jsonl"
    lines = [l for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == 1, f"expected exactly the example line, found {len(lines)}"
    rec = json.loads(lines[0])
    assert rec.get("schema") == "ledger@2", rec.get("schema")
    assert rec.get("example") is True and rec.get("eligible") is False
    assert rec.get("run_dir") and rec.get("dossier_sha256") and rec.get("docket_mode")
    assert rec.get("independence_mode")
    assert all(lens.get("model") for lens in rec["lenses"]), "per-lens model family required"
    # cross-check: the line is the finalize_run.py projection of the example run record
    import importlib.util
    spec = importlib.util.spec_from_file_location("fin", ROOT / "scripts" / "finalize_run.py")
    fin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fin)
    record = json.loads((ROOT / "examples" / "example-run" / "run-record.json").read_text(encoding="utf-8"))
    derived = fin.build_ledger_line(record, ROOT / "examples" / "example-run",
                                    fin.load_registry_entries(), example=True)
    assert json.loads(json.dumps(derived, sort_keys=True)) == json.loads(lines[0]), \
        "ledger line is not the finalize_run.py derivation of the example run record"
    print("[PASS] shipped example ledger line is the derived projection")


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
    """lens_stats is non-governing telemetry and emits no lifecycle decision flags."""
    import json as _json, subprocess, sys as _sys, tempfile, os
    recs = []
    for i in range(20):
        recs.append({"ts": f"t{i}", "subject": "s", "depth": "deep", "verdict": "NO-GO",
                     "eligible": True, "lenses": [
            {"id": "wildcard-lens", "lifecycle": "available", "upheld_unique": 1, "upheld_dup": 0},
            {"id": "dup-lens", "lifecycle": "available", "upheld_unique": 0, "upheld_dup": 3,
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
        assert data["lenses"]["dup-lens"]["dup_rate"] == 1.0
        assert "flags" not in data["lenses"]["dup-lens"]
        assert "flags" not in data["lenses"]["wildcard-lens"]
    finally:
        os.unlink(path)
    print("[PASS] lens_stats aggregation is non-governing telemetry")


def test_subject_seeded_wildcards(sel):
    base = {"subject": "same dossier", "axis": "fixed", "depth": "standard",
            "domains": ["infra"], "risk_classes": []}
    first = sel.run(dict(base, subject_sha256="a" * 64))
    repeat = sel.run(dict(base, subject_sha256="a" * 64))
    changed = sel.run(dict(base, subject_sha256="b" * 64))
    assert first["replay"]["wildcard_ids"] == repeat["replay"]["wildcard_ids"]
    assert first["replay"]["subject_seed_sha256"] == "a" * 64
    assert first["replay"]["seed_source"] == "subject_sha256"
    assert first["replay"]["wildcard_rank_sha256"] != changed["replay"]["wildcard_rank_sha256"]
    assert "ledger" not in json.dumps(first["replay"]).lower()
    print("[PASS] subject-seeded wildcard replay is deterministic and ledger-independent")


def test_arbitrator_seat_provenance_neutrality():
    import importlib.util
    path = ROOT / "evals" / "arbitrator-certification" / "score.py"
    spec = importlib.util.spec_from_file_location("arbitrator_score", path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    gt = {"expected_verdict": "NO-GO", "flawed_finding_id": "F-wildcard"}
    correct = {"verdict": "NO-GO", "dispositions": [{"finding_id": "F-wildcard", "disposition": "upheld"}]}
    prejudiced = {"verdict": "GO", "dispositions": [{"finding_id": "F-wildcard", "disposition": "excluded"}]}
    assert scorer.score_case("AC-07-seat-provenance-prejudice", gt, correct)[0]
    assert not scorer.score_case("AC-07-seat-provenance-prejudice", gt, prejudiced)[0]
    print("[PASS] arbitrator certification rejects seat-provenance prejudice")


def test_verify_evidence_fails_closed_on_binary():
    """F13 regression (gauntlet-plugin-publish-2026-07-17).

    A [V path:line] tag citing a BINARY file must downgrade to [H]: a line-oriented
    oracle cannot observe binary content, and before this guard the verifier counted
    newlines in a .pyc and certified the tag 100% verified. An oracle that cannot fail
    is not evidence. Also asserts the positive control -- a real text citation still
    verifies -- so the guard cannot pass by rejecting everything.
    """
    import py_compile
    import tempfile
    sys.path.insert(0, str(ROOT / "scripts"))
    import verify_evidence

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        blob = root / "blob.pyc"
        py_compile.compile(str(ROOT / "scripts" / "select_lenses.py"), cfile=str(blob))
        text = root / "real.md"
        text.write_text("line one\nline two\n", encoding="utf-8")

        binary_tag = verify_evidence.verify_tag("blob.pyc", 5, root)
        assert binary_tag.status == "H", f"binary [V] must fail closed, got {binary_tag.status}"
        assert "Binary" in binary_tag.reason, f"reason must name the cause, got {binary_tag.reason!r}"

        # positive control: the guard must not have broken ordinary verification
        text_tag = verify_evidence.verify_tag("real.md", 1, root)
        assert text_tag.status == "V", f"text [V] must still verify, got {text_tag.status}"

        missing = verify_evidence.verify_tag("nope.md", 1, root)
        assert missing.status == "H"
    print("[PASS] verify_evidence fails closed on binary [V] tags (F13 regression)")


def test_materialized_role_binding():
    """A runtime without native custom-agent registration keeps the exact role contract.

    This is the portability regression: Codex packaged the role files but did not
    register them as collaboration agent types. The fallback must materialize the
    canonical role definition and selected persona into a deterministic prompt,
    reject unresolved placeholders, and record hashes for replay.
    """
    import hashlib
    import json as _json
    import subprocess
    import tempfile

    script = ROOT / "scripts" / "materialize_role.py"
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        persona = tmp / "persona.md"
        dossier = tmp / "dossier.md"
        output = tmp / "binding.json"
        persona.write_text("Audit the publication boundary and name falsifiers.\n", encoding="utf-8")
        dossier.write_text("# Frozen dossier\nOnly verified facts may be used.\n", encoding="utf-8")

        result = subprocess.run(
            [PY, str(script), "--role", "gauntlet-adversary", "--persona", str(persona),
             "--dossier", str(dossier), "--out", str(output)],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        record = _json.loads(output.read_text(encoding="utf-8"))
        prompt = record["prompt"]
        assert "{{PERSONA_SPEC}}" not in prompt
        assert persona.read_text(encoding="utf-8").strip() in prompt
        assert dossier.read_text(encoding="utf-8").strip() in prompt
        assert "Falsifier contract" in prompt or "falsifier contract" in prompt
        assert record["binding_mode"] == "materialized-role"
        assert record["role"] == "gauntlet-adversary"
        assert record["role_sha256"] == hashlib.sha256(
            record["role_source"].encode("utf-8")
        ).hexdigest()
        assert len(record["persona_sha256"]) == 64
        assert len(record["dossier_sha256"]) == 64

        bad = subprocess.run(
            [PY, str(script), "--role", "not-a-role", "--persona", str(persona),
             "--dossier", str(dossier), "--out", str(output)],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert bad.returncode != 0
    print("[PASS] materialized role binding preserves exact contract + replay hashes")


def test_role_frontmatter_is_cross_runtime_portable():
    """Shared role files must not pin vendor-specific models or tool identifiers."""
    agents_root = ROOT.parent.parent / "agents"
    role_files = sorted(agents_root.glob("gauntlet-*.md"))
    assert len(role_files) == 5, f"expected five canonical roles, found {len(role_files)}"
    for role_file in role_files:
        text = role_file.read_text(encoding="utf-8")
        assert text.startswith("---\n"), f"missing frontmatter: {role_file.name}"
        frontmatter = text.split("---", 2)[1]
        assert "\nmodel:" not in frontmatter, f"vendor-specific model pin in {role_file.name}"
        assert "\ntools:" not in frontmatter, f"vendor-specific tool names in {role_file.name}"
        assert "\nname:" in frontmatter and "\ndescription:" in frontmatter
    print("[PASS] shared role frontmatter is portable across Claude/Cursor/Gemini")


def test_codex_agent_renderer():
    """Codex's user-agent registry receives all five canonical Markdown roles."""
    import subprocess
    import tempfile
    import tomllib

    script = ROOT / "scripts" / "render_codex_agents.py"
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "agents"
        result = subprocess.run(
            [PY, str(script), "--out", str(out)],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        rendered = sorted(out.glob("gauntlet-*.toml"))
        assert len(rendered) == 5, f"expected five Codex agents, found {len(rendered)}"
        adversary = tomllib.loads((out / "gauntlet-adversary.toml").read_text(encoding="utf-8"))
        assert adversary["name"] == "gauntlet-adversary"
        assert "hostile scrutiny" in adversary["description"]
        assert "Falsifier contract" in adversary["developer_instructions"]
        assert "tools:" not in adversary["developer_instructions"]
    print("[PASS] Codex renderer registers all five canonical roles")


if __name__ == "__main__":
    raise SystemExit(main())
