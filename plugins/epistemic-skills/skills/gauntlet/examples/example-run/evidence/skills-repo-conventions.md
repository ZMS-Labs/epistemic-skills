# Skills repo conventions (excerpt) — SYNTHETIC EXAMPLE artifact

1. All schemas are versioned with an @N suffix and never edited in place; changes ship as a new version.
2. Verifiers are stdlib-only Python and fail closed with a named reason.
3. A schema change and its verifier release for the same contract land in the same PR.
