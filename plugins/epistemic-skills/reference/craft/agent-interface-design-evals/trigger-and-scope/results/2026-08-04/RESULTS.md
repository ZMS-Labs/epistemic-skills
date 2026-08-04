# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: PASS — 14/14 fixtures pass the deterministic scorer.** First
fully passing live epoch in the suite. This record supersedes
`results/BLOCKED.md`.

## Methodology

Protocol as in the 2026-08-04 open-questions and context-audit epochs
(claude-fable-5, Claude Code harness, subject-level blinding — expected
actions and trigger labels withheld; subjects read exactly SKILL.md, evals/
forbidden; shipped score.py unmodified; N=1), with one disclosed
divergence: **fixtures were batched seven-per-subagent (two subagents),
not one-per-agent.** Each batch was instructed to reason fresh per trial,
but trials within a batch share a context window, so within-batch
contamination (set-level answer patterns) is possible in a way the fully
isolated epochs exclude. Batch 1 held the six engage fixtures + one hard
negative; batch 2 held five hard negatives + the two state fixtures.
Preregistration (before scoring): 14/14 PASS — confirmed.

## Results

engage 6 · no-fire 6 · consumer-gate 1 · example-lint 1; zero failures.
Every engage reported the method's structure-first rule and cold-consumer
test; every hard negative stayed silent, with the two excluded crossings
correctly routed (`write-goal/outsource`, `context-audit`); the failed
cold-consumer gate chose a structural fix naming the failing parameter
with the transcript kept; the example-lint justified the one example with
a real weaker-consumer audience and deleted the two whose content
structure already carries, each with its named structural replacement.

## Honest limits

Smoke-scale, N=1, one model/harness, same model family throughout. The
batched dispatch weakens per-trial isolation relative to the sibling
epochs — a passing result under batching is not stronger than one under
isolation, and any future failing epoch should re-run isolated before
diagnosis. A PASS here certifies trigger/scope conformance on these 14
scenarios, not interface-design quality.
