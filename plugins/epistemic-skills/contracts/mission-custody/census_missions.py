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

from custody_mission import (  # noqa: E402
    CustodyError, Mission, _ascii_case_fold, _normalize_relpath,
)
from custody_store import MissionStore, StoreError  # noqa: E402

TERMINAL = ("completed", "cancelled")


def _fold(text: str) -> str:
    """The contract's platform-aware case rule, same as the gate's `_fold`.

    Only for identities that CANNOT be resolved to an inode (absent paths).
    On NT, `Doc.md` and `doc.md` name one artifact, so leaving the spelling
    case-sensitive would report two missions writing the same file as
    disjoint -- the overlap Q4 exists to find. A-Z only, never
    str.casefold (see `_ascii_case_fold`)."""
    return _ascii_case_fold(text) if os.name == "nt" else text


def _safe(value) -> str:
    """Render an untrusted string for a TERMINAL, never raw.

    A guard `name` only has to be a non-empty string -- validation says
    nothing about newlines or escape sequences -- and mission directory
    names come from the filesystem, which allows both. Interpolated raw into
    this report, such a name FORGES ROWS: a name containing
    "\\n  !! ZERO COVERAGE /etc::forged" printed exactly that line under Q5,
    indistinguishable from a finding, and an ANSI sequence recolored
    everything after it. An instrument whose output can be authored by the
    thing it measures is not an instrument.

    Escaping here rather than refusing at ingestion is deliberate for this
    change: refusing would reject manifests that already exist on armed
    fleets, which is an enforcement-surface change. Ingestion-side refusal
    belongs with the contract@2 batch (es#118)."""
    text = value if isinstance(value, str) else repr(value)
    out = []
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif ch.isprintable():
            out.append(ch)
        else:
            out.append(f"\\x{ord(ch):02x}" if ord(ch) < 256
                       else f"\\u{ord(ch):04x}")
    return "".join(out)


def _under(root: Path, abs_path: str) -> bool:
    """Is this resolved target inside `root`?

    Coverage is a claim ABOUT THIS ROOT. If a receipted path's parent was
    replaced by a symlink pointing out of the tree, `resolve()` yields an
    external path that exists and is a regular file -- and counting it would
    report coverage under a root that holds none of the artifact. Overlap is
    deliberately NOT filtered this way: escaped or not, those are still the
    same bytes two missions can both write."""
    target = Path(abs_path)
    return target == root or root in target.parents


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

    AUTHORITY AND HEALTH ARE DIFFERENT QUESTIONS. Taking the path from the
    chain does not make the receipt file irrelevant: an absent, corrupt or
    schema-invalid receipt is exactly what `Mission.resume()` reports as
    RECEIPT-MISSING drift, and a census that never opens the file would
    count that id as ordinary coverage and print no partial warning. So the
    path comes from the chain AND the receipt is loaded anyway, through
    `_load_receipt` -- the contract's own loader, which already applies
    `validate_record` and the content-addressed request_id check. Reusing it
    is the point: a fourth paraphrase of that rule is a fourth chance to
    disagree with it.

    The whole chain is indexed in ONE pass (`_effect_path_index`). Asking
    the per-id lookup about every id rescans from revision 1 each time, so a
    mission with one effect per revision made this quadratic -- an estate
    walk over thousands of revisions, millions of parses.
    """
    paths: list[str] = []
    problems: list[str] = []
    try:
        index = mission._effect_path_index()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        index = {}
        problems.append(f"chain index unreadable: {type(exc).__name__}: {exc}")
    for rid in _lget(latest, "receipt_ids"):
        if not isinstance(rid, str):
            problems.append(f"receipt id {rid!r} is not a string")
            continue
        try:
            receipt = mission._load_receipt(rid)
        except (OSError, ValueError) as exc:
            receipt = None
            problems.append(f"{rid}: receipt unreadable: {type(exc).__name__}")
        chained = index.get(rid)
        if receipt is None:
            problems.append(
                f"{rid}: RECEIPT-MISSING (absent, corrupt or schema-invalid) "
                "-- `resume` reports this id as drift")
        elif isinstance(chained, str) and chained \
                and receipt.get("artifact_path") != chained:
            problems.append(
                f"{rid}: receipt names {receipt.get('artifact_path')!r}, "
                f"chain records {chained!r} -- chain wins")
        if isinstance(chained, str) and chained:
            paths.append(_norm(chained))
            continue
        # chain silent -- fall back to the receipt file, and say so
        if receipt is None:
            problems.append(
                f"{rid}: no chained effect note and no loadable receipt "
                "-- path unknown, this id contributes nothing")
            continue
        ap = receipt.get("artifact_path")
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


def _identity(abs_path: str) -> tuple[tuple, str | None]:
    """(identity, problem) for overlap comparison.

    ABSENCE AND UNREADABILITY ARE DIFFERENT ANSWERS. A path that is not
    there yields a spelling-keyed identity and that is the whole truth about
    it. A path whose stat FAILS for any other reason -- traversal denied on
    a parent, a transient filesystem error -- yields the same fallback while
    being a measurement that did not happen: two hard-linked names then read
    as disjoint and Q4 prints "none", the one answer that hides the hazard
    Q4 exists to find. Verified: two missions receipting one inode under a
    traversal-denied parent were reported as non-overlapping AND as zero
    coverage, with no partial-data warning anywhere.

    Resolved path STRINGS do not identify hard links: two names for one
    inode stay distinct after resolve(), yet a write through either changes
    the same bytes -- exactly the cross-mission drift hazard Q4 exists to
    find, and the hazard this contract already tracks as MULTIPLY LINKED.
    For paths that exist, identity is (st_dev, st_ino); for paths that do
    not, the normalized spelling is the best available key -- case-folded on
    NT, where `Doc.md` and `doc.md` are one artifact and a case-sensitive
    key would report two missions writing that file as disjoint.
    """
    try:
        st = os.stat(abs_path)
    except FileNotFoundError:
        return ("path", _fold(abs_path)), None
    except (OSError, ValueError) as exc:
        return ("path", _fold(abs_path)), (
            f"{abs_path}: identity probe failed ({type(exc).__name__}) -- "
            "a hard-link overlap on this artifact CANNOT be detected")
    return ("inode", st.st_dev, st.st_ino), None


def census(root: Path) -> dict:
    root = root.resolve()
    missions_root = root / "missions"
    report: dict = {"root": str(root), "missions": [], "unreadable": [],
                    "environmental": [], "integrity": []}
    # DISCOVERY ITSELF CAN FAIL. A missions/ directory that cannot be statted
    # or enumerated raised out of census() entirely -- aborting the whole
    # multi-root walk with a traceback and no report, so every LATER root
    # went uninspected because an earlier one was unreadable. That is also a
    # workspace where `Mission.load` raises and the hook fails open, which
    # makes it a finding to report, not a reason to stop reporting.
    try:
        if not missions_root.is_dir():
            report["note"] = "no missions/ directory"
            return report
        mission_dirs = sorted(p for p in missions_root.iterdir() if p.is_dir())
    except OSError as exc:
        report["environmental"].append({
            "mission": "<missions/ not enumerable>",
            "reason": f"{type(exc).__name__}: {exc}",
            "fails_open": True,
        })
        report["discovery_failed"] = True
        return report
    for md in mission_dirs:
        # ONE STORE, POSSIBLY SEVERAL NAMES. `missions/alias -> missions/real`
        # is two entries over one store: the gate sees two active missions and
        # is genuinely disarmed (verified -- Mission.load raises
        # MultipleActiveMissions), so Q1 must keep both. Every other question
        # is about the STORE, and counting it twice doubled the armed total
        # and reported the mission as overlapping ITSELF.
        try:
            st = os.stat(md)
            store_identity = f"inode:{st.st_dev}:{st.st_ino}"
        except OSError:
            store_identity = f"path:{md.resolve()}"
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
        # INTEGRITY. Loadability is not the gate's last word: `run_gate` goes
        # on to call `mission.status()`, which runs `_verify_manifest`. A
        # schema-valid, chain-valid tail carrying an unsanctioned manifest
        # edit therefore raises INSIDE the gate, and `custody_hook` catches
        # CustodyError and FAILS OPEN for that mission -- while a census that
        # stopped at load_latest reported it as armed and enforcing. Verified
        # live: an enforce-mode guard whose tail path_globs were rewritten
        # makes run_gate raise "actuator guards changed with no new authority
        # amendment recorded (tampered)". Reporting a tampered ARMED mission
        # as healthy is the worst false-healthy this instrument can produce.
        integrity_ok = True
        # A TERMINAL mission's manifest never reaches the gate: discovery
        # skips completed and cancelled stores, so `Mission.load` resolves the
        # healthy active sibling and enforcement CONTINUES. Verified -- with a
        # tampered completed mission beside a healthy armed one, run_gate
        # returns decision='block'. Calling that a live fail-open is the same
        # "cry fail-open" defect this reader was corrected for in round 2:
        # it sends the operator hunting a hole while the guard is holding.
        # The damage is still disclosed, as history.
        is_active = latest.get("status") not in TERMINAL
        except_kwargs = {"mission": md.name, "active": is_active,
                         "status": latest.get("status"),
                         "fails_open": is_active}
        try:
            mission._verify_manifest(latest)
        except CustodyError as exc:
            report["integrity"].append({
                **except_kwargs, "kind": "tamper",
                "reason": f"{type(exc).__name__}: {exc}",
            })
            integrity_ok = False
        except Exception as exc:  # noqa: BLE001
            # The hook's own handler is equally broad and equally fail-open,
            # so anything that stops the check stops enforcement too.
            report["integrity"].append({
                **except_kwargs, "kind": "unverifiable",
                "reason": f"{type(exc).__name__}: {exc}",
            })
            integrity_ok = False
        if not integrity_ok:
            # IT STILL COUNTS TOWARD AMBIGUITY. `Mission.load` raises
            # MultipleActiveMissions during DISCOVERY -- before it ever calls
            # status(), so before any manifest is verified. With a duplicate
            # present, ambiguity is the LIVE cause and the tamper is never
            # reached. Dropping this mission from the roster printed tamper
            # as the sole cause and hid the still-active duplicate, so
            # repairing the manifest would leave the gate inert for a reason
            # this census never named. It stays counted, and stays out of
            # every enforcement metric below.
            report["missions"].append({
                "mission": md.name,
                "store_identity": store_identity,
                "status": latest.get("status"),
                "active": latest.get("status") not in TERMINAL,
                "revision": latest.get("revision"),
                "integrity_ok": False,
                "guard_mode": None, "guard_count": 0,
                "guard_classes": [], "guard_names": [],
                "scope_in": [], "scope_out": [],
                "receipt_count": 0, "receipt_paths": [], "absolute_paths": [],
                "identities": [], "artifacts_present_under_root": 0,
                "escaped_targets": [], "recover_obligations": [],
                "receipt_problems": [], "coverage_probe_failures": 0,
            })
            continue
        manifest = _dget(latest, "manifest")
        auth = _dget(manifest, "authority")
        scope = _dget(manifest, "scope")
        guards = _lget(auth, "actuator_guards")
        paths, problems = _receipts(mission, store, latest)
        abs_paths = [str((root / p).resolve()) for p in paths]
        probed = [_identity(a) for a in abs_paths]
        identities = [i for i, _ in probed]
        identity_failures = sum(1 for _, p in probed if p)
        problems.extend(p for _, p in probed if p)
        # COVERAGE counts DISTINCT ARTIFACTS, not receipt events: a second
        # effect or a reconciliation on one path leaves both ids in
        # receipt_ids, and counting each would report two present artifacts
        # for one file. It counts only REGULAR FILES (the effect writer only
        # ever write_bytes()es one, so a path since replaced by a directory
        # or socket is not the artifact), and only targets still UNDER THIS
        # ROOT (an escaped symlink target exists, but not here).
        present_ids: set = set()
        escaped: list[str] = []
        probe_failures = 0
        for rel, ap, ident in zip(paths, abs_paths, identities):
            if not _under(root, ap):
                escaped.append(f"{rel} -> {ap}")
                continue
            try:
                st = os.stat(ap)
            except FileNotFoundError:
                # Definitely absent: a real zero-coverage signal.
                continue
            except (OSError, ValueError) as exc:
                # NOT absence -- a probe that failed. Counting it as absent
                # manufactures a ZERO COVERAGE finding out of a file nobody
                # could look at.
                problems.append(
                    f"{ap}: coverage probe failed ({type(exc).__name__}) -- "
                    "presence UNKNOWN, not absent")
                probe_failures += 1
                continue
            if stat.S_ISREG(st.st_mode):
                present_ids.add(ident)
        present = len(present_ids)
        # LOST COVERAGE is not silence. acknowledge_receipt_loss retires the
        # id and records RECOVER:<path> -- an artifact known to be uncovered.
        # Reading the resulting empty receipt_ids as "nothing written yet"
        # conceals exactly the loss the obligation exists to publish.
        unresolved = _lget(_dget(latest, "state"), "unresolved_verdicts")
        recover = [u[len("RECOVER:"):] for u in unresolved
                   if isinstance(u, str) and u.startswith("RECOVER:")]
        if escaped:
            problems.append("targets resolve OUTSIDE this root (not counted "
                            "as coverage here): " + "; ".join(escaped))
        if problems:
            report["unreadable"].append({
                "mission": md.name,
                "reason": "receipt problems: " + "; ".join(problems),
                "counts_toward_ambiguity": False,
                "partial_answer": True,
            })
        report["missions"].append({
            "mission": md.name,
            "store_identity": store_identity,
            "status": latest.get("status"),
            "active": latest.get("status") not in TERMINAL,
            "revision": latest.get("revision"),
            "integrity_ok": True,
            "coverage_probe_failures": probe_failures,
            "identity_probe_failures": identity_failures,
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
            "identities": [list(i) for i in identities],
            "artifacts_present_under_root": present,
            "escaped_targets": escaped,
            "recover_obligations": recover,
            "receipt_problems": problems,
        })
    return report


def summarize(reports: list[dict]) -> dict:
    # Q1 counts every GATE-LOADABLE active mission, integrity-failing ones
    # included: discovery ambiguity is decided before any manifest is read.
    # Every other question is about ENFORCEMENT, and a mission whose manifest
    # the gate will refuse enforces nothing -- so those questions run over
    # `sound` only, and the exclusion is disclosed as partial data.
    # ALIAS COLLAPSE. Two entries over one store (`missions/alias -> real`)
    # are two missions to DISCOVERY -- the gate is genuinely disarmed, so Q1
    # below reads the raw per-root roster and keeps both names. Every other
    # question is about the store itself, and counting it twice doubled the
    # armed total and reported the mission as overlapping ITSELF in Q4.
    seen_stores: set = set()
    all_missions = []
    aliases = 0
    for r in reports:
        for m in r["missions"]:
            key = (r["root"], m.get("store_identity") or m["mission"])
            if key in seen_stores:
                aliases += 1
                continue
            seen_stores.add(key)
            all_missions.append((r, m))
    active = [(r, m) for r, m in all_missions if m["active"]]
    sound = [(r, m) for r, m in active if m.get("integrity_ok", True)]
    armed = [(r, m) for r, m in sound
             if m["guard_count"] > 0 and m["guard_mode"]]
    enforce = [(r, m) for r, m in armed if m["guard_mode"] == "enforce"]
    fail_open = []
    no_active = []
    for r in reports:
        act = [m["mission"] for m in r["missions"] if m["active"]]
        if len(act) > 1:
            fail_open.append({"root": r["root"], "cause": "multiple active",
                              "missions": act})
        elif not act:
            # NOT a disarmed guard -- there is nothing here to arm. But
            # `Mission.load` raises NoActiveMission and the gate is inert, so
            # a Q1 that says nothing about this root leaves the summary line
            # claiming live enforcement everywhere it measured.
            #
            # The CAUSE must not out-run the evidence: an uninspected store
            # might well hold an active mission, so a root whose only stores
            # were skipped is "no READABLE active mission", never "terminal
            # only". (Caught by reading this instrument's own output: the
            # environmental fixture was being described as terminal-only on
            # the strength of a checkpoint nobody could open.)
            unread = (len(r["unreadable"]) + len(r.get("environmental", []))
                      + len(r.get("integrity", [])))
            if r.get("discovery_failed"):
                cause = "missions/ could not be enumerated"
            elif r.get("note"):
                cause = "no missions/ directory"
            elif not r["missions"] and unread:
                cause = f"no readable mission ({unread} store(s) uninspected)"
            elif unread:
                cause = (f"no active mission among readable stores "
                         f"({unread} uninspected)")
            else:
                cause = "no active mission (terminal only)"
            no_active.append({"root": r["root"], "cause": cause})
        for e in r.get("environmental", []):
            fail_open.append({"root": r["root"],
                              "cause": f"unreadable store ({e['reason']})",
                              "missions": [e["mission"]]})
        for t in r.get("integrity", []):
            if not t.get("fails_open"):
                continue  # terminal: the gate never loads it (see census())
            fail_open.append({"root": r["root"],
                              "cause": f"manifest {t['kind']} ({t['reason']})",
                              "missions": [t["mission"]]})
    # OVERLAP: a live hazard needs TWO LIVE MISSIONS. A completed mission and
    # its successor both receipting one project file is the ordinary
    # sequential case -- the terminal one cannot resume or reconcile, so
    # nobody will read anybody's writes as drift. Reported, but as history.
    overlaps = []
    historical = []
    for i, (ra, a) in enumerate(all_missions):
        ida = {tuple(x) for x in a["identities"]}
        for rb, b in all_missions[i + 1:]:
            idb = {tuple(x) for x in b["identities"]}
            shared = sorted(str(s) for s in (ida & idb))
            if not shared:
                continue
            row = {"a": f"{ra['root']}::{a['mission']}",
                   "b": f"{rb['root']}::{b['mission']}",
                   "shared": shared}
            if a["active"] and b["active"]:
                overlaps.append(row)
            else:
                row["terminal"] = [m["mission"] for m in (a, b)
                                   if not m["active"]]
                historical.append(row)
    # ZERO COVERAGE is an assertion about files that were LOOKED AT. A
    # mission none of whose artifacts could be statted has unknown coverage,
    # and printing it as zero manufactures a detached-store finding out of a
    # directory nobody could read.
    zero_cov = [f"{r['root']}::{m['mission']}" for r, m in sound
                if m["receipt_count"] > 0
                and m["artifacts_present_under_root"] == 0
                and not m.get("coverage_probe_failures")]
    unknown_cov = [{"mission": f"{r['root']}::{m['mission']}",
                    "unreadable_artifacts": m["coverage_probe_failures"]}
                   for r, m in sound
                   if m.get("coverage_probe_failures")
                   and m["artifacts_present_under_root"] == 0]
    lost = [{"mission": f"{r['root']}::{m['mission']}",
             "artifacts": m.get("recover_obligations", [])}
            for r, m in sound if m.get("recover_obligations")]
    # VACUITY: a mission with no receipts cannot fail the coverage test, and
    # printing "none" for it reads as a pass. Silence that means "not yet
    # testable" must be labelled, or this instrument commits the vacuous-
    # green error it exists to detect. (Found by USE, not review: the
    # freshly-opened attribution mission reported clean coverage while being
    # structurally incapable of receipting anything it governed.)
    untested = [f"{r['root']}::{m['mission']}" for r, m in sound
                if m["receipt_count"] == 0 and not m.get("recover_obligations")]
    # PARTIAL is about what was NOT inspected, whatever the cause. An
    # environmental failure leaves a store entirely unread while the gate
    # fails open on it; a corruption-skipped store is invisible to the gate
    # too (so Q1-Q3 and Q5 stand) but its receipts still exist on disk, so
    # Q4 and Q6 can be missing a real answer. Claiming complete either way
    # is the vacuous green this instrument exists to refuse.
    because: list[str] = []
    for r in reports:
        for u in r["unreadable"]:
            if u.get("partial_answer"):
                because.append(f"{r['root']}/{u['mission']}: receipt problems")
            else:
                because.append(f"{r['root']}/{u['mission']}: store unreadable "
                               "-- its receipts are invisible to Q4/Q6")
        for e in r.get("environmental", []):
            because.append(f"{r['root']}/{e['mission']}: store uninspected "
                           "(environmental) -- absent from Q2-Q6 entirely")
        for t in r.get("integrity", []):
            because.append(
                f"{r['root']}/{t['mission']}: manifest {t['kind']} -- "
                + ("guards NOT enforced, absent from Q2-Q6"
                   if t.get("fails_open") else
                   f"terminal ({t.get('status')}), historical damage only; "
                   "absent from Q2-Q6, live enforcement unaffected"))
    return {
        "q1_fail_open_roots": fail_open,
        "q1_no_active_mission_roots": no_active,
        "q2_armed_active_missions": len(armed),
        "q3_enforce_mode": len(enforce),
        "q3_audit_mode": len(armed) - len(enforce),
        "q4_artifact_overlaps": overlaps,
        "q4_historical_overlaps": historical,
        # An unqualified "none" is a claim the probe failures cannot support.
        "q4_unprobed_artifacts": sum(m.get("identity_probe_failures", 0)
                                     for _, m in all_missions),
        "q5_guard_classes": [
            {"mission": f"{r['root']}::{m['mission']}",
             "classes": m["guard_classes"], "names": m["guard_names"]}
            for r, m in armed],
        "q6_zero_coverage_missions": zero_cov,
        "q6_coverage_untested_no_receipts": untested,
        "q6_coverage_lost": lost,
        "q6_coverage_unknown": unknown_cov,
        "active_total": len(active),
        "active_sound_total": len(sound),
        "alias_entries_collapsed": aliases,
        "mission_total": len(all_missions),
        "answers_are_partial": bool(because),
        "partial_because": because,
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
          f"{summary['active_total']} active")
    if summary["alias_entries_collapsed"]:
        print(f"  ({summary['alias_entries_collapsed']} extra directory "
              "entr(y/ies) resolve to a store already counted — collapsed "
              "here, but STILL COUNTED BY Q1, because discovery sees them "
              "as separate missions and the gate is disarmed by that)")
    print()
    print("Q1 FAIL-OPEN REACHABILITY (roots whose gate is inert RIGHT NOW):")
    if summary["q1_fail_open_roots"]:
        for a in summary["q1_fail_open_roots"]:
            print(f"  !! {_safe(a['root'])}  [{_safe(a['cause'])}]: "
                  f"{', '.join(_safe(x) for x in a['missions'])}")
        print("  -> guards under these roots are retired until resolved.")
    else:
        print("  none — no root holds >= 2 gate-loadable active missions")
    if summary["q1_no_active_mission_roots"]:
        print("  (gate INERT, nothing to enforce — no active mission:)")
        for n in summary["q1_no_active_mission_roots"]:
            print(f"     -  {_safe(n['root'])}  [{_safe(n['cause'])}]")
    excluded = summary["active_total"] - summary["active_sound_total"]
    print(f"\nQ2 ARMED: {summary['q2_armed_active_missions']} of "
          f"{summary['active_sound_total']} active missions carry guards"
          + (f"  ({excluded} excluded: manifest integrity — see below)"
             if excluded else ""))
    print(f"Q3 POLARITY: {summary['q3_enforce_mode']} enforce, "
          f"{summary['q3_audit_mode']} audit "
          "(audit-mode guards already allow)")
    print("\nQ4 ARTIFACT OVERLAP (by filesystem identity, hard links included):")
    if summary["q4_artifact_overlaps"]:
        for o in summary["q4_artifact_overlaps"]:
            print(f"  !! {_safe(o['a'])}\n     <-> {_safe(o['b'])}  "
                  f"{[_safe(x) for x in o['shared']]}")
        print("  -> each mission reads the other's writes as drift; the")
        print("     discharge (reconcile) OVERWRITES the artifact.")
    elif summary["q4_unprobed_artifacts"]:
        print("  none FOUND — but "
              f"{summary['q4_unprobed_artifacts']} artifact(s) could not be")
        print("  identified, and a hard link through one of those is exactly")
        print("  what this question would otherwise catch. NOT a clean bill.")
    else:
        print("  none — no two ACTIVE missions receipt the same bytes")
    if summary["q4_historical_overlaps"]:
        print("  historical (>= 1 mission terminal — the ordinary sequential")
        print("  case; a terminal mission cannot resume or reconcile):")
        for o in summary["q4_historical_overlaps"]:
            print(f"     ~  {_safe(o['a'])}\n        <-> {_safe(o['b'])}  "
                  f"{[_safe(x) for x in o['shared']]}")
    print("\nQ5 GUARD CLASSIFICATION (heuristic — verify by eye):")
    for g in summary["q5_guard_classes"] or []:
        print(f"  {_safe(g['mission'])}: " + ", ".join(
            f"{_safe(n)} [{_safe(c)}]"
            for n, c in zip(g["names"], g["classes"])))
    if not summary["q5_guard_classes"]:
        print("  (no armed missions)")
    print("\nQ6 COVERAGE:")
    if summary["q6_zero_coverage_missions"]:
        for m in summary["q6_zero_coverage_missions"]:
            print(f"  !! ZERO COVERAGE {_safe(m)}")
        print("  -> detached store: receipted artifacts are not under this")
        print("     root as regular files (es#173 P10).")
    if summary["q6_coverage_lost"]:
        for m in summary["q6_coverage_lost"]:
            print(f"  !! COVERAGE LOST {_safe(m['mission'])}: "
                  f"{[_safe(a) for a in m['artifacts']]}")
        print("  -> a receipt was retired and the artifact is KNOWN")
        print("     uncovered (RECOVER obligation). Not 'never written':")
        print("     re-cover each artifact with a fresh effect.")
    if summary["q6_coverage_unknown"]:
        for m in summary["q6_coverage_unknown"]:
            print(f"  ?  COVERAGE UNKNOWN {_safe(m['mission'])}: "
                  f"{m['unreadable_artifacts']} artifact(s) could not be read")
        print("  -> NOT zero coverage: the probe failed (traversal denied or")
        print("     a filesystem error). Re-run where the artifacts are")
        print("     readable before concluding anything about this store.")
    if summary["q6_coverage_untested_no_receipts"]:
        for m in summary["q6_coverage_untested_no_receipts"]:
            print(f"  ?  UNTESTED (0 receipts) {_safe(m)}")
        print("  -> NOT a pass: nothing has been written yet, so coverage")
        print("     cannot be checked. Verify the root contains the")
        print("     artifacts this mission governs BEFORE work starts.")
    if not (summary["q6_zero_coverage_missions"]
            or summary["q6_coverage_untested_no_receipts"]
            or summary["q6_coverage_lost"]
            or summary["q6_coverage_unknown"]):
        print("  all active missions have receipted artifacts present here")
    unreadable = [(r["root"], u) for r in reports for u in r["unreadable"]]
    if unreadable:
        print("\nUNREADABLE / PARTIAL (reported, never silently dropped):")
        for root, u in unreadable:
            tag = "partial" if u.get("partial_answer") else "skipped-by-gate"
            print(f"  ?? [{tag}] {_safe(root)}/{_safe(u['mission'])}: "
                  f"{_safe(u['reason'])}")
    integrity = [(r["root"], t) for r in reports
                 for t in r.get("integrity", [])]
    live_int = [(r, t) for r, t in integrity if t.get("fails_open")]
    past_int = [(r, t) for r, t in integrity if not t.get("fails_open")]
    if live_int:
        print("\nMANIFEST INTEGRITY (the GATE FAILS OPEN on these):")
        for root, t in live_int:
            print(f"  !! [{_safe(t['kind'])}] {_safe(root)}/"
                  f"{_safe(t['mission'])}: {_safe(t['reason'])}")
        print("  -> run_gate calls status() -> _verify_manifest; the hook")
        print("     catches the error and allows the call. An ARMED mission")
        print("     here is NOT enforcing, however its guards read.")
    if past_int:
        print("\nMANIFEST INTEGRITY, HISTORICAL (terminal missions — the gate")
        print("never loads these, so enforcement is UNAFFECTED):")
        for root, t in past_int:
            print(f"  ~  [{_safe(t['kind'])}] {_safe(root)}/"
                  f"{_safe(t['mission'])} ({_safe(t.get('status'))}): "
                  f"{_safe(t['reason'])}")
        print("  -> the record is damaged and an auditor should know; the")
        print("     live gate is not.")
    environmental = [(r["root"], e) for r in reports
                     for e in r.get("environmental", [])]
    if environmental:
        print("\nENVIRONMENTAL (store unreadable — the GATE FAILS OPEN here):")
        for root, e in environmental:
            print(f"  !! {_safe(root)}/{_safe(e['mission'])}: "
                  f"{_safe(e['reason'])}")
        print("  -> Mission.load propagates OSError rather than skipping, so")
        print("     the hook allows every call under this workspace.")
    if summary["answers_are_partial"]:
        print("\n!! Some answers above are INCOMPLETE:")
        for why in summary["partial_because"]:
            print(f"     - {_safe(why)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
