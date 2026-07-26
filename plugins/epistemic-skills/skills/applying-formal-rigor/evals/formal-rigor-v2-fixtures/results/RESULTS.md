# Formal-rigor v2 fixture results

**Blinded conformance smoke check; not a population rate.**

| Arm | Structural | Semantic | Gate |
|---|---|---|---|
| neutral/run-1 | RED: 4/22 pass | NOT_RUN | RED ESTABLISHED |
| v1-current/run-1 | RED: 1/22 pass | NOT_RUN | RED ESTABLISHED |
| v2-candidate diagnostic | FAIL: 18/22 pass | NOT_RUN | FAIL |
| six parody arms | NOT_RUN | NOT_RUN | FAIL-CLOSED |

The neutral and current-v1 runs are retained under
`2026-07-24-red-baseline/`. They used 44 fresh, ephemeral, read-only Codex
sessions with scorer truth, ground truth, thresholds, other fixtures, and
other-arm outputs absent from every packet. One neutral response contained an
extra closing brace; its raw bytes are retained and it is scored as S1 invalid
JSON, not repaired.

This establishes the required pre-production RED. It does not establish
semantic-adjudication results or candidate GREEN.

## 2026-07-25 candidate diagnostic

This diagnostic used root `C:\tmp\formal-rigor-canonical2-0e3b0e2` at source
commit `0e3b0e203acbe3829032e702c047b35903d1c021`. All 22/22 Codex
`gpt-5.6-sol` calls completed and were parseable. No calls were retried or
repaired. The content pin was
`d787ff560e5908c72839842484878ed179ff4f6e09f56cee8d588c49ca6d94cd`.

Structural scoring was **18/22**. The four misses were:

- `cc-03`: high-assurance invocation not allowed.
- `mt-01`: P7 missing an adequate module.
- `um-01`: P7 expected unmapped. This fixture contract is disputed because
  its expectation conflicts with P7 resource semantics and the label-only
  rule.
- `um-02`: P6 fired, but the module was missing.

Semantic adjudication was intentionally not run because the structural gate
failed. This diagnostic therefore does **not** establish candidate GREEN.

The interrupted root `C:\tmp\formal-rigor-canonical-0e3b0e2` is excluded. It
contains four valid terminal records, one all-zero `call.json`, and 17 absent
records; it was never overwritten.

**Candidate gate: FAIL.** A new source/campaign is required. Three pinned
passing repetitions, all parody arms, and all semantic gates remain required
before candidate GREEN can be claimed.

## 2026-07-25 agy transport diagnostic

The first full-campaign attempt at source
`2ff58cdc9883e120c7b70241ec81df02aaab0aea` stopped at the first terminal
fixture failure, with 27/198 arm calls recorded. Twenty-four were parseable;
three agy calls completed with exit code zero and clean secret screens but
wrapped one JSON envelope in prose or a Markdown fence. The root
`C:\tmp\formal-rigor-final-2ff58cd` is diagnostic-only and content-pinned as
`69f8500aeb95fa7838f10927f7ccaaa99bbfa10114ecd3d570e2c4b198a21329`.
It was not resumed, repaired, or semantically adjudicated.

The subsequent runner change permits only deterministic extraction of exactly
one recognized top-level envelope while retaining raw stdout and rejecting
zero, repeated, nested, ambiguous, or truncated envelopes. That change requires
a new source commit and fresh campaign; it does not upgrade this failed epoch.

## 2026-07-25 Fleet/Cursor transport diagnostic

The campaign at source `8a3bfdf` stopped at 36/198 arms, with 35 parseable.
The Fleet/Cursor response for `cc-04` / `parody-jargon-only` contained an
earlier malformed snapshot followed by a later valid snapshot. No call was
retried or repaired. The root `C:\tmp\formal-rigor-final-8a3bfdf` is excluded
from scoring and content-pinned as
`49588e690c991d63abecb2fcd3ae9eef20271464fc4daa8c56f90c55c90a9d45`.

## 2026-07-25 Cursor closed-taxonomy diagnostic

The campaign at source `14a9543` completed fixtures 1-4 and stopped on fixture
5, `fc-01`. It contains 45 call records: 44 parseable and one unparseable
Cursor `parody-closed-taxonomy` response. The epoch was not retried, resumed,
or repaired. The root `C:\tmp\formal-rigor-final-14a9543` is excluded from
scoring and content-pinned as
`4ad19cac6812eb0b2cb7c25931dd1b85bd14025b9ee477bd0c7020326e34c3d8`.

## 2026-07-25 prioritized `fc-01` diagnostic

The campaign at source `2c1c38f` prioritized `fc-01` first and recorded nine
calls: eight parseable and the same Cursor `parody-closed-taxonomy` response
unparseable again. The epoch was not retried, resumed, or repaired. The root
`C:\tmp\formal-rigor-final-2c1c38f` is excluded from scoring and content-pinned
as `2febab93d1d6a1a40e0a3e0853b155ad5a481dbb882fe1830fdd9ff0921614ea`.

## 2026-07-25 live-prompt regression diagnostic

At source `c24e39b`, `fc-01` produced 9/9 valid live-prompt regression calls.
The campaign then stopped at `cc-04` with 18 total calls, 17 parseable. The
Cursor candidate response contained two same-identity snapshots, each ending
with an extra unmatched closer. The terminal snapshot was itself invalid and
therefore was not normalized. The epoch was not retried, resumed, or repaired.
The root
`C:\tmp\formal-rigor-final-c24e39b` is excluded from scoring and content-pinned
as `9c1789b1c9507b486cc841f32d9e018cc519cc9ebab2ce6acd129af18e0893b2`.

## 2026-07-25 extended fragile-probe diagnostic

At source `c235d98`, `fc-01` and `cc-04` produced 18/18 valid fragile-probe
calls. The campaign continued through `mt-03`, then stopped with 81 total call
records: 79 parseable and two unparseable Cursor outputs (`candidate` run 3
and `parody-closed-taxonomy`). In both outputs, both snapshots omit an internal
comma before `empirical_closure`. The epoch was not retried, resumed, or
repaired. The root `C:\tmp\formal-rigor-final-c235d98` is excluded from scoring
and content-pinned as
`add00f8b271e33487a5a61df225e44536f9f30e14fedc5d370d817f4dce6be1e`.

## 2026-07-25 `fc-02` transport diagnostic

At source `2a61eef`, the fragile `mt-03`, `fc-01`, and `cc-04` probes all
passed. The campaign recorded 63 calls: 62 parseable and one unparseable Cursor
`parody-closed-taxonomy` response at `fc-02`. Its two snapshots share the same
internal structural/syntax error: a derivation object is placed where an object
member name is required. The epoch was not retried, resumed, or repaired. The
root `C:\tmp\formal-rigor-final-2a61eef` is excluded from scoring and
content-pinned as
`1708148471a8827a0dcd7e18fd07f0c4ad49bfba574554e56c7637b6d9e03786`.

## 2026-07-25 frozen Cursor provider-contract blocker

At source `fb6c914`, the `fc-02` control regression produced 9/9 valid calls.
The subsequent `mt-03` probe recorded nine calls, eight parseable; Cursor
`candidate` run 3 remained unparseable despite terminal-boundary, concision,
and explicit full-JSON syntax-check prompts. The epoch therefore contains 18
calls, 17 parseable. It was not retried, resumed, or repaired. The root
`C:\tmp\formal-rigor-final-fb6c914` is excluded from scoring and content-pinned
as `6395c596b66a545d604af2457e17a551664f485636880ed267a5926d5cf07cce`.

These repeated failures, together with the live Cursor CLI providing no schema
flag, establish a provider-contract blocker for the frozen Cursor arm.

## 2026-07-25 noncursor-degraded failed epoch

The fresh `noncursor-degraded-v1` epoch at source
`fb19e9e9d2ee97b23d8408f54652fe2d86eb6a02` recorded all 286 terminal arm
calls (154 Codex and 132 agy/Gemini; no Cursor calls). Of those, 285 responses
were JSON-parseable and 281 were valid under the frozen transport schema. Four
parseable responses were transport-schema-invalid because
`empirical_closure.tests` contained objects where the schema requires strings;
one agy response was nonparseable after emitting self-talk/multiple envelopes.

The canonical evidence-root content pin is
`2b28b75b18adcab2e41faa2b375641b8e0fee2737de52ed3c0a14adabdff9c13`,
computed with the repository's established sorted relative-path plus
file-SHA-256 manifest algorithm. This epoch is excluded: it receives no
structural score, semantic-adjudication result, or release credit. Its terminal
records will not be retried, repaired, resumed, or reused.
