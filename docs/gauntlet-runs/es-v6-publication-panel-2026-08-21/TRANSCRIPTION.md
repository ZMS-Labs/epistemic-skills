# Provenance and limits of this record

## What this is

`arbitration.md` in this directory is the verbatim ruling of the isolated judge
seat of run `es-v6-publication-panel-2026-08-21`, the fourth and last
publication review of the v6.0.0 lineage. Subject:
`48009fef938bfa989fb797380080824b050f3bb4`. Verdict: **NO-GO**.

## How it was produced

A fourteen-agent orchestrated panel: five reviewing seats, a verification stage
that re-executed each seat's load-bearing claims from primary sources, and a
final judge seat that authored no seat report and did not build the candidate.
The judge re-executed the pivotal claims itself rather than adopting any seat's
word — its ruling says which.

Only the judge's arbitration was retained. The individual seat reports and the
verification stage outputs were not committed. That is a real retention gap and
it is stated rather than hidden: an auditor cannot reconstruct how the panel
reached the judge from this directory alone.

## The structural limit that bounds this verdict

**This panel was dispatched by the implementing lineage** — the same actor that
authored the candidate under review. It shares a model family with that actor.

The consequence is asymmetric and it is the whole point:

- Its **blocking** findings are credible, and one of them (RG1-01, a false scope
  statement in `docs/release/RELEASE-6.0.0.md` that concealed two material
  changes) was found against its own dispatcher's work. A panel that finds a
  defect its dispatcher would have preferred buried has earned that finding.
- Its **clearing** power is nil. A GO from a panel the implementer seated would
  establish nothing the implementer did not already believe. Dispatch controls
  selection — which verdicts reach the operator at all — and no amount of
  isolation downstream of dispatch repairs that.

So this run can block a release and cannot clear one. It is recorded on those
terms. The release record credits it only for its blocking findings.

## Relationship to run 8

Run `es-v6-publication-openai-2026-08-20` was **operator-dispatched** and
cross-family, and does not carry this limit. It judged an earlier candidate
(`d0165bd0`). Neither verdict transfers across SHAs; neither is discharged.

## Disposition

Every agent-actionable finding in `arbitration.md` was repaired in the successor
candidate, in a single commit, because step 7 supersedes the candidate on any
commit and preparing the repairs piecemeal would have compounded the problem.
The findings the judge classified as reachable only by the operator were not
repaired by an agent and are disclosed in the release record instead.

The judge's central ruling — that no owner authority reaches past RG-8, and that
the ruleset disarm is functionally the authorization act — was accepted, not
worked around. v6.0.0 ships as an **exception release** under `RELEASING.md`
§ "Independent judgment gate", with the five required disclosures made before
tag creation.
