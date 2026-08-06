---
name: watch
description: Use when something must be noticed while nobody is looking — a bound that matters between runs, a condition whose first symptom would otherwise be an outage, or an existing watcher that must be proven to still fire. Do NOT fire when you want the current state right now (that is a health readout), when the condition is already known crossed and the cause is wanted, or when nothing would change by learning about it late.
metadata:
  hands-to: [triage, decision-ledger]
---

# watch — a bound was crossed while nobody was looking

> Every other member of this collection answers when asked. This one is the only
> member that acts **unattended**, and that inverts its risk: an unasked skill
> that stays silent looks exactly like an unasked skill that is broken.
>
> This skill owns one decision: **what must be noticed between runs, and how do I
> know I would actually be told?**

## The state it must earn

A watcher is not a file. It is a claim that you will be told, and that claim has
exactly one honest state until proven.

| State | Meaning | Rule |
|---|---|---|
| `DECLARED` | bound, probe, and destination written down | the only state a new watcher may ship in |
| `INERT` | installed, deliberately disabled | **required** — see SAFETY-1 below |
| `PROVEN` | has fired once, on a bound crossed **on purpose**, and the alert arrived | the only state in which it may be called installed |
| `SUSPECT` | its own probe failed, or the proof has expired | treated as an alert, never as silence |

**A watcher that has never fired is not a watcher.** It is an intention with a
config file. `PROVEN` is not reachable by inspection, by unit test, or by
reasoning about the code — only by crossing the bound and receiving the alert.

## Iron constraints

These are not defaults. They are the conditions under which this skill may
create anything at all.

1. **Ships inert.** A newly authored watcher is installed disabled and enabled as
   a separate, explicit act. An autonomous actuator that arrives already running
   has never been reviewed in its live form.
2. **Has a kill switch that has been exercised.** Not documented — *used*. The
   procedure that stops it must have been run, and it must work without a code
   change or a deploy. **If the kill switch is untested, the watcher stays inert.**
3. **Reports its own failure to observe.** A probe that errors, times out, or
   cannot authenticate raises an alert. **Silent watcher failure is the worst
   outcome in this design** — it is indistinguishable from "nothing is wrong",
   and it is the state a broken watcher decays into by default.
4. **Names its destination before it is enabled.** An alert with no reachable
   recipient is a log line.

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

1. **Write the bound as a comparison, not a feeling.** A threshold with units and
   a direction. "Disk getting full" is not a bound; a percentage is.
2. **Name the probe and its failure modes.** How is the bound observed, and what
   does the probe return when it cannot observe? That answer becomes an alert
   path, not a silence.
3. **Name the destination and prove it is reachable** before enabling anything.
4. **Install inert.**
5. **Exercise the kill switch.** Then confirm the watcher is still inert.
6. **Cross the bound on purpose.** Confirm the alert arrives, at the destination,
   with enough content to act on. Only now may it be described as installed.
7. **Record the proof with a date.** A proof is perishable; liveness decays into
   assumption without one.
8. **Hand crossings to diagnosis.** This skill notices. It does not diagnose and
   it does not remediate.

## Boundaries

- **Never remediates.** Noticing and fixing are different acts with different
  authority. An auto-remediating watcher is an unattended actuator with a
  consent problem, and this skill does not create one.
- **Never claims installed before `PROVEN`.**
- **Never treats its own outage as quiet.** No probe result is not a good result.
- **Never adds a watcher whose alert nobody will act on.** A muted alert is worse
  than none: it costs attention and manufactures false assurance.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "The config is deployed, so it is watching" | Deployed is not proven. Cross the bound. |
| "It has not alerted, so everything is fine" | Or it is broken. Those look identical. When did it last fire? |
| "The unit test covers the alert path" | The test proves the code can format an alert. It does not prove one arrives. |
| "I will enable it now and verify later" | Later is where unverified watchers live permanently. Inert until proven. |
| "The kill switch is documented" | Then run it. A documented kill switch that has never been used is a hypothesis. |
| "Just alert on everything to be safe" | Alerts nobody acts on get muted, and muted is indistinguishable from absent. |
| "It fired last month, it is fine" | That is a proof with a date. Is the date still good? |

## Degraded operation

| Condition | Behaviour |
|---|---|
| probe fails | **alert** — `SUSPECT`, never silence |
| destination unreachable | `SUSPECT`; a watcher that cannot deliver is not watching |
| kill switch untested | remains `INERT`; may not be enabled |
| proof expired | `SUSPECT` until re-proven by another deliberate crossing |
| bound undeclared or unitless | refuse to create; there is nothing to compare against |

## Oracle

The failure is silence, and silence passes every naive test. The fixture set must
assert:

- a **crossed bound produces an alert at the destination** — proven by crossing,
  not by inspecting configuration;
- a **failed probe produces an alert**, not a quiet skip;
- an **unreachable destination is `SUSPECT`**, not success;
- a watcher that has never fired reports `INERT`, **never** installed;
- the **kill switch actually stops it** — exercised in the fixture, not asserted.

**One control must fail against a build that treats "no alert" as "no problem",
or the suite proves nothing.**

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It binds
concrete bounds, probes, destinations, kill-switch procedures, and the dates of
the last proofs. This file must stay free of them.
