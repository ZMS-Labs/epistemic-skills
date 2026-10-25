# Disposition memo — the perspective `adjustment` pin (E3)

**Filed into the evidence-program record 2026-10-25** (Phase 2 design
stream memo of the same date, filed with the successor stack so the
disposition travels with the stack it concerns). **Decision owner:
Zach** (decision ledger D10) — **status: PENDING.** This filing makes
no change to the fixture, the battery, or the E3 record: the memo's
recommended disposition (Option 1) is stated below, and a follow-on
commit executes it only if Zach approves. All readings below are
conformance to a battery-defined contract, never evidence about the
perspective skill as written (the program's binding frame for E2/E3,
unchanged by anything in this memo).

## The pin

Fixture `metric-fitness-lens-fires` (perspective trigger-and-scope battery)
pins `expected_finding: adjustment`. Its scenario, in full substance: a team
is about to judge a search-quality change by its click-through dashboard;
whether that metric measures search quality has never been examined; the
agent examines the metric's fitness through a single lens before the change
is judged. **The scenario states no outcome of that examination and no
evidence about the metric's fitness** — nothing from which `adjustment`
(rather than `remaining-uncertainty` or `insight`) follows.

E3's epoch result reduces to this pin exactly: the scorer report's only
failure line is *"metric-fitness-lens-fires: expected finding adjustment,
got remaining-uncertainty"* — 12/13, with this as the sole miss.

## Why the pin is defective under the battery's own rule

The battery README states its pinning principle explicitly: of the seven
`apply-lens` fixtures, four are shape-only because their scenarios "state no
evidence from which the finding's content could follow: the finding is the
lens's output on facts the scenario does not contain, so pinning one would
score a guess, not a determination." The three pinned fixtures were kept
because their scenarios *do* determine the finding:

- `evidence-unavailable-limit-fires` → `remaining-uncertainty`: the scenario
  states the lens's evidence does not exist in the environment — the finding
  follows.
- `no-material-finding-fires` → `no-material-finding`: the scenario states
  the inspection result ("nothing in them exceeds those limits") — the
  finding follows.

`metric-fitness-lens-fires` satisfies neither pattern: it is a fire whose
scenario, by the battery's own taxonomy, belongs with the four shape-only
fixtures, yet it carries a content pin. The E3 subject's
`remaining-uncertainty` is a defensible reading of the scenario as written;
the pin scores a guess and calls the guess wrong.

## Options

1. **Re-pin with a determining scenario.** Rewrite the scenario so the
   examination's evidence is stated and `adjustment` follows (e.g. the
   scenario states what the lens found: the dashboard counts clicks the
   change itself mechanically inflates). *Cost:* the fixture changes, so the
   E3 comparable line re-baselines at this row; the battery gains a genuinely
   determining metric-fitness case, which is the seam WO-3 wants to test
   (a lens whose evidence supports a concrete change returns `adjustment`).
2. **Retire the pin (make the fixture shape-only).** Smallest change; the
   battery returns to internal consistency with its own principle, and E3's
   line is reported as 12/13-as-run with the pin defect recorded — under this
   option nothing about the row is re-scored or restated as a pass.
   *Cost:* the battery loses its only metric-fitness finding case; the
   WO-3 seam then has no fixture that tests it as a determination.
3. **Carry as known-defective.** Keep the pin, annotate the fixture and the
   E3 record. *Cost:* every future epoch on this battery inherits a row
   known to score a guess; scorers and subjects keep paying for a defect
   already adjudicated. This is the option the record currently sits in by
   default, and it is the worst of the three.

## Recommendation

**Option 1 — re-pin with a determining scenario**, executed as a battery
revision in the same round as WO-3's work (after the P1 decision), with the
E3 record annotated to name the pin defect (the 12/13 stands as run; the
revised row starts a new line, never a restated pass). It is the only option
that both repairs the battery's internal consistency and preserves a
determining test of the exact verdict boundary E3 exists to measure.
