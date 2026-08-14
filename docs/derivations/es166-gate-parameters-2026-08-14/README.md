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

| file | question | outcome |
|---|---|---|
| `predicate.json` | Which census-computable predicate defines a "substantive mission" so that adoption is measurable and not controlled by the measured party? | `conditional` — option A (≥1 chain-bound receipt **and** a non-scratch root), pending one non-emptiness observation |
| `grant-authorship.json` | Operator-confirmed or steward-authored grants? | `reversal` on steward-authored; **no option selected** |

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
`incomplete`, resolvable only by the window's own adoption evidence. A third
alternative — operator confirms a *class* of grants once — was surfaced by the
derivation and is not yet evaluated.

## Open obligations these records carry

1. **Non-emptiness check before the window opens.** `predicate.json`'s
   `empirical_closure` is `pending` with a preregistered prediction. If the
   predicate selects ∅ on the live estate, the recorded recovery move is *not* a
   looser predicate — it is a finding that the estate has no substantive
   missions to measure, which is itself an answer to es#166 direction 1.
2. **Re-fire the authorship derivation at window close** against observed
   adoption data, with the standing-grant variant enumerated as a third
   alternative.

## Validity and limits

Both records carry the mandatory `never_attests` boundaries: the envelope
attests structure, provenance and validity window only — never derivation
correctness, never an unobserved empirical fact, never gauntlet independence.
Both were produced by the same model family that produced the es#150
adjudication itself, so there is **no cross-family independence** on this
question. Neither record discharges any externally-enforced safety gate.

`valid_while` voids each record on a change to the pinned subject revision, and
`predicate.json` additionally voids if the census's computable field set changes
or the estate's armed count moves off zero.
