> **Applies to:** epistemic-skills v5.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/skills)

# Skill Catalog

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

**Craft doctrine (not disciplines):** intent-traced-merge and agent-interface-design live under [`plugins/epistemic-skills/reference/craft/`](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/reference/craft) (v4.0.0 demotion).

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
