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
| `watch-commission@1` | the durable specification, current operating state, proof history, block evidence, and evidence references | evidence that an observer exists merely because the record exists |
| external observer | the real mechanism that probes, persists, and delivers alerts | this Markdown file or the agent session that read it |

Only the external observer operates between sessions. This skill may configure one
through an available adapter, but it never promotes its own instructions into a
persistence claim.

## Current state, proof history, and blocking evidence are different facts

| State | Meaning | Honest claim |
|---|---|---|
| `DECLARED` | bound, probe, destination, kill-switch requirement, and proof plan are specified | a commission specification exists; no external mechanism is prepared |
| `BLOCKED` | a required dependency was checked and found absent or unproven | no active watch exists; `block_reason` and dated `block_evidence` say exactly why |
| `INERT` | a real external mechanism is persistence-proven, its real kill switch is exercised, and it is currently disabled | the mechanism exists but is not watching; a complete prior proof may remain as history |
| `PROVEN` | the mechanism is externally persistent, currently enabled under authority, proof-fired safely through the production path, and the alert arrived | the observer is currently watching; this is the only state that permits that phrase |
| `SUSPECT` | a specific mechanism, probe, delivery, proof, kill-switch, or freshness failure was observed and receipted | observation cannot currently be relied upon; treat the observed failure as an alert |

`state` reports the observer **now**. The `proof` object records an end-to-end
proof event and may outlive the state that followed it. A proof can succeed and
the mechanism can then be deliberately disabled; the honest result is `INERT`
with a complete historical proof bundle, not `PROVEN` and not erased evidence.
A partial proof bundle is invalid because it is easy to misread as end-to-end
validation.

`BLOCKED` is also evidence-bearing. A reason string alone cannot establish that
no substrate, authority, destination, kill switch, safe crossing, or usable probe
exists. Every blocked record carries the check performed, its observation time,
and a durable evidence reference. Those fields are empty in every non-blocked
state.

A commission that has never completed an end-to-end proof is not an active watch.
It is `DECLARED`, `BLOCKED`, or `INERT`. Inspection, deployment, unit tests, and
silence cannot reach `PROVEN`.

```text
DECLARED -> BLOCKED(NO_EXECUTION_SUBSTRATE) when discovery finds no external mechanism
DECLARED -> BLOCKED(KILL_SWITCH_UNPROVEN)   when a mechanism is prepared but its real disable path is not yet proven
BLOCKED  -> INERT                           after persistence and kill-switch evidence exist and the mechanism is disabled
INERT -> [authorized bounded enable + safe production-path crossing]
      -> PROVEN                             when continued operation is authorized and remains enabled
      -> INERT                              when proof succeeds but the mechanism is then disabled
any observed live/proof/delivery/freshness/kill-switch failure after a mechanism exists
      -> SUSPECT                            with failure kind, detail, time, and receipt
```

A pre-existing mechanism whose persistence and kill-switch evidence already
exist may enter `INERT` directly. Merely deploying a new mechanism does not.

## Closed block reasons

A missing or unproven dependency is not `SUSPECT`; it is an explicit `BLOCKED`
commission. Use exactly one of:

| Reason | Meaning |
|---|---|
| `NO_EXECUTION_SUBSTRATE` | capability discovery found no scheduler, listener, monitoring provider, human cadence, or other persistent mechanism |
| `NO_REACHABLE_DESTINATION` | a reachability check found no recipient or endpoint that can be reached and acted upon |
| `NO_AUTHORITY_TO_ENABLE` | the authority check does not permit the mechanism to be enabled or left operating |
| `NO_KILL_SWITCH` | the proposed mechanism has no bounded disable path |
| `KILL_SWITCH_UNPROVEN` | a real mechanism and disable procedure exist, but the procedure has not stopped that mechanism under observation |
| `NO_SAFE_PROOF_CROSSING` | the proof analysis found that crossing the bound would create the protected harm or another irreversible condition |
| `PROBE_UNAVAILABLE` | a probe attempt or capability check found that the subject cannot be observed through the proposed path |

The chosen reason must agree with the record. For example,
`NO_EXECUTION_SUBSTRATE` cannot coexist with a populated external mechanism and
persistence receipt; `KILL_SWITCH_UNPROVEN` requires a prepared persistent
mechanism and a named procedure that is not yet exercised. Every reason also
requires `block_evidence.detail`, `block_evidence.observed_at`, and a durable
`block_evidence.receipt_ref`.

`BLOCKED` is a successful act of epistemic honesty. It prevents “we should watch
this” from quietly becoming “we are watching this.”

## Iron constraints

These are conditions of commission, not preferences.

1. **The observer is external and persistent.** A skill, chat, source file, or
   configuration document cannot be the observer. The closed `substrate_kind`
   vocabulary permits schedulers, event listeners, monitoring services, human
   cadences, other external mechanisms, and isolated fixtures — never Markdown.
   Obvious skill, chat, prompt, session, or memory references are refused even
   when mislabeled as an allowed substrate kind.
2. **Positive claims carry evidence references.** Reachability, persistence,
   kill-switch exercise, proof authority, and alert receipt each require a
   durable receipt reference. A boolean without its evidence carrier is not a
   trusted fact. Self-asserted or prompt/session-memory references are not
   external evidence.
3. **Blocked claims carry evidence too.** The missing or unproven dependency, the
   time it was checked, and the external check receipt are mandatory. “I could
   not think of one” is not `NO_EXECUTION_SUBSTRATE`.
4. **Fixtures disclose their scope.** A fixture may prove the contract and an
   isolated faithful path; its coverage limits must explicitly say that it is a
   fixture/test and what production environment is not established.
5. **New mechanisms arrive disabled and blocked until controllable.** Preparing
   or deploying a mechanism does not yet earn `INERT`. Until the real kill
   switch has been exercised and receipted, the state is
   `BLOCKED: KILL_SWITCH_UNPROVEN`.
6. **The kill switch is exercised against the real mechanism.** Documentation is
   not proof. If the mechanism cannot be stopped without a code change or deploy,
   it remains `BLOCKED`.
7. **Probe failure is visible.** Error, timeout, authentication failure, and the
   inability to observe are not quiet skips. Once commissioned, an actual
   failure produces `SUSPECT` plus a failure kind, detail, time, and receipt.
8. **The destination exists before enablement.** A log line with no reachable
   recipient is not an alert.
9. **The proof crossing is bounded and reversible.** Never cause the outage,
   data loss, exposure, or irreversible state the observer exists to prevent.
10. **The production path is the proof path.** A formatter test, source read,
    dry parse, or direct test message that bypasses the real probe and delivery
    chain cannot establish `PROVEN`.
11. **Trusted proof has an expiry boundary.** `PROVEN`, and `INERT` records that
    retain a complete prior proof, name when or under what condition it must be
    re-proved. A proof with no freshness boundary silently becomes permanent.
12. **Noticing never implies fixing.** This discipline does not remediate. Any
    corrective action requires its own authority and workflow.
13. **No alert without an actor.** Do not commission a notification nobody has
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
2. **Write the bound as a comparison.** Give it units, one closed direction
   (`above`, `below`, `equals`, `changes`, or `absent`), and a scalar threshold.
   “Disk getting full” is not a bound; `free_space_percent < 15` is.
3. **Name the probe and its possible failure modes.** State how the subject is
   observed, when observation occurs, and what timeout, authentication failure,
   malformed output, or absence would look like. Possible failures guide design;
   they do not themselves establish that a failure occurred.
4. **Name and reach the destination.** A generic delivery test may establish that
   the recipient exists. Retain its reachability receipt. It does not yet prove
   the production alert path. If the check fails, emit
   `BLOCKED: NO_REACHABLE_DESTINATION` with dated block evidence.
5. **Discover an external execution substrate.** Search the capabilities actually
   available in the current environment and name the closed `substrate_kind`,
   provider or human cadence, and adapter that would remain active after this
   engagement. If none is found, emit `BLOCKED: NO_EXECUTION_SUBSTRATE` with the
   discovery receipt and stop.
6. **Emit and validate the initial commission.** Record the subject, bound, probe,
   destination, proposed observer, safety controls, proof plan, empty failure
   carrier, empty block-evidence carrier, and current state in
   `watch-commission@1`.
7. **Prepare the real mechanism disabled.** Confirm and retain the external
   `mechanism_ref` and a receipt establishing persistence outside the session.
   If the real kill switch is not already proven, the current result is
   `BLOCKED: KILL_SWITCH_UNPROVEN` with dated block evidence — not `INERT`.
8. **Exercise the kill switch.** Use the smallest safe activity needed to show
   that the real mechanism is alive, invoke the disable path, observe that it
   stops without a code change or deploy, and retain the exercise receipt.
   Success clears the block fields and yields `INERT`. Failure remains
   `BLOCKED: KILL_SWITCH_UNPROVEN` before ordinary operation, or becomes
   `SUSPECT` with a receipted observed failure for a previously commissioned
   observer.
9. **Authorize the bounded proof run.** Record the authorizing identity, durable
   authorization reference, scope, stop condition, and whether continued
   operation after proof is authorized. If authority is absent, emit
   `BLOCKED: NO_AUTHORITY_TO_ENABLE` with the authority-check receipt.
   Enabled-but-unproven is not `PROVEN`.
10. **Establish a safe crossing.** If no bounded reversible proof can exercise
    the real path, emit `BLOCKED: NO_SAFE_PROOF_CROSSING` with the analysis or
    test receipt. Do not create the protected harm to satisfy a ritual.
11. **Cross the bound safely through the production path.** Observe the actual
    probe detect the crossing and the real delivery path place an actionable
    alert at the named destination. Retain the alert receipt and receipt time.
12. **Assign current state without destroying proof history.** A complete proof
    plus authorized continued enablement yields `PROVEN`. A successful proof
    followed by deliberate disablement yields `INERT` with the complete proof
    bundle retained. An abandoned attempt leaves the proof bundle wholly absent;
    never persist a persuasive-looking partial proof as trusted history.
13. **Record actual failures separately.** A live probe, delivery, proof,
    freshness, kill-switch, or mechanism failure yields `SUSPECT` only when the
    record names the failure kind, detail, observation time, and receipt.
14. **Set the re-proof boundary.** Record the date or condition after which the
    proof no longer supports trust. Crossing that boundary creates a receipted
    `freshness` failure and `SUSPECT` until another deliberate production-path
    crossing succeeds.
15. **Hand real crossings to diagnosis and persistence.** This discipline notices
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

The record separates:

- **current operating state** — `DECLARED`, `BLOCKED`, `INERT`, `PROVEN`, or
  `SUSPECT`;
- **proof history** — wholly absent or a complete production-path proof bundle;
- **positive-claim evidence** — destination, persistence, kill-switch,
  authorization, and alert receipt references;
- **block evidence** — detail, observation time, and receipt for the missing or
  unproven dependency when state is `BLOCKED`; and
- **observed failure** — kind, detail, observation time, and receipt, populated
  when current state is `SUSPECT`.

A structurally valid record is not automatically trusted; the semantic verifier
applies the cross-field rules. Only a validated record with `state: PROVEN`, an
enabled externally persistent mechanism, a complete proof bundle, all required
receipts, and a re-proof boundary supports the present-tense claim “watching.”
A validated `INERT` record may preserve exactly the same proof history while
honestly saying the observer is currently disabled. A validated `BLOCKED` record
must show the check that established the block; it cannot be created from an
agent's unsearched assumption.

When a mission-control layer is available, hand the validated commission record
outward so it can select an authorized adapter, retain the external mechanism
reference, checkpoint the evidence receipts, and route later crossings or
failures back into the mission. This package does not assume that layer is
installed.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| “The skill will watch it” | The skill commissions and proves. Which external mechanism remains active after the session? |
| “I labeled it a fixture, so the skill path counts” | An allowed label cannot hide a `SKILL.md`, chat, prompt, session, or memory reference. The mechanism itself must be external. |
| “The receipt says self-asserted” | Self-assertion is not external evidence. Use a durable receipt produced by the capability, authority source, probe, or destination. |
| “I could not think of a monitor” | That is not `NO_EXECUTION_SUBSTRATE`. Show the capability-discovery check and its receipt. |
| “The config is deployed, so it is inert” | A prepared mechanism remains `BLOCKED: KILL_SWITCH_UNPROVEN` until the real disable path has been exercised. |
| “It has not alerted, so everything is fine” | Silence and observer failure look identical. Where is the last production-path proof receipt? |
| “The boolean says persistent” | What durable receipt establishes operation outside this session, and is the substrate type actually external? |
| “The unit test covers alerts” | It may prove formatting. It does not prove the real probe, scheduler, delivery service, and destination. |
| “The destination received my test message” | A bypass message proves reachability, not the production observation path. |
| “The kill switch is documented” | Exercise it against the real mechanism and retain the receipt. Until then the commission is blocked. |
| “The proof succeeded, so it is watching” | Only if the external observer remains enabled. Successful proof followed by disablement is `INERT` with proof history. |
| “Some proof fields are better than none” | A partial proof bundle is easier to overread than an explicit absence. Retain the complete proof or no trusted proof. |
| “These are possible failure modes, so the watch is suspect” | `SUSPECT` requires an observed failure with kind, detail, time, and receipt. Possibility is not an incident. |
| “I will enable it now and prove it later” | Later is where unproven observers remain forever. Prepare disabled; enable only as an authorized proof act. |
| “There is no safe test, but the configuration is obvious” | Emit `BLOCKED: NO_SAFE_PROOF_CROSSING` with evidence; do not manufacture danger or confidence. |
| “The fixture passed, so production is proven” | Fixture evidence proves only the disclosed isolated scope. It must explicitly name what production environment remains unestablished. |
| “Just alert on everything” | Alerts nobody acts on become muted; muted is operationally indistinguishable from absent. |
| “It fired last month” | That is dated proof evidence. Has its re-proof boundary passed, and what is its current state? |

## Degraded operation

| Condition | Required result |
|---|---|
| no persistent substrate after capability discovery | `BLOCKED: NO_EXECUTION_SUBSTRATE` with discovery evidence |
| destination absent or unreachable | `BLOCKED: NO_REACHABLE_DESTINATION` with reachability evidence |
| enablement or continued operation lacks authority | `BLOCKED: NO_AUTHORITY_TO_ENABLE` with authority-check evidence |
| no kill switch | `BLOCKED: NO_KILL_SWITCH` with capability evidence |
| mechanism prepared but kill switch not exercised | `BLOCKED: KILL_SWITCH_UNPROVEN` with mechanism and block evidence |
| no safe proof crossing | `BLOCKED: NO_SAFE_PROOF_CROSSING` with analysis evidence |
| subject cannot be probed | `BLOCKED: PROBE_UNAVAILABLE` with probe evidence |
| prepared mechanism disabled, persistence and kill switch proven, no prior proof | `INERT` with an absent proof bundle |
| proof succeeded and mechanism was then disabled | `INERT` with the complete historical proof and re-proof boundary retained |
| partial proof history | invalid record; clear or complete it before relying on the commission |
| live probe, delivery, proof, freshness, kill-switch, or mechanism failure | `SUSPECT` with failure kind, detail, observation time, and receipt; never quiet success |
| fixture or test substrate | state applies only to the disclosed isolated scope; no production claim |
| contract verifier unavailable | retain the record as unverified; never promote it by inspection |

## Oracle

The failure is false assurance produced from silence, configuration presence, an
unsearched absence claim, or an evidence field detached from the fact it
supposedly supports. The executable corpus must reject:

- this skill or another Markdown file presented as the external observer, even
  when it is mislabeled as an allowed substrate and fills every proof boolean;
- self-asserted, prompt, chat, session, or memory references presented as
  external evidence;
- a fixture whose coverage limits do not disclose its isolated/test scope and
  missing production coverage;
- a prepared mechanism represented as `DECLARED` or `INERT` before the real kill
  switch is exercised;
- a `BLOCKED` record without dated evidence, or with a reason contradicted by its
  other fields;
- a deployed-but-disabled mechanism reported as watching;
- a `PROVEN` record with no permitted external substrate or persistent
  `mechanism_ref`;
- positive claims with no evidence receipt reference;
- silence reported as health;
- a destination test substituted for the production delivery chain;
- an unexercised or unreceipted kill switch;
- a proof crossing without durable scoped authorization;
- an unsafe crossing performed for ceremony;
- `PROVEN` or complete historical proof with no re-proof boundary;
- partial proof history stored under `INERT`;
- `SUSPECT` inferred only from possible failure modes rather than a receipted
  observed failure; and
- a missing dependency omitted instead of represented as evidence-bearing
  `BLOCKED`.

Positive controls must accept:

- a currently enabled `PROVEN` observer;
- a currently disabled `INERT` observer that retains the same complete proof
  history;
- `SUSPECT` only when the later failure is independently observed and
  receipted;
- `BLOCKED: NO_EXECUTION_SUBSTRATE` only with a discovery receipt; and
- a prepared persistent mechanism as `BLOCKED: KILL_SWITCH_UNPROVEN` until its
  real disable path is exercised.

A corpus that merely rejects every record proves nothing.

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
safe crossings, authorization rules, evidence-receipt formats, block-evidence
procedures, and proof-expiry policy. It may never treat local configuration,
prompt/session memory, or self-assertion as proof, and it may never replace the
external-observer requirement.
