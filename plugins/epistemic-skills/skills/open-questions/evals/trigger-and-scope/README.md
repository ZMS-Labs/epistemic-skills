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
