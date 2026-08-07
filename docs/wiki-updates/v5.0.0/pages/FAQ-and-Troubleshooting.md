> **Applies to:** epistemic-skills v5.0.0
>
> **Canonical sources:** [installation](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/README.md#installation-and-compatibility), [release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-5.0.0.md)

# FAQ and Troubleshooting

## I see duplicate skill triggers

You likely installed more than one copy (for example, a native plugin plus `npx skills add`). Keep exactly one v5.0.0 mechanism per harness, verify the retained checkout is tagged `v5.0.0`, then reload/restart the harness. Cursor must not combine its loaded plugin with `~/.cursor/skills/`. A v5.0.0 install registers exactly fourteen skills. A retired name (`using-epistemic-skills`, `helix`, or a pre-4.0 consolidated name) appearing as a distinct trigger indicates a leftover older copy.

## I expected a skill to trigger, but nothing happened

Start with the routine test. A reversible, local, directly checkable, non-precedential task exits silently after its bounded check. Otherwise, confirm the released frontmatter description actually has a positive trigger. Absent triggers and routine exits do not generate skip records. If the approach itself is uncertain, invoke [`metacognate`](Skill-Metacognate) — silence is a success state. If a harness does not auto-load descriptions, load skills according to its native integration.

## The harness has no subagents or custom role types

Do not pretend the missing runtime primitive exists. Gauntlet needs exact-role, context-isolated evaluators; its stated degradation is sequential isolated calls, and runtimes without custom-role registration use the replayable materialized-role adapter. Codex requires the tagged renderer for native user-agent registry roles. For material UAT, lack of separate actor/verifier/judge contexts prevents a ready-looking PASS packet.

## Research connectors or the durable library are unavailable

Resolve's literature instrument (the evidence-research method) requires the Consensus + Scite + Zotero/equivalent triad for its full contract. State the missing layer and its label; do not substitute general search or a single internal document for the triad.

- **No Scite:** run Consensus + Zotero and stamp each matrix row `reception: UNVERIFIED (Scite unavailable)`.
- **No Consensus:** use Scite-led discovery (and label the loss of Consensus study-design filtering) plus Zotero holdings/deposit.
- **No Zotero/equivalent:** run Consensus + Scite and stamp each matrix row `holdings: UNVERIFIED (Zotero unavailable)`; record `deposit: SKIPPED` and name the visible durability gap.

Hold, escalate, or use a bounded reversible probe only when the qualified evidence cannot support the particular load-bearing premise the consumer needs.

## UAT returned `INCONCLUSIVE`

`INCONCLUSIVE` is never PASS. Preserve the verdict, inspect the evidence/criterion gap, and either collect valid evidence, repair the surface, or leave the acceptance claim open. A routine presentation edit should use its direct preview/test instead of manufacturing a full UAT packet.

## My external model handoff is blocked

Outsource is not ready until `docs/outsource/<work-id>/HANDOFF.md` is context-complete, committed at an exact GitHub ref, pushed, and target-readable. Without that, return `BLOCKED`; do not send a short prompt that conceals the missing packet. Record every return relay in-repo and re-verify it before relying on it.

## I resumed from a summary but cannot verify the claimed state

Run decision-ledger's resume mode (continuity-verify) before taking the next load-bearing action. Re-anchor claims to durable files, Git refs, issues, or receipts. If an anchor is unavailable or contradictory, produce an unresolved-state result and stop at the hold/escalation/reversible-probe boundary; a summary is a claim, not state.

## Cursor says `/add-plugin epistemic-skills` cannot find the plugin

This is expected in v4.0.0: the plugin is not publicly listed, so the public marketplace path is unavailable. Use a tagged local install or a Teams/Enterprise team marketplace import. Do not report public-marketplace support until Cursor lists the plugin.

Separately, the retained Cursor behavioral/runtime evaluation epoch remains `BLOCKED_EXTERNAL`; that label applies only to the retained evaluation evidence.

## Does the release prove the skills are better across every provider?

No. v4.0.0 is an immutable support point, not universal behavioral proof. Its release record states the boundaries explicitly: no behavioral-superiority claim (the four-arm campaign ran under its committed design and found no arm separation), no claim that consolidation improves outcomes, no post-consolidation trigger-epoch evidence, and single-model-family evidence throughout. Earlier retained limitations — two genuine P0 behavioral failures, AGY quota availability failures, Cursor's blocked external epoch, the no-credit post-hoc diagnostic — remain preserved in the append-only risk record. See [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations).

## Where is the exact answer when this handbook is brief?

Follow the page's tagged canonical source link. Released `SKILL.md`, contracts, schemas, checks, and release records outrank wiki summaries. The Wiki is unversioned navigation over versioned sources.
