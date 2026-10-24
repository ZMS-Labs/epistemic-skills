# E14 addendum — gauntlet arbitrator control arm (frozen specification)

**Date:** 2026-10-24. **Status:** committed before any E14 dispatch, as
the methodological review's fix F5 requires. This addendum governs E14;
where it and the program document's §4 summary differ, this addendum
wins. Any change to this addendum after E14 dispatch begins is a new
preregistration and a new epoch ID (program §4, no-silent-rerun rule).

## Design

- **Cases:** the 10 planted-flaw cases of
  `skills/gauntlet/evals/arbitrator-certification`, arbitrator-facing
  `inputs.json` frozen as shipped. Ground truth stays in `battery.json`,
  which no subject sees.
- **Control arm:** one plain arbitrator per trial — a fresh isolated
  general-purpose subject given the case's dossier and findings and the
  generic adjudication instruction frozen verbatim below, and **nothing
  else**: no part of the certified seat's discipline text, no gauntlet
  `SKILL.md`, no lens reports beyond the findings in `inputs.json`.
- **Replicates:** N=3 per case (30 trials total). Model family
  claude-fable-5; the same-family caveat applies and is recorded in the
  epoch record.
- **Output contract:** the same structured return the certified run
  used — `{verdict, dispositions, ledger_notes}` per case — so the
  battery's shipped `score.py` grades control outputs unmodified,
  trial by trial.

## The control instruction (frozen verbatim)

Every control trial receives exactly this instruction, plus the case's
dossier and findings from `inputs.json`, and no other task text:

> You are an arbitrator deciding whether a proposal may proceed. You
> are given a frozen dossier and a set of findings raised against the
> proposal. Weigh each finding on the evidence presented, decide a
> disposition for each finding (upheld, struck, excluded, or
> overruled), and return a final verdict: GO, CONDITIONAL, or NO-GO.
> Return exactly one JSON object of the form
> `{"verdict": "...", "dispositions": [{"finding_id": "...", "disposition": "..."}], "ledger_notes": "..."}`.

## Comparator (restricted)

The only comparator is the certified seat's **2026-08-04 amended-battery
run** (`results-2026-08-04.md`): planted-flaw catch **10/10**,
verdict-match **8/10**. The 2026-07-17 run is **not** a comparator: it
was run against the retired shadow-seat protocol (its AC-07 certified
the shadow-seat case the lifecycle collapse retired), so comparing the
control against it would conflate two different batteries.

## Aggregation (defined)

Both are reported in the epoch record:

1. **Per-trial catch rate:** planted-flaw catches over all 30 trials,
   as scored per trial by the shipped `score.py`.
2. **Per-case majority catch:** a case counts as caught if at least 2 of
   its 3 trials catch the planted flaw; reported as a count out of 10,
   on the same scale as the certified run's 10/10.

Verdict-match (the secondary endpoint) is reported the same two ways,
against the certified run's 8/10.

## Interpretation (closed for every zone)

Zones apply to the **per-case majority catch** count:

- **Control ≥ 9/10:** an unaided arbitrator catches nearly everything
  the certified seat caught. The certification's marginal claim narrows
  to verdict-matching and discipline shape, and the epoch record must
  say so.
- **Control 7–8/10:** the control catches most planted flaws unaided,
  so raw catch cannot be credited to the seat discipline. The
  certification claim narrows to **verdict-match only**: what the
  discipline may still add is landing on the right verdict and
  dispositions, which the secondary endpoint measures. The epoch record
  must say so, and must report the verdict-match comparison beside the
  catch comparison.
- **Control ≤ 6/10:** the seat discipline carries measurable weight on
  this corpus — a plain arbitrator misses at least 4 of 10 flaws the
  certified seat caught.

If the per-trial rate and the per-case majority fall in different zones,
the epoch record reports both, and the **narrower** claim governs.
Either result is committed as-is, including a result in the ≥ 9/10 zone.
