> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)
>
> Post-release corrective work fixed the inert≠installed state machine; see tagged SKILL.md and successor progress notes.

# Watch

## What it does

Specifies and **proves** an external watcher that notices a crossed bound while nobody is looking. The skill is not itself a scheduler, probe, or alerting service.

A watcher that has never fired is not a watcher. `PROVEN` requires explicitly enabling the external mechanism, crossing the bound on purpose, and receiving the alert.

| State | Meaning |
|---|---|
| `DECLARED` | Bound, probe, destination, kill switch written down |
| `INERT` | Mechanism prepared/deployed but deliberately disabled — **not installed** |
| `PROVEN` | Enabled, proof-fired, alert received — the only "installed/watching" state |
| `SUSPECT` | Probe/delivery/proof failed or expired — treated as an alert |

## Use it when

- Something must be noticed between runs.
- First symptom of a condition would otherwise be an outage.
- An existing watcher must be proven to still fire.

## Do not use it when

- You want the current state right now → [`health`](Skill-Health).
- The condition is already known crossed and the cause is wanted → [`triage`](Skill-Triage).
- Nothing would change by learning about it late.

## Related

- Hands to: [`triage`](Skill-Triage), [`decision-ledger`](Skill-Decision-Ledger)

## Canonical sources

- [SKILL.md at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/watch/SKILL.md)
