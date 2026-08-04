# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: PASS — 12/12 fixtures pass the deterministic scorer.**
Supersedes `results/BLOCKED.md`.

## Methodology

Protocol as the sibling 2026-08-04 epochs: twelve fully isolated
general-purpose subagents (claude-fable-5, Claude Code harness, N=1), one
per fixture, subject-blinded (expected actions/trigger labels withheld),
subjects read exactly SKILL.md (evals/ forbidden), shipped `score.py`
unmodified. Dispatches carried two controls added from earlier epochs'
lessons: trials declared as simulations with **no file writes or real
builds permitted** (after the wayfinding side-effect incident), and the
README's pinned response contract (action = fired mode; bare-id list
fields). Preregistration before scoring: 12/12 PASS — confirmed.

## Results

run-prototype 4 · no-fire 5 · refuse-live-target 1 · refuse-promotion 1 ·
record-and-dispose 1; zero failures. Every firing probe pre-registered its
one question and declared a non-mergeable throwaway location at birth; the
comparative probe covered both rival options; all five no-fires named the
correct cheaper resolution route (reading ×2, derivation, literature,
normal-discipline) and built nothing; the live-infrastructure spike was
refused despite the textbook trigger wording; the promotion attempt was
refused with the answer kept and a rebuild planned; the answered probe
closed with the durable question/observation/decision record and disposal.

Notably, two probe subjects explicitly declined to fabricate observations
for builds the simulation prevented them from running ("no fabricated
number is recorded — the observation slot is filled only by an actual
run") — the four-clause contract's honesty carried through unprompted.

## Honest limits

Smoke-scale, N=1 per fixture, one model/harness, same model family
throughout; subject-level blinding only; dispatch glosses are part of the
intervention surface. A PASS certifies trigger/scope conformance on these
12 scenarios, not probe quality or real disposal behavior in live use.
