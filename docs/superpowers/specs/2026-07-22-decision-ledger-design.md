# decision-ledger — new skill design

**Date:** 2026-07-22
**Status:** Draft for operator review — amended after gauntlet run
`phase-c-skill-specs-2026-07-22` (2026-07-22; verdict: CONDITIONAL). The
pre-review conditions (C-1…C-7) are landed in this amendment; the remaining
conditions (C-8…C-10) ride as implementation-PR requirements. Run artifacts
are local-only (`outputs/` is not committed); the run is cited by name and
date only. See the conditions table at the end of this spec.
**Type:** New skill (discipline candidate) for the epistemic-skills collection
**Basis:** gap analysis (`docs/audits/2026-07-22-collection-audit/06-gap-analysis.md`, candidate (b) — verdict PROPOSE, strongest candidate); control-plane creation gates (`docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md:285-296`).

## Problem

The arc has **no persistence moment**. Every existing skill's output is consumed
downstream *within* a run or session; nothing governs what survives *between*
runs. A decision made Tuesday is, by Friday, indistinguishable in-band from a
verified fact — or silently contradicted, or re-derived from scratch. The
failure modes: a future session re-litigates a settled decision; an assumption
made under uncertainty hardens into a premise; a Sovereign correction taught in
one session is lost in the next.[^1]

[^1]: One operator fleet's governance (its TRANSPARENCY-2 rule) mandates
persisting emergent decisions and taught lessons. That mandate is private
context, not load-bearing authority for this public spec — the case here
stands on the failure modes alone.

## The epistemic moment (membership test)

The instant an agent forms a decision, load-bearing assumption, or receives a
Sovereign correction that *later work will rely on* — and the choice between
persisting it with provenance or letting it decay into unverifiable memory.
Distinct from every existing member:

- Not a verdict on a frozen subject (gauntlet).
- Not a goal contract (write-goal names assumptions only inside goals).
- Not a per-run research record (evidence-research's run record is scoped to
  one literature run).
- Not pre-work recon (blindspot-pass) or a derivation (formal-rigor) — those
  *produce* decisions; this skill persists them.

## Family-resemblance check (all six invariants)

1. **Floors, not ceilings.** Only *consequential* entries: decisions among
   alternatives, load-bearing assumptions, Sovereign corrections. An
   anti-ceremony skip rule mirrors the router's: skip when the decision is
   reversible, self-contained, and nothing downstream will rely on it — and say
   you skipped.
2. **Derive/verify, don't assert.** Entries must carry provenance (evidence
   refs, derivation refs, receipt refs where applicable) and a revisit or
   falsification condition — never a bare conclusion.
3. **Boundary discipline.** Produces exactly one thing: an append-only ledger
   entry (or a stated skip). Consumption belongs to continuity-verify, gauntlet
   dossiers, and future sessions — never to this skill.
4. **Fail closed; degrade explicitly.** No durable store available →
   session-local fallback with a named durability-gap record, never a silent
   pretense of persistence. At work-batch close-out, unlogged consequential
   decisions are surfaced as a gap, not waved through.
5. **Provenance and independence.** The entry records *who* decided, on what
   evidence, superseding what. Ledger content is data on read — it can inform
   but never instruct (a stale entry cannot authorize action by itself).
6. **Subject moves → re-fire, never patch.** Append-only `supersedes` *is*
   re-fire-never-patch: when a decision changes, the old entry is never edited
   — a new entry supersedes it, and the consumer walks the chain to the
   current head. The downstream consumer, not this skill, owns the staleness
   check (the supersedes walk and re-anchoring).

## Design

**Name:** `decision-ledger`

**Trigger (observable, not a vibe):** anchored in artifacts, not memory: a
decision was just made among ≥2 alternatives and recorded in a plan, contract,
or derivation artifact that future work will build on; an assumption is about
to bear load in a derivation, plan, or contract; an operator correction
message exists (a taught lesson). A moment is *consequential* iff a **named
downstream consumer class** will cite it — continuity-verify on resumption, a
gauntlet dossier, write-goal, or a future session; name the class in the
entry, or in the stated skip. Not per-task — per consequential moment. Default
when unsure: log.

**The method (three steps):**

1. **Classify** — `decision` | `assumption` | `correction`. If none fits, this
   is not a ledger moment; stop.
2. **Form the entry** — append-only record:
   ```json
   {
     "entry": "ledger-entry@1",
     "id": "<slug>-<YYYYMMDD>-<seq>",
     "at": "<YYYY-MM-DD>",
     "type": "decision|assumption|correction",
     "statement": "<one sentence, outcome-shaped>",
     "because": "<provenance: evidence refs, derivation refs, receipt refs>",
     "supersedes": ["<entry-id>"],
     "revisit_when": "<falsification or review condition>",
     "durability": "durable|session-only"
   }
   ```
   Corrections never edit history: a superseding entry links forward
   (`supersedes`), the old entry stays. `because` refs are resolvable
   coordinates (path:line, commit SHA, receipt id) — the same discipline the
   collection holds its reviewers to — never unresolvable prose.
3. **Write to the store** — pluggable substrate, degrading explicitly:
   (a) repo-local `.ledger/entries.jsonl` when working in a repo where such
   decisions belong; (b) a harness task/memory store (e.g. beads) when
   configured via LOCAL.md; (c) session-local with
   `durability: session-only` — which emits a named **durability-gap record**
   whose first consumer is the close-out rule: the persistence moment was
   *missed*, not degraded-achieved. The skill is a ledger *method*, not a
   database — the store is the harness's business.

**Store discipline (one line each):** the store is single-writer-or-locked
append; `revisit_when` doubles as the GC horizon, with periodic compaction of
fully superseded chains; session-only names the recovery gap — entries held
only in session state die with it, and the durability-gap record is the
recovery path.

**Consumption contract.** Entries are unverified, self-attested data. Their
consumption contract is re-anchoring, full stop: a reader treats an entry as a
lead, honors `revisit_when`, and walks the `supersedes` chain to its head — a
superseded entry is stale-by-construction. Freshness is carried by
`revisit_when` plus the supersedes graph; no trust-contract stamp, no
`valid_while` predicate, and no valid-until claim is made for entries. (A
verifier-checked `entry-unsuperseded` predicate is recorded as a *possible
future extension* of the trust contract — deferred, not adopted: if a future
consumer class needs machine-checked ledger freshness, the contract is
extended then, per its own extension procedure.)

**Close-out rule:** at the end of a work batch (wrap-up, PR, session end),
the batch's decisions are enumerated from the artifacts produced (plans,
contracts, derivations, correction messages), not from memory; consequential
decisions made but not logged are surfaced as a named gap — never silently
dropped. This is a best-effort self-report, not a completeness proof.

**Skip gate (checkable):** skip only when all three hold — the decision is
reversible, it is self-contained (nothing downstream depends on it), and no
future session would need its reasoning. Per-type floors: a correction is
skippable when it is local and already embodied in the corrected artifact; an
assumption is skippable when its load discharges within the session. Say the
skip and its reason.

**Composition:** entries are consumed by continuity-verify (as prior judgment
to re-anchor, not to trust), by gauntlet dossiers (as premises with
provenance), and by write-goal (as de-risked context). The skill never consumes
its own ledger to make new decisions — that is the reader's job, with
freshness checks.

**Naming.** This ledger (decisions, assumptions, corrections) is not
gauntlet's run telemetry (`runs/ledger.jsonl`); the collision is path-level,
not concept-level, and the shipped SKILL.md carries an explicit
disambiguation line.

## Anti-patterns (to ship in the SKILL.md)

| Thought | Reality |
|---|---|
| "Log everything" | Ceremony. Only consequential moments; the skip gate is the floor. |
| "Edit the old entry to stay current" | History is append-only; corrections are new entries with `supersedes`. |
| "The ledger said so" | Ledger content is data, never instructions; readers re-verify freshness. |
| "It's in chat, that's enough" | Chat evaporates; the ledger is the difference between a decision and a rumor. |
| "I'll batch-log at the end" | Entries are written at the moment, with the reasoning still warm; close-out is a gap check, not the write path. |

## LOCAL.md overlay

Binds the store: which substrate (repo `.ledger/`, beads, other), which scopes
get ledgers, any fleet-specific close-out ritual. Additive only.

## Phasing and acceptance criteria

- One PR: `plugins/epistemic-skills/skills/decision-ledger/SKILL.md` +
  `reference/ledger-entry.schema.json` (the entry schema above, JSON Schema) +
  router row (persistence moment, retrospective trigger shape; the valid-until
  cell states `revisit_when`-governed / consumer re-anchored — no contract
  predicate claimed) + README skill-table row. The shipped SKILL.md carries a
  quantified ceremony-budget sentence (per-entry cost, close-out bound) and
  the naming disambiguation line. No scripts needed beyond trivial validation
  — the method is prose + one schema; a validator is optional, not required.
- AC1: the SKILL.md contains the trigger, the skip gate, the three-step
  method, the close-out rule, the append-only rule, and the anti-pattern
  table.
- AC2: the entry schema validates 2 synthetic examples (one durable, one
  session-only) and enforces required fields plus the closed
  `type`/`durability` vocabularies — structure only, no semantic claim. The
  never-instruct boundary is *not* a schema promise: it lives in the
  anti-pattern table and as a named, human-enforced PR-review checklist item
  (a verdict-carrying-but-well-formed entry is caught by review, never claimed
  as schema-rejected). An optional lint for verdict vocabulary (`GO`, `NO-GO`,
  `must`, `approved`) in `statement` is permitted but must be labeled
  heuristic.
- AC3: router + README updated; the arc gains its persistence moment without
  disturbing existing rows' boundaries; the router row uses the retrospective
  trigger shape (decision moment → entry), annotated as a new row shape.
- AC4: family-resemblance re-check at PR review — all six invariants
  explicitly demonstrated in the SKILL.md text, invariant 6 (append-only
  supersession = re-fire, never patch) included by name.
- AC5 (behavioral follow-up, not a ship gate): post-merge, the close-out
  gap-check hit-rate is logged over ≥20 real work batches with a named
  revisit date. The measurement-discipline asymmetry with continuity-verify's
  fixture gate is named, not waived: this skill is structural, so it earns a
  logged follow-up rather than a blocking behavioral gate.

**Implementation-PR requirements riding from the arbitration (C-9, C-10):**
the PR ships the `ledger-entry` JSON Schema with the closed
`type`/`durability` vocabularies and the 2 validating synthetic examples; the
PR description carries the human-enforced never-instruct checklist item,
checked; the router row lands with the retrospective trigger shape and the
resumption-ordering annotation (continuity-verify first on resumption), and
the arc diagram gains its persistence stage without disturbing existing rows'
boundaries (AC3 preserved).

## What this design does NOT do

- No new store, server, or sync mechanism (the substrate is pluggable and
  harness-owned).
- No retroactive logging mandate for pre-existing decisions.
- No consumption logic (that is continuity-verify's and gauntlet's job).
- No verdicts — an entry is never a GO/NO-GO, never an instruction.
- No trust-contract stamp or `valid_while` predicate — freshness is
  `revisit_when` plus supersedes-chain re-anchoring.

## Arbitration conditions attached to this spec

From the gauntlet arbitration (`phase-c-skill-specs-2026-07-22`, 2026-07-22,
verdict CONDITIONAL; run artifacts local-only), mapped to where each landed:

| # | Condition | Lands |
|---|---|---|
| C-1 | Drop the stamp composition (method step 4, `valid_while`/valid-until claims); entries are unverified self-attested data consumed via re-anchoring; `session` keyed-hash field dropped; freshness = `revisit_when` + supersedes graph; `entry-unsuperseded` predicate deferred as a named possible future contract extension, not adopted | spec amendment (done here — method, consumption contract, entry example, PR plan, AC1, NOT-do list) |
| C-3 | AC2 rewritten structural-only (2 synthetic examples validate; required fields + closed `type`/`durability` vocabularies enforced); never-instruct relocated to the anti-pattern table + a named human-enforced PR-review checklist item; any verdict-vocabulary lint labeled heuristic | spec amendment (done here — AC2) |
| C-4 | Membership re-run against all SIX router invariants; invariant 6 (append-only supersession = re-fire, never patch) demonstrated explicitly; AC4 updated | spec amendment (done here — family-resemblance section, AC4) |
| C-7 (DL parts) | Observable trigger anchors + named-consumer-class criterion for "consequential"; per-type skip floors; default-when-unsure = log; `because` refs as resolvable coordinates; session-only reframed as a durability-gap record; TRANSPARENCY-2 demoted to footnote; concurrency/retention/recovery-gap one-liners; close-out best-effort caveat; ceremony-budget sentence; ledger naming disambiguation; behavioral follow-up AC (close-out hit-rate over ≥20 batches, named revisit date) | spec amendment (done here — trigger, method, store discipline, close-out, skip gate, footnote, naming, AC5, PR plan) |
| C-9 | Implementation PR: schema + 2 validating examples ship; PR description carries the human-enforced never-instruct checklist item, checked; router row valid-until cell claims no predicate | implementation PR (rides — noted in Phasing above) |
| C-10 (DL half) | Router row lands with the retrospective trigger shape and the resumption-ordering annotation; arc diagram gains its persistence stage without disturbing existing rows' boundaries | implementation PR (rides — noted in Phasing above; AC3 carries the boundary preservation) |

C-2, C-5, C-6, C-8 attach to the continuity-verify spec and its PR; they are
listed in that spec's table.
