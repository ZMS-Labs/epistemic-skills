# Live behavioral epoch — 2026-10-24 (E2: metacognate first epoch)

**Outcome: FAIL — 11/13 fixtures pass the deterministic scorer (exit 1).**
Two named failures, recorded as-is; no re-run. This record supersedes
`results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/metacognate/SKILL.md`) plus
core-directed references, never anything under `evals/`. The pinned
response contract was quoted from the battery README with prior-epoch
history stripped (this battery had no prior epoch). Trials were
declared simulations; the shipped `score.py` ran unmodified. Raw
extracted responses in `responses.json`; scorer output in
`scorer-report.json`.

Extraction: 13/13 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies.

## Results

Actions: examine 9 · no-fire 4.

- **PASS (11):** all three holdouts and eight further rows, including
  the settled-choice-no-new-evidence no-fire and the
  sound-approach-survives-challenge `approach-retained` verdict.
- **FAIL (2):**
  - `evidence-conflicts-migration-assertion` — expected verdict
    `approach-corrected`, got `question-reframed`. Characterisation:
    **(a) conduct.** The subject fired correctly and produced every
    contract field with substantive content; the divergence is the
    verdict selection itself, which is the disciplined judgement this
    battery's contract scores, not a reporting-shape error.
  - `reconstruct-context-available-in-task` — expected `no-fire`, got
    `examine`. Characterisation: **(a) conduct** (over-firing). The
    subject examined a task whose governing criteria were already
    present in context; its own discriminating observation ("read the
    brief and find the criteria there") describes the no-fire path it
    did not take.

## Holdout line

Holdout fixtures (`proxy-signups-stand-for-retention`,
`settled-choice-no-new-evidence`, `sound-approach-survives-challenge`):
3/3 pass, reported separately per the preregistration; no dispatch text
was tuned against them.

## Reading (within the preregistered claim fence — binding constraint)

Per the methodological review's binding constraint, this result is
reported strictly as **conformance to the battery-defined observable
contract**: on 11 of 13 fixtures, an isolated agent's declared
examine/no-fire decisions and verdicts conformed to that contract. It
is **not** evidence about the metacognate skill as written, and must
never be quoted as such; dropping that qualifier reverts this skill's
evidence grade to NONE.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
