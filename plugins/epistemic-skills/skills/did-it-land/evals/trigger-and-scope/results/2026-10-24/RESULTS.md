# Live behavioral epoch — 2026-10-24 (E9: did-it-land first epoch)

**Outcome: PASS — 13/13 fixtures pass the deterministic scorer (exit 0).**
This record supersedes `results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/did-it-land/SKILL.md`) plus
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

Actions: verify-landing 9 · no-fire 4. Verdicts among verify rows:
LANDED 4 · UNVERIFIED 4 · REVERTED 1.

- **PASS (13):** every fixture — all four silent no-fire rows; the
  four LANDED rows each resolved the deployed artifact (not the
  source/merge) and cited an observation at the consumer; the
  partial-coverage row (one of three regional consumers observed)
  correctly stayed UNVERIFIED; the two anti-lazy rows (a merge plus
  passing tests with no consumer observation; a CI grep of source
  standing in for the running system) correctly returned UNVERIFIED
  with a null observation rather than upgrading; and the
  observed-then-reverted row correctly reported REVERTED with
  persistence observed.
- **FAIL (0).**

## Holdout line

Holdout fixtures (`config-edit-runtime-loads-cache`,
`nofire-still-deciding-what-to-change`,
`observed-effect-reverted-by-reconciler`): 3/3 pass, reported
separately per the preregistration; no dispatch text was tuned against
them. The config-cache holdout is the sharpest row in the battery: the
subject resolved the artifact to the cached bundle the runtime
actually loads and reported the consumer still serving the old value,
rather than crediting the repository edit.

## Reading (within the preregistered claim fence)

Verdict selection and artifact resolution on declared responses: on
these 13 fixtures, an isolated agent's declared verdicts conformed to
the skill's own trigger text — the verification target was resolved to
the consumer-side artifact and no verdict was upgraded past the
observation available. This supports no claim about verdict accuracy
on live systems or persistence beyond the scenarios' stated facts.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
