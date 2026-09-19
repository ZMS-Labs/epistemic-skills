# Gauntlet execution model — STANDARD method (Phase 0.5)

> Adopted 2026-07-07 as the **standard way to run the panel**, replacing
> ad-hoc consecutive general-purpose subagents. Origin: the first live gauntlet
> (FO "worth building?") was hand-orchestrated with fresh general-purpose agents
> and hand-written per-lens prompts — which surfaced two structural fixes.

## Execution contract

This reference describes one Workflow implementation of separate initial
examinations followed by evidence checking and adjudication. The authoritative
method is `../SKILL.md`; a particular Workflow API is not a package dependency.
Use the actual host's supported primitives and report what separation occurred.

Prefer isolated role calls on the same frozen dossier, with initial findings
joined only after each pass finishes. Bind the canonical role and selected
shared method either natively or with `scripts/materialize_role.py`. Parallel
execution can reduce latency; sequential isolated calls can preserve the same
initial information boundary. Without isolated calls, label same-context use
explicitly. It cannot claim blinded or independent examination.

The owner designates the reviewer. A different model family is optional;
model tiers within one family do not establish family diversity, and family
diversity alone does not establish independent evidence. Shared prompts,
evidence and inherited context remain sources of correlation. Role binding
improves reproducibility but does not guarantee discipline or independence.

## Reference Workflow

`assets/gauntlet-workflow.template.js` expresses fan-out, barrier, evidence checks,
gates and adjudication. Use it only on a host that actually supports its APIs.
The host journal and meter are evidence only when executed and captured. A
shipped template is not a live deployment or a promise of resume support.

Missing panel or required gate results leave the review incomplete. The template
retains malformed findings instead of silently deleting them, and refuses GO
while a material finding lacks its revision condition. A required gate's BLOCK
cannot be voted away. Finalize and verify the material review record using the
canonical scripts; template output alone does not establish factual correctness.
The synthetic completion tests exercise this boundary, not an actual agent panel.

After initial comparison, use constructive synthesis for a revised candidate
when useful. Recheck changed claims and their dependencies, preserve unaffected
evidence and material dissent, and stop at the scoped closure condition. Budget
exhaustion preserves unresolved findings; it does not certify success.

## Pipeline roles (replaces the "five groups" mental model)

`generate_options` → `evaluate` → `gate` → `adjudicate` (see
`reference/lens-registry.md`). On **open questions**, 1-2 option generators run
BEFORE the panel and emit `option-set@1` (3-5 materially distinct alternatives,
null option mandatory); those alternatives seed the DeepReason docket and the
evaluators inspect them. **Generator runs never satisfy evaluator-panel
diversity.** Gates (`governance-lawyer`, `red-lines-arbitrator`) can block
regardless of evidence weighing. The final judge is `pragmatic-judge` by default.

Prospective failure analysis can elicit separate narratives before comparison.
An AI-generated set of narratives is not evidence that actual stakeholders or
independent human participants were consulted. Preserve that provenance limit.
The retired premortem ID remains historical; the protocol belongs to the method.

## Depth → evaluator seats (judge always separate)

quick 3 · standard 5 · deep 5 · max 7. The proposed measurement bundle is unbuilt and cannot count toward
completed review coverage. Panel selection is deterministic: `scripts/select_lenses.py` (constraints
+ replay record). The Workflow `parallel()` fans out the selected panel; the
arbitrator runs after the barrier.
