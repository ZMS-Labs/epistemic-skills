> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released resolve source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/resolve/SKILL.md)
>
> **v4.0.0 consolidation:** resolve consolidated the former applying-formal-rigor, evidence-research, and throwaway-prototyping skills (2026-08-04). Their full methods are the instrument `METHOD.md` files unchanged, with their reference material, evals, and committed epoch results intact in each instrument's subtree. The tagged v4.0.0 sources are the sole contract; this page defers to them where they differ.

# Resolve

## What it does

Resolve settles a live question or material decision with the cheapest sufficient instrument rather than an opinion. The skill owns exactly one decision — **which instrument settles this question at the lowest sufficient cost** — and then hands the work to that instrument's full method. It never renders the downstream verdict itself: a matrix is not a GO, a derivation is not an approval, a probe answer is not a merged feature.

## Instrument selection

Ask, in cost order. Ordinary reading of the artifact is the routine path, not this skill; recon owns territory-mapping; a factual lookup is nobody's trigger.

| Question shape | Instrument | Former skill | Method file |
|---|---|---|---|
| A correctness, complexity, consistency, or measurable-property question with named theory behind it | **derivation** | applying-formal-rigor ([historical guide](Skill-Applying-Formal-Rigor)) | [`derivation/METHOD.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/resolve/derivation/METHOD.md) |
| A scholarly premise, "studies show…", an imminent scholarly-connector call, or citation verification | **literature** | evidence-research ([historical guide](Skill-Evidence-Research)) | [`literature/METHOD.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/resolve/literature/METHOD.md) |
| A disposable build would answer it faster than further derivation, literature, or debate | **probe** | throwaway-prototyping ([historical guide](Skill-Throwaway-Prototyping)) | [`probe/METHOD.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/resolve/probe/METHOD.md) |

Two instruments can fire in sequence: a derivation names an empirical premise, literature qualifies it, and the derivation closes; a probe answers what neither could. Each instrument keeps its own boundary, artifact, and handoff exactly as its `METHOD.md` defines.

## Use it when

- A bounded formal/correctness/complexity question needs settling, a proposed design needs correctness confirmation or reversal, or a ≥2-option design fork is governed by theory (**derivation**).
- A premise rests on "the research says…", a scholarly-connector call is imminent, or citations need verification (**literature**).
- A question is cheaper to answer by building a disposable probe than by more argument, derivation, or reading (**probe**).

## What each instrument produces

- **Derivation** (the applying-formal-rigor method): a focused inline derivation for the lightweight tier, or a revision-bound `formal-rigor-record@2` with P1–P9 coverage and its module registry for standard/high-assurance work.
- **Literature** (the evidence-research method): a claim-evidence matrix built through three-layer discovery/reception/holdings, with degradation stated per unavailable layer — never a GO/NO-GO.
- **Probe** (the throwaway-prototyping method): a recorded probe answer to one pre-registered question, with disposal declared at birth, capture-then-delete, and never a promotion of the build.

## Do not use it when

- The routine bounded check already answers the question.
- The decision is pure preference with no measurable property.
- The purpose is to decorate a decision already made — evidence after a verdict is rationalization.

## Shared invariants

- **The instrument produces evidence; the decision consumes it.** No instrument renders the downstream verdict.
- **Cheapest sufficient wins.** Escalating instruments without a reason is ceremony; a probe that answers in an hour beats a derivation that argues for a day — and vice versa when theory already settles it.
- **Preregistration before result**, in every instrument's own form: prediction before test; matrix before verdict; question before build.

## Related skills and handoffs

- [Recon](Skill-Recon) hands frontier decisions (initiative mode) and probe residues (candidate mode) to resolve's instruments.
- A derivation or matrix becomes input to planning, implementation, review, or [Gauntlet](Skill-Gauntlet); Gauntlet independently attacks it.
- Probe findings land in [Decision Ledger](Skill-Decision-Ledger) as an outcome-shaped entry before the build is disposed.
- [Helix: Central Passage](Helix-Central-Passage) places the derivation instrument inside material design choices, debugging correctness claims, and design-asserting review feedback; the literature instrument cross-cutting at scholarly premises; the probe instrument inside brainstorming.

## Historical guides

[Applying Formal Rigor](Skill-Applying-Formal-Rigor), [Evidence Research](Skill-Evidence-Research), and [Throwaway Prototyping](Skill-Throwaway-Prototyping) are retained as historical guides to the three instrument methods. The instrument `METHOD.md` files at the v4.0.0 tag are the former `SKILL.md` bodies, moved verbatim with git history; committed batteries and epoch results moved with their methods as historical evidence and re-arm per [`docs/policy/EVIDENCE-POLICY.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/policy/EVIDENCE-POLICY.md).

## Canonical sources and evidence

- [Resolve core at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/SKILL.md)
- [Derivation instrument method at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/derivation/METHOD.md)
- [Literature instrument method at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/literature/METHOD.md)
- [Probe instrument method at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/probe/METHOD.md)
- [Record validator at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/derivation/validate_record.py)
- [v4.0.0 release record (consolidation mapping and evidence posture)](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md)
