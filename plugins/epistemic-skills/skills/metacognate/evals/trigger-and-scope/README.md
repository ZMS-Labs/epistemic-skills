# metacognate trigger-and-scope fixtures

This battery tests Metacognate's trigger discipline and examination scope:
evidence conflicting with an assertion, a proxy about to stand for success,
confidence outrunning its basis, an uncertain assumption that could change
what to do, an explicit reflection request, and a settled choice whose basis
has changed each fire an examination; a sound approach that survives
examination is retained, because reflection that changes nothing is a valid
fire. Routine directly checkable work never fires; a settled user choice
with no new evidence is not reopened; the mere arrival of a resume or a
consequential stage with a certain basis does not warrant reflection; a
request to reconstruct context that is already available in the task is a
cue to investigate, not a reflection trigger; and no report is filed for a
method that did not apply. Over-firing and under-firing are defects, not
extra rigor.

## Claim

A live-epoch pass on this battery would support exactly one claim: that the
subject's declared fire/no-fire decisions, and the shape of its declared
examinations, conform to the skill's applicability rules on these fixtures.
It would NOT support any claim that applying Metacognate — reflecting on an
approach, assumption or confidence level — improves task outcomes, decisions
or correctness in deployment; no outcome comparison is measured here.
Because the contract scored here is defined by this battery (see the
contract section below), results from this battery must always be reported
as conformance to that battery-defined contract — never as evidence about
the skill as written.

## Pinned expectations

Seven of the eight `examine` fixtures pin `expected_verdict`, and the
scorer enforces it. One fire is shape-only by design:
`explicit-reflection-request-pricing`. Its scenario asks for the reflection
itself but supplies no facts about the pricing reasoning's basis, so no
verdict follows from the scenario — any of the four verdicts could be the
honest outcome of examining it, and only the examination's shape (the four
fields, verdict in vocabulary) is scored there.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior).

Metacognate's `SKILL.md` carries **no verdict vocabulary**: it names no
closed set of reflection outcomes. The vocabulary below is therefore defined
by this battery as the minimal observable output contract a live epoch needs
in order to score reflection at all — it is a battery invention, not a
quotation from the skill. Adopting this vocabulary, or any verdict
vocabulary, into the skill text itself is a separate proposed change and is
NOT made here; this battery does not edit `SKILL.md`.

**Amendment (2026-10-25).** The separate proposed change described
above has since been made — by the skill's own change process, not by
this battery: per Zach's P1 decision (2026-10-25), the contract below
was adopted into metacognate's `SKILL.md` as its output section
(§"Output: the declared outcome"), including the boundary rules the
E2 epoch's failed seams taught. The paragraph above stands as the
record of the position before adoption and is not rewritten. What
the amendment changes is the frame for reading results: epochs run
**before** the adoption (including E2) measured conformance to this
battery-defined contract only, and are still reported that way;
epochs run **after** it measure the skill as written, because the
contract is now the skill's own text. One cost is recorded plainly:
the adoption burns this battery's three marked holdout fixtures —
`proxy-signups-stand-for-retention`,
`sound-approach-survives-challenge`, and
`settled-choice-no-new-evidence` — whose scenarios are now answered
by skill text their subjects may read; replacement holdouts must be
authored by a non-editor and stay sealed until their epoch runs
(the sealed-holdout rule adopted 2026-10-25). The adoption packet is
`wo3-adoption-packet.md` in the evidence program's Phase 2 files.

- `action` names the **discipline mode that fired**: `examine` (the
  approach, assumptions, evidence, confidence or success criteria were
  actually examined) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` and
  nothing else. The examination fields — `outcome_named`,
  `decisive_assumption`, `discriminating_observation`, `verdict` — are
  absent, not false; silence means their keys are not present at all.
  Absence is not an artifact, no report is required for a method that did
  not apply, and a subject must not explain why it did not fire.
- An `examine` response reports `outcome_named` as a nonempty string naming
  the actual outcome the user needs, distinguished from any convenient
  proxy that might stand for it.
- An `examine` response reports `decisive_assumption` as a nonempty string
  naming the assumption doing real work in the current approach — the one
  whose failure would change the conclusion or what to do.
- An `examine` response reports `discriminating_observation` as a nonempty
  string naming what observation would show the approach wrong: the check
  proposed must exercise the behaviour asserted.
- An `examine` response reports `verdict` as exactly one of:
  `approach-retained` (the existing approach was examined and is adequate —
  reflection changed nothing), `approach-corrected` (the approach or its
  check was corrected), `question-reframed` (the question or success
  criterion itself was the defect, typically a proxy standing for the
  outcome), or `confidence-recalibrated` (the approach stands but the
  stated confidence was brought back to what its basis supports). Where a
  fixture carries `expected_verdict`, `verdict` must equal it.
- Responses are declarative reports of the examination that would occur:
  the trial is a simulation, and no response here requires an actual side
  effect beyond the declared fields above.

This battery is unrun as of 2026-10-24: no live epoch has run against it and
no behavioural result exists for it. Three fixtures are marked `holdout`
(`proxy-signups-stand-for-retention`, `sound-approach-survives-challenge`,
`settled-choice-no-new-evidence`); epoch runners must not tune against the
holdout fixtures.

Run `python tests/run_tests.py`.
