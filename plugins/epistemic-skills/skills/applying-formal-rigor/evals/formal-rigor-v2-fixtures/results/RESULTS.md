# Formal-rigor v2 fixture results

**Blinded conformance smoke check; not a population rate.**

| Arm | Structural | Semantic | Gate |
|---|---|---|---|
| neutral/run-1 | RED: 4/22 pass | NOT_RUN | RED ESTABLISHED |
| v1-current/run-1 | RED: 1/22 pass | NOT_RUN | RED ESTABLISHED |
| v2-candidate | NOT_RUN | NOT_RUN | FAIL-CLOSED |
| six parody arms | NOT_RUN | NOT_RUN | FAIL-CLOSED |

The neutral and current-v1 runs are retained under
`2026-07-24-red-baseline/`. They used 44 fresh, ephemeral, read-only Codex
sessions with scorer truth, ground truth, thresholds, other fixtures, and
other-arm outputs absent from every packet. One neutral response contained an
extra closing brace; its raw bytes are retained and it is scored as S1 invalid
JSON, not repaired.

This establishes the required pre-production RED. It does not establish
semantic-adjudication results or candidate GREEN.
