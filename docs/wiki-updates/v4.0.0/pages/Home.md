> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical source:** [released source](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills)

# epistemic-skills handbook

epistemic-skills helps an agent use the least process that can still expose an error capable of changing the action or completion claim. It complements a workflow layer: workflow skills organize how work is done; epistemic skills keep the target, evidence, and claims honest.

## Start from the current release

This handbook is unversioned navigation over the versioned [v4.0.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v4.0.0). It explains the released contracts; the [canonical repository](https://github.com/ZMS-Labs/epistemic-skills) and its versioned sources control if this handbook and a contract differ. The release documents defined behavior and known limits, not universal behavioral superiority or cross-provider generality.

v4.0.0 is the consolidation release: eleven skills — the `using-epistemic-skills` router, `helix`, and nine disciplines. Several v3.x skill names now live on as mode/instrument vocabulary inside `recon`, `resolve`, and `decision-ledger`; the [Skill Catalog](Skill-Catalog) carries the full v3.x → v4.0.0 mapping and [Version History](Version-History) the release summary.

| Use the skills | Start with |
|---|---|
| New to the collection | [Start Here](Start-Here) |
| Need the right amount of process | [Routine Work and Proportionality](Routine-Work-and-Proportionality) |
| Need to decide what fires | [Choosing a Skill](Choosing-a-Skill) |
| Running workflow and epistemic layers together | [Helix: Central Passage](Helix-Central-Passage) |
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

Start with the routine gate. Work stays routine only when it is reversible, local, directly checkable, and non-precedential. Make that change and run its bounded check; do not create a router record, a Helix skip inventory, or process-only evidence to say nothing happened. See [Routine Work and Proportionality](Routine-Work-and-Proportionality).

When a real trigger remains, read `using-epistemic-skills`: it is the router that selects and orders the epistemic discipline(s), then defines the handoff between them.

## The central passage

When a workflow-skill layer is active too, Helix is the passage that pairs its stages with positively triggered epistemic disciplines:

```text
workflow skills  <->  Helix central passage  <->  epistemic router and disciplines
```

Helix does not replace the routine exit or route within the epistemic collection. Read [Helix: Central Passage](Helix-Central-Passage) for the pairing map and [Choosing a Skill](Choosing-a-Skill) for the decision boundary.

## A compact arc

`decision-ledger`'s resume mode (the former `continuity-verify`) re-anchors a genuine resumption; the routine path exits before the arc. For work with positive triggers, the router can sequence recon, decision, evidence, an explicit goal contract, a gate, and proof. `decision-ledger` persists qualifying consequential moments; `outsource` governs execution boundaries. [The Epistemic Arc](The-Epistemic-Arc) shows the handoffs, and [Core Concepts](Core-Concepts) defines the shared safeguards.

## Source of truth

Use this handbook to navigate. Use immutable v4.0.0 sources to establish released behavior, and label `main` only as current development. Historical evaluations retain their stated scope; see [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations) before treating evidence as a broad guarantee.
