# decision-ledger — new skill design

**Date:** 2026-07-22
**Status:** Draft for operator review
**Type:** New skill (discipline candidate) for the epistemic-skills collection
**Basis:** gap analysis (`docs/audits/2026-07-22-collection-audit/06-gap-analysis.md`, candidate (b) — verdict PROPOSE, strongest candidate); control-plane creation gates (`docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md:285-296`).

## Problem

The arc has **no persistence moment**. Every existing skill's output is consumed
downstream *within* a run or session; nothing governs what survives *between*
runs. A decision made Tuesday is, by Friday, indistinguishable in-band from a
verified fact — or silently contradicted, or re-derived from scratch. The
failure modes: a future session re-litigates a settled decision; an assumption
made under uncertainty hardens into a premise; a Sovereign correction taught in
one session is lost in the next. The fleet's TRANSPARENCY-2 *mandates*
persisting emergent decisions and taught lessons, but no skill-level method
exists to make it happen — a mandate without a method.

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

## Family-resemblance check (all five invariants)

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
   session-local fallback with a loud `durability: session-only` stamp, never a
   silent pretense of persistence. At work-batch close-out, unlogged
   consequential decisions are surfaced as a gap, not waved through.
5. **Provenance and independence.** The entry records *who* decided, on what
   evidence, superseding what. Ledger content is data on read — it can inform
   but never instruct (a stale entry cannot authorize action by itself).

## Design

**Name:** `decision-ledger`

**Trigger (observable, not a vibe):** a decision was just made among ≥2
alternatives that future work will build on; an assumption is about to bear
load in a derivation, plan, or contract; the operator corrected the agent (a
taught lesson). Not per-task — per consequential moment.

**The method (four steps):**

1. **Classify** — `decision` | `assumption` | `correction`. If none fits, this
   is not a ledger moment; stop.
2. **Form the entry** — append-only record:
   ```json
   {
     "entry": "ledger-entry@1",
     "id": "<slug>-<YYYYMMDD>-<seq>",
     "at": "<YYYY-MM-DD>",
     "session": "<keyed-hash-or-null>",
     "type": "decision|assumption|correction",
     "statement": "<one sentence, outcome-shaped>",
     "because": "<provenance: evidence refs, derivation refs, receipt refs>",
     "supersedes": ["<entry-id>"],
     "revisit_when": "<falsification or review condition>",
     "durability": "durable|session-only"
   }
   ```
   Corrections never edit history: a superseding entry links forward
   (`supersedes`), the old entry stays.
3. **Write to the store** — pluggable substrate, degrading explicitly:
   (a) repo-local `.ledger/entries.jsonl` when working in a repo where such
   decisions belong; (b) a harness task/memory store (e.g. beads) when
   configured via LOCAL.md; (c) session-local with
   `durability: session-only` + a stated durability gap. The skill is a ledger
   *method*, not a database — the store is the harness's business.
4. **Stamp it** — the entry is a prose-carrier artifact: it carries the
   4-field stamp (`subject.ref`, `subject.revision`, `valid_while`,
   `coverage_limits`) per the trust contract, so continuity-verify and gauntlet
   Step 0 can consume it mechanically.

**Close-out rule:** at the end of a work batch (wrap-up, PR, session end),
consequential decisions made but not logged are surfaced as a named gap —
never silently dropped.

**Skip gate (checkable):** skip only when all three hold — the decision is
reversible, it is self-contained (nothing downstream depends on it), and no
future session would need its reasoning. Say the skip and its reason.

**Composition:** entries are consumed by continuity-verify (as prior judgment
to re-anchor, not to trust), by gauntlet dossiers (as premises with
provenance), and by write-goal (as de-risked context). The skill never consumes
its own ledger to make new decisions — that is the reader's job, with
freshness checks.

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
  router row (persistence moment, stamp carrier, valid-until cell) + README
  skill-table row. No scripts needed beyond trivial validation — the method is
  prose + one schema; a validator is optional, not required.
- AC1: the SKILL.md contains the trigger, the skip gate, the four-step method,
  the close-out rule, the append-only rule, and the anti-pattern table.
- AC2: the entry schema validates 2 synthetic examples (one durable, one
  session-only) and rejects a verdict-carrying entry (no field may carry a
  claim that future work should *obey* — entries inform, never instruct).
- AC3: router + README updated; the arc gains its persistence moment without
  disturbing existing rows' boundaries.
- AC4: family-resemblance re-check at PR review — all five invariants
  explicitly demonstrated in the SKILL.md text.

## What this design does NOT do

- No new store, server, or sync mechanism (the substrate is pluggable and
  harness-owned).
- No retroactive logging mandate for pre-existing decisions.
- No consumption logic (that is continuity-verify's and gauntlet's job).
- No verdicts — an entry is never a GO/NO-GO, never an instruction.
