# Blast-radius quiz — optional close-out bookend

> This is an optional close-out bookend, not part of the core blindspot pass. The
> core pass (SKILL.md) runs *before* work starts; this runs *after*, at merge/close.

The essay's *after* half. Use before merging/closing a non-trivial change when the
operator (or a future you) needs to be sure the change is understood, not just green:

- Produce a short **comprehension report**: what changed, how the changed pieces
  interact, and the mental model needed to maintain it.
- Then a **quiz weighted toward edge cases and blast radius over trivia** — the
  questions whose wrong answers cost the most.
- **Fixed bar, simplify-if-fail:** at most two rounds. If the change can't be
  explained/passed, that is evidence the change is too complex — **simplify the change
  rather than re-quiz the explanation.** The bar tests the artifact, not the student.

This bookends the epistemic arc (find unknowns before → confirm understanding after)
without duplicating capabilities that belong to other skills (brainstorming,
plan-writing, verification-before-completion).
