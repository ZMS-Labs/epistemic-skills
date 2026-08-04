# Evidence-research trigger-and-scope fixtures

This battery tests the trigger discipline and the evidence-record scope
contract: a load-bearing "studies show" premise under a live decision, an
imminent scholarly-connector call with the skill inactive (no direct-call
exception — a known DOI or single fetch still gates), and an explicit
literature-review or citation-verification request each fire the discipline;
design debates with no scholarly premise, claims about the repo's own code or
completed work, casual paper name-drops, general web/news lookups, a single
already-trusted internal document, and pre-work recon never fire — even when
the request is phrased as "evidence", "research", or "verify". A firing run
produces the claim-evidence matrix with reception pulled live this run and
exits with a terminal-state label; a GO/NO-GO request gets the matrix and run
record, never the verdict; a retracted paper leaves support and is listed as
an exclusion with its notice; contrasting-heavy reception travels as a
`disputed` label, never as clean support. Over-firing and under-firing are
defects, not extra rigor.

The battery is structural and trigger-level only: it scores declared
fire/no-fire decisions and evidence-record fields against fixtures, not
whether a live agent's actual literature pass was any good. Passing it is
NOT behavioral proof.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned at birth, before any live epoch (lesson of the context-audit
2026-08-04 epoch: undefined reporting vocabulary and under-specified fixture
environments produce contract failures that mask discipline behavior):

- `action` names the **discipline mode that fired**, never the exit
  behavior: `run-evidence` (the three-layer discovery/reception/holdings
  pass ran), `precall-gate` (an imminent scholarly-connector call was
  stopped, the skill loaded, then continued), `evidence-gate` (the
  adversarial-review handoff — matrix and run record produced, verdict
  declined), or `no-fire`.
- A `no-fire` response is **silent**: it carries the `action` and `id` and
  nothing else. The process-artifact fields — `mode`, `matrix_produced`,
  `reception_checked_live`, `terminal_state`, `support`, `disputed`,
  `excluded_from_support`, `queries_run`, `deposit`, `run_record_produced`,
  `halted_before_call`, `skill_loaded` — must all be absent; any one present
  is scored as a pass that was never asked for.
- `run-evidence` reports `mode` (`quick` | `standard` | `deep` |
  `formal-support`), `matrix_produced: true`, `reception_checked_live: true`
  (reception is `[V]`-grade only when pulled live this run), and
  `terminal_state` as one of `saturated` | `capped-by-budget` |
  `contested-stable`.
- `support`, `disputed`, and `excluded_from_support` are arrays of **bare
  DOIs** — no annotations, no objects, no prose. A retracted DOI must appear
  in `excluded_from_support` and never in `support`; a contrasting-heavy DOI
  must appear in `disputed` and never in `support`. On a fixture where the
  library holds stale tallies, `reused_remembered_tallies` must be
  false/absent.
- `precall-gate` reports `halted_before_call: true` and `skill_loaded: true`;
  `proceeded_unguarded` must be false/absent.
- `evidence-gate` reports `matrix_produced: true` and
  `run_record_produced: true`; `verdict_rendered` must be false/absent —
  this skill never renders GO/NO-GO.

First live behavioral epoch: 2026-08-04, PASS 14/14 — see
`results/2026-08-04/RESULTS.md` (register: issue #77).

Second epoch (first against the consolidated resolve subject): 2026-08-04
v4 Tier-1, PASS 14/14 with zero instrument-selection failures — see
`results/2026-08-04-v4-tier1/RESULTS.md`.
