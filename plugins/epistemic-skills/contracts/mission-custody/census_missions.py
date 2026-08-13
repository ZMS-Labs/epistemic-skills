#!/usr/bin/env python3
"""Read-only census of live mission stores — one walk, six answers.

The es#173 adjudication (2026-08-13) ruled this the single most important
next action: every option for concurrent missions was ranked on assumptions
about the live estate that NOBODY HAS MEASURED — above all how many missions
are actually armed. The armed count alone can re-order the urgency of the
whole backlog, and the ruling says so explicitly.

STRICTLY READ-ONLY. It opens no Mission, calls no lifecycle verb, and writes
nothing anywhere: it reads checkpoint files directly, because
`Mission.load()` RAISES on the very condition question 1 exists to find
(`MultipleActiveMissions`), and every CLI verb except `open`/`gate` sits
below that call. A census that cannot see the broken case is not a census.

The six questions, in the ruling's order:

  1. FAIL-OPEN REACHABILITY  Does any root already hold >= 2 active
     missions? Such a root's gate is inert RIGHT NOW -- an unarmed decoy is
     enough (SECURITY.md, "Discovery ambiguity DISARMS the gate"), and no
     CLI verb can repair it.
  2. ARMED COUNT             How many missions carry guard_mode/actuator_
     guards at all? If ~zero, several "urgent" enforcement findings are
     urgent about nothing yet, and cheap-but-breaking repairs get cheaper.
  3. GUARD POLARITY          enforce vs audit. An audit-mode guard already
     allows; only enforce-mode guards can be disarmed into a false allow.
  4. RECEIPT-PATH OVERLAP    Do any two missions receipt intersecting
     artifact paths? That is the cross-mission drift hazard, measured
     rather than assumed -- two missions over one artifact make each
     other's writes read as tampering, and the discharge OVERWRITES.
  5. GUARD CLASSIFICATION    Standing guards (a durable prohibition) vs
     effort guards (scoped to one mission's work). They migrate differently
     under every candidate design.
  6. COVERAGE                Can each mission receipt anything at all under
     its own root? A mission whose workspace contains none of the artifacts
     it names has structurally ZERO coverage (the scratch-workspace
     convention, es#173 P10) -- custody theater, and this reports it.

Usage:
    python3 census_missions.py <root> [<root> ...]
    python3 census_missions.py --json <root> ...

Exit codes: 0 always on a completed walk (this is an instrument, not a
gate -- a census that fails CI is a census nobody runs). 2 = invalid
invocation. Unreadable stores are REPORTED, never skipped silently.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

TERMINAL = ("completed", "cancelled")


def _read_latest(mission_dir: Path) -> tuple[dict | None, str | None]:
    """The highest-revision checkpoint, read directly off disk.

    Deliberately NOT MissionStore.load_latest: that verifies the hash chain
    and raises on a break, and a census must be able to describe a broken
    store rather than die on it. Chain integrity is `verify` and `status`'s
    job; this only counts and classifies.
    """
    cps = sorted(mission_dir.glob("checkpoints/*.json"))
    if not cps:
        return None, "no checkpoints"
    try:
        return json.loads(cps[-1].read_text(encoding="utf-8")), None
    except (OSError, ValueError) as exc:
        return None, f"{type(exc).__name__}: {exc}"


def _receipt_paths(mission_dir: Path) -> list[str]:
    out: list[str] = []
    for rp in sorted(mission_dir.glob("receipts/*.json")):
        try:
            rec = json.loads(rp.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        p = rec.get("artifact_path")
        if isinstance(p, str):
            out.append(p.replace("\\", "/").lstrip("./"))
    return out


def _classify_guard(rule: dict) -> str:
    """Standing (durable prohibition) vs effort (scoped to this work).

    A heuristic, and labelled as one in the output: a rule naming a secret
    or credential shape reads as standing; one naming the mission's own
    working paths reads as effort. The census reports the guess AND the
    rule, so the operator corrects it rather than trusting it.
    """
    blob = json.dumps(rule).lower()
    for marker in ("secret", "credential", ".env", "token", "key", "passwd",
                   "shadow", ".ssh", "vault"):
        if marker in blob:
            return "standing?"
    return "effort?"


def census(root: Path) -> dict:
    missions_root = root / "missions"
    report: dict = {"root": str(root), "missions": [], "unreadable": []}
    if not missions_root.is_dir():
        report["note"] = "no missions/ directory"
        return report
    for md in sorted(p for p in missions_root.iterdir() if p.is_dir()):
        latest, err = _read_latest(md)
        if latest is None:
            report["unreadable"].append({"mission": md.name, "reason": err})
            continue
        auth = (latest.get("manifest") or {}).get("authority") or {}
        guards = auth.get("actuator_guards") or []
        scope = (latest.get("manifest") or {}).get("scope") or {}
        paths = _receipt_paths(md)
        # COVERAGE: does anything this mission receipted actually live under
        # this root? A mission receipting nothing that exists here is either
        # brand new or structurally detached -- the census cannot tell those
        # apart and says so, rather than guessing.
        present = sum(1 for p in paths if (root / p).exists())
        report["missions"].append({
            "mission": md.name,
            "status": latest.get("status"),
            "active": latest.get("status") not in TERMINAL,
            "revision": latest.get("revision"),
            "guard_mode": auth.get("guard_mode"),
            "guard_count": len(guards),
            "guard_classes": [_classify_guard(g) for g in guards],
            "guard_names": [g.get("name") for g in guards],
            "scope_in": scope.get("in") or [],
            "scope_out": scope.get("out") or [],
            "receipt_count": len(paths),
            "receipt_paths": paths,
            "artifacts_present_under_root": present,
        })
    return report


def summarize(reports: list[dict]) -> dict:
    all_missions = [m for r in reports for m in r["missions"]]
    active = [m for m in all_missions if m["active"]]
    armed = [m for m in active if m["guard_count"] > 0 and m["guard_mode"]]
    enforce = [m for m in armed if m["guard_mode"] == "enforce"]
    ambiguous = [{"root": r["root"],
                  "missions": [m["mission"] for m in r["missions"] if m["active"]]}
                 for r in reports
                 if sum(1 for m in r["missions"] if m["active"]) > 1]
    # Q4: pairwise receipt-path intersection, across ALL missions -- drift
    # does not care which root a mission was opened at, only which bytes two
    # missions both claim.
    overlaps = []
    for i, a in enumerate(all_missions):
        for b in all_missions[i + 1:]:
            shared = sorted(set(a["receipt_paths"]) & set(b["receipt_paths"]))
            if shared:
                overlaps.append({"a": a["mission"], "b": b["mission"],
                                 "shared_paths": shared})
    zero_cov = [m["mission"] for m in active
                if m["receipt_count"] > 0
                and m["artifacts_present_under_root"] == 0]
    return {
        "q1_fail_open_roots": ambiguous,
        "q2_armed_active_missions": len(armed),
        "q3_enforce_mode": len(enforce),
        "q3_audit_mode": len(armed) - len(enforce),
        "q4_receipt_overlaps": overlaps,
        "q5_guard_classes": [
            {"mission": m["mission"], "classes": m["guard_classes"],
             "names": m["guard_names"]} for m in armed],
        "q6_zero_coverage_missions": zero_cov,
        "active_total": len(active),
        "mission_total": len(all_missions),
    }


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    roots = [Path(a) for a in argv if not a.startswith("--")]
    if not roots:
        print(__doc__.split("Usage:")[1].strip(), file=sys.stderr)
        return 2
    reports = [census(r) for r in roots]
    summary = summarize(reports)
    if as_json:
        print(json.dumps({"roots": reports, "summary": summary},
                         indent=1, sort_keys=True))
        return 0

    print(f"# mission census — {len(roots)} root(s), "
          f"{summary['mission_total']} mission(s), "
          f"{summary['active_total']} active\n")
    print("Q1 FAIL-OPEN REACHABILITY (roots whose gate is inert RIGHT NOW):")
    if summary["q1_fail_open_roots"]:
        for a in summary["q1_fail_open_roots"]:
            print(f"  !! {a['root']}: {', '.join(a['missions'])}")
        print("  -> every guard under these roots is retired until exactly")
        print("     one mission is active. No CLI verb can repair this.")
    else:
        print("  none — every root holds at most one active mission")
    print(f"\nQ2 ARMED: {summary['q2_armed_active_missions']} of "
          f"{summary['active_total']} active missions carry guards")
    print(f"Q3 POLARITY: {summary['q3_enforce_mode']} enforce, "
          f"{summary['q3_audit_mode']} audit "
          "(audit-mode guards already allow)")
    print("\nQ4 RECEIPT-PATH OVERLAP (cross-mission drift hazard):")
    if summary["q4_receipt_overlaps"]:
        for o in summary["q4_receipt_overlaps"]:
            print(f"  !! {o['a']} <-> {o['b']}: {', '.join(o['shared_paths'])}")
        print("  -> each mission reads the other's writes as drift; the")
        print("     discharge (reconcile) OVERWRITES the artifact.")
    else:
        print("  none — no two missions receipt the same artifact path")
    print("\nQ5 GUARD CLASSIFICATION (heuristic — verify by eye):")
    for g in summary["q5_guard_classes"] or []:
        print(f"  {g['mission']}: " + ", ".join(
            f"{n} [{c}]" for n, c in zip(g["names"], g["classes"])))
    if not summary["q5_guard_classes"]:
        print("  (no armed missions)")
    print("\nQ6 ZERO-COVERAGE MISSIONS (receipts exist, none present here):")
    if summary["q6_zero_coverage_missions"]:
        for m in summary["q6_zero_coverage_missions"]:
            print(f"  !! {m}")
        print("  -> detached store: the record names artifacts this")
        print("     workspace does not contain (es#173 P10).")
    else:
        print("  none")
    unreadable = [(r["root"], u) for r in reports for u in r["unreadable"]]
    if unreadable:
        print("\nUNREADABLE STORES (reported, never skipped silently):")
        for root, u in unreadable:
            print(f"  ?? {root}/{u['mission']}: {u['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
