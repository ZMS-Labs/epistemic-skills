# Theory battery compatibility index

This filename remains as a compatibility surface for links created before
`applying-formal-rigor` v2. It is not a normative all-lenses checklist and must
not be loaded as one monolithic battery.

The v2 registry is [`reference/modules/index.md`](reference/modules/index.md).
Reconcile P1-P9 in `SKILL.md`, then load only the bounded specialist modules for
families marked `fired`. Mark material terrain `unmapped` when the registry has
no adequate module; do not approximate it with a neighboring topic.

Legacy mapping:

| Former lens | v2 destination |
|---|---|
| Relational and normalization | `relational-dependencies` |
| Transactions and concurrency | `transaction-histories` |
| Distributed data and consistency | `distributed-consistency` |
| Complexity and algorithms | `algorithms-data-structures` and, when capacity matters, `queueing-capacity-parallelism` |
| Type theory and formal methods | P1/P2; currently `unmapped` unless a listed first-release module is adequate |
| Information theory | P6/P8; currently `unmapped` unless a listed first-release module is adequate |
| Architecture formalisms | P5/P7/P9; use a precise listed module or mark `unmapped`; architecture slogans are not theorems |

The invalid ranked-contact 4NF example has been retired. The corrected MVD
example and caveats live in
[`reference/modules/relational-dependencies.md`](reference/modules/relational-dependencies.md).
