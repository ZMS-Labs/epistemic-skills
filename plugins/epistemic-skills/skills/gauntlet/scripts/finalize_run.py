#!/usr/bin/env python3
"""finalize_run.py — emit the gauntlet-run-record@1 manifest + ledger v2 line for a run.

Stdlib only. Deterministic: same run directory => same record. Adds nothing to the run
itself — it hashes and derives from artifacts that already exist (one writable home per
fact; this script never dual-writes):

  dossier.md            writable home of: freeze timestamp, subject path/revision,
                        evidence root path + content pin — via a machine-readable header
                        block (see below)
  prompts/selection.json  writable home of: panel selection + replay record (selector)
  prompts/seats.json    writable home of: per-seat model identity. The record carries
                        model at FAMILY granularity only; an exact "model" value is
                        local-only and is never copied into the record (data axis:
                        committed projections are family-granular)
  reports/*.md          per-lens reports (hashed)
  reports/fingerprint.json  Sovereign Fingerprint JSON (verify_evidence.py --json)
  arbitration.md        writable home of: the ruling-set@1 fenced JSON block — rulings,
                        acceptance criteria, computed verdict. The verdict and the
                        conditions array are DERIVED from it, never restated
  GAUNTLET-SUMMARY.md   writable home of: depth, docket mode, independence mode,
                        role binding — via the Meta block lines
  prompts/role-binding.json (optional)  gauntlet-role-binding@1 record (hashed)

Dossier header contract (an HTML comment at the top of dossier.md):

  <!-- gauntlet-dossier@1
  frozen_at: 2026-07-22T00:00:00Z
  subject_path: evidence/handoff-receipt.schema.json
  subject_revision: example-rev-1
  evidence_root: evidence
  evidence_root_sha256: <64-hex tree hash, from --pin-evidence-root at Step 1 freeze>
  -->

Verdict gate (re-derived, never trusted): any P1 ruling with status "open" => NO-GO;
else any P2 "open" => CONDITIONAL; else GO. The derivation must equal the ruling-set's
own computed_verdict or finalize FAILS — a computed verdict that disagrees with the
gate is a defect, not a choice.

Usage:
  python finalize_run.py --run-dir <dir>                 # writes <dir>/run-record.json
  python finalize_run.py --run-dir <dir> --ledger-line   # also print the ledger v2 line
  python finalize_run.py --run-dir <dir> --example       # stamp the line "example": true
  python finalize_run.py --pin-evidence-root <dir>       # print the tree hash (Step 1)
  python finalize_run.py --self-test                     # against examples/example-run

Exit codes: 0 ok · 1 derivation/check failure (named reason) · 2 invalid invocation
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_RUN = ROOT / "examples" / "example-run"

RECORD_KIND = "gauntlet-run-record@1"
LEDGER_SCHEMA = "ledger@2"
DOSSIER_HEADER_RE = re.compile(r"<!--\s*gauntlet-dossier@1\s*(.*?)-->", re.S)
FENCED_JSON_RE = re.compile(r"```json\s*(.*?)```", re.S)
META_RES = {
    "depth": re.compile(r"^- \*\*Depth:\*\*\s*(\S+)", re.M),
    "docket_mode": re.compile(r"^- \*\*Docket mode:\*\*\s*(\S+)", re.M),
    "independence_mode": re.compile(r"^- \*\*Independence mode:\*\*\s*(.+?)\s*$", re.M),
    "role_binding": re.compile(r"^- \*\*Role binding:\*\*\s*(\S+)", re.M),
}
UPHELD = {"UPHELD", "UPHELD-WITH-QUALIFICATIONS"}


class FinalizeError(Exception):
    """Named-reason failure; message IS the reason (fail closed, never silent)."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(root: Path) -> str:
    """Content pin over a directory: sha256 of sorted (relpath, file-sha256) pairs.

    Deterministic; ignores nothing — every file under the root is bound. This is the
    evidence-root pin: a [V path:line] verification is valid only while the pin holds.
    """
    root = Path(root)
    if not root.is_dir():
        raise FinalizeError(f"EVIDENCE-ROOT-MISSING: {root}")
    h = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(f.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(hashlib.sha256(f.read_bytes()).hexdigest().encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def parse_dossier_header(text: str) -> dict:
    m = DOSSIER_HEADER_RE.search(text)
    if not m:
        raise FinalizeError("DOSSIER-HEADER-MISSING: no <!-- gauntlet-dossier@1 ... --> block")
    header = {}
    for line in m.group(1).strip().splitlines():
        if ":" not in line:
            raise FinalizeError(f"DOSSIER-HEADER-MALFORMED: {line!r}")
        k, v = line.split(":", 1)
        header[k.strip()] = v.strip()
    required = ("frozen_at", "subject_path", "subject_revision", "evidence_root",
                "evidence_root_sha256")
    missing = [k for k in required if not header.get(k)]
    if missing:
        raise FinalizeError(f"DOSSIER-HEADER-INCOMPLETE: missing {missing}")
    return header


def extract_ruling_set(text: str) -> dict:
    """The ruling-set@1 fenced JSON block is the ONLY fenced JSON in arbitration.md
    carrying a ruling_set key."""
    for block in FENCED_JSON_RE.findall(text):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("ruling_set") == "ruling-set@1":
            return obj
    raise FinalizeError("RULING-SET-MISSING: no fenced ruling-set@1 JSON in arbitration.md")


def derive_verdict(rulings: list) -> str:
    """The gate, from ruling-set@1 P1/P2 status fields. Nothing else sets a verdict."""
    def open_at(priority):
        return any(r.get("priority") == priority and r.get("status") == "open"
                   for r in rulings)
    if open_at("P1"):
        return "NO-GO"
    if open_at("P2"):
        return "CONDITIONAL"
    return "GO"


def derive_conditions(rulings: list) -> list:
    """CONDITIONAL's structured conditions: acceptance criteria of every OPEN P2 ruling,
    lifted verbatim — {condition, falsifier{method,threshold,timeframe}, owner}."""
    conditions = []
    for r in rulings:
        if r.get("priority") != "P2" or r.get("status") != "open":
            continue
        for ac in r.get("acceptance_criteria", []):
            fals = ac.get("falsifier", {})
            conditions.append({
                "condition": ac.get("condition", ""),
                "falsifier": {"method": fals.get("method", ""),
                              "threshold": fals.get("threshold", ""),
                              "timeframe": fals.get("timeframe", "")},
                "owner": ac.get("owner", ""),
            })
    return conditions


def derive_lens_counts(rulings: list) -> dict:
    """Per-lens arbitration counts (the ledger's telemetry fields) from the ruling-set.

    upheld_unique vs upheld_dup uses basin disjointness: a basin reached by exactly one
    lens's upheld rulings is unique to that lens. SPLIT counts toward findings_p1p2 only.
    STRUCK-UNSUPPORTED / STRUCK-FALSE-HIGH are mechanical-criticism outcomes.
    """
    counts = {}
    basins = {}
    for r in rulings:
        lens = r.get("lens")
        if not lens or r.get("priority") not in ("P1", "P2"):
            continue  # ledger telemetry counts P1/P2 rulings only (runs/README.md)
        c = counts.setdefault(lens, {"findings_p1p2": 0, "upheld_unique": 0, "upheld_dup": 0,
                                     "overruled": 0, "unsupported": 0, "false_high": 0})
        c["findings_p1p2"] += 1
        ruling = r.get("ruling")
        if ruling in UPHELD:
            basins.setdefault(r.get("basin", r.get("id")), set()).add(lens)
        if ruling == "OVERRULED":
            c["overruled"] += 1
        elif ruling == "STRUCK-UNSUPPORTED":
            c["unsupported"] += 1
        elif ruling == "STRUCK-FALSE-HIGH":
            c["false_high"] += 1
    for r in rulings:
        lens, ruling = r.get("lens"), r.get("ruling")
        if lens and r.get("priority") in ("P1", "P2") and ruling in UPHELD:
            key = "upheld_unique" if len(basins[r.get("basin", r.get("id"))]) == 1 else "upheld_dup"
            counts[lens][key] += 1
    return counts


def parse_summary_meta(text: str) -> dict:
    meta = {}
    for field, rx in META_RES.items():
        m = rx.search(text)
        if not m:
            raise FinalizeError(f"SUMMARY-META-MISSING: no '{field}' line in GAUNTLET-SUMMARY.md "
                                "(Step 8 mandates recording depth, docket mode, independence "
                                "mode, role binding)")
        meta[field] = m.group(1)
    return meta


def load_json(path: Path, reason: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise FinalizeError(f"{reason}: {path}: {e}")


def build_record(run_dir: Path) -> dict:
    run_dir = Path(run_dir)
    dossier_path = run_dir / "dossier.md"
    selection_path = run_dir / "prompts" / "selection.json"
    arbitration_path = run_dir / "arbitration.md"
    summary_path = run_dir / "GAUNTLET-SUMMARY.md"
    for p in (dossier_path, selection_path, arbitration_path, summary_path):
        if not p.is_file():
            raise FinalizeError(f"ARTIFACT-MISSING: {p}")

    header = parse_dossier_header(dossier_path.read_text(encoding="utf-8"))
    evidence_root = run_dir / header["evidence_root"]
    pin = tree_sha256(evidence_root)
    if pin != header["evidence_root_sha256"]:
        raise FinalizeError("EVIDENCE-ROOT-DRIFT: dossier pin "
                            f"{header['evidence_root_sha256'][:12]}… != live tree {pin[:12]}… "
                            "— the evidence root moved after the Step 1 freeze")

    selection = load_json(selection_path, "SELECTION-MALFORMED")
    replay = selection.get("replay") or {}
    arbitration_text = arbitration_path.read_text(encoding="utf-8")
    ruling_set = extract_ruling_set(arbitration_text)
    rulings = ruling_set.get("rulings", [])
    verdict = derive_verdict(rulings)
    recorded = ruling_set.get("computed_verdict")
    if recorded != verdict:
        raise FinalizeError(f"VERDICT-MISMATCH: gate derives {verdict} from P1/P2 status "
                            f"but ruling-set records {recorded!r}")
    meta = parse_summary_meta(summary_path.read_text(encoding="utf-8"))

    seats_doc = {}
    seats_path = run_dir / "prompts" / "seats.json"
    if seats_path.is_file():
        seats_doc = load_json(seats_path, "SEATS-MALFORMED")
    seats = [{"seat": s["seat"], "model_family": s["model_family"]}
             for s in seats_doc.get("seats", [])]

    reports = []
    reports_dir = run_dir / "reports"
    for p in sorted(reports_dir.glob("*.md")) if reports_dir.is_dir() else []:
        reports.append({"lens": p.stem, "path": p.relative_to(run_dir).as_posix(),
                        "sha256": sha256_file(p)})
    fingerprint_path = reports_dir / "fingerprint.json"
    fingerprint = ({"path": fingerprint_path.relative_to(run_dir).as_posix(),
                    "sha256": sha256_file(fingerprint_path)}
                   if fingerprint_path.is_file() else None)
    binding_path = run_dir / "prompts" / "role-binding.json"
    binding_ref = ({"path": binding_path.relative_to(run_dir).as_posix(),
                    "sha256": sha256_file(binding_path)}
                   if binding_path.is_file() else None)

    return {
        "run_record": RECORD_KIND,
        "run_id": run_dir.name,
        "generated_by": "scripts/finalize_run.py",
        "dossier": {"path": "dossier.md", "sha256": sha256_file(dossier_path),
                    "frozen_at": header["frozen_at"]},
        "subject": {"path": header["subject_path"], "revision": header["subject_revision"]},
        "evidence_root": {"path": header["evidence_root"], "content_sha256": pin},
        "selection": {"path": "prompts/selection.json",
                      "replay_sha256": sha256_file(selection_path),
                      "registry_version": replay.get("registry_version"),
                      "registry_sha256": replay.get("registry_sha256"),
                      "selected_ids": replay.get("selected_ids", []),
                      "exploration_id": replay.get("exploration_id")},
        "reports": reports,
        "fingerprint": fingerprint,
        "ruling_set": {"path": "arbitration.md", "sha256": sha256_file(arbitration_path)},
        "summary": {"path": "GAUNTLET-SUMMARY.md", "sha256": sha256_file(summary_path)},
        "verdict": verdict,
        "conditions": derive_conditions(rulings),
        "depth": meta["depth"],
        "docket_mode": meta["docket_mode"],
        "independence_mode": meta["independence_mode"],
        "role_binding": {"mode": meta["role_binding"], "ref": binding_ref},
        "seats": seats,
        "valid_while": {"subject_revision": header["subject_revision"],
                        "evidence_root_sha256": pin},
    }


def build_ledger_line(record: dict, run_dir: Path, registry_entries: dict,
                      example: bool = False) -> dict:
    """The ledger v2 line: a DERIVED POINTER PROJECTION of the run record (never a
    second writable record). Per-lens model at family granularity; per-lens counts
    derived from the ruling-set (see derive_lens_counts)."""
    ruling_set = extract_ruling_set((Path(run_dir) / "arbitration.md").read_text(encoding="utf-8"))
    counts = derive_lens_counts(ruling_set.get("rulings", []))
    seat_family = {s["seat"]: s["model_family"] for s in record["seats"]}
    lenses = []
    selection = load_json(Path(run_dir) / "prompts" / "selection.json", "SELECTION-MALFORMED")
    seats = [(e, "core") for e in selection["selection"]["evaluators"]]
    if selection["selection"].get("exploration"):
        seats.append((selection["selection"]["exploration"], "exploration"))
    zero = {"findings_p1p2": 0, "upheld_unique": 0, "upheld_dup": 0,
            "overruled": 0, "unsupported": 0, "false_high": 0}
    for entry, seat in seats:
        lid = entry["id"]
        reg = registry_entries.get(lid, {})
        # shadow-seat findings never enter arbitration => no rulings => zero counts here
        lenses.append({
            "id": lid,
            "role": reg.get("workflow_role", "evaluate"),
            "lifecycle": reg.get("status", entry.get("status")),
            "seat": seat,
            "model": seat_family.get(f"{'exploration' if seat == 'exploration' else 'evaluator'}:{lid}"),
            **counts.get(lid, dict(zero)),
        })
    line = {
        "schema": LEDGER_SCHEMA,
        "ts": record["dossier"]["frozen_at"],
        "subject": record["run_id"],
        "depth": record["depth"],
        "registry_sha256": record["selection"]["registry_sha256"],
        "verdict": record["verdict"],
        "eligible": record["depth"] in ("standard", "deep", "max"),
        "run_dir": record["run_id"],
        "dossier_sha256": record["dossier"]["sha256"],
        "docket_mode": record["docket_mode"],
        "independence_mode": record["independence_mode"],
        "lenses": lenses,
    }
    if example:
        line["example"] = True
        line["eligible"] = False  # synthetic telemetry never feeds lifecycle thresholds
    return line


def load_registry_entries() -> dict:
    reg = json.loads((ROOT / "roster" / "registry.json").read_text(encoding="utf-8"))
    return {e["id"]: e for e in reg["entries"]}


def self_test() -> int:
    """Positive control: the shipped synthetic example finalizes into a schema-conformant
    record byte-identical to the shipped run-record.json, plus a conformant ledger line.
    Negative control: a tampered copy (verdict flipped in the ruling-set) must FAIL with
    a named reason."""
    fails = 0
    shipped = EXAMPLE_RUN / "run-record.json"
    record = build_record(EXAMPLE_RUN)
    emitted = json.dumps(record, indent=1, sort_keys=True) + "\n"
    if not shipped.is_file():
        print("self-test: FAIL — examples/example-run/run-record.json not shipped", file=sys.stderr)
        return 1
    if shipped.read_text(encoding="utf-8") != emitted:
        fails += 1
        print("self-test: FAIL — emitted record != shipped run-record.json "
              "(regenerate: python scripts/finalize_run.py --run-dir examples/example-run)",
              file=sys.stderr)
    for key in ("dossier", "subject", "evidence_root", "selection", "reports",
                "ruling_set", "summary", "verdict", "conditions", "depth",
                "docket_mode", "independence_mode", "role_binding", "seats", "valid_while"):
        if key not in record:
            fails += 1
            print(f"self-test: FAIL — record missing {key}", file=sys.stderr)
    if any("model" in s for s in record["seats"]):
        fails += 1
        print("self-test: FAIL — exact model identity leaked into the record (family only)",
              file=sys.stderr)
    line = build_ledger_line(record, EXAMPLE_RUN, load_registry_entries(), example=True)
    if line["schema"] != LEDGER_SCHEMA or not line.get("example") or line.get("eligible"):
        fails += 1
        print("self-test: FAIL — ledger line not a conformant example projection", file=sys.stderr)
    if any(not l.get("model") for l in line["lenses"]):
        fails += 1
        print("self-test: FAIL — ledger lenses missing family-granular model", file=sys.stderr)

    with tempfile.TemporaryDirectory() as td:
        import shutil
        tampered = Path(td) / "run"
        shutil.copytree(EXAMPLE_RUN, tampered)
        arb = tampered / "arbitration.md"
        arb.write_text(arb.read_text(encoding="utf-8").replace(
            '"computed_verdict": "CONDITIONAL"', '"computed_verdict": "GO"'), encoding="utf-8")
        try:
            build_record(tampered)
            fails += 1
            print("self-test: FAIL — tampered ruling-set verdict did not fail closed",
                  file=sys.stderr)
        except FinalizeError as e:
            if "VERDICT-MISMATCH" not in str(e):
                fails += 1
                print(f"self-test: FAIL — wrong reason: {e}", file=sys.stderr)

    print(f"finalize_run self-test: {'PASS' if fails == 0 else 'FAIL'}"
          " (example record reproducible, ledger projection conformant, tamper fails closed)")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", type=Path)
    ap.add_argument("--ledger-line", action="store_true")
    ap.add_argument("--example", action="store_true",
                    help="stamp the ledger line example:true (synthetic runs only)")
    ap.add_argument("--pin-evidence-root", type=Path,
                    help="print the evidence-root content pin (use at Step 1 freeze)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.pin_evidence_root:
        try:
            print(tree_sha256(args.pin_evidence_root))
            return 0
        except FinalizeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
    if not args.run_dir:
        print("ERROR: --run-dir (or --self-test / --pin-evidence-root) required",
              file=sys.stderr)
        return 2
    try:
        record = build_record(args.run_dir)
    except FinalizeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    out_path = args.run_dir / "run-record.json"
    out_path.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    if args.ledger_line or args.example:
        line = build_ledger_line(record, args.run_dir, load_registry_entries(),
                                 example=args.example)
        print(json.dumps(line, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
