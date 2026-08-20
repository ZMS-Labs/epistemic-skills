{
 "schema_version": 1,
 "id": "chesterton-gate",
 "version": 2,
 "status": "available",
 "workflow_role": "evaluate",
 "stance": "metatextual",
 "base": "base-metatextual",
 "group": "metatextual",
 "primary_capability": "process-integrity",
 "domains": [
  "deletion",
  "legacy",
  "incident-history"
 ],
 "subject_axes": [
  "fixed",
  "open"
 ],
 "object_of_scrutiny": "ONE specific proposed deletion/simplification: approve or block based on evidence that its originating incident/consumer is obsolete \u00e2\u20ac\u201d requires a deletion in scope",
 "required_evidence": "the fence's reconstructed origin (incident/edge case/constraint), evidence the origin is obsolete or extant, reachability/liveness data",
 "causal_mechanism": "scar tissue encodes incidents; deleting a fence whose origin is merely unknown (vs known-obsolete) re-runs the incident that built it",
 "canonical_questions": [
  "What incident/consumer created this, and is it provably gone?",
  "Is the justification 'origin obsolete' or just 'I don't see why'?"
 ],
 "output_contract": "finding-set@1",
 "falsifier_template": "the origin is demonstrated obsolete (method: incident/consumer liveness check; threshold: provably unreachable/retired; timeframe: verification)",
 "positive_signals": [
  "cleanup PRs",
  "simplification proposals",
  "'obviously redundant' claims"
 ],
 "contraindications": [
  "HARD BOUNDARY: no specific deletion proposed (history reconstruction belongs to protocol-archeologist)",
  "greenfield code with no scar tissue"
 ],
 "neighbors": [
  {
   "id": "protocol-archeologist",
   "boundary": "archeologist reconstructs history with NO deletion in scope; gate adjudicates ONE proposed deletion \u00e2\u20ac\u201d enforced boundary"
  },
  {
   "id": "minimalist-zen-master",
   "boundary": "zen-master generates deletion candidates; gate adjudicates each candidate against origin evidence"
  }
 ],
 "cost_class": "standard",
 "provenance": "pr74-roster-expansion-2026-07-09 (sovereign-gauntlet lineage)",
 "card": {
  "heuristic": "Do not remove a fence until you know why it was put there. Every \"obviously redundant\" check, weird workaround, and ugly special case is scar tissue over a wound someone bled from. The confident deletion is the dangerous one.",
  "vector": "For each thing the proposal removes, simplifies, or \"cleans up,\" reconstruct the reason it existed \u00e2\u20ac\u201d the incident it prevents, the edge case it handles, the constraint it encodes. Flag every deletion whose justification is \"I don't see why this is here.\" Distinguish genuine cruft (dead, provably unreached) from load-bearing ugliness (invisible until it is gone).",
  "vector_label": "Critique vector",
  "bias": "Conservatism can ossify genuine cruft into permanent debt; weigh against evidence a fence is truly dead."
 }
}