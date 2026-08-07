> **Applies to:** epistemic-skills v5.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/skills)
>
> **v5.0.0** is the loop release: fourteen skills (one entry point + thirteen disciplines). The former router and Helix seats are deleted; pairing is a `metacognate` judgment. Post-publication gate honesty: item 6 PARTIALLY MET, item 8 WAIVED — see [Version History](Version-History).

# epistemic-skills handbook

epistemic-skills helps an agent use the least process that can still expose an error capable of changing the action or completion claim. It complements a workflow layer: workflow skills organize how work is done; epistemic skills keep the target, evidence, and claims honest.

## Start from the current release

This handbook is unversioned navigation over the versioned [v5.0.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v5.0.0). It explains the released contracts; the [canonical repository](https://github.com/ZMS-Labs/epistemic-skills) and its versioned sources control if this handbook and a contract differ. The release documents defined behavior and known limits, not universal behavioral superiority or cross-provider generality.

v5.0.0 ships **fourteen** skills: `metacognate` (the only skill you invoke by name) and thirteen disciplines. `using-epistemic-skills` and `helix` were deleted; their evaluation corpora were preserved at package level. The operational loop seats are `watch`, `health`, `triage`, and `did-it-land`. See the [Skill Catalog](Skill-Catalog) and [Version History](Version-History).

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

Use this handbook to navigate. Use immutable v5.0.0 sources to establish released behavior, and label `main` only as current development. Historical evaluations retain their stated scope; see [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations) before treating evidence as a broad guarantee.
