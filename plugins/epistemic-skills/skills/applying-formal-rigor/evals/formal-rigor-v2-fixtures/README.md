# applying-formal-rigor v2 blinded fixtures

This directory implements Phase B of the approved v2 design. It is a blinded conformance
smoke check, not a population measurement or truth oracle.

- `fixtures/<id>/scenario.md` and `artifacts/` are run-agent visible.
- `ground-truth.json`, `score.py`, thresholds, and other results are scorer-only.
- the two schemas close the public response and v2 record vocabularies;
- `semantic-adjudication.md` owns independent derivation judgment;
- `results/` records immutable identities, hashes, dissent, and coverage limits.

Run `python tests/run_tests.py` and `python score.py --inventory-only`.

Absent or non-isolated model execution is `NOT_RUN`, never a RED result credited to an
arm. Production skill edits remain blocked until neutral and current-v1 RED runs are
durably recorded under the blinded protocol.
