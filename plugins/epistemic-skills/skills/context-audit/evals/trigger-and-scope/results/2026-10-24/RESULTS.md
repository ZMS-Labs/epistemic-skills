# Live behavioral epoch — 2026-10-24 (E10: context-audit second epoch)

**Outcome: FAIL — 11/14 fixtures pass the deterministic scorer (exit 1).**
Reported **against** the first-epoch baseline
(`results/2026-08-04/RESULTS.md`, FAIL 8/14), which this record does not
overwrite. Per methodological-review fix F2, the baseline-comparable
line and the v7 scorer-validation line are reported separately below.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/context-audit/SKILL.md`)
plus core-directed references, never anything under `evals/`. The
pinned response contract was quoted from the battery README with
prior-epoch history stripped. Trials were declared simulations; the
shipped `score.py` ran unmodified. Raw extracted responses in
`responses.json`; scorer output in `scorer-report.json`.

Extraction: 14/14 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies — and for a second epoch
it matters doubly: epoch 1 and epoch 2 subjects are the same model
family in the same harness, so epoch-to-epoch movement is not
cross-model replication.

## Results — baseline-comparable line (14 fixtures)

Actions: full-audit 5 · report-only-audit 3 · no-fire 6.

- **PASS (11):** all six no-fire hard negatives stayed silent; the
  full apply row (`explicit-claudemd-audit`) passed with version
  control, apply, and the complete five-class apply order; and three
  of the six first-epoch failures now pass — `explicit-prune-instructions`,
  `model-upgrade-stale-guardrails`, and `keep-gotcha-with-origin`
  (KEEP:GOTCHA with the origin actually read).
- **FAIL (3):**
  - `midtask-layer-conflict` — expected full-audit, got
    report-only-audit. The inner ruling was substantively right (the
    squash-merge conflict located across both layers, CONFLICT class,
    nothing applied). Characterisation: **(a)** conduct — trigger-mode
    selection. This is the same divergence mechanism the first epoch's
    record diagnosed: where a fixture leaves version-control status
    unstated, subjects resolve toward the report-only mode.
  - `governance-projection-conflict` — expected full-audit, got
    report-only-audit (with the conflict correctly routed upstream).
    Characterisation: **(a)** conduct — same mode-selection mechanism.
  - `duplicate-most-local-survives` — the mode failure from epoch 1 is
    fixed (full-audit, DUPLICATE class), but the survivor named was
    "always-loaded system prompt", where the fixture pins the survivor
    to one of the duplicate's locations and expects the most-local
    copy (`tool-description`). The subject kept the always-loaded copy
    instead. Characterisation: **(a)** conduct — wrong survivor
    selected, not merely misnamed.

## v7 scorer-validation line (separate, per F2)

The 4 cases in `v7-cases.json` are **scorer-validation cases, not live
trials**: each ships a canned response that must pass and canned
mutations that must be rejected. They were exercised through the
shipped `tests/run_tests.py`, unmodified: **PASS (exit 0)**. No agent
behaviour is claimed for this line.

## Reading (within the preregistered claim fence)

Against the baseline: 8/14 → 11/14 on the comparable line. The
remaining failures are two recurrences of the epoch-1 mode divergence
on fixtures that leave version control unstated, plus one genuine
survivor-selection error. Nothing here rehabilitates the battery's
known design tension (the epoch-1 record's diagnosis stands and is
corroborated, not resolved); equally, the improvement is real movement
on the comparable line, not a changed ruler — fixtures and scorer are
byte-identical to epoch 1.

## Honest limits

N=1 per fixture, one harness, single repetition per epoch; two epochs
from the same model family do not estimate a population rate or a
trend. Declared-response scoring only.
