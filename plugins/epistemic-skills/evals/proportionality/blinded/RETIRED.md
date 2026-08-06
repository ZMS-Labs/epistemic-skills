# RETIRED 2026-08-06 — the subject no longer exists

**This corpus is evidence, not a live suite. Its results stand. Its harness is gone.**

## What was retired, and what was kept

| Retired | Kept |
|---|---|
| `runner.py` | `README.md` · `arms.json` · `scenarios.json` |
| `tests/run_tests.py` | `prompts/` (all three arms) · the response schema |
| | `results/BLOCKED.md` · `results/RESULTS.md` |

The **experimental design is kept in full** — arms, scenarios, prompts, and
response schema. A design is how a result can be read and challenged; discarding
it would leave the results unfalsifiable. Only the executable harness went.

## Why

This battery measured the **router's** behavior: it assembled prompts from
`using-epistemic-skills/SKILL.md` and its `routine-fast-path.md`, and asserted
properties of the router's enumerated routing content — for example,
*"router must preserve the member-owned single-design formal-rigor trigger"*.

The router seat was **deleted** on 2026-08-06 and replaced by `metacognate`, which
**enumerates nothing**. That is not an accident of the rewrite; it is the property
`metacognate` exists to have, because the router's member list was the single
largest source of the enumeration tax and had already shipped a description naming
two skills that no longer existed (see PR #91).

So the assertions cannot be repointed. Aiming them at `metacognate` would assert
that the new skill preserves member-owned triggers — the exact thing removing the
router was meant to eliminate. A test that demands the defect back is worse than no
test.

## What is NOT being claimed

Retirement does not retire the **finding**. The four-arm campaign's headline result
stands and is still reported in the README:

> **no arm separation** — primary D>A `p=0.875`; A=5 B=4 C=7 D=4 of 18.

Behavioral superiority remains **UNESTABLISHED**. Nothing in the v5.0.0 work
changes that, and a tidier architecture is not evidence that the skills improve
outcomes.

## The rule this follows

**Keep the evidence; retire the machinery whose subject is gone.** A corpus that
measured a deleted thing is a historical record, not a broken test.

Removed from CI in the same change. Recoverable in full from git history.
