# Manifest and mission-custody usability completion contract

**Status:** revised execution charter; planning remains gated on a new frozen gauntlet  
**Date:** 2026-08-14  
**Source baseline:** `ZMS-Labs/epistemic-skills` main `af7b72fe0460876fb96a458daaa44c7b008449cf`  
**Portable-projection review:** PR #176, head tree `2374e7900b20530be3188221e74f4f72d5e63d2f` before this charter  
**Fleet surface baseline:** `ZMS-Labs/fleet-orchestrator` main tree `61274d9297f61c4d42cff36e0fc97bc2126aec22`  
**Related authorities:** issues #104, #118, #124, #129, #136-#142, #147-#151, #154, #157-#170, and #173

## Decision

`manifest` and `mission-custody` may be called **usable** only for an exact,
versioned product/surface profile whose real consumer boundary has been
observed. They are **completed** only when every applicable profile in a finite
support registry has either achieved its claimed cumulative tier or is
explicitly classified `not_applicable`, `unsupported`, or `unverified` with a
reason. Unknown products, surfaces, releases and channels remain `unverified`.

Repository presence, a valid `SKILL.md`, green source tests, a generated ZIP,
or successful installation does not by itself establish usability.

## Terms

- **Core**: the Python custody record, lifecycle, integrity, audit and CLI
  implementation under `contracts/mission-custody`.
- **Manifest**: the package-bound skill that instructs an agent to use the core
  while preserving authority, custody, resumption and independent acceptance.
- **Profile**: `product + surface + resolved_release_or_build + profile_revision + achieved_tier + custody_capacity_policy_revision + evidence_epoch`.
- **Projection**: deterministic host-native bytes derived from canonical source
  and a profile. A projection never becomes an authored procedure source.
- **Served bytes**: the exact files the host actually loads after installation,
  not the source tree or archive intended for installation.
- **Applicable profile**: a host surface capable of loading agent instructions
  or invoking a custody adapter. Model endpoints, API relays and communication
  gateways are not skill hosts merely because Fleet Orchestrator calls them
  surfaces.

## Normative gauntlet amendment: claim, authority, and recovery contract

This section is normative and supersedes any less-specific language elsewhere
in this document. It closes the planning-contract defects identified by the
gauntlet of the frozen `56ea8b675da64fe7310452dd3c559320b5a3be4440bda4ac0f0e06bbfe3d373e`
subject. It does not assert that an implementation has passed these rules.

### Claim identity and vocabulary

Every machine-readable and human-readable capability claim is keyed by:

`product + surface + resolved_release_or_build + profile_revision + achieved_tier + custody_capacity_policy_revision + evidence_epoch`

The generated vocabulary is the sole source for registry entries, receipts,
conformance results, completion summaries, and release notes. An unqualified
sentence such as “manifest is usable” or “mission-custody is complete” is
invalid. A valid statement names the exact claim key and one of these capacity
modes:

- `singleton-safe@1`: duplicate or overlapping active state deterministically
  blocks protected work and provides a recovery path; it does not serve two
  active missions;
- `n-active-unverified`: a reserved value that can never satisfy a usability
  gate; or
- a future versioned `n-active` policy that is awardable only after the four
  issue #173 kernels, a separately frozen concurrency design, a separate
  gauntlet GO, explicit operator authority, and live overlapping/disjoint
  proofs.

U3 means evidence-bearing custody workflow with actual actor separation. U4
means preventive native-boundary enforcement. Neither term may be rendered as
the other. A deliberately single-operator profile that cannot demonstrate
independent acceptance stops at U2; logical aliases do not simulate actors.

Schema validation must reject a missing claim dimension, an unrecognized
capacity policy, an unqualified usability string, a U4 claim without U3, and
any `n-active` award without the required authority artifacts.

### Frozen support baseline and denominator governance

Before the first profile probe or implementation PR boundary is planned, a
versioned support-baseline artifact must:

1. bind the Fleet source revision and every surface kind found there;
2. map every operator-required consumer to a concrete profile or to an explicit
   `not_applicable`, `unsupported`, or `unverified` record with rationale;
3. identify external profiles and publisher-only profiles separately;
4. retain every probe result, including failures, in append-only history; and
5. make any post-freeze removal, reclassification to a weaker claim, or scope
   reduction an explicit recorded operator decision.

An automated baseline diff must fail on an unmapped required consumer,
unexplained deletion, hidden failed profile, or unapproved scope reduction.
Finiteness remains essential: this rule prevents denominator gaming without
turning the claim into open-world universality.

### Authority-stage DAG

Work is divided into three non-interchangeable stages:

| Stage | Authorized objective | Reachable terminal | Required transition artifact |
|---|---|---|---|
| A | contract correction, four concurrency-safety prerequisites, core safety fixes, disposable two-surface evidence | `decision-ready-not-usable` | revised contract gauntlet GO plus custodied implementation plans |
| B | design and implement an N-active custody policy | `n-active-candidate` | explicit operator decision, frozen successor design, separate gauntlet GO, and prerequisite-kernel evidence |
| C | claim promotion, merge, release, catalog publication, or production rollout | exact bounded claim only | independent acceptance, green exact-head CI, live conformance evidence, and the separately required operator promotion decision |

Stage A may inject duplicate/overlap state only to prove deterministic blocking,
non-destructive recovery, and zero uncustodied effects while the singleton
remains enabled. It may not make concurrent missions operational. Mechanical
DAG validation must show that Stage A reaches its terminal without crossing a
Stage B or C edge, and that no full-usability terminal is reachable while the
N-active blocker is asserted.

### Per-operation fault, degraded-state, and recovery oracle

Before testing begins, each claimed profile must publish a decision table for
every applicable state-changing operation: mission effect, verification start,
close/accept, install, upgrade, rollback, uninstall, duplicate resolution, and
guarded action. Each row binds:

- the injected fault and exact cut point;
- protected-action and neighboring-action outcomes;
- maximum timeout and user-visible result;
- permitted durable state and forbidden residue;
- required receipt/checkpoint/audit evidence;
- the sole retry, reconciliation, or rollback procedure;
- the required terminal state after recovery; and
- the tier consequence of any non-conforming outcome.

Timeout, crash, malformed output, and interruption are not passed merely
because they were observed. A passing row yields the predeclared outcome,
zero unexplained durable mutations, no orphaned or silently missing evidence,
and a linked recovery record. A protected matched action allowed because a
trusted decision was absent, late, ambiguous, or invalid disqualifies U4.

### Executable U3 authority and lifecycle matrix

Each U3 candidate must bind an actor-and-authority matrix containing actual
principal identity, credential class, delegated/recovery paths, administrative
capabilities, and forbidden duty pairs. At minimum, executable negative tests
must prove:

- effect before approval is denied;
- the actual effecting actor is recorded;
- an effecting or approving actor cannot perform independent acceptance where
  separation is required;
- the read-only integrity/audit command mutates nothing;
- terminal cancellation without a non-empty byte-faithful reason is denied;
- an effect outside the resolved authorized scope is denied;
- duplicated active state cannot disarm the gate; and
- a planted re-enablement of each unsafe transition fails acceptance.

Primary, delegated, recovered, and impersonation-capable test credentials are
included when the profile exposes them. An intentionally single-operator
deployment records that limitation and cannot claim U3 by manufacturing
logical identities.

### Evidence-invalidating administration

Each profile must inventory principals capable of mutating canonical source
policy, projection or installed bytes, the support registry, profile/hook
configuration, mission stores, anchors, or audit continuity. Every such action
must produce an independently retained record containing actual actor, target,
before and after digests, outcome, time, and evidence epoch. The acting
credential must not be able to unilaterally rewrite both the governed state and
the only record of its change.

Before testing, the profile declares detection bounds for direct mutation and
audit interruption. Acceptance exercises both. Where reusable administrative
credentials or persistence exist, U5 also requires inventory, revocation,
ownership transfer, reinstall prevention, and recovery tests. Where they do
not exist, the profile records the scoped absence instead of performing
irrelevant offboarding theater.

### Evidence epoch, invalidation, workload, and scoped exposure

Every conformance result binds an evidence epoch and fingerprints the resolved
release/build, profile, installer bytes, installed tree, native trust boundary,
and applicable hook configuration. A change to any bound input demotes the
claim to `unverified` until the affected probes pass again; history is retained.

Each profile declares one maximum supported mission shape and the native host
deadline. Repeated close/accept trials at that bound must either complete in
time or take the declared non-mutating degraded path with evidence continuity
and no partial terminal transition. The claim says nothing about capacity
beyond that finite bound.

Each profile also inventories actual listeners, callbacks, public artifacts,
credential-bearing paths, and versioned external components. Every non-empty
class triggers its corresponding targeted exposure, credential, secret, or
version-vulnerability check and claim consequence. Empty classes are recorded;
a generic internet-exposure ceremony is not imposed on a profile with no such
path.

### Planning gate for this amendment

No implementation PR boundary may be treated as approved by this document
until a new frozen gauntlet confirms that the six planning-contract blockers
above are closed. After that review:

- unresolved P1 yields `NO-GO`;
- P1 closed with an applicable P2 open yields `CONDITIONAL`; and
- P1 and applicable P2 accepted yields `GO` for implementation planning only.

That GO still does not authorize N-active operation, singleton switch-off,
merge, release, production installation or mutation, destructive migration,
credential expansion, paid action, or wholesale stale-branch reuse.

## Normative round-2 closure: generated state and assurance schemas

This section is normative and supersedes inconsistent generic completion or
delivery wording below. It closes the round-2 gauntlet blockers against subject
`8b60c9b8e13aac425bd0b5e6908f0e2bad55715fbb4d630a0743503993bd3ddf`.
The required records are schemas and test oracles, not assertions that any
profile has already passed.

### `capability-claim@1` state machine

Historical achievement and current validity are orthogonal:

- `achieved_tier` records the highest tier once proved in an evidence epoch;
- `validity` is one of `verified`, `unverified`, `invalidated`, `unsupported`,
  or `not_applicable`;
- only `validity=verified` may render a current usability statement; and
- invalidation retains historical achievement and evidence but cannot render it
  as current capability.

The generated compatibility table is closed, not advisory:

| Capacity policy | Awardable tiers | Required overlap behavior |
|---|---|---|
| `singleton-safe@1` | U0-U4 | duplicate/overlap state blocks protected effects, recovers within the declared bound, and produces zero uncustodied effects; coexistence is neither required nor claimed |
| `n-active-unverified` | none | cannot render `verified` or usable |
| future authorized `n-active@N` | U0-U5 | overlapping and disjoint missions coexist under the separately approved policy and live proofs |

`singleton-safe@1 + U5`, `n-active-unverified + any tier`, a stale/changed bound
digest with `validity=verified`, and any `unverified` record rendered as usable
are schema errors. Registry, receipt, conformance result, completion summary,
and release-note renderers consume this one state machine and must agree on a
fixture corpus containing conforming singleton, fail-open singleton, N-active
without coexistence, conforming authorized N-active, invalidated historical,
and unsupported cases. No fixture enables N-active service.

### `evidence-invalidation-map@1`

The invalidation dependency map is total over every inventoried mutable target:
canonical source and source policy, support registry, IR/projection, installer
and installed/served bytes, profile, release/build, hook configuration, native
trust boundary, mission store, receipt/verdict chain, external anchor, audit
continuity, and each behavior-affecting external component.

Each entry binds affected claim keys, probes to rerun, immediate degraded
behavior, maximum detection bound, required independently retained record,
successor evidence epoch, and re-award rule. Mutation or detected drift moves
every affected claim out of `verified`; unaffected claims remain unchanged. A
governed mutation refuses or enters its declared fail-closed state when the
independent record cannot be retained. Epoch identifiers are non-reusable, and
re-award requires every mapped probe to pass in the successor epoch.

For U4, invalidation of the decision boundary takes effect before the next
protected action. For versioned behavior-affecting external components, the map
also binds scanner or advisory-source identity and version, snapshot time,
severity policy, maximum evidence age, matching-advisory reaction, and
unavailable/error behavior. A stale, unavailable, or blocking result demotes
only affected profiles to `unverified`; no paid intelligence source is implied.

Seeded dependency tests mutate each target class, remove the independent audit
sink, add one undeclared behavior dependency, and prove exact scoped demotion
and successor-epoch re-award.

### `operation-fault-matrix@1`

The operation denominator is generated from all lifecycle, installer,
profile/registry, and evidence-administration transitions, including open,
approve, effect, begin-verification, audit, reconcile, close/accept, cancel,
install, duplicate resolution, upgrade, rollback, uninstall, profile change,
anchor repair, and audit administration.

For each applicable transition the matrix crosses the applicable fault families
(timeout, crash, malformed output, interruption, denied evidence retention)
with at least these durable cut classes: before mutation, partial mutation,
after mutation before durable evidence, and after durable evidence before
acknowledgement. Every omitted cell carries a schema-validated
`not_applicable` rationale. Recovery is idempotent, has total attempt and time
budgets, and ends in a declared terminal or fail-closed escalation. Seeded
omissions, duplicate effects, orphan evidence, and unbounded recovery fail.

### Distinct evidence decision addresses

`stage-a-portability-spike@1` answers only `proceed`, `pivot`, or `narrow` for
the projection architecture and precedes every Stage-B/profile edge it can
invalidate. A failing spike mechanically blocks those edges.

`stage-c-exact-conformance@1` runs against the exact promotion candidate in a
fresh evidence epoch. Spike evidence cannot be reused as exact-candidate
conformance, and only exact conformance can support a tier award.

### Stage-C principal and revocation rules

Every machine-enforced promotion edge binds immutable principal identity,
credential class, incompatible duties, native pre-mutation enforcement point,
decision digest, and independently retained audit record. External/manual gates
are labeled as such and never described as native prevention. Before promotion
authority exists, positive tests use fixtures, dry runs, or disposable targets.

For any U3+ profile with reusable authority or persistence capable of mutating
claim-bound inputs, acceptance includes credential inventory, revocation,
ownership transfer, reinstall prevention, and recovery. A profile with no such
mechanism records the scoped absence. A profile that retains unrevocable
claim-mutating authority is capped below U3 or carries a non-usable trust-
dependent result; it cannot emit an unqualified current usability claim.

### `workload-oracle@1` and typed residuals

Before testing, each profile binds mission-shape dimensions, environment and
warm/cold state, trial count or deterministic proof basis, latency statistic or
quantile, allowed failure budget, safe-degraded counting rule, native deadline,
maximum detection SLO, and automatic tier consequence. Authority, integrity,
and false-allow properties have an allowed failure budget of zero. Missing
fields or threshold breaches mechanically fail or downgrade the claim.

`residual-disposition@1` binds issue, exact claim key, final-candidate
observation, linked falsifying probe, invariant and tier consequence, scope
narrowing, independent adjudicator, required operator authority, and evidence
epoch. A residual cannot waive a cumulative tier invariant. It is accepted only
when the exact claim excludes the affected capability and any scope reduction
has the required recorded authority.

### Scoped authentication and replay negatives

For each non-empty listener, callback, credential-bearing, or administrative-
request class, conformance tests applicable unauthenticated, blank/default,
stock, expired/revoked, wrong-scope, delegated/recovered, and impersonation-
capable credentials. Replaying a captured state-changing request produces no
second effect and no evidence discontinuity. Planted weak controls fail the
exact claim gate. Recorded empty exposure classes remain exempt from generic
internet ceremony.

## Normative round-3 closure: remaining planning conditions

This section is normative and closes the four P2 conditions against subject
`ee6abdb0207f4035e6d5a99b38d6438e92450d6ca3db9c0f5d1fdd78c9f14064`.

### `stage-a-portability-spike@1` binding and invalidation

The spike record binds exact source, IR, generator, transform, projection,
profile, host/release, installer, installed-tree, and consumer digests; evidence
epoch; outcome criteria; decision digest; and supersession rule. It contains the
complete set of downstream DAG edge identifiers that consume its portability
conclusion. A changed bound digest or newly discovered dependent edge
invalidates the decision and makes every affected edge unreachable until a
fresh spike passes. Omitted-edge, changed-input, stale-epoch, and spike-as-final-
conformance fixtures fail; the unchanged conforming fixture passes.

### Concrete material-boundary coverage

Every designed durable mutation, external effect, durable-evidence publication,
and acknowledgement boundary on an applicable path has a stable `cut_id`. The
operation/fault/cut-class matrix reconciles to these IDs; one representative
point cannot satisfy another ID. Adding or changing a material boundary without
updating the matrix and its injection oracle fails before acceptance. Every
critical `cut_id` reaches the declared bounded idempotent recovery or fail-
closed terminal with zero unexplained mutation, duplicate effect, or orphan
evidence. Instruction-level and unknowable runtime boundary enumeration are not
claimed.

### `inventory-completeness@1`

An authored profile inventory is reconciled against an independently executed
enumerator of runtime bindings, native host configuration, installed artifacts,
listeners/callbacks, credential-bearing routes, behavior-affecting external
components, and effective claim-mutating principals. The enumerator and the
authored inventory are produced through separate paths. An unexplained item,
missing enumerator, or enumerator error demotes the exact claim to `unverified`.
Each pilot plants one undeclared exposure or credential route and one undeclared
effective principal; both discovery paths must detect their positive controls
and block U3+ rendering on the omissions. Tests remain isolated and neither
scan production nor create real credentials.

### Scoped privileged-data access denominator

Each profile declares whether its exact claim contains confidential or
credential-bearing objects and enumerates applicable read, list, download,
export, backup, and bulk-copy routes plus effective principals. Every applicable
cell is natively denied or emits an independently retained, secret-safe record
binding actual principal, route/object class without secret content, outcome,
time, evidence epoch, detection/response bound, and claim consequence.
Delegated, recovered, revoked, wrong-scope, and impersonation-capable
credentials are covered where the route supports them. A planted silent export
fails conformance. Unavailable independent retention fails closed or demotes
the affected claim. Profiles with no such object or route record a validated
non-applicable rationale and incur no generic confidentiality ceremony.

## Normative round-4 closure: executable planning oracles

This section is normative and closes the round-4 P2 ruling set against subject
`d5fec845a55863e5f7e799546074184a59990ecb1a7079cf1b6dee673104ca72`.
The generated records below are the sole executable interpretation; the older
generic numbered sequence is non-normative and must be regenerated from them.

### `planning-dag@1`

One generated DAG replaces the prose delivery order. A fresh
`stage-a-portability-spike@1` and disposable two-surface result dominate every
profile or Stage-B edge they can invalidate. Concurrency prerequisite evidence,
a frozen successor design, separate gauntlet GO, and operator decision all
dominate every N-active edge. Reverse-order and missing-predecessor fixtures
have zero reachable paths. Generated prose must byte-bind the DAG digest.

### Controller-equivalence and offboarding

`authority-equivalence@1` resolves a controlling principal across human or
automation controller, primary, delegated, recovered, shared, service, cached,
and impersonation-capable credentials. A governed-state mutator and the
independent-record controller must have different equivalence identities.
Seeded dual-control credentials permit zero deletion, rewrite, suppression, or
false independent acceptance.

Where privileged data, audit, recovery, service, persistence, session, or
reinstall authority exists, `offboarding-proof@1` binds trigger, owner,
independent verifier, completion bound, credential/session/persistence
inventory, secret rotation or ownership transfer, and denial tests. After the
bound, every former-principal read, list, download, export, backup, bulk copy,
audit, recovery, session, and reinstall route denies and records the attempt.
Current authorized access may remain independently recorded. Empty classes
carry validated non-applicability.

### Authoritative initial denominator and success terminals

Before the first support freeze, `consumer-requirements@1` records the
operator-authorized issuer identity and decision digest, scope, revision,
required consumers, and external/publisher dispositions. Baseline creation
fails if any required consumer is omitted or silently weakened. Successor
epochs allow zero unexplained differences or unsigned scope reductions.

The state machine has separate terminals:

- `registry-disposition-complete`: every required consumer is classified; it
  is not a product-success or usability result; and
- `bounded-product-usable`: every operator-required applicable consumer has
  reached its operator-defined minimum tier under a current verified claim.

An all-unverified registry may reach only the first terminal and produces zero
completed/usable/success renderings.

### Independent material-boundary census

Stable `cut_id`s are reconciled against a separate static or executable
side-effect analysis plus disposable runtime instrumentation of material
reachable durable mutations, external effects, evidence publication, and
acknowledgements. A seeded undeclared material cut fails. The census reruns on
boundary-changing revisions and the exact candidate. It claims only material
reachable coverage, never unknowable runtime or instruction-level completeness.

### Threshold provenance and workload bulkheading

`workload-oracle@1` additionally binds threshold source and rationale, sampling
frame, trial-count rationale, statistic/quantile rationale, and planted slow,
over-budget, and just-over-bound controls. A one-trial empirical claim fails
unless it cites an accepted deterministic proof obligation and checker.

Each supported mission-shape dimension maps to a pre-mutation admission
predicate or isolated quota, queue, and retry budget. Just-over-bound and
sustained over-bound work cause zero durable mutation or evidence loss from
rejected work, while concurrent in-bound controls retain the profile deadline.
No service above the finite declared bound is promised.

### Class-complete inventories and public-artifact checking

One closed inventory vocabulary covers runtime bindings, host configuration,
installed artifacts, listeners/callbacks, credential routes, external
components, effective principals, public artifacts, repositories, buckets, and
publication destinations. Applicable planted omission, clean negative, and
enumerator-error controls are generated for every class. All omissions are
detected, clean negatives produce no false positives, and enumerator failure
demotes affected claims to `unverified`.

`exposure-secret-check@1` binds checker identity/version, snapshot time,
maximum age, independently reconciled target closure, unavailable/error
behavior, positive controls, and exact claim consequence. Synthetic omitted
destinations and planted secrets are detected. A stale, missing, errored, or
non-discriminating checker demotes only affected claims. Validated empty classes
remain unaffected; no publication or paid service is authorized.

### Claim-bounded U4 policy coverage

U4 coverage is generated from the exact policy and hook configuration. Every
claimed matcher, actuator class, exclusion, and material interaction binds a
matched deny, near-miss allow, failure-behavior case, and disarming mutation.
Omitted configured branches fail schema validation and protected false allows
have zero budget. When only one route is demonstrated, the generated claim is
route-specific and cannot render as policy-wide guarding.

### `failure-domain-map@1`

Inventoried dependencies used by multiple protected controls bind consumers,
blast radius, isolation/bulkhead/breaker or explicit shared-fate disposition,
degraded state, and recovery order. One undeclared shared dependency and loss
of each declared high-impact dependency are injected. Passing requires zero
protected false allows, zero orphan evidence, and bounded declared degradation.
Arbitrary all-pairs fault injection is not required.

### Safety-relevant timebase

Every profile binds civil-time authority and provenance for audit/freshness,
monotonic elapsed-time source for deadlines and retries, maximum skew, reboot
and rollback behavior, unavailable-time consequence, and non-reusable epoch
semantics. Backward jump, forward jump, reboot, and unavailable-time fixtures
produce zero stale-evidence false allows; unknown U4 freshness demotes before
the next protected action; attempt and time budgets terminate monotonically.

## Cumulative usability tiers

| Tier | Name | Required observation |
|---|---|---|
| U0 | structurally packaged | deterministic declared-byte closure, digests, provenance and non-release/release label are correct |
| U1 | discovered | a clean install followed by the host's real reload/new-session path lists or selects the skill |
| U2 | callable | the host invokes a positive-control standalone skill and produces a discriminating expected effect |
| U3 | custodied | `manifest` invokes the installed package-bound launcher and completes an interruption/recovery/independent-acceptance lifecycle without source-tree assumptions |
| U4 | guarded | a trusted native pre-tool boundary blocks a matched actuator and allows a neighboring unmatched actuator through the same boundary |
| U5 | fleet-operable | duplicate install, upgrade, rollback, uninstall, concurrent missions, telemetry, ownership and recovery are proven for the exact profile |

Tiers are cumulative. A profile cannot claim U4 without U0-U3. A host without a
native trusted pre-tool boundary may stop at U3 and must say that U4 is
`not_applicable` or `unsupported`; it may not inherit another surface's guard
claim.

Two separately useful completion statements follow:

1. **Core usable**: the local reference CLI achieves U3 and the contract's
   integrity, lifecycle, concurrency and acceptance gates pass.
2. **Fleet usable**: every applicable registered Fleet Orchestrator skill host
   achieves its declared tier, with U3 required for `manifest` and U4 required
   only where the profile claims native guard enforcement.

Neither statement means open-world universality.

## Finite support registry

The registry is derived from the pinned Fleet Orchestrator `SURFACE_KINDS`, then
classified by capability rather than name. Its first committed revision must
contain every current kind:

`codex`, `claude_code`, `cursor_agent`, `gemini`, `kimi_code`, `aider`,
`litellm`, `hermes`, `ollama`, `openclaw_memory`, `openclaw_browser`,
`openclaw_voice`, `openclaw_phone`, `acp_runtime`, `discord_gateway`,
`signal_gateway`, `imessage_gateway`, `vllm`, and `deepseek_harness`.

The initial classification is intentionally conservative:

- candidate skill hosts: `codex`, `claude_code`, `cursor_agent`, `gemini`,
  `kimi_code`, and `aider`;
- candidate adapter or composite hosts requiring empirical classification:
  `hermes`, `acp_runtime`, and `deepseek_harness`;
- non-skill execution/model/gateway surfaces unless future evidence changes the
  classification: `litellm`, `ollama`, `vllm`, the four `openclaw_*` kinds,
  and the three communication gateways.

`antigravity` is tracked as an external custody-hook profile because issue #129
already claims an adapter obligation, even though it is not in the pinned Fleet
Orchestrator surface list. ChatGPT/plugin and GitHub Copilot distribution may be
tracked as publisher profiles but do not silently expand the fleet denominator.

Every profile record must bind:

- product, surface, release/channel, profile revision and observation date;
- official source URLs and the observed host version;
- native manifest, skill roots, recursion/parent rules and resource path base;
- installation, trust/consent, reload and subagent visibility behavior;
- hook event, input schema, CWD/root semantics, output protocol, timeout/crash/
  malformed-output behavior and exact guard exclusions;
- source, IR, projection, installed-tree and conformance-result digests;
- achieved tier and explicit non-achieved reasons;
- installer, upgrade, rollback, duplicate and uninstall evidence; and
- evidence retention location and privacy classification.

## Completion blockers in the current custody core

Green tests are not a completion oracle: current tests intentionally assert
that draft effects are legal, multiple active missions make the gate inert and
allow, and an empty path glob stays inert. The following issue families must be
resolved or explicitly adjudicated as a disclosed non-blocking residual.

### A. Authority and lifecycle

- #149: no artifact or external effect may be receipted while status is `draft`;
  approval must precede effects.
- #148: actual performing actors, not only the static initial steward, must be
  recorded and excluded from independent acceptance.
- #138: the lifecycle transition must be named `begin-verification`; a separate
  read-only integrity/audit command must mutate nothing.
- #139: terminal cancellation requires a non-empty byte-faithful reason.
- #154: mission-store durability mode must be declared and observable; the
  untracked-and-unignored state cannot be silent.

### B. Integrity, receipts and acceptance

- #118 contract@2: chain receipt hashes, acceptance-verdict hashes and an
  external tail anchor; provide version-aware degraded readers, migration,
  rollback and anchor-repair refusal semantics before the first @2 write.
- #124: re-probe the remaining phantom-reconciliation residue after #118;
  receipt continuity remains a separately surfaced finding.
- #147 and #164: bind resolved artifact identity and link-count evidence at
  effect time so later alias removal cannot erase a finding.
- #151: close the `scope.in` resolved-path gap, disclose uncompared entries to
  the acceptor and cover the missing CLI surfaces.
- #169: an effect that fails before receipt/checkpoint publication must not
  leave unreceipted parent mutations; degraded acceptance probes must be loud.
- #161: mandatory close/acceptance work must be linear enough to remain usable
  at the measured 800-receipt scale.

### C. Enforcement and native boundaries

- #137: close the three false-allow paths and four refusal/API gaps; every new
  regression must prove RED against the vulnerable behavior.
- #141: path guards require a scoped target and cannot false-block an unrelated
  workspace.
- #142: capture real payloads through real host boundaries; documentation prose
  is not wire-format evidence.
- #129: Antigravity remains `unverified` until its native configuration,
  payload and block output are live-fired.
- #136: Cursor CLI installation must use an installed absolute launcher from an
  unrelated CWD; the IDE profile is a separate claim.
- #168 and #173: operator regexes require bounded validation-time cost and exact
  disclosed anchor semantics.

### D. Concurrent missions — issue #173

The existing singleton refusal is the safe interim state. Naively permitting N
missions is prohibited by the prior deep-gauntlet `NO-GO`. These four kernels
must land before any N-permitting implementation:

1. Cross-mission drift suppression and non-destructive reconciliation must land
   before any `load_all` path.
2. Regex cost must be bounded during validation.
3. The fail-open inversion and a duplicate-resolution verb above the
   `Mission.load` funnel must ship together.
4. Any CHARTER migration must use the conjoin reading and refuse unmigrated
   stores.

The successor design must then prove:

- block-wins conjunctive guard routing across every applicable active mission;
- non-spoofable session-to-mission binding for lifecycle mutations;
- artifact ownership/conflict semantics that do not convert a sibling receipt
  into tampering or permit destructive reconcile loops;
- fairness and deterministic ordering when missions contend;
- explicit selection, list, inspect, park/resume or terminal resolution verbs
  without making pre-upgrade readers fail open;
- migration or durable quarantine of synthetic scratch-workspace missions; and
- a two-active-mission live proof with one overlapping and one disjoint case.

### E. Cross-platform and record fidelity

Windows, Linux and macOS are separate profiles. #140, #157-#160, #162, #163 and
#170 must be fixed or result in an explicit platform limitation. Control
characters, spaces, backslashes, comma-bearing paths, case folding, trailing
dots and paste-safe acknowledgements require byte-level fixtures. #167 remains
a disclosed display-identity residual unless a structured principal identity
design supersedes it.

### F. Semantics, adoption and residuals

- #150's typed `{path, kind}` acknowledgement belongs in contract@2. A
  steward-authored grant is not an authority control.
- #166's effect-shaped mission gap must be resolved by a typed enforceable
  effect condition or by narrowing the public claim to file-shaped custody.
  The adoption window closes 2026-10-13 and cannot substitute for runtime
  evidence.
- #104's successor release gate requires a complete supported-harness matrix
  and independently isolated gauntlet.
- #145 is a public-release privacy blocker, not a runtime capability claim.
- #165 is a recorded null review result, not an implementation blocker or
  positive assurance.

No issue is closed merely because a neighboring patch landed. Each issue is
reproduced at the final candidate or closed with a linked falsifying probe.

## Two-surface walking skeleton

The first empirical pilot uses two deliberately different profiles:

1. Claude Code CLI plugin installation: package root, native skill discovery
   and native hook configuration.
2. Codex CLI project/user skill installation: filesystem skill discovery plus
   an explicit installed launcher path for package-bound custody resources.

If either exact surface is unavailable, substitute only after recording why the
replacement is at least as discriminating. The pilot uses the same source
revision and tests both a simple positive-control standalone skill and
`manifest`.

For each profile, in an isolated temporary home and workspace:

1. Record executable version, channel and official docs.
2. Install only generated projection bytes; source checkout must be absent from
   the runtime search path.
3. Read back served files and compare the installed-tree digest.
4. Start a fresh session and prove discovery.
5. Invoke the positive-control skill and prove a discriminating expected
   effect; invoke a neighboring non-skill prompt to prove the oracle is not
   always green.
6. Invoke `manifest` and open a mission using the installed package-bound
   launcher from an unrelated CWD.
7. Prove draft effects refuse, approval enables them, interruption/resume sees
   a deliberate drift, reconciliation is non-destructive and a distinct actor
   performs acceptance.
8. When the profile claims U4, prove one matched tool call blocks and one
   neighboring unmatched call allows through the same native hook. Probe
   timeout, crash and malformed output; record whether the host fails open or
   closed.
9. Install a duplicate and prove deterministic refusal or ownership resolution.
10. Upgrade, rollback and uninstall; prove no stale discovery, hook or custody
    state remains.
11. Dispose the temporary home/workspace and retain only minimized evidence.

The pilot passes only when profile differences are declarative and generated.
Any duplicated procedure logic, source-checkout dependency, parser-specific
behavioral fork or unbounded executable transform fails the architecture and
forces a pivot to first-class surface overlays, a broker/native extension, or a
narrower support claim.

## Delivery sequence generated from `planning-dag@1`

1. **Contract and denominator:** land only the reviewed contract, authoritative
   consumer-requirements record, finite support baseline, generated schemas,
   seeded fixtures, and non-release controls on the review branch.
2. **Stage-A portability spike:** run the disposable two-surface spike against
   exact bound inputs. A failed `proceed/pivot/narrow` result blocks every
   dependent profile or Stage-B edge.
3. **Core lifecycle safety:** separate test-first PRs for current draft-effect,
   actor, verification, cancellation, durability, false-allow, and scope flaws.
4. **Contract@2 reconstruction:** rebuild on current main with versioned readers,
   tail anchor, migration/rollback, and the adversarial evidence corpus; never
   merge the stale branch wholesale.
5. **Identity, integrity, and oracle schemas:** implement actual-principal and
   equivalence identity, receipt/path/link evidence, invalidation, fault/cut,
   inventory, workload, timebase, failure-domain, and residual schemas with
   Linux/Windows/macOS fixtures.
6. **Concurrency prerequisites:** implement and independently review only issue
   #173's four prerequisite kernels while the singleton remains enabled.
7. **Concurrency decision boundary:** freeze the successor N-active design,
   obtain a separate gauntlet GO and explicit operator decision. Without all
   three artifacts, no N-active implementation edge exists.
8. **N-active candidate:** if and only if step 7 passes, implement block-wins
   routing, session binding, ownership/conflicts, deterministic ordering,
   lifecycle verbs, migration/quarantine, and overlapping/disjoint proofs.
9. **Profiles and installers:** implement only profiles whose Stage-A conclusion
   is current; use deterministic projections, installers, and digest-bound
   conformance artifacts.
10. **Stage-C exact conformance:** in a new epoch, run every applicable exact-
    candidate profile. Spike evidence is inadmissible for tier award.
11. **Fleet consumption and UAT:** consume only source-owned digest-bound
    projections and observe the deployed consumer, not repository configuration.
12. **Independent acceptance and promotion decision:** a non-implementing actor
    evaluates exact-head evidence. Merge, release, publication, and production
    rollout remain separately authorized actions and are re-observed after the
    landing window.

## Completion gates

The exact release candidate is not usable unless all applicable gates pass:

- no unresolved P1 or concrete P2 against claimed U0-U5 behavior;
- every mandatory issue above is fixed or explicitly adjudicated residual;
- seeded vulnerable controls go RED and corrected controls go GREEN;
- contract schemas, examples, migration and rollback tests pass;
- clean-room source tests pass on Linux, Windows and macOS or the unsupported
  platform is removed from the support claim;
- every claimed profile has host-native installed/readback/new-session evidence;
- `manifest` completes the real U3 lifecycle without a source checkout;
- U4 profiles prove matched deny plus neighboring allow and failure behavior;
- capacity-policy predicates pass: `singleton-safe@1` proves deterministic
  duplicate/overlap refusal, bounded recovery and zero uncustodied effects; only
  an authorized `n-active@N`/U5 claim proves two-mission coexistence;
- duplicate, upgrade, rollback and uninstall paths are observed;
- evidence is digest-bound, privacy-minimized and retained durably;
- exact-head GitHub CI is green and review threads are resolved on merit;
- independent acceptance passes at the declared tier; and
- merge/release/runtime landing are observed separately.

## Current verdict

As of the baselines above:

- Phase-1 projection: **U0 local structural evidence only**.
- Mission-custody source suite: **green but not an adequate usability oracle**.
- `manifest` standalone: **deliberately refused**.
- Core usable: **NO — blocked by authority, integrity and concurrency defects**.
- Fleet usable/universal: **NO — profiles and live consumer evidence absent**.

This contract changes those answers only through the observations listed above.
