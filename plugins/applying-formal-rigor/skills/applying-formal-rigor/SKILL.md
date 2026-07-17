---
name: applying-formal-rigor
description: Use when making any non-trivial design, architecture, schema, data-modeling, concurrency, caching, consistency, indexing, or algorithmic decision with two or more viable options, OR when justifying why one option is correct. Symptoms you need this: "both are fine", "it'll be slow", "this violates normalization", "stale data", "just pick one". Sets a graduate-level formal-theory floor for the analysis.
---

# Applying Formal Rigor

## Overview

Most design decisions get *senior-engineer* reasoning: correct instincts, named informally, one lens deep. This skill sets the floor at **graduate-level formal rigor**: name the *precise* theoretical construct, **derive** the conclusion from the formal apparatus instead of asserting it, and **sweep every relevant lens** instead of stopping at the first salient one.

**Core principle:** A design conclusion is not earned until it is *derived* from named formal theory. "It's better" is an opinion; "it's a 4NF decomposition eliminating the MVD `user_id ↠ method`, so the update anomaly is unrepresentable" is a result.

This is a **floor, not a ceiling** — the minimum bar for any non-trivial decision, not the most you may do.

## When to Use

- Any decision with ≥2 viable options (schema shape, store placement, cache strategy, isolation level, index, algorithm, data structure, API contract, propagation model).
- Any time you're about to assert one option is "correct/better/cleaner."
- Reviewing someone else's design rationale for rigor.

**When NOT to use:** purely mechanical edits with one correct answer; pure preference with no objective axis (naming a variable). If there's a *theorem* that bears on it, this applies.

## The Three Disciplines (the actual rules)

**Violating the letter of these is violating the spirit.** Surface-level rigor that *sounds* formal but skips the derivation is the failure mode this skill exists to kill.

### 1. Name the PRECISE construct, not the first salient one
Stopping at the nearest concept is the most common undershoot. Push to the exact formal object:

| Undershoot (first salient) | Precise construct (required) |
|---|---|
| "violates normalization / repeating group / 1NF" | the **functional/multivalued dependency** at fault, the **candidate keys**, and the **exact normal form** violated (2NF/3NF/BCNF/4NF/5NF) |
| "it'll be slow" | the **complexity class** (worst *and* amortized), and *in what parameter* (`O(offset)`, not "slow") |
| "stale data / eventual consistency" | the **consistency guarantee violated** in the lattice (read-your-writes? monotonic reads? linearizability?) |
| "race condition" | the **non-serializable schedule** / the **isolation anomaly** (dirty / non-repeatable / phantom / write-skew) |
| "it's coupled / not DRY" | the **anomaly class** (update/insertion/deletion) or the **shared mutable invariant** that can desync |

### 2. DERIVE, don't assert
Show the formal chain. Examples of the required move:
- Schema: `attributes + dependencies → candidate keys (attribute closure) → normal-form test → anomaly class → verdict`.
- Concurrency: `schedule → precedence graph → cycle? → (non-)conflict-serializable → anomaly → verdict`.
- Distributed: `partition/latency assumption → CAP/PACELC branch → required consistency level → mechanism (quorum/clock/CRDT) → verdict`.
- Algorithmic: `operation profile → cost per op (worst+amortized) → aggregate over workload → verdict`.

### 3. SWEEP every relevant lens
Run the decision through the lens index below. For each lens that bears on it, name the construct and derive. Do **not** stop at the first one that fires. A schema decision is usually *also* a complexity decision *and* an integrity-invariant decision.

## Lens Index (sweep these; details in theory-battery.md)

1. **Relational & normalization** — FDs, Armstrong's axioms, attribute closure, candidate keys, 1NF→6NF/BCNF/DKNF, **MVD/4NF**, **JD/5NF**, lossless-join & dependency-preserving decomposition, relational algebra, anomaly classes.
2. **Transaction & concurrency** — ACID, schedules, **conflict/view serializability** (precedence graph), recoverability (recoverable/ACA/strict), **isolation levels & their anomalies** (dirty, non-repeatable, **phantom**, write-skew), 2PL/SS2PL, MVCC, OCC, deadlock.
3. **Distributed data & consistency** — **CAP, PACELC**, the **consistency lattice** (linearizable > sequential > causal > PRAM > eventual) + **session guarantees** (read-your-writes, monotonic reads/writes, writes-follow-reads), **quorums (R+W>N)**, Lamport/vector clocks, **CRDTs / LWW registers**, consensus (Paxos/Raft), 2PC/saga/outbox.
4. **Complexity & algorithms** — asymptotic (O/Θ/Ω), **amortized** (aggregate/accounting/potential), worst vs average, space-time tradeoff, complexity classes, data-structure operation profiles, **index theory** (B+-tree seek vs scan, covering, selectivity).
5. **Type theory & formal methods** — **make illegal states unrepresentable**, invariants, pre/postconditions, loop invariants, totality, refinement, algebraic data types, parametricity.
6. **Information theory** — entropy, encoding/compression bounds, **hashing & collision** (birthday bound), cardinality estimation (HLL).
7. **Architecture formalisms** — coupling/cohesion, **SSOT / normalization-for-code** (same anomaly theory applied to config/state), idempotency, referential transparency, **blast radius / failure domains**, reversibility.

## Output Shape

For a fork, produce: per-lens construct + derivation → a comparison keyed by the *named* properties (not vibes) → an explicit verdict → and the **synthesis move** ("take A; recover B's one advantage via the materialized-view pattern"). The dominant option rarely wins on *every* axis; name what it concedes.

## Red Flags — you are undershooting, STOP

- You wrote "normalization" without naming the dependency, key, and normal form.
- You wrote "slow"/"fast"/"scales" without a complexity class and its parameter.
- You wrote "stale"/"consistent" without naming the guarantee in the lattice.
- You wrote "race"/"concurrency issue" without the schedule or the named isolation anomaly.
- You picked an option after firing **one** lens (no sweep).
- You asserted a verdict you did not **derive** from a named result.
- "Both are fine / it depends" with no formal axis identified.

**All of these mean: go back, name the precise construct, derive it, sweep the rest.**

## Worked Example (before → after)

**Decision:** store a user's ranked contact methods as `contact_method_1..3` columns (A) vs `user_contact_preferences(user_id, method, priority)` (B).

**Undershoot (senior-floor):** "A violates 1NF — repeating group across columns; B is the normalized child table. Pick B."  *Correct verdict, but not derived and not swept.*

**Formal floor (this skill):**
- *Relational lens:* The relation `user → {method}` exhibits a **multivalued dependency** `user_id ↠ method` (methods are independent of any other multivalued attribute). A relation with a nontrivial MVD that isn't a superkey-determined is **not in 4NF**; B is the **4NF decomposition**. The FDs `(user_id, method) → priority` and `(user_id, priority) → method` give two candidate keys; declaring both as `PRIMARY KEY (user_id,method)` + `UNIQUE (user_id,priority)` is *derived from the FDs*, which is precisely why duplicate-method and shared-rank states become **unrepresentable** (illegal states excluded by the keys — the type-theory lens agreeing with the relational one).
- *Complexity/index lens:* "who prefers SMS?" is `O(disjunction width)` and unindexable under A (predicate spans columns); under B it's a single B+-tree range seek on `(method)`, `O(log N + k)`.
- *Architecture lens:* A bakes cardinality 3 into DDL → adding a 4th method is an `ALTER` on the hot `users` table (high blast radius); B is `O(1)` rows, zero migration (reversible, low blast radius).
- *Synthesis:* B dominates on normalization, complexity, blast radius. A's only edge — join-free single-row read — is recoverable under B via a covering index / array aggregation. **Verdict: B**, edge recovered.

**REQUIRED REFERENCE:** the full formal apparatus per lens — definitions, the derivation templates, and the canonical decision questions — is in `theory-battery.md`. Load it when a lens fires and you need the exact construct.
