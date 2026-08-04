# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: FAIL — 10/13 fixtures pass the deterministic scorer; 3 named
failures — and the epoch found a real scorer defect.** Supersedes
`results/BLOCKED.md`.

## Methodology

Protocol as the sibling 2026-08-04 epochs: thirteen fully isolated
general-purpose subagents (claude-fable-5, Claude Code harness, N=1),
subject-blinded, simulation-declared (no file writes/git commands),
subjects read exactly SKILL.md (evals/ forbidden), scored by `score.py`.

**Preregistration (two-part, recorded before scoring):** (1) the shipped
scorer crashes with a TypeError on the dropped-intent response's honest
`"mechanical": false` — CONFIRMED verbatim (`set()` over a bool, the same
defect class the Codex review found in `verify_calibration.py`); the
scorer was then given a minimal fail-closed fix (named shape-violation
failure, semantics unchanged, battery tests green) and the epoch scored
under it. (2) Amended prediction of 11/13 — PARTIALLY CONFIRMED: both
predicted failures occurred, plus one unpredicted failure of the
already-established decorated-value class.

## Results

trace-and-resolve 3 · escalate-decision 2 · review-provenance 1 ·
abort-restart 1 · mechanical-resolve 2 · regenerate 3 · no-fire 1.

- **PASS (10):** semantic-overlap traced with both origins/checks and a
  recorded ruling; the mixed merge's two trivial hunks resolved
  mechanically with only the semantic hunk traced; the workaround drop
  ruled side-a-dropped with reason + ledger ref and both origin checks;
  the pagination collision escalated with both intents named and no
  silent resolution; the undocumented merge review demanded rulings; the
  uncertain tree aborted with traces kept and a restart; all three
  regenerable conflicts (including the 400-line semantic-looking
  lockfile) regenerated untraced; the disjoint-import and formatting
  conflicts resolved mechanically untraced; the fully documented merge
  review stayed silent.
- **FAIL (3):**
  1. `ambiguous-textual-trace` — the subject escalated the symmetric
     rename collision (style ADR-3 vs API-sweep PR #88) as a genuine
     naming decision instead of trace-and-resolving. This is a
     **judgment-boundary divergence, not vocabulary**: the skill's step 3
     says a genuine collision "is a decision, not a merge," and with two
     sanctioned origins the subject's reading is defensible. The fixture
     sits exactly on that boundary — a battery-design question for issue
     #77: either the scenario should make one side's subordination
     legible, or `escalate-decision` should be an accepted action here.
  2. `mixed-hunks-classify` — ruling value decorated
     ("both-preserved — <rationale>") where the enum requires the bare
     value; the decorated-value class already seen in wayfinding.
  3. `dropped-intent-recorded` — `"mechanical": false` instead of an
     array; scored as the named shape violation under the fixed scorer.

## Diagnosis

Failures 2 and 3 extend the cross-battery reporting-layer pattern (now
12 of 13 total failures across four failing epochs). Failure 1 is the
suite's first observed **substantive divergence** — a contested
compose-vs-escalate boundary worth a doctrine clarification or fixture
redesign rather than a contract sentence. The scorer crash (found and
fixed) is the epoch program's first direct repair to eval
infrastructure: live epochs also test the scorers.

## Honest limits

Smoke-scale, N=1 per fixture, one model/harness, same family throughout;
subject-level blinding; dispatch glosses are part of the intervention
surface. The scorer fix landed mid-epoch (before scoring completed
once); the raw crash and the fixed-scorer report are both preserved.
