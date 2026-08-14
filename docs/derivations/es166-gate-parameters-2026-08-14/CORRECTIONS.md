# Corrections — round 2 of PR #175

The records in this directory were reviewed on the PR that committed them, and
four findings landed against them. All four were upheld. The records now in
place are the corrected versions; the originals are in git history at
`9fbfea4` and are worth reading beside this file, because three of the four
defects are ones the records themselves were written to guard against.

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

## Standing limit

These corrections came from an automated reviewer, not from a second
derivation. They are code-review findings against reasoning artifacts, which is
weaker than an independent re-derivation and stronger than nothing. Both
records remain single-model-family work with no cross-family independence, and
neither discharges any externally-enforced safety gate.
