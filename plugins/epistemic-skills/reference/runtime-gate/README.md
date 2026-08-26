# Runtime tool-call gate — cooperative-agent-grade reference (issue #42)

**Design decision (2026-08-04, closing the probe's revisit condition):**
productized as an **optional per-harness adapter shipped as reference
machinery** — not a skill, not a default, not a security control.

## What it does

Binds the epistemic closure-control state to mechanical tool-call denial:
while the active `epistemic-process-trace@1` control is `hold` or
`escalate`, side-effecting tool calls are denied at the harness layer
before execution. This is the runtime half that `validate_trace.py`
cannot provide (issue #42's finding: a static validator sees only
self-authored declarations, never the action's runtime effect).

Verified behavior (2026-08-04 probe, 9/9 matrix, first execution):

| Control state | Side-effecting tool | Read-only tool |
|---|---|---|
| `hold` | **DENY** | allow |
| `escalate` | **DENY** | allow |
| `proceed` / absent | allow | allow |
| malformed event/state | **DENY (fail closed)** | DENY (fail closed) |

**The table is now executed**, by `test_hook.py` in this directory (wired into
`epistemic-flexibility.yml`). Until it was, three of its rows were false:
`MultiEdit` -- the standard multi-file edit path -- was permitted under
`hold`; every mutating MCP tool outside five `mcp__github__*` prefixes was
permitted; and an out-of-vocabulary `control` value (a typo, a number) read as
`proceed` rather than as the malformed state this table says must DENY. A
published behaviour table that nothing runs is a claim, not a control.

**What counts as side-effecting.** Built-ins: `Write`, `Edit`, `MultiEdit`,
`NotebookEdit`, `Bash`. MCP: any tool whose name carries a mutating verb
(`create`, `delete`, `write`, `patch`, `post`, `send`, `click`, `run`, ... --
the full set is `MCP_MUTATING_VERBS` in `hook.py`), in ANY namespace, because
an allowlist of GitHub prefixes has its blind spot exactly where nobody
enumerated. Deliberately over-broad in the safe direction: under `hold` a
false deny costs a retry and a false allow costs the action.

**Named residue:** a mutating MCP tool whose name carries none of those verbs
(`mcp__x__thing`) is still allowed. That vocabulary is the measured set, not a
proof of completeness.

## Honest boundary (read before trusting it)

- **Cooperative-agent-grade.** The control-state file's writer defines the
  trust boundary: an agent that writes `proceed` before acting defeats the
  gate. This is a mechanical step beyond document validation — it converts
  "the trace says hold" into "the harness refuses the push" — but it is
  **not adversary-proof** and satisfies no externally-enforced safety gate.
- **Harness capability labels:** Claude Code — supported (PreToolUse hook,
  `hook.py` here). Other harnesses ship no adapter until an equivalent
  pre-execution hook exists; absence of an adapter means NO runtime
  enforcement there, and no skill text may imply otherwise.
- A validator-owned (rather than agent-owned) state writer would strengthen
  the boundary; that substrate does not exist today and this reference does
  not pretend it does.

## Install (Claude Code, optional)

Register `hook.py` as a PreToolUse hook per your harness settings; the gate
reads `EPISTEMIC_CONTROL_STATE` (path to the state file, default
`.epistemic-control.json`: `{"control": "hold|escalate|proceed"}`).
Denials return the hook's structured deny decision with the active control
named, so the transcript records why the call was refused.
