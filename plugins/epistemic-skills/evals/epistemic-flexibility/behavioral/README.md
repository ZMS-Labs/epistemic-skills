# Epistemic-flexibility behavioral fixture scaffold

This directory is the bridge between the deterministic protocol conformance battery one
level up and a real four-arm behavioral evaluation. It contains small, artifact-grounded
scenarios with deterministic outcome rules. Each scenario has:

- `scenario.json` — the prompt/artifact facts and scoring contract;
- `gold.json` — a trace that should pass;
- `bad.json` — a planted failure that should fail.

Run the scorer self-test:

```bash
python run_tests.py
```

Score a new trace:

```bash
python score_behavior.py fixtures/<id>/scenario.json /path/to/trace.json
```

Structural validity is delegated entirely to `../validate_trace.py` — the
single trace authority (it accepts `residual_uncertainty` as a string or an
array; the 2026-08-04 four-arm run found live subjects split between the
two). A blinded harness that withholds the fixture id from subjects and
binds trace to fixture itself passes `--bound`: an absent `trace.scenario`
is then tolerated, while a present-but-wrong one still fails.

## What this proves

The self-test proves that the scorer distinguishes the committed gold and planted-bad
traces. It does **not** prove that a model reliably produces the gold behavior, that the
controls improve coding outcomes, or that the fixture set represents production traffic.

## Required four-arm run

A future runner with model/API or isolated-agent access should execute every scenario under:

1. **A — baseline:** normal coding-agent workflow;
2. **B — repository v2.8.0:** skills before this integration;
3. **C — psychology language only:** ACT/DBT/CBT-inspired reflection without artifact
   contracts;
4. **D — integrated controls:** this branch.

Use fresh contexts, randomized arm order, at least three repeats per model/configuration, and
record raw outputs plus scorer results. Primary outcomes: correct control/action, false hold
on clean controls, false act on traps, source anchoring, proxy resistance, preregistration,
recurrent-chain completeness, and residual-tension preservation. Secondary outcomes: tokens,
latency, tool calls, and user-correction burden.

The committed fixtures are a smoke subset. Add real incidents before making a superiority
claim. A release may say “protocol and fixture scaffold shipped”; it may not say “behaviorally
superior” until the four-arm run exists.

The valid campaign design (full schema in the pinned dispatch text, arm
materialization pinned by content hash, preregistered paired analysis with a
clean-control guard, telemetry incl. actual serving model) is committed at
[`campaign-design-2026-08-04.md`](campaign-design-2026-08-04.md); issue #39
stays open until a run under that design is committed.
