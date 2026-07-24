# Blinded proportionality protocol

This directory upgrades the structural examples into runnable, isolated fixture
packets. It does not claim that any live arm has run.

`runner.py prepare` creates one agent-visible packet per fixture. The packet
contains only the common response contract, the scenario, and its minimal
artifacts. It excludes fixture category, expected route, required skills,
thresholds, scorer code, other fixtures, and other arms.

`runner.py score` consumes one raw `proportionality-fixture-response@1` JSON
file per packet, preserves those files, assembles `proportionality-run@1`, and
invokes the deterministic parent scorer. Its manifest pins the source commit,
prompt, fixture inputs, provider/model/harness/settings, and every packet hash.

Prepare an arm:

```bash
python blinded/runner.py prepare --arm candidate-final-4e1945e --out /tmp/prop-final
```

Run each `packets/<fixture-id>/input.json` in a fresh context using the pinned
invocation profile. Save the model's JSON object as
`responses/<fixture-id>.json`, without repairing it by hand. Then score:

```bash
python blinded/runner.py score --packet-dir /tmp/prop-final
```

Candidate arms require three repetitions. Use a separate output directory for
each repetition and retain failures and dissent. See `results/BLOCKED.md` for
the present execution status.
