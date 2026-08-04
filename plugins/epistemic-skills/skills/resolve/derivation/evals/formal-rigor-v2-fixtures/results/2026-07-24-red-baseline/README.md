# Neutral and current-v1 RED baseline

This directory is the immutable pre-production behavioral baseline required by
the applying-formal-rigor v2 implementation order.

- Provider/model: OpenAI `gpt-5.6-sol`.
- Harness: Codex CLI 0.144.6, ephemeral, read-only, high reasoning.
- Isolation: one fresh packet-only directory and session per fixture; plugin
  injection disabled; no scorer, ground truth, thresholds, other fixtures, or
  other-arm output present.
- Runs: 22 neutral and 22 current-v1 calls, no model failure retried.
- Structural result: neutral 4/22; current-v1 1/22.
- Semantic adjudication: NOT_RUN.

`manifest.json` pins settings and source hashes. `evidence.json` binds every
raw response. `status.json` records ingest status. The two score files contain
all named failures.

The neutral `cc-02-comparison-bound-is-valid` response ends with one extra
closing brace. The exact malformed response is retained and scored S1 invalid
JSON. It was not repaired or rerun.
