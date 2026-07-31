# epistemic-skills 3.4.0

**Release record date:** 2026-07-31
**Intended channel:** stable
**Release type:** minor — three new disciplines, five amendment sets, router/helix
ripple, backward compatible
**Validity contract:** this record is authoritative only when the exact-commit
gates pass and the annotated tag plus non-draft GitHub Release satisfy the
publication-identity checks in RELEASING.md.

## What's new

- **`wayfinding` (new discipline):** decompose large foggy efforts by
  *decisions*, not tasks — a dependency map whose nodes are decisions, a
  frontier rule (work only decisions whose prerequisites are resolved), and
  build tickets minted only from fog-free regions, each carrying the
  three-fact handoff (resolved dependencies, proving observation, the
  upstream decision whose reversal would invalidate it). Falsifiable gate:
  any open ticket walks upstream to fully-resolved ancestors.
- **`throwaway-prototyping` (new discipline):** resolve a live decision by
  building a disposable probe under a four-clause contract — one
  pre-registered question, disposal declared at birth, answer captured
  durably before deletion, never promote prototype code. The concrete form
  of the "bounded reversible probe" closure control.
- **`intent-traced-merge` (new discipline):** resolve non-trivial merge/rebase
  hunks by tracing both sides to their origin commits and the intent each
  served; preserve both intents or record the drop; verify against BOTH
  origins' motivating checks; record per-hunk rulings in the merge commit.
  Deliberate correction of community "never abort" absolutism: aborting is
  the return path, not a failure.
- **Amendment sets (five):** open-questions — frontier discipline for
  dependent docket items; gauntlet — revision-loop discipline (revised
  subject = new attack surface, delta-scoped re-review, hard cap of three
  panels per subject lineage); decision-ledger — outcome reviews with the
  anti-hindsight boundary (prediction and result recorded as separate
  untouched facts; generalized lessons need operator approval) + prototype
  finding capture; evidence-locked-uat — two new oracle-honesty rows
  (artifact existence is not render proof; unread console/error channels are
  unexercised oracles, relevant non-empty error sets are hard FAIL);
  agent-interface-design — domain-vocabulary naming clause (never mint a
  synonym for a concept the project already names). gauntlet-generator now
  names throwaway-prototyping as the execution discipline for
  prototype-instantiated options.
- **Ripple:** router handoff/routing tables + arc notes, helix pairing map
  (+3 rows), README (seventeen skills / fifteen disciplines), GEMINI.md, ten
  version manifests + root plugin.json → 3.4.0, outsource integration-test
  assertions (17 dirs).

## Provenance and evidence posture

Idea provenance, all re-derived and re-worded (no text copied):
ConnorGriffin/skills (MIT; wayfinder, grilling frontier, plan-review delta
cap, prototype patterns), the Matt Pocock agentic-coding community synthesis
(merge-conflict intent-tracing, prototype disposal, vocabulary clause), and
the fleet's own field practice. Each new skill names its provenance inline.

**Honest limits:** the three new disciplines have NO eval battery or
behavioral epoch (register: issue #70, scope extended to 3.4.0). The 3.2.0
evaluation posture is inherited, not extended. The gauntlet revision-loop cap
(three panels) is a design judgment, not a measured threshold — revisit on
the first field case it bites.

## Migration from 3.3.0

Update the install coordinate to `v3.4.0` and reload the harness. No existing
trigger, contract, schema, or output shape changed; amendments are additive
clauses inside existing sections.

## Harness verification tiers

Unchanged from 3.3.0: Claude Code primary (deterministic suite on the release
commit); Codex/Gemini/Kimi manifest-validated; Cursor packaged but not
publicly listed.
