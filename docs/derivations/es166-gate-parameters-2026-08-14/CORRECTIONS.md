# Corrections — PR #175

The records in this directory were reviewed on the PR that committed them.
**Twenty-three findings landed across rounds 2, 3, 4, 6, 7, 8, 9 and 11** —
every round that reviewed them — and all twenty-three were upheld. The records now in place are
the corrected versions; the originals are in git history at `9fbfea4` and are
worth reading beside this file, because three of round 2's four defects are
ones the records themselves were written to guard against.

Two patterns run through the whole list, and both are worth more than any
individual entry:

- **A correction applied to one field and not its sibling**, in five
  consecutive rounds. The es#166-window dependency alone took three rounds to
  remove from one short record, because each time I corrected the field I was
  pointed at and did not grep the file for the claim.
- **A fix sound about the case in front of it that silently assumed the next
  one away.** The cohort rule needed correcting in FOUR consecutive rounds:
  survivorship selection (6), then total-but-not-partial attrition (7), then a
  partial-attrition rule depending on an observation nobody takes (8), then
  new entrants with no admission rule and two rules disagreeing on which
  snapshot a missing member contributes (9), then unresolved attrition folded
  in as non-adoption and admissions with no persisted qualifying evidence
  (11).

The same lesson landed on the code side of this PR twice over: fixing the
structure and leaving the prose is not a fix.

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

## Round 4

### P2 — the record voided itself the moment its own commit landed

`valid_while` carried `census-computable-field-set-unchanged`, and the README
spelled out that this voids the record when the census's field set changes.
**The very commit publishing these records adds `epoch_skew` to every census
report** relative to the pinned `0fee7a0`. So the predicate was invalid on
landing, before its window could open — a governing rule that expired on
publication.

Corrected by narrowing the condition to the fields option A and the numerator
actually read (`root`, `active`, `receipt_count`, `scope_in`, `scope_out`,
`guard_count`) rather than the whole reported surface. Re-pinning to the
post-change census was the alternative and was rejected: the SHA does not
exist until this commit lands, so the record would have had to name its own
future.

### P2 — the numerator was never defined

The denominator was specified down to the field. The numerator was the phrase
*"a populated envelope"*, unglossed, while the census reports `scope_in`,
`scope_out`, `guard_mode` and `guard_count` as independent candidates. An
admitted mission with populated scope and no guards is adoption under one
reading and non-adoption under another, so two operators derive different
values of `p` from identical output.

**This is the same defect as the original "non-scratch root", on the other
half of the ratio** — and it survived a round in which that exact defect was
found, disposed, and written up. I fixed the denominator and did not look at
the numerator beside it.

Fixed: the numerator is now `scope_in` non-empty OR `scope_out` non-empty OR
`guard_count > 0`, recorded as a hard constraint and a synthesis condition so
it cannot be renegotiated after observation begins. The concession is recorded
too: `permissions` and `protected_state` appear in es#166's finding but are
not census-reported, so this numerator measures the reported subset and
understates envelope adoption as a whole.

### P2 — the window dependency, a third time

`coverage_limits[0]` still read *"the es#166 window is the instrument that
would observe it"* — after round 2 blocked the closure and round 3 fixed the
synthesis basis. Same claim, third field, third round. Corrected to state that
no currently planned instrument can observe it and that a bounded pilot is
required.

That this needed three rounds to remove from one short file is the honest
headline of round 4.

## Round 6

### P1 — the denominator would have shrunk by ordinary success

The cohort was *"active missions"*, read at the closing census. Over a 60-day
window missions complete. A mission that satisfied the predicate, adopted the
envelope, and then finished would leave **both** the numerator and the
denominator — so the closing ratio was computed over long-lived survivors, and
could have come back empty while a great deal of qualifying adoption happened
and finished.

That is survivorship selection, in a record whose P8 coverage exists to catch
selection defects, and whose `d1` refutes option D for a sibling of the same
error. I caught selection on the dependent variable and missed selection on
*survival* in the same ratio.

Corrected: the cohort is now fixed by **observation over the interval** — a
mission counts whether it is active or terminal when observed — with the
opening cohort recorded so attrition is visible, and an explicit closing rule:
an empty denominator against a non-empty opening cohort is attrition, reported
as such, never an adoption ratio over zero.

### P2 — the prerequisite passed on a partial census

The non-emptiness test said nothing about `answers_are_partial`. The census
sets that flag precisely when it has skipped stores it could not read — for
corruption, environmental failure, or epoch skew — and those stores are the
ones whose contribution to the ratio is unknown. So the window could open, and
later compute `p`, from a selectively incomplete estate.

The instrument this record governs was built to make incompleteness loud, and
the record consuming it ignored the flag. Corrected: both the prerequisite run
and the closing run must report `answers_are_partial == false`, and computing
a ratio over the readable subset is explicitly refused as a recovery move.

### P2 — the README still described the old validity condition

Round 4 narrowed `valid_while` to the six fields the measurement reads. The
README kept telling operators the record voids whenever "the census's
computable field set changes", which would have them discard a record its own
durable condition says still applies.

**Fourth consecutive round in which a correction landed in one surface and not
its sibling.** Rounds 3 and 4 each found two; round 6 found one. That the count
is falling is not evidence the habit is fixed.

## Round 7

### P1 — the cohort fix handled total attrition and not partial

Round 6 added a rule for an **empty** closing denominator. With two cohort
members and one disappearance the denominator is non-empty, so that rule never
fires — and because the opening record preserved only mission id, root and
lifecycle state, the disappeared member took its adoption state with it. An
adopted mission vanishing moves the reported ratio from **1/2 to 0/1**, in a
direction nobody chose and with nothing in the readout saying so.

So the fix for survivorship bias reintroduced survivorship bias one case in.
Corrected: the opening record now captures each member's denominator **and
numerator** state; a member observed adopting counts in the numerator at close
even if it later disappears; a member that vanishes having never been observed
adopting is reported as unresolved attrition rather than dropped; and whenever
any member is missing, the readout reports the full-cohort ratio **and** the
survivor-only ratio and states the gap.

### P2 — a premise the record itself called unobserved read as established

`empirical_premises` said flatly that candidate A *"selects a non-empty set of
missions on the live estate today"*, while `coverage_limits` said the estate
was unreachable and `empirical_closure` said `pending`. A consumer treating
listed premises as facts would take the prerequisite as already satisfied and
skip the complete census run the window depends on.

Corrected to state its own status in the field: pending observation, not
established, with an explicit instruction not to read the list as verified
facts.

### P2 — a fixed close plus a floating open silently shortened the window

Round 2 changed the opening to `planned`. The close stayed pinned at
2026-10-13, so a prerequisite passing on, say, 24 August yields 50 days of
observation with nothing saying whether that is acceptable.

The close **does not move** — it is the calendar deadline es#150 requires, and
sliding it to preserve a 60-day interval is the null-by-drift that ruling
forbids. So a late open shortens the observation, and that is now governed: the
readout states the actual interval rather than the nominal 60 days; the gate
owner records *before* opening whether a shortened interval still supports a
judgement (deciding that after seeing the ratio is choosing the standard to fit
the result); and non-passage by the close date is reported as the es#166
direction-1 finding rather than extending the window in silence.

## Round 8

### P1 — the partial-attrition rule assumed an observation nobody takes

Round 7 said a disappeared member's adoption counts *"on the strength of the
opening-cohort record."* But a member that starts with an empty envelope,
**adopts after opening**, and then disappears is recorded pre-adoption in that
snapshot and is gone from the closing census — and no observation cadence was
required anywhere in the record. So the rule asserted an observation
capability that did not exist, and the full-cohort numerator is unknowable in
exactly the case the cohort record was added to cover.

Corrected: interval re-observation on a cadence fixed before observation
begins, with every observation persisted; "observed adopting" now means a
persisted observation, never an inference. The residue is recorded as a
concession rather than glossed — an adoption and a disappearance that both
fall between two observations are indistinguishable from no adoption, and
that case is reported as unresolved attrition rather than absorbed into
either side of the ratio.

**Three consecutive rounds on one ratio.** Round 6 fixed survivorship
selection; round 7 found the fix handled only total attrition; round 8 found
the partial-attrition fix depended on an observation that never happens. Each
correction was sound about the case in front of it and silently assumed the
next one away.

### P2 — the README cohort procedure kept the old three-field record

`predicate.json` was corrected in round 7 to require each member's numerator
state; the operator-facing procedure in the README still said *mission id,
root, lifecycle state*. An operator following the README would leave no
numerator state for a disappeared member, making the required full-cohort
ratio unreconstructable — the durable condition and the instructions for
satisfying it disagreed.

**Sixth consecutive round** in which a correction landed in one surface and
not its sibling.

## Round 9

### P1 — new entrants had no admission rule

`d1`'s model says the cohort is *every qualifying mission observed at any
point in the interval*. The cadence procedure re-observed **only the opening
members**. A mission created during the 60 days, or one gaining its first
chain-bound receipt, therefore had no admission rule and could be omitted
entirely — biasing the ratio toward the opening population.

That is the same survivorship error as closing on survivors, taken at the
other end of the interval, and it appeared in the fix for the first one.
Corrected: each cadence observation now discovers and admits newly qualifying
missions.

### P2 — two rules disagreed on which snapshot a missing member contributes

The partial-attrition rule counts a vanished member's **later-observed**
adoption. The reporting rule computed the full-cohort ratio from the member's
**opening** state. One observation history, two numerators, depending on which
rule the reader happened to follow. Corrected: a missing member contributes
its *latest persisted observation*, never its opening snapshot.

### Where this leaves the record

**Four consecutive rounds on the cohort rule** — survivorship (6),
total-but-not-partial attrition (7), an observation nobody takes (8), and now
admission plus snapshot conflict (9). Each fix was sound about the case in
front of it. None of them was sound about the next one.

The correct reading is not that the rule is now finally right. It is that a
measurement design has been rewritten four times under review without an
independent derivation, and that the next round has found something every
time.

## Round 11

### P1 — a lower bound reported as the ratio

The round-9 rule had a missing member contribute its **latest persisted
observation**. For a member last seen with an empty envelope that adopts and
then disappears, that observation says *non-adopting* — and the same record
classifies it as **unresolved attrition**, i.e. numerator unknown. So the
readout would state a lower bound as if it were the adoption ratio, and could
drive the gate toward rejection on a value the record itself calls unknown.

Corrected to bounds: `p_low` (unresolved counted as non-adopting), `p_high`
(counted as adopting), the survivor-only ratio, and the unresolved count —
with the window closing **inconclusive** on any question where `p_low` and
`p_high` would answer differently. Picking either end and calling it the ratio
is choosing a result the evidence does not determine.

### P2 — admissions with no persisted evidence of qualifying

Option A's denominator requires `receipt_count >= 1`, and the persisted
observation fields recorded envelope state only. Once a store vanished,
nothing durable established that the member had ever qualified — so the cohort
could not be reproduced, and an erroneous or disputed admission was
indistinguishable from a valid one. The qualifying evidence is now persisted
at the admitting observation.

### P2 — the validity condition named six fields and depended on nine

Round 4 narrowed `valid_while` to the six fields then in use. Rounds 6–9 added
requirements on `answers_are_partial` (every governing run) and on mission
identity and lifecycle status (to construct and re-observe the cohort) without
extending the list. The record could therefore declare itself valid while its
own measurement had become unexecutable. Now enumerates all nine.

**This is the fix-one-surface pattern again, and this time it accumulated
across four rounds rather than one.** Each round added a dependency; none
updated the field that tracks dependencies.

## Standing limit

These corrections came from an automated reviewer, not from a second
derivation. They are code-review findings against reasoning artifacts, which is
weaker than an independent re-derivation and stronger than nothing. Both
records remain single-model-family work with no cross-family independence, and
neither discharges any externally-enforced safety gate.
