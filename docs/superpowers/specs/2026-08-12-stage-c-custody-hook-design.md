# Stage-C custody enforcement hook — design (es#117)

Date: 2026-08-12
Issue: ZMS-Labs/epistemic-skills#117
Status: approved by operator (section-by-section, brainstorming session 2026-08-12); goal contract live in the executing session

## Provenance

- Tracer retro (`tracer-media-missing`, RETRO.md on vanta branch
  `mission/tracer-media-missing-record` @ `4540ddb`, ruling quoted in es#117):
  **"Build teeth (PreToolUse enforcement boundary earned)… scoped to the successor
  mission's real actuators (arr acquisition calls, filesystem moves), not built
  speculatively."**
- Manifest-efficacy evaluation (receipted into `media-library-rebuild` as
  `efficacy-eval-2026-08-12`): custody is convention-held; `effect` went unused for
  43/52 checkpoints of real work; no custody hook exists anywhere in the plugin.
- This design closes the loop the retro opened. It also carries the issue's second
  deliverable: the retro-consumption path (the README still says "Stage C is gated
  on the tracer retro" — after this PR, the ruling is recorded as consumed).

## Operator decisions (2026-08-12, brainstorming)

1. **Harnesses:** all harnesses epistemic-skills ships, plus Antigravity CLI (`agy`)
   and a generic adapter for the long tail.
2. **Enforcement staging:** inert → audit-only → enforce (SAFETY-1: ship inert).
3. **Guard rules location:** in the mission manifest, operator-approved, as additive
   optional fields within `mission-manifest@1` (no epoch bump).
4. **Gating mechanism:** Approach A — envelope-compiled gate. The manifest's
   machine-checkable guard rules ARE the gate; no per-action intent bookkeeping
   (the 43/52 adoption lesson: friction is where convention-held compliance dies).

## Data model (additive within `mission-manifest@1`)

Two optional fields inside `authority`:

```json
"authority": {
  "...": "existing fields unchanged",
  "guard_mode": "audit",
  "actuator_guards": [
    {
      "name": "arr-api-mutations",
      "tool_names": ["Bash"],
      "command_regexes": ["https?://[^\\s]*(7878|8989|8686|9696)[^\\s]*/api/"],
      "path_globs": []
    },
    {
      "name": "media-fs-moves",
      "tool_names": ["Bash", "Write", "Edit"],
      "command_regexes": ["\\b(mv|robocopy|rsync|Move-Item)\\b[^\\n]*[Mm]edia"],
      "path_globs": ["M:/Media/**", "//10.10.10.107/Media/**"]
    }
  ]
}
```

Semantics:

- **Guards absent → hook fully inert.** Installing the plugin changes nothing for
  any mission that does not opt in. This is the ship-inert state.
- `guard_mode`: `"audit"` | `"enforce"`; absent = inert even if guards exist.
- **Match:** a tool call matches a rule iff the tool name is in `tool_names` AND at
  least one pattern matches — `command_regexes` against Bash `tool_input.command`,
  `path_globs` against Write/Edit `tool_input.file_path`.
- **Match + audit mode:** allow; append one JSONL line to
  `missions/<id>/guard-log.jsonl`.
- **Match + enforce mode:** block (exit 2); stderr names the rule and the discharge
  path (amend the envelope or stop); the block is also appended to `guard-log.jsonl`.
- **Mode/guard transitions are authority changes.** Guards and mode are set at
  `open` via new `--guards-file` / `--guard-mode` flags (a file, to avoid argv
  bloat) and changed only via `amend` gaining the same two flags; the amend's
  verbatim operator text is the grant. Guard relaxation leaves the same paper
  trail as any authority change.
- **The hook never mutates chain state.** `guard-log.jsonl` is a side observation
  log (actor recorded as `hook:custody-gate` plus the payload's `session_id`), not
  a checkpoint. The chain stays writable only by declared stewards.
- **Deliberate over-matching bias** (per the handoff's error-direction lesson):
  a false block names its rule and is recoverable in-session via amend; a false
  allow silently retires custody of the exact actuator class the retro named.

## Gate evaluator (CLI)

New read-only verb in `custody_cli.py`:

```
python custody_cli.py gate --workspace <root> [--actor hook:custody-gate]
```

- Reads a normalized tool-call JSON on stdin (`--input-file` escape hatch).
- Resolves the single active mission pathlessly (same discovery as `resume`).
- Evaluates the call against the current checkpoint's manifest guards.
- Prints verdict JSON `{decision, rule, reason, mode}` on stdout.
- Exit 0 = allow, exit 2 = block (mirrors hook semantics).
- Never touches chain state; the only write is the `guard-log.jsonl` append on a
  match.

## Hook script

`contracts/mission-custody/custody_hook.py`, stdlib-only:

```
python custody_hook.py --harness <claude|kimi|codex|cursor|gemini|generic>
```

- Reads the harness payload from stdin; the named per-harness adapter normalizes it
  to `{tool_name, command?, file_path?, session_id, cwd}`.
- Calls the gate logic **in-process** (imports the contract modules — no subprocess
  layer, so no RULE-027 escaping surface and no extra process latency).
- Maps the verdict to the harness's blocking contract: exit 2 with the reason on
  stderr (claude/kimi/codex/generic), decision JSON on stdout where the platform
  uses one (cursor; gemini `BeforeTool` — exact schema verified at implementation).
- Any exception, malformed payload, or missing mission → exit 0 (fail-open,
  documented).
- `generic` adapter: normalized `{tool_name, tool_input}` JSON in, exit 0/2 out —
  the documented recipe for any harness with a PreToolUse-equivalent (Copilot CLI,
  OpenCode, Pi, Hermes, Grok, …).
- **agy** (Antigravity CLI) shares Gemini's `~/.gemini/settings.json` hook surface
  (`BeforeTool`), so the `gemini` adapter covers it; the docs say so.

### Fast path

The hook fires on every matched tool call in every session with the plugin enabled.
Inert must be near-free: one directory stat for `missions/`; no mission dir →
immediate exit 0. Armed: one checkpoint read + pattern evaluation. Timeout budget
10s configured; expected <200ms armed, <20ms inert.

## Harness wiring matrix

| Harness | Wiring artifact | Event/matcher | Status of contract |
|---|---|---|---|
| Claude Code | plugin `hooks/hooks.json` | `PreToolUse`, `Bash\|Write\|Edit\|mcp__.*` | Established on this fleet (safety_gate et al.) |
| Kimi Code | `.kimi-plugin/plugin.json` `hooks` array | `PreToolUse`, tool-name regex | Verified against official docs 2026-08-12 |
| Codex | `hooks/hooks.json` (user/project level; plugin-level support verified at implementation) | `PreToolUse`, `Bash\|apply_patch\|mcp__.*` | Docs-verify at implementation; hooks on by default in current builds |
| Cursor | `.cursor-plugin/plugin.json` `hooks` key → `hooks/cursor-hooks.json` | `beforeShellExecution`, `beforeMCPExecution`, `preToolUse` | Docs-verify at implementation |
| Gemini CLI (+ agy) | `gemini-extension.json` where supported, else documented `~/.gemini/settings.json` snippet | `BeforeTool` | Docs-verify at implementation |
| Generic | documented wiring recipe | any PreToolUse-equivalent | By construction |

**Docs-verification gate:** every per-harness wiring is verified against that
harness's official documentation during implementation; a wiring whose contract
cannot be confirmed from official docs ships marked unverified in the README table
rather than asserted.

## Fail-open disclosure (SECURITY.md)

Hooks fail open on error/timeout/crash on every platform (Kimi documents this
explicitly; Claude's contract is the same). SECURITY.md gains a section: the hook
is an enforcement layer over convention, not a sole barrier; denial travels only
via exit 2 / decision JSON; guards are only as good as their patterns; the
over-matching bias is stated.

## Retro-consumption edits (es#117 "also in scope")

- `contracts/mission-custody/README.md`: replace "Stage C (enforcement) is gated on
  the tracer retro" with the landed ruling — pointer to RETRO.md @ `4540ddb`, this
  design doc, and the hook's inert-by-default posture.
- `skills/manifest/SKILL.md` boundary bullet: updated to reflect that the hook
  exists and is armed per-mission; honest label remains where a mission has not
  opted in.

## Testing

- `test_custody_gate.py` (contract corpus style):
  - schema corpus — valid/invalid guard manifests; every `invalid-*` example MUST
    fail validation (the corpus is the regression suite);
  - gate evaluator — per-field match/no-match; modes inert/audit/enforce; no
    mission; mission closed; guard-log written in audit and enforce, not in inert;
    chain head hash + revision byte-identical across a gate evaluation;
  - hook end-to-end — each adapter's canonical stdin payload → exit 0/2; malformed
    payload → exit 0; Windows and POSIX path handling for globs.
- Live evidence-locked UAT (post-merge, per the goal contract): scratch mission,
  audit mode logs a guarded call; promote via `amend --guard-mode enforce`; enforce
  blocks with the named rule; on at least the Claude Code and Kimi wirings.

## Non-goals

- es#118 (contract@2: receipt-hash chaining + tail anchor).
- es#124 residue (superseded-receipt visibility; disclosed, not patched).
- Arming any live mission to enforce mode (operator act, not this PR).
- Speculative actuator coverage: the hook ships with **no** built-in patterns;
  policy is per-mission and operator-approved. The mechanism is generic; the rules
  are not ours to write.
- Actor-identity verification: hook payloads carry no custody actor; `session_id`
  is logged, not authenticated.
- O(n²) checkpoint storage (separately tracked, harmless at current revision).
