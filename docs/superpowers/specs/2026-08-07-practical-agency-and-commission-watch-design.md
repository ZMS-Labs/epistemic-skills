# Practical Agency and Commission-Watch — design

**Date:** 2026-08-07  
**Status:** approved  
**Scope:** successor design for `epistemic-skills/watch` plus the boundary and seed-adoption contract for the existing `practical-agency` project

## Summary

### As-built cross-repo status

As of 2026-08-07, `ZMS-Labs/practical-agency` exists. Its inspected `main`
revision is `e244d534a6e26bc9a352846a25ffce18b8d93a53` and contains one initial root
`skills/manifest/SKILL.md`, root/Cursor plugin metadata, a README, and a v0
Markdown mission-manifest field guide. Cursor metadata declares `0.1.0`, but no
tag or GitHub release exists; that value is an unreleased seed version, not
evidence that the deterministic mission kernel has shipped.

**Landed (as-built):**

- Practical Agency repository identity and sole public entry skill `manifest`;
- unreleased seed packaging (root/Cursor plugin metadata, README, v0 guide);
- authorization-and-recording steward behavior in the seed `manifest` skill.

**Not established by repository existence alone:**

- installation of `manifest` in this or any harness;
- a compatible execution adapter;
- a persistent external observer;
- automatic `watch`→`manifest` routing.

That seed establishes the project identity and sole public entry skill. It is an
authorization-and-recording steward, not yet the approved mission driver: its
current trigger explicitly declines use when a current mission manifest already
governs the task, and its completion flow does not require an independent
acceptor. It also lacks the deterministic `mission-manifest@1` kernel, target
lifecycle, create/resume/reconcile/advance/verify/close modes, atomic checkpoints,
dynamic capability discovery, bounded return points, `"helix it"` compatibility,
and `watch-commission@1` intake described later in this document. The v0 guide's
`draft|active|hold|complete|cancelled` vocabulary is an input to migrate, not the
`mission-manifest@1` state machine.

All later repository shapes, lifecycle rules, invocation aliases, and handoff
diagrams are approved **target / planned architecture**, not claims about the
inspected external repository. Implementation must adopt the seed and preserve
the root `skills/manifest/SKILL.md` as the one canonical skill body rather than
create a competing copy.

PR #110 does not modify the external repository or verify its target kernel,
checkpoint, adapter, or intake behavior. It records the inspected seed baseline
above so this design does not reason from a nonexistent repository.
The PR creates no automatic `watch`→`manifest` route; generic outward transport
remains the truthful boundary until a versioned Practical Agency intake contract
is implemented, verified, and admitted. Consumption remains conditional on
installation and capability; no live observer is implied.

Two defects are resolved together:

1. `watch` was described in a way that blurred a prompt-time discipline, a specification, and the external mechanism that actually remains active between sessions.
2. The collection no longer has an actor that can receive an operator's high-level intention, preserve it across interruptions, coordinate workflow and epistemic capabilities, and continue until the intended state is independently established.

The decisions are:

- `watch` is a **commission-watch discipline**. It specifies, commissions, and proof-fires an **external observer**. It never claims that its Markdown instructions remain awake.
- The stable skill id remains `watch` through the current major line for compatibility. Its title, description, output contract, documentation, and tests use the unambiguous term **commission-watch**. A future major-version rename requires evidence that the migration benefit exceeds the compatibility cost.
- A separate project named **Practical Agency** owns durable mission control. Its repository is `practical-agency` and its sole public entry skill is **`manifest`**.
- Practical Agency is not an epistemic-skill suite. It is a mission-control system containing one public skill plus contracts, deterministic state logic, roles, adapters, evaluations, and documentation.
- `metacognate` remains the bounded epistemic governor. `gauntlet` remains an independent adversarial judge inside `epistemic-skills`. Neither becomes the mission actor.
- The phrase **"helix it"** remains a compatibility intent meaning: invoke `manifest` and coordinate the available workflow and epistemic layers in concert. No static Helix pair table returns.

## Problem statement

### The watch category error

Three distinct objects were previously called a watcher:

| Object | Reality |
|---|---|
| `watch` skill | Prompt-time instructions for deciding and proving what should be observed |
| watch specification | A durable record of the bound, probe, destination, safety controls, and proof requirements |
| external observer | A scheduler, event listener, monitoring service, human cadence, or other persistent mechanism that actually operates between sessions |

Only the third object watches. The first can create and validate a commission for the third. Treating the first as persistent creates false assurance precisely where silence is the failure mode.

### The missing actor

The v5 architecture correctly removed an enumerating router and a static workflow-to-epistemic pair table. `metacognate` now answers a bounded question: what must be true, what cannot presently be answered, which discipline owns that uncertainty, and where control should return.

That does not answer a different need:

> Given the operator's authorized will, what keeps the mission coherent, acts through available capabilities, preserves state, resumes after interruption, observes consequences, and continues until completion is independently established or authority is required?

That is mission control, not an epistemic discipline.

## Goals

Practical Agency must:

- preserve the operator's actual intent, authority, protected state, acceptable costs, and right to interrupt;
- create or resume one durable mission manifest;
- discover available capabilities rather than carry a hand-maintained inventory;
- invoke workflow and epistemic methods through their own published contracts;
- retain control-flow custody while bounded disciplines return control to the point of interruption;
- dispatch authorized execution through available adapters;
- checkpoint observed state and provenance after every material transition;
- survive session interruption without treating summaries or memory as ground truth;
- commission real unattended observation when an external substrate exists;
- state degradation and missing capabilities visibly;
- require independent acceptance for material completion claims; and
- stop on completion, revocation, an authority boundary, or a named unavailable substrate.

Commission-watch must:

- state clearly that it is a commissioning and proof discipline;
- distinguish its own execution from the external observer;
- emit a machine-checkable commission record;
- allow `BLOCKED` as an honest outcome when no execution substrate, destination, authority, or safe proof exists;
- preserve the existing no-silence, safe-proof, kill-switch, and no-auto-remediation rules; and
- never promote configuration presence, deployment, or unit tests into a claim that observation is active.

## Non-goals

This design does not:

- give an artificial agent independent ends;
- replace an ordinary workflow methodology;
- turn every internal mission operation into another public skill;
- reintroduce an exhaustive stage-to-skill pairing table;
- make `manifest` certify its own completion;
- make `commission-watch` a scheduler, daemon, monitoring provider, or actuator;
- require a cluster or a particular orchestration product;
- silently continue when operator authority is missing; or
- claim that a written plan, created task, deployed configuration, or green source-level test is a realized outcome.

## Architectural layers

```text
operator authority
    owns ends, permissions, protected state, acceptable cost, interruption
                         │
                         ▼
Practical Agency / manifest
    owns mission custody, continuity, capability coordination, next-action frontier
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
workflow methods               epistemic methods
    design / plan / build       know / derive / gate / verify
             └───────────┬───────────┘
                         ▼
execution substrates
    tools, repositories, agents, schedulers, monitors, humans, services
```

No layer may silently absorb another layer's authority:

- the operator supplies the ends;
- Practical Agency preserves and advances the mission;
- workflow methods structure work;
- epistemic methods decide what may bear load;
- execution substrates perform or observe persistent effects; and
- independent judges accept or reject material completion claims.

## Repository and public surface

The project title is **Practical Agency**. The repository slug is `practical-agency`.

Its initial public capability surface contains exactly one skill:

```text
manifest
```

Everything else begins as an internal contract, module, role, adapter, or evaluation. A supporting operation becomes another public skill only when it has all four properties:

1. an independent positive trigger recognizable without first invoking `manifest`;
2. a decision boundary distinct from "one phase of manifesting";
3. an independently useful output consumed outside a mission run; and
4. measured benefit sufficient to justify another resident description and another user-facing choice.

### Recommended repository shape

The existing root skill remains canonical. Each harness metadata surface uses
its native schema; surfaces that support an explicit skill-path field point at
`./skills`. No second independently editable skill tree or copied skill inventory
is introduced.

```text
practical-agency/
├── skills/manifest/SKILL.md
├── plugin.json
├── .cursor-plugin/plugin.json
├── .claude-plugin/plugin.json        # optional harness metadata; points at ./skills
├── contracts/
│   ├── mission-manifest.schema.json
│   ├── mission-event.schema.json
│   ├── checkpoint.schema.json
│   ├── capability-request.schema.json
│   ├── capability-result.schema.json
│   └── execution-receipt.schema.json
├── practical_agency/
│   ├── manifest_model.py
│   ├── state_machine.py
│   ├── authority.py
│   ├── capability_discovery.py
│   ├── coordinator.py
│   └── checkpoint_store.py
├── roles/
│   ├── mission-steward.md
│   └── independent-acceptor.md
├── adapters/
│   ├── generic-agent-skills/
│   ├── repository/
│   ├── scheduler/
│   └── execution-orchestrator/
├── evals/
├── examples/
└── docs/
```

The initial implementation is stdlib-first Python for deterministic contracts and state transitions, with Markdown for the portable skill and role surfaces. Adapters may use their native stacks behind narrow interfaces.

## The `manifest` public contract

### Invocation

The concise resident description should communicate:

> Use when the operator asks to make an intended outcome real through durable, coordinated, resumable work. Preserve authority and mission state, invoke available workflow and epistemic capabilities, act only through authorized substrates, and never self-certify material completion.

Explicit invocation is the normal path. This avoids turning a wide mission-control trigger into a tax on every routine task.

Supported compatibility intent includes:

- "manifest this";
- "make this real";
- "carry this through"; and
- "helix it".

### Mission-manifest object

A mission is represented by a durable `mission-manifest@1` record containing at least:

```yaml
schema: mission-manifest@1
mission_id: <stable id>
revision: <monotonic revision>

authority:
  operator_ref: <identity or local authority reference>
  instruction: <operator-authored or operator-approved intent>
  permissions: []
  protected_state: []
  acceptable_costs: []
  escalation_required_for: []
  revocation: <how authority is withdrawn>

outcome:
  desired_state: <observable durable end state>
  completion_proof: []
  integrity_guards: []
  scope_proof: []
  stop_conditions: []

truth:
  subject_refs: []
  verified_facts: []
  assumptions: []
  contradictions: []
  unknowns: []

state:
  status: draft|active|paused|blocked|verifying|completed|cancelled
  completed_actions: []
  current_frontier: []
  blockers: []
  next_action: <one bounded next action or null>

capabilities:
  discovered_at: <timestamp>
  available: []
  invoked: []
  unavailable: []
  degraded: []

continuity:
  prior_checkpoint: <ref or null>
  durable_artifacts: []
  decisions: []
  external_handoffs: []
  watch_commissions: []

integrity:
  actor_may_self_accept: false
  required_gates: []
  unresolved_verdicts: []
  completion_acceptor: <independent actor or null>
```

Operator instruction and approved amendments are append-preserved. The steward may interpret them into executable fields, but it may not rewrite the operator's source text in place.

### Lifecycle

```text
DRAFT ──operator approval──▶ ACTIVE
ACTIVE ──interruption──────▶ PAUSED
ACTIVE ──missing authority/substrate──▶ BLOCKED
ACTIVE ──proof bundle ready──▶ VERIFYING
VERIFYING ──independent pass──▶ COMPLETED
VERIFYING ──fail/inconclusive──▶ ACTIVE or BLOCKED
DRAFT|ACTIVE|PAUSED|BLOCKED|VERIFYING ──revocation──▶ CANCELLED
```

`COMPLETED` is unreachable from the mission steward alone for any material claim whose acceptance contract requires independence.

### Coordination loop

For each active mission revision:

1. Re-anchor the manifest to live artifacts and receipts.
2. Reconcile operator authority and revocation.
3. Discover the capabilities available in the current harness and environment.
4. Identify the smallest current condition that prevents justified progress.
5. Invoke the capability that owns that condition, if available.
6. Return to the exact interrupted mission point with the bounded result.
7. Dispatch one authorized execution step.
8. Observe the actual target or runtime, not merely the edited source.
9. Append a mission event and checkpoint the new state.
10. Repeat only while the mission remains authorized and a bounded next action exists.
11. Enter verification only when the complete proof bundle is ready.
12. Complete only on the required independent verdict.

The loop is driven by mission state, not by a static inventory or stage table.

## Capability discovery and invocation

Practical Agency discovers capabilities from installed package metadata and current harness facilities. It must not maintain a copied list of skill names.

A normalized capability descriptor includes:

```yaml
capability_id: <stable identity>
kind: skill|tool|agent|service|human|adapter
source_ref: <immutable or locally authoritative reference>
description: <resident trigger/role text>
input_contract: <schema or prose ref>
output_contract: <schema or prose ref>
authority_required: []
persistence: prompt|session|external
independence: actor|reviewer|either
availability: available|degraded|unavailable
```

Selection is condition-driven:

- the member owns whether its positive trigger is satisfied;
- `metacognate` may identify the bounded epistemic uncertainty;
- the workflow layer may own the current production stage;
- Practical Agency owns mission continuity and the point to which control returns;
- no member's result is silently softened, widened, or converted into another member's verdict.

## Relationship to `epistemic-skills`

### `metacognate`

`metacognate` remains the epistemic governor. It determines what would have to be true, which condition is not presently answerable, which discipline owns that uncertainty, and where control returns. It does not own the mission, execute the work, or persist between sessions.

### `gauntlet`

`gauntlet` remains in `epistemic-skills` because its owned decision is epistemic: whether a frozen consequential subject survives independent adversarial review. Practical Agency may prepare and submit the subject, but cannot choose the panel's findings, rewrite the computed verdict, or treat a non-GO as permission.

The mission actor and the court remain separate.

### `watch` as commission-watch

The stable skill id is `watch`; its canonical role name is **commission-watch**.

It owns one decision:

> What must be noticed between runs, which external mechanism could do so, and what evidence establishes that the complete observation and delivery path actually works?

It produces a `watch-commission@1` record. It does not run continuously.

## `watch-commission@1`

The carrier separates five facts that must never be collapsed:

1. **current operating state** — whether the observer is absent, blocked,
   disabled, currently trusted and enabled, or presently suspect;
2. **proof history** — either wholly absent or a complete end-to-end proof
   bundle, retained even after deliberate disablement;
3. **positive-claim evidence** — durable references supporting reachability,
   external persistence, kill-switch exercise, proof authority, and alert
   receipt;
4. **block evidence** — the checked missing or unproven dependency, observation
   time, and external receipt used only when current state is `BLOCKED`; and
5. **observed failure** — a separately typed, timestamped, receipted incident
   used only when current state is `SUSPECT`.

The JSON Schema is the structural carrier. The stdlib semantic verifier is the
cross-field oracle; a schema-valid record is not automatically trusted.

### Required fields

```yaml
schema: watch-commission@1
commission_id: <stable id>
subject:
  ref: <watched subject>
  revision: <revision or bounded dynamic identity>
bound:
  expression: <comparison>
  units: <units>
  direction: above|below|equals|changes|absent
  threshold: <scalar value>
probe:
  mechanism: <how state is observed>
  cadence_or_event: <when observation occurs>
  failure_modes: []
destination:
  ref: <recipient or endpoint>
  reachable: <boolean>
  reachability_receipt_ref: <durable evidence ref or null>
external_observer:
  substrate_kind: scheduler|event-listener|monitoring-service|human-cadence|other-external|fixture|null
  substrate: <provider/runtime/human-cadence label or null>
  mechanism_ref: <external id or null>
  persistence_receipt_ref: <durable evidence ref or null>
  persistent_outside_session: <boolean>
  enabled: <boolean>
kill_switch:
  procedure_ref: <reference or null>
  exercised: <boolean>
  exercise_receipt_ref: <durable evidence ref or null>
proof:
  authorized_by: <authority identity or null>
  authorization_ref: <durable authority ref or null>
  safe_crossing: <description or null>
  production_path: <boolean>
  bound_crossed: <boolean>
  alert_received: <boolean>
  received_at: <timestamp or null>
  alert_receipt_ref: <durable evidence ref or null>
failure:
  kind: probe|delivery|proof|freshness|kill-switch|external-mechanism|unknown|null
  detail: <observed failure or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable evidence ref or null>
block_evidence:
  detail: <checked missing or unproven dependency, or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable external check ref or null>
state: DECLARED|BLOCKED|INERT|PROVEN|SUSPECT
block_reason: <closed enum or null>
reprove_after: <timestamp/condition or null>
handoff:
  on_crossing: [triage, decision-ledger]
coverage_limits: []
```

`handoff.on_crossing` is closed to exactly `triage` and `decision-ledger`;
ordering is not semantic. It classifies possible epistemic consumers after a
real crossing, does not compel either to fire, and never denotes mission custody.

### State semantics

| State | Meaning |
|---|---|
| `DECLARED` | The commission specification exists; no external mechanism or proof attempt is implied. |
| `BLOCKED` | A required dependency was checked and found absent or unproven, the reason agrees with the recorded fields, dated block evidence exists, and the observer remains disabled. |
| `INERT` | A permitted external mechanism is persistence-proven, disabled, and governed by an exercised kill switch. Proof history is either wholly absent or complete. |
| `PROVEN` | The external mechanism is currently enabled, every positive claim is evidence-bound, the production path was safely proof-fired, and a re-proof boundary exists. |
| `SUSPECT` | A permitted external mechanism exists and a specific later failure is recorded with kind, detail, observation time, and receipt. Possible failure modes alone cannot establish this state. |

`state` reports the observer now. A successful proof followed by deliberate
disablement yields `INERT` with complete proof history retained. It does not stay
`PROVEN`, and the proof is not erased. Partial proof history is invalid because it
manufactures an easy-to-overread intermediate state.

Preparing or deploying a new persistent mechanism does not immediately earn
`INERT`. Until the real disable procedure has stopped that mechanism under
observation, the honest state is `BLOCKED: KILL_SWITCH_UNPROVEN` with dated block
evidence. Successful kill-switch exercise clears the block and yields `INERT`.
A pre-existing mechanism may enter `INERT` directly only when persistence and
kill-switch receipts already exist.

`BLOCKED` reasons are closed initially:

```text
NO_EXECUTION_SUBSTRATE
NO_REACHABLE_DESTINATION
NO_AUTHORITY_TO_ENABLE
NO_KILL_SWITCH
KILL_SWITCH_UNPROVEN
NO_SAFE_PROOF_CROSSING
PROBE_UNAVAILABLE
```

The semantic verifier rejects a reason contradicted by the record, such as
`NO_EXECUTION_SUBSTRATE` beside a populated external mechanism and persistence
receipt. Every `BLOCKED` record also requires `block_evidence.detail`,
`block_evidence.observed_at`, and an external `block_evidence.receipt_ref`.
Those fields are empty in all non-blocked states; a reason string or an agent's
unsearched inability to imagine a capability is not evidence of absence.

### Positive-claim, evidence, and promotion rules

A positive boolean never bears load alone:

- `destination.reachable: true` requires `reachability_receipt_ref`;
- `persistent_outside_session: true` requires `persistence_receipt_ref`;
- `kill_switch.exercised: true` requires `exercise_receipt_ref`;
- named proof authority requires `authorization_ref`; and
- `alert_received: true` requires both `received_at` and
  `alert_receipt_ref`.

A `BLOCKED` result likewise requires a dated evidence carrier naming the check
that established the missing or unproven dependency. The reason must agree with
the other fields. In particular, a prepared persistent mechanism whose disable
procedure is not yet exercised is `BLOCKED: KILL_SWITCH_UNPROVEN`, not `INERT`.

Evidence references using self-assertion, prompt/chat/session state, or remembered
model context are refused. An allowed substrate label cannot hide an obvious
`SKILL.md` or other prompt-time mechanism reference. A fixture is permitted only
for isolated contract/proof-path evaluation and must disclose fixture/test scope
and the unestablished production environment in `coverage_limits`.

`PROVEN` additionally requires:

- a permitted external `substrate_kind`, not skill text or chat state;
- populated substrate and external `mechanism_ref`;
- current enablement;
- a named reachable destination;
- an exercised and receipted kill switch;
- a complete proof bundle;
- safe crossing through the production observation and delivery path;
- observed bound crossing and alert receipt; and
- a dated or condition-bound `reprove_after` value.

`INERT` may retain that same complete proof bundle only while the mechanism is
currently disabled and its kill switch is already proven. `SUSPECT` may retain
historical receipts but requires its own later observed-failure carrier.
Configuration presence, source inspection, deployment, formatter tests,
self-asserted persistence, partial proof fields, generic failure possibilities,
bypass messages, and "no alert yet" cannot satisfy these rules.

### Runtime division

```text
commission-watch
    defines and proves the observation claim
                         │
                         ▼
future admitted mission-control intake (for example `manifest`)
    selects an authorized adapter, retains the commission, routes later events
                         │
                         ▼
external observer
    scheduler, listener, monitor, service, or human cadence that actually persists
```

Where an admitted, intake-capable Practical Agency mission-control layer is unavailable, commission-watch may still produce `DECLARED`, `BLOCKED`, or a provider-specific commission if the current harness can directly configure and prove an external observer. It must never infer intake capability from repository or package existence.

## Authority and integrity

Practical Agency extends the operator's agency through bounded delegation. It does not originate sovereign ends.

The following are invariant:

- operator-authored intent and explicit amendments are preserved verbatim;
- permissions are allowlisted, not inferred from ambition;
- protected state and acceptable costs are first-class;
- irreversible or materially consequential actions require prior scoped authority;
- revocation stops future dispatch and disables commissioned mechanisms where the revocation contract requires it;
- mission state never upgrades from a self-authored assertion alone;
- the actor that performed material work does not certify its acceptance;
- unavailable capabilities and failed adapters are visible state, not silent skips;
- a summary or remembered state is evidence to verify, not authority to continue; and
- no persistence claim is made without an external durable receipt.

## Degraded operation

| Condition | Required behavior |
|---|---|
| No durable store | Run may proceed only as a session-bounded mission; output states that resumption is unavailable. |
| No execution adapter | Preserve the mission and enter `BLOCKED`; do not substitute prose for action. |
| No epistemic package | Continue only for routine directly checkable work; mark unavailable gates and refuse claims requiring them. |
| No workflow package | Use the harness's native workflow while preserving mission and epistemic contracts. |
| No independent acceptor | Material completion remains `VERIFYING` or `BLOCKED`; never self-promote. |
| Capability description missing or dropped | Treat capability as unavailable; do not infer its body or identity from memory. |
| Watch substrate absent | `watch-commission@1.state = BLOCKED`, reason `NO_EXECUTION_SUBSTRATE`. |
| Checkpoint contradicts live state | Live state wins; record the contradiction and re-open affected decisions. |

## Description-budget posture

Practical Agency installs one explicit-entry skill. Its resident description must remain concise and include a clear decline boundary. Internal mission operations do not become separate skills merely to make them discoverable.

Package-local description checks are necessary but not sufficient. Supported harness verification must also inspect the loaded estate, because a separate repository still spends from the same harness-wide description budget.

## Evaluation strategy

### Commission-watch

The executable corpus must include controls that reject:

- skill text presented as a persistent observer;
- a deployed but disabled mechanism reported as installed;
- silence reported as health;
- a generic destination test substituted for the production delivery path;
- a proof crossing without explicit enablement;
- a proof crossing that creates the protected harm;
- a kill switch documented but not exercised;
- a `PROVEN` record with no external mechanism reference; and
- an unavailable substrate silently omitted rather than reported `BLOCKED`.

Positive controls must establish a real or isolated faithful adapter path from probe through destination.

### Practical Agency

The v1 corpus must include:

- intent preservation across multiple checkpoints;
- revocation before dispatch;
- protected-state refusal;
- capability discovery without a hard-coded member list;
- bounded epistemic interruption and exact return-point restoration;
- resumed state contradicted by live artifacts;
- adapter failure becoming visible `BLOCKED` state;
- commission-watch integration with a fake external observer;
- crash/restart recovery from the last committed checkpoint;
- independent acceptance required for material completion;
- a seeded actor-self-certification attempt rejected; and
- "helix it" resolving to the same mission semantics as explicit `manifest` invocation.

Tests follow red-green-refactor. Deterministic contract and state tests precede adapter implementation. No acceptance claim rests solely on the author reading its own green result.

## Migration and compatibility

### `watch`

- Keep directory and frontmatter id `watch` in the current major line.
- Change the resident description to lead with "commission or re-prove an external watch" and state that the skill itself does not watch.
- Change the visible title to `watch — commission and prove an external observer`.
- Introduce and validate `watch-commission@1`.
- Update live README/catalog language to **Commission Watch (`watch`)**.
- Preserve immutable v5.0.0 documentation as historical evidence.
- Record a future rename decision separately; do not force a breaking migration merely to improve prose.

### Helix compatibility

`helix` does not return as a skill, router, table, or package member. The phrase is accepted only as a user-facing compatibility intent:

> "helix it" = manifest this mission using the applicable workflow and epistemic capabilities in concert.

The mission driver discovers capabilities dynamically and asks each member to own its own trigger. Adding or removing a skill does not require editing a pair table.

## Repository boundary

`practical-agency` is a separate repository because its owned subject is the durable mission, not whether a claim may bear epistemic load. It has a different lifecycle, runtime surface, state store, adapter set, threat model, and release cadence.

It remains one repository at v1. Runtime or protocol extraction occurs only after at least two independent consumers require a separately versioned component or the release cadence becomes demonstrably incompatible.

## Acceptance criteria

This design is implemented when:

1. `watch`'s description and body unambiguously identify it as commission-watch.
2. A machine-checkable `watch-commission@1` contract and executable semantic verifier exist.
3. Tests prove `PROVEN` is unreachable without an external persistent mechanism and complete proof path.
4. Missing substrates produce explicit `BLOCKED` outcomes.
5. Live documentation distinguishes the discipline, commission record, and external observer.
6. `practical-agency` exists as a separate project with one public `manifest` skill.
7. `mission-manifest@1` and its deterministic state machine are executable and tested.
8. Capability discovery contains no copied inventory or static Helix pairing table.
9. A session can checkpoint, restart, re-anchor against live state, and continue without silently trusting memory.
10. Material completion requires the declared independent acceptor or gate.
11. A fake external observer demonstrates end-to-end commission-watch integration before any production adapter is claimed.
12. Supported harness evidence confirms that the one-skill package is actually loaded and callable.

## Naming

- Project/repository: **Practical Agency** / `practical-agency`
- Public skill: **`manifest`**
- Durable mission artifact: **mission manifest** / `mission-manifest@1`
- Acting role: **mission steward**
- Governance doctrine: **bounded delegated agency**
- Existing epistemic discipline: **Commission Watch (`watch`)**

The concise relationship is:

> `epistemic-skills` governs what may bear epistemic load. Practical Agency governs how authorized intent becomes durable action.
