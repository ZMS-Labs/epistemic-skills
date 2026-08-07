# Lens report — usability, proportionality, and repository boundary

> **Current-status notice (2026-08-07):** This is a preserved frozen review
> artifact. Its cross-repository premises and current merge conditions are
> superseded by [POST-FREEZE-RECONCILIATION.md](../POST-FREEZE-RECONCILIATION.md).
> Do not use statements below that Practical Agency does not exist, that no
> `manifest` skill exists, or that workflows created no jobs as current facts.


**Role:** constructive/maintainability evaluator  
**Subject:** frozen `review/pr110-commission-watch-candidate-v2`  
**Question:** Does the design recover useful agency without recreating Helix's routing and ceremony failures?

## Validation kernel

The operator's original experience had real value: one phrase could recruit a
workflow and epistemic estate into coherent motion. The redesign must preserve
that ease while refusing the false claim that a static skill table or prompt-time
agent possesses persistence.

## Usability assessment

### What improved

- The public skill id remains `watch`, avoiding a current-major breaking rename.
- Its resident description directly says “commission or re-prove an external
  watch” and “it does not itself watch.”
- The body gives the human-facing conceptual model first: skill, commission
  record, external observer.
- `BLOCKED` is a valid result, so a user does not need to invent infrastructure
  before invoking the discipline.
- The complex JSON carrier is intended for adapters and machines; the operator
  still invokes one skill rather than manually choosing internal state-machine
  operations.
- No alias skill was added, so description-budget pressure and duplicate routing
  were avoided.
- The description total falls to 8,159 bytes rather than growing.
- README and `health` use “external observer commissioned under `watch`,” which
  makes the composition legible without requiring the reader to infer the
  runtime boundary.

### What remains necessarily complex

The commission record is substantial. That complexity is justified only when a
condition matters between sessions; it would be disproportionate for a current
health readout or an alert nobody will act upon. The skill's positive and negative
triggers keep ordinary work out.

Human users should not be expected to hand-author the full JSON except for
inspection or debugging. Practical Agency and provider adapters should generate,
validate, and present it through a compact status view.

## Repository-boundary assessment

### `commission-watch` belongs in `epistemic-skills`

It owns the trust question: what evidence supports the claim that an external
observer exists, is controllable, has been proof-fired through the real path, and
can currently be relied upon? It does not own a scheduler or execution runtime.

### `gauntlet` remains epistemic

Gauntlet freezes evidence, attacks claims, preserves dissent, and renders a
verdict. Its size does not change its subject. Moving it into the acting layer
would let the mission driver own its own court.

### Practical Agency belongs outside `epistemic-skills`

Practical Agency owns mission custody: preserving operator intent, authority,
protected state, continuity, capability discovery, execution frontier, and
checkpointing. Its sole public skill is `manifest`. It consumes workflow and
epistemic capabilities but does not become one of them.

This division also prevents the new actor from quietly redefining epistemic
verdicts. Practical Agency may invoke `metacognate`, `gauntlet`, UAT, or
`commission-watch`; it must consume their results without rewriting them.

### `fleet-orchestrator` remains an execution substrate

Fleet Orchestrator routes concrete work across runtimes. Practical Agency may use
it as an adapter, but mission semantics cannot depend on the k3s implementation
or any one installed runtime.

## Findings

### F-UB-1 — The one-command experience is designed but not yet delivered

**Severity:** P2 program scope  
**Status:** open by explicit exclusion

The candidate creates the design and implementation plan for Practical Agency,
but there is no `practical-agency` repository or live `manifest` skill. Therefore
“this is my will; manifest it” is not yet an available operational entry point.

**Falsifier:** This finding closes when the separate repository exists, its sole
public `manifest` skill is installable, it can create/resume a validated mission
manifest, and at least one supported harness passes the clean-install examples.

**Impact:** This does not invalidate commission-watch. It prevents the PR from
being described as completing the larger mission-control program.

### F-UB-2 — Compatibility alias should remain linguistic, not packaged

**Severity:** positive design constraint  
**Status:** retained

“Helix it” may be recognized later as compatibility intent for `manifest`, but a
second `helix` skill would reintroduce another resident description, another
routing surface, and ambiguity over which actor owns the mission.

**Falsifier:** A packaged alias would be justified only if real usage data shows
that natural-language compatibility cannot be maintained and its benefit exceeds
the global description-budget and routing costs. No such evidence exists.

### F-UB-3 — Complex records need a compact operator view

**Severity:** P3 future usability requirement  
**Status:** assigned to Practical Agency plan

The machine carrier is intentionally explicit; presenting it raw would recreate
the ceremony tax the project is trying to reduce.

**Recommendation:** `manifest status` should summarize current state, next action,
blocking evidence, proof freshness, and unresolved receipts, with the full record
available for inspection rather than required for ordinary use.

## Verdict from this lens

**PASS for the repository boundary and commission-watch user model. CONDITIONAL
for the larger agency objective**, because Practical Agency and `manifest` remain
designed rather than implemented.
