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

## Operator-authorized prospective amendment: `noncursor-degraded-v1`

This amendment is prospective only. The frozen three-provider evidence above,
including every Cursor failure, root, and content pin, remains immutable
historical evidence. Cursor remains `BLOCKED_EXTERNAL`.

The operator authorizes one new protocol identity, `noncursor-degraded-v1`.
Cursor ceases to block publication only if one complete, content-pinned epoch
under that identity passes every unchanged gate. The epoch must use a new empty
root with the matching campaign plan, and must contain neither a Cursor nor a
Fleet Cursor call. Partial roots, repaired output, resumed-after-terminal-
failure roots, mixed-protocol roots, substituted roots, and historical roots do
not qualify.

A qualifying result supports only two-provider blinded conformance, not
three-provider robustness or Cursor reliability. Revisit the Cursor block when
Cursor exposes schema-constrained generation, or when a separately approved
targeted third-provider protocol exists.

## Completed excluded `noncursor-degraded-v1` epochs and v2 amendment

The completed v1 epoch at source `a18e8ba41085c7d45b126e342b3222a19e497bc6`
is excluded with canonical root pin
`11eecc3d589a88ccb19dc5117a2a0cfdd5019252f4bc5c528a98581c61efbe5a`: of 286
terminal calls, 281 qualify and five fail. The failures are two raw telemetry
user-profile-path leaks (one agy and one Codex, with clean final response
objects), two agy strict-schema violations (v1-style record shape and object
`uncertainty_posture`), and one agy self-talk/fenced multi-draft response with
two identical schema-valid envelopes. It receives no scoring, semantic, or
release credit and is never retried, repaired, resumed, or reused.

The operator authorizes a new, distinct prospective identity,
`noncursor-degraded-v2`; it does not relabel or repair v1. It keeps v1's
two-provider allocation and counts, unchanged gates, no-retry rule, and
two-provider-only claim boundary. Before calling models, v2 rejects an
output-adjacent neutral packet root if profile-bound; it uses direct
`agy --add-dir .`, medium-effort agy arms, high-effort agy semantics and Codex
calls, and the exact frozen transport schema embedded in every non-native-schema
arm prompt. Every non-native-schema semantic prompt receives only the exact
semantic transport schema, never truth or scorer material. Campaign and call
records must retain the canonical packet root and execution policy/settings.
Frozen and v1 identities remain inspectable but non-runnable under current
source and require their pinned historical commits. Active v2 Codex and agy
harnesses reject Fleet-bridge overrides; a bridge-backed evaluation requires a
separately preregistered protocol identity. Cursor remains `BLOCKED_EXTERNAL`,
and release remains HOLD until a complete v2 epoch passes.

## Completed excluded `noncursor-degraded-v2` epoch and v3 amendment

V2 at source `54d3bae4fe51a69cd9cab7658d703d695073006b`, root
`C:\tmp\formal-rigor-noncursor-v2-54d3bae`, and canonical pin
`ce8c7253c8bc2a18f93a2591a4566295b9d69468a4bc7911760bc182309397b0` is
excluded. It recorded 286 terminal arms: 154 qualifying Codex calls and 132
failed agy calls. Each agy call failed before execution because
`--model gemini-3.1-pro-high conflicts with --effort=medium`. It earns no
structural score, semantic adjudication, or release credit and cannot be
retried, repaired, resumed, or reused.

`noncursor-degraded-v3` is a separate prospective identity, not a v2 repair.
It keeps the same counts, gates, no-retry behavior, and two-provider claim
boundary. Its exact matrix is arms: Codex `gpt-5.6-sol`/high and agy
`gemini-3.6-flash-medium`/medium; semantic: Codex `gpt-5.6-sol`/high and agy
`gemini-3.1-pro-high`/high; Cursor is zero/unavailable. A fresh source/root,
v3 manifest and per-call provenance, and an AGY 1.1.7 version/catalog/suffix
capability preflight plus receipt are mandatory before fixture calls. That
preflight is AGY-only; Codex has no catalog preflight and relies narrowly on
V2's 154/154 qualifying `gpt-5.6-sol`/high calls, while V2 remains excluded.
Cursor remains `BLOCKED_EXTERNAL`; release remains HOLD until a complete v3
epoch passes every unchanged gate.
