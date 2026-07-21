# helix — design

**Date:** 2026-07-20
**Status:** Approved (operator, this session)
**Type:** New skill (pairing/interleave layer)

## Problem

The collection already documents composition with a workflow-skill layer in a
buried section of `using-epistemic-skills`, but in practice: (1) there is no
unified entry point — an agent at task start faces two routers and no single
artifact that emits one combined sequence; (2) ordering at stage boundaries
(blindspot-pass vs brainstorming, gauntlet vs finishing-a-branch) is ambiguous
enough to cause skipped or duplicated work; (3) co-firing is not automatic —
the workflow skills fire and the epistemic ones don't interleave, or vice
versa. The operator's goal: using the two collections together should be
natural, automatic, and complete — without the user needing to know how.

## Decision

Add one skill, **`helix`**, to the epistemic-skills collection.

- **Name/metaphor:** the double helix. Two strands, one axis. The workflow
  strand (superpowers) is *how the work gets done*; the epistemic strand is
  *what counts as knowing it's right*. Every stage of one strand pairs with a
  base on the other; the task is the axis both wind around.
- **Shape:** an *interleave contract* (Approach A). helix defines the pairing
  rules between workflow stages and epistemic disciplines. It **never
  duplicates either router's trigger tables** — it hands off to
  `using-superpowers` and `using-epistemic-skills` for member-level detail.
  Rejected alternative: a super-router merging both trigger tables (rots on
  every upstream superpowers release; violates the collection's "know where
  you stop" invariant).
- **Coupling:** superpowers-named, explicit. Stage names are superpowers'
  skill names (brainstorming, writing-plans, test-driven-development,
  systematic-debugging, verification-before-completion,
  finishing-a-development-branch, executing-plans). This is safe because
  superpowers is itself multi-harness. A short "other layers" note maps the
  pairings for non-superpowers workflow layers: the pairings are
  stage-shaped, not tool-shaped.

## The governing rule

At every stage boundary, **the epistemic member fires first** — it decides
whether you are solving the right problem with real evidence — then the
workflow member carries the stage out. (This restates and operationalizes the
existing router's "epistemic discipline runs first" line as helix's single
axiom.)

## The pairing map (core content of SKILL.md)

| Workflow stage (superpowers) | Epistemic pair | Position |
|---|---|---|
| task start | blindspot-pass | *before* brainstorming — recon the territory first |
| brainstorming | applying-formal-rigor | *inside* — every ≥2-option design choice is derived, not asserted |
| brainstorming (scholarly premise) | evidence-research | *cross-cutting* — any "research says…" gets reception-checked |
| brainstorming approval / writing-plans | gauntlet | *at approval* — irreversible / one-way-door designs only |
| executing-plans / persistent runs | write-goal | *before* persistent execution, on explicit goal intent only |
| test-driven-development / implementation | (none mandatory) | epistemic disciplines fire only on their own triggers |
| systematic-debugging | applying-formal-rigor | *inside* — complexity/correctness claims in fixes get derived |
| verification-before-completion | evidence-locked-uat | *is* its UI-facing instance |
| finishing-a-development-branch | gauntlet | *pre-merge* — irreversible or high-blast-radius changes only |

## Co-fire checklist (the automaticity mechanism)

Bidirectional prompts, e.g.: "brainstorming just fired → did blindspot-pass
run, or was its trigger absent?"; "about to claim UI-facing work done → this
is verification-before-completion, so it is evidence-locked-uat"; "about to
merge → is anything here irreversible? then gauntlet." Every entry ends with
the skip-and-say rule: absent trigger → skip the stage and *state* that you
skipped it. Fire-nothing is a valid outcome; helix manufactures no work.

## Harness-agnosticism (hard requirement)

helix must work on any harness — Claude Code, Codex, Cursor, Gemini, Kimi,
agy, and beyond:

1. **Neutral by construction.** Plain markdown. No harness-specific tool
   names, no slash-command syntax, no session-hook mechanics. Invocation
   verbs are "read/load the skill."
2. **Discovery per harness.** Description-triggering harnesses (Claude Code,
   Cursor, Codex) fire it via frontmatter at non-trivial task start when a
   workflow layer is in play. Context-file harnesses (Gemini via GEMINI.md,
   agy, single-context-file harnesses) discover it via an entry-point pointer
   added to GEMINI.md and README.
3. **Fallback rule stated in the skill:** if the harness auto-triggers
   nothing, the path in is the `using-epistemic-skills` pointer plus the
   GEMINI.md/README references.
4. **No install dependency on superpowers.** If superpowers is absent, the
   stage concepts still map to whatever design/debug/verify steps the
   session actually has.

## Placement and wiring

- `plugins/epistemic-skills/skills/helix/SKILL.md` (canonical; root
  `skills/` is a git symlink to it, so directory scan registers it — the
  "dual-copy" assumption in the approved draft was wrong).
- `using-epistemic-skills/SKILL.md` (both copies) gains a one-line pointer:
  when a workflow layer is present, read `helix` for the stage pairings. The
  router remains authoritative for the epistemic-only case.
- `GEMINI.md`: one line naming helix as the tandem entry point.
- Manifest surfaces (root `plugin.json`, `gemini-extension.json`, both
  `marketplace.json`, `.claude-plugin`/`.codex-plugin`/`.cursor-plugin`
  plugin.json) and README: descriptions/skill counts reconciled to the tree's
  actual state at commit time (working tree is mid-bump for `write-goal`;
  counts are verified, not assumed).

## Anti-patterns (to be included in SKILL.md)

| Thought | Reality |
|---|---|
| "Run every discipline at every stage" | Ceremony. Fire only matched triggers; say what you skipped. |
| "Workflow first, epistemics after" | Backwards. The epistemic member gates the stage, then the workflow member executes it. |
| "helix replaces the routers" | It only pairs. Member-level routing lives in the two routers. |
| "Superpowers isn't installed, so nothing applies" | Map the stage names to your workflow layer; the pairings are stage-shaped. |

## Out of scope

No changes to superpowers. No merged trigger tables. No LOCAL.md overlay
shipped (helix honors the same overlay convention as the router, but ships
none). No new agents, commands, or harness adapters.
