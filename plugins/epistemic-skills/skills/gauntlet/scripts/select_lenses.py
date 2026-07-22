#!/usr/bin/env python3
"""select_lenses.py — deterministic constrained panel selection from roster/registry.json.

Stdlib only. Same input => same output (no randomness; ties broken by lens id).

Usage:
  python select_lenses.py --subject subject.json [--out selection.json]
  python select_lenses.py --self-test            (runs the 1000-fixture constraint battery)

Subject feature vector (subject.json):
{
  "subject": "one-line",                      # free text, used for signal keyword matching
  "axis": "fixed" | "open",
  "depth": "quick" | "standard" | "deep" | "max",
  "domains": ["infra", "security", ...],
  "risk_classes": ["irreversible", "security", "safety", ...],
  "stakeholders": ["operator", "users", ...],          # optional
  "horizon": "short" | "long",                          # optional
  "capability_needs": ["reliability", ...],             # optional required capability families
  "domain_confidence": "high" | "low",                  # optional, default low
  "defensible_priors": false,                           # optional: bayesian-adjudicator eligibility
  "operator_values_in_dossier": false,                  # optional: sovereign-ruler eligibility
  "intentional_contrast": ["leverage-vs-sovereignty"],  # optional: allows a mutex pair, counted as ONE diversity unit
  "exclude_ids": [], "include_ids": [],                 # optional operator overrides (recorded)
  "allow_probation_seat": true                          # optional; DEFAULT TRUE. Set false to skip the
                                                        # exploration seat (quick depth never seats one)
}

Panel constraints enforced (validated after selection; violation is a hard error):
  quick=3 / standard=5 / deep=5 / max=7 evaluator seats — judge is ALWAYS separate.
  >=1 adversarial, >=1 constructive, >=1 metatextual evaluator.
  >=3 distinct primary capability families at standard, >=4 at deep/max.
  >=1 domain specialist when domain_confidence == "high".
  No stance holds more than half the evaluator seats (ceil(n/2)).
  Mutex peers never co-selected unless their group is in intentional_contrast —
    and then the pair counts as ONE unit toward stance/family diversity.
  Generators and judges NEVER count toward evaluator diversity.
  Probation lenses NEVER hold core seats. Instead, at standard/deep/max, exactly one
    probation lens is seated in an ADDITIONAL exploration seat (panel size +1, outside
    all diversity/stance math), chosen rotation-balanced: fewest prior seatings per
    runs/ledger.jsonl, deterministic id tie-break. Default ON — this is how probation
    lenses accumulate their activation track record; disable only with
    allow_probation_seat=false. SHADOW-ONLY: its findings never enter arbitration or
    the verdict. Candidates are never seated anywhere.

Output: selection + full replay record (registry hash, eligibility, scores, exclusions).
Domain matching (fit Jaccard, specialist seed, specialist constraint) canonicalizes both
sides through DOMAIN_ALIASES first — see the comment above the map.
Runtime cost note: load full card text ONLY for the selected ids (the registry is scored on
compact fields; panel prompt tokens scale with panel size, not registry size).
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG_PATH = ROOT / "roster" / "registry.json"

DEPTH_SIZE = {"quick": 3, "standard": 5, "deep": 5, "max": 7}
# Leaner deep/max defaults per the 2026-07-14 external-review adjudication: no
# panel-size dose-response has been measured, saturation evidence says marginal
# seats add prose faster than information, and >5 seats grow false-high surface.
# Restore larger panels only with a measured marginal-yield justification.
MIN_FAMILIES = {"quick": 2, "standard": 3, "deep": 4, "max": 4}
W_DOMAIN, W_CAP, W_SIGNAL, W_FAMILY_GAIN, W_STANCE_GAIN, W_OVERLAP, W_COST = 3.0, 2.5, 1.0, 1.5, 1.0, 2.0, 0.5
# FROZEN (2026-07-14): the fit/MMR scoring layer showed NO detectable benefit over
# random fill under the same hard constraints (v3 arm D control). It stays because it
# is deterministic, token-free, and auditable — but treat it as UNPROVEN: do not add
# sophistication here; deletion is gated on a randomized shadow trial (adjudication doc).
COST_PENALTY = {"light": 0.0, "standard": 0.25, "heavy": 1.0}

# Domain vocabulary normalization (2026-07-22, collection audit 08 Part 2c): the
# registry's domain strings are uncontrolled free text (200+ unique strings), so
# exact-set Jaccard scored 0 for obviously on-point lenses — `finance` != `cost`
# left both economics lenses unseated on a $120k spend decision; `ux` !=
# `accessibility`/`wcag`/`inclusive-design` missed wcag-accessibility-expert on a
# UX change. This CONTROLLED alias map canonicalizes both the subject vector and
# lens domains BEFORE any domain set operation (fit Jaccard, specialist seed,
# specialist constraint check). Conservative by design: collapse only clusters
# whose members name the same diagnostic surface; anything ambiguous stays as-is.
# Single writable home: here. The registry keeps its raw strings (historical runs
# replay by id+version); canonicalization is a selector-side read transform.
DOMAIN_ALIASES = {
    # economics — the $120k spend-decision miss
    "finance": "economics", "cost": "economics", "cost-benefit": "economics",
    "spend": "economics", "cashflow": "economics", "runway": "economics",
    "resource-allocation": "economics",
    # ux-accessibility — the wcag-accessibility-expert miss
    "ux": "ux-accessibility", "ui": "ux-accessibility",
    "accessibility": "ux-accessibility", "wcag": "ux-accessibility",
    "inclusive-design": "ux-accessibility", "microcopy": "ux-accessibility",
    # infra-ops — three strings, one meaning
    "infra": "infra-ops", "operations": "infra-ops", "ops": "infra-ops",
    # security exposure
    "internet-exposure": "security", "threat-modeling": "security",
    # reliability & failure
    "robustness": "reliability", "failure-design": "reliability",
    # disaster recovery
    "backups": "disaster-recovery", "restore": "disaster-recovery",
    "dr": "disaster-recovery",
    # migration & release
    "migrations": "migration", "cutover": "migration",
    "deployment": "release", "versioning": "release",
    # legal & compliance
    "legal": "legal-compliance", "compliance": "legal-compliance",
    "regulation": "legal-compliance", "jurisdiction": "legal-compliance",
    "licensing": "legal-compliance",
    # governance
    "oversight": "governance", "accountability": "governance",
    "controls": "governance",
    # privacy
    "data-minimization": "privacy", "data-residency": "privacy",
    "surveillance": "privacy",
    # incidents & forensics
    "incident-investigation": "incident-response",
    "incident-history": "incident-response", "forensics": "incident-response",
    # observability
    "telemetry": "observability", "logging": "observability",
    "metrics": "observability",
    # tech debt
    "legacy": "tech-debt", "end-of-life": "tech-debt",
    # ml
    "ml-evaluation": "ml",
}


def canon_domains(domains):
    """Canonicalize a domain list through DOMAIN_ALIASES (identity for unmapped terms)."""
    return {DOMAIN_ALIASES.get(d, d) for d in domains}


def tokens(s):
    return set(re.findall(r"[a-z]{3,}", (s or "").lower()))


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def load_registry():
    raw = REG_PATH.read_bytes()
    reg = json.loads(raw.decode("utf-8"))
    return reg, hashlib.sha256(raw).hexdigest()


def fit_score(e, subj):
    dj = jaccard(canon_domains(e["domains"]), canon_domains(subj.get("domains", [])))
    cap = 1.0 if e["primary_capability"] in set(subj.get("capability_needs", [])) else 0.0
    subj_toks = tokens(subj.get("subject", "")) | set(subj.get("risk_classes", []))
    sig = sum(1 for s in e["positive_signals"] if tokens(s) & subj_toks)
    sig = min(sig / 2.0, 1.0)
    contra = sum(1 for c in e["contraindications"] if tokens(c) & subj_toks)
    return W_DOMAIN * dj + W_CAP * cap + W_SIGNAL * sig - 1.5 * min(contra, 2) - W_COST * COST_PENALTY[e["cost_class"]]


def overlap(e, chosen):
    if not chosen:
        return 0.0
    return max(jaccard(tokens(e["object_of_scrutiny"]), tokens(c["object_of_scrutiny"])) for c in chosen)


def eligible_evaluators(entries, subj):
    """Core-panel pool: ACTIVE evaluators only. Probation lenses are seated exclusively
    via the exploration seat (select_exploration_seat) so they never displace the panel."""
    out, excluded = [], []
    for e in entries:
        why = None
        if e["id"] in set(subj.get("exclude_ids", [])):
            why = "operator-excluded"
        elif e["workflow_role"] != "evaluate":
            why = f"role:{e['workflow_role']}"
        elif e["status"] == "active":
            pass
        else:
            why = f"status:{e['status']}"
        if why is None and subj.get("axis") not in e["subject_axes"]:
            why = f"axis:{subj.get('axis')} not in {e['subject_axes']}"
        (excluded if why else out).append((e, why) if why else e)
    return out, [(e["id"], w) for e, w in excluded]


def select_panel(entries, subj):
    size = DEPTH_SIZE[subj["depth"]]
    contrast = set(subj.get("intentional_contrast", []))
    pool, excluded = eligible_evaluators(entries, subj)
    scores = {e["id"]: round(fit_score(e, subj), 4) for e in pool}
    pool = sorted(pool, key=lambda e: (-scores[e["id"]], e["id"]))

    chosen = []
    def stance_count(st):
        return sum(1 for c in chosen if c["stance"] == st)
    def violates(e):
        if any(c["id"] == e["id"] for c in chosen):
            return "dup"
        mg = e.get("mutex_group")
        if mg and any(c.get("mutex_group") == mg for c in chosen) and mg not in contrast:
            return "mutex"
        if stance_count(e["stance"]) + 1 > math.ceil(size / 2):
            return "stance-cap"
        return None

    def take(e):
        chosen.append(e)

    # operator include_ids first (recorded, still constraint-checked)
    for iid in sorted(subj.get("include_ids", [])):
        e = next((x for x in pool if x["id"] == iid), None)
        if e and not violates(e) and len(chosen) < size:
            take(e)

    # domain specialist when confidence is high — seed FIRST (it also fills a stance slot)
    sd = canon_domains(subj.get("domains", []))
    if subj.get("domain_confidence") == "high" and sd and len(chosen) < size:
        if not any(canon_domains(c["domains"]) & sd for c in chosen):
            for e in pool:
                if canon_domains(e["domains"]) & sd and not violates(e):
                    take(e)
                    break

    # seed the three required stances with the best-fit member of each
    for st in ("adversarial", "constructive", "metatextual"):
        if len(chosen) >= size or stance_count(st) > 0:
            continue
        for e in pool:
            if e["stance"] == st and not violates(e):
                take(e)
                break

    # greedy constrained MMR fill, with capability-family gain
    while len(chosen) < size:
        fams = {c["primary_capability"] for c in chosen}
        stances = {c["stance"] for c in chosen}
        best, best_key = None, None
        for e in pool:
            if violates(e):
                continue
            mmr = (scores[e["id"]]
                   + W_FAMILY_GAIN * (e["primary_capability"] not in fams)
                   + W_STANCE_GAIN * (e["stance"] not in stances)
                   - W_OVERLAP * overlap(e, chosen))
            key = (-mmr, e["id"])
            if best_key is None or key < best_key:
                best, best_key = e, key
        if best is None:
            break
        take(best)

    # repair pass: capability-family minimum
    minfam = MIN_FAMILIES[subj["depth"]]
    def families():
        fams = {}
        for c in chosen:
            fams.setdefault(c["primary_capability"], []).append(c)
        return fams
    from collections import Counter
    guard = 0
    while len(families()) < minfam and guard < 10:
        guard += 1
        fams = families()
        stc = Counter(c["stance"] for c in chosen)
        # stance-preserving swap: evict a member of an over-represented family for a
        # new-family candidate, keeping every required stance covered
        swap = None
        victims = sorted((c for f, members in fams.items() if len(members) >= 1
                          for c in members if len(fams[c["primary_capability"]]) == max(len(m) for m in fams.values())),
                         key=lambda c: (scores[c["id"]], c["id"]))
        for victim in victims:
            stance_safe_needed = (victim["stance"] in ("adversarial", "constructive", "metatextual")
                                  and stc[victim["stance"]] <= 1)
            for e in pool:
                if e["primary_capability"] in fams or any(c["id"] == e["id"] for c in chosen) or violates(e):
                    continue
                if stance_safe_needed and e["stance"] != victim["stance"]:
                    continue
                swap = (victim, e)
                break
            if swap:
                break
        if swap is None:
            break
        chosen.remove(swap[0])
        take(swap[1])

    return chosen, scores, excluded, pool


LEDGER_PATH = ROOT / "runs" / "ledger.jsonl"


def ledger_seat_counts(ledger_path=None):
    """Seatings per lens id from runs/ledger.jsonl (rotation input). Missing/bad ledger => {}."""
    path = Path(ledger_path) if ledger_path else LEDGER_PATH
    counts = {}
    if not path.exists():
        return counts
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("example"):
            continue  # synthetic example lines never feed rotation
        for lens in rec.get("lenses", []) if isinstance(rec, dict) else []:
            lid = lens.get("id") if isinstance(lens, dict) else None
            if lid:
                counts[lid] = counts.get(lid, 0) + 1
    return counts


def select_exploration_seat(entries, subj, chosen, ledger_path=None):
    """The probation SHADOW seat: an ADDITIONAL seat at standard/deep/max (default ON).

    SHADOW semantics (2026-07-14): the seated probation lens runs with the panel and is
    mechanically criticized, and its outcomes are ledger-recorded for lifecycle telemetry —
    but its findings are EXCLUDED from arbitration and can never touch the verdict. This
    removes the panel-size confound and keeps unvalidated lenses out of the decision path.

    Rotation-balanced: among probation evaluators eligible for this subject, seat the one
    with the FEWEST prior seatings in runs/ledger.jsonl (deterministic id tie-break) so
    every probation lens accumulates its activation track record. Outside all panel
    diversity/stance math; mutex vs the core panel still enforced. Returns (entry|None, note)."""
    if subj.get("allow_probation_seat") is False:
        return None, "disabled by subject (allow_probation_seat=false)"
    if subj.get("depth") not in ("standard", "deep", "max"):
        return None, "no exploration seat at quick depth"
    contrast = set(subj.get("intentional_contrast", []))
    chosen_ids = {c["id"] for c in chosen}
    pool = []
    for e in entries:
        if e["status"] != "probation" or e["workflow_role"] != "evaluate":
            continue
        if e["id"] in set(subj.get("exclude_ids", [])) or e["id"] in chosen_ids:
            continue
        if subj.get("axis") not in e["subject_axes"]:
            continue
        mg = e.get("mutex_group")
        if mg and any(c.get("mutex_group") == mg for c in chosen) and mg not in contrast:
            continue
        pool.append(e)
    if not pool:
        return None, "no eligible probation lens for this subject"
    counts = ledger_seat_counts(ledger_path)
    pool.sort(key=lambda e: (counts.get(e["id"], 0), e["id"]))
    return pool[0], f"rotation: {pool[0]['id']} has {counts.get(pool[0]['id'], 0)} prior seatings"


def select_adjuncts(entries, subj):
    """Generators (open axis), gates, judge — all outside the evaluator panel."""
    act = {e["id"]: e for e in entries if e["status"] == "active"}
    adj = {"generators": [], "gates": [], "judge": None, "synthesis": None, "judge_note": ""}
    if subj.get("axis") == "open":
        gens = sorted((e for e in act.values() if e["workflow_role"] == "generate_options"),
                      key=lambda e: (-fit_score(e, subj), e["id"]))
        picked = [g["id"] for g in gens[:2]]
        if "null-hypothesis-advocate" in act and "null-hypothesis-advocate" not in picked:
            picked = ["null-hypothesis-advocate"] + picked[:1]
        adj["generators"] = picked
    if subj.get("depth") in ("deep", "max"):
        adj["gates"].append("governance-lawyer")
    if set(subj.get("risk_classes", [])) & {"irreversible", "safety", "security", "consent", "legality"}:
        adj["gates"].append("red-lines-arbitrator")
    if subj.get("defensible_priors"):
        adj["judge"], adj["judge_note"] = "bayesian-adjudicator", "defensible priors/likelihoods declared"
    else:
        adj["judge"], adj["judge_note"] = "pragmatic-judge", "default evidence-weighted judge"
    if subj.get("operator_values_in_dossier"):
        adj["judge_note"] += "; sovereign-ruler eligible for values-laden conflicts (operator values recorded)"
    if subj.get("depth") in ("deep", "max"):
        adj["synthesis"] = "dialectical-synthesizer"
    adj["gates"] = sorted(set(adj["gates"]))
    return adj


def check_constraints(chosen, subj, pool):
    size, errs = DEPTH_SIZE[subj["depth"]], []
    contrast = set(subj.get("intentional_contrast", []))
    if len(chosen) != size:
        errs.append(f"panel size {len(chosen)} != {size}")
    # mutex pairs in an intentional contrast count as ONE diversity unit
    units, seen_mutex = [], set()
    for c in chosen:
        mg = c.get("mutex_group")
        if mg and mg in contrast:
            if mg in seen_mutex:
                continue
            seen_mutex.add(mg)
        units.append(c)
    stances = [u["stance"] for u in units]
    for st in ("adversarial", "constructive", "metatextual"):
        if st not in stances:
            errs.append(f"missing {st} evaluator")
    from collections import Counter
    for st, n in Counter(c["stance"] for c in chosen).items():
        if n > math.ceil(size / 2):
            errs.append(f"stance {st} holds {n} > half of {size}")
    fams = {u["primary_capability"] for u in units}
    if len(fams) < MIN_FAMILIES[subj["depth"]]:
        errs.append(f"only {len(fams)} capability families < {MIN_FAMILIES[subj['depth']]}")
    mutex_groups = [c["mutex_group"] for c in chosen if c.get("mutex_group")]
    for mg, n in Counter(mutex_groups).items():
        if n > 1 and mg not in contrast:
            errs.append(f"mutex group {mg} co-selected without intentional contrast")
    if any(c["status"] != "active" for c in chosen):
        errs.append("non-active lens in core panel (probation belongs in the exploration seat)")
    if subj.get("domain_confidence") == "high":
        sd = canon_domains(subj.get("domains", []))
        available = any(canon_domains(e["domains"]) & sd for e in pool)
        if sd and available and not any(canon_domains(c["domains"]) & sd for c in chosen):
            errs.append("no domain specialist despite high domain confidence and an eligible specialist")
    return errs


def run(subj, ledger_path=None):
    reg, reg_hash = load_registry()
    entries = reg["entries"]
    chosen, scores, excluded, pool = select_panel(entries, subj)
    errs = check_constraints(chosen, subj, pool)
    adj = select_adjuncts(entries, subj)
    exp, exp_note = select_exploration_seat(entries, subj, chosen, ledger_path)
    return {
        "selection": {
            "evaluators": [{"id": c["id"], "version": c["version"], "stance": c["stance"],
                            "capability": c["primary_capability"], "status": c["status"]} for c in chosen],
            "exploration": ({"id": exp["id"], "version": exp["version"], "stance": exp["stance"],
                             "capability": exp["primary_capability"], "status": exp["status"],
                             "seat": "exploration"} if exp else None),
            "exploration_note": exp_note,
            **adj,
        },
        "constraint_violations": errs,
        "replay": {
            "registry_version": reg["registry_version"],
            "registry_sha256": reg_hash,
            "subject_vector": subj,
            "scores": dict(sorted(scores.items())),
            "exclusions": sorted(excluded),
            "selected_ids": [f"{c['id']}@{c['version']}" for c in chosen],
            "exploration_id": f"{exp['id']}@{exp['version']}" if exp else None,
        },
    }


def self_test():
    """1000 deterministic synthetic subject vectors; every selection must satisfy all constraints."""
    import itertools, random
    rng = random.Random(20260710)
    reg, _ = load_registry()
    domains = sorted({d for e in reg["entries"] for d in e["domains"]})
    caps = sorted({e["primary_capability"] for e in reg["entries"] if e["primary_capability"]})
    fails = 0
    for i in range(1000):
        subj = {
            "subject": f"fixture-{i} " + " ".join(rng.sample(domains, k=rng.randint(1, 3))),
            "axis": rng.choice(["fixed", "open"]),
            "depth": rng.choice(["quick", "standard", "deep", "max"]),
            "domains": rng.sample(domains, k=rng.randint(1, 4)),
            "risk_classes": rng.sample(["irreversible", "security", "safety", "spend", "reputation"], k=rng.randint(0, 3)),
            "capability_needs": rng.sample(caps, k=rng.randint(0, 2)),
            "domain_confidence": rng.choice(["high", "low"]),
            "defensible_priors": rng.random() < 0.2,
            "operator_values_in_dossier": rng.random() < 0.3,
            "intentional_contrast": ["leverage-vs-sovereignty"] if rng.random() < 0.1 else [],
        }
        if rng.random() < 0.2:
            subj["allow_probation_seat"] = False  # default (absent) = ON
        res = run(subj)
        if res["constraint_violations"]:
            fails += 1
            if fails <= 5:
                print(f"fixture {i}: {res['constraint_violations']}", file=sys.stderr)
        # determinism: second run must match (panel AND exploration seat)
        res2 = run(subj)
        if (res2["replay"]["selected_ids"] != res["replay"]["selected_ids"]
                or res2["replay"]["exploration_id"] != res["replay"]["exploration_id"]):
            fails += 1
            print(f"fixture {i}: NONDETERMINISTIC", file=sys.stderr)
        # candidates never seated; probation never in core panel
        if any(s["status"] != "active" for s in res["selection"]["evaluators"]):
            fails += 1
            print(f"fixture {i}: non-active in core panel", file=sys.stderr)
        exp = res["selection"]["exploration"]
        if exp is not None:
            if exp["status"] != "probation":
                fails += 1
                print(f"fixture {i}: exploration seat holds {exp['status']}", file=sys.stderr)
            if subj.get("allow_probation_seat") is False or subj["depth"] == "quick":
                fails += 1
                print(f"fixture {i}: exploration seat present when disabled/quick", file=sys.stderr)
            if exp["id"] in {s["id"] for s in res["selection"]["evaluators"]}:
                fails += 1
                print(f"fixture {i}: exploration duplicates a core seat", file=sys.stderr)
        elif (subj.get("allow_probation_seat") is not False and subj["depth"] != "quick"
              and "probation" not in res["selection"]["exploration_note"]
              and "eligible" not in res["selection"]["exploration_note"]):
            fails += 1
            print(f"fixture {i}: exploration seat unexpectedly empty: {res['selection']['exploration_note']}", file=sys.stderr)
    print(f"self-test: {1000 - fails}/1000 fixtures satisfy all panel constraints deterministically")
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.subject:
        print("ERROR: --subject or --self-test required", file=sys.stderr)
        return 2
    subj = json.loads(args.subject.read_text(encoding="utf-8"))
    res = run(subj)
    out = json.dumps(res, indent=1)
    if args.out:
        args.out.write_text(out, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(out)
    return 1 if res["constraint_violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
