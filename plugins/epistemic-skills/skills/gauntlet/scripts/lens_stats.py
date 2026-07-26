#!/usr/bin/env python3
"""Aggregate runs/ledger.jsonl into non-governing per-lens observability.

These measurements can inform a human review, but never activate, withhold, retire,
weight, or select a lens. stdlib only; --json for machine output.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
LEDGER = SKILL / "runs" / "ledger.jsonl"

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
    hdr = f"{'lens':38} {'life':10} {'seat':5} {'elig':5} {'uniq':5} {'dup':5} {'yield':6} {'dupR':6}"
    print(hdr + "\n" + "-" * len(hdr))
    for lid in sorted(stats, key=lambda k: (-stats[k]["runs_seated"], k)):
        s = stats[lid]
        print(f"{lid:38} {s['lifecycle'] or '?':10} {s['runs_seated']:5} {s['eligible_runs']:5} "
              f"{s['upheld_unique']:5} {s['upheld_dup']:5} {s['unique_yield_per_run']:6} "
              f"{s['dup_rate']:6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
