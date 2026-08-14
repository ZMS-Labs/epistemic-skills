# Corrections — PR #175

The records in this directory were reviewed on the PR that committed them.
Seven findings landed across two rounds; all seven were upheld. The records now
in place are the corrected versions; the originals are in git history at
`9fbfea4` and are worth reading beside this file, because three of round 2's
four defects are ones the records themselves were written to guard against.

The round-3 findings are recorded at the bottom. Two of the three were **the
round-2 fixes not carried through the whole file** — a corrected claim in one
field left standing in its contradicted form in another. That is its own
lesson, and it is the same one the census learned twice on the code side of
this PR: fixing the structure and leaving the prose is not a fix.

## Round 2

## P1 — the authorship record's empirical closure was vacuous

`grant-authorship.json` recorded `empirical_closure: pending` with the
prediction that, at window close, *"no mission adopts a confirmation-gated
field."* That record's own `valid_while` includes
**`grants_paths-remains-unshipped`**. A field that cannot exist cannot be
adopted, so the prediction was true by construction.

This matters more than a spoiled test: the synthesis named that observation as
the route by which the operator-confirmed option would be settled. The record
therefore claimed a path to closing the authorship question that could never
produce a discriminating result — and adoption of *unrelated* high-friction
declarations, the fallback proxy, cannot separate "operator-confirmed grants
were rejected" from "envelope adoption behaves as it always has."

Corrected to `blocked`, naming what would actually be required: a bounded pilot
of at least one authorship mechanism, which is a separate authorization. The
authorship question is now open **by construction rather than by evidence**,
and the record says so.

The irony is exact: this is the vacuous-green defect the census was built to
detect, committed inside the record that governs the census's own gate.

## P2 — option A was not census-computable, which was the constraint it won on

`predicate.json` selected *"≥1 chain-bound receipt AND a **non-scratch**
workspace root"* against a hard constraint reading *"computable by the census
from fields it already reports."* The census emits the root **path string** and
nothing else; nothing in the record or the code defined what makes a root
non-scratch. Two readers could produce different denominators from identical
census output, and a renamed scratch root could not be classified consistently
at all.

So the option that beat three others *on computability* was not computable. It
had smuggled in a human judgement and called it a field.

Corrected: option A now requires a root drawn from an **admitted-root set fixed
and recorded before observation begins**, with a hard constraint requiring
membership to be reproducible from census output plus that list. The concession
is recorded too — this moves the judgement from "what is a scratch root" to
"which roots count", which is smaller, made once, and auditable, but it is not
the elimination of judgement.

## P2 — the window was described as already open

`system_boundary` said the window *"opened now"* while the same record's
synthesis conditioned it on a non-emptiness check that has not run. If
observation had begun in that state, the denominator could have been empty and
the interval before predicate admission would have had no reproducible
membership rule. Corrected to **planned**, opening only when the precondition
passes.

## P2 — the gate owner was never actually named

The README claimed these records discharge the es#150 requirement for a *named
owner*, while both records carried only the unassigned actor label
`gate owner`. A prerequisite is not met by an artifact that describes the role
and omits the person. The operator is now named as the principal
(`operator:zach`, the `operator_ref` convention this contract's own fixtures
use), with the readout-preparing agent listed separately and explicitly not
judging.

That defect is the same shape as the reversal recorded *inside*
`grant-authorship.json`: a declaration that names no principal is not a
control. It appeared in the record that says so.

## Round 3

### P2 — the non-emptiness test still asked the reader to judge "scratch"

Round 2 replaced "non-scratch root" with membership in a recorded
admitted-root set — in the *option* and in a new *hard constraint*. The
preregistered test in `empirical_closure` was left exactly as written: *"a
real repository checkout rather than a scratch/ path"*, disconfirmed by *"all
receipt-bearing missions sit under scratch-style roots."*

So the instrument that actually decides whether the window may open still
carried the defect, and could not satisfy the very condition round 2 added
two fields away (*"the non-emptiness test passes against that recorded set"*).
Two operators could still produce different prerequisite results from one
census run.

Corrected: the test is now string membership in the admitted-root set, with
the recording step sequenced ahead of the census run inside the test itself.

**I had fixed the conclusion and left the measurement.** The correction was
applied where the argument lived and not where the work happens.

### P2 — the authorship record still routed the decision through the es#166 window

Round 2 set `empirical_closure` to `blocked` and rewrote the recovery moves to
require a pilot, stating that re-firing against window data would repeat the
vacuity. The synthesis `basis` — the field a consumer reads for the durable
outcome — still said the decision *"cannot be closed before the es#166 window
returns adoption evidence."*

A reader following the outcome would therefore wait for evidence the same
record says that window cannot produce. Corrected: the basis now states the
question stays open and explicitly **not** pending on that window, pointing at
the pilot.

### P2 — a validity condition that the window's own success would trip

`valid_while` carried `estate-armed-count-remains-zero`. Option A references
receipts and admitted-root membership only; the zero-armed count is dated
evidence (census run 2026-08-13) bearing on option **D** via `d3`. As a
validity condition it would void the governing record the moment any mission
armed — and arming is a positive envelope-adoption event this window exists to
measure. **The first interesting datapoint would have destroyed the rule it
arrived under**, leaving the adoption result with no valid governing
predicate.

Removed from `valid_while`, with the evidential role kept where it belongs and
the consequence recorded: a nonzero armed count retires `d3`'s second line of
evidence against D, but not `d1`'s refutation, which is structural and
observation-independent. The selection of A stands either way.

## Standing limit

These corrections came from an automated reviewer, not from a second
derivation. They are code-review findings against reasoning artifacts, which is
weaker than an independent re-derivation and stronger than nothing. Both
records remain single-model-family work with no cross-family independence, and
neither discharges any externally-enforced safety gate.
