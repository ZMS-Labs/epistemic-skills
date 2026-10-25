# perspective trigger-and-scope fixtures

This battery tests the trigger discipline and the scope boundary of
Perspective: a focused concern, assumption, or tradeoff that would benefit
from a different evidence-based lens — or an explicit request for one —
fires a lens application on a bounded question; several lenses may be
applied to one bounded question without that becoming adjudication; a
reversibility-only question fires a single narrow lens. It never fires
when the evidence already settles the question, for routine work, for an
interesting adjacent issue that is not the live assignment, or when what
is actually requested is plural examination plus adjudication of a common
subject (that is Gauntlet) or an approval verdict (Perspective is not a
verdict). Over-firing and under-firing are defects, not extra rigor.

## Claim

A live-epoch pass on this battery would support one claim only: that the
subject's *declared* fire/no-fire decisions and lens-application shape
conform to the skill's trigger and scope text on these fixtures —
trigger/scope conformance of declared decisions. It would NOT support any
claim that applying a lens improved an outcome, that a finding was
correct, or that the skill helps in live work; outcome improvement is a
different claim needing different evidence. The synthetic example traces
under `examples/` are scorer-discrimination evidence only.

Note on the contract's provenance: the perspective `SKILL.md` defines no
verdict or reporting vocabulary — it returns its result in prose to the
work it informs. The response contract pinned below is therefore a
*minimal observable contract defined by this battery*, not a quotation of
skill text. Adopting this vocabulary into the skill text is a separate
proposed change; it is NOT made here, and no `SKILL.md` was edited for
this battery. Results from this battery must always be reported as
conformance to that battery-defined contract — never as evidence about
the skill as written.

**Amendment (2026-10-25).** The separate proposed change described
above has since been made — by the skill's own change process, not
by this battery: per Zach's P1 decision (2026-10-25), the contract
below was adopted into perspective's `SKILL.md` as its output section
(§"Output: the declared finding"), including the boundary rule the
E3 epoch's failed seam taught. The note above stands as the record
of the position before adoption and is not rewritten. What the
amendment changes is the frame for reading results: epochs run
**before** the adoption (including E3) measured conformance to this
battery-defined contract only, and results from those epochs must
still be reported that way — never as evidence about the skill as
written; epochs run **after** it measure the skill as written,
because the contract is now the skill's own text. One cost is
recorded plainly: the adoption burns this battery's three marked
holdout fixtures — `several-lenses-bounded-no-adjudication`,
`gauntlet-adjudication-no-fire`, and
`evidence-unavailable-limit-fires` — whose scenarios are now
answered by skill text their subjects may read; replacement holdouts
must be authored by a non-editor and stay sealed until their epoch
runs (the sealed-holdout rule adopted 2026-10-25). The adoption
packet is `wo3-adoption-packet.md` in the evidence program's
Phase 2 files.

## Pinned expectations

Three of the seven `apply-lens` fixtures pin `expected_finding`, and the
scorer enforces it. The other four fires are shape-only by design:
`focused-cache-assumption-fires`, `explicit-different-lens-tradeoff-fires`,
`several-lenses-bounded-no-adjudication`, and
`reversibility-single-lens-fires`. Their scenarios determine that a lens
fires, the bounded question it answers, and how many lenses apply — but
they state no evidence from which the finding's content could follow: the
finding is the lens's output on facts the scenario does not contain, so
pinning one would score a guess, not a determination. For those four, the
scorer checks shape only (lens named, question bounded, count within the
fixture's bounds, finding in vocabulary, no adjudication).

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch (per
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: the pinned contract travels
verbatim with vocabularies inline, and silence semantics are explicit):

- `action` names the **discipline mode that fired**: `apply-lens` (a lens
  was applied to a bounded question) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` only —
  no `lens`, no `question`, no `lenses_applied`, no `finding`, no other
  field at all. Absence is not an artifact; a process field present on a
  silent response is scored as over-firing, not generosity.
- An `apply-lens` response reports:
  - `lens` — a nonempty string naming the lens or method applied;
  - `question` — a nonempty string stating the bounded question the lens
    was applied to;
  - `lenses_applied` — an integer `>= 1` counting the lenses actually
    applied;
  - `finding` — exactly one of `insight`, `adjustment`,
    `supported-finding`, `no-material-finding`, `remaining-uncertainty`.
- A perspective row **never carries adjudication**: a row with
  `"adjudication": true`, or with a `verdict` field present under any
  value, fails — lens count is not adjudication, and Perspective issues
  no verdicts.
- Where a fixture carries `expected_finding`, the row's `finding` must
  equal it. Where a fixture carries `min_lenses`, the row's
  `lenses_applied` must be at least it; where it carries `max_lenses`,
  at most it.

## Status

Unrun as of 2026-10-24: no live epoch has been run against these
fixtures. Three fixtures are marked `"holdout": true` in `fixtures.json`
(`several-lenses-bounded-no-adjudication`, `gauntlet-adjudication-no-fire`,
`evidence-unavailable-limit-fires`); epoch runners must not tune against
the holdout fixtures.
