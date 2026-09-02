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
`epistemic-flexibility.yml`). Until it was, several of its rows were false:
`MultiEdit` -- the standard multi-file edit path -- was permitted under
`hold`; every mutating MCP tool outside five `mcp__github__*` prefixes was
permitted; an out-of-vocabulary `control` value (a typo, a number) read as
`proceed` rather than as the malformed state this table says must DENY; and
five more built-ins were permitted under `hold` because the built-in denial
set was an allowlist nobody had tested from outside -- `KillShell`,
`TodoWrite`, `Task`, `Agent` and `SlashCommand`. A published behaviour table
that nothing runs is a claim, not a control.

**What counts as side-effecting.** Any tool -- built-in or MCP, in ANY
namespace -- whose name carries a mutating verb (`create`, `delete`, `write`,
`patch`, `post`, `send`, `click`, `run`, `kill`, ... -- the full set is
`MCP_MUTATING_VERBS` in `hook.py`), plus the built-ins `Write`, `Edit`,
`MultiEdit`, `NotebookEdit` and `Bash` by name, plus the delegating built-ins
`Task`, `Agent` and `SlashCommand`. Deliberately over-broad in the safe
direction: under `hold` a false deny costs a retry and a false allow costs the
action.

The verb test applies to built-in names for the same reason it applies across
MCP namespaces. The five built-in names were an allowlist exactly like the
five `mcp__github__*` prefixes, with the same blind spot. Measured against the
shipped built-ins under `hold` before that was closed: `KillShell`, which
terminates a running process, was allowed; so were `TodoWrite` and all three
delegating tools. Closing the MCP allowlist and leaving the built-in allowlist
open would have fixed one instance of a defect and left its sibling.

**Delegation is action.** `Task`, `Agent` and `SlashCommand` write nothing
themselves; they hand the work to another executor. Under `hold` that is the
evasion the control exists to prevent. "The subagent runs the same hook" is an
assumption about another process's configuration, not a property of this one,
and a gate that denies the edit while permitting the order to make it has
denied a spelling rather than an action.

**Known over-broad denials.** `TodoWrite` mutates only the agent's own task
list and is denied anyway, because `write` is in the vocabulary. That is the
safe direction working as stated, and it costs a held agent the ability to
record its own state; it is named here rather than left to be discovered.

**Named residue:** a mutating tool whose name carries none of those verbs
(`mcp__x__thing`, or an opaque built-in) is still allowed. That vocabulary is
the measured set, not a proof of completeness.

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
