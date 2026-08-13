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
import os
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_mission import Mission, _normalize_relpath  # noqa: E402
from custody_store import MissionStore, StoreError  # noqa: E402
from verify_mission_custody import validate_record  # noqa: E402

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


def _receipts(mission: Mission, store: MissionStore,
              latest: dict) -> tuple[list[str], list[str]]:
    """(normalized artifact paths, problems) for CHAIN-BOUND receipt ids.

    THE CHAIN IS THE AUTHORITY ON WHICH PATH, not just on which ids.
    `scope_consistency()` already refuses to trust the receipt file for this
    exact reason -- a schema-valid replacement can keep the chained
    request_id while naming a different artifact_path, which would
    manufacture or hide an overlap and move coverage. So the path comes from
    `_historical_effect_path` (the effect note appended by the revision that
    put the id into receipt_ids, inside the tamper-evident chain), and the
    receipt file is consulted only when the chain has nothing to say.

    The receipt is additionally put through `validate_record`, the rule
    `_load_receipt` applies: a parseable but schema-invalid record is NOT a
    receipt. An empty artifact_path, for instance, normalizes to "" and
    would make the workspace root itself count as a covered artifact.
    """
    paths: list[str] = []
    problems: list[str] = []
    for rid in _lget(latest, "receipt_ids"):
        if not isinstance(rid, str):
            problems.append(f"receipt id {rid!r} is not a string")
            continue
        chained = None
        try:
            chained = mission._historical_effect_path(rid)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append(f"{rid}: chain unreadable: {type(exc).__name__}")
        if isinstance(chained, str) and chained:
            paths.append(_norm(chained))
            continue
        # chain silent -- fall back to the receipt file, and say so
        rp = store.receipt_path(rid)
        try:
            rec = json.loads(rp.read_text(encoding="utf-8"))
        except FileNotFoundError:
            problems.append(f"{rid}: no chained effect note and receipt missing")
            continue
        except (OSError, ValueError) as exc:
            problems.append(f"{rid}: {type(exc).__name__}: {exc}")
            continue
        if not isinstance(rec, dict):
            problems.append(f"{rid}: receipt is {type(rec).__name__}")
            continue
        errors = validate_record(rec)
        if errors:
            problems.append(f"{rid}: receipt fails schema: {errors[:2]}")
            continue
        if rec.get("request_id") != rid:
            problems.append(f"{rid}: receipt disagrees about its request_id")
            continue
        ap = rec.get("artifact_path")
        if not isinstance(ap, str) or not ap:
            problems.append(f"{rid}: artifact_path missing or empty")
            continue
        problems.append(f"{rid}: path from RECEIPT FILE (chain silent)")
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


def _identity(abs_path: str) -> tuple:
    """Filesystem identity for overlap comparison.

    Resolved path STRINGS do not identify hard links: two names for one
    inode stay distinct after resolve(), yet a write through either changes
    the same bytes -- exactly the cross-mission drift hazard Q4 exists to
    find, and the hazard this contract already tracks as MULTIPLY LINKED.
    For paths that exist, identity is (st_dev, st_ino); for paths that do
    not, the normalized spelling is the best available key.
    """
    try:
        st = os.stat(abs_path)
    except (OSError, ValueError):
        return ("path", abs_path)
    return ("inode", st.st_dev, st.st_ino)


def census(root: Path) -> dict:
    root = root.resolve()
    missions_root = root / "missions"
    report: dict = {"root": str(root), "missions": [], "unreadable": [],
                    "environmental": []}
    if not missions_root.is_dir():
        report["note"] = "no missions/ directory"
        return report
    for md in sorted(p for p in missions_root.iterdir() if p.is_dir()):
        store = MissionStore(md)
        try:
            latest, _ = store.load_latest()
        except (StoreError, ValueError) as exc:
            # CORRUPTION: Mission.load catches exactly this pair and SKIPS
            # the store, so the gate resolves the healthy sibling and keeps
            # enforcing. Visible, but never counted toward ambiguity.
            raw, why = _raw_tail(md)
            report["unreadable"].append({
                "mission": md.name,
                "reason": f"{type(exc).__name__}: {exc}",
                "raw_status": (raw or {}).get("status") if raw else None,
                "raw_note": why,
                "counts_toward_ambiguity": False,
            })
            continue
        except OSError as exc:
            # ENVIRONMENTAL: Mission.load deliberately does NOT catch OSError
            # -- it propagates, because skipping a merely-busy store would
            # reroute discovery around it and invite a duplicate open. The
            # hook therefore FAILS OPEN for this workspace. Reporting it as
            # "skipped" would print the root as healthy while the live gate
            # allows everything: the one answer a safety instrument must
            # never give.
            report["environmental"].append({
                "mission": md.name,
                "reason": f"{type(exc).__name__}: {exc}",
                "fails_open": True,
            })
            continue
        if not isinstance(latest, dict):
            report["unreadable"].append({
                "mission": md.name,
                "reason": f"checkpoint is {type(latest).__name__}, not an object",
                "counts_toward_ambiguity": False,
            })
            continue
        try:
            mission = Mission(store, root, "census:read-only")
        except Exception as exc:
            report["unreadable"].append({
                "mission": md.name,
                "reason": f"unconstructable: {type(exc).__name__}: {exc}",
                "counts_toward_ambiguity": False,
            })
            continue
        manifest = _dget(latest, "manifest")
        auth = _dget(manifest, "authority")
        scope = _dget(manifest, "scope")
        guards = _lget(auth, "actuator_guards")
        paths, problems = _receipts(mission, store, latest)
        abs_paths = [str((root / p).resolve()) for p in paths]
        # COVERAGE counts only REGULAR FILES: the effect writer only ever
        # write_bytes()es a regular file, so a receipted path that is now a
        # directory or socket is not the artifact and must not read as
        # coverage.
        present = 0
        for ap in abs_paths:
            try:
                if stat.S_ISREG(os.stat(ap).st_mode):
                    present += 1
            except (OSError, ValueError):
                pass
        if problems:
            report["unreadable"].append({
                "mission": md.name,
                "reason": "receipt problems: " + "; ".join(problems),
                "counts_toward_ambiguity": False,
                "partial_answer": True,
            })
        report["missions"].append({
            "mission": md.name,
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
            "absolute_paths": abs_paths,
            "identities": [list(_identity(a)) for a in abs_paths],
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
    fail_open = []
    for r in reports:
        act = [m["mission"] for m in r["missions"] if m["active"]]
        if len(act) > 1:
            fail_open.append({"root": r["root"], "cause": "multiple active",
                              "missions": act})
        for e in r.get("environmental", []):
            fail_open.append({"root": r["root"],
                              "cause": f"unreadable store ({e['reason']})",
                              "missions": [e["mission"]]})
    overlaps = []
    for i, (ra, a) in enumerate(all_missions):
        ida = {tuple(x) for x in a["identities"]}
        for rb, b in all_missions[i + 1:]:
            idb = {tuple(x) for x in b["identities"]}
            shared = sorted(str(s) for s in (ida & idb))
            if shared:
                overlaps.append({
                    "a": f"{ra['root']}::{a['mission']}",
                    "b": f"{rb['root']}::{b['mission']}",
                    "shared": shared})
    zero_cov = [f"{r['root']}::{m['mission']}" for r, m in active
                if m["receipt_count"] > 0
                and m["artifacts_present_under_root"] == 0]
    # VACUITY: a mission with no receipts cannot fail the coverage test, and
    # printing "none" for it reads as a pass. Silence that means "not yet
    # testable" must be labelled, or this instrument commits the vacuous-
    # green error it exists to detect. (Found by USE, not review: the
    # freshly-opened attribution mission reported clean coverage while being
    # structurally incapable of receipting anything it governed.)
    untested = [f"{r['root']}::{m['mission']}" for r, m in active
                if m["receipt_count"] == 0]
    partial = any(u.get("partial_answer") for r in reports
                  for u in r["unreadable"])
    return {
        "q1_fail_open_roots": fail_open,
        "q2_armed_active_missions": len(armed),
        "q3_enforce_mode": len(enforce),
        "q3_audit_mode": len(armed) - len(enforce),
        "q4_artifact_overlaps": overlaps,
        "q5_guard_classes": [
            {"mission": f"{r['root']}::{m['mission']}",
             "classes": m["guard_classes"], "names": m["guard_names"]}
            for r, m in armed],
        "q6_zero_coverage_missions": zero_cov,
        "q6_coverage_untested_no_receipts": untested,
        "active_total": len(active),
        "mission_total": len(all_missions),
        "answers_are_partial": partial,
    }


def main(argv: list[str]) -> int:
    # Unknown options are REFUSED, not ignored: silently discarding `--jsno`
    # would emit human output where a caller asked for JSON and exit 0,
    # corrupting an automated consumer while the docstring promises exit 2.
    as_json = False
    raw_roots: list[str] = []
    for arg in argv:
        if arg == "--json":
            as_json = True
        elif arg.startswith("-"):
            print(f"unknown option: {arg}", file=sys.stderr)
            return 2
        else:
            raw_roots.append(arg)
    # DEDUPE by resolved identity: the same root passed twice (or once via a
    # symlink alias) would double every count and compare each mission with
    # its own copy, manufacturing an overlap.
    roots: list[Path] = []
    seen: set[str] = set()
    for r in raw_roots:
        rp = Path(r).resolve()
        if str(rp) not in seen:
            seen.add(str(rp))
            roots.append(rp)
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
            print(f"  !! {a['root']}  [{a['cause']}]: "
                  f"{', '.join(a['missions'])}")
        print("  -> guards under these roots are retired until resolved.")
    else:
        print("  none — every root resolves exactly one active mission")
    print(f"\nQ2 ARMED: {summary['q2_armed_active_missions']} of "
          f"{summary['active_total']} active missions carry guards")
    print(f"Q3 POLARITY: {summary['q3_enforce_mode']} enforce, "
          f"{summary['q3_audit_mode']} audit "
          "(audit-mode guards already allow)")
    print("\nQ4 ARTIFACT OVERLAP (by filesystem identity, hard links included):")
    if summary["q4_artifact_overlaps"]:
        for o in summary["q4_artifact_overlaps"]:
            print(f"  !! {o['a']}\n     <-> {o['b']}  {o['shared']}")
        print("  -> each mission reads the other's writes as drift; the")
        print("     discharge (reconcile) OVERWRITES the artifact.")
    else:
        print("  none — no two missions receipt the same bytes")
    print("\nQ5 GUARD CLASSIFICATION (heuristic — verify by eye):")
    for g in summary["q5_guard_classes"] or []:
        print(f"  {g['mission']}: " + ", ".join(
            f"{n} [{c}]" for n, c in zip(g["names"], g["classes"])))
    if not summary["q5_guard_classes"]:
        print("  (no armed missions)")
    print("\nQ6 COVERAGE:")
    if summary["q6_zero_coverage_missions"]:
        for m in summary["q6_zero_coverage_missions"]:
            print(f"  !! ZERO COVERAGE {m}")
        print("  -> detached store: receipted artifacts are not under this")
        print("     root as regular files (es#173 P10).")
    if summary["q6_coverage_untested_no_receipts"]:
        for m in summary["q6_coverage_untested_no_receipts"]:
            print(f"  ?  UNTESTED (0 receipts) {m}")
        print("  -> NOT a pass: nothing has been written yet, so coverage")
        print("     cannot be checked. Verify the root contains the")
        print("     artifacts this mission governs BEFORE work starts.")
    if not (summary["q6_zero_coverage_missions"]
            or summary["q6_coverage_untested_no_receipts"]):
        print("  all active missions have receipted artifacts present here")
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
