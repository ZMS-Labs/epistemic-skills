> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)

# Did-It-Land

## What it does

Answers whether a change is in effect on the thing that actually runs. Writing a control is not installing one. A green check whose oracle only read source does not establish a runtime claim.

| Verdict | Meaning |
|---|---|
| `LANDED` | Observed in effect at the runtime, after the revert window |
| `REVERTED` | Landed, then undone |
| `UNVERIFIED` | Could not observe the runtime — **the default** |

## Use it when

- A deploy, merge, config edit, guard, hook, or migration is believed applied.
- A fix is about to be called done and something depends on that.
- A check is green but its oracle only read source.

## Do not use it when

- The change is local, reversible, and directly observable in the same breath.
- Nothing yet depends on it having landed.
- You are still deciding what to change.

## Related

- Hands to: [`decision-ledger`](Skill-Decision-Ledger)
- Loop partners: [`health`](Skill-Health), [`triage`](Skill-Triage)

## Canonical sources

- [SKILL.md at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/did-it-land/SKILL.md)
