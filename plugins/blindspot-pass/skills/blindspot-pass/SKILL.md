---
name: blindspot-pass
description: Use for pre-dispatch epistemic reconnaissance — surfacing the unknown-unknowns BEFORE committing effort, freezing a review subject, or dispatching work, then rewriting the request in light of what you find. Fires before non-trivial work in unfamiliar territory, before writing plans or dispatching subagents on a fuzzy brief, before locking the subject of an adversarial review, and on explicit request ("blindspot pass", "what am I missing", "find my unknowns", "recon this before we start", "de-risk the dispatch"). Do NOT fire for well-understood reversible work, factual lookups, or tasks whose territory you already hold in context. Provenance: Thariq Shihipar (Anthropic), "A Field Guide to Claude Fable 5: Finding Your Unknowns" (2026-07-03).
---

# Blindspot Pass — find the unknowns before they get expensive

> **The map is not the territory.** A request is a *map*; the codebase and the real
> world are the *territory*. Most expensive failures are territory the map didn't
> show — an unstated constraint, a landmine everyone-who's-been-here knows, a
> question an expert would have asked before touching anything. This skill spends a
> cheap pass finding that territory *before* you commit, and ends by **rewriting the
> request** so the work that follows aims at the real target.
>
> **Provenance:** the technique is from Thariq Shihipar (Anthropic Claude Code team),
> *"A Field Guide to Claude Fable 5: Finding Your Unknowns"* (2026-07-03). Cite the
> essay, not any third-party skill repackaging of it.

## Where this sits (the reflex, not a chore)

| Slot | Skill | What it operates on |
|---|---|---|
| **Before there is a subject** | **blindspot-pass** (this) | a fuzzy *request* → recon → a rewritten, de-risked request |
| Turning idea into design | brainstorming | a request you already understand → a design |
| Reviewing a frozen thing | adversarial review (a red-team / gauntlet pass) | a locked subject → GO/CONDITIONAL/NO-GO |
| Proving work is done | verification-before-completion | a claim → evidence |

Adversarial review is *post-hoc scrutiny of a frozen subject*. Blindspot-pass is
*pre-work reconnaissance* — it fires when there is **not yet a subject to freeze**,
and its output feeds everything downstream. Rigorously reviewing the wrong subject
is rigorous review of a map that doesn't match the territory; this is the guard
against that. Two recurring dispatch failures motivate it: work dispatched using
vocabulary the codebase doesn't actually use, and a prescribed fix whose premise
the code contradicts — both map/territory mismatches caught too late.

## Auto-fire discipline

If you run a skill-triggering harness (e.g. the superpowers plugin), this skill
should self-suggest. It fires when **you are about to commit effort into territory
you do not fully hold in context**:

- **Triggers (consider firing):** a brief that is vague, ambitious, or in an
  unfamiliar codebase/domain; before writing plans or dispatching subagents on a
  non-trivial task; before **locking the subject of an adversarial review**; before
  a multi-agent fan-out where a wrong premise multiplies across agents; when
  the operator says "just build X" and X has hidden surface area.
- **Never fires on:** well-understood reversible work, factual lookups, tasks whose
  territory is already fully in context, or mechanical edits. A blindspot pass on
  work you already understand is ceremony — skip it and say so.
- Always operator-overridable. The pass is **cheap** (one read-heavy reconnaissance
  turn); the failure it prevents is not.

## The one rule

**Do not start implementing. This skill ends at understanding.** If you find
yourself editing files or writing the solution, you have left the skill. The
deliverable is a *rewritten request*, not a change.

## The protocol

1. **Reconnoiter the territory (read, don't write).** Read the actual code / docs /
   data the request touches — not the request's description of them. Find the working
   examples, the constraints already baked in, the seams. Live-verify anything the
   brief *asserts* about the territory (the brief is a map; check it). If the
   environment is degraded (a mount down, a mirror stale), verify the source-of-truth
   before trusting repo facts.

2. **Report in exactly four sections** (this is the format — keep it):
   - **Landmines** — the mistakes someone new to this territory typically makes, plus
     the repo-/domain-specific potholes you can see. Concrete, with file:line where
     it's a code landmine.
   - **Hidden context** — decisions already made that constrain the work (an
     architecture choice, a convention, a prior incident, a dependency's real
     behavior). The things "everyone who's been here" knows and the brief omits.
   - **What good looks like** — 2–3 examples of this pattern *done well* in this
     codebase/domain, so the target is concrete, not abstract.
   - **Questions you should be asking** — the 3–5 questions an expert would ask before
     starting, **each with your current best-guess answer.** (Best-guess answers are
     mandatory: an unanswered question is a deferral; a best-guess is a falsifiable
     claim the operator can correct in one word.)

3. **Rewrite the original request.** End with a rewritten version of the request that
   folds in what you found — the constraints made explicit, the real target named, the
   scope corrected. This rewritten request is what brainstorming / plan-writing /
   adversarial review / the dispatch then consume.

4. **Hand off.** State which downstream skill should run next on the rewritten request
   (usually brainstorming for a design, or straight to adversarial review if the
   rewritten subject is now concrete enough to freeze). If the recon revealed the task
   is ill-posed or the wrong thing to build, say that — the highest-value blindspot
   pass sometimes kills the dispatch.

## Optional close-out bookend — the blast-radius quiz

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

## Anti-patterns (you are rationalizing if you think these)

| Thought | Reality |
|---|---|
| "I basically know this codebase" | Then the pass is 30 seconds and confirms it. Do it, or say why you're skipping. |
| "The request is clear enough" | Clarity of the *map* says nothing about the *territory*. |
| "I'll just start and find out" | Finding out mid-implementation is the expensive path this prevents. |
| "This is just recon, let me also fix the thing I found" | Stop. The skill ends at understanding. Capture the fix as a note; don't act. |
| "I'll list questions without answering them" | An unanswered question is a deferral. Best-guess every one. |
