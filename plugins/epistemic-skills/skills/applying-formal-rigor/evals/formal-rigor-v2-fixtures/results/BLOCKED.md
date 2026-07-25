# Historical live-arm capability block

Status: `RESOLVED_FOR_BASELINE` on 2026-07-24.

The original implementation context did not expose a qualifying invocation
primitive. On resumption, `codex exec --ephemeral` was verified and used from
packet-only temporary directories with read-only access and plugin injection
disabled.

Consequently, the prior block is closed for the required RED baseline:

- neutral and current-v1 are recorded under `2026-07-24-red-baseline/`;
- no hand-authored or repaired output is credited;
- structural RED is established at 4/22 and 1/22 respectively;
- production files may now change under the RED-before-production-edit gate.

The first candidate diagnostic subsequently ran and failed structurally; see
[`RESULTS.md`](RESULTS.md) for its immutable root and content pin. Parody and
semantic-adjudication gates remain incomplete. This historical file does not
claim candidate GREEN or any later gate is complete.

## Current Cursor structured-output block

Status: `BLOCKED_EXTERNAL` on 2026-07-25 for the frozen Cursor arm.

The Fleet Cursor stream was exercised repeatedly with retained raw NDJSON and
without retrying or repairing terminal records. The live Cursor CLI exposes
`--output-format text|json|stream-json`, but no JSON Schema or constrained
response flag. Its stream frames therefore carry unconstrained assistant text,
not provider-enforced structured output.

Terminal-boundary, concision, whole-response syntax-check, and bounded-control
prompt changes each closed specific observed failures. They did not make the
frozen Cursor arm reliable: at source `fb6c914`, `fc-02` produced 9/9 valid
control calls, then Cursor `candidate` run 3 for `mt-03` was unparseable. See
[`RESULTS.md`](RESULTS.md) for the immutable root and content pin.

The required three-provider campaign is therefore not GREEN. Closure requires
either an enforceable structured-output capability for the Cursor arm or an
explicitly approved replacement protocol followed by a new preregistered
epoch. More calls through the same unconstrained contract, partial epochs,
post-hoc repair, or provider substitution do not close this block.
