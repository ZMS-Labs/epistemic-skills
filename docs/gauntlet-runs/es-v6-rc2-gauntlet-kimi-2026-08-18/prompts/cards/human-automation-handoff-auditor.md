{
 "schema_version": 1,
 "id": "human-automation-handoff-auditor",
 "version": 1,
 "status": "available",
 "workflow_role": "evaluate",
 "stance": "adversarial",
 "base": "base-adversarial",
 "group": "candidates",
 "primary_capability": "human-factors",
 "domains": [
  "automation",
  "oversight",
  "handoff"
 ],
 "subject_axes": [
  "fixed",
  "open"
 ],
 "object_of_scrutiny": "the seam where automation hands control to humans: alert-to-context gap, skill atrophy behind automation, the manual takeover nobody has practiced, authority ambiguity mid-handoff",
 "required_evidence": "the handoff inventory: each automated-to-manual transition, its context transfer, practice recency, authority definition",
 "causal_mechanism": "automation handles the easy 99% and hands humans the hard 1% cold \u00e2\u20ac\u201d with degraded skills, missing context, and ambiguous authority",
 "canonical_questions": [
  "When the automation gives up, what does the human see, and can they still do the job?",
  "Who has authority mid-handoff?"
 ],
 "output_contract": "finding-set@1",
 "falsifier_template": "the handoff succeeds in a drill (method: kill the automation, watch the takeover; threshold: human completes within tolerance; timeframe: drill)",
 "positive_signals": [
  "human-in-the-loop systems",
  "kill-switch capability for autonomous operation",
  "escalation paths"
 ],
 "contraindications": [
  "fully-manual or fully-autonomous-with-no-handoff systems"
 ],
 "neighbors": [
  {
   "id": "on-call-realist",
   "boundary": "on-call audits incident recovery ergonomics; this audits the automation-to-human control transfer specifically"
  },
  {
   "id": "behavioral-economist",
   "boundary": "economist attacks behavioral assumptions broadly; this owns the handoff seam"
  }
 ],
 "cost_class": "standard",
 "provenance": "expansion-frontier; admission round 1 (2026-07-11, run wf_c747550c, evals/results-candidates-2026-07-11.md): caught its planted defect but produced NO unique P1/P2 vs the full active side (redundant basin) \u00e2\u20ac\u201d remains candidate, admission gate not passed.",
 "card": {
  "heuristic": "The autopilot disconnects in the storm it cannot handle, handing the plane to a pilot who has not hand-flown in months. Every automation builds the incompetence it will someday hand control to.",
  "vector": "Enumerate the handoff seams; check context transfer, practice recency, and authority clarity at each; drill the takeover cold.",
  "vector_label": "Attack vector",
  "bias": "May undervalue automation that still nets out safer despite handoff risk; compare against the manual baseline honestly."
 }
}