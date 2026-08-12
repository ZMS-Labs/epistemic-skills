# mission-custody@1

Durable mission-custody contract family: `mission-manifest@1` (authority,
append-only instruction), `checkpoint@1` (revisioned snapshots,
`prev_checkpoint_sha256` chain), `receipt@1` (effect -> artifact hash binding),
`acceptance-verdict@1` (tiered acceptance; self-certification refused).

Provenance: FOLD cell of the practical-agency gauntlet decision rule; design
`docs/superpowers/specs/2026-08-11-mission-custody-contracts-design.md`.
practical-agency (ZMS-Labs) is parked prior art; its schemas seeded this family.

Validate: `python verify_mission_custody.py examples/valid-manifest-minimal.json`
Test: `python test_mission_custody.py` (exit 0 = green; every `invalid-*.json`
example MUST fail validation — the corpus is the regression suite).

Evolution: additive optional fields only within `@1`; anything else is a new
epoch with a documented migration. Acceptance tiers are closed:
`operator-accepted`, `declared-role-separation` — no `externally-proven` tier
exists until evidence could support one.

## Harness bindings

- Skill: `manifest`
- CLI: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
- Stage C (enforcement): the tracer retro (2026-08-11, vanta
  `mission/tracer-media-missing-record` @ `4540ddb`) ruled teeth IN, scoped to
  the successor mission's real actuators. Shipped as `custody_hook.py` +
  `gate` (design: `docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md`).
  Inert by default: a mission arms it by adding operator-approved
  `actuator_guards` + `guard_mode` to its manifest (`open --guards-file` /
  `amend --guard-mode`). Harness wiring:
  | harness | mechanism | verified |
  |---|---|---|
  | Claude Code | plugin `hooks/hooks.json` PreToolUse | yes |
  | Kimi Code | plugin.json `hooks` array | yes (official docs 2026-08-12) |
  | Codex | `hooks/codex-hooks.json` install note | yes — https://developers.openai.com/codex/hooks (2026-08-12): payload shape, exit-2 block, and `~/.codex/hooks.json` / `<repo>/.codex/hooks.json` discovery all confirmed; hosted tools never fire hooks (their docs' caveat, ours too) |
  | Cursor | plugin.json `hooks` key -> `hooks/cursor-hooks.json` | mostly — https://cursor.com/docs/agent/hooks (2026-08-12) confirms payload shapes and exit-2 block; the plugin manifest `hooks` key is confirmed by https://cursor.com/docs/plugins plus third-party plugins using it, but the CWD plugin-shipped hook commands run from is undocumented (our `./contracts/...` command assumes the plugin root), and a 2026-06 forum report says Cursor CLI ignores plugin-shipped hooks (IDE honors them) |
  | Gemini CLI + agy | `~/.gemini/settings.json` BeforeTool snippet (`hooks/gemini-settings-snippet.json`) | yes — https://geminicli.com/docs/hooks/reference/ (2026-08-12): payload shape, exit-2 block, millisecond timeout; built-in tool names differ (`run_shell_command` etc.) so guards must name them; agy coverage rests on the shared `~/.gemini/settings.json` surface (third-party evidence) |
  | others | `generic` adapter recipe (below) | by construction |

  Generic adapter recipe: point any harness that can pipe a JSON tool-call
  payload to a script at `custody_hook.py --harness generic`. The payload
  needs `tool_name` plus a `tool_input` object carrying `command` and/or
  `file_path`, and a `cwd` naming the workspace that holds `missions/`;
  anything missing degrades to allow (fail-open). Exit 0 allows, exit 2
  blocks with the reason on stderr.

  MCP coverage note: `tool_names` in a guard rule are exact-match against the
  harness's tool name (`mcp__sonarr__post`, `run_shell_command`, ...);
  `command_regexes` match the shell command when there is one, and otherwise
  the full `tool_input` JSON serialized with sorted keys -- so MCP arguments
  (URLs, paths) are coverable by regex, crudely and deliberately over-broad.

  Mixed-fleet hazard: arming guards writes the new manifest fields into that
  mission's checkpoints, which pre-#117 plugin caches cannot validate (the
  armed mission reads as ChainBroken/unreadable there). Update every custody
  consumer before arming guards on a shared mission.
