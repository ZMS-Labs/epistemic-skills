# Theory Battery — the formal apparatus per lens

Load the section for whichever lens fired. Each gives: the constructs you must be able to **name**, the **derivation template**, the **canonical decision questions**, and the **undershoot** to avoid. The goal is always: name the precise construct → derive → state the result.

---

## 1. Relational & Normalization Theory

**Constructs to name:** relation/attribute/tuple/domain; **functional dependency** (X→Y); **multivalued dependency** (X↠Y); **join dependency** (JD); **Armstrong's axioms** (reflexivity, augmentation, transitivity; + union, decomposition, pseudotransitivity); **attribute closure** X⁺; **candidate key / superkey / prime attribute**; **minimal (canonical) cover**; normal forms **1NF, 2NF, 3NF, BCNF, 4NF, 5NF/PJNF, 6NF, DKNF**; **lossless-join decomposition** (the chase / the common-attribute superkey test); **dependency preservation**; **anomaly classes** (insertion, update, deletion); **relational algebra** (σ select, π project, ⋈ join {theta/equi/natural/semi/anti/outer}, ÷ division, set ops) and its equivalence to safe relational calculus (**Codd's theorem**).

**Normal-form ladder (what each removes):**
- **1NF** — atomic attributes, no repeating groups (no `col_1,col_2,col_3` smearing of a set).
- **2NF** — no partial dependency of a non-prime attribute on part of a candidate key.
- **3NF** — no transitive dependency (non-prime → non-prime). 3NF is always achievable losslessly *and* dependency-preservingly (synthesis algorithm).
- **BCNF** — every nontrivial FD's left side is a superkey. May sacrifice dependency preservation; BCNF decomposition is lossless but not always dependency-preserving (the 3NF-vs-BCNF tradeoff is a *named* decision).
- **4NF** — no nontrivial **MVD** whose left side isn't a superkey. This is the one most often missed: a set-valued / independent-multivalued attribute (user→{phone}, user→{skill}) is a 4NF concern, not merely 1NF.
- **5NF/PJNF** — no nontrivial **join dependency** not implied by candidate keys (relevant when a relation reconstructs only via 3+ way join).
- **DKNF** — every constraint is a logical consequence of domain + key constraints (the ideal; rarely fully attainable).

**Derivation template (schema decision):**
1. List attributes + the real-world FDs and MVDs.
2. Compute attribute closures → candidate keys.
3. Test each FD/MVD against the NF definitions → identify the highest NF violated and *why*.
4. Map the violation to its **anomaly class** (insertion/update/deletion) — this is the concrete cost.
5. Propose the decomposition; **prove it lossless** (common attribute is a key of one side) and check **dependency preservation**.
6. Cross-check the type-theory lens: do the keys make illegal states unrepresentable?

**Canonical questions:** What are the FDs/MVDs? The candidate keys? Highest NF satisfied? Which anomaly does the un-decomposed form admit? Is the decomposition lossless and dependency-preserving? Is denormalization being chosen *deliberately* (named: a materialized/derived redundancy with a stated refresh/coherence mechanism) or accidentally (an anomaly waiting to happen)?

**Undershoot:** "violates normalization / 1NF" with no dependency, key, NF, or anomaly class named.

---

## 2. Transaction & Concurrency Theory

**Constructs to name:** **ACID**; **schedule/history**; conflicting operations (R-W, W-R, W-W on same item); **conflict-serializability** (acyclic **precedence/serialization graph**); **view-serializability** (superset, NP-hard to test); **recoverability** levels (recoverable ⊂ avoids-cascading-aborts ⊂ strict); concurrency control: **2PL / strict 2PL (SS2PL)**, **timestamp ordering**, **MVCC** (snapshot isolation), **OCC** (validation); **deadlock** (wait-for graph) vs **livelock**; **lock granularity / intention locks**.

**Isolation levels & the anomalies they permit (ANSI + the real ones):**
- READ UNCOMMITTED → **dirty read**.
- READ COMMITTED → **non-repeatable read**.
- REPEATABLE READ → **phantom read** (the row *set* of a predicate changes). *Pagination duplicate/skip under concurrent insert/delete IS the phantom phenomenon.*
- SERIALIZABLE → none of the above.
- **Snapshot isolation (MVCC)** is *not* serializable: admits **write-skew** and read-only-anomaly. Name it; don't assume "MVCC = serializable."

**Derivation template (concurrency decision):**
1. Write the schedule of the contending operations.
2. Identify conflicts; build the precedence graph.
3. Cycle ⇒ not conflict-serializable ⇒ name the resulting anomaly.
4. Choose the mechanism (2PL/MVCC/OCC) and the *minimum* isolation level that excludes the named anomaly — over-isolating is a (named) throughput cost.

**Canonical questions:** What schedule produces the bug? Which named anomaly is it? What is the *minimum* isolation level / mechanism that excludes it? Does the chosen store's "SERIALIZABLE" actually mean serializable or snapshot? Recoverability guarantees on abort?

**Undershoot:** "race condition" / "add a lock" with no schedule, no precedence-graph reasoning, no named isolation anomaly.

---

## 3. Distributed Data & Consistency Theory

**Constructs to name:** **CAP** (under partition, choose C or A); **PACELC** (Else: Latency vs Consistency — the *non-partition* tradeoff most systems actually live in); the **consistency lattice**: **linearizable (atomic) > sequential > causal > PRAM/FIFO > eventual**; **session guarantees**: **read-your-writes**, **monotonic reads**, **monotonic writes**, **writes-follow-reads**; **quorum** systems (**R + W > N** for read-your-writes on a single object; **W > N/2** for write conflict-avoidance); **Lamport clocks** (total order, no causality capture) vs **vector clocks** (causality / concurrent-detection); **CRDTs** (CvRDT/CmRDT, join-semilattice merge) and the **LWW register** (last-writer-wins = a clock-guarded set); **consensus** (Paxos/Raft) for linearizable replicated state; **2PC** (blocking) vs **saga/outbox/CDC** (eventual, compensating).

**Cache-in-front-of-DB is a replication problem.** A read cache is an async replica; the question is which consistency guarantee you owe. "Old profile after my own write" = **read-your-writes violation**. Fixes mapped to theory: invalidate-on-write (delete-after-commit) restores RYW on the writer's path; a **version/CAS guard** on cache writes is an **LWW register** preventing stale repopulation; TTL alone only bounds the **eventual-consistency** window (doesn't give RYW).

**Derivation template:** state partition/latency assumptions → CAP/PACELC branch → the *required* guarantee (which session guarantee or lattice level the use case demands) → the mechanism that provides exactly it (quorum / clock / CRDT / consensus / invalidation) → residual windows (name them).

**Canonical questions:** Which lattice level / session guarantee does the UX actually require (often just RYW + monotonic reads, not linearizability)? Is this PACELC-C or PACELC-A? Does the fix *guarantee* the level or merely shrink the window? What repopulation/merge races remain, and what clock/version closes them?

**Undershoot:** "eventual consistency / stale / just lower the TTL" without naming the required guarantee or recognizing it as replication.

---

## 4. Complexity & Algorithmic Analysis

**Constructs to name:** asymptotic **O/Θ/Ω**; **worst vs average vs amortized**; **amortized methods** (aggregate, accounting, **potential**); **space-time tradeoff**; complexity classes (P/NP/PSPACE) when relevant; **data-structure operation profiles** (the cost vector that should drive the choice); **index theory** — B+-tree **seek O(log N)** vs **scan/discard O(n)**, covering index (no heap fetch), composite-key **lexicographic range**, **selectivity / cardinality estimation**, sort-avoidance via index order.

**Name the parameter, always.** `LIMIT k OFFSET n` is **O(n+k)** (produce-and-discard n rows) → a full traversal is **O(N²/k)**; keyset/cursor is **O(log N + k)** per page, **O(N)** for the traversal. "Slow" is not an analysis; "O(offset), quadratic over a full crawl" is.

**Derivation template:** define the operation/workload mix → cost per op (worst + amortized) → aggregate over the realistic N and access pattern → compare named complexities → name the constant-factor / cache / IO effects only after the asymptotics.

**Canonical questions:** Cost in which parameter, worst and amortized? What's the workload's read/write/scan mix? Does an index turn a scan into a seek? Is a sort implied, and does index order remove it? Are we trading space for time deliberately?

**Undershoot:** "fast/slow/scales/won't scale" with no complexity class and no parameter.

---

## 5. Type Theory & Formal Methods

**Constructs to name:** **make illegal states unrepresentable** (the type/schema excludes bad values by construction); **invariants** (representation invariant, system invariant); **pre/postconditions** & **Hoare triples**; **loop invariants**; **totality** (total vs partial functions; exhaustiveness); **algebraic data types** (sum/product; encode "exactly one of"); **refinement** (spec → implementation preserving behavior); **parametricity / referential transparency**; **idempotency** as a typed property.

**The bridge to the relational lens:** a `PRIMARY KEY`/`UNIQUE`/`CHECK`/`NOT NULL`/FK is the *type-level* exclusion of an illegal state; "the constraint enforces it" and "the type makes it unrepresentable" are the same result reached from two lenses — cite both.

**Canonical questions:** Can the bad state be *written at all*, or is it excluded by construction? What invariant must hold, and where is it established/preserved? Is the operation total? Idempotent? Is this enforced by the type/schema or merely by convention (the latter is a future anomaly)?

**Undershoot:** "we'll validate it in code" where a key/type/ADT could make it unrepresentable.

---

## 6. Information Theory

**Constructs to name:** **entropy** (bits of real information; drives encoding/compression bounds — you cannot losslessly compress below entropy); **hashing**: uniformity, **collision / birthday bound** (~√(space) before a collision is likely — sizes IDs, dedup keys, sharding); **cardinality estimation** (**HyperLogLog**) for count-distinct at scale; **error-detection/correction** coding when integrity over a channel matters.

**Canonical questions:** How many bits of entropy does this identifier/token actually carry (collision risk, guessability)? Is a hash space large enough given the birthday bound at expected N? Is an approximate-distinct (HLL) acceptable vs an exact, expensive `COUNT(DISTINCT)`?

**Undershoot:** choosing ID/hash widths or "unique enough" tokens without a birthday-bound calculation.

---

## 7. Architecture Formalisms (theory applied to code/config/state)

**Constructs to name:** **coupling** (afferent/efferent) & **cohesion**; **SSOT / normalization-for-code** — the *same* insertion/update/deletion anomaly theory applies to duplicated config, denormalized state, copied constants (a value stored twice is an update anomaly); **derived vs base data** & the **materialized-view pattern** (keep normalized source + a checked-in/generated derived artifact — recovers "pointability" without duplication); **idempotency** & **referential transparency**; **blast radius / failure domains** (what breaks if this changes/fails; how reversible); **essential vs accidental complexity**.

**The recurring synthesis move:** when option A is normalized (no anomaly) but option B is "one nice pointable artifact," you usually don't choose — you take A's normalized source **plus** a generated materialized view (A's correctness, B's ergonomics). Name it as the materialized-view / base-table pattern.

**Canonical questions:** Is any fact stored in >1 place (update anomaly)? Is the duplicate a *deliberate derived view* with a refresh/coherence mechanism, or accidental? What's the blast radius and reversibility of this change? Is added complexity essential or accidental? Does this preserve the system's stated invariants (SSOT, single-source registry conventions)?

**Undershoot:** "it's cleaner / DRY-er / more cohesive" without naming the anomaly avoided or the invariant preserved.

---

## Cross-lens discipline

Most real decisions fire **3+ lenses**. A schema choice is relational *and* complexity *and* type-theory *and* architecture. A caching choice is consistency *and* concurrency *and* complexity. **Sweep them all**, derive each, then synthesize — the verdict names what the winner concedes and how to recover it.
