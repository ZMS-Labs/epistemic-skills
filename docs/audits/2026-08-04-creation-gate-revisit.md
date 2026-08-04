# Creation-gate revisit — calibration-review and outcome-review (2026-08-04)

**Provenance:** v3.5.0 improvement wave (PR #78), Track C2/C3, operator-authorized
fork "both new-discipline candidates through the formal creation gate." Applies
the six creation gates of `docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md:285-296`
as bound by the 2026-07-22 gap analysis
(`docs/audits/2026-07-22-collection-audit/06-gap-analysis.md`). Evidence read:
the epistemic-events contract at its current 17-producer state
(`plugins/epistemic-skills/contracts/epistemic-events/epistemic-event.schema.json` —
forecast records carrying `outcome_class`, `probability`, `resolution_rule`;
outcome records; supersession), decision-ledger SKILL.md (trigger, no-op gate,
outcome-review section, composition), the router's trigger table, and the helix
pairing map.

Both candidates were evaluated to a verdict. **Neither mints a new skill in
this wave.** One is deferred behind a mechanical data threshold; the other is
promoted to a first-class trigger inside its existing owner. Per the gate
protocol, gauntlet review fires at design approval; a DEFER and an
in-place-promotion never reach a new-skill design, so no gauntlet run is owed
by this document.

---

## C2 — calibration-review

**The 2026-07-22 verdict being revisited:** candidate (c) — REJECT as a skill;
fold interpretation guidance in as machinery; "revisit only if calibration data
becomes rich enough that *interpretation* — not lookup — needs judgment."

**What changed since:** the epistemic-events contract now defines forecast
records for all 17 skills — `probability` (0–1), `outcome_class`, and a closed
`resolution_rule` vocabulary (`deterministic-fixture` |
`independent-adjudication` | `field-observation` | `supersession-chain`) — with
outcome records and supersession chains (B1, `2e6284d`). Interpreting a corpus
of such records is genuinely judgment-shaped: calibration curves vs base rates,
heterogeneous resolution rules that must not be pooled naively, sample-size
honesty, supersession-aware counting, and the public/private split. The
*schema-richness* half of the revisit condition is met.

**What did not change:** the *corpus* half. The ECS collection layer is
fire-and-forget and operator-private; this repository contains example records
and sentinel fixtures, not accumulated resolved forecasts. In-repo resolved
forecast→outcome pairs: approximately zero. Gate 1 (recurs in real runs) and
gate 5 (measured benefit over unskilled baseline) therefore cannot be
evidenced today — there is no track record whose interpretation recurs, and no
baseline mis-interpretation to beat.

**Verdict: DEFER, behind a mechanical mint threshold.** Design investment in a
calibration-review discipline is authorized **when** an operator-visible store
holds **≥ 25 resolved forecast→outcome pairs spanning ≥ 3 producer skills and
≥ 2 resolution rules**. Below that, interpretation reduces to a lookup with
error bars too wide to need a method, and the 2026-07-22 fold-in remains the
right home (gauntlet Step 7/9 discipline, UAT `calibration_status`,
`lens_stats.py`). The threshold is deliberately checkable in one query so a
future session can re-run this gate without re-arguing it. This is a reasoned
refusal to mint now, not a rejection of the moment: the schema investment
(B1) is exactly what makes the threshold reachable.

---

## C3 — outcome-review

**The wave-plan ask:** promote decision-ledger's "Outcome reviews — the
anti-hindsight boundary" (`decision-ledger/SKILL.md:196-211`) to a first-class
trigger + composition-contract moment + helix row, **or** record the reasoned
refusal.

**Gate analysis for a separate skill:** the moment is genuinely distinct *in
time* — an outcome becomes observable at a different point (usually a
different session) than the decision was formed, and the anti-hindsight rule
(original prediction and observed result as separate untouched facts; lessons
gated behind operator approval) is real discipline, not ceremony. But the
moment fails **gate 2 (not already owned)**: decision-ledger owns it
explicitly, in normative language, including the two-stage lesson rule and the
throwaway-prototyping capture path. Its deliverable — an outcome-shaped
append to the same ledger under the same store discipline — is the same
artifact family as decision-ledger's; a separate skill would split one
append-only store's write discipline across two SKILL.md files and force every
consumer to learn which half owns which append. The 2026-07-22 analysis's own
trust-contract reasoning applies: a moment whose deliverable lives entirely
inside another skill's artifact and store contract is a *trigger* of that
skill, not a sibling.

**Verdict: PROMOTE IN PLACE, refuse the separate skill.** Outcome arrival
becomes a named first-class trigger of decision-ledger rather than prose in a
late section, wired into the three routing surfaces (same commit as this
document):

1. **decision-ledger SKILL.md** — the trigger section names outcome arrival as
   a second observable trigger with its own fire condition and the
   anti-hindsight section as its method.
2. **Router trigger table + decision table** — the decision-ledger row fires
   on both moments (decision formed / outcome observed), so routing does not
   depend on remembering a subsection.
3. **Helix map** — the decision-ledger row's trigger phrasing covers outcome
   arrival, so paired workflows fire it at completion/verification stages.

The ECS surface needs no change: `ledger-revisit` is already decision-ledger's
event kind and is the natural carrier for outcome-review episodes.

---

## Verdict summary

| Candidate | Gate that decides | Verdict | Re-entry condition |
|---|---|---|---|
| calibration-review | 1 + 5 (no corpus; no measurable recurrence/benefit) | **DEFER — mechanical mint threshold** | ≥ 25 resolved forecast→outcome pairs, ≥ 3 producers, ≥ 2 resolution rules, operator-visible |
| outcome-review | 2 (owned by decision-ledger; same artifact + store) | **PROMOTE IN PLACE — first-class trigger, no new skill** | none needed — landed with this document |
