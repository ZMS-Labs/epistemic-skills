# Decision Ledger proportionality fixtures

This battery tests the persistence boundary: routine no-op, reuse of an adequate durable
artifact, creation for an uncovered consequential decision, and recurrent correction with
the required failure chain. Duplicate stores are a defect, not extra rigor.

Run `python tests/run_tests.py`.

## Synthetic resume and outcome cases

`continuity-fixtures.json` and `examples/continuity-balanced.json` extend this runner
with interrupted authorized repair, relevant revision drift, preserved prior answers
and authority, original predictions versus outcomes, and ADR reuse without false
resumption/JSONL-validation claims. Negative mutations must fail. These synthetic
records test scorer discrimination; they are not blinded agent trials or evidence of
behavioral improvement. Historical resume-fixture results retain their prior scope.
