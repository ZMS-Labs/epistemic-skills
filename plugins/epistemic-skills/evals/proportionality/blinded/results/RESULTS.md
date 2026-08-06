# Proportionality blinded evaluation results — 2026-07-25

## Pinned subjects and coverage

- Canonical repository-arm root (local-only): `C:\tmp\proportionality-final-7cdf6fc`
- Protocol commit: `7cdf6fc`
- Compared subjects: main `80eb0827108d46e521f44f4fed3c20da0edc79a7`, PR46 `a4f2210fe3e955b77bb2593fa3c6c991304a4142`, and final product `b73b04af46255bddf103a3f7e80e69b442ebddab`
- Canonical-root SHA-256: `11168ef457764778be19c5ace54f3f263621f260377e4bbf9c87eb281b8d2e59`
- Canonical run integrity: 162/162 terminal, schema-valid, and matched; no retry or repair.

## Blinded results

- **Final product:** r1/r2/r3 all PASS. Each run scored routine 10/10, material 4/4, and high-risk 4/4. Median visible process was 7, 6.5, and 6 words for r1, r2, and r3 respectively.
- **Main:** FAIL, with skip inventory and unknown router names.
- **PR46:** three FAILs. r1 and r2 omitted `blindspot-pass` on m3; r3 used an unknown router name.

## Negative controls

The initial always-routine parody correctly FAILed. The initial full-ceremony parody wrongly PASSed because its adapter neutralized the parody; this was diagnosed and is not credited.

Corrected negative-control root (local-only): `C:\tmp\proportionality-parody-correction-15cce7e`; adapter commit `15cce7e`; root pin `cb5a8d7f64d7ec78321005a938bbf040d99af62e316a932522b8c37180c97d4c`. The corrected runs were 18/18 terminal, parseable, and matched per parody, with no retry or repair:

- Full-ceremony: FAIL, routine 0/10.
- Always-routine: FAIL, material 0/4 and high-risk 0/4.

## Scope and exclusions

These are conformance smoke checks, not population effect estimates. Raw transcripts remain local-only.

Excluded diagnostic roots:

- `C:\tmp\proportionality-live-b83c78c` — source not exposed.
- `C:\tmp\proportionality-source-exposed-48e355f` — no installed-style catalog.
- `C:\tmp\proportionality-final-3d5f508` and `C:\tmp\proportionality-final-e149179` — partial runs.

## Gate conclusion

Candidate: 3/3 PASS, and both corrected parodies FAIL. Release remains separately gated.
