# Claude Opus 5 blinded verification-proportionality packets

This directory prepares identical, isolated task packets for model/prompt arms
without embedding fixture expectations in the model-visible input.

## Arms

- `neutral-opus5`: no model-specific verification instruction;
- `candidate-opus5`: the proposed scope-and-verification overlay;
- `legacy-final-pass`: forces a separate final rerun and verifier;
- `verifier-subagent`: forces a verifier on every task; and
- `never-verify`: suppresses all evidence gathering.

The parody arms are polarity controls. They are not candidate prompts.

## Prepare

Use a clean checkout at the exact source commit being evaluated. Pin the exact
API model identifier at preparation time; the committed `arms.json` deliberately
uses `null` so a vague family name cannot masquerade as a reproducible run.

```bash
python runner.py plan
python runner.py prepare \
  --arm candidate-opus5 \
  --repetition 1 \
  --model-id <exact-claude-opus-5-model-id> \
  --source-root <clean-checkout> \
  --out <durable-output-dir>
```

Invoke one fresh context per `packets/<fixture>/input.json`. Store the raw JSON
response as `responses/<fixture>.json`; do not retry or overwrite a first
response. Then score:

```bash
python runner.py score --packet-dir <durable-output-dir>
```

A complete behavioral comparison should run all declared repetitions with the
same model, effort, tools, harness, source commit, and sampling settings.
Preserve raw responses, manifests, scores, failures, and prompt/source hashes.

## Response boundary

The response records observable process choices rather than hidden reasoning.
It maps each verification action to a material claim, oracle, subject revision,
independence mode, reuse/rerun state, and discriminating purpose. The scorer
does not infer correctness from fluent explanations.

No live result is committed here. Structural tests establish only packet
integrity and scorer polarity.
