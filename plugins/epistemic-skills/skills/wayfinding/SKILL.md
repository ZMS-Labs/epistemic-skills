---
name: wayfinding
description: 'Use when decomposing a large, foggy effort into tracked work — the goal is real but the path is full of unresolved decisions ("chart this initiative", "break this down", a brief where materially different architectures are still live) — or when reviewing a backlog whose tickets encode guesses about decisions nobody has made. Do NOT fire for efforts whose decisions are already resolved (plan decomposition belongs to the workflow layer''s planning skill), for a single open decision (open-questions or the decision itself owns it), for pre-work recon on one task (blindspot-pass), or for goal-shaping (write-goal).'
---

# wayfinding — decompose by decisions, not tasks

A large effort under fog fails in a specific way: the fog gets pre-sliced into
plausible-sounding build tickets, each silently encoding a guess about a
decision nobody has made. When the decision finally resolves the other way,
the tickets are not just stale — they are *wrong in a way no one recorded*,
and the work done against them is loss.

Wayfinding decomposes by decisions first. The map is a dependency tree whose
nodes are **decisions** (tracked items in their own right), not tasks. Build
tickets are minted only for regions where the fog is gone.

Provenance: distilled from the "wayfinder" pattern in ConnorGriffin/skills
(MIT) and convergent community practice; re-derived and hardened here.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| One open decision, operator present | open-questions | Owns the interview for a single fork or a known finite docket; wayfinding builds the *map* of decisions and feeds ready frontier decisions to it |
| Pre-work recon on one task | blindspot-pass | Recons a single brief's territory; wayfinding operates at initiative scale, and may dispatch blindspot-pass to de-fog one region |
| The decisions themselves | applying-formal-rigor / gauntlet / throwaway-prototyping | A frontier decision resolves by derivation, adversarial review, or a built probe — wayfinding sequences them, never decides |
| Persisting resolutions | decision-ledger | Every resolved node lands there (or in the tracker item itself) with provenance and a revisit condition |

## Protocol

1. **Chart the map.** One durable map artifact (in the project tracker — an
   issue/document that owns the tree, not chat). Nodes are decisions, each
   with: what it decides, what it blocks, its parent decisions, and the
   cheapest way to resolve it (derive / research / prototype / ask).
2. **Compute the frontier.** A decision is *frontier* iff every decision it
   depends on is resolved. Only frontier decisions may be worked. Asking (or
   deciding) a non-frontier question wastes the answer: it will be re-litigated
   when its prerequisites land.
3. **Resolve frontier decisions** by their cheapest adequate method, one
   region at a time. Record each resolution on the map with provenance.
   Recompute the frontier after every resolution — answers open and close
   branches.
4. **Mint build tickets only from fog-free regions.** A region is fog-free
   when no unresolved decision, anywhere upstream, could invalidate the
   ticket. Each ticket is a tracer-bullet vertical slice — it runs end-to-end,
   however thin — so the first build pass also tests the resolved decisions.
5. **Handoff gate.** A build ticket leaves wayfinding only with three facts
   attached: the decisions it depends on (resolved, linked), the observable
   behavior that proves the slice works, and the upstream decision whose
   reversal would invalidate it (or "none").

## Falsifiable gate

The map is honest when this check passes: pick any open build ticket and walk
upstream — every decision on the path is resolved and linked. One unresolved
ancestor found = the ticket was minted from fog; pull it back to the map.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "We can slice the whole thing now and adjust later" | Pre-sliced fog encodes silent guesses. "Adjusting later" means discovering which tickets were wrong *after* paying for them. |
| "This decision is obvious, skip the node" | If it's obvious, resolving the node costs one line with provenance. If it isn't, you just pre-sliced fog. |
| "Asking everything up front is thorough" | Non-frontier answers are re-litigated when their prerequisites resolve. Thoroughness is asking the *frontier*, completely, each round. |
| "The map is overhead; the backlog is the map" | A backlog of tasks cannot represent a decision dependency — that is precisely the information whose absence causes the loss. |

## Handoff boundaries

Ends at a maintained map plus fog-free build tickets carrying the three-fact
handoff. Downstream: the workflow layer's planning/execution skills own the
tickets; open-questions conducts operator interviews for frontier decisions
that need one; decision-ledger persists resolutions. Wayfinding never builds
and never decides — it sequences.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (tracker conventions, map-issue
templates, region-sizing norms). An overlay may add bindings and examples; it
never overrides the protocol.
