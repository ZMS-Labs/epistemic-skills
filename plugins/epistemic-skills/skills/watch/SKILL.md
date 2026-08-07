---
name: watch
description: Use when something must be noticed while nobody is looking — a bound that matters between runs, a condition whose first symptom would otherwise be an outage, or an existing watcher that must be proven to still fire. Do NOT fire when you want the current state right now (that is a health readout), when the condition is already known crossed and the cause is wanted, or when nothing would change by learning about it late.
metadata:
  hands-to: [triage, decision-ledger]
---

# watch — prove the external observer that notices a crossed bound

> Every other member of this collection answers when asked. This discipline
> specifies and proves an **external watcher** that acts unattended. The skill is
> not itself a scheduler, probe, or alerting service.
>
> Unattended observation inverts the ordinary risk: a watcher that stays silent
> because nothing is wrong looks exactly like a watcher that stays silent because
> it is broken.
>
> This skill owns one decision: **what must be noticed between runs, and how do I
> know the external watcher would actually tell me?**

## The state it must earn

A watcher is not a file. It is a claim that you will be told, and that claim has
exactly one honest state until proven.

| State | Meaning | Rule |
|---|---|---|
| `DECLARED` | bound, probe, destination, and kill switch written down | no runtime mechanism is implied |
| `INERT` | mechanism prepared or deployed but deliberately disabled | **not installed, not watching, and the only state in which a new mechanism may arrive** |
| `PROVEN` | enabled explicitly, then fired on a bound crossed **on purpose**, and the alert arrived | the only state in which it may be called installed or watching |
| `SUSPECT` | its probe failed, delivery failed, the proof failed, or the proof expired | treated as an alert, never as silence |

**A watcher that has never fired is not a watcher.** It is an intention with a
configuration file. `PROVEN` is not reachable by inspection, by unit test, or by
reasoning about the code — only by explicitly enabling the external mechanism,
crossing the bound, and receiving the alert.

The enablement used for proof is a **transient transition**, not a fifth trusted
state:

```text
DECLARED -> INERT -> [explicit bounded enable for proof] -> PROVEN
                      \-> any proof failure -> SUSPECT
```

Until the alert is received, the mechanism remains unproven even while temporarily
enabled. If the proof is abandoned, disabled, or inconclusive, return it to
`INERT`; never promote it by intent.

## Iron constraints

These are not defaults. They are the conditions under which this skill may create
or enable anything at all.

1. **Ships inert.** A newly authored external watcher is deployed disabled.
   Enabling it is a separate, explicit, scoped act. An autonomous observer that
   arrives already running has never been reviewed in its live form.
2. **Has a kill switch that has been exercised.** Not documented — *used*. The
   procedure that stops it must have been run against the real mechanism, and it
   must work without a code change or deploy. **If the kill switch is untested,
   the watcher stays `INERT`.**
3. **Reports its own failure to observe.** A probe that errors, times out, or
   cannot authenticate raises an alert. **Silent watcher failure is the worst
   outcome in this design** — it is indistinguishable from "nothing is wrong,"
   and it is the state a broken watcher decays into by default.
4. **Names its destination before it is enabled.** An alert with no reachable
   recipient is a log line.
5. **Uses a bounded, reversible proof crossing.** Deliberately crossing a bound
   must not create the outage, data loss, security exposure, or irreversible
   condition the watcher exists to prevent. If no safe proof exists, report
   `SUSPECT (unproven)` and escalate rather than manufacture danger.

## Trigger

Fires when:

- a bound matters *between* runs and nothing currently observes it;
- the first symptom of a condition would be an outage or data loss;
- a health readout is green and someone is about to conclude they would be told;
- an existing watcher needs re-proving — it has not fired in long enough that its
  liveness is now an assumption.

Does **not** fire when:

- you want current state now — that is a health readout;
- the condition is already known crossed and the cause is wanted;
- nothing would change by learning about it late;
- a human reliably looks at the thing on a cadence shorter than the harm.

## Method

1. **Write the bound as a comparison, not a feeling.** Give it units and a
   direction. "Disk getting full" is not a bound; a percentage is.
2. **Name the probe and its failure modes.** How is the bound observed, and what
   does the probe return when it cannot observe? That answer becomes an alert
   path, not a silence.
3. **Name the destination and prove it is reachable** before enabling the
   watcher. A generic test message is not yet proof of the production alert path,
   but it establishes that the destination exists.
4. **Deploy the external mechanism inert.** Confirm it is disabled and cannot
   perform unattended observation in this state. Record `INERT`, never
   "installed."
5. **Exercise the kill switch against the real mechanism.** Enable only the
   smallest safe proof activity needed to observe that it is alive, invoke the
   kill switch, and confirm the activity stops without a code change or deploy.
   Return the mechanism to `INERT`.
6. **Explicitly authorize and enable the bounded proof run.** This is the
   transition missing from a naive inert-to-proof procedure. Record who or what
   authorized it, its scope, and the stop condition. Enabled-but-unproven is not
   `PROVEN`.
7. **Cross the bound on purpose, safely.** Confirm the alert arrives at the named
   destination through the same path production will use, with enough content to
   act. A source read, dry configuration parse, or formatter unit test cannot
   satisfy this step.
8. **Assign the state from the observation.** Alert received through the real
   path: `PROVEN`. Probe, delivery, or proof failure: `SUSPECT`. Proof abandoned
   or disabled before completion: return to `INERT`. Never infer promotion from
   intent.
9. **Exercise the post-proof operating decision explicitly.** Leave the watcher
   enabled only when that state is authorized and its kill switch remains
   available. Otherwise return it to `INERT`; a successful proof does not itself
   authorize indefinite operation.
10. **Record the proof with a date.** A proof is perishable; liveness decays into
    assumption without one.
11. **Hand real crossings to diagnosis.** This skill notices. It does not
    diagnose and it does not remediate.

## Boundaries

- **Never remediates.** Noticing and fixing are different acts with different
  authority. An auto-remediating watcher is an unattended actuator with a consent
  problem, and this skill does not create one.
- **Never treats its Markdown instructions as the watcher.** The external probe,
  scheduler, delivery path, and recipient are the mechanism under proof.
- **Never claims installed before `PROVEN`.** `INERT` means prepared but disabled,
  not installed.
- **Never treats its own outage as quiet.** No probe result is not a good result.
- **Never adds a watcher whose alert nobody will act on.** A muted alert is worse
  than none: it costs attention and manufactures false assurance.
- **Never crosses a dangerous bound merely to satisfy the proof ritual.** Unsafe
  proof yields `SUSPECT (unproven)` and escalation.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "The config is deployed, so it is watching" | Deployed and disabled is `INERT`. Explicitly enable, cross the bound, and receive the alert. |
| "It has not alerted, so everything is fine" | Or it is broken. Those look identical. When did it last fire? |
| "The unit test covers the alert path" | The test proves the code can format an alert. It does not prove one arrives. |
| "I will enable it now and verify later" | Later is where unverified watchers live permanently. Enable only as a bounded proof act. |
| "The kill switch is documented" | Then run it against the real mechanism. Documentation is a hypothesis. |
| "It is inert; now I will cross the bound" | A disabled watcher cannot alert. The explicit proof enable transition comes first. |
| "Just alert on everything to be safe" | Alerts nobody acts on get muted, and muted is indistinguishable from absent. |
| "It fired last month, it is fine" | That is a proof with a date. Is the date still good? |
| "The skill will watch it" | The skill specifies the proof. Which external mechanism actually runs between sessions? |

## Degraded operation

| Condition | Behaviour |
|---|---|
| probe fails | **alert** and `SUSPECT`, never silence |
| destination unreachable | `SUSPECT`; a watcher that cannot deliver is not watching |
| kill switch untested | remains `INERT`; may not be enabled for ordinary operation |
| proof enablement unauthorized | remains `INERT`; no proof run occurs |
| no safe deliberate crossing exists | `SUSPECT (unproven)` and escalate; do not create harm to prove observation |
| proof expired | `SUSPECT` until re-proven by another deliberate crossing |
| bound undeclared or unitless | refuse to create; there is nothing to compare against |

## Oracle

The failure is silence, and silence passes every naive test. The fixture set must
assert:

- a **crossed bound produces an alert at the destination** — proven by an explicit
  enable followed by crossing, not by inspecting configuration;
- the pre-fix sequence **deploy inert -> exercise kill switch -> remain inert ->
  cross the bound** cannot reach `PROVEN`, because the watcher is still disabled;
- a **failed probe produces an alert**, not a quiet skip;
- an **unreachable destination is `SUSPECT`**, not success;
- a watcher that has never fired reports `INERT`, **never** installed;
- the **kill switch actually stops it** — exercised in the fixture, not asserted;
- a positive control exercises the same runtime and delivery path production uses;
  and
- an unsafe deliberate crossing is refused rather than performed for ceremony.

**One control must fail against a build that treats "no alert" as "no problem,"
and another must fail against the v5.0.0 inert-without-enable sequence, or the
suite proves nothing.**

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It binds
concrete bounds, probes, destinations, kill-switch procedures, safe proof
crossings, authorization rules, and the dates of the last proofs. This file must
stay free of them.
