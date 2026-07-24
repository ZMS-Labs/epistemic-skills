# applying-formal-rigor v2 blinded fixtures

This directory implements Phase B of the approved v2 design. It is a blinded conformance
smoke check, not a population measurement or truth oracle.

- `fixtures/<id>/scenario.md` and `artifacts/` are run-agent visible.
- `ground-truth.json`, `score.py`, thresholds, and other results are scorer-only.
- the two schemas close the public response and v2 record vocabularies;
- `semantic-adjudication.md` owns independent derivation judgment;
- `results/` records immutable identities, hashes, dissent, and coverage limits.

Run `python tests/run_tests.py` and `python score.py --inventory-only`.

The authorized full live battery is executed by `run_live.py` from a clean,
pushed candidate commit:

```text
python run_live.py plan
python run_live.py run-arms --output-root <durable-temp-root> --arm v2-candidate --repetition 1 --fixture tm-01-false-mvd --workers 1
python run_live.py run-arms --output-root <durable-temp-root> --workers 4
python run_live.py run-semantic --output-root <durable-temp-root> --workers 4
python run_live.py summarize-semantic --output-root <durable-temp-root>
```

The plan contains 286 arm calls (the two missing repetitions for each baseline,
three candidate repetitions, and all six 22-fixture parodies) plus 132 isolated
semantic-seat calls. Calls are fresh and terminal: once a `call.json` exists,
the runner never retries it. Transport, parse, secret-screen, packet hashes,
raw response, events, and stderr are retained for adjudication and export.

Absent or non-isolated model execution is `NOT_RUN`, never a RED result credited to an
arm. Neutral and current-v1 RED runs were durably recorded before production edits under
`results/2026-07-24-red-baseline/`; candidate, parody, and semantic arms remain separately
gated and `NOT_RUN` until executed.
