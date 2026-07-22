#!/usr/bin/env python3
"""Aggregate runs/ledger.jsonl into per-lens lifecycle stats and threshold flags.

The numeric thresholds come from reference/lens-registry.md:
- probation -> activation review after >= 20 eligible runs seated
- deprecate/merge candidate when duplicate rate > 70% AND unique upheld yield < 0.1/run
  (only flagged once a lens has >= MIN_RUNS_FOR_DEPRECATION seated runs)

stdlib only. Exit 0 always (reporting tool, not a gate); --json for machine output.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
LEDGER = SKILL / "runs" / "ledger.jsonl"

ACTIVATION_ELIGIBLE_RUNS = 20
DEPRECATION_DUP_RATE = 0.70
DEPRECATION_YIELD = 0.10
MIN_RUNS_FOR_DEPRECATION = 10


def load_ledger(path):
    runs = []
    if not path.exists():
        return runs
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"WARN: ledger line {i} unparseable, skipped: {e}", file=sys.stderr)
            continue
        if isinstance(rec, dict) and rec.get("example"):
            continue  # synthetic example lines are never lifecycle telemetry
        if isinstance(rec, dict) and isinstance(rec.get("lenses"), list):
            runs.append(rec)
        else:
            print(f"WARN: ledger line {i} missing lenses[], skipped", file=sys.stderr)
    return runs


def aggregate(runs):
    stats = defaultdict(lambda: {
        "runs_seated": 0, "eligible_runs": 0, "upheld_unique": 0, "upheld_dup": 0,
        "overruled": 0, "unsupported": 0, "false_high": 0, "lifecycle": None,
    })
    for rec in runs:
        eligible = bool(rec.get("eligible", False))
        for lens in rec["lenses"]:
            lid = lens.get("id")
            if not lid:
                continue
            s = stats[lid]
            s["runs_seated"] += 1
            s["eligible_runs"] += 1 if eligible else 0
            for k in ("upheld_unique", "upheld_dup", "overruled", "unsupported", "false_high"):
                s[k] += int(lens.get(k, 0) or 0)
            s["lifecycle"] = lens.get("lifecycle") or s["lifecycle"]
    out = {}
    for lid, s in stats.items():
        upheld_total = s["upheld_unique"] + s["upheld_dup"]
        s["dup_rate"] = round(s["upheld_dup"] / upheld_total, 3) if upheld_total else 0.0
        s["unique_yield_per_run"] = (
            round(s["upheld_unique"] / s["runs_seated"], 3) if s["runs_seated"] else 0.0
        )
        flags = []
        if s["lifecycle"] == "probation" and s["eligible_runs"] >= ACTIVATION_ELIGIBLE_RUNS:
            flags.append("ACTIVATION-REVIEW-DUE")
        if (
            s["runs_seated"] >= MIN_RUNS_FOR_DEPRECATION
            and s["dup_rate"] > DEPRECATION_DUP_RATE
            and s["unique_yield_per_run"] < DEPRECATION_YIELD
        ):
            flags.append("DEPRECATE-MERGE-CANDIDATE")
        if s["false_high"] > 0:
            flags.append(f"FALSE-HIGH-x{s['false_high']}")
        s["flags"] = flags
        out[lid] = s
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    runs = load_ledger(Path(args.ledger))
    stats = aggregate(runs)
    if args.json:
        print(json.dumps({"runs": len(runs), "lenses": stats}, indent=1, sort_keys=True))
        return 0

    print(f"ledger: {args.ledger}\nruns recorded: {len(runs)}")
    if not stats:
        print("no lens data yet — append run records per runs/README.md (Step 8).")
        return 0
    hdr = f"{'lens':38} {'life':10} {'seat':5} {'elig':5} {'uniq':5} {'dup':5} {'yield':6} {'dupR':6} flags"
    print(hdr + "\n" + "-" * len(hdr))
    for lid in sorted(stats, key=lambda k: (-stats[k]["runs_seated"], k)):
        s = stats[lid]
        print(f"{lid:38} {s['lifecycle'] or '?':10} {s['runs_seated']:5} {s['eligible_runs']:5} "
              f"{s['upheld_unique']:5} {s['upheld_dup']:5} {s['unique_yield_per_run']:6} "
              f"{s['dup_rate']:6} {' '.join(s['flags'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
