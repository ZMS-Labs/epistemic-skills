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

Candidate, parody, and semantic-adjudication arms remain `NOT_RUN`; this file
does not claim those later gates are complete.
