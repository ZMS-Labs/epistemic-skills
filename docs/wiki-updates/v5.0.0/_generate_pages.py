#!/usr/bin/env python3
"""Generate the v5.0.0 wiki hand-off pages.

Run from repo root:
  python docs/wiki-updates/v5.0.0/_generate_pages.py

Idempotent: overwrites docs/wiki-updates/v5.0.0/pages/*.md authored here.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
TAG = "v5.0.0"
SRC = f"https://github.com/ZMS-Labs/epistemic-skills/blob/{TAG}"
TREE = f"https://github.com/ZMS-Labs/epistemic-skills/tree/{TAG}"


def banner(extra: str = "") -> str:
    lines = [
        f"> **Applies to:** epistemic-skills {TAG}",
        ">",
        f"> **Canonical source:** [released skill tree]({TREE}/plugins/epistemic-skills/skills)",
    ]
    if extra:
        lines.append(">")
        lines.append(f"> {extra}")
    return "\n".join(lines) + "\n\n"


def hist_banner(retired: str, survivor: str, tag_note: str) -> str:
    return (
        f"> **Historical page.** `{retired}` is not a live skill in {TAG}. "
        f"Use **`{survivor}`**. {tag_note}\n"
        f">\n"
        f"> Body text below is retained for method vocabulary and migration; "
        f"where it conflicts with a tagged `{TAG}` contract, the tagged source controls.\n\n"
    )


def write(name: str, body: str) -> None:
    path = PAGES / name
    path.write_text(body.rstrip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT.parent.parent.parent)}")


# ---------------------------------------------------------------------------
# Core navigation
# ---------------------------------------------------------------------------

write(
    "Home.md",
    banner(
        "**v5.0.0** is the loop release: fourteen skills (one entry point + thirteen "
        "disciplines). The former router and Helix seats are deleted; pairing is a "
        "`metacognate` judgment. Post-publication gate honesty: item 6 PARTIALLY MET, "
        "item 8 WAIVED — see [Version History](Version-History)."
    )
    + f"""# epistemic-skills handbook

epistemic-skills helps an agent use the least process that can still expose an error capable of changing the action or completion claim. It complements a workflow layer: workflow skills organize how work is done; epistemic skills keep the target, evidence, and claims honest.

## Start from the current release

This handbook is unversioned navigation over the versioned [{TAG} release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/{TAG}). It explains the released contracts; the [canonical repository](https://github.com/ZMS-Labs/epistemic-skills) and its versioned sources control if this handbook and a contract differ. The release documents defined behavior and known limits, not universal behavioral superiority or cross-provider generality.

{TAG} ships **fourteen** skills: `metacognate` (the only skill you invoke by name) and thirteen disciplines. `using-epistemic-skills` and `helix` were deleted; their evaluation corpora were preserved at package level. The operational loop seats are `watch`, `health`, `triage`, and `did-it-land`. See the [Skill Catalog](Skill-Catalog) and [Version History](Version-History).

| Use the skills | Start with |
|---|---|
| New to the collection | [Start Here](Start-Here) |
| Need the right amount of process | [Routine Work and Proportionality](Routine-Work-and-Proportionality) |
| Need to decide what fires | [Choosing a Skill](Choosing-a-Skill) |
| Need the entry-point contract | [metacognate](Skill-Metacognate) |
| Need the whole sequence | [The Epistemic Arc](The-Epistemic-Arc) |
| Installing or selecting a capability | [Installation and Harness Compatibility](Installation-and-Harness-Compatibility) or [Skill Catalog](Skill-Catalog) |

| Develop and maintain | Start with |
|---|---|
| Need the system boundaries | [Architecture and Contracts](Architecture-and-Contracts) |
| Need packaging details | [Cross-Harness Packaging](Cross-Harness-Packaging) |
| Need evidence and limits | [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations) |
| Need to run checks | [Testing and Evaluations](Testing-and-Evaluations) |
| Need to contribute or release | [Contributing](Contributing) or [Release Process and Versioning](Release-Process-and-Versioning) |
| Need provenance expectations | [Security, Provenance, and DCO](Security-Provenance-and-DCO) |

## First decision: routine or a positive trigger?

Start with the routine gate. Work stays routine only when it is reversible, local, directly checkable, and non-precedential. Make that change and run its bounded check; do not invent an entry-point record or process-only evidence to say nothing happened. See [Routine Work and Proportionality](Routine-Work-and-Proportionality).

When the approach itself is uncertain, a claim is about to bear load, an observation contradicts a tool, or work resumes from a summary, invoke **`metacognate`**. It applies the routine gate first; **silence is a success state**. Every other member fires on its own description. See [metacognate](Skill-Metacognate) and [Choosing a Skill](Choosing-a-Skill).

## Pairing with a workflow layer

When a workflow-skill layer (such as superpowers) is also active, pairing is a judgment `metacognate` makes at the moment it is needed — not a separate seat and not a stage-to-skill table. Either strand may interrupt the other; control returns to the point of interruption. The historical [Helix](Helix-Central-Passage) page documents the deleted pair-table seat.

## A compact arc

`decision-ledger` resume mode re-anchors a genuine resumption; the routine path exits before the arc. For non-routine work, `metacognate` names the unanswerable condition and the discipline it implies. The operational loop is watch → health → triage → did-it-land. Recon, resolve, goal, gate, and proof remain trigger-dependent handoffs. [The Epistemic Arc](The-Epistemic-Arc) shows the handoffs; [Core Concepts](Core-Concepts) defines the shared safeguards.

## Source of truth

Use this handbook to navigate. Use immutable {TAG} sources to establish released behavior, and label `main` only as current development. Historical evaluations retain their stated scope; see [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations) before treating evidence as a broad guarantee.
""",
)

write(
    "Start-Here.md",
    banner()
    + f"""# Start Here

This collection does not turn every edit into a ceremony. Its job is to recognize when a task needs more than ordinary workflow, then apply only the discipline that can reveal an action-changing error.

## 1. Check for routine work first

If the work is reversible, local, directly checkable, and non-precedential, make the change and run its bounded check. For unfamiliar routine-looking work, read the target and its closest test, example, or local convention first. When those reads agree, proceed without an entry-point record, a list of skipped skills, or process-only artifacts. See [Routine Work and Proportionality](Routine-Work-and-Proportionality).

## 2. Invoke `metacognate` when the approach is uncertain

`metacognate` is the **only** skill you invoke by name. Every other member fires on its own frontmatter `description`. It decides how much process the moment deserves — usually none — and hands control back. It never enumerates members and never does the work itself. Read [metacognate](Skill-Metacognate) and [Choosing a Skill](Choosing-a-Skill).

## 3. Pairing is a judgment, not a table

If a workflow-skill layer is also active, `metacognate` Tier 2 decides whether and how to pair. There is no Helix seat in {TAG}. The historical [Helix](Helix-Central-Passage) page remains for migration context only.

## 4. Follow the handoff, not a checklist

Most tasks clear the routine gate or fire zero or one discipline. The larger sequence is useful only when the task actually has multiple triggers. [The Epistemic Arc](The-Epistemic-Arc) maps those handoffs and [Skill Catalog](Skill-Catalog) leads to the individual guides.

## Read the source for a release claim

This handbook is a guide. For a behavior, contract, or limitation that must bear weight, read the linked {TAG} source and its references. The repository contract is authoritative.
""",
)

write(
    "_Sidebar.md",
    """[Home](Home)

## Use the skills

- [Start Here](Start-Here)
- [metacognate](Skill-Metacognate)
- [Choosing a Skill](Choosing-a-Skill)
- [Routine Work and Proportionality](Routine-Work-and-Proportionality)
- [The Epistemic Arc](The-Epistemic-Arc)
- [Workflow Recipes](Workflow-Recipes)
- [Installation and Harness Compatibility](Installation-and-Harness-Compatibility)
- [Skill Catalog](Skill-Catalog)

### Current skills (v5.0.0)

- [metacognate](Skill-Metacognate)
- [health](Skill-Health)
- [triage](Skill-Triage)
- [did-it-land](Skill-Did-It-Land)
- [watch](Skill-Watch)
- [recon](Skill-Recon)
- [resolve](Skill-Resolve)
- [decision-ledger](Skill-Decision-Ledger)
- [write-goal](Skill-Write-Goal)
- [outsource](Skill-Outsource)
- [open-questions](Skill-Open-Questions)
- [context-audit](Skill-Context-Audit)
- [gauntlet](Skill-Gauntlet)
- [evidence-locked-uat](Skill-Evidence-Locked-UAT)

### Historical (deleted or consolidated)

- [using-epistemic-skills](Skill-Using-Epistemic-Skills) *(deleted v5)*
- [helix](Helix-Central-Passage) *(deleted v5)*
- [blindspot-pass](Skill-Blindspot-Pass)
- [wayfinding](Skill-Wayfinding)
- [applying-formal-rigor](Skill-Applying-Formal-Rigor)
- [evidence-research](Skill-Evidence-Research)
- [throwaway-prototyping](Skill-Throwaway-Prototyping)
- [continuity-verify](Skill-Continuity-Verify)
- [intent-traced-merge](Skill-Intent-Traced-Merge)
- [agent-interface-design](Skill-Agent-Interface-Design)

## Develop and maintain

- [Architecture and Contracts](Architecture-and-Contracts)
- [Cross-Harness Packaging](Cross-Harness-Packaging)
- [Testing and Evaluations](Testing-and-Evaluations)
- [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations)
- [Contributing](Contributing)
- [Release Process and Versioning](Release-Process-and-Versioning)
- [Security, Provenance, and DCO](Security-Provenance-and-DCO)
- [Design History and Audits](Design-History-and-Audits)

## Shared reference

- [Core Concepts](Core-Concepts)
- [Glossary](Glossary)
- [FAQ and Troubleshooting](FAQ-and-Troubleshooting)
- [Version History](Version-History)

## Navigation

- [Sidebar](_Sidebar)
- [Footer](_Footer)
""",
)

write(
    "Skill-Catalog.md",
    banner()
    + f"""# Skill Catalog

The released package has exactly **fourteen** skills: one entry point (`metacognate`) and thirteen disciplines. Descriptions below summarize released triggers; the linked guide and tagged `SKILL.md` control.

| Skill | Entry trigger | Purpose | Output | Guide |
|---|---|---|---|---|
| `metacognate` | Approach uncertain; claim about to bear load; observation contradicts a tool; resume from summary | Decide how much process this deserves — usually none — and hand control back | Unanswerable condition + named discipline; silence when routine clears | [Guide](Skill-Metacognate) |
| `health` | State of a running system wanted, or a health claim about to bear load | Probe declared subjects against declared bounds; say what could not be reached | Per-subject `OK`/`WARN`/`CRITICAL`/`UNKNOWN`; roll-up with any `UNKNOWN` is at best `UNKNOWN` | [Guide](Skill-Health) |
| `triage` | Specific subject broken/degraded; cause not established | Eliminate candidates by observation, cheapest discriminator first | `CAUSE`/`NARROWED`/`UNKNOWN`/`NOT-BROKEN` with discriminating observation | [Guide](Skill-Triage) |
| `did-it-land` | Change believed applied and something depends on it | Observe the runtime; re-check past the revert window | `LANDED`/`REVERTED`/`UNVERIFIED` | [Guide](Skill-Did-It-Land) |
| `watch` | Bound must be noticed while unattended; watcher must be proven | Specify and prove an external watcher | `DECLARED`/`INERT`/`PROVEN`/`SUSPECT`; never "installed" before first proof fire | [Guide](Skill-Watch) |
| `recon` | Territory must be mapped before effort commits (brief / initiative / candidate) | Read, decompose, or harvest — understanding only | Rewritten request; decision map + fog-free tickets; harvest record | [Guide](Skill-Recon) |
| `resolve` | Live question needs an instrument (derivation / literature / probe) | Settle with the cheapest sufficient instrument | Derivation or formal record; claim-evidence matrix; recorded probe answer | [Guide](Skill-Resolve) |
| `write-goal` | Explicit durable goal / completion contract | Bind intent to proof, scope, blockers, stop rule | Approved goal contract | [Guide](Skill-Write-Goal) |
| `decision-ledger` | Consequential uncovered moment needs durability; resume depends on remembered state | Persist the gap; re-anchor on resume | Artifact reference or `ledger-entry@1`; state digest; never a verdict | [Guide](Skill-Decision-Ledger) |
| `outsource` | Durable handoff to external model/agent/process | Repo-backed complete handoff | Exact-ref packet/pointer, or `BLOCKED` | [Guide](Skill-Outsource) |
| `gauntlet` | High-stakes / irreversible / risky pre-merge gate | Multi-lens adversarial review of frozen subject | Conflict Ledger + GO/CONDITIONAL/NO-GO | [Guide](Skill-Gauntlet) |
| `evidence-locked-uat` | Material UI acceptance or explicit UAT | Blinded acceptance from evidence | Packet + verdict; `INCONCLUSIVE` stays inconclusive | [Guide](Skill-Evidence-Locked-UAT) |
| `open-questions` | Exhaustive interview; un-best-guessable irreversible fork with operator present | Walk question ledger to empty/parked | Emptied-or-parked ledger + 4-field stamp | [Guide](Skill-Open-Questions) |
| `context-audit` | Explicit audit; cross-layer instruction conflict; model-generation upgrade | Audit assembled instruction context | Cut list, conflict ledger, re-baseline watch | [Guide](Skill-Context-Audit) |

**Craft doctrine (not disciplines):** intent-traced-merge and agent-interface-design live under [`plugins/epistemic-skills/reference/craft/`]({TREE}/plugins/epistemic-skills/reference/craft) (v4.0.0 demotion).

## Deleted in v5.0.0

| Former skill | Replacement | Historical guide |
|---|---|---|
| `using-epistemic-skills` | `metacognate` | [Using Epistemic Skills](Skill-Using-Epistemic-Skills) |
| `helix` | `metacognate` Tier 2 pairing judgment (not a pair table) | [Helix: Central Passage](Helix-Central-Passage) |

## Consolidated names (v3.x → v4.0.0, still current vocabulary)

| v3.x skill | Current home | Historical guide |
|---|---|---|
| `blindspot-pass` | `recon` — brief mode | [Blindspot Pass](Skill-Blindspot-Pass) |
| `wayfinding` | `recon` — initiative mode | [Wayfinding](Skill-Wayfinding) |
| `harvest-before-adopt` | `recon` — candidate mode | [Recon](Skill-Recon) |
| `applying-formal-rigor` | `resolve` — derivation | [Applying Formal Rigor](Skill-Applying-Formal-Rigor) |
| `evidence-research` | `resolve` — literature | [Evidence Research](Skill-Evidence-Research) |
| `throwaway-prototyping` | `resolve` — probe | [Throwaway Prototyping](Skill-Throwaway-Prototyping) |
| `continuity-verify` | `decision-ledger` — resume mode | [Continuity Verify](Skill-Continuity-Verify) |

Routine work is not a fifteenth skill. [Choosing a Skill](Choosing-a-Skill) and [Workflow Recipes](Workflow-Recipes) provide task-first routes.
""",
)

write(
    "Choosing-a-Skill.md",
    banner()
    + f"""# Choosing a Skill

Choose from an observed trigger, not from the size of the task or a desire to be thorough. The default is ordinary work; additional process is justified only when it can expose an error that could change the action or completion claim.

## Start with this decision

| What you can observe | Next step |
|---|---|
| All four routine conditions hold | Use the bounded ordinary workflow; no special record. |
| Approach uncertain; claim about to bear load; contradiction; resume from summary | Invoke `metacognate`; silence is success when the routine gate clears. |
| State of a running system wanted, or health claim about to bear load | `health` |
| Specific thing broken/degraded; cause not established | `triage` |
| Change believed applied and something depends on it | `did-it-land` |
| Bound must be noticed unattended, or watcher must be proven | `watch` |
| Remembered summary/handoff controls the next action | `decision-ledger` resume mode |
| Request conflicts with territory, hides coupling, or risks fan-out | `recon` (brief) |
| Large foggy effort / backlog encodes unmade decisions | `recon` (initiative) |
| External project overlaps your own; adopt/replace/ignore | `recon` (candidate) |
| Material design/property claim needs a derivation | `resolve` (derivation) |
| Claim depends on research or a scholarly tool call | `resolve` (literature) |
| Live question cheaper to answer with a disposable build | `resolve` (probe) |
| Explicit persistent goal authoring | `write-goal` |
| Work crosses to an external model, agent, or process | `outsource` |
| One-way-door or high-blast-radius decision | `gauntlet` |
| Material UI-facing completion claim needs independent proof | `evidence-locked-uat` |
| Consequential decision/assumption/recurrent correction lacks durable record | `decision-ledger` |
| Operator asks for exhaustive interview, or irreversible fork with operator present | `open-questions` |
| Explicit audit / cross-layer instruction conflict / model-generation upgrade | `context-audit` |

If more than one positive trigger exists, each member's own description governs firing; `metacognate` names the unanswerable condition when the approach itself is the question. There is no inventory-holding router in {TAG}.

## Pairing with a workflow layer

When a workflow-skill layer also runs, `metacognate` decides pairing at the moment it is needed. Historical [Helix](Helix-Central-Passage) is not a live seat.

## Keep the negative path real

The routine path is not a lesser result. It is the correct result when the four conditions hold after the two-read micro-recon, and it stays silent. [Routine Work and Proportionality](Routine-Work-and-Proportionality) defines the gate; [Skill Catalog](Skill-Catalog) provides the individual reference guides.

## Canonical references

- [`metacognate` at {TAG}]({SRC}/plugins/epistemic-skills/skills/metacognate/SKILL.md)
- [Routine fast path at {TAG}]({SRC}/plugins/epistemic-skills/skills/metacognate/reference/routine-fast-path.md)
- [Generated ROUTING.md at {TAG}]({SRC}/plugins/epistemic-skills/ROUTING.md)
""",
)

write(
    "The-Epistemic-Arc.md",
    banner()
    + f"""# The Epistemic Arc

The arc is a handoff model, not a mandatory checklist. Most tasks take the routine exit or fire zero or one discipline. When several observable triggers are present, each member's description governs firing; `metacognate` owns the approach question and returns control.

```text
routine -> change + bounded check

resume -> decision-ledger resume mode -> metacognate / ordinary work
task -> metacognate -> (named discipline) -> hand control back

operational loop (when those triggers fire):
  watch (notice) -> health (assess) -> triage (cause) -> did-it-land (verify)

territory / settle / contract / gate / prove (trigger-dependent):
  recon (three modes) -> resolve (three instruments) -> write-goal
    -> gauntlet -> evidence-locked-uat

persist -> decision-ledger
delegate -> outsource
interview -> open-questions
maintain instructions -> context-audit
```

## The moments and their boundaries

- **Entry:** `metacognate` decides how much process the moment deserves. Silence is success. It never enumerates members.
- **Resumption:** `decision-ledger` resume mode re-anchors remembered state before resumed work.
- **Operational loop:** `watch` proves an unattended observer; `health` reports state without converting `UNKNOWN` into `OK`; `triage` establishes cause by discriminating observation; `did-it-land` requires a runtime observation.
- **Recon / resolve / contract / gate / proof:** unchanged in role from v4 — trigger-dependent, not conveyor-belt.
- **Persistence / delegate / interview / context:** cross-cutting as before.

## Ordering has a purpose

A later consumer re-checks whether its input is still valid; if the subject changed materially, the relevant skill re-fires instead of patching stale output. A one-skill task relies on its own output; a zero-skill task emits no entry-point record.

## Canonical references

- [`metacognate` at {TAG}]({SRC}/plugins/epistemic-skills/skills/metacognate/SKILL.md)
- [Skill tree at {TAG}]({TREE}/plugins/epistemic-skills/skills)
""",
)

# ---------------------------------------------------------------------------
# New skill guides
# ---------------------------------------------------------------------------

write(
    "Skill-Metacognate.md",
    banner("Replaces deleted `using-epistemic-skills` and `helix` seats.")
    + f"""# Metacognate

## What it does

`metacognate` is the **only** skill you invoke by name. It owns one decision: what would have to be true for this to be right, and which of those you cannot currently answer. The unanswerable condition names the work. If every condition is answerable, the correct output is **silence**.

It carries a **procedure, never an inventory**. No member list appears in it, and none may be added. Selection belongs to each member's own description.

## Two tiers

**Tier 1 — Iron** (irreversible scope only): consent precedes the irreversible; an oracle must be adequate to its claim; no actor certifies its own acceptance; a hard gate is not overridable from the other side. These bind both this collection and any workflow layer.

**Tier 2 — Wise:** name the unanswerable condition; engage the discipline whose description matches it; hand control back. Pairing with a workflow layer is a judgment at a moment, not a stage-to-skill table.

## Use it when

- The approach itself is uncertain rather than just the answer.
- A claim is about to bear load ("it works", "it is done", "it is deployed", "it is fine").
- An observation contradicts what a tool or document just asserted.
- Work resumes from a summary, handoff, or remembered state.

## Do not use it when

- Routine reversible, local, directly checkable, non-precedential work.
- Lookups or mechanical edits.
- A call the operator has already made.
- From inside a discipline this would hand to (no recursive invocation).

## Related

- [Routine Work and Proportionality](Routine-Work-and-Proportionality)
- [Choosing a Skill](Choosing-a-Skill)
- Historical: [Using Epistemic Skills](Skill-Using-Epistemic-Skills), [Helix](Helix-Central-Passage)

## Canonical sources

- [SKILL.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/metacognate/SKILL.md)
- [routine-fast-path.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/metacognate/reference/routine-fast-path.md)
""",
)

write(
    "Skill-Health.md",
    banner()
    + f"""# Health

## What it does

Reports whether a running system is in the state it should be — and for each part of that answer, whether you actually looked. A roll-up containing any `UNKNOWN` is itself at best `UNKNOWN`. Absence of evidence never renders as healthy.

| State | Meaning |
|---|---|
| `OK` | Probed, within declared bounds |
| `WARN` | Probed, outside a soft bound |
| `CRITICAL` | Probed, outside a hard bound or required service down |
| `UNKNOWN` | Could not probe — never rendered as `OK` |

## Use it when

- You need the current state of a running system.
- Before a change with blast radius, after restart/power events.
- A health claim is about to bear load.

## Do not use it when

- A specific thing is already known broken and you want the cause → [`triage`](Skill-Triage).
- One metric you could read directly would answer it.
- The question is about a change you are making rather than the state you are in.

## Related

- Hands to: [`triage`](Skill-Triage), [`decision-ledger`](Skill-Decision-Ledger)
- Loop partners: [`watch`](Skill-Watch), [`did-it-land`](Skill-Did-It-Land)

## Canonical sources

- [SKILL.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/health/SKILL.md)
""",
)

write(
    "Skill-Triage.md",
    banner()
    + f"""# Triage

## What it does

Finds the cause of a known failure and stops there. A cause is established only by an observation that would have come out differently if the cause were something else. Fitting the symptom is not enough.

| Verdict | Meaning |
|---|---|
| `CAUSE` | Observation distinguishes this cause |
| `NARROWED` | Some candidates eliminated; cause not isolated |
| `UNKNOWN` | Could not observe enough |
| `NOT-BROKEN` | Report was wrong; subject within bounds |

## Use it when

- A specific subject is known broken or degraded and the cause is not established.
- A check went red, a deploy failed, a service is unreachable.
- A health readout named something wrong.

## Do not use it when

- You do not yet know whether anything is wrong → [`health`](Skill-Health).
- The cause is already established and you are applying the fix.
- The question is about a change you are making rather than a failure you face.

## Related

- Hands to: [`decision-ledger`](Skill-Decision-Ledger)
- After a fix lands, verify with [`did-it-land`](Skill-Did-It-Land)

## Canonical sources

- [SKILL.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/triage/SKILL.md)
""",
)

write(
    "Skill-Did-It-Land.md",
    banner()
    + f"""# Did-It-Land

## What it does

Answers whether a change is in effect on the thing that actually runs. Writing a control is not installing one. A green check whose oracle only read source does not establish a runtime claim.

| Verdict | Meaning |
|---|---|
| `LANDED` | Observed in effect at the runtime, after the revert window |
| `REVERTED` | Landed, then undone |
| `UNVERIFIED` | Could not observe the runtime — **the default** |

## Use it when

- A deploy, merge, config edit, guard, hook, or migration is believed applied.
- A fix is about to be called done and something depends on that.
- A check is green but its oracle only read source.

## Do not use it when

- The change is local, reversible, and directly observable in the same breath.
- Nothing yet depends on it having landed.
- You are still deciding what to change.

## Related

- Hands to: [`decision-ledger`](Skill-Decision-Ledger)
- Loop partners: [`health`](Skill-Health), [`triage`](Skill-Triage)

## Canonical sources

- [SKILL.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/did-it-land/SKILL.md)
""",
)

write(
    "Skill-Watch.md",
    banner(
        "Post-release corrective work fixed the inert≠installed state machine; "
        "see tagged SKILL.md and successor progress notes."
    )
    + f"""# Watch

## What it does

Specifies and **proves** an external watcher that notices a crossed bound while nobody is looking. The skill is not itself a scheduler, probe, or alerting service.

A watcher that has never fired is not a watcher. `PROVEN` requires explicitly enabling the external mechanism, crossing the bound on purpose, and receiving the alert.

| State | Meaning |
|---|---|
| `DECLARED` | Bound, probe, destination, kill switch written down |
| `INERT` | Mechanism prepared/deployed but deliberately disabled — **not installed** |
| `PROVEN` | Enabled, proof-fired, alert received — the only "installed/watching" state |
| `SUSPECT` | Probe/delivery/proof failed or expired — treated as an alert |

## Use it when

- Something must be noticed between runs.
- First symptom of a condition would otherwise be an outage.
- An existing watcher must be proven to still fire.

## Do not use it when

- You want the current state right now → [`health`](Skill-Health).
- The condition is already known crossed and the cause is wanted → [`triage`](Skill-Triage).
- Nothing would change by learning about it late.

## Related

- Hands to: [`triage`](Skill-Triage), [`decision-ledger`](Skill-Decision-Ledger)

## Canonical sources

- [SKILL.md at {TAG}]({SRC}/plugins/epistemic-skills/skills/watch/SKILL.md)
""",
)

# ---------------------------------------------------------------------------
# Version history (prepend v5; keep prior content from v4 file when present)
# ---------------------------------------------------------------------------

prior_vh = (PAGES / "Version-History.md").read_text(encoding="utf-8")
# Strip old banner and title; keep body from first ## heading of prior file
prior_body = prior_vh
if "# Version History" in prior_body:
    prior_body = prior_body.split("# Version History", 1)[1]
    # drop leading blank lines
    prior_body = prior_body.lstrip("\n")
    if not prior_body.startswith("##"):
        # keep from first ##
        idx = prior_body.find("\n## ")
        prior_body = prior_body[idx + 1 :] if idx >= 0 else prior_body

write(
    "Version-History.md",
    banner(
        f"Canonical release record: [{TAG} release notes]({SRC}/docs/release/RELEASE-5.0.0.md)."
    )
    + f"""# Version History

The Wiki is unversioned navigation over immutable released sources. For exact behavioral contracts, schemas, test results, and install coordinates, use the tagged repository—not this summary.

## v5.0.0 — 2026-08-06 — the loop release

**Breaking. Published**, with gate honesty stated up front:

- Items 4–5 met on the exact tagged commit.
- **Item 6 PARTIALLY MET** (secret scan met; public-content/provenance review was not performed at publication — later remediated on `main`).
- **Item 7** never assessed as a gate row.
- **Item 8 WAIVED / NOT MET** (owner waiver; no publication Gauntlet GO).

Fourteen skills: `metacognate` + thirteen disciplines. Deletes `using-epistemic-skills` and `helix`. Adds the operational loop: `watch`, `health`, `triage`, `did-it-land`.

Post-release independent review: **NO-GO** for retrospective certification. Corrective successor work (issues #104/#105, PR #107) landed on `main` after the immutable tag. Do not move the `v5.0.0` tag.

Sources:

- [RELEASE-5.0.0.md]({SRC}/docs/release/RELEASE-5.0.0.md)
- [Errata]({SRC}/docs/release/RELEASE-5.0.0-ERRATA-2026-08-06.md)
- [Post-release independent review]({SRC}/docs/release/POST-RELEASE-INDEPENDENT-REVIEW-5.0.0-2026-08-06.md)
- [Successor progress]({SRC}/docs/release/SUCCESSOR-PROGRESS-104-105-2026-08-07.md)
- [Design]({SRC}/docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md)

"""
    + prior_body,
)

# ---------------------------------------------------------------------------
# Installation — rewrite from README truth at v5
# ---------------------------------------------------------------------------

write(
    "Installation-and-Harness-Compatibility.md",
    banner(
        f"Prefer immutable `{TAG}` coordinates. `main` is current development and may move ahead of the tag."
    )
    + f"""# Installation and Harness Compatibility

Install exactly **one** copy of the {TAG} skills per harness. The skills have one canonical tree; harness manifests are thin entrypoints. Layering a native plugin and a generic skills install creates duplicate triggers.

## First: stable coordinates and migration

Use immutable `{TAG}` coordinates for stable behavior claims. Existing untagged installs must be replaced rather than layered; then reload the harness or start a new task. Expect **fourteen** skills at {TAG}.

Post-release corrective commits on `main` (after the immutable tag) may include documentation and contract hardening that are not in the annotated tag. Prefer the tag for reproducible installs; prefer `main` only when you intentionally want post-tag corrective work.

## Claude Code

```bash
git clone --depth 1 --branch {TAG} https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-{TAG}
```

```text
/plugin marketplace add /absolute/path/to/epistemic-skills-{TAG}
/plugin install epistemic-skills@epistemic-skills
```

Use one marketplace source only, then start a fresh task.

## Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref {TAG}
codex plugin add epistemic-skills@epistemic-skills
python "$HOME/.codex/plugins/cache/epistemic-skills/epistemic-skills/5.0.0/skills/gauntlet/scripts/render_codex_agents.py" --out "$HOME/.codex/agents"
```

Start a new Codex task after rendering.

## Cursor

The plugin is **not publicly listed**. Use a tagged local checkout or a Cursor Teams/Enterprise team-marketplace import. Verify fourteen skills after reload. Do not also install into `~/.cursor/skills/`.

```bash
git clone --depth 1 --branch {TAG} https://github.com/ZMS-Labs/epistemic-skills.git ./epistemic-skills-{TAG}
cd ./epistemic-skills-{TAG}
test "$(git describe --tags --exact-match)" = "{TAG}"
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/epistemic-skills" ~/.cursor/plugins/local/epistemic-skills
```

## Gemini CLI

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --ref {TAG} --consent
```

Restart and validate. Prefer the tagged install over a mutable development link.

## Antigravity (`agy`)

```bash
git clone --depth 1 --branch {TAG} https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-{TAG}
agy plugin install /path/to/epistemic-skills-{TAG}
agy plugin validate /path/to/epistemic-skills-{TAG}
```

Choose one of native install, Gemini extension link, or `agy plugin import gemini`.

## Kimi Code

```text
/plugins install https://github.com/ZMS-Labs/epistemic-skills/tree/{TAG}
```

Run `/reload` or start a new session.

## Generic Agent Skills harness

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/{TAG}/plugins/epistemic-skills/skills
```

Use only when no native plugin or extension exists. Frontmatter `description` is the trigger; the body is the method.

## Further reading

- [README installation section at {TAG}]({SRC}/README.md#installation-and-compatibility)
- [Cross-Harness Packaging](Cross-Harness-Packaging)
- [Harness verification matrix (successor)]({SRC}/docs/release/HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md)
""",
)

# ---------------------------------------------------------------------------
# Bulk: retarget v4 banners/links; add historical banners to retired pages
# ---------------------------------------------------------------------------

REPLACEMENTS = [
    ("epistemic-skills v4.0.0", f"epistemic-skills {TAG}"),
    ("epistemic-skills v3.0.0", f"epistemic-skills {TAG}"),
    ("epistemic-skills v3.4.0", f"epistemic-skills {TAG}"),
    ("/tree/v4.0.0/", f"/tree/{TAG}/"),
    ("/blob/v4.0.0/", f"/blob/{TAG}/"),
    ("/tree/v3.0.0/", f"/tree/{TAG}/"),
    ("/blob/v3.0.0/", f"/blob/{TAG}/"),
    ("/releases/tag/v4.0.0", f"/releases/tag/{TAG}"),
    ("/releases/tag/v3.0.0", f"/releases/tag/{TAG}"),
    ("branch v4.0.0", f"branch {TAG}"),
    ("--branch v4.0.0", f"--branch {TAG}"),
    ("--ref v4.0.0", f"--ref {TAG}"),
    ("/tree/v4.0.0", f"/tree/{TAG}"),
    ("eleven skills", "fourteen skills"),
    ("Verify eleven skills", "Verify fourteen skills"),
    ("registers eleven skills", "registers fourteen skills"),
    ("exactly eleven skills", "exactly fourteen skills"),
]

HISTORICAL = {
    "Skill-Using-Epistemic-Skills.md": (
        "using-epistemic-skills",
        "metacognate",
        "Deleted in v5.0.0; evaluation corpora preserved at package level.",
    ),
    "Helix-Central-Passage.md": (
        "helix",
        "metacognate (Tier 2 pairing judgment)",
        "Deleted in v5.0.0; pair tables cannot hand control back.",
    ),
    "Skill-Blindspot-Pass.md": (
        "blindspot-pass",
        "recon (brief mode)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Wayfinding.md": (
        "wayfinding",
        "recon (initiative mode)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Applying-Formal-Rigor.md": (
        "applying-formal-rigor",
        "resolve (derivation)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Evidence-Research.md": (
        "evidence-research",
        "resolve (literature)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Throwaway-Prototyping.md": (
        "throwaway-prototyping",
        "resolve (probe)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Continuity-Verify.md": (
        "continuity-verify",
        "decision-ledger (resume mode)",
        "Consolidated in v4.0.0.",
    ),
    "Skill-Intent-Traced-Merge.md": (
        "intent-traced-merge",
        "reference/craft/intent-traced-merge.md",
        "Demoted to craft doctrine in v4.0.0.",
    ),
    "Skill-Agent-Interface-Design.md": (
        "agent-interface-design",
        "reference/craft/agent-interface-design.md",
        "Demoted to craft doctrine in v4.0.0.",
    ),
}

# Pages that are still live skills — strip Helix-as-current language lightly
LIVE_SKILL_PAGES = [
    "Skill-Recon.md",
    "Skill-Resolve.md",
    "Skill-Decision-Ledger.md",
    "Skill-Write-Goal.md",
    "Skill-Outsource.md",
    "Skill-Gauntlet.md",
    "Skill-Evidence-Locked-UAT.md",
    "Skill-Open-Questions.md",
    "Skill-Context-Audit.md",
    "Workflow-Recipes.md",
    "Routine-Work-and-Proportionality.md",
    "Evidence-Status-and-Known-Limitations.md",
    "FAQ-and-Troubleshooting.md",
    "Architecture-and-Contracts.md",
    "Contributing.md",
    "Testing-and-Evaluations.md",
    "Core-Concepts.md",
    "Cross-Harness-Packaging.md",
    "Design-History-and-Audits.md",
    "Glossary.md",
    "Release-Process-and-Versioning.md",
    "Security-Provenance-and-DCO.md",
    "_Footer.md",
]

HELI_X_CURRENT_FIXES = [
    (
        "[Helix: Central Passage](Helix-Central-Passage) places recon",
        "Historical [Helix](Helix-Central-Passage) once placed recon",
    ),
    (
        "Read [Helix: Central Passage](Helix-Central-Passage) for the pairing map",
        "Pairing is now a `metacognate` judgment; historical [Helix](Helix-Central-Passage) documents the deleted seat",
    ),
    (
        "When a workflow-skill layer also runs, [Helix: Central Passage](Helix-Central-Passage)",
        "When a workflow-skill layer also runs, `metacognate` decides pairing; historical [Helix](Helix-Central-Passage)",
    ),
    (
        "`using-epistemic-skills` sequences them",
        "`metacognate` and each member's description govern them",
    ),
    (
        "If more than one positive trigger exists, `using-epistemic-skills` sequences them and defines what each output must hand to the next.",
        "If more than one positive trigger exists, each member's description governs firing; `metacognate` owns the approach question.",
    ),
    (
        "When several observable triggers are present, `using-epistemic-skills` orders the work",
        "When several observable triggers are present, each member's description governs firing",
    ),
    (
        "The router sequences multiple positive triggers",
        "Multiple positive triggers",
    ),
    (
        "a zero-skill task emits no router record",
        "a zero-skill task emits no entry-point record",
    ),
    (
        "Emits no skip inventory and no process-only artifact",
        "Emits no entry-point skip inventory and no process-only artifact",
    ),
]


def bump_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    for a, b in REPLACEMENTS:
        text = text.replace(a, b)
    for a, b in HELI_X_CURRENT_FIXES:
        text = text.replace(a, b)
    if path.name in HISTORICAL:
        retired, survivor, note = HISTORICAL[path.name]
        hb = hist_banner(retired, survivor, note)
        # Remove leading applies-to block if present
        if text.startswith(">"):
            # drop consecutive quote-preamble until blank line after quotes
            lines = text.splitlines()
            i = 0
            while i < len(lines) and (lines[i].startswith(">") or lines[i].strip() == ""):
                if lines[i].strip() == "" and i > 0 and not lines[i - 1].startswith(">"):
                    break
                if lines[i].strip() == "" and i > 0 and lines[i - 1].startswith(">"):
                    i += 1
                    break
                i += 1
            text = "\n".join(lines[i:]).lstrip("\n")
        text = hb + text
    if text != original:
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print(f"bumped {path.name}")


for name in LIVE_SKILL_PAGES + list(HISTORICAL):
    p = PAGES / name
    if p.exists():
        bump_file(p)

# Evidence page: prepend v5 honesty pointer
ev = PAGES / "Evidence-Status-and-Known-Limitations.md"
if ev.exists():
    text = ev.read_text(encoding="utf-8")
    pointer = (
        f"> **{TAG} honesty:** publication item 6 was only PARTIALLY MET; item 8 was "
        f"WAIVED. Read the [errata]({SRC}/docs/release/RELEASE-5.0.0-ERRATA-2026-08-06.md) "
        f"and [post-release independent review]({SRC}/docs/release/POST-RELEASE-INDEPENDENT-REVIEW-5.0.0-2026-08-06.md) "
        f"(NO-GO for retrospective certification) before treating {TAG} as gate-complete.\n"
        f">\n"
        f"> Successor corrective work on `main`: "
        f"[SUCCESSOR-PROGRESS-104-105-2026-08-07.md]({SRC}/docs/release/SUCCESSOR-PROGRESS-104-105-2026-08-07.md).\n\n"
    )
    if "v5.0.0 honesty" not in text:
        # insert after initial banner block
        if text.startswith(">"):
            lines = text.splitlines()
            i = 0
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            text = "\n".join(lines[:i]) + "\n\n" + pointer + "\n".join(lines[i:])
        else:
            text = pointer + text
        ev.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("amended Evidence-Status-and-Known-Limitations.md")

print("done")
