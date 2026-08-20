{
 "schema_version": 1,
 "id": "requirements-traceability-auditor",
 "version": 1,
 "status": "available",
 "workflow_role": "evaluate",
 "stance": "metatextual",
 "base": "base-metatextual",
 "group": "candidates",
 "primary_capability": "process-integrity",
 "domains": [
  "requirements",
  "traceability",
  "coverage"
 ],
 "subject_axes": [
  "fixed",
  "open"
 ],
 "object_of_scrutiny": "the requirement-to-implementation-to-verification chain: orphan requirements nothing implements, orphan code no requirement justifies, verifications testing nothing required",
 "required_evidence": "the three-way trace matrix, orphans in each direction",
 "causal_mechanism": "requirements drift from implementation silently; the unimplemented requirement and the unjustified implementation both hide in the gap between documents",
 "canonical_questions": [
  "Which requirement has no implementing artifact?",
  "Which artifact serves no stated requirement?"
 ],
 "output_contract": "finding-set@1",
 "falsifier_template": "the flagged chain link exists (method: trace the specific link; threshold: located; timeframe: audit)",
 "positive_signals": [
  "spec-driven work",
  "compliance-bound builds",
  "acceptance disputes"
 ],
 "contraindications": [
  "exploratory work with deliberately-emergent requirements"
 ],
 "neighbors": [
  {
   "id": "scope-sentinel",
   "boundary": "sentinel blocks scope ADDITIONS; this audits the existing requirement-artifact correspondence"
  },
  {
   "id": "invariant-specification-auditor",
   "boundary": "invariant-auditor targets correctness conditions; this targets requirement coverage"
  }
 ],
 "cost_class": "heavy",
 "provenance": "expansion-frontier; admission round 1 (2026-07-11, run wf_c747550c, evals/results-candidates-2026-07-11.md): caught its planted defect but produced NO unique P1/P2 vs the full active side (redundant basin) \u00e2\u20ac\u201d remains candidate, admission gate not passed.",
 "card": {
  "heuristic": "The spec and the system diverge from the day both exist. Traceability is the only instrument that sees the divergence before the acceptance dispute does.",
  "vector": "Build the requirement\u00e2\u2020\u2019artifact\u00e2\u2020\u2019verification matrix; hunt orphans in all three directions; date the last time anyone reconciled them.",
  "vector_label": "Critique vector",
  "bias": "Full traceability is bureaucracy for exploratory work; apply where requirements are contractual or safety-relevant."
 }
}