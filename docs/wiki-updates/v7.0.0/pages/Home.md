> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)
>
> **v7.0.0** ships **fifteen** skills: `metacognate` (the only skill you invoke by
> name) and fourteen disciplines. The skill surface did not grow from v6.0.0 — the
> major version marks two published schemas tightened in place at their existing
> contract versions, which is what makes it incompatible rather than minor.
> Triggers, routing and the catalog are unchanged.
>
> **v6.0.0 is an exception release.** Four independent publication reviews across
> three model families all returned NO-GO, and the owner published anyway under a
> recorded exception. Every NO-GO was about the release *process*, not the shipped
> skills. Read [Version History](Version-History) before citing this release's
> assurance posture.

# epistemic-skills handbook

epistemic-skills helps an agent use the least process that can still expose an
error capable of changing the action or completion claim. It complements a
workflow layer: workflow skills organize how work is done; epistemic skills keep
the target, evidence, and claims honest.

## Start from the current release

This handbook describes **v7.0.0**. Until that tag is published, the release to
install is
[v6.0.0](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v6.0.0), and
every source link on these pages points at it for the same reason: a link to an
unpublished tag is a 404, not a coordinate.
It explains the released contracts; the
[canonical repository](https://github.com/ZMS-Labs/epistemic-skills) and its
versioned sources control if this handbook and a contract differ. The release
documents defined behavior and known limits, not universal behavioral
superiority or cross-provider generality.

The operational loop seats are `watch`, `health`, `triage`, and `did-it-land`.
`manifest` custodies mission-shaped work. See the
[Skill Catalog](Skill-Catalog) and [Version History](Version-History).

| Use the skills | Start with |
|---|---|
| New to the collection | [Start Here](Start-Here) |
| Need the right amount of process | [Routine Work and Proportionality](Routine-Work-and-Proportionality) |
| Need to decide what fires | [Choosing a Skill](Choosing-a-Skill) |
| Need the entry-point contract | [metacognate](Skill-Metacognate) |
| Need the whole sequence | [The Epistemic Arc](The-Epistemic-Arc) |
| Need mission custody | [manifest](Skill-Manifest) |
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

Start with the routine gate. Work stays routine only when it is reversible,
local, directly checkable, and non-precedential. Make that change and run its
bounded check; do not invent an entry-point record or process-only evidence to
say nothing happened. See
[Routine Work and Proportionality](Routine-Work-and-Proportionality).

When the approach itself is uncertain, a claim is about to bear load, an
observation contradicts a tool, or work resumes from a summary, invoke
**`metacognate`**. It applies the routine gate first; **silence is a success
state**. Every other member fires on its own description. See
[metacognate](Skill-Metacognate) and [Choosing a Skill](Choosing-a-Skill).

## Pairing with a workflow layer

When a workflow-skill layer (such as superpowers) is also active, pairing is a
judgment `metacognate` makes at the moment it is needed — not a separate seat and
not a stage-to-skill table. Either strand may interrupt the other; control
returns to the point of interruption. The historical
[Helix](Helix-Central-Passage) page documents the deleted pair-table seat.

## A compact arc

`decision-ledger` resume mode re-anchors a genuine resumption; the routine path
exits before the arc. For non-routine work, `metacognate` names the unanswerable
condition and the discipline it implies. The operational loop is watch → health →
triage → did-it-land. Recon, resolve, goal, gate, and proof remain
trigger-dependent handoffs; `manifest` custodies work that must survive
interruption. [The Epistemic Arc](The-Epistemic-Arc) shows the handoffs;
[Core Concepts](Core-Concepts) defines the shared safeguards.

## Source of truth

Use this handbook to navigate. Use immutable v6.0.0 sources to establish released
behavior, and label `main` only as current development. Historical evaluations
retain their stated scope; see
[Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations)
before treating evidence as a broad guarantee.
