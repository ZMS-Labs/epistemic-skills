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

## ENFORCEMENT STATUS -- what actually refuses, and what only informs

Every field below is either a CONTROL (a machine evaluates it and refuses) or a
DECLARATION (a human reads it; the record preserves it for later comparison).
Both are legitimate. "Unenforced" is not a defect. The defects are: a field
whose class you must INFER, a declaration nobody is ever SHOWN, and a
declaration nothing ever COMPARES.

| field | who reads it | what happens on violation |
|---|---|---|
| `authority.actuator_guards` + `guard_mode` | `custody_gate.evaluate()` at the PreToolUse hook | **CONTROL — with the inert paths named below.** enforce mode blocks the tool call (exit 2) naming the rule; audit mode logs to `guard-log.jsonl` and allows. It is a control ONLY while the gate resolves exactly one readable active mission, and every way that resolution can fail is a way the guards stop holding. Measured, each flipping an armed enforce mission from `block` to `allow`: **(1)** a second active mission under the same workspace root (an *unarmed* decoy is enough); **(2)** a payload that reports no usable location — cwd outside the workspace tree **and** no usable `workspace_roots` (Cursor payloads supply roots and are evaluated per-candidate, blocking if any candidate blocks, so that harness is not covered by this row); **(3)** any harness failing open on hook error; **(4)** a store that CLAIMS a NEWER contract epoch than the local reader, which fails validation and is skipped (`checkpoint@2` against an `@1` reader — including a `checkpoint@1` whose *embedded* `mission-manifest` claims `@2`); **(5)** an ordinary corrupt or chain-broken store, skipped by `Mission.load` for the same structural reason, leaving the workspace reporting no active mission; **(6)** a store unreadable for environmental reasons, where `Mission.load` propagates `OSError` and the hook's own handler allows. Paths 4 and 5 are reported separately, but **that is a difference in what the store CLAIMS, not a finding about what it is**: this reader has no `@2` validator, so a corrupt or tampered store relabelled `checkpoint@2` is indistinguishable here from a genuine newer one — which is why "update the reader" is the way to FIND OUT the remedy, never itself the remedy. Reading path 4 as "not corrupt, just newer" is the corruption-suppression attack SECURITY.md documents. The posture is identical either way: inert. **This list is what has been measured, not a proof of completeness**; earlier revisions of this row claimed four paths and then five, and each count was falsified by the next review. See SECURITY.md, "Discovery ambiguity disarms the gate" and "A newer epoch disarms a stale reader". |
| `authority.instruction` / `.amendments` | steward, acceptor, auditor | **DECLARATION.** Append-only and inside the tamper-compare. Nothing refuses; a guard change without a new amendment IS detected as tampering |
| `scope.in` / `scope.out` | steward (shown by `status --brief` and `resume`); path-pattern entries compared against the receipt set at acceptance | **DECLARATION at run time, COMPARED at acceptance.** No runtime gate consumes it -- it is a top-level sibling of `authority` and the gate is only ever handed `authority`. At acceptance a crossing refuses PASS until the acceptor acknowledges each finding BY KIND (`accept --scope-ack <path>` for a boundary crossing, `--scope-ack linked:<path>` for a MULTIPLY LINKED disclosure -- different judgements, neither spelling discharges the other); an amendment mentioning a path is a HINT, never a discharge. Honest scope of this control: it is a control against FORGETTING, not against intent -- the acknowledgement is authored by the acceptor and the amendment text by whoever runs `amend`, and the contract cannot verify a principal said either (principal binding is the runtime boundary's job, as everywhere else in this table). Prose entries cannot be compared and are reported as uncompared -- a scope.in mixing prose with patterns disables the include comparison entirely and says so. Immutable, so it cannot be retro-fitted to match the drift |
| `authority.protected_state` | steward | **DECLARATION.** Nothing refuses |
| `stop_rules.hold_if` / `stop_if` / `escalate_if` | steward, at the moment the condition arises | **DECLARATION.** Nothing refuses. These have demonstrably changed outcomes anyway -- because each names a MOMENT a steward recognises, not a category |
| `authority.acceptable_costs` | steward, acceptor | **DECLARATION.** Nothing refuses |
| `acceptance.required_tier` | `record_verdict` | **CONTROL.** A PASS below the required tier, or self-certification, is refused |
| receipts / `prev_checkpoint_sha256` | `resume`, `load_latest` | **CONTROL.** Drift and chain breaks are reported; `load_latest` refuses a broken chain |

An **empty** declaration is UNBOUNDED, not safely defaulted. Validation accepts
`[]` forever (`all()` over an empty list is True), so `status --brief` reports
which envelope fields are unset rather than leaving silence to imply
boundedness.

## Harness bindings

- Skill: `manifest`
- CLI: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
- Stage C (enforcement): the tracer retro (2026-08-11, vanta
  `mission/tracer-media-missing-record` @ `4540ddb`) ruled teeth IN, scoped to
  the successor mission's real actuators. Shipped as `custody_hook.py` +
  `gate` (design: `docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md`).
  Inert by default: a mission arms it by adding operator-approved
  `actuator_guards` + `guard_mode` to its manifest (`open --guards-file` /
  `amend --guard-mode`). The CLI can downgrade enforce -> audit
  (`amend --guard-mode audit`), but full guard REMOVAL is API-only
  (`Mission.amend_authority(..., actuator_guards=None)` -- the CLI's
  `amend --guards-file` with `[]` is refused by validation); plan disarm
  accordingly mid-incident. Harness wiring:
  | harness | mechanism | verified |
  |---|---|---|
  | Claude Code | plugin `hooks/hooks.json` PreToolUse | yes |
  | Kimi Code | plugin.json `hooks` array | yes (official docs 2026-08-12) |
  | Codex | `hooks/codex-hooks.json` install note | yes — https://developers.openai.com/codex/hooks (2026-08-12): payload shape, exit-2 block, and `~/.codex/hooks.json` / `<repo>/.codex/hooks.json` discovery all confirmed; hosted tools never fire hooks (their docs' caveat, ours too) |
  | Cursor (IDE) | plugin.json `hooks` key -> `hooks/cursor-hooks.json` | mostly — https://cursor.com/docs/agent/hooks (2026-08-12) confirms payload shapes and exit-2 block; the plugin-manifest `hooks` field (path or inline config) is documented at https://cursor.com/docs/reference/plugins. Two caveats: (1) the CWD plugin-shipped hook commands run from remains undocumented — official docs specify hook CWD only for project/user/enterprise/team sources, not plugin-manifest hooks; our `./contracts/...` command assumes the plugin root. The payload carries `cwd` on `preToolUse`/`beforeShellExecution`; `beforeMCPExecution`'s documented payload has none, only `workspace_roots`, which the adapter now reads (es#130). Discovery gathers EVERY candidate workspace (cwd first, then each root) and blocks if ANY of them blocks — a first-match policy let IDE-controlled root ORDER decide whether an armed guard fired at all. With no usable location the gate stays inert rather than searching from the hook process's own directory. **The `workspace_roots` entry shape is taken from docs prose, not a captured payload** — bare paths, `file://` URIs and `{uri}`/`{path}` objects are all accepted, so a wrong guess cannot silently turn the fallback into a no-op. (2) See the Cursor CLI row. |
  | Cursor CLI | NOT COVERED via plugin hooks | Cursor's own team confirmed (forum, 2026-06-24, unresolved as of 2026-08-12: https://forum.cursor.com/t/cursor-cli-ignores-hooks-from-marketplace-plugin/163890) that the CLI does not run plugin-installed hooks at all — only the IDE does. Until fixed, CLI-run missions need the hook additionally placed at `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user), the two sources confirmed to work on CLI. |
  | Gemini CLI | `~/.gemini/settings.json` BeforeTool snippet (`hooks/gemini-settings-snippet.json`) | yes — https://geminicli.com/docs/hooks/reference/ (2026-08-12): payload shape, exit-2 block, millisecond timeout; built-in tool names differ (`run_shell_command` etc.) so guards must name them |
  | Antigravity (agy) | NOT WIRED — needs its own hooks.json + a dedicated adapter (tracked follow-up) | the previous "shared `~/.gemini/settings.json` surface" claim is REFUTED by official docs: https://antigravity.google/docs/hooks (2026-08-12) — Antigravity reads `.agents/hooks.json` (workspace) or `~/.gemini/config/hooks.json` (global), never `settings.json`; its `PreToolUse` payload is `toolCall.name`/`toolCall.args` + `workspacePaths` (no `session_id`/`cwd`); blocking is a JSON `decision` field (`deny` etc.) with exit 0 always — exit-2 does not block. Third-party corroboration agrees on all load-bearing facts (medium.com/google-cloud/a-developers-guide-to-agent-hooks-in-antigravity-cli-4c1440febd11, atamel.dev/posts/2026/07-16_where_agy_hooks/) though the exact global-path spelling differs across sources. |
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
  The haystack is `json.dumps` output: backslashes and quotes in arguments
  are JSON-escaped before your regex sees them, so prefer matching on
  `host:port` substrings (e.g. `:7878/api`) over literal Windows paths.
  Unknown tool names are the operator's responsibility: the validator refuses
  silently-inert shapes only for the known shell / fs-write / `mcp__` classes.

  Mixed-fleet hazard: arming guards writes the new manifest fields into that
  mission's checkpoints, which pre-#117 plugin caches cannot validate (the
  armed mission reads as ChainBroken/unreadable there). Update every custody
  consumer before arming guards on a shared mission.
