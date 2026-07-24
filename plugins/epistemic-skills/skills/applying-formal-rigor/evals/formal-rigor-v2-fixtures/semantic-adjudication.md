# Blinded semantic adjudication protocol

Structural scoring never attests that a derivation is valid. For each fixture, two
context-isolated adjudicators receive only `scenario.md`, `artifacts/`, the candidate
response, and that fixture's scorer-only proof obligations and forbidden propositions.
They do not receive arm identity, model identity, other fixtures, thresholds, prior
results, or one another's report.

Each returns `VALID`, `INVALID`, or `INCONCLUSIVE`, with obligation ids and exact response
coordinates. Agreement on `VALID` passes. Any `INVALID` fails. P0 disagreement or
`INCONCLUSIVE` fails closed. One bounded arbitration round may resolve a non-P0
disagreement; original reports remain immutable.

This scaffold cannot manufacture isolation by writing two answers in one context. A run
is `NOT_RUN` until the harness supplies independently isolated seats and exact identities.
