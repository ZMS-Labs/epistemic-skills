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
Source-skill hashes are recorded when the file exists and as JSON `null` when
a pinned historical commit predates that skill; historical absence is evidence,
not a packet-preparation failure.

Prepare an arm:

```bash
python blinded/runner.py prepare --arm candidate-final-4e1945e --out /tmp/prop-final
```

Run each `packets/<fixture-id>/input.json` in a fresh context using the pinned
invocation profile. Save the model's JSON object as
`responses/<fixture-id>.json`, without repairing it by hand. Then score:

```bash
python blinded/runner.py run-live --packet-dir /tmp/prop-final --source-root <pinned-checkout> --codex <codex-path> --workers 4
python blinded/runner.py score --packet-dir /tmp/prop-final
```

`run-live` verifies the checkout commit and every pinned skill hash, then runs
each fixture in a fresh read-only Codex context rooted at that checkout. Its
scorer-free adapter projects the checkout's exact member-skill name/description
frontmatter catalog (matching normal installed skill discovery), activates the
checkout's `using-epistemic-skills` router, and permits full reads only for
positively triggered member skills. The sealed packet is sent on stdin and
model output is constrained by the committed response schema;
terminal call records are never retried or overwritten. Running from the packet
directory without exposing and activating the pinned source is not a valid
repository-arm measurement.

Candidate arms require three repetitions. Use a separate output directory for
each repetition and retain failures and dissent. See `results/BLOCKED.md` for
the present execution status.
