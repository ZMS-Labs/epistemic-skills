#!/usr/bin/env python3
"""verify_run.py — mechanical post-run re-check of a gauntlet run against its record.

Stdlib only. Given a run directory + its gauntlet-run-record@1 (run-record.json,
produced by finalize_run.py), re-checks — independently, all legs reported:

  1. HASH CHAIN — recompute sha256 of every artifact the record binds (dossier,
     selection, per-lens reports, fingerprint, arbitration/ruling-set, summary,
     role-binding ref) and compare. Any edit after finalize is detected:
     HASH-MISMATCH:<path>.
  2. EVIDENCE-ROOT PIN — recompute the evidence-root tree hash; a mismatch means
     the run's [V path:line] verifications are no longer bound to what was verified:
     EVIDENCE-ROOT-DRIFT.
  3. SELECTOR REPLAY — re-run scripts/select_lenses.py against the subject vector in
     prompts/selection.json and diff the full output against the recorded selection.
     CAVEAT (non-hermetic replay): the replay runs against the CURRENT registry, so a
     mutated registry makes the re-derivation diverge for legitimate reasons. The
     recorded replay's registry_sha256 is checked FIRST; on divergence the verdict is
     REGISTRY-DRIFT (exit 3) — an explicit named outcome, never a silent pass/fail.
     Wildcard seats are deterministic from the frozen subject seed and registry; run
     telemetry is never an input.
  4. VERDICT GATE — re-derive GO/CONDITIONAL/NO-GO from the ruling-set@1 P1/P2 status
     fields (P1 open => NO-GO; else P2 open => CONDITIONAL; else GO) and compare to
     both the ruling-set's computed_verdict and the record's verdict: VERDICT-MISMATCH.

This converts "computed verdict" and "replayable selection" from doctrine to check.
What it NEVER certifies: verdict-truth, lens independence, freshness beyond the
record's valid_while coordinates (see runs/README.md — the never-attest list).

Usage:
  python verify_run.py --run-dir <dir> [--record <path>]
  python verify_run.py --self-test

Exit codes: 0 all legs pass · 1 a check failed (named reason) · 2 invalid invocation ·
3 REGISTRY-DRIFT (registry mutated since the run; re-run the selector or pin the registry)
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_RUN = ROOT / "examples" / "example-run"

RECORD_KIND = "gauntlet-run-record@1"
FENCED_JSON_RE = re.compile(r"```json\s*(.*?)```", re.S)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(root: Path) -> str:
    root = Path(root)
    if not root.is_dir():
        return "MISSING:" + str(root)
    h = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(f.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(hashlib.sha256(f.read_bytes()).hexdigest().encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def extract_ruling_set(text: str) -> dict | None:
    for block in FENCED_JSON_RE.findall(text):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("ruling_set") == "ruling-set@1":
            return obj
    return None


def derive_verdict(rulings: list) -> str:
    def open_at(priority):
        return any(r.get("priority") == priority and r.get("status") == "open"
                   for r in rulings)
    if open_at("P1"):
        return "NO-GO"
    if open_at("P2"):
        return "CONDITIONAL"
    return "GO"


def load_selector():
    spec = importlib.util.spec_from_file_location("select_lenses", ROOT / "scripts" / "select_lenses.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Leg:
    def __init__(self, name):
        self.name, self.failures, self.drift = name, [], False


def verify_run(run_dir: Path, record_path: Path | None = None) -> tuple[list, bool]:
    """Returns (legs, registry_drift). Each leg carries named failures."""
    run_dir = Path(run_dir)
    record_path = Path(record_path) if record_path else run_dir / "run-record.json"
    legs = [Leg(n) for n in ("hash-chain", "evidence-root", "selector-replay", "verdict-gate")]
    chain, pin_leg, replay_leg, gate_leg = legs
    drift = False

    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("run_record") != RECORD_KIND:
        chain.failures.append(f"RECORD-KIND: expected {RECORD_KIND}, got {record.get('run_record')!r}")
        return legs, drift

    # Leg 1 — hash chain over every bound artifact
    bound = [record["dossier"], record["selection"], record["ruling_set"], record["summary"]]
    bound += record.get("reports", [])
    if record.get("fingerprint"):
        bound.append(record["fingerprint"])
    if (record.get("role_binding") or {}).get("ref"):
        bound.append(record["role_binding"]["ref"])
    for art in bound:
        path, want = run_dir / art["path"], art.get("sha256") or art.get("replay_sha256")
        if not path.is_file():
            chain.failures.append(f"ARTIFACT-MISSING:{art['path']}")
            continue
        got = sha256_file(path)
        if got != want:
            chain.failures.append(f"HASH-MISMATCH:{art['path']} "
                                  f"(record {want[:12]}… != file {got[:12]}… — edited after finalize)")

    # Leg 2 — evidence-root pin
    er = record["evidence_root"]
    got = tree_sha256(run_dir / er["path"])
    if got != er["content_sha256"]:
        pin_leg.failures.append(f"EVIDENCE-ROOT-DRIFT: record {er['content_sha256'][:12]}… "
                                f"!= live {got[:12]}… — [V path:line] verifications invalidated")

    # Leg 3 — selector replay (non-hermetic: registry checked first, drift is explicit)
    selection_path = run_dir / record["selection"]["path"]
    recorded_selection = json.loads(selection_path.read_text(encoding="utf-8"))
    replay = recorded_selection.get("replay") or {}
    sel = load_selector()
    _, current_reg_sha = sel.load_registry()
    if current_reg_sha != replay.get("registry_sha256"):
        drift = True
        replay_leg.drift = True
        replay_leg.failures.append(f"REGISTRY-DRIFT: run used registry {str(replay.get('registry_sha256'))[:12]}… "
                                   f"but current is {current_reg_sha[:12]}… — replay is non-hermetic "
                                   "against a mutated registry; re-run the selector or restore the pinned registry")
    else:
        rerun = sel.run(replay.get("subject_vector", {}))
        # JSON-normalize the re-run (the in-memory exclusions are tuples; the recorded
        # file is a JSON round-trip) so the comparison is content, not container type.
        rerun = json.loads(json.dumps(rerun, sort_keys=True))
        if rerun != recorded_selection:
            diffs = []
            if rerun["replay"]["selected_ids"] != replay.get("selected_ids"):
                diffs.append("panel")
            if rerun["replay"]["wildcard_ids"] != replay.get("wildcard_ids"):
                diffs.append("subject-seeded-wildcards")
            if rerun["replay"]["scores"] != replay.get("scores"):
                diffs.append("scores")
            if rerun.get("constraint_violations"):
                diffs.append(f"constraints {rerun['constraint_violations']}")
            replay_leg.failures.append("SELECTOR-MISMATCH: re-derivation diverges from the "
                                       f"recorded selection ({'; '.join(diffs) or 'record shape'})")

    # Leg 4 — verdict gate from ruling-set@1 P1/P2 fields
    arb_path = run_dir / record["ruling_set"]["path"]
    ruling_set = extract_ruling_set(arb_path.read_text(encoding="utf-8")) if arb_path.is_file() else None
    if ruling_set is None:
        gate_leg.failures.append("RULING-SET-MISSING: no fenced ruling-set@1 JSON in arbitration.md")
    else:
        derived = derive_verdict(ruling_set.get("rulings", []))
        if derived != ruling_set.get("computed_verdict"):
            gate_leg.failures.append(f"VERDICT-MISMATCH: gate derives {derived} but ruling-set "
                                     f"records {ruling_set.get('computed_verdict')!r}")
        if derived != record.get("verdict"):
            gate_leg.failures.append(f"VERDICT-MISMATCH: gate derives {derived} but run record "
                                     f"records {record.get('verdict')!r}")
    return legs, drift


def report(legs) -> int:
    worst = 0
    for leg in legs:
        if not leg.failures:
            print(f"[PASS] {leg.name}")
            continue
        for f in leg.failures:
            print(f"[FAIL] {leg.name}: {f}")
        worst = max(worst, 3 if leg.drift else 1)
    return worst


def self_test() -> int:
    """Positive control: the shipped synthetic example verifies clean. Negative controls
    (each on a tampered temp copy): an edited report => HASH-MISMATCH; a flipped
    ruling-set verdict => VERDICT-MISMATCH; a forged registry sha => REGISTRY-DRIFT."""
    fails = 0
    legs, drift = verify_run(EXAMPLE_RUN)
    if any(l.failures for l in legs) or drift:
        fails += 1
        print("self-test: FAIL — shipped example did not verify clean:", file=sys.stderr)
        report(legs)

    def tamper(mutate):
        td = tempfile.mkdtemp()
        run = Path(td) / "run"
        shutil.copytree(EXAMPLE_RUN, run)
        mutate(run)
        lgs, dft = verify_run(run)
        shutil.rmtree(td, ignore_errors=True)
        return [f for l in lgs for f in l.failures], dft

    fs, _ = tamper(lambda r: (r / "reports" / "integration-weaver.md")
                   .write_text("tampered\n", encoding="utf-8"))
    if not any("HASH-MISMATCH" in f for f in fs):
        fails += 1
        print(f"self-test: FAIL — edited report not caught: {fs}", file=sys.stderr)

    def flip_verdict(r):
        arb = r / "arbitration.md"
        arb.write_text(arb.read_text(encoding="utf-8").replace(
            '"computed_verdict": "CONDITIONAL"', '"computed_verdict": "GO"'), encoding="utf-8")
    fs, _ = tamper(flip_verdict)
    if not any("VERDICT-MISMATCH" in f for f in fs):
        fails += 1
        print(f"self-test: FAIL — flipped verdict not caught: {fs}", file=sys.stderr)

    def forge_registry(r):
        sp = r / "prompts" / "selection.json"
        sp.write_text(sp.read_text(encoding="utf-8").replace(
            json.loads(sp.read_text(encoding="utf-8"))["replay"]["registry_sha256"],
            "0" * 64), encoding="utf-8")
    fs, dft = tamper(forge_registry)
    if not dft or not any("REGISTRY-DRIFT" in f for f in fs):
        fails += 1
        print(f"self-test: FAIL — mutated registry not reported as drift: {fs}", file=sys.stderr)

    print(f"verify_run self-test: {'PASS' if fails == 0 else 'FAIL'}"
          " (example verifies; hash/verdict/registry tampering each named)")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", type=Path)
    ap.add_argument("--record", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.run_dir:
        print("ERROR: --run-dir or --self-test required", file=sys.stderr)
        return 2
    try:
        legs, _ = verify_run(args.run_dir, args.record)
    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: RUN-RECORD-UNREADABLE: {e}", file=sys.stderr)
        return 2
    return report(legs)


if __name__ == "__main__":
    raise SystemExit(main())
