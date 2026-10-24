# Live behavioral epoch — 2026-10-24 (E3: perspective first epoch)

**Outcome: FAIL — 12/13 fixtures pass the deterministic scorer (exit 1).**
One named failure, recorded as-is; no re-run. This record supersedes
`results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/perspective/SKILL.md`) plus
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

Actions: apply-lens 7 · no-fire 6.

- **PASS (12):** all three holdouts and nine further rows, including
  all six silent no-fire rows (the gauntlet-adjudication boundary held:
  no lens response smuggled in an adjudication or a GO verdict) and the
  bounded three-lens row with no adjudication fields.
- **FAIL (1):**
  - `metric-fitness-lens-fires` — expected finding `adjustment`, got
    `remaining-uncertainty`. Characterisation: **(a) conduct.** The
    subject fired, named a lens, and bounded the question as the
    contract requires; the divergence is the finding value itself —
    the substantive output the battery-defined contract scores — not a
    reporting-shape error.

## Holdout line

Holdout fixtures (`evidence-unavailable-limit-fires`,
`gauntlet-adjudication-no-fire`,
`several-lenses-bounded-no-adjudication`): 3/3 pass, reported
separately per the preregistration; no dispatch text was tuned against
them.

## Reading (within the preregistered claim fence — binding constraint)

Per the methodological review's binding constraint, this result is
reported strictly as **conformance to the battery-defined observable
contract**: on 12 of 13 fixtures, an isolated agent's declared
apply-lens/no-fire decisions and findings conformed to that contract.
It is **not** evidence about the perspective skill as written, and
must never be quoted as such; dropping that qualifier reverts this
skill's evidence grade to NONE.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
