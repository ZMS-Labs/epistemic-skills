---
name: watch
description: Use to commission or re-prove an external watch when a bound must be noticed between sessions. This skill specifies the bound, substrate, destination, kill switch, safe proof crossing, and alert receipt; it does not itself watch. Do NOT use for a current-state readout, diagnosis of a known crossing, auto-remediation, or a condition nobody will act on.
metadata:
  hands-to: [triage, decision-ledger]
---

# watch — commission and prove an external observer

> `watch` is the **commission-watch** discipline. It runs during an agent
> engagement and produces a validated `watch-commission@1` record.
>
> **The skill is not the external observer.** The observer is the scheduler,
> event listener, monitoring service, human cadence, or other mechanism that
> remains active after the engagement ends.
>
> This discipline owns one decision: **what must be noticed between runs, which
> external mechanism can notice it, and what evidence proves the complete
> observation and delivery path works?**

## Three objects, one honest boundary

| Object | What it is | What it is not |
|---|---|---|
| `watch` | the prompt-time commissioning and proof discipline | a daemon, scheduler, probe, recipient, or background actor |
| `watch-commission@1` | the durable specification and current commission state | evidence that an observer exists merely because the record exists |
| external observer | the real mechanism that probes, persists, and delivers alerts | this Markdown file or the agent session that read it |

Only the external observer operates between sessions. This skill may configure one
through an available adapter, but it never promotes its own instructions into a
persistence claim.

## States

| State | Meaning | Honest claim |
|---|---|---|
| `DECLARED` | bound, probe, destination, kill-switch requirement, and proof plan are specified | a commission specification exists; no mechanism is implied |
| `BLOCKED` | a required dependency is absent | no watch exists; the closed `block_reason` names why |
| `INERT` | a real external mechanism is prepared or deployed but disabled | the mechanism exists but is not watching |
| `PROVEN` | the mechanism is externally persistent, enabled under authority, proof-fired safely through the production path, and the alert arrived | the observer is currently watching; this is the only state that permits that phrase |
| `SUSPECT` | the mechanism, probe, delivery path, proof, or freshness failed or expired | observation cannot currently be relied upon; treat this as an alert |

A commission that has never completed an end-to-end proof is not an active watch.
It is `DECLARED`, `BLOCKED`, or `INERT`. Inspection, deployment, unit tests, and
silence cannot reach `PROVEN`.

```text
DECLARED -> BLOCKED  when a required commission dependency is absent
DECLARED -> INERT    when a real external mechanism is prepared disabled
INERT -> [authorized bounded enable + safe production-path crossing] -> PROVEN
INERT -> [proof abandoned or continuing operation not authorized]    -> INERT
any live/proof/delivery/freshness failure after a mechanism exists    -> SUSPECT
```

## Closed block reasons

A missing dependency is not `SUSPECT`; it is an explicit `BLOCKED` commission.
Use exactly one of:

| Reason | Meaning |
|---|---|
| `NO_EXECUTION_SUBSTRATE` | no scheduler, listener, monitoring provider, human cadence, or other persistent mechanism is available |
| `NO_REACHABLE_DESTINATION` | no recipient or endpoint can be reached and acted upon |
| `NO_AUTHORITY_TO_ENABLE` | the mechanism cannot be enabled or left operating under current authority |
| `NO_KILL_SWITCH` | the proposed mechanism has no bounded disable path |
| `KILL_SWITCH_UNPROVEN` | a disable path is described but has not stopped the real mechanism |
| `NO_SAFE_PROOF_CROSSING` | proving the path would create the protected harm or another irreversible condition |
| `PROBE_UNAVAILABLE` | the subject cannot be observed through the proposed probe |

`BLOCKED` is a successful act of epistemic honesty. It prevents “we should watch
this” from quietly becoming “we are watching this.”

## Iron constraints

These are conditions of commission, not preferences.

1. **The observer is external and persistent.** A skill, chat, source file, or
   configuration document cannot be the observer. `PROVEN` requires a real
   `mechanism_ref` whose operation survives this engagement.
2. **New mechanisms arrive disabled.** Preparation or deployment first yields
   `INERT`. Enablement is a separate, explicit, scoped act.
3. **The kill switch is exercised against the real mechanism.** Documentation is
   not proof. If the mechanism cannot be stopped without a code change or deploy,
   it remains `BLOCKED` or `INERT`.
4. **Probe failure is visible.** Error, timeout, authentication failure, and the
   inability to observe are not quiet skips. Once commissioned, they produce a
   `SUSPECT` condition and an alert path.
5. **The destination exists before enablement.** A log line with no reachable
   recipient is not an alert.
6. **The proof crossing is bounded and reversible.** Never cause the outage,
   data loss, exposure, or irreversible state the observer exists to prevent.
7. **The production path is the proof path.** A formatter test, source read,
   dry parse, or direct test message that bypasses the real probe and delivery
   chain cannot establish `PROVEN`.
8. **Noticing never implies fixing.** This discipline does not remediate. Any
   corrective action requires its own authority and workflow.
9. **No alert without an actor.** Do not commission a notification nobody has
   agreed to receive and act upon.

## Trigger

Fire when:

- a bound matters between agent runs and nothing currently observes it;
- the first natural symptom would otherwise be an outage, loss, or material
  degradation;
- someone is about to infer from a green health readout that they would be told
  if the condition changed;
- an external observer exists but has never completed an end-to-end proof; or
- a prior proof is old enough that liveness has become an assumption.

Do not fire when:

- the user wants the current state now — use `health`;
- the bound is already known crossed and the cause is wanted — use `triage`;
- learning late would change no action;
- a human reliably observes the condition on a cadence shorter than the harm;
- the request is to auto-remediate; or
- the only proposed “mechanism” is the skill or current agent session.

## Method

1. **Confirm that late notice changes an action.** Name the recipient and what
   they would do. If no action changes, decline rather than manufacture alert
   debt.
2. **Write the bound as a comparison.** Give it units, direction, and threshold.
   “Disk getting full” is not a bound; `free_space_percent < 15` is.
3. **Name the probe and its failure modes.** State how the subject is observed,
   when observation occurs, and what timeout, authentication failure, malformed
   output, or absence looks like. Those failures become alert conditions after
   commission.
4. **Name and reach the destination.** A generic delivery test may establish that
   the recipient exists. It does not yet prove the production alert path.
5. **Identify the external execution substrate.** Name the scheduler, listener,
   monitoring service, human cadence, or adapter that will remain active after
   this engagement. If none exists, emit `BLOCKED` with
   `NO_EXECUTION_SUBSTRATE` and stop.
6. **Emit and validate the initial commission.** Record the subject, bound, probe,
   destination, proposed observer, safety controls, proof plan, and current state
   in `watch-commission@1`.
7. **Prepare the real mechanism disabled.** Confirm the returned external
   `mechanism_ref`, persistence outside the session, and disabled state. The
   result is `INERT`, never installed or watching.
8. **Exercise the kill switch.** Use the smallest safe activity needed to show
   that the real mechanism is alive, invoke the disable path, observe that it
   stops without a code change or deploy, and return it to `INERT`. Failure is
   `BLOCKED: KILL_SWITCH_UNPROVEN` before ordinary operation, or `SUSPECT` for a
   previously commissioned observer.
9. **Authorize the bounded proof run.** Record the authorizing identity, scope,
   stop condition, and whether continuing operation after proof is authorized.
   Enabled-but-unproven is not `PROVEN`.
10. **Cross the bound safely through the production path.** Observe the actual
    probe detect the crossing and the real delivery path place an actionable
    alert at the named destination.
11. **Assign the current state from observation.** A complete receipt plus
    authorized continued enablement yields `PROVEN`. Probe, proof, or delivery
    failure yields `SUSPECT`. If the proof is abandoned or continued operation
    is not authorized, disable the mechanism and leave the current commission
    `INERT`; retain the proof-run evidence separately without claiming an active
    watch.
12. **Set the re-proof boundary.** Record the date or condition after which the
    current proof expires. Expiration yields `SUSPECT` until another deliberate
    production-path crossing succeeds.
13. **Hand real crossings to diagnosis and persistence.** This discipline notices
    only. `triage` determines cause; `decision-ledger` records consequential
    decisions or outcomes when its own trigger fires.

## Output

Every engagement that does not decline produces one complete
`watch-commission@1` JSON record conforming to:

```text
plugins/epistemic-skills/contracts/watch-commission/watch-commission.schema.json
```

Validate it with:

```bash
python plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py <record.json>
```

A structurally valid record is not automatically `PROVEN`; the semantic verifier
applies the state-specific promotion rules. `DECLARED`, `BLOCKED`, `INERT`,
`PROVEN`, and `SUSPECT` are all legitimate results. Only a validated record with
`state: PROVEN`, an enabled externally persistent mechanism, and a complete alert
receipt supports the present-tense claim “watching.”

When a mission-control layer is available, hand the validated commission record
outward so it can select an authorized adapter, retain the external mechanism
reference, checkpoint the proof receipt, and route later crossings back into the
mission. This package does not assume that layer is installed.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| “The skill will watch it” | The skill commissions and proves. Which external mechanism remains active after the session? |
| “The config is deployed” | Configuration presence is not observation. Disabled is `INERT`; missing substrate is `BLOCKED`. |
| “It has not alerted, so everything is fine” | Silence and observer failure look identical. Where is the last production-path proof receipt? |
| “The unit test covers alerts” | It may prove formatting. It does not prove the real probe, scheduler, delivery service, and destination. |
| “The destination received my test message” | A bypass message proves reachability, not the production observation path. |
| “The kill switch is documented” | Exercise it against the real mechanism. Until then it is a hypothesis. |
| “I will enable it now and prove it later” | Later is where unproven observers remain forever. Prepare inert; enable only as an authorized proof act. |
| “There is no safe test, but the configuration is obvious” | Emit `BLOCKED: NO_SAFE_PROOF_CROSSING`; do not manufacture danger or confidence. |
| “Just alert on everything” | Alerts nobody acts on become muted; muted is operationally indistinguishable from absent. |
| “It fired last month” | That is a dated proof. Has its re-proof boundary passed? |

## Degraded operation

| Condition | Required result |
|---|---|
| no persistent substrate | `BLOCKED: NO_EXECUTION_SUBSTRATE` |
| destination absent or unreachable | `BLOCKED: NO_REACHABLE_DESTINATION` |
| enablement or continued operation lacks authority | `BLOCKED: NO_AUTHORITY_TO_ENABLE` |
| no kill switch | `BLOCKED: NO_KILL_SWITCH` |
| kill switch not exercised | `BLOCKED: KILL_SWITCH_UNPROVEN` |
| no safe proof crossing | `BLOCKED: NO_SAFE_PROOF_CROSSING` |
| subject cannot be probed | `BLOCKED: PROBE_UNAVAILABLE` |
| prepared mechanism disabled | `INERT` |
| live probe, delivery, proof, or freshness failure | `SUSPECT` and an alert; never quiet success |
| contract verifier unavailable | retain the record as unverified; never promote it by inspection |

## Oracle

The failure is false assurance produced from silence or configuration presence.
The executable corpus must reject:

- this skill or another Markdown file presented as the external observer;
- a deployed-but-disabled mechanism reported as watching;
- a `PROVEN` record with no externally persistent `mechanism_ref`;
- silence reported as health;
- a destination test substituted for the production delivery chain;
- an unexercised kill switch;
- a proof crossing without prior scoped enablement;
- an unsafe crossing performed for ceremony; and
- a missing substrate silently omitted rather than represented as `BLOCKED`.

The positive control must exercise a faithful path from external probe through
external delivery to the named destination. A corpus that merely rejects every
record proves nothing.

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"watch","decision":"fired|declined","discipline_engaged":"watch|<name-or-null>","action_changed":true|false}
```

The append records use of the discipline. It does not prove that an external
observer was commissioned; only the validated commission and external receipts
can do that. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It may bind
concrete bounds, probes, destinations, adapter names, kill-switch procedures,
safe crossings, authorization rules, and proof-expiry policy. It may never treat
local configuration as proof or replace the external-observer requirement.
