---
name: resolve
description: 'Use when a live question or material decision must be settled by evidence rather than assertion, and the choice of instrument matters: a bounded formal/correctness/complexity question, when a proposed design needs correctness confirmation or reversal, or a >=2-option design fork governed by theory (derivation); a premise resting on "the research says…", an imminent scholarly-connector call, or a citation-verification request (literature); or a question cheaper to answer by building a disposable probe than by more argument, derivation, or reading (probe). Do NOT fire when the routine bounded check already answers it, when the decision is pure preference with no measurable property, or to decorate a decision already made.'
---

# resolve — settle the question with the cheapest sufficient instrument

A live question deserves an instrument, not an opinion. This skill owns one
decision — **which instrument settles this question at the lowest sufficient
cost** — and then hands the work to that instrument's full method. It never
renders the downstream verdict itself.

## Instrument selection (the only routing this core does)

Ask, in cost order:

1. **Can reading settle it?** Ordinary reading of the artifact is the routine
   path, not this skill. (recon owns territory-mapping; a factual lookup is
   nobody's trigger.)
2. **Is it theory-governed?** A correctness, complexity, consistency, or
   measurable-property question with named theory behind it →
   **derivation** — read and follow [`derivation/METHOD.md`](derivation/METHOD.md)
   (the applying-formal-rigor method: focused inline tier, or a
   standard/high-assurance `formal-rigor-record@2` with P1–P9 coverage and
   its module registry).
3. **Does it rest on published research?** A scholarly premise, "studies
   show…", an imminent scholarly-connector call, or citation verification →
   **literature** — read and follow [`literature/METHOD.md`](literature/METHOD.md)
   (the evidence-research method: three-layer discovery/reception/holdings,
   claim-evidence matrix, never a GO/NO-GO).
4. **Is building cheaper than arguing?** A disposable build would answer it
   faster than further derivation, literature, or debate → **probe** — read
   and follow [`probe/METHOD.md`](probe/METHOD.md) (the throwaway-prototyping
   method: pre-registered question, disposal declared at birth,
   capture-then-delete, never promote).

Two instruments can fire in sequence (a derivation names an empirical
premise → literature qualifies it → the derivation closes; a probe answers
what neither could). Each instrument keeps its own boundary, artifact, and
handoff exactly as its METHOD.md defines.

## Shared invariants (all instruments)

- **The instrument produces evidence; the decision consumes it.** No
  instrument renders the downstream verdict — a matrix is not a GO, a
  derivation is not an approval, a probe answer is not a merged feature.
- **Cheapest sufficient wins.** Escalating instruments without a reason is
  ceremony; a probe that answers in an hour beats a derivation that argues
  for a day — and vice versa when theory already settles it.
- **Preregistration before result**, in every instrument's own form
  (prediction before test; matrix before verdict; question before build).

## Historical note

resolve consolidated the applying-formal-rigor, evidence-research, and
throwaway-prototyping skills (v4.0.0, 2026-08-04); their full methods are
the instrument METHOD.md files unchanged, with their reference material,
evals, and committed epoch results intact in each instrument's subtree
(evidence re-arms per `docs/policy/EVIDENCE-POLICY.md`).
