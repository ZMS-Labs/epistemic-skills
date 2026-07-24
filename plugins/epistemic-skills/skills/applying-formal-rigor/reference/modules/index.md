# Specialist module registry

Load modules only after P1-P9 reconciliation and only for property families
marked `fired`. A module is a bounded formal apparatus, not a separate skill or
trigger. Its presence does not prove applicability: every use still supplies
the six-link chain required by `SKILL.md`.

## First-release modules

| Module | Primary families | Use for |
|---|---|---|
| [`relational-dependencies`](relational-dependencies.md) | P2 | FDs, MVDs, keys, normal forms, decomposition |
| [`transaction-histories`](transaction-histories.md) | P1, P3 | histories, serializability, isolation, recovery |
| [`distributed-consistency`](distributed-consistency.md) | P3, P4, P5 | consistency predicates, clocks, quorums, consensus |
| [`algorithms-data-structures`](algorithms-data-structures.md) | P7 | bounds, recurrences, lower bounds, data structures |
| [`temporal-specification-model-checking`](temporal-specification-model-checking.md) | P1, P3, P5 | transition systems, safety, liveness, counterexamples |
| [`dependability-fault-models`](dependability-fault-models.md) | P5 | faults, failures, availability, recovery |
| [`security-information-flow-privacy`](security-information-flow-privacy.md) | P1, P6 | threat/authority models, information flow, privacy |
| [`queueing-capacity-parallelism`](queueing-capacity-parallelism.md) | P5, P7, P8 | stability, saturation, backpressure, parallel limits |
| [`numerical-analysis-floating-point`](numerical-analysis-floating-point.md) | P7, P8 | conditioning, error, stability, IEEE 754 behavior |
| [`interface-protocol-evolution`](interface-protocol-evolution.md) | P1, P5, P9 | compatibility, protocol state, migration, version skew |
| [`decision-theory-multiobjective`](decision-theory-multiobjective.md) | synthesis | feasibility, Pareto sets, authorized choice rules, value of information |

## Explicitly unmapped in the first release

The following proposed terrains do not yet have production modules: general
type theory/program logics beyond the bounded modules above, real-time
scheduling, general probability/statistics/randomization, and general
architecture quality attributes. Custom hardware memory models, legal or
regulatory semantics, and any other unregistered formal terrain are also
`unmapped` unless an adequate pinned module is added. Never route them to a
generic architecture substitute.
