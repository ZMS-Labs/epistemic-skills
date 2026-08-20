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
| Who authorized this scope? | A recorded authority, bound at mission open |
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
unmeasured-or-red at this release (`KL-MACOS-162` — case-insensitive filesystems
collapse two contract-distinct filenames into one physical file), and Windows
shipped with no native requalification (`KL-WINDOWS`).

## Related

- [Skill Catalog](Skill-Catalog)
- [Architecture and Contracts](Architecture-and-Contracts)
- [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations)
