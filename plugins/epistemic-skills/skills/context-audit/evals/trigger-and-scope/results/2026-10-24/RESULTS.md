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
Muse Wonder). Same model family and harness as epoch 1's subjects is
**not** the case here — epoch 1 (`results/2026-08-04/RESULTS.md`) ran
claude-fable-5 in the Claude Code harness — so epoch-to-epoch
movement mixes a model/harness change with the epoch change and
cannot be read as within-model improvement or as cross-model
replication of either model. (Corrected 2026-10-24: this note
originally asserted the two epochs shared a model family and harness;
see the correction section at the end of this record.)

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
corroborated, not resolved). The 8/14 → 11/14 difference is movement
on the comparable line under an unchanged ruler — fixtures and scorer
are byte-identical to epoch 1 — but it is **not** within-model
improvement: the epochs ran different model families in different
harnesses (see the corrected model note), so the difference mixes the
model/harness change with any epoch effect and is reported
descriptively only.

## Honest limits

N=1 per fixture, single repetition per epoch; the two epochs ran
different model families in different harnesses, so together they do
not estimate a population rate, a trend, or a within-model change.
Declared-response scoring only.

## Correction (2026-10-24, post-epoch)

Review (Codex P2, raised on PR #281's thread against this file)
identified a false statement in this record as originally written:
the model note asserted that epoch 1 and epoch 2 subjects were "the
same model family in the same harness". They were not. The epoch 1
record (`results/2026-08-04/RESULTS.md`) states its subjects ran as
claude-fable-5 in the Claude Code harness; this epoch's subjects ran
as Muse Wonder subagents of the coordinating runtime. The model
note, the Reading's improvement framing, and the Honest limits line
have been corrected above to state the model/harness change and its
consequence: the 8/14 → 11/14 difference mixes that change with the
epoch change and cannot be interpreted as within-model improvement.
The epoch's per-fixture results and FAIL outcome are unchanged. The
correction matches the wording the E12 (outsource) second-epoch
record used for the same confound.
