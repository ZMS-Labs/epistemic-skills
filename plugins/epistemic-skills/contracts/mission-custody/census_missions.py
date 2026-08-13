#!/usr/bin/env python3
"""Read-only census of live mission stores — one walk, six answers.

The es#173 adjudication (2026-08-13) ruled this the single most important
next action: every option for concurrent missions was ranked on assumptions
about the live estate that NOBODY HAS MEASURED — above all how many missions
are actually armed. The armed count alone can re-order the urgency of the
whole backlog, and the ruling says so explicitly.

STRICTLY READ-ONLY. It opens no Mission, calls no lifecycle verb, and writes
nothing anywhere.

WHAT COUNTS AS A MISSION THE GATE CAN SEE. Question 1 asks whether a root's
gate is disarmed by ambiguity, so it must count missions exactly the way the
gate does. `Mission.load` calls `MissionStore.load_latest()` and SKIPS any
store that raises — a chain-broken directory beside one healthy mission
leaves the gate resolving the healthy one and still ENFORCING. Counting that
directory as a second active mission would report a fail-open that does not
exist and send the operator hunting it. So loadability is decided by the
same call the gate uses, and unloadable stores are reported in their own
section: visible, but never counted toward ambiguity.

WHAT COUNTS AS COVERAGE. Receipt paths come from the checkpoint chain's
`receipt_ids`, not from whatever JSON happens to sit in `receipts/`. A
copied, forged, or crash-orphaned receipt file is not custody: the chain
decides which ids the mission owns, and `receipt_path()` is content-
addressed (`sha256(request_id)`), so a receipt whose recorded `request_id`
disagrees with the id that names it is refused here exactly as `_load_
receipt` refuses it. Anything unreadable is REPORTED, never silently
dropped — a census that quietly omits data turns a real overlap into
"none".

The six questions, in the ruling's order:

  1. FAIL-OPEN REACHABILITY  Does any root hold >= 2 GATE-LOADABLE active
     missions? Such a root's gate is inert RIGHT NOW -- an unarmed decoy is
     enough (SECURITY.md, "Discovery ambiguity DISARMS the gate"), and no
     CLI verb can repair it.
  2. ARMED COUNT             How many missions carry guard_mode/actuator_
     guards at all? If ~zero, several "urgent" enforcement findings are
     urgent about nothing yet.
  3. GUARD POLARITY          enforce vs audit. An audit-mode guard already
     allows; only enforce-mode guards can be disarmed into a false allow.
  4. ARTIFACT OVERLAP        Do any two missions receipt the same artifact?
     Compared as RESOLVED ABSOLUTE paths, because two missions at different
     roots each receipting `src/x` touch different bytes, while a parent
     root's `sub/x` and a child root's `x` are the same file. Root-relative
     string comparison gets both wrong.
  5. GUARD CLASSIFICATION    Standing guards (a durable prohibition) vs
     effort guards (scoped to one mission's work).
  6. COVERAGE                Can each mission's receipted artifacts be found
     under its own root? A mission whose workspace contains none of them has
     structurally ZERO coverage (the scratch-workspace convention, es#173
     P10) -- custody theater, and this reports it.

Usage:
    python3 census_missions.py <root> [<root> ...]
    python3 census_missions.py --json <root> ...

Exit codes: 0 always on a completed walk (this is an instrument, not a
gate). 2 = invalid invocation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_mission import _normalize_relpath  # noqa: E402
from custody_store import MissionStore, StoreError  # noqa: E402

TERMINAL = ("completed", "cancelled")


def _norm(path: str) -> str:
    """Segment-aware normalization, borrowed from the contract itself.

    NOT `lstrip("./")`: lstrip takes a character SET, so it eats every
    leading dot and slash -- turning `.env` into `env` and `.gitignore`
    into `gitignore`, which then probes the wrong file for coverage and
    compares the wrong identity for overlap.
    """
    return _normalize_relpath(path)


def _raw_tail(mission_dir: Path) -> tuple[dict | None, str | None]:
    """The highest-numbered checkpoint read directly, for VISIBILITY ONLY.

    Used to describe a store the gate cannot load. Never feeds Q1.
    """
    cps = sorted(mission_dir.glob("checkpoints/*.json"))
    if not cps:
        return None, "no checkpoints"
    try:
        rec = json.loads(cps[-1].read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(rec, dict):
        return None, f"checkpoint is {type(rec).__name__}, not an object"
    return rec, None


def _dget(record: dict, key: str) -> dict:
    """A dict-valued field, or an empty dict.

    Every field read off a checkpoint is type-guarded: a store can be valid
    JSON and structurally wrong (`manifest` a list, the record itself an
    array), and an AttributeError here would abort the whole walk -- exactly
    the broken-store condition this reader exists to survive.
    """
    value = record.get(key)
    return value if isinstance(value, dict) else {}


def _lget(record: dict, key: str) -> list:
    value = record.get(key)
    return value if isinstance(value, list) else []


def _receipts(store: MissionStore, latest: dict) -> tuple[list[str], list[str]]:
    """(normalized artifact paths, problems) for CHAIN-BOUND receipt ids.

    Ids come from the checkpoint, and each receipt must be findable at its
    content-addressed path AND agree about its own request_id -- the rule
    `_load_receipt` already applies. An orphaned or copied receipt file is
    therefore invisible to this count, which is the point: it is not custody.
    """
    paths: list[str] = []
    problems: list[str] = []
    for rid in _lget(latest, "receipt_ids"):
        if not isinstance(rid, str):
            problems.append(f"receipt id {rid!r} is not a string")
            continue
        rp = store.receipt_path(rid)
        try:
            rec = json.loads(rp.read_text(encoding="utf-8"))
        except FileNotFoundError:
            problems.append(f"{rid}: receipt missing (chain-bound)")
            continue
        except (OSError, ValueError) as exc:
            problems.append(f"{rid}: {type(exc).__name__}: {exc}")
            continue
        if not isinstance(rec, dict):
            problems.append(f"{rid}: receipt is {type(rec).__name__}")
            continue
        if rec.get("request_id") != rid:
            problems.append(f"{rid}: receipt disagrees about its request_id")
            continue
        ap = rec.get("artifact_path")
        if not isinstance(ap, str):
            problems.append(f"{rid}: artifact_path is not a string")
            continue
        paths.append(_norm(ap))
    return paths, problems


def _classify_guard(rule) -> str:
    """Standing (durable prohibition) vs effort (scoped to this work).

    A heuristic, labelled as one in the output: the census reports the guess
    AND the rule name, so the operator corrects it rather than trusting it.
    """
    blob = json.dumps(rule).lower() if rule is not None else ""
    for marker in ("secret", "credential", ".env", "token", "key", "passwd",
                   "shadow", ".ssh", "vault"):
        if marker in blob:
            return "standing?"
    return "effort?"


def census(root: Path) -> dict:
    root = root.resolve()
    missions_root = root / "missions"
    report: dict = {"root": str(root), "missions": [], "unreadable": []}
    if not missions_root.is_dir():
        report["note"] = "no missions/ directory"
        return report
    for md in sorted(p for p in missions_root.iterdir() if p.is_dir()):
        store = MissionStore(md)
        try:
            latest, _ = store.load_latest()
            gate_loadable = True
        except (StoreError, ValueError, OSError) as exc:
            # The gate SKIPS this store, so it cannot contribute ambiguity.
            # Describe it from the raw tail for visibility only.
            raw, why = _raw_tail(md)
            report["unreadable"].append({
                "mission": md.name,
                "reason": f"{type(exc).__name__}: {exc}",
                "raw_status": (raw or {}).get("status") if raw else None,
                "raw_note": why,
                "counts_toward_ambiguity": False,
            })
            continue
        if not isinstance(latest, dict):
            report["unreadable"].append({
                "mission": md.name,
                "reason": f"checkpoint is {type(latest).__name__}, not an object",
                "counts_toward_ambiguity": False,
            })
            continue
        manifest = _dget(latest, "manifest")
        auth = _dget(manifest, "authority")
        scope = _dget(manifest, "scope")
        guards = _lget(auth, "actuator_guards")
        paths, problems = _receipts(store, latest)
        present = sum(1 for p in paths if (root / p).exists())
        if problems:
            report["unreadable"].append({
                "mission": md.name,
                "reason": "receipt problems: " + "; ".join(problems),
                "counts_toward_ambiguity": False,
                "partial_answer": True,
            })
        report["missions"].append({
            "mission": md.name,
            "gate_loadable": gate_loadable,
            "status": latest.get("status"),
            "active": latest.get("status") not in TERMINAL,
            "revision": latest.get("revision"),
            "guard_mode": auth.get("guard_mode"),
            "guard_count": len(guards),
            "guard_classes": [_classify_guard(g) for g in guards],
            "guard_names": [g.get("name") if isinstance(g, dict) else None
                            for g in guards],
            "scope_in": _lget(scope, "in"),
            "scope_out": _lget(scope, "out"),
            "receipt_count": len(paths),
            "receipt_paths": paths,
            "absolute_paths": [str((root / p).resolve()) for p in paths],
            "artifacts_present_under_root": present,
            "receipt_problems": problems,
        })
    return report


def summarize(reports: list[dict]) -> dict:
    all_missions = [(r, m) for r in reports for m in r["missions"]]
    active = [(r, m) for r, m in all_missions if m["active"]]
    armed = [(r, m) for r, m in active
             if m["guard_count"] > 0 and m["guard_mode"]]
    enforce = [(r, m) for r, m in armed if m["guard_mode"] == "enforce"]
    # Q1: only GATE-LOADABLE active missions create ambiguity, because only
    # those are what Mission.load counts.
    ambiguous = []
    for r in reports:
        act = [m["mission"] for m in r["missions"] if m["active"]]
        if len(act) > 1:
            ambiguous.append({"root": r["root"], "missions": act})
    # Q4: compare RESOLVED ABSOLUTE paths, so different roots spelling the
    # same relative path are not conflated and nested roots are not missed.
    overlaps = []
    for i, (ra, a) in enumerate(all_missions):
        for rb, b in all_missions[i + 1:]:
            shared = sorted(set(a["absolute_paths"]) & set(b["absolute_paths"]))
            if shared:
                overlaps.append({
                    "a": f"{ra['root']}::{a['mission']}",
                    "b": f"{rb['root']}::{b['mission']}",
                    "shared_paths": shared})
    zero_cov = [f"{r['root']}::{m['mission']}" for r, m in active
                if m["receipt_count"] > 0
                and m["artifacts_present_under_root"] == 0]
    partial = any(u.get("partial_answer") for r in reports
                  for u in r["unreadable"])
    return {
        "q1_fail_open_roots": ambiguous,
        "q2_armed_active_missions": len(armed),
        "q3_enforce_mode": len(enforce),
        "q3_audit_mode": len(armed) - len(enforce),
        "q4_artifact_overlaps": overlaps,
        "q5_guard_classes": [
            {"mission": m["mission"], "classes": m["guard_classes"],
             "names": m["guard_names"]} for _, m in armed],
        "q6_zero_coverage_missions": zero_cov,
        "active_total": len(active),
        "mission_total": len(all_missions),
        "answers_are_partial": partial,
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
          f"{summary['mission_total']} gate-loadable mission(s), "
          f"{summary['active_total']} active\n")
    print("Q1 FAIL-OPEN REACHABILITY (roots whose gate is inert RIGHT NOW):")
    if summary["q1_fail_open_roots"]:
        for a in summary["q1_fail_open_roots"]:
            print(f"  !! {a['root']}: {', '.join(a['missions'])}")
        print("  -> every guard under these roots is retired until exactly")
        print("     one mission is active. No CLI verb can repair this.")
    else:
        print("  none — every root holds at most one gate-loadable active")
        print("  mission (stores the gate cannot load are listed below and")
        print("  do NOT disarm it: Mission.load skips them)")
    print(f"\nQ2 ARMED: {summary['q2_armed_active_missions']} of "
          f"{summary['active_total']} active missions carry guards")
    print(f"Q3 POLARITY: {summary['q3_enforce_mode']} enforce, "
          f"{summary['q3_audit_mode']} audit "
          "(audit-mode guards already allow)")
    print("\nQ4 ARTIFACT OVERLAP (cross-mission drift hazard, absolute paths):")
    if summary["q4_artifact_overlaps"]:
        for o in summary["q4_artifact_overlaps"]:
            print(f"  !! {o['a']}\n     <-> {o['b']}")
            for p in o["shared_paths"]:
                print(f"       {p}")
        print("  -> each mission reads the other's writes as drift; the")
        print("     discharge (reconcile) OVERWRITES the artifact.")
    else:
        print("  none — no two missions receipt the same file")
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
        print("\nUNREADABLE / PARTIAL (reported, never silently dropped):")
        for root, u in unreadable:
            tag = "partial" if u.get("partial_answer") else "skipped-by-gate"
            print(f"  ?? [{tag}] {root}/{u['mission']}: {u['reason']}")
    if summary["answers_are_partial"]:
        print("\n!! Some answers above are INCOMPLETE — see PARTIAL rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
