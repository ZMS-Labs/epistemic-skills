#!/usr/bin/env python3
"""validate_roster.py — mechanical validation of roster/registry.json. Stdlib only.

Checks (all must pass; exit 0 clean / 1 violations / 2 invocation error):
  1. Schema conformance (stdlib implementation of the lens.schema.json subset).
  2. Unique ids; aliases/superseded_by resolve; retired entries never deleted-in-place
     (superseded_by target must exist and be non-retired).
  3. Workflow-role coherence: role<->output_contract mapping; final_judge only on adjudicate;
     retired entries have role null; >=1 available final-judge adjudicate; >=1 available gate;
     generators are open-axis.
  4. Neighbor refs resolve; mutex groups have >=2 members and symmetric awareness.
  5. Collision heuristics on AVAILABLE evaluators: canonical-question Jaccard >= 0.60,
     or same primary_capability + domain-overlap >= 0.70, or object-of-scrutiny token
     similarity >= 0.84 — every flagged pair must be merged, mutexed, neighbored
     (explicit boundary), or listed in COLLISION_WAIVERS with a reason.
  6. Falsifier structural check: falsifier_template must name a method, a threshold,
     and a timeframe (structurally observable, not merely non-empty).
  7. Generated-view freshness (delegates to render_roster.py --check).
  8. Lifecycle is deliberately two-state: available or retired. Historical admission
     notes remain provenance, not selection authority.
"""
from __future__ import annotations
import json, re, subprocess, sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "roster" / "registry.json"

ROLE_CONTRACT = {"generate_options": "option-set@1", "evaluate": "finding-set@1",
                 "gate": "ruling-set@1", "adjudicate": "ruling-set@1"}
STATUSES = {"available", "retired"}
STANCES = {"adversarial", "constructive", "metatextual", "arbitral", "generative"}
BASES = {"base-adversarial", "base-constructive", "base-metatextual", "base-arbitrator", "base-generative"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Reviewed pairs that trip a similarity heuristic but are deliberately distinct
# (boundary encoded on both cards). Format: (id_a, id_b): reason.
COLLISION_WAIVERS = {
    ("protocol-archeologist", "chesterton-gate"):
        "hard boundary enforced on both cards: archeologist reconstructs history with NO deletion in scope; gate adjudicates ONE proposed deletion",
    ("cloud-native-purist", "local-first-survivalist"):
        "intentional counter-mode pair, mutex_group leverage-vs-sovereignty, counted as one diversity unit",
}

REQUIRED = ["schema_version", "id", "version", "status", "workflow_role", "stance", "base", "group",
            "primary_capability", "domains", "subject_axes", "object_of_scrutiny", "required_evidence",
            "causal_mechanism", "canonical_questions", "output_contract", "falsifier_template",
            "positive_signals", "contraindications", "neighbors", "cost_class", "provenance", "card"]

FALSIFIER_METHOD_RE = re.compile(r"method\s*:", re.I)
FALSIFIER_THRESHOLD_RE = re.compile(r"threshold\s*:", re.I)
FALSIFIER_TIMEFRAME_RE = re.compile(r"timeframe\s*:", re.I)


def tokens(s):
    return set(re.findall(r"[a-z]{3,}", (s or "").lower())) - {
        "the", "and", "that", "this", "with", "for", "not", "its", "into", "vs", "which",
        "what", "where", "when", "who", "how", "does", "each", "one", "two"}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def main():
    errors, warnings = [], []
    try:
        reg = json.loads(REG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: cannot parse {REG}: {e}", file=sys.stderr)
        return 2
    entries = reg.get("entries", [])
    ids = [e.get("id") for e in entries]
    dup = [i for i, c in Counter(ids).items() if c > 1]
    if dup:
        errors.append(f"duplicate ids: {dup}")
    idset = set(ids)
    all_aliases = []

    for e in entries:
        eid = e.get("id", "<missing>")
        retired = e.get("status") == "retired"
        for k in REQUIRED:
            if k not in e:
                errors.append(f"{eid}: missing field {k}")
        if not ID_RE.match(eid):
            errors.append(f"{eid}: bad id format")
        if e.get("schema_version") != 1:
            errors.append(f"{eid}: schema_version != 1")
        if e.get("status") not in STATUSES:
            errors.append(f"{eid}: bad status {e.get('status')}")
        if e.get("stance") not in STANCES:
            errors.append(f"{eid}: bad stance {e.get('stance')}")
        if e.get("base") not in BASES:
            errors.append(f"{eid}: bad base {e.get('base')}")
        role = e.get("workflow_role")
        if retired:
            if role is not None:
                errors.append(f"{eid}: retired entry must have workflow_role null")
            if not e.get("superseded_by"):
                errors.append(f"{eid}: retired entry missing superseded_by")
            else:
                tgt = e["superseded_by"]
                if tgt not in idset:
                    errors.append(f"{eid}: superseded_by {tgt} does not exist")
                else:
                    t = next(x for x in entries if x["id"] == tgt)
                    if t.get("status") == "retired":
                        errors.append(f"{eid}: superseded_by {tgt} is itself retired (chain not allowed)")
            if not e.get("card"):
                errors.append(f"{eid}: retired entry must preserve its card verbatim for replay")
        else:
            if role not in ROLE_CONTRACT:
                errors.append(f"{eid}: bad workflow_role {role}")
            elif e.get("output_contract") != ROLE_CONTRACT[role]:
                errors.append(f"{eid}: role {role} requires contract {ROLE_CONTRACT[role]}, got {e.get('output_contract')}")
            if role == "generate_options" and e.get("subject_axes") != ["open"]:
                errors.append(f"{eid}: generate_options must be open-axis only")
            for k in ("object_of_scrutiny", "required_evidence", "causal_mechanism", "falsifier_template",
                      "primary_capability"):
                if not e.get(k):
                    errors.append(f"{eid}: {k} empty on non-retired entry")
            if not e.get("canonical_questions"):
                errors.append(f"{eid}: canonical_questions empty")
            card = e.get("card") or {}
            for k in ("heuristic", "vector", "vector_label", "bias"):
                if not card.get(k):
                    errors.append(f"{eid}: card.{k} missing/empty")
            f = e.get("falsifier_template") or ""
            if not (FALSIFIER_METHOD_RE.search(f) and FALSIFIER_THRESHOLD_RE.search(f)
                    and FALSIFIER_TIMEFRAME_RE.search(f)):
                errors.append(f"{eid}: falsifier_template not structurally observable (needs method:/threshold:/timeframe:)")
        if e.get("final_judge") is not None and role != "adjudicate":
            errors.append(f"{eid}: final_judge set on non-adjudicate role")
        for n in e.get("neighbors", []):
            if n.get("id") not in idset:
                errors.append(f"{eid}: neighbor {n.get('id')} does not exist")
            if not n.get("boundary"):
                errors.append(f"{eid}: neighbor {n.get('id')} missing non-overlap boundary")
        all_aliases += e.get("aliases", [])
    alias_dup = [a for a, c in Counter(all_aliases).items() if c > 1 or a in idset]
    if alias_dup:
        errors.append(f"aliases colliding with ids or each other: {alias_dup}")

    # role-structure invariants
    available = [e for e in entries if e.get("status") == "available"]
    if not any(e.get("workflow_role") == "adjudicate" and e.get("final_judge") for e in available):
        errors.append("no available final-judge adjudicator")
    if not any(e.get("workflow_role") == "gate" for e in available):
        errors.append("no available gate")

    # mutex symmetry
    mutex = {}
    for e in available:
        if e.get("mutex_group"):
            mutex.setdefault(e["mutex_group"], []).append(e["id"])
    for g, members in mutex.items():
        if len(members) < 2:
            errors.append(f"mutex group {g} has <2 members: {members}")

    # collision heuristics on available evaluators
    evals = [e for e in available if e.get("workflow_role") == "evaluate"]
    def waived(a, b):
        return (a, b) in COLLISION_WAIVERS or (b, a) in COLLISION_WAIVERS
    def neighbored(ea, eb):
        return any(n["id"] == eb["id"] for n in ea.get("neighbors", [])) or \
               any(n["id"] == ea["id"] for n in eb.get("neighbors", []))
    def mutexed(ea, eb):
        return ea.get("mutex_group") and ea.get("mutex_group") == eb.get("mutex_group")
    flagged = 0
    for ea, eb in combinations(evals, 2):
        qj = jaccard(tokens(" ".join(ea["canonical_questions"])), tokens(" ".join(eb["canonical_questions"])))
        dj = jaccard(set(ea["domains"]), set(eb["domains"]))
        oj = jaccard(tokens(ea["object_of_scrutiny"]), tokens(eb["object_of_scrutiny"]))
        hit = qj >= 0.60 or (ea["primary_capability"] == eb["primary_capability"] and dj >= 0.70) or oj >= 0.84
        if hit:
            flagged += 1
            if not (waived(ea["id"], eb["id"]) or neighbored(ea, eb) or mutexed(ea, eb)):
                errors.append(f"UNRESOLVED collision {ea['id']} / {eb['id']} (qJ={qj:.2f} dJ={dj:.2f} oJ={oj:.2f}) — merge, mutex, add explicit neighbor boundary, or waive with reason")
    warnings.append(f"collision heuristic flagged {flagged} pair(s); all resolved/waived" if not any('UNRESOLVED' in x for x in errors) else f"collision heuristic flagged {flagged} pair(s)")

    # generated-view freshness
    rc = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_roster.py"), "--check"],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        errors.append(f"generated roster views stale: {rc.stderr.strip() or rc.stdout.strip()}")

    for w in warnings:
        print(f"note: {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} violation(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK — {len(entries)} entries validate; role/lifecycle structure sound; views fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
