# Gauntlet execution model — STANDARD method (Phase 0.5)

> Adopted 2026-07-07 as the **standard way to run the panel**, replacing
> ad-hoc consecutive general-purpose subagents. Origin: the first live gauntlet
> (FO "worth building?") was hand-orchestrated with fresh general-purpose agents
> and hand-written per-lens prompts — which surfaced two structural fixes.

## Two decisions, now standard

> **Scope.** This document is the **Claude Code reference implementation** of the
> harness-agnostic Step-5 contract (concurrent, context-isolated role-agents behind a
> barrier). The *contract* is what binds; the Workflow-tool specifics below are one way to
> meet it. Native custom-agent registration is preferred but not required: a harness
> may materialize the exact canonical role into a replayable prompt binding (see
> `runtime-role-binding.md`). On a harness without a parallel-subagent primitive, use
> the degrade fallback (consecutive isolated agent calls) — the isolation, exact role
> contract, and falsifier discipline are the invariants, not the Workflow API.

### 1. Orchestrate the panel as a dynamic Workflow (not consecutive subagents)

The panel is a deterministic **fan-out → barrier → mechanical-criticism →
arbitrate → verdict** — exactly the Workflow tool's shape. Standard for
**depth ≥ standard**; manual consecutive subagents are the **degrade-only
fallback** when Workflow is unavailable/unauthorized (disclose it in the
summary as `orchestration: manual-degraded`).

Why it is the standard:
- **Determinism** — the 8 steps are code, not recollection; the barrier before
  arbitration is enforced, not remembered.
- **Structured schemas** force every lens to return
  `{findings[], falsifier-per-finding, hypothesis_vote, verdict}`; a finding
  with no falsifier is rejected at the tool layer — the falsifiability contract
  gets teeth for free.
- **meter==log + replayable log come free** — the Workflow journal IS the
  append-only record; `budget.spent()` IS the spend meter. Two of the four
  DeepReason disciplines delivered natively instead of approximated.
- **Resumable** — a gauntlet that dies mid-panel resumes from cache.

Template: `assets/gauntlet-workflow.template.js`. The invoking skill (or the
operator saying `/gauntlet`) is the Workflow opt-in.

### 2. Predefined role-agents, not fresh general-purpose agents

Each lens is a **predefined agent type**, not a general-purpose agent
hand-prompted each run:

- **Five base-role agents** — `gauntlet-adversary`, `gauntlet-constructive`,
  `gauntlet-metatextual`, `gauntlet-generator`, `gauntlet-arbitrator`
  (`agents/`). Each has the base discipline (falsifier contract, `[V]`/`[I]`/`[H]`
  evidence tiers, verbalized sampling, no-pre-arbitration) **baked into its
  system prompt** and a **pinned model**.
- **The personas stay as parameters** — the role agent receives the roster card
  as `{{PERSONA_SPEC}}` (cards are generated views of `roster/registry.json`;
  counts live only in the generated `roster/INDEX.md`). So it is *5 disciplined
  roles × the registry*, not one agent file per persona, and not a fresh
  improvised prompt each time.
- **Model-family separation is enforced** — the arbitrator is pinned to the most
  capable tier and, where configurable, a **different family than the lenses**
  (arbitrator `opus`, lenses `sonnet` as the in-house default; cross-provider is
  the ideal when wired). The arbitrator self-reports if it detects it shares a
  family with the lenses.

Benefit: reproducibility (a gauntlet discipline), guaranteed discipline (can't
forget the falsifier contract), and guaranteed independence + family-separation —
none of which a hand-crafted general-purpose prompt guarantees.

## What stays MANUAL (do not "improve" into a team)

**Structural independence of the lens phase is the source of the gauntlet's
value** and must not be turned into an agent team. Lenses must NOT see each
other's findings before arbitration — cross-talk collapses independent signal
into consensus mush. (In the first live run, the most valuable moment — one lens
killing a hypothesis another independently declared decisive — happened ONLY
because they could not talk.) The Workflow's `parallel()` barrier gives exactly
this: concurrent, isolated, joined only after all complete.

Agent teams are acceptable ONLY at the **bounded-reinstatement** sub-round
(arbitrator + one challenger, one round) — never for the panel.

## Pipeline roles (replaces the "five groups" mental model)

`generate_options` → `evaluate` → `gate` → `adjudicate` (see
`reference/lens-registry.md`). On **open questions**, 1-2 option generators run
BEFORE the panel and emit `option-set@1` (3-5 materially distinct alternatives,
null option mandatory); those alternatives seed the DeepReason docket and the
evaluators inspect them. **Generator runs never satisfy evaluator-panel
diversity.** Gates (`governance-lawyer`, `red-lines-arbitrator`) can block
regardless of evidence weighing. The final judge is `pragmatic-judge` by default.

**The premortem, done right, is this architecture** — independent participant
narratives elicited before any cross-talk is exactly the `parallel()` barrier.
That is why `premortem-facilitator` was retired as a lens: the protocol lives
here, in the methodology, not in a persona card.

## Depth → evaluator seats (judge always separate)

quick 3 · standard 5 · deep 5 · max 7 + measurement bundle (Phase 3 — not yet
built). Panel selection is deterministic: `scripts/select_lenses.py` (constraints
+ replay record). The Workflow `parallel()` fans out the selected panel; the
arbitrator runs after the barrier.
