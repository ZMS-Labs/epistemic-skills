# Arm registry

Exact model/provider, harness, prompt hash, skill hash, fixture hash, schema
hash, scorer hash, and sampling settings are mandatory per run.

| Arm | Run | Status | Evidence |
|---|---:|---|---|
| neutral | 1 | RED: 4/22 structural pass | `2026-07-24-red-baseline/` |
| v1-current | 1 | RED: 1/22 structural pass | `2026-07-24-red-baseline/` |
| v2-candidate | — | NOT_RUN | — |
| parody arms | — | NOT_RUN | — |

The two completed arms used identical model/provider/harness/settings and
fresh packet-only contexts. Their semantic-adjudication column remains
NOT_RUN; structural RED does not attest derivation correctness.
