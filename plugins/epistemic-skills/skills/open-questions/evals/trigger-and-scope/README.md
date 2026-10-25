# Open Questions trigger-and-scope fixtures

This battery tests the trigger discipline and the auto-fire scope contract:
explicit invocation runs the full exhaustion interview; a fuzzy brief or an
active design dialogue never fires; an absent operator parks reversible forks
and holds irreversible un-best-guessable ones; the narrow auto-trigger walks
only the fork's lineage, makes exactly one offer for other surfaced
questions, and defers declined items to a durable tracker with their
best-guess defaults. Over-firing, scope creep, and lost deferrals are
defects, not extra rigor.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Two clarifications pinned after the 2026-08-04 epoch (both of its failures
were vocabulary divergences over behaviorally-correct conduct):

- `action` names the **discipline mode that fired**, never the exit
  behavior. An explicit full interview that the operator releases mid-way is
  `full-interview` with `operator_release: true` and the remaining items in
  `parked` — not `park-and-proceed`, which is reserved for the
  absent-operator reversible-fork path where no interview mode fired.
- `visible_process` means a **process-only artifact the discipline required
  silence about** (an interview transcript where no interview should fire, a
  ledger/stamp emitted on the no-fire path). The escalation notice a
  `hold-escalate` must deliver and the parking announcement a
  `park-and-proceed` must make are the discipline's own required outputs —
  they are NOT `visible_process` and must not be reported as such.

First live behavioral epoch: 2026-08-04, FAIL 8/10 — see
`results/2026-08-04/RESULTS.md` for the record, methodology, and the two
diagnosed reporting-contract failures (register: issue #77).

Second live epoch: 2026-10-24 (E11), FAIL — the shipped scorer crashed
on one response carrying `parked` as an integer count and produced no
fixture verdicts; the crash is the epoch's recorded result
(`results/2026-10-24/RESULTS.md`). Scorer robustness fix (issue #277):
a non-list `parked` now scores as a per-fixture shape failure instead of
raising, at both sites that iterate it; regression coverage in
`tests/run_tests.py` with `examples/parked-as-count.json`. The fixed
scorer's reading of E11's frozen responses is recorded at
`results/2026-10-24/rescore/` — an instrument-repair record; it does
not re-run or alter the epoch.

## V7 synthetic regression boundary (2026-09-18)

The current scorer and its new cases exercise response-contract checks, not
model behavior or native-host execution. Historical `results/` outputs retain
their original verdicts and limitations. Changed v7 scoring does not rescore
old failures as successes. Existing example self-tests remain compatibility
checks; new cases cover only the documented v7 contract changes. No empirical
activation or comparative task-benefit claim follows from these tests.
