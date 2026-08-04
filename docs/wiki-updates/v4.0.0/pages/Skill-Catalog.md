> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills)

# Skill Catalog

The released package has exactly eleven skills: the epistemic router, Helix, and nine disciplines. Descriptions below summarize released triggers; the linked guide and tagged `SKILL.md` control.

| Skill | Entry trigger | Purpose | Output | Guide |
|---|---|---|---|---|
| `using-epistemic-skills` | Non-routine work that may need more than one discipline, ordering, external crossing, or resumption | Applies the routine gate and routes positive epistemic triggers | Routing/handoff path; routine exit is record-free | [Guide](Skill-Using-Epistemic-Skills) |
| `helix` | Workflow layer plus epistemic collection, non-routine task, and a positive pairing trigger; external crossing; ambiguous sequencing | Central passage pairing workflow stages to epistemic members | Member artifact plus fired/overridden `helix-check` where applicable | [Guide](Helix-Central-Passage) |
| `recon` | Territory must be mapped before effort commits: a fuzzy/contradicted brief, a large foggy effort, or an external project overlapping your own (three modes: brief / initiative / candidate) | Read, decompose, or harvest — understanding only, never a change | Rewritten request; decision map + fog-free tickets; or harvest record with per-level spend decisions | [Guide](Skill-Recon) |
| `resolve` | A live question or material decision needs an instrument, not an opinion (three instruments: derivation / literature / probe) | Settle it with the cheapest sufficient instrument; the instrument produces evidence, never the downstream verdict | Derivation or `formal-rigor-record@2`; claim-evidence matrix; or recorded probe answer with the build disposed | [Guide](Skill-Resolve) |
| `write-goal` | Explicit request to author/start/refine a durable goal or completion contract | Bind intent to proof, scope, blockers, and stop rule | Approved goal contract | [Guide](Skill-Write-Goal) |
| `decision-ledger` | Uncovered consequential decision, assumption, or recurrent correction needs durable reuse; a ledgered decision's outcome arrives; resumption depends on remembered state (resume mode, pre-arc) | Persist only what an adequate durable artifact does not already carry; re-anchor remembered state before resumed work | Reused durable artifact or `ledger-entry@1`; verified state digest on resumption; never a verdict | [Guide](Skill-Decision-Ledger) |
| `outsource` | Durable handoff to external model, agent, or process | Create and publish a complete repo-backed handoff | Exact-ref packet/pointer, or `BLOCKED` | [Guide](Skill-Outsource) |
| `gauntlet` | High-stakes/irreversible decision, risky pre-merge, or high-stakes hard-to-verify claim | Multi-lens adversarial gate on a frozen subject | Conflict Ledger and computed GO/CONDITIONAL/NO-GO | [Guide](Skill-Gauntlet) |
| `evidence-locked-uat` | Material UI acceptance claim or explicit UAT request | Blinded acceptance from evidence | Deterministic verdict and packet; `INCONCLUSIVE` stays inconclusive | [Guide](Skill-Evidence-Locked-UAT) |
| `open-questions` | Operator asks an exhaustive one-by-one interview; un-best-guessable irreversible fork with operator present | Walk an append-allowed question ledger to empty | Emptied-or-parked ledger + 4-field stamp | [Guide](Skill-Open-Questions) |
| `context-audit` | Explicit audit request; detected cross-layer instruction conflict; model-generation upgrade | Audit the assembled instruction context for conflicts, duplicates, and dead weight | Cut list as diff, conflict ledger, re-baseline watch; operator-gated apply | [Guide](Skill-Context-Audit) |

**Craft doctrine (not disciplines):** intent-traced-merge and agent-interface-design are preserved as reference doctrine at [`plugins/epistemic-skills/reference/craft/`](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/reference/craft), with their archived batteries and epoch results — workflow/craft methods, not epistemic moment disciplines, and no longer routed.

## Consolidated names (v3.x → v4.0.0)

Every absorbed method survives verbatim (mode/instrument files are the former `SKILL.md` bodies, moved with git history); every old name survives as mode/instrument vocabulary. The linked historical guides remain readable; the tagged v4.0.0 sources are the sole contract.

| v3.x skill | v4.0.0 home | Historical guide |
|---|---|---|
| `blindspot-pass` | `recon` — brief mode | [Blindspot Pass](Skill-Blindspot-Pass) |
| `wayfinding` | `recon` — initiative mode | [Wayfinding](Skill-Wayfinding) |
| `harvest-before-adopt` | `recon` — candidate mode | covered in the [Recon guide](Skill-Recon) (no prior wiki page) |
| `applying-formal-rigor` | `resolve` — derivation instrument | [Applying Formal Rigor](Skill-Applying-Formal-Rigor) |
| `evidence-research` | `resolve` — literature instrument | [Evidence Research](Skill-Evidence-Research) |
| `throwaway-prototyping` | `resolve` — probe instrument | [Throwaway Prototyping](Skill-Throwaway-Prototyping) |
| `continuity-verify` | `decision-ledger` — resume mode (pre-arc) | [Continuity Verify](Skill-Continuity-Verify) |
| `intent-traced-merge` | reference craft doctrine (`reference/craft/`) | [Intent-Traced Merge](Skill-Intent-Traced-Merge) |
| `agent-interface-design` | reference craft doctrine (`reference/craft/`) | [Agent Interface Design](Skill-Agent-Interface-Design) |

Routine work is not a twelfth skill. It exits after a bounded check when it is reversible, local, directly checkable, and non-precedential. [Choosing a Skill](Choosing-a-Skill) and [Workflow Recipes](Workflow-Recipes) provide task-first routes.
