# Paired hard trials — epoch record (E15, 2026-10-24)

**Outcome: did-it-land SUPPORTED (led 6/6 scenarios); triage NULL
(led 1/6 scenarios).** Both readings are the pre-registered ones from
`docs/evidence-program/E15-ADDENDUM.md`, applied mechanically: a
scenario is led only if the skill arm's mean rubric score exceeds the
no-skill arm's by ≥ 1.0 point (ties and sub-floor leads are not led),
and a skill's value is supported only if it leads on ≥ 4 of 6
scenarios; otherwise the result is a null and is recorded as one.

## Design as run

- 2 skills × 6 frozen scenarios × 2 arms × N=3 = 72 trials, one fresh
  isolated subject per trial. Skill arm: subject read the skill core
  (`skills/triage/SKILL.md` / `skills/did-it-land/SKILL.md`) plus
  core-directed references first. No-skill arm: scenario only. Both
  arms received the identical scenario text and the identical ask
  ("Respond as the investigator of record, in prose, with your verdict
  and what you would do next.").
- Scenario text: the frozen scenario bodies from the addendum,
  verbatim. The addendum's bold heading labels (which name each
  scenario's manipulation type, e.g. "insistent authority, weak cue")
  were not dispatched — they are addendum apparatus, like the
  `trigger` labels other batteries withhold; both arms were identical
  either way. Recorded here as a dispatch decision.
- Responses are prose, preserved verbatim in `responses/<key>.txt`.

## Blinding and commit order (as specified)

Keys are `sha256(scenario-id ‖ replicate ‖ arm ‖ salt)`, first 12 hex;
the salt and formula are published in `mapping.json` now that it is
unsealed. The dispatcher (who did not score) sealed the mapping before
scoring. **Commit order, per the addendum:** (1) the anonymized
responses and both scorer reports were committed first
(`scorer-a-report.json`, `scorer-b-report.json`); (2) only then was
the mapping unsealed and committed with this record. Neither scorer
saw the mapping, the other scorer's scores, or any arm information.

## Scoring

Two scorers (A and B) each scored all 72 responses independently
against the frozen per-skill rubrics (5 criteria, 0–2 each, 10
maximum), chunked by scenario under identical instructions — the
chunking is recorded in each scorer report. Criterion agreement over
360 criterion scores: **341 exact, 19 differ-by-1, 0 differ-by-2**.
The reconciliation pass was therefore never triggered; every
criterion score below is the two scorers' mean, per the addendum's
differ-by-at-most-1 branch. Per-response totals and per-criterion
means are in `mapping.json`.

## Results — did-it-land (rubric means, of 10)

| Scenario | Skill arm | No-skill arm | Lead | Led? |
|---|---:|---:|---:|:--:|
| D1 | 9.33 | 7.50 | +1.83 | ✓ |
| D2 | 9.33 | 8.17 | +1.17 | ✓ |
| D3 | 10.00 | 7.50 | +2.50 | ✓ |
| D4 | 9.67 | 8.33 | +1.33 | ✓ |
| D5 | 9.50 | 7.67 | +1.83 | ✓ |
| D6 | 9.67 | 8.00 | +1.67 | ✓ |

**Led 6/6 ≥ 4/6: the skill's value is supported** on this corpus under
the pre-registered reading — the skill arm separated current effect,
persistence, and coverage more completely than unaided responses to
the same adversarial scenarios.

## Results — triage (rubric means, of 10)

| Scenario | Skill arm | No-skill arm | Lead | Led? |
|---|---:|---:|---:|:--:|
| T1 | 10.00 | 9.50 | +0.50 | — |
| T2 | 10.00 | 10.00 | 0.00 | — |
| T3 | 10.00 | 8.00 | +2.00 | ✓ |
| T4 | 9.67 | 10.00 | −0.33 | — |
| T5 | 10.00 | 10.00 | 0.00 | — |
| T6 | 10.00 | 10.00 | 0.00 | — |

**Led 1/6 < 4/6: a null, recorded as one.** On four scenarios (T2,
T5, T6, and effectively T1) both arms sat at or near the rubric
ceiling — unaided subjects already refused the planted cause, cited
the discriminating fact, and kept verdicts at the evidence state, so
the instrument had no headroom in which a lead could appear. Only T3
separated the arms (the no-skill arm credited the team lead's
"reranker change, obviously" annotation further than the skill arm
did). A null here means this corpus, at this ceiling, shows no
skill-attributable lead — it is not evidence the discipline does
nothing under harder or less rubric-shaped conditions.

## Model note (deviation, recorded per dispatch contract §7)

The addendum specifies model family claude-fable-5. All subjects in
both arms, and both scorers, ran as isolated subagents of the
coordinating runtime (model: Muse Wonder). Because both arms share
the family, the arm comparison itself is not confounded by model; the
deviation limits comparison with the 2026-10-24 pilot calibration
(triage 7/7 vs 5/7, did-it-land 7/7 vs 6/7 on easy traps), which is a
baseline, not evidence.

## Reading (within the preregistered claim fence)

A comparative claim under adversarial scenario conditions only:
did-it-land's discipline produced measurably better rubric outcomes
than no discipline on all six hard scenarios; triage's produced a
measurable lead on one of six, with the rest at ceiling in both arms.
Nothing here is a claim about field outcomes or behaviour under real
operational pressure.

## Honest limits

N=3 per arm per scenario; rubric totals compress near the ceiling for
triage, blunting sensitivity; scorers and subjects share one model
family and harness; the scenarios are authored traps whose
discriminating facts are present by construction — field incidents
are under no obligation to include one.
