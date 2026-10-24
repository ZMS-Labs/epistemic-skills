# Live behavioral epoch — 2026-10-24 (E12: outsource second epoch)

**Outcome: FAIL — full battery 13/18; baseline-comparable line 11/14
against the first epoch's 12/14 (FAIL).** The first-epoch record
(`results/2026-08-04/RESULTS.md`) is not overwritten. This epoch's
reading rule, recorded here as preregistered for E12: fixtures.json at
HEAD carries 18 pinned fixtures (v7.3 added 4 after epoch 1 ran 14), so
all 18 ran live and two lines are reported — the full battery and the
baseline-comparable line over epoch 1's 14 fixture ids — plus the
4 new fixtures as their own line.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/outsource/SKILL.md`) plus
core-directed references, never anything under `evals/`. The pinned
response contract was quoted from the battery README with prior-epoch
history stripped. Trials were declared simulations; the shipped
`score.py` ran unmodified. Raw extracted responses in
`responses.json`; scorer output in `scorer-report.json`.

Extraction: 18/18 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). Same model family and harness as epoch 1's subjects is
**not** the case here — epoch 1 ran claude-fable-5 — so epoch-to-epoch
movement mixes a model change with everything else and is reported
descriptively, not as a trend.

## Results

Actions: publish-packet 7 · transfer-packet 1 · verify-relay 1 ·
verify-acceptance 2 · report-blocked 3 · no-fire 4. All publish rows
reported packet-before-prompt ordering with pointer prompts and no
pasted context; all three blocks named a single blocker and emitted no
prompt; all four no-fire rows stayed silent.

**FAIL (5 fixtures):**

- `capable-target-preflight-fires` — preflight ran and verified the
  capabilities, but named them `runnable-test-shell`,
  `authenticated-github-mutation`, `isolated-execution-contexts`
  where the scorer pins `test-shell`, `github-mutation`,
  `isolated-context`. **(b)** reporting shape over correct conduct.
- `readonly-target-preflight-blocked-state` — the block and the
  failed-capability set were substantively right, named in the
  subject's own words (`shell`, `test-execution`, `branch-commit-push`,
  …) instead of the pinned ids. **(b)**.
- `relay-claim-verified-state` — every relayed claim was checked and
  the reply stored verbatim, but the tests claim was recorded as
  `all-tests-pass` where the fixture pins `tests-pass`. **(b)**.
- `acceptance-gap-state` *(new in v7.3)* — the read-back gap was
  surfaced and the packet amended, recorded as
  `weekly-dependency-bump-check` where the fixture pins
  `dependency-bump-check`. **(b)**.
- `custody-acceptance-state` *(new in v7.3)* — acceptance was read
  back and verified, but the response declares no custody state
  transition: the scorer requires state TRANSFERRED, divestiture
  completing the transfer (a still-running watcher is an obligation
  still owned), and origin residual NONE; none of the three appears.
  **(a)** conduct — the acceptance-verification step ran, the
  state-machine completion the fixture pins did not.

## The two lines

- **Baseline-comparable (epoch 1's 14 ids): 11/14.** Epoch 1 scored
  12/14 with exactly two failures — the two preflight naming rows.
  Both recurred here by the identical mechanism, and
  `relay-claim-verified-state` (passed in epoch 1) joined the same
  defect class. The epoch-1 record diagnosed this as the
  reporting-vocabulary failure mode (issue #77): the canonical bare ids
  live in the battery README while scenarios and SKILL.md speak prose.
  This epoch corroborates the diagnosis from the other side — even
  with the README contract pinned into dispatch, subjects paraphrased
  the ids from the scenario prose. The fix belongs in the shared
  response-contract work, not in retrying epochs.
- **New v7.3 fixtures (4): 2/4** — `full-custody-handover-fires` and
  `bounded-delegation-stays-delegate` pass; `acceptance-gap-state` (b)
  and `custody-acceptance-state` (a) fail as detailed above.

## Reading (within the preregistered claim fence)

Trigger and ordering discipline held across all 18 rows — no
over-firing, no pasted context, no prompt before packet, no unverified
relay trusted. What failed is narrower: pinned-vocabulary fidelity in
four rows and one custody state completion. Against the baseline the
comparable line moved 12/14 → 11/14, entirely within the defect class
epoch 1 already named.

## Honest limits

N=1 per fixture, one harness, single repetition per epoch; the two
epochs differ in subject model family, so the comparison is
descriptive. Declared-response scoring only.
