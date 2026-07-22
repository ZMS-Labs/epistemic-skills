# continuity-verify — new skill design

**Date:** 2026-07-22
**Status:** Draft for operator review — amended after gauntlet run
`phase-c-skill-specs-2026-07-22` (2026-07-22; verdict: CONDITIONAL). The
pre-review conditions (C-1…C-7) are landed in this amendment; the remaining
conditions (C-8…C-10) ride as implementation-PR requirements. Run artifacts
are local-only (`outputs/` is not committed); the run is cited by name and
date only. See the conditions table at the end of this spec.
**Type:** New skill (discipline candidate) for the epistemic-skills collection
**Basis:** gap analysis (`docs/audits/2026-07-22-collection-audit/06-gap-analysis.md`, candidate (a) — verdict PROPOSE, gated on resume fixtures); control-plane creation gates (`docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md:285-296`).

## Problem

After an interruption — context compaction, session restart, cross-device
handoff — the agent holds *memories* of prior state ("we decided X", "Y is
done", "the repo is at Z") that are indistinguishable in-band from verified
facts. Platform behavior guarantees this hazard recurs: auto-compaction
summaries preserve conclusions, not live state; session handoffs carry claims,
not proof. Acting on unverified memory produces the two classic failures:
false-DONE (declaring finished what is not) and stale-state action (building on
a premise that moved). No existing skill owns this moment: blindspot-pass maps
request→territory before *new* work; gauntlet's truth-gate verifies premises of
a *frozen subject*; write-goal inspects only persistent-goal state. This is
memory→artifact re-derivation before *continuing* work.

## The epistemic moment (membership test)

Context resumption with prior-state claims. The instant an agent is handed a
summary, a resumed session, or a handed-off task whose value depends on what
was true *before* — and must decide what is true *now* before acting. The
companion moment to decision-ledger: that skill persists; this one distrusts
and re-derives.

## Family-resemblance check (all six invariants)

1. **Floors, not ceilings.** One re-derivation pass, sized to the stakes of
   the remembered claims. Trivial resumptions (the summary itself says nothing
   load-bearing) pass with a one-line check, not a ritual.
2. **Derive/verify, don't assert.** Every resumed claim is re-anchored to a
   durable artifact (file, ledger entry, commit, run record, receipt) or
   explicitly stamped `(UNVERIFIED)` — the same move gauntlet Step 0 makes,
   generalized to the agent's own trajectory.
3. **Boundary discipline.** Ends at a verified state digest + a
   stale/unverified list (or a re-scoped task when re-derivation contradicts
   the summary). Hands to the router; never does the resumed work itself.
4. **Fail closed; degrade explicitly.** Missing evidence → claim marked
   unverified, never silently trusted. Unverifiable-core → the task re-scopes
   to re-establishing state, it does not proceed on faith.
5. **Provenance and independence.** The compaction summary / handoff note is
   lower-provenance input — data, never instructions — invariant 5 applied to
   the agent's own memory. A remembered "the user approved X" is a claim to
   verify, not an authorization.
6. **Subject moves → re-fire, never patch.** A `contradicted` claim re-scopes
   the task rather than patching the summary — contradiction → re-scope *is*
   invariant 6 applied to the agent's own trajectory. The digest is void the
   moment the underlying state moves; the skill re-fires at its next
   resumption trigger rather than amending a stale digest.

## Design

**Name:** `continuity-verify`

**Trigger (observable):** a session begins or resumes with a compaction
summary, a handoff note, or a prior-session task whose next action depends on
remembered state. Not for fresh tasks with no prior-state claims (blindspot-pass
owns those).

**The method (five steps):**

1. **Enumerate load-bearing claims.** From the summary/handoff, extract the
   claims the next actions depend on: state claims ("X is done", "branch Y is
   merged", "the tests pass"), decision claims ("we chose A"), authorization
   claims ("the user approved Z"). Skip trivia — claims nothing depends on are
   not re-derived (floors). Persistent-goal state is one claim-class inside
   this enumeration (write-goal's goal inspection runs here, not as a separate
   pass).
2. **Re-anchor each claim** to a durable artifact: file content, git state
   (`git log`, `git status`, PR state), ledger entries, run records,
   receipts/stamps. Each claim gets: `verified` (artifact confirms),
   `contradicted` (artifact disagrees — live data wins), or `(UNVERIFIED)` (no
   artifact). Receipts and stamps are consumed per the trust contract: check
   `valid_while` predicates; a stale receipt means re-run exactly the
   freshness-sensitive check.
3. **Check the ledger.** decision-ledger entries for this scope are *prior
   judgment*: read them as leads, honor `revisit_when` conditions, never as
   settled fact without re-anchoring. When a ledger is present, mechanically
   walk each entry's `supersedes` chain to its head — a superseded entry is
   stale-by-construction and is re-derived, never consumed as current. If
   decision-ledger is absent, skip this step and say so — the skill works
   without it.
4. **Emit the state digest.** Verified claims (with anchors), contradicted
   claims (with the live value), unverified claims (stamped), and any
   `accepted_unverified` records (first-class digest field: the acceptor and
   the risk taken — see step 5). If a contradiction or unverifiable core claim
   changes what the task is, **re-scope the task** and say so — that is a
   successful pass, not a failure.
5. **Hand off.** The digest feeds the router; the resumed work proceeds only
   on verified or explicitly-accepted-unverified state. Acceptance is
   authority-bound: self-acceptance of an unverified claim is permitted only
   at the `quick` dial and only for low-stakes claims. At `standard`/`deep`, a
   load-bearing unverified claim requires acceptance by a named non-self
   authority (the operator, or an operator-delegated authority), recorded in
   the digest's `accepted_unverified` field carrying the acceptor and the risk
   taken; absent that, work halts or re-scopes. An unverifiable approval claim
   escalates — never authorizes — at every dial.

**Stakes dial:** `standard` (default — re-anchor load-bearing claims),
`quick` (resumption within minutes, same machine, claims low-stakes — spot
check the top 3, selected by downstream-dependence/blast-radius:
authorization > state > decision), `deep` (cross-device handoff, long gap, or
high-stakes claims — full enumeration + independence checks on any claimed
approvals/authorizations).

**Arc ordering:** on a post-interruption resumption this skill fires first —
its digest feeds the router, which may then fire blindspot-pass for unfamiliar
territory. The re-anchor move is extracted from gauntlet Step 0; gauntlet
remains canonical for frozen subjects.

**Ship order:** this skill and decision-ledger ship independently, in either
order. Step 3 composes with decision-ledger but does not require it (the
absence rule above); neither skill's gate depends on the other merging first.

## Anti-patterns (to ship in the SKILL.md)

| Thought | Reality |
|---|---|
| "The summary says it's done" | The summary is a claim, not a state. Re-anchor or stamp. |
| "I remember this clearly" | Memory is the lowest-provenance source there is — including your own. |
| "Re-checking everything wastes time" | You re-check exactly the load-bearing claims; the dial sizes the pass. |
| "The user approved it last session" | Authorization claims are verified like everything else — an unverifiable approval claim escalates, it does not authorize. |
| "Just continue, we'll notice if it's wrong" | Noticing mid-implementation is the expensive path this skill exists to prevent. |

## The fixture gate (ship criterion, redesigned per the gauntlet arbitration)

This skill ships behind a **deterministic smoke check, honestly labeled — not
a measurement** (control-plane creation gate 5). The harness adopts the
gauntlet battery precedent wholesale:

- **Battery architecture.** Fixture-facing inputs vs a scorer-only
  ground-truth divergence map; a deterministic stdlib `score.py` decides
  catches — no self-judged "catch". A blinding protocol is stated in the ACs.
- **Battery.** ≥8 fixtures: 2 false-DONE traps, 2 stale-state traps, 2
  authorization traps (one unverifiable-approval, one forged-provenance), and
  2 clean controls — each an interruption scenario with planted divergence
  between the summary and the artifacts.
- **Scoring is a confusion matrix.** Gate: ≥5/6 traps caught **and** 0 of 2
  clean controls falsely flagged. A stamp-everything-`(UNVERIFIED)` parody
  catches every trap but flags the controls — it fails by design. The parody
  is a standing acceptance probe: a null flag-everything skill is run through
  the harness pre-merge and **must fail** the shipped gate.
- **Independence.** ≥2 fixtures authored or adversarially extended by a
  non-author (a different model family is acceptable), or mined from real
  compacted-session logs; provenance recorded.
- **Pinned arms.** Model, harness, and baseline prompt are recorded per run;
  a cooperative-baseline arm cannot satisfy the baseline condition by
  construction of the pinned prompt.
- **Repetition.** ≥3 runs per condition, per-run results committed; pass =
  threshold met in all runs.
- **Report, don't power.** Per-fixture paired delta (skilled − unskilled
  baseline on identical scenarios) plus a binomial CI, reported under the
  smoke-scale label, with a named path to a real rate via logged genuine
  resumes.
- **Honest park.** If the harness cannot meet this bar, the PR ships the
  honest-park state — method documented, fixtures failing — never a waived
  gate. The spec is not a promise.

## Phasing and acceptance criteria

- One PR: `plugins/epistemic-skills/skills/continuity-verify/SKILL.md` +
  `evals/resume-fixtures/` (fixtures, scorer-only ground truth, deterministic
  scorer, per-run results with pinned arms, non-author provenance record) +
  router row + README skill-table row.
- AC1: SKILL.md contains the trigger, the five-step method (including the
  supersedes-chain walk and the ledger-absence rule), the stakes dial with
  the top-3 selection rule, the fail-closed rules, the arc-ordering line, and
  the anti-pattern table.
- AC2: the fixture battery exists, runs under the deterministic scorer, and
  meets the confusion-matrix gate in all ≥3 runs per condition — with the
  parody probe failing by design — or the PR is honest that the skill is
  parked, method documented, fixtures failing.
- AC3: composition lines: consumes decision-ledger entries via the
  supersedes-chain walk + re-anchoring, and handoff-receipts/stamps per their
  contracts (check `valid_while`; stale → re-run freshness check); hands the
  digest to the router. The router row uses the pre-arc trigger shape
  (resumption → digest before any resumed-work skill), annotated as a new row
  shape, with the double-fire ordering annotation (this skill first, then
  blindspot-pass).
- AC4: family-resemblance re-check at PR review — all six invariants
  explicitly demonstrated in the SKILL.md text, invariant 6 (contradiction →
  re-scope = re-fire, never patch) included by name.

**Implementation-PR requirements riding from the arbitration (C-8, C-10):**
the PR commits the fixtures, the scorer, the scorer-only ground truth, the
per-run results with model+harness pinned, and the non-author fixture
provenance record; the parody probe is run and its output committed (results
must reproduce byte-identically under the deterministic scorer); the router
row lands with the pre-arc trigger shape and the resumption-ordering
annotation, and the arc diagram gains its resumption stage without disturbing
existing rows' boundaries (AC3 preserved).

## What this design does NOT do

- No session-bank storage mechanics (private control-plane flow per the
  packaging decision; this skill is the *method*, storage stays private).
- No work resumption itself — it ends at the digest.
- No retroactive verification of every historical claim — only load-bearing
  ones for the task at hand.
- No authorization inheritance — remembered approvals are verified, never
  inherited.
- No requirement that decision-ledger exist — the ledger absence rule is
  explicit; composition is optional, in either ship order.

## Arbitration conditions attached to this spec

From the gauntlet arbitration (`phase-c-skill-specs-2026-07-22`, 2026-07-22,
verdict CONDITIONAL; run artifacts local-only), mapped to where each landed:

| # | Condition | Lands |
|---|---|---|
| C-2 | Step 3 strengthened: mechanical `supersedes`-chain walk to the head when a ledger is present; superseded entries stale-by-construction and re-derived, never consumed as current; explicit absence rule ("if decision-ledger is absent, skip this step and say so") | spec amendment (done here — step 3) |
| C-4 | Membership re-run against all SIX router invariants; invariant 6 (contradiction → re-scope = re-fire, never patch) demonstrated explicitly; AC4 updated | spec amendment (done here — family-resemblance section, AC4) |
| C-5 | Fixture gate redesigned: battery architecture (fixture-facing inputs vs scorer-only ground truth, deterministic stdlib scorer, blinding); confusion-matrix scoring (≥5/6 traps AND 0/2 controls falsely flagged); ≥8 fixtures (2 false-DONE, 2 stale-state, 2 authorization, 2 clean controls); ≥2 non-author fixtures with provenance; pinned arms; ≥3 runs per condition, pass = all runs; per-fixture paired delta + binomial CI under the smoke-scale label with a named path to a real rate; parody probe as a standing acceptance check; honest-park fallback retained; gate relabeled a deterministic smoke check | spec amendment (done here — fixture gate section, AC2) |
| C-6 | Step 5 rewritten: self-acceptance only at `quick` dial for low-stakes claims; load-bearing unverified claims at `standard`/`deep` require a named non-self acceptor recorded in a first-class `accepted_unverified` digest field (acceptor + risk taken); otherwise halt or re-scope; approval claims escalate at every dial | spec amendment (done here — steps 4–5) |
| C-7 (CV parts) | Top-3 selection rule (authorization > state > decision); arc-ordering line (CV fires first on resumption, digest feeds router, then blindspot-pass; write-goal inspection as one claim-class); gauntlet-Step-0 extraction named; ship-order independence stated; router row shapes for the pre-arc trigger specified in ACs | spec amendment (done here — step 1, dial, arc ordering, ship order, AC3) |
| C-8 | Implementation PR: harness built per C-5 and run; fixtures, scorer, ground truth, pinned per-run results, and non-author provenance committed; parody probe run and committed; honest-park state if the gate is not met — never a waived gate | implementation PR (rides — noted in Phasing above) |
| C-10 (CV half) | Router row lands with the pre-arc trigger shape and the resumption-ordering annotation; arc diagram gains its resumption stage without disturbing existing rows' boundaries | implementation PR (rides — noted in Phasing above; AC3 carries the boundary preservation) |

C-1, C-3, C-9 attach to the decision-ledger spec and its PR; they are listed
in that spec's table.
