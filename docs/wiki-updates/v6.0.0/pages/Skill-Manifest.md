> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)

# Manifest

## What it does

Custodies a **mission** — work too large, too consequential, or too
interruption-prone to survive in a chat transcript. It records who authorized
the scope, checkpoints progress durably, re-anchors when the work drifts from
its stated objective, and requires a **distinct acceptor**: the actor that did
the work never certifies its own completion.

It answers three questions a transcript cannot:

| Question | What custody provides |
|---|---|
| Will this survive interruption? | Hash-chained checkpoints under `missions/<id>/`, not conversation memory |
| Who authorized this scope? | A recorded authority, bound at mission open — see the scope caveat below |
| What makes "done" defensible? | Acceptance by an actor distinct from the one that executed |

## Use it when

- Work is mission-shaped: multi-session, consequential, cross-agent, or
  expensive to interrupt.
- The explicit phrase `manifest this` (or `/manifest`) is used — this is the one
  discipline besides `metacognate` you may invoke by name.
- A mission must be opened, resumed, advanced, verified, or closed.

## Do not use it when

- The work is routine one-step work checkable in-session. Custody on a
  reversible local edit is pure overhead.
- You want a decision remembered rather than a mission custodied →
  [`decision-ledger`](Skill-Decision-Ledger).
- You want an adversarial verdict rather than custody →
  [`gauntlet`](Skill-Gauntlet).

## The envelope is advisory at run time, compared at acceptance

Read this before relying on a declared scope. It is the easiest thing about
custody to misread, and the contract itself calls the misreading out.

**Nothing blocks a tool call on the envelope.** No `scope`, `permission`, or
`protected` field reaches the runtime chokepoint — that chokepoint is only ever
handed `authority`, so **only `authority.actuator_guards` can refuse an action**
before it happens. Declaring `scope.out` does not stop a write.

**But `scope` is not inert either.** At acceptance, path-pattern entries in
`scope.in` / `scope.out` are machine-compared against the receipted artifacts,
and a PASS is *refused* when work crossed the declared boundary — until a
**distinct acceptor** acknowledges each crossing path (`--scope-ack`). Prose
entries cannot be compared and are reported as uncomparable rather than silently
dropped; a `scope.in` mixing prose with patterns disables the include comparison
entirely and says so.

So: **advisory at run time, compared at acceptance.** Collapsing that in either
direction misleads — "the envelope constrains the agent" is false, and "nothing
refuses on it" is equally false.

Declare the envelope anyway. It is immutable, which makes it the fixed reference
an acceptor and an auditor compare finished work against, and it cannot be
retro-fitted later to match whatever the mission drifted into.

## Output

Durable state under `missions/<id>/` as `mission-custody@1` records — **never**
the chat. A mission that exists only in a transcript is not custodied.

## Security note for v6.0.0

The custody guard is the subject of this release's headline security fix
(es#137): three P1 false-allow bypasses and four P2 refusal gaps are closed.
Paths the guard previously allowed through those bypasses are now refused, and a
refusal fails closed with an explicit refusal rather than a silent no-op.

One residual limit is disclosed rather than fixed: `KL-GUARD-LEXICAL` — guard
path matching is lexical, so a write spelled through a **symlinked parent** can
resolve inside a guarded tree while the guard does not match it. If you rely on
custody to bound where an agent may write, read that limit before relying on it.

Platform limits also bound the guarantee: macOS custody lifecycle behavior is
unmeasured-or-red at this release (`KL-MACOS-162` — macOS default volumes are
case-insensitive under *full Unicode case folding*, in which `ß` folds to `ss`,
so `straße.txt` and `strasse.txt` are one physical file there; the contract's own
comparison is correct and does not fold, the filesystem does), and Windows
shipped with no native requalification (`KL-WINDOWS`).

## Related

- [Skill Catalog](Skill-Catalog)
- [Architecture and Contracts](Architecture-and-Contracts)
- [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations)
