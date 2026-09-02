> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)

# Triage

## What it does

Finds the cause of a known failure and stops there. A cause is established only by an observation that would have come out differently if the cause were something else. Fitting the symptom is not enough.

| Verdict | Meaning |
|---|---|
| `CAUSE` | Observation distinguishes this cause |
| `NARROWED` | Some candidates eliminated; cause not isolated |
| `UNKNOWN` | Could not observe enough |
| `NOT-BROKEN` | Report was wrong; subject within bounds |

## Use it when

- A specific subject is known broken or degraded and the cause is not established.
- A check went red, a deploy failed, a service is unreachable.
- A health readout named something wrong.

## Do not use it when

- You do not yet know whether anything is wrong → [`health`](Skill-Health).
- The cause is already established and you are applying the fix.
- The question is about a change you are making rather than a failure you face.

## Related

- Hands to: [`decision-ledger`](Skill-Decision-Ledger)
- After a fix lands, verify with [`did-it-land`](Skill-Did-It-Land)

## Canonical sources

- [SKILL.md at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/triage/SKILL.md)
