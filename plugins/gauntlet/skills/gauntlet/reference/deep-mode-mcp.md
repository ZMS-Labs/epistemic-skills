# Deep Mode — DeepReason MCP (first-class)

Deep mode uses the `deepreason` MCP server (`python -m deepreason.mcp_server`). Read tool schemas from the MCP descriptor folder before calling.

## Preconditions

1. `deepreason` package installed (`pip install git+https://github.com/AHepi/DeepReason.git`).
2. At least one provider API key set in the environment Cursor inherits (`OPENAI_API_KEY` and/or `DEEPSEEK_API_KEY` per `config/operator.yaml`).
3. Frozen verified dossier from Step 0 exists.

## Run directory

Use a dedicated root per review:

```
~/.agents/deepreason-runs/<subject-slug>-<YYYY-MM-DD>/
```

Pass this absolute path as `root` on every MCP call.

## Standard deep-mode loop

Config path (absolute):

```
${CLAUDE_PLUGIN_ROOT}/skills/gauntlet/config/operator.yaml
```

### 1. `seed_problem`

Register the decision question. Use the frozen dossier as context in `problem.description`. For fixed-artifact gates, phrase as rival failure-mode exploration; for open questions, phrase as rival explanations.

Minimum fields:

- `problem.id` — short slug
- `problem.description` — the locked question + scope + pointer to frozen dossier path
- `problem.criteria` — include falsifiability-related criteria when applicable

### 2. `run_cycles`

Fund cycles under a hard budget. Start small; fund more only if frontier is thin.

Suggested first pass:

- `cycles`: 4–6
- `token_budget`: 50000–150000 (scale to stakes)
- `config`: operator.yaml path above

If metered vs logged tokens diverge in the response, stop and investigate before trusting metrics.

### 3. `frontier`

Read surviving artifacts and open problems. This is the rival-hypothesis map for the native panel.

### 4. `theory` / `why`

For each survivor worth adjudicating, read the committed theory view and justification chain. Feed these into lens prompts — not as verdicts, as **candidates to stress-test**.

### 5. `eval_report` + `docket`

Use `eval_report` to steer attention (never as verdict). Clear disagreements via `appellate_rule` on docketed cases when standards conflict — rulings calibrate future reads, they do not flip existing verdicts.

## Rules of engagement (do not fight the harness)

1. You cannot set a status — acceptance/refutation are computed.
2. Operator judgment enters only through the docket (`appellate_rule`), budgeted by `USER_RULINGS_BUDGET`.
3. Nothing is deleted; bad artifacts are answered by criticism.
4. Metrics steer attention, never status.
5. Always pass `token_budget` to `run_cycles`.

## After deep mode

Return to the native protocol: independent lenses review survivors against the **frozen dossier** with `[V path:line]` tags, mechanical falsifier + evidence criticism, arbitration, computed GO/CONDITIONAL/NO-GO.

DeepReason survivors are **best-argued in the bracket**, not externally verified truth.
