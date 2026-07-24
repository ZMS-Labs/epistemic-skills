#!/usr/bin/env python3
"""render_roster.py — generate the human-readable roster views from roster/registry.json.

The registry is CANONICAL; the markdown files are projections. Never hand-edit the
generated files — edit registry.json and re-render. validate_roster.py fails on staleness.

Generates:
  roster/adversaries.md, visionaries.md, metatextual.md,
  roster/arbitrators-and-specialists.md, generative-counterfactual.md   (persona-card views,
      same ## <id> card format the Workflow injects as {{PERSONA_SPEC}})
  roster/INDEX.md   (role/lifecycle-separated counts + capability map — the only place counts live)

Usage: python render_roster.py [--check]   (--check: exit 1 if any generated file is stale)
Stdlib only.
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "roster"
HEADER = "<!-- GENERATED from registry.json by scripts/render_roster.py — DO NOT EDIT BY HAND -->\n"

GROUP_FILES = {
    "adversaries": ("adversaries.md", "Roster Group A — Adversaries (Hostile Scrutiny)",
                    "Use with `bases/base-adversarial.md`. Each card below is a `{{PERSONA_SPEC}}` body."),
    "visionaries": ("visionaries.md", "Roster Group B — Visionaries (Constructive Ally)",
                    "Use with `bases/base-constructive.md`. Each card below is a `{{PERSONA_SPEC}}` body."),
    "metatextual": ("metatextual.md", "Roster Group C — Metatextual Critics (Foundational)",
                    "Use with `bases/base-metatextual.md`. Each card below is a `{{PERSONA_SPEC}}` body."),
    "arbitrators-and-specialists": ("arbitrators-and-specialists.md", "Roster Group D — Arbitrators, Gates & Specialists",
                    "Judges and gates use `bases/base-arbitrator.md`; specialists use the base named on their card."),
    "generative-counterfactual": ("generative-counterfactual.md", "Roster Group E — Generative & Counterfactual (pre-panel option generators + alternative-surfacing evaluators)",
                    "generate_options cards run BEFORE the panel on open questions and emit `option-set@1` (3-5 materially distinct alternatives, always including the null/status-quo option) — generator runs never satisfy evaluator-panel diversity. Cards are base-tagged."),
    "candidates": ("candidates.md", "Expansion frontier — available evaluators",
                    "Complete fingerprints whose provenance records the former admission lifecycle. They are available to the ordinary subject-seeded selector; provenance never changes claim weight."),
}


def load():
    reg = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
    return reg, reg["entries"]


def render_card(e):
    lines = [f"## {e['id']}"]
    tags = []
    if e["status"] != "available":
        tags.append(e["status"].upper())
    if e.get("workflow_role") and e["workflow_role"] != "evaluate":
        tags.append(e["workflow_role"])
    if e.get("final_judge"):
        tags.append("final-judge")
    if e.get("mutex_group"):
        tags.append(f"mutex:{e['mutex_group']}")
    base = e.get("base")
    if tags or base:
        lines[0] += f"  *({', '.join(([base] if base else []) + tags)})*"
    if e["status"] == "retired":
        lines.append(f"**RETIRED** → superseded by `{e['superseded_by']}`. {e.get('notes','')}")
        c = e.get("card")
        if c:
            lines.append(f"**Core heuristic (preserved for replay):** {c['heuristic']}")
        return "\n".join(lines)
    c = e["card"]
    lines.append(f"**Core heuristic:** {c['heuristic']}")
    lines.append(f"**{c['vector_label']}:** {c['vector']}")
    lines.append(f"**Bias to declare:** {c['bias']}")
    lines.append(f"**Object of scrutiny:** {e['object_of_scrutiny']}")
    lines.append(f"**Falsifier shape:** {e['falsifier_template']}")
    if e["neighbors"]:
        nb = "; ".join(f"`{n['id']}` — {n['boundary']}" for n in e["neighbors"])
        lines.append(f"**Not to be confused with:** {nb}")
    if e.get("notes"):
        lines.append(f"**Note:** {e['notes']}")
    return "\n".join(lines)


def render_group(entries, group, title, blurb):
    cards = [e for e in entries if e["group"] == group]
    out = [HEADER, f"# {title}", "", blurb, ""]
    for e in cards:
        out.append("---\n")
        out.append(render_card(e))
        out.append("")
    return "\n".join(out)


def render_index(reg, entries):
    by_status = Counter(e["status"] for e in entries)
    available = [e for e in entries if e["status"] == "available"]
    by_role = Counter(e["workflow_role"] for e in available)
    caps = defaultdict(list)
    for e in available:
        if e["workflow_role"] == "evaluate":
            caps[e["primary_capability"]].append(e["id"])
    out = [HEADER, "# Gauntlet lens registry — INDEX (all counts computed from registry.json)", ""]
    out.append(f"Registry version: **{reg['registry_version']}** · total entries: **{len(entries)}**")
    out.append("")
    out.append("## Counts by lifecycle status")
    out.append("")
    out.append("| status | count |")
    out.append("|---|---:|")
    for s in ("available", "retired"):
        if by_status.get(s):
            out.append(f"| {s} | {by_status[s]} |")
    out.append("")
    out.append("## Counts by workflow role (available)")
    out.append("")
    out.append("| role | count | meaning |")
    out.append("|---|---:|---|")
    meanings = {"evaluate": "panel evaluators (the only seats that count toward panel diversity)",
                "generate_options": "pre-panel option generators (open questions; option-set@1)",
                "gate": "categorical / process-conformance gates (can block regardless of weighing)",
                "adjudicate": "judges + synthesis (consume the record; never count as evaluators)"}
    for r in ("evaluate", "generate_options", "gate", "adjudicate"):
        out.append(f"| {r} | {by_role.get(r, 0)} | {meanings[r]} |")
    out.append("")
    n_caps = len([c for c in caps if c])
    out.append(f"## Active evaluator capability families ({n_caps} unique diagnostic capability atoms)")
    out.append("")
    for cap in sorted(caps):
        out.append(f"- **{cap}** ({len(caps[cap])}): {', '.join('`%s`' % i for i in sorted(caps[cap]))}")
    out.append("")
    mutex = defaultdict(list)
    for e in available:
        if e.get("mutex_group"):
            mutex[e["mutex_group"]].append(e["id"])
    if mutex:
        out.append("## Mutual-exclusion / counter-mode groups (each counts as ONE diversity unit)")
        out.append("")
        for g, ids in sorted(mutex.items()):
            out.append(f"- `{g}`: {', '.join('`%s`' % i for i in ids)}")
        out.append("")
    retired = [e for e in entries if e["status"] == "retired"]
    if retired:
        out.append("## Retired aliases (IDs preserved for replay; never re-add without behavioral evidence)")
        out.append("")
        for e in retired:
            out.append(f"- `{e['id']}` → `{e['superseded_by']}`")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify generated files are fresh; exit 1 if stale")
    args = ap.parse_args()
    reg, entries = load()
    outputs = {}
    for group, (fname, title, blurb) in GROUP_FILES.items():
        outputs[ROOT / fname] = render_group(entries, group, title, blurb)
    outputs[ROOT / "INDEX.md"] = render_index(reg, entries)
    stale = []
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            if args.check:
                stale.append(path.name)
            else:
                path.write_text(content, encoding="utf-8")
                print(f"rendered {path.name}")
    if args.check:
        if stale:
            print(f"STALE generated views (re-run render_roster.py): {stale}", file=sys.stderr)
            return 1
        print("generated views fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
