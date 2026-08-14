# es#166 gate parameters — derivation records (2026-08-14)

Two `formal-rigor-record@2` records, standard tier, both structurally validated
with `.claude/skills/resolve/derivation/validate_record.py`. Subject revision
pinned to `0fee7a0f59bdc5aac9ab6b4b2ee581d8e6c8b232` (merged main).

They exist because the [es#150 gauntlet
adjudication](https://github.com/ZMS-Labs/epistemic-skills/issues/150#issuecomment-5285714717)
gated `grants_paths` on "a repaired #166 window" and required that window to
have a named owner, a checkable predicate and a calendar deadline **before it
governs anything** — and separately required the grant-authorship model to be
"decided on the record before `grants_paths` ships". These records are that
record; the
[es#150 comment](https://github.com/ZMS-Labs/epistemic-skills/issues/150#issuecomment-5288169782)
and
[es#166 comment](https://github.com/ZMS-Labs/epistemic-skills/issues/166#issuecomment-5288171588)
cite them.

> **STATUS: DO NOT RUN THIS PROCEDURE AS THE es#166 WINDOW.** Round 13 found
> that the close judgement is undefined — `p_low` and `p_high` are specified,
> but no threshold turns either into a verdict, so *"close inconclusive if the
> judgement would differ"* cannot be applied reproducibly. Two further open
> defects are recorded beside it (a retry cannot recover a store that vanished
> before it; mission identity is not incarnation identity, so a recreated
> mission id merges two members into one). All three are upheld and
> **deliberately not patched** — they are inputs to the re-derivation below,
> because twelve rounds of in-place patching is what produced the drift that
> re-derivation exists to repair.
>
> **This record's coverage analysis also does not cover the procedure it
> now governs.** Round 12 established that P3 (ordering/history) and P5
> (durability/recovery) were recorded not-applicable on a justification that
> was true of the 2026-08-14 procedure and false of the one six rounds of
> review produced. Both are now **unmapped with the analysis owed**. What a
> lost, reordered or non-durable observation does to the cohort
> reconstruction is analyzed **nowhere**. A standard-tier re-derivation of the
> FINAL procedure is required before the window governs anything — it is a
> separate authorization and is **not** discharged by the corrections here.
>
> **Rounds 2–15 of PR #175 found thirty-two defects in these records,
> all upheld.** The files here are corrected; see
> [`CORRECTIONS.md`](CORRECTIONS.md) for what was wrong and why it matters.
> Several were defects the records were written to guard against — a vacuous
> preregistration, a declaration naming no principal, selection on survival in
> a record whose P8 coverage exists to catch selection. **Seven rounds** found
> a correction applied to one field and not its sibling — round 15 finding it
> between two whole surfaces, with the *authoritative* one carrying the
> obsolete text — and the cohort rule alone needed correcting in SIX
> consecutive rounds, each fix sound about the case in front of it and
> silently assuming the next one away. Read that trend as what it is: these
> records have needed a correction every single round they have been reviewed,
> and no round has yet come back clean.

| file | question | outcome |
|---|---|---|
| `predicate.json` | Which census-computable predicate defines a "substantive mission" so that adoption is measurable and not controlled by the measured party? | `conditional` — option A (≥1 chain-bound receipt **and** a root from the recorded admitted-root set), pending one non-emptiness observation |
| `grant-authorship.json` | Operator-confirmed or steward-authored grants? | `reversal` on steward-authored; **no option selected**; empirical closure **blocked** |

## What they establish

**Envelope-referencing predicates are refuted** (`d1`, predicate record):
defining membership by `guard_mode` or non-empty `scope` selects on the
dependent variable, pinning the adoption ratio at 1 regardless of estate state.

**No census-computable predicate is non-gameable** (`d2`): every candidate input
— receipts, checkpoints, root — is steward-produced. The achievable property is
*detectable* gaming, which only the root condition supplies, because es#173
already named the scratch-workspace detachment as an observed evasion and the
census prints every mission's root.

**Steward-authored grants cannot be a control** (`d1`, authorship record): the
granted party would author the bound that constrains it, which reduces
`grants_paths` to a DECLARATION in the README's own taxonomy — precisely what it
is proposed to be more than.

**That refutation does not select operator-confirmed** (`d2`): es#166's measured
finding is that envelope fields are abandoned where using them is inconvenient,
and per-grant confirmation is higher friction than an empty field. Recorded
`incomplete` — and **not** resolvable by the es#166 window, which cannot
observe a mechanism that does not exist (see `CORRECTIONS.md`). A third
alternative — operator confirms a *class* of grants once — was surfaced by the
derivation and is not yet evaluated.

## Open obligations these records carry

0. **Record the admitted-root set** before observation begins. Option A is
   only reproducible against an explicit list of repository checkouts fixed in
   advance; without it the predicate is not census-computable. The
   **numerator** is now fixed in the record too (`scope_in` non-empty OR
   `scope_out` non-empty OR `guard_count > 0`) and must not be renegotiated
   once observation starts — a reproducible denominator with a reader-chosen
   numerator is not a reproducible ratio.
1. **Non-emptiness check before the window opens.** `predicate.json`'s
   `empirical_closure` is `pending` with a preregistered prediction. If the
   predicate selects ∅ on the live estate, the recorded recovery move is *not* a
   looser predicate — it is a finding that the estate has no substantive
   missions to measure, which is itself an answer to es#166 direction 1.
   The check counts **terminal missions as well as active ones**, and the
   census run must report `answers_are_partial == false` — a partial run is a
   refusal to answer, not a result (round 6). **Every** run the measurement
   relies on carries that requirement, cadence observations included: a
   partial cadence run does not advance the schedule (round 12).
1b. **Record the opening cohort** when the window opens — per member: mission
   id, root, lifecycle state, **`scope_in`/`scope_out` non-emptiness, and
   `guard_count`**. Identity alone is not enough: a member that disappears
   takes its adoption state with it, and the full-cohort ratio can no longer
   be reconstructed (round 7). An empty denominator at close against a
   non-empty opening cohort is **not** evidence of non-adoption, and neither
   is a shrunken one — when any member is missing, report the full-cohort
   ratio and the survivor-only ratio and state the gap.
1c. **Re-observe the cohort on a recorded cadence**, persisting each
   observation. A member that adopts *after* opening and then disappears is
   invisible to both the opening record and the closing census, so without
   intermediate observations the full-cohort numerator is unknowable in
   exactly the case the cohort record exists to cover (round 8). The cadence
   is fixed before observation begins, like everything else here. Each
   observation also **admits newly qualifying missions** — a mission created
   during the interval, or one gaining its first chain-bound receipt, joins
   the cohort at the observation that first sees it qualify; re-observing only
   the opening members biases the ratio toward the opening population (round
   9). Each admitting observation also persists the **qualifying evidence**
   (`receipt_count`, and the root as matched against the admitted-root set),
   or the cohort cannot be reproduced once a store vanishes.
1d. **Report bounds, not a point value, whenever a member has disappeared.**
   A member last seen without a populated envelope and gone before the next
   observation has an **unknown** numerator state; folding it in as
   non-adoption reports a lower bound as if it were the ratio. Report
   `p_low`, `p_high` and the survivor-only ratio with the unresolved count,
   and close **inconclusive** on any question where `p_low` and `p_high`
   would give different answers (round 11).
2. **A bounded pilot, if the authorship question must close.** The es#166
   window cannot settle it: with `grants_paths` unshipped, no observation can
   discriminate the alternatives, so re-firing against window data would repeat
   the vacuity `CORRECTIONS.md` records. The standing-grant variant should be
   enumerated as a third alternative before any pilot is designed.

## Validity and limits

Both records carry the mandatory `never_attests` boundaries: the envelope
attests structure, provenance and validity window only — never derivation
correctness, never an unobserved empirical fact, never gauntlet independence.
Both were produced by the same model family that produced the es#150
adjudication itself, so there is **no cross-family independence** on this
question. Neither record discharges any externally-enforced safety gate.

`valid_while` voids each record on a change to the pinned subject revision, and
`predicate.json` additionally voids only if the census **stops reporting** one
of the fields the measurement actually reads — `root`, `active`, `status`,
`mission_id`, `receipt_count`, `scope_in`, `scope_out`, `guard_count`, and
`answers_are_partial`. The earlier list named six and omitted three the
procedure depends on, so the record could have declared itself valid while its
own measurement had become unexecutable (round 11). A census that gains an
unrelated field does **not** void it; the earlier, broader wording
("computable field set changes") was self-refuting, since the commit
publishing these records added one (round 4).

It deliberately does **not** void when a mission arms either: arming is a
positive adoption event this window exists to measure, and a rule that expires
on its own first interesting datapoint governs nothing (round 3). Both are in
[`CORRECTIONS.md`](CORRECTIONS.md).
