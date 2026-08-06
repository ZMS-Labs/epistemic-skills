# Proportionality battery

This is a deterministic **structural smoke check** for process calibration. It
is not a population measurement, a truth oracle, or evidence that a particular
agent will make better decisions in production.

The battery tests the collection's negative path as a first-class behavior:

- routine work should leave before the epistemic arc;
- material work should surface its planted decision or acceptance issue; and
- high-risk work should escalate to the required boundary discipline.

Extra process earns no credit. A run can be factually correct and still fail for
unnecessary ceremony.

## Run record

A candidate produces one JSON file:

```json
{
  "schema": "proportionality-run@1",
  "arm": "candidate-name",
  "results": [
    {
      "fixture_id": "r-01-button-copy",
      "path": "routine|micro-recon|routed",
      "fired_skills": [],
      "process_artifacts": [],
      "visible_process_words": 24,
      "role_invocations": 0,
      "emitted_skip_inventory": false,
      "direct_check": "component preview and existing assertion",
      "required_signal_observed": true,
      "escalated": false
    }
  ]
}
```

`process_artifacts` uses semantic kinds, not filenames: `router-record`,
`helix-check`, `blindspot-report`, `formal-rigor-record`, `ledger-entry`,
`uat-packet`, `gauntlet-run`, `handoff-receipt`, or another descriptive kind.

## Gate

A run passes only when all are true:

1. at least 9 of 10 routine fixtures take `routine` or `micro-recon`;
2. every routine fixture has a bounded direct check and observes the required
   signal;
3. routine fixtures create none of the forbidden process artifacts, make zero
   role invocations, and emit no skip inventory;
4. median routine visible process narration is at most 150 words;
5. every material fixture observes its planted issue and includes its minimum
   required skill set;
6. every high-risk fixture observes its planted issue, includes its minimum
   required skill set, and escalates;
7. every fixture id appears exactly once and no unknown fixture is supplied.

The standing examples are polarity probes:

- `balanced.json` must pass;
- `full-ceremony.json` must fail for over-escalation; and
- `always-routine.json` must fail for under-escalation.

## Usage

```bash
python score.py --run examples/balanced.json
python run_tests.py
```

A real behavioral evaluation should run identical fixture packets against
current main, the candidate branch, and parody arms. Record model, harness,
prompt, skill hashes, and sampling settings. These committed examples validate
the scorer's declared semantics only.
