> **Historical page.** `wayfinding` is not a live skill in v5.0.0. Use **`recon (initiative mode)`**. Consolidated in v4.0.0.
>
> Body text below is retained for method vocabulary and migration; where it conflicts with a tagged `v5.0.0` contract, the tagged source controls.

# Wayfinding

## What it does

Wayfinding decomposes a large, foggy effort by **decisions, not tasks**. The map is a dependency tree in the project tracker whose nodes are decisions — each recording what it decides, what it blocks, its parents, and its cheapest adequate resolution method (derive / research / prototype / ask). Only *frontier* decisions (all prerequisites resolved) may be worked; the frontier is recomputed after every resolution. Build tickets are minted only from fog-free regions — where no unresolved upstream decision could invalidate them — as tracer-bullet vertical slices carrying a three-fact handoff: resolved dependencies (linked), the observable behavior that proves the slice, and the upstream decision whose reversal would invalidate it.

The failure it prevents: pre-slicing fog into plausible build tickets that silently encode guesses about unmade decisions — wrong in a way nobody recorded, discovered only after the work is paid for.

## Falsifiable gate

Pick any open build ticket and walk upstream: every decision on the path must be resolved and linked. One unresolved ancestor = the ticket was minted from fog; pull it back to the map.

## Use it when

- Decomposing a large effort whose path holds unresolved decisions ("chart this initiative", materially different architectures still live).
- Reviewing a backlog whose tickets encode guesses about decisions nobody has made.

## Do not use it when

- The decisions are already resolved — plan decomposition belongs to the workflow layer's planning skill.
- There is a single open decision — open-questions (or the decision's own process) owns it.
- You need pre-work recon on one task — Blindspot Pass.
- You need goal-shaping — Write Goal.

## Boundary and handoffs

Wayfinding sequences; it never builds and never decides. Frontier decisions resolve via open-questions (operator interview), applying-formal-rigor (derivation), gauntlet (adversarial review), or throwaway-prototyping (built probe); resolutions persist via decision-ledger; fog-free tickets go to the workflow layer.

Provenance: distilled from the "wayfinder" pattern in ConnorGriffin/skills (MIT), re-derived and hardened.
