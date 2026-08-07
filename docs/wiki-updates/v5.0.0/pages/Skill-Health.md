> **Applies to:** epistemic-skills v5.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/skills)

# Health

## What it does

Reports whether a running system is in the state it should be — and for each part of that answer, whether you actually looked. A roll-up containing any `UNKNOWN` is itself at best `UNKNOWN`. Absence of evidence never renders as healthy.

| State | Meaning |
|---|---|
| `OK` | Probed, within declared bounds |
| `WARN` | Probed, outside a soft bound |
| `CRITICAL` | Probed, outside a hard bound or required service down |
| `UNKNOWN` | Could not probe — never rendered as `OK` |

## Use it when

- You need the current state of a running system.
- Before a change with blast radius, after restart/power events.
- A health claim is about to bear load.

## Do not use it when

- A specific thing is already known broken and you want the cause → [`triage`](Skill-Triage).
- One metric you could read directly would answer it.
- The question is about a change you are making rather than the state you are in.

## Related

- Hands to: [`triage`](Skill-Triage), [`decision-ledger`](Skill-Decision-Ledger)
- Loop partners: [`watch`](Skill-Watch), [`did-it-land`](Skill-Did-It-Land)

## Canonical sources

- [SKILL.md at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/health/SKILL.md)
