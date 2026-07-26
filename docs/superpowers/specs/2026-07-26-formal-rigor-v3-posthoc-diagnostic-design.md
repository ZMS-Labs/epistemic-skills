# Formal-rigor V3 post-hoc diagnostic design

## Decision and purpose

The excluded `noncursor-degraded-v3` arm epoch contains useful behavioral
observations even though it cannot satisfy the release protocol. This diagnostic
will measure every retained content-bearing response under frozen structural and
semantic criteria, while preserving the original root and its exclusion.

The result is confidence evidence only. It cannot qualify, repair, resume, or
promote V3; it cannot satisfy a 3.0.0 release gate; and it cannot replace a fresh
complete campaign. Release remains on HOLD regardless of the diagnostic result.

## Frozen source and population

- Excluded protocol: `noncursor-degraded-v3`.
- V3 source commit: `693c0fb26fa4e0c4f54e63b52497783c4ce60131`.
- Raw arm root: `C:\tmp\formal-rigor-noncursor-v3-693c0fb`.
- Canonical raw-root pin:
  `87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1`.
- Planned arm calls: 286.
- Content-bearing arm responses: 215.
- Originally qualifying arm responses: 204.
- Repeated-frame responses with recoverable content: 11.
- Responses with no model content: 71; these remain unscorable missing data.
- Content-bearing candidate responses: 65 of 66.

The diagnostic implementation source, output root, and final root pin will be
recorded separately from these frozen V3 coordinates. Before and after the run,
the V3 root pin must recompute to the canonical value above.

## Alternatives considered

1. **Discard all excluded-epoch content.** This is safest for release gating but
   throws away evidence relevant to whether the implementation appears sound.
2. **Score retained content in a separately identified post-hoc diagnostic.**
   Preserves the release boundary while extracting bounded information from the
   observations. **Selected.**
3. **Normalize the V3 root in place and continue its release workflow.** This
   would retroactively alter the frozen transport criterion and is prohibited.
4. **Treat structural validity as merit.** This confuses transport/schema
   qualification with correctness and is prohibited.

## Derived evidence model

The diagnostic is a materialized view over immutable raw observations:

```text
frozen V3 root
  -> byte-preserving inventory
  -> diagnostic response views
  -> structural scores for all content-bearing arm responses
  -> blinded semantic packets for all content-bearing candidates
  -> two isolated cross-provider judge reports per candidate
  -> aggregate confidence report and content pin
```

Every derived record carries the raw response coordinate, raw SHA-256, fixture,
arm, repetition, origin provider, normalization status, and diagnostic protocol
identity. Derived data lives under a new root and never overwrites the source.

## Structural scoring contract

All 215 content-bearing arm responses are scored against the existing frozen
fixture expectations and structural scorer.

- The 204 originally qualifying responses are copied or referenced without
  semantic modification.
- Each of the 11 repeated-frame raw outputs is parsed into frames. A diagnostic
  view may be formed only when every frame is individually schema-valid, has the
  expected fixture and protocol markers, and is byte-identical after extraction.
- The diagnostic view contains exactly one preserved frame. Its record includes
  the raw hash, view hash, frame count, equality proof, and the explicit status
  `normalized_identical_repeated_frames`.
- Divergent frames, malformed frames, identity mismatch, secret-screen failure,
  or ambiguous extraction remain unscorable. No best-effort selection is
  allowed.
- The 71 no-content calls receive coverage records, not imputed scores.

The report presents both:

1. **Conditional-on-content merit:** score distributions among responses that
   contain recoverable model content.
2. **Intent-to-test coverage:** results against all 286 planned calls, retaining
   missing or invalid outcomes in the denominator.

Candidate performance is reported separately from current-v1, neutral, and
parody controls. Polarity claims are limited to the controls actually observed.
The three entirely absent AGY parody arms are never inferred from other arms.

## Semantic adjudication contract

Every one of the 65 content-bearing candidate responses receives two new,
candidate-blinded, context-isolated semantic judge calls under the existing
semantic rubric and transport schema. The diagnostic therefore plans 130 calls.

- The 21 AGY-origin candidate responses receive two Codex
  `gpt-5.6-sol`/high seats: 42 calls.
- The 44 Codex-origin candidate responses receive two AGY
  `gemini-3.1-pro-high`/high seats: 88 calls.
- A seat cannot see the other seat's output, aggregate scores, scorer code,
  hidden truth material, or any non-redacted rubric content.
- Same-provider seats are independent contexts but correlated observations;
  the report does not describe them as independent model families.
- Raw prompt, stdout, stderr, terminal status, model, effort, version, timings,
  hashes, and parsed report are retained per call.
- Calls are at-most-once within this diagnostic identity. A terminal call is
  not silently retried or replaced.

The AGY transport is preregistered as AGY 1.1.7 with
`--output-format json`, `--print-timeout 10m`, and an outer runner timeout of
720 seconds. The outer timeout exceeds the 600-second AGY wait. Exact provider
and catalog preflights are retained before inference.

The existing semantic decision rules remain unchanged: both seats must be
`VALID` for a candidate response to count as semantically valid; any `INVALID`
fails that response; P0 disagreement or inconclusive output fails; and only the
existing bounded non-P0 arbitration rule may be used. Missing judge calls remain
missing and are not converted to merit failures or successes.

## Measures and interpretation

The aggregate report includes, at minimum:

- planned, content-bearing, normalized, structurally scorable, structurally
  passing, semantically complete, semantically valid, and missing counts;
- results by arm, fixture, repetition, origin provider, and judge provider;
- candidate structural pass rate over available candidates and over all planned
  candidates;
- available control/parody polarity and candidate-to-control separation;
- semantic VALID/INVALID/INCONCLUSIVE/disagreement counts and P0 findings;
- sensitivity excluding the 11 normalized repeated-frame observations;
- exact unavailable-arm and unavailable-response accounting.

The report may increase confidence only to the extent that available candidates
perform strongly, semantic judgments agree, and observed controls show expected
separation. Confidence decreases with candidate failures, weak separation,
provider-linked divergence, judge disagreement, or substantial missingness.

The following disconfirming observations are registered before scoring:

- low candidate structural or semantic validity;
- candidate results resembling controls or parodies;
- materially different results by origin or judge provider;
- P0 findings, INVALID judgments, INCONCLUSIVE judgments, or disagreement;
- normalization-sensitive conclusions;
- inability to observe the missing AGY parody arms.

No numeric posterior probability or all-286 merit claim will be fabricated from
the incomplete, non-random sample.

## Integrity and failure boundaries

- The raw V3 root is read-only input and its pre/post content pin is an invariant.
- A new diagnostic identity and empty output root are required.
- The diagnostic manifest records that all evidence is post-hoc and non-release.
- Secret scanning and identity checks remain fail closed.
- Source, derived views, semantic packets, judgments, aggregates, and reports are
  hash-addressed or content-pinned.
- A scorer or orchestration failure stops the diagnostic; it does not alter V3.
- No diagnostic artifact may be copied into V3's qualifying/semantic locations
  or represented as satisfying `noncursor-degraded-v3` gates.

## Complexity and proportionality

Let `A` be the number of content-bearing arm responses and `S` the number of
semantic seats. Inventory, normalization, structural scoring, and aggregation
are `Theta(A + S)` time with `Theta(A + S)` retained evidence. Any complete
analysis has an `Omega(A + S)` lower bound because each retained response and
judge result must be inspected. With `A = 215` and `S = 130`, the design is
asymptotically tight and avoids recomputing absent responses.

The process is proportionate because it reuses frozen scorers and semantic
contracts, adds only the machinery necessary to preserve post-hoc provenance,
and makes no release claim.

## Completion criteria

The diagnostic is complete only when:

1. the immutable source pin is verified before and after processing;
2. every content-bearing response has a structural score or explicit fail-closed
   exclusion reason;
3. every available candidate has two terminal semantic seat records or an exact
   missing-call account;
4. aggregate and human-readable reports expose both conditional merit and full
   planned-call coverage;
5. an independent review finds no release-credit leakage or hidden repair of V3;
6. deterministic checks pass and the diagnostic root is content-pinned; and
7. source, protocol, results, limitations, and dissent are committed to draft
   PR #48.

Even if all seven criteria hold, the diagnostic closes only the question
"what do the returned outputs suggest?" It does not close the 3.0.0 release
gate.
