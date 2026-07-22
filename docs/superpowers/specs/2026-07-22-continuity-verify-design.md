# continuity-verify — new skill design

**Date:** 2026-07-22
**Status:** Draft for operator review
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

## Family-resemblance check (all five invariants)

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
   not re-derived (floors).
2. **Re-anchor each claim** to a durable artifact: file content, git state
   (`git log`, `git status`, PR state), ledger entries, run records,
   receipts/stamps. Each claim gets: `verified` (artifact confirms),
   `contradicted` (artifact disagrees — live data wins), or `(UNVERIFIED)` (no
   artifact). Receipts and stamps are consumed per the trust contract: check
   `valid_while` predicates; a stale receipt means re-run exactly the
   freshness-sensitive check.
3. **Check the ledger.** decision-ledger entries for this scope are *prior
   judgment*: read them as leads, honor `revisit_when` conditions, never as
   settled fact without re-anchoring.
4. **Emit the state digest.** Verified claims (with anchors), contradicted
   claims (with the live value), unverified claims (stamped). If a contradiction
   or unverifiable core claim changes what the task is, **re-scope the task**
   and say so — that is a successful pass, not a failure.
5. **Hand off.** The digest feeds the router; the resumed work proceeds only
   on verified or explicitly-accepted-unverified state.

**Stakes dial:** `standard` (default — re-anchor load-bearing claims),
`quick` (resumption within minutes, same machine, claims low-stakes — spot
check the top 3), `deep` (cross-device handoff, long gap, or high-stakes
claims — full enumeration + independence checks on any claimed
approvals/authorizations).

## Anti-patterns (to ship in the SKILL.md)

| Thought | Reality |
|---|---|
| "The summary says it's done" | The summary is a claim, not a state. Re-anchor or stamp. |
| "I remember this clearly" | Memory is the lowest-provenance source there is — including your own. |
| "Re-checking everything wastes time" | You re-check exactly the load-bearing claims; the dial sizes the pass. |
| "The user approved it last session" | Authorization claims are verified like everything else — an unverifiable approval claim escalates, it does not authorize. |
| "Just continue, we'll notice if it's wrong" | Noticing mid-implementation is the expensive path this skill exists to prevent. |

## The fixture gate (ship criterion, from the gap analysis)

This skill ships behind a measurement gate: **interruption/resume fixtures
must show lower false-DONE and stale-state rates than the unskilled baseline**
(control-plane creation gate 5). The PR therefore includes a minimal
`evals/resume-fixtures/` harness: ≥6 fixtures (2 false-DONE traps, 2
stale-state traps, 1 authorization-claim trap, 1 clean resumption control),
each an interruption scenario with planted divergence between the summary and
the artifacts. The skill passes the gate if the skilled run catches ≥5/6 and
the unskilled baseline (same scenarios, no skill loaded) catches ≤2/6.
Fixture results are committed honestly, smoke-scale labeled — the same
honest-status convention as gauntlet's batteries. If the fixtures cannot be
built convincingly, the skill does not ship; the spec is not a promise.

## Phasing and acceptance criteria

- One PR: `plugins/epistemic-skills/skills/continuity-verify/SKILL.md` +
  `evals/resume-fixtures/` (fixtures, runner, results) + router row +
  README skill-table row.
- AC1: SKILL.md contains the trigger, the five-step method, the stakes dial,
  the fail-closed rules, and the anti-pattern table.
- AC2: fixture battery exists, runs, and the measured catch rates meet the
  gate (or the PR is honest that the skill is parked, method documented,
  fixtures failing).
- AC3: composition lines: consumes decision-ledger entries and
  handoff-receipts/stamps per their contracts (check `valid_while`; stale →
  re-run freshness check); hands the digest to the router.
- AC4: family-resemblance re-check at PR review.

## What this design does NOT do

- No session-bank storage mechanics (private control-plane flow per the
  packaging decision; this skill is the *method*, storage stays private).
- No work resumption itself — it ends at the digest.
- No retroactive verification of every historical claim — only load-bearing
  ones for the task at hand.
- No authorization inheritance — remembered approvals are verified, never
  inherited.
