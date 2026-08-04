> **Applies to:** epistemic-skills v3.0.0
>
> **Canonical source:** [released Applying Formal Rigor source](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/SKILL.md)
>
> **v4.0.0 consolidation:** applying-formal-rigor was consolidated into [resolve](Skill-Resolve) as its **derivation instrument** at v4.0.0 (2026-08-04); the name survives as instrument vocabulary, and the full method moved verbatim to [`resolve/derivation/METHOD.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/derivation/METHOD.md). This page is retained as a historical guide; the tagged v4.0.0 sources are the sole contract.

# Applying Formal Rigor

## What it does

Applying Formal Rigor establishes software-and-systems properties inside an explicit model, then applies operator-authorized priorities to those results. It requires three disciplines: name the precise construct, prove its preconditions and derive the result, and reconcile all material property terrain without pretending the shipped module library is exhaustive.

Formal theory can establish properties. It cannot manufacture runtime observations, operator values, product semantics, or a winning option.

## Use it when

- The operator explicitly requests a proof, complexity derivation, or rigorous comparison.
- A material software or systems decision has multiple viable alternatives with different measurable or theorem-governed properties.
- A proposed design needs correctness confirmation or reversal.
- Review feedback asserts a bound, theorem, consistency or isolation guarantee, safety property, or similar formal claim.

Use `focused` for one closed, supplied, bounded property whose answer will not select or reverse a persistent design. Use `standard` for a material fork or downstream justification. Use `high-assurance` when safety, security, privacy, irreversibility, public compatibility, cross-service consistency, or explicit operator direction bears load.

## Do not use it when

- The choice is pure preference, a one-answer mechanical edit, or a low-cost reversible choice whose plausible loss is below the analysis cost, unless rigor was explicitly requested.
- A supposedly focused answer crosses property families, depends on product/runtime facts, or will mandate a persistent architecture, schema, protocol, or operational decision.
- You want formal vocabulary to stand in for a derivation.
- You want a valid JSON envelope to certify that the reasoning inside it is correct.

## Inputs and prerequisites

For `standard` and `high-assurance`, define the exact question, subject and revision, system boundary, actors, environment, horizon, exclusions, stable alternatives, one null/status-quo option, hard constraints, authorized objectives, priority rule and authority, assumptions, empirical premises, uncertainty posture, and tier reason.

Load specialist modules only for fired property families from the released registry. Sources must match the claim: canonical theory for definitions and theorems, pinned official documentation for product/version semantics, and revision-bound coordinates for code, configuration, and measurements.

## Normal workflow

1. Apply the proportionality gate using cost of error, uncertainty, downstream dependence, and irreversibility versus analysis and reversible-probe cost.
2. For material work, build the decision frame without inferring engineering preferences as operator priorities.
3. Reconcile P1–P9: functional semantics; state and integrity; time and concurrency; distribution and consistency; dependability and recovery; security and information flow; algorithms and capacity; uncertainty and numerics; evolution and operations. Mark each `fired`, `not-applicable` with a boundary-tied reason, or `unmapped` with a coverage limit.
4. For every load-bearing construct, show `model → preconditions → fact mapping → derivation → result → residual mismatch`. Use `established`, `refuted`, `conditional`, or `incomplete` for derivation state.
5. Keep formal result, empirical closure, and normative synthesis separate. Preregister belief, prediction, disconfirming observation, and bounded test before reading a runtime result.
6. End in one honest synthesis outcome: `dominance`, `pareto-set`, `conditional`, `underdetermined`, `reversal`, or `reversible-probe`. Name concessions and recovery moves.
7. Re-run the tier and cue checks before emitting. Validate structural records, but do not equate schema success with proof correctness.

## Outputs and durable artifacts

A focused run is intentionally record-free: at most six short bullets or 250 visible words, covering the subject, closed model, construct, preconditions/fact map, derivation or counterexample, result, residual limit, and a bounded empirical check only if material. It emits no P1–P9 inventory or process artifact.

Standard and high-assurance work emits `formal-rigor-record@2`: subject and validity, coverage limits, decision frame, exactly one P1–P9 row per family, module/version provenance, derivations, empirical closure, synthesis, concessions, recovery moves, and explicit `never_attests` boundaries. A fork has exactly one null option. `pareto-set`, `underdetermined`, and `reversible-probe` do not select an option. Load-bearing `unmapped` terrain forbids unconditional dominance.

## Boundaries and failure modes

- Naming a theorem without mapping preconditions is assertion, not derivation.
- “Technically superior” does not authorize selection; preserve the Pareto set when no priority rule breaks the tie.
- Product isolation labels do not establish behavior. Pin the product/version and analyze a concrete history.
- MVD/4NF requires independent variation; paired method/priority facts alone do not establish the MVD.
- Lamport timestamp order does not imply causality, and consistency guarantees do not form one universal strength chain.
- Lower bounds require a fixed problem, model, preprocessing, randomization, exactness, posture, and resource.
- Any material change to revision, boundary, options, constraints, priorities, model, or product version voids the record; re-fire instead of patching.

## Example prompts

- “Prove the worst-case and amortized complexity of this bounded queue operation, including the parameter and residual assumptions. Do not recommend an architecture.”
- “Compare the current schema and a normalized child table. Reconcile every material P1–P9 family, preserve the authorized priority, and return `underdetermined` if the tie-break is missing.”
- “A review says PostgreSQL Repeatable Read prevents this write-skew. Pin the version semantics and analyze the concrete history before accepting or reversing the claim.”

## Related skills and handoffs

- [Blindspot Pass](Skill-Blindspot-Pass) establishes uncertain territory before a material formal fork.
- [Evidence Research](Skill-Evidence-Research) closes material scholarly or empirical premises but never supplies the design verdict.
- [Gauntlet](Skill-Gauntlet) independently attacks high-stakes consequential records.
- [Decision Ledger](Skill-Decision-Ledger) may reuse a durable formal record; persistence does not upgrade truth.
- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) handles proportional routing and the decide-stage loop.

## Canonical sources and evidence

- [Applying Formal Rigor source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/SKILL.md)
- [Specialist module registry at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/reference/modules/index.md)
- [`formal-rigor-record@2` schema at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/formal-rigor-record.schema.json)
- [Valid record example at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/examples/valid-formal-rigor-record.json)
- [Formal-rigor fixture suite at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures)
