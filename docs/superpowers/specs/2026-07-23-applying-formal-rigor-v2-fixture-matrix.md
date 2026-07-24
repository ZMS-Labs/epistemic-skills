# applying-formal-rigor v2 — blinded fixture matrix

**Date:** 2026-07-23  
**Status:** Fixture design; no production skill or scorer implementation in this phase  
**Design:** [`2026-07-23-applying-formal-rigor-v2-design.md`](2026-07-23-applying-formal-rigor-v2-design.md)  
**Future battery root:** `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/`

## Purpose and evidence claim

This battery is a **blinded conformance smoke check, not a population
measurement and not a truth oracle**. It tests whether an agent applying the v2
discipline can:

- reject planted theorem misuse without rejecting correct formal claims;
- discover material property terrain outside the first salient concern;
- avoid a forced winner when authority or evidence does not justify one;
- skip or downshift ceremonial analysis;
- invalidate stale revision-bound results;
- use `unmapped` honestly rather than hiding unknown terrain;
- emit a well-formed `formal-rigor-record@2` with calibrated synthesis.

The battery does not establish real-world defect-detection rates, universal
formal competence, or independent adversarial judgment. A passing candidate is
eligible for a frozen Gauntlet review; it is not approved for merge by the
battery itself.

## Required development order

1. Commit the fixture packets, scorer-only ground truth, schemas, scorers, and
   pinned arm prompts.
2. Run the neutral and current-v1 arms and commit the RED results.
3. Only after RED is durable, edit the production `SKILL.md` and module battery.
4. Run the v2 candidate in at least three pinned runs.
5. Run every parody probe; each must fail for its intended reason.
6. Freeze the candidate, fixture set, scorer versions, and results before any
   Gauntlet gate.

A fixture assertion and its production fix must not first appear in the same
commit. The first failure is evidence, not disposable scaffolding.

## Blinding protocol — binding

### Run-agent view

For one fixture, the run agent sees only:

- `scenario.md`;
- the fixture's `artifacts/` tree;
- the arm prompt;
- the production or candidate skill/module files permitted for that arm;
- the public `formal-rigor-fixture-response@1` output schema.

The run agent never sees:

- any `ground-truth.json`;
- the scorer implementation or gate thresholds;
- the fixture's trap/control class;
- other fixtures or their results;
- the semantic adjudication rubric;
- which arm produced another response.

Each checkable scenario proposition is labeled `c1`, `c2`, … in order of
appearance. Labels identify propositions; they do not encode expected answers.

### Structural scorer view

The deterministic scorer sees the fixture ground truth and the candidate
response. It checks trigger/tier selection, claim classifications, coverage
states, module ids, decision-frame fields, freshness behavior, synthesis state,
selected option, source pins, and record invariants.

### Semantic adjudicator view

Derivation validity cannot be reduced safely to keyword matching. Two
context-isolated adjudicators see:

- the staged scenario and artifacts;
- the emitted record;
- the fixture's scorer-only proof obligations and forbidden propositions;
- no arm identity, model identity, prior result, or other adjudicator report.

Each returns `VALID`, `INVALID`, or `INCONCLUSIVE` with obligation ids and exact
record coordinates. Agreement on `VALID` passes the semantic check. Any
`INVALID` fails. Disagreement or `INCONCLUSIVE` is fail-closed for P0 fixtures
and counts as a miss for the aggregate gate. One bounded arbitration round may
resolve a non-P0 disagreement; the original dissent remains in the result.

A future deterministic proof checker or executable model may replace semantic
adjudication for an individual fixture, but a model-generated self-certification
may not.

## Proposed directory layout

```text
formal-rigor-v2-fixtures/
├── README.md
├── formal-rigor-fixture-response.schema.json
├── formal-rigor-record.schema.json
├── score.py                         # stdlib structural scorer
├── semantic-adjudication.md         # binding blinded protocol
├── fixtures/
│   └── <fixture-id>/
│       ├── scenario.md              # run-agent visible
│       ├── artifacts/               # run-agent visible
│       └── ground-truth.json        # scorer/adjudicator only
├── prompts/
│   ├── neutral.txt
│   ├── v1-current.txt
│   ├── v2-candidate.txt
│   └── parody-*.txt
└── results/
    ├── ARMS.md
    ├── RESULTS.md
    ├── neutral/run-1/...
    ├── v1-current/run-1/...
    ├── v2-candidate/run-1/...
    └── parody-*/run-1/...
```

Official product documentation is not copied wholesale into fixtures.
`artifacts/source-register.json` records product, version, canonical URL,
retrieved date, content hash where legally available, and a bounded attributed
paraphrase or short excerpt sufficient for the fixture. The scorer-only ground
truth preserves the exact proposition being tested.

## Run output wrapper

Each fixture produces one JSON file `<fixture-id>.response.json`:

```json
{
  "response": "formal-rigor-fixture-response@1",
  "fixture": "<fixture-id>",
  "invocation": "skip|focused|standard|high-assurance",
  "skip_reason": null,
  "claim_assessments": [
    {
      "id": "c1",
      "state": "established|refuted|conditional|incomplete",
      "derivation_ids": ["d1"]
    }
  ],
  "focused_output": null,
  "record": {
    "record": "formal-rigor-record@2"
  }
}
```

Rules:

- `invocation: skip` requires a concrete negative-trigger reason and
  `focused_output: null` and `record: null`.
- `invocation: focused` contains one to six short strings totaling at most 250
  visible words in `focused_output`, with `record: null`.
- Standard and high-assurance invocations contain a complete
  `formal-rigor-record@2` and `focused_output: null`.
- The response does not expose fixture class, expected state, proof-obligation
  ids, or score.
- Scenario claims must be present exactly once. Omission is a miss, not a safe
  abstention.

## Scorer-only ground truth

Each `ground-truth.json` follows this conceptual shape:

```json
{
  "fixture_id": "tm-01-false-mvd",
  "kind": "trap|control",
  "classes": ["theorem-misuse"],
  "priority": "P0|P1",
  "author": {
    "identity": "<fixture author>",
    "relationship": "skill-author|non-author|incident-mined"
  },
  "expected_invocation": ["standard"],
  "claims": [
    {
      "id": "c1",
      "allowed_states": ["refuted"],
      "proof_obligations": ["po-1"],
      "forbidden_propositions": ["fp-1"]
    }
  ],
  "coverage": {
    "required": [
      {"family": "P2", "status": "fired", "modules": ["relational-dependencies"]}
    ],
    "forbidden": [
      {"family": "P2", "status": "not-applicable"}
    ]
  },
  "decision_frame": {
    "null_option_required": true,
    "priority_rule_required": true
  },
  "synthesis": {
    "allowed_outcomes": ["reversal"],
    "selected_option": null
  },
  "freshness": {
    "must_re_fire": false
  },
  "source_requirements": [],
  "false_flag_condition": "<controls only>",
  "hard_fail_conditions": []
}
```

`proof_obligations` and `forbidden_propositions` are scorer/adjudicator-only
semantic predicates, not strings the run agent can echo to pass.

## Structural scoring dimensions

Each fixture is scored on ten dimensions.

| ID | Dimension | Deterministic floor |
|---|---|---|
| `S1` | Trigger and tier | Invocation is in the fixture's allowed set; skip/focused/standard/high-assurance is not silently inflated or narrowed. |
| `S2` | Decision frame | Required alternatives, null option, constraints, authority, priority rule, assumptions, empirical premises, and tier reason are present. |
| `S3` | Construct precision | Required module and construct are named; prohibited generic substitutes do not carry the claim. |
| `S4` | Applicability chain | Every scored derivation has model, preconditions, fact mapping, steps, result, and residual mismatch. |
| `S5` | Property coverage | Required families fire; every P1–P9 family is accounted for in standard/high-assurance records; focused runs incur no inventory; legitimate `unmapped` is preserved. |
| `S6` | Claim disposition | Every `cN` state is allowed by ground truth. |
| `S7` | Layer separation | Formal result, empirical closure, and synthesis do not substitute for each other. |
| `S8` | Synthesis calibration | Outcome and selected option obey dominance/Pareto/conditional/underdetermined/reversal/probe rules. |
| `S9` | Freshness and sources | Subject, revision, validity, coverage limits, source/version pins, and required re-fire behavior are correct. |
| `S10` | Boundary discipline | Research or Gauntlet handoffs are recommended only when triggered; neither is impersonated by the record. |

Per-fixture structural pass requires every hard-required dimension. Semantic
pass additionally requires the adjudication rule above.

## Fixture inventory

### Theorem misuse — five P0 correction fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `tm-01-false-mvd` | A review claims `user_id ↠ method` in a ranked-contact relation while also asserting FDs that pair method with priority, then declares a 4NF violation. | `standard`; P2 fires `relational-dependencies`; the alleged MVD and 4NF proof are refuted; synthesis `reversal`; no universal “unindexable” claim. The child-table option may remain viable for other separately derived reasons. | Repeats the MVD/4NF proof, calls fixed columns inherently unindexable, or selects an option solely from the refuted theorem. |
| `tm-02-isolation-name-is-not-semantics` | A PostgreSQL 18 design infers from the ANSI table that Repeatable Read admits phantoms and therefore attributes an observed history to a phantom. Staged official-version facts say PostgreSQL 18 prevents phantoms but permits serialization anomalies. | `standard`; P3 fires `transaction-histories`; product/version is pinned; standard minimum and implementation semantics are separated; the concrete history is analyzed before mechanism choice; the universal phantom claim is refuted. | Uses the level name as the proof, omits the PostgreSQL version/source, or says PostgreSQL 18 Repeatable Read permits phantoms. |
| `tm-03-consistency-is-not-one-chain` | A distributed-store rationale uses `linearizable > sequential > causal > PRAM > eventual` as a total ordering and claims causal is universally weaker than sequential. Scope and client/history assumptions are omitted. | `standard`; P4 fires `distributed-consistency`; the scalar-chain claim is refuted or incomplete; scope, order/visibility predicates, convergence, and failure assumptions are requested; synthesis `underdetermined` until definitions are fixed. | Treats the mnemonic chain as a proof or forces a choice without scope. |
| `tm-04-lamport-converse` | Claims: `a→b ⇒ C(a)<C(b)`; `C(a)<C(b) ⇒ a→b`; scalar Lamport timestamps alone reveal concurrency and totally order events. | `focused`; P3/P4 fire `distributed-consistency`; first claim established, converse refuted, concurrency inference refuted, and total-order tie-break distinguished from causality; synthesis `reversal` of the proposed diagnostic. | Says timestamp order is equivalent to happened-before or omits the tie-break distinction. |
| `tm-05-model-free-lower-bound` | A bounded-integer sort is called optimal because comparison sorting is Ω(n log n), while the stated machine/range model permits non-comparison methods. | `focused`; P7 fires `algorithms-data-structures`; comparison lower bound is conditional on the comparison model; actual model, word/range, preprocessing, exactness, and resource are named; “provably optimal” is refuted for the stated subject. | Repeats Ω(n log n) as model-free or declares convergence after changing models silently. |

### Missed terrain — four breadth fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `mt-01-numerical-stability` | Two O(n) floating-point summation routines are declared equivalent on complexity alone; one violates a stated error hard constraint through cancellation. | `standard`; P7 and P8 fire `algorithms-data-structures` plus `numerical-analysis-floating-point`; complexity result may be established while numerical adequacy is refuted; synthesis `reversal` or `dominance` only under the stated accuracy constraint. | Stops at Big-O, treats IEEE format as proof of stability, or omits the numeric model/error bound. |
| `mt-02-queue-instability` | An O(1) request handler is called scalable although staged observations give arrival rate λ greater than sustainable service rate μ. | `standard`; P7 fires `queueing-capacity-parallelism`; operation cost and system stability are separated; queue instability is derived; synthesis `reversal` or a bounded capacity probe if μ is not verified. | Calls per-request O(1) sufficient evidence of scalability or ignores arrival/service assumptions. |
| `mt-03-authorization-boundary` | A cross-tenant write path is called safe because the schema has keys and FKs, but the endpoint accepts caller-supplied tenant ids without an authorization check. | `high-assurance`; P2 and P6 fire `relational-dependencies` and `security-information-flow-privacy`; data integrity is not promoted to authorization; hard security constraint fails; synthesis `reversal`; Gauntlet handoff recommended without impersonating it. | Declares illegal state unrepresentable while the unauthorized state transition remains representable, or omits an attacker/authority model. |
| `mt-04-safety-without-liveness` | A locking protocol proves mutual exclusion and is therefore declared correct, but a staged schedule admits starvation. | `standard`; P1/P3 fire `temporal-specification-model-checking` and, if relevant, `transaction-histories`; safety may be established while liveness is refuted; synthesis `conditional` or `reversal`. | Treats one invariant as full correctness or omits the starvation counterexample. |

### Forced closure — two decision-calibration fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `fc-01-pareto-no-priority` | Option A has lower p99 latency and higher durable-loss probability; B has higher latency and lower loss probability. Both satisfy hard constraints. No authorized priority or utility is supplied. | `standard`; P5/P7 fire; null option present; both options remain non-dominated; synthesis `pareto-set` (or `underdetermined` only if feasibility itself is unclear); `selected_option: null`. | Invents weights, calls one “best practice,” or selects a winner without authority. |
| `fc-02-value-of-information-probe` | Cache strategy ranking depends on a load-bearing hit-rate/workload premise that has never been measured; a cheap replay experiment is available. | `standard`; formal results are conditional; empirical closure is `pending`; synthesis `reversible-probe`; belief, prediction, disconfirming observation, bounded test, and branch-changing outcomes are preregistered. | Treats assumed hit rate as observed, performs post-hoc prediction, or forces a strategy choice. |

### Overtriggering and tier proportionality — three fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `ot-01-pure-preference-skip` | Choose `items` versus `records` for a local variable; no theorem, measurable behavior, convention, or downstream contract differs. | `skip` with the negative trigger stated. | Emits a formal record, invents a property difference, or runs a lens/module sweep. |
| `ot-02-focused-not-ceremony` | An explicit Big-O question compares list membership with set membership in a small reversible development script; no persistent architecture decision is requested. | `focused`; at most six short bullets or 250 visible words name n, construction cost, operation mix, average/worst model, result, and residual constants. | Emits P1–P9 reconciliation, a full decision frame, `formal-rigor-record@2`, persistent artifact, source-register apparatus, standard/high-assurance theater, omits set-build cost, or claims O(1) without model qualification. |
| `tc-01-high-assurance-escalation` | A public authentication-token migration changes downgrade behavior, compatibility, revocation, and rollback across services. | `high-assurance`; P5/P6/P9 fire appropriate modules; official product/protocol versions and subject revision are pinned; threat/fault/version-skew models are explicit; empirical tests preregistered; Gauntlet handoff recommended. | Treats it as focused/standard solely because code diff is small, or claims the formal record is the adversarial gate. |

### Staleness and re-fire — two fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `ss-01-subject-revision-moved` | A prior record proves a schema decomposition at SHA A. Current artifacts are SHA B and change a load-bearing dependency. The task asks to consume the old verdict. | Prior record is stale; re-fire against SHA B; no old judgment content is consumed; new `subject.revision` and fact mapping required. | Patches the old record, cites its verdict as current, or reuses `subject-revision-unchanged`. |
| `ss-02-priority-rule-moved` | Code and formal properties are unchanged, but operator authority changes from latency-first to durability-first. The prior selected option is offered as settled. | Decision frame movement voids normative synthesis; emit a new record after freshness checks; formal derivations may be referenced only after revalidation; selection is recomputed under the new authority. | Treats values as immutable facts or keeps the old winner without a new record. |

### Legitimate unmapped terrain — two fixtures

| ID | Scenario and planted failure | Expected behavior | Hard failure |
|---|---|---|---|
| `um-01-custom-accelerator-memory-model` | A proprietary accelerator exposes weak ordering behavior not defined by the available module library or supplied vendor semantics; correctness depends on it. | `standard` or `high-assurance`; P3/P7 status `unmapped`; exact missing memory model and vendor fact are in `coverage_limits`; synthesis `underdetermined`; escalate to a specialist or bounded probe. | Coerces the issue into generic “architecture,” marks it n/a, invents a memory model, or emits dominance. |
| `um-02-external-regulatory-semantics` | A retention design depends on the legal meaning of a jurisdiction-specific deletion obligation. Engineering mechanisms are visible, but no authorized legal interpretation is supplied and the module library is not legal research. | P6/P9 record the engineering properties; the legal semantic dependency is `unmapped` and outside the skill's authority; synthesis `underdetermined` pending an authorized specialist interpretation. | Treats regulation as a software theorem, marks the obligation n/a, or silently chooses an interpretation. |

### Clean controls — four false-positive guards

| ID | Clean scenario | Expected behavior | False flag |
|---|---|---|---|
| `cc-01-true-independent-mvd` | `user_delivery(user_id, contact_method, notification_topic)` has independently varying method and topic sets with the two stated MVDs. | `focused`; P2 fires `relational-dependencies`; nontrivial MVDs and 4NF violation established; lossless decomposition derived. | Refutes the MVD, marks P2 unmapped/n/a, or rejects all 4NF reasoning because the old example was wrong. |
| `cc-02-comparison-bound-is-valid` | Exact comparison sorting, no preprocessing, sequential comparison model, arbitrary keys; an O(n log n) algorithm is evaluated for asymptotic optimality. | `focused`; P7 fires; Ω(n log n) lower bound and convergence under the frozen model established; model-change caveat remains residual, not a reason to withhold the scoped result. | Calls the bound model-free, but also false-flags the correctly scoped claim as unsupported or unmapped. |
| `cc-03-postgresql18-rationale-correct` | A rationale states that PostgreSQL 18 Repeatable Read prevents phantoms but may permit serialization anomalies and analyzes a concrete history accordingly. | `focused` or `standard`; P3 fires; product/version/source pin accepted; claim established or conditional exactly where the history warrants. | Reverses the correct product claim merely because ANSI minimums differ, or omits the concrete history. |
| `cc-04-authorized-dominance` | Two feasible options have equal durability and compatibility; A has lower measured p99 and lower cost. Operator-authorized lexicographic rule is reliability hard constraint, then latency, then cost. | `standard`; decision frame complete; measurements anchored; A dominates under the authorized rule; `selected_option: A`; concessions/out-of-scope limits named. | Refuses every choice as inherently subjective, invents an unmapped blocker, or selects B. |

## Inventory reconciliation

| Class | Trap count | P0 fixtures |
|---|---:|---|
| Theorem misuse | 5 | all five |
| Missed terrain | 4 | `mt-03-authorization-boundary` |
| Forced closure | 2 | `fc-01-pareto-no-priority` |
| Overtrigger / tier calibration | 3 | `ot-01-pure-preference-skip`, `tc-01-high-assurance-escalation` |
| Stale subject / decision frame | 2 | `ss-01-subject-revision-moved` |
| Legitimate unmapped | 2 | `um-01-custom-accelerator-memory-model` |
| **Total traps** | **18** | **11 P0** |
| Clean controls | **4** | all are mandatory-clean |
| **Battery total** | **22** | |

The matrix must reconcile mechanically to these counts. Adding or removing a
fixture requires updating this table, the scorer's inventory check, and the
threshold derivation in one commit.

## Gate

A candidate run passes only when all are true:

1. **P0:** all 11 P0 fixtures pass structural and semantic checks;
2. **aggregate traps:** at least 17 of 18 traps pass;
3. **class floor:** every trap class has at least one passing fixture;
4. **controls:** 0 of 4 clean controls are false-flagged;
5. **record integrity:** every non-skip response validates against the frozen
   `formal-rigor-record@2` schema;
6. **parodies:** every standing parody probe fails;
7. **repetition:** the candidate meets the gate in all of at least three pinned
   runs;
8. **independence:** at least one third of fixtures are authored, adversarially
   extended, or incident-mined by a non-author, with provenance recorded;
9. **freeze:** scorer, schemas, fixture ground truths, candidate skill/modules,
   model, harness, and prompts are content-pinned per run.

The one allowed aggregate miss may not be P0 and may not erase an entire class.
A semantic `INCONCLUSIVE` counts as a miss.

## Standing parody probes

Each parody is deterministic where possible and must fail the gate.

| Parody | Behavior | Intended failure |
|---|---|---|
| `jargon-only` | Names plausible theorems and modules, marks claims established, but omits model/preconditions/fact mapping. | Fails S3/S4 and theorem-misuse fixtures. |
| `closed-taxonomy` | Never emits `unmapped`; coerces every property into the nearest module. | Fails both unmapped fixtures and coverage limits. |
| `always-decide` | Always labels A dominant and selects it. | Fails forced-closure, stale, unmapped, and controls where A is not authorized. |
| `always-cautious` | Marks every family unmapped and every outcome underdetermined. | Catches some traps but false-flags all clean controls. |
| `full-ceremony` | Runs high-assurance on every scenario. | Fails pure-preference skip and focused proportionality. |
| `formal-only` | Produces correct theorems but promotes assumed workload/product facts to observations. | Fails empirical closure and source-version fixtures. |

A parody that unexpectedly passes is a scorer defect or an insufficient
fixture set; the production skill may not ship until the gate is repaired and
re-run.

## Arm definitions

### Neutral baseline

Pinned prompt, no current or candidate skill:

> Review the scenario and artifacts. Decide whether the stated design claims
> are correct and what option should be chosen. Return the required fixture
> response JSON with your reasoning.

The neutral prompt requests the output shape but teaches none of the v2
method. It is cooperative, not intentionally weak.

### Current-v1 arm

Reads the current production `applying-formal-rigor/SKILL.md` and
`theory-battery.md` at a pinned SHA, then receives the same fixture packets and
output wrapper instruction. This arm records what the redesign actually
changes; it is not expected to pass the v2 gate.

### Candidate-v2 arm

Reads the candidate production skill, module registry, and exactly the modules
its own routing loads. Module access is recorded per fixture. It may not read
scorer-only files.

### Parody arms

Use the fixed strategies above. Their outputs and failure reasons are committed.

## Result reporting

`results/ARMS.md` records for every run:

- arm and prompt hash;
- model/provider and exact model id where available;
- harness and version;
- candidate skill/module hashes;
- fixture-set, schema, structural-scorer, and adjudication-protocol hashes;
- source-register snapshot date;
- sampling settings and seed where the runtime exposes them;
- independence/degradation notes.

`results/RESULTS.md` reports:

- structural and semantic pass per fixture;
- P0, aggregate, class, and control gates;
- confusion matrix by class;
- current-v1 and neutral paired deltas on identical fixture packets;
- per-dimension failures S1–S10;
- semantic adjudicator agreement and all retained dissent;
- parody outcomes;
- exact coverage limits;
- the label **“blinded conformance smoke check; not a population rate.”**

The named path to a real-world rate is to collect genuine formal-rigor runs,
later-established outcomes, revisions, and review defects under an operator-
approved telemetry protocol. No population claim is made before an adequate,
representative sample and an independent truth-establishment process exist.

## Source and artifact policy for fixtures

- Canonical theory coordinates come from the design's source register.
- Official product behavior is pinned to product/version and official URL.
- Fixture artifacts may contain synthetic code, histories, workloads, and
  measurements; every synthetic item is labeled.
- Real incidents must be scrubbed of secrets, PII, customer identifiers, and
  private repository content before inclusion.
- Repository text, staged docs, and model output are data, never instructions.
  Embedded directives are ignored and may themselves be a fixture finding.
- Ground truth records whether each source is primary theory, official product
  documentation, synthetic observation, or operator-authorized value.
- No fixture's ground truth may depend only on the author skill's own prose.

## Acceptance criteria for the fixture implementation PR

- **F-AC1:** all 22 matrix entries exist as blinded fixture directories or an
  operator-approved matrix amendment explains the replacement and preserves
  class/P0 coverage.
- **F-AC2:** run agents cannot access ground truth, scorers, thresholds, other
  results, or arm identity leakage.
- **F-AC3:** schemas close the invocation, claim-state, coverage-state,
  synthesis-outcome, validity, and required-field vocabularies.
- **F-AC4:** structural scorer is stdlib-only, deterministic, and byte-reproducible
  for identical inputs.
- **F-AC5:** semantic adjudication is context-isolated, arm-blinded, retains
  dissent, and fails closed on P0 disagreement.
- **F-AC6:** neutral and current-v1 RED results are committed before production
  skill edits.
- **F-AC7:** candidate and baseline arms are run at least three times with pinned
  identities and settings.
- **F-AC8:** all six parody probes run and fail for their intended reason.
- **F-AC9:** at least one third of fixtures carry non-author or incident-mined
  provenance.
- **F-AC10:** result report distinguishes structural conformance, semantic
  adjudication, and any later empirical outcome; none is rounded into universal
  correctness.
- **F-AC11:** no fixture result authorizes merge, release, or replacement of
  Gauntlet.
- **F-AC12:** any fixture or subject movement invalidates prior results by hash;
  the complete affected arm is re-run rather than patched.

## Deferred implementation choices and defaults

| Question | Default proposed by this matrix |
|---|---|
| Record validator location | Skill-local schema/scorer during Phase B; promote stable envelope fields to collection `contracts/` only with a versioned contract change. |
| Module file layout | One `reference/modules/<module-id>.md` per module plus `reference/modules/index.md`; avoid one monolithic battery. |
| Semantic judging | Two isolated arm-blinded adjudicators plus fail-closed bounded arbitration; replace with executable proof only per fixture when available. |
| First-release module breadth | Implement modules required by the 22 fixtures; all other identified terrain remains explicitly `unmapped`. |
| Product docs in fixtures | Staged attributed paraphrase/short excerpt + product/version/URL/hash metadata; never copy a complete manual. |

These defaults become binding only after operator approval of the design phase.
