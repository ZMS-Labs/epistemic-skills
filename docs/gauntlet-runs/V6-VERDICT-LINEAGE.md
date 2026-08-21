# v6 verdict lineage — the record of what was reviewed and what was ruled

Nine independent reviews were run against the v6 candidate lineage. Until this
file landed, every one of them lived only on a mutable branch, while
`docs/release/RELEASE-6.0.0.md` told readers the run records were here. That
gap is publication-gate finding **PG-03**: publishing would have made a false
statement immutable at a tag.

Each row's verdict is bound to an **exact commit**. A verdict never transfers to
a different SHA — that rule is why this lineage has eight NO-GOs rather than one.

| # | Run | Subject commit | Verdict | Seat family |
|---|---|---|---|---|
| 1 | `es-v6-candidate-freeze-2026-08-18` | `00e5146e43ff` | **NO-GO** | same-family |
| 2 | `es-v6-rc2-gauntlet-kimi-2026-08-18` | `6db8c50420b1` | **NO-GO** | **cross-family** (kimi) |
| 3 | `es-v6-rc3-delta-review-2026-08-18` | `16b80ac6ada2` | **NO-GO** | same-family |
| 4 | `es-v6-rc4-delta-review-2026-08-19` | `7408a462b413` | **NO-GO** | same-family |
| 5 | `es-v6-rc5-narrow-review-2026-08-19` | `03e972c5d427` | **GO** (BUILD freeze only) | same-family |
| 6 | `es-v6-publication-grok-2026-08-19` | `186b16eb2c06` | **NO-GO** | **cross-family** (xAI/Grok) |
| 7 | `es-v6-publication-gate-2026-08-19` | `186b16eb2c06` | **NO-GO** | same-family |
| 8 | `es-v6-publication-openai-2026-08-20` | `d0165bd0cf1e` | **NO-GO** | **cross-family** (OpenAI) |
| 9 | `es-v6-publication-panel-2026-08-21` | `48009fef938b` | **NO-GO** | same-family |

Rows 1–5 reviewed the **BUILD freeze**. Rows 6–9 reviewed the **publication
act**, each against a different candidate, and reached the same conclusion
independently — none adopted another's reasoning.

## Who dispatched each review, and why that column matters

Independence has two limbs, and this lineage learned the second one late. A seat
can be fresh, non-authoring, and cross-family, and still tell you nothing if the
actor being judged chose whether to seat it and whether its output ever
surfaced. **Dispatch controls selection.** Row 9's judge made that argument
against its own dispatcher, and it is recorded here rather than argued with.

| # | Dispatched by | What that means for the verdict |
|---|---|---|
| 1–7, 9 | implementing lineage | Blocking findings are credible — each cost the dispatcher work. A `GO` from any of these establishes little. |
| **8** | **operator** | The only review in the lineage whose *selection* the implementer did not control. |

Row 8 is therefore the load-bearing publication review. It found that the
authorization sequence in `RELEASING.md` was not executable, that a candidate's
sign-off trailers were false attestations, and that two gating workflows had
never run on the exact subject. All three were repaired.

Row 5's `GO` was **ratified** by the operator (D20) rather than dispatched by
them. Row 9 ruled that inadequate on the selection argument above. That dispute
is unresolved and is disclosed in `docs/release/RELEASE-6.0.0.md` rather than
settled in this release's favour.

## What row 5's GO does and does not authorize

It authorizes recording the BUILD-freeze state at `03e972c5` and nothing else.
It is not a publication approval, and it left two obligations open that only the
operator can discharge: the standing D8 cross-family consult, and operator
acceptance under `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`. Rows 6 and 7 both
ruled those blocking.

## Independence limits, stated plainly

Six of the nine seats shared a model family with the candidate's authors. Those
panels recorded that as an independence **limit**, not as independence. Only rows
2, 6 and 8 were cross-family, and only row 8 was also operator-dispatched. This
is the limit the lineage has never retired, and it is the reason D8 exists — a
standing cross-family consult obligation that is **still owed** and carries
forward to 6.1.0.

## Redactions applied when these records were brought in-tree

The records are otherwise verbatim. Two classes of change were made, both
mechanical and both disclosed:

1. **Private fleet repository name** — three occurrences in run 1
   (`arbitration.md` ×1, `evidence/dossier-challenge-2026-08-18.json` ×2),
   replaced with `<private-fleet-repo>`. See that run's `REDACTIONS.md`. The
   irony is worth stating: run 1's own finding was that this string had been
   *allowlisted rather than remediated*, and restating the finding reproduced
   the string. Quoting a detector's trigger re-arms it.
2. **Build-host absolute paths** — 17 files carried the build container's
   scratch directory (including a session id) or its checkout path, replaced
   with `<build-scratch>` and `<repo>`. This is publication-gate finding
   **PG-24**: no credential or personal data, but a class the public-content
   pattern set could not see. The generator that emitted them
   (`v6_collect_candidate_evidence.py`) now records commands in portable form.

No verdict, severity, ruling, finding, or evidence conclusion was altered.

## Verifying against the originals

Every record's unredacted bytes remain immutable on the branch it was recorded
on. To audit any row:

```bash
git diff origin/<branch> -- docs/gauntlet-runs/<run-id>/
```

Originating branches: run 1 `claude/epistemic-skills-v6-completion-nwptmc`,
run 2 `kimi/es-v6-rc2-gauntlet-2026-08-18`, run 3 `claude/es-v6-rc3-delta-review`,
run 4 `claude/es-v6-rc4-delta-review`, run 5 `claude/es-v6-rc5-review`,
run 6 `cursor/es-v6-publication-gauntlet-63a8`,
run 8 `review/v6.0.0-publication-gate-openai-2026-08-20` (recorded there at
`ac0a91e` by the operator-dispatched seat, brought in-tree unaltered).

Runs 7 and 9 are first recorded here; for both, only the arbitration was
retained, not the individual seat reports. Run 9 states that gap and its own
structural limit in its `TRANSCRIPTION.md`.
