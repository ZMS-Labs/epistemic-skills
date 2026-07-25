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
