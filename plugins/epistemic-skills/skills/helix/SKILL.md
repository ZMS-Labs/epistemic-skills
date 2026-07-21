---
name: helix
description: "Use when both a workflow-skill layer (such as superpowers) and the epistemic-skills collection are installed and a task is about to begin; when a workflow skill (brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, finishing-a-development-branch) has just fired and its epistemic pair needs checking; or when sequencing the two collections is ambiguous. Not for single-collection routing (that's using-superpowers / using-epistemic-skills) or trivial, fully-held-context work needing no ceremony."
---

# helix — two strands, one axis

A workflow-skill layer (such as [superpowers](https://github.com/obra/superpowers))
is the strand for *how the work gets done*: brainstorming, plan-writing,
test-driven development, systematic debugging, verification. The
epistemic-skills collection is the strand for *what counts as knowing it's
right*: reconnaissance, derived decisions, evidenced claims, adversarial
gates, blinded verification. Neither strand is complete alone — workflow
without epistemics executes the wrong thing efficiently; epistemics without
workflow knows the right thing and never ships it.

`helix` is the pairing between them. Like the base pairs of a double helix,
each stage of one strand binds to a specific member of the other, and the
task is the axis both wind around. This skill tells you which member pairs
with which stage, in what position — and nothing else. **It never routes
within a collection** — `using-superpowers` and `using-epistemic-skills`
remain the routers; read the skill this map pairs you to.

## The governing rule

At every stage boundary, **the epistemic member fires first, then the
workflow member carries the stage out.** The epistemic skill decides whether
you are solving the right problem, with real evidence, before effort is
spent; the workflow skill then structures the effort. Never run a workflow
stage first and bolt its epistemic pair on afterward — recon after design is
archaeology, and evidence after the verdict is rationalization.

## The pairing map

| Workflow stage | Epistemic pair | Position |
|---|---|---|
| task start (non-trivial, unfamiliar territory) | **blindspot-pass** | *before* brainstorming — recon the territory, then design |
| brainstorming (any ≥2-option design choice) | **applying-formal-rigor** | *inside* — the choice is derived from named theory, not asserted |
| brainstorming (a premise leans on "research says…") | **evidence-research** | *cross-cutting* — reception-check the literature before the premise bears load |
| brainstorming approval / writing-plans (irreversible or one-way-door design) | **gauntlet** | *at approval* — freeze the design as the subject; GO/CONDITIONAL/NO-GO before planning on top of it |
| executing-plans / persistent or long-horizon runs (explicit goal intent only) | **write-goal** | *before* persistent execution — bind the outcome to proof and stop rules |
| test-driven-development / implementation | (none mandatory) | epistemic disciplines fire only on their own triggers; clean implementation needs no ceremony |
| systematic-debugging (fix rests on a complexity or correctness claim) | **applying-formal-rigor** | *inside* — "this is O(n log n) now" and "this can't race" are derived, not asserted |
| verification-before-completion (UI-facing surface) | **evidence-locked-uat** | *is* that skill's UI-facing instance — blinded verifier, never self-certification |
| finishing-a-development-branch (irreversible / high-blast-radius change) | **gauntlet** | *pre-merge* — the last gate before a commit you can't take back |
| any workflow stage not listed above | *(none mandatory)* | disciplines still fire on their own standalone triggers — e.g. gauntlet's own trigger, not helix, governs a code-review approval |

Positions mean exactly what they say: *before* = the epistemic output is an
input to the stage; *inside* = the stage pauses at the decision point, runs
the discipline, and resumes with its verdict; *at approval* / *pre-merge* =
the stage's exit gate; *cross-cutting* = called at the moment a qualifying
premise appears, at any stage.

## Co-fire checklist

When a strand fires, check its pair — in both directions. Make the check auditable: at each
stage boundary, emit one line in the form `helix-check: <stage> → <pair> → fired|skipped(<reason>)`.

- **A workflow stage just fired.** Ask: does its epistemic pair's own trigger
  match right now? If yes, run it in its position. If no, skip it **and say
  you skipped it** — an unfired pair is a stated decision, not an omission.
- **brainstorming is starting** → did blindspot-pass run, or was its trigger
  absent (territory already fully held in context)?
- **a design choice is being argued** → is "better / cleaner / faster" being
  asserted? That is applying-formal-rigor's trigger.
- **a plan is about to be approved** → is anything in it irreversible? That
  is gauntlet's trigger, now — before effort is spent building on it.
- **a persistent goal is being created** → only on explicit goal-authoring
  intent does write-goal fire; length of task alone is not intent.
- **"it's done" is about to be claimed** → verification-before-completion is
  the stage; if the surface is UI-facing, the stage *is* evidence-locked-uat.
- **a branch is about to merge** → irreversible or high-blast-radius? gauntlet
  gates the merge, not the retrospective.
- **An epistemic discipline just fired standalone.** Ask: which workflow
  stage consumes its output? blindspot-pass's rewritten request feeds
  brainstorming; formal-rigor's verdict feeds the plan; a gauntlet
  CONDITIONAL feeds the branch-finishing checklist. An epistemic output no
  workflow stage consumes is a report no one reads.

Fire-nothing is a valid outcome. helix manufactures no work: a trivial,
reversible task in held territory pairs zero disciplines with zero ceremony.

## Any harness, any layer

This file is plain markdown and assumes no harness. "Read/load the skill"
means whatever your harness does — description-triggered skill loading,
a context-file include, or pasting the file into the loop.

- **If your harness auto-triggers by description** (Claude Code, Cursor,
  Codex): this skill fires at non-trivial task start when a workflow layer
  is in play.
- **If your harness loads one context file** (Gemini CLI via GEMINI.md, or
  similar): the collection's context file names helix as the tandem entry
  point; read it from there.
- **If nothing auto-triggers**: the path in is `using-epistemic-skills`,
  which points here whenever a workflow layer is present.
- **If your workflow layer is not superpowers** (Kimi, agy, a house style,
  or beyond): map the stage names — every layer has a design step, a
  planning step, an implementation step, a debugging step, and a "done?"
  step; bind them to your layer's equivalents. Example — a plan→build→verify
  harness (Cursor, agy): pair blindspot-pass with plan, gauntlet with any
  irreversible pre-build decision, evidence-locked-uat with verify.

## Anti-patterns

| Thought | Reality |
|---|---|
| "Both layers are installed — run every discipline at every stage" | Ceremony. Fire only matched triggers; state what you skipped. |
| "I'll do the workflow stage first and add the epistemic check after" | Backwards. The pair fires first at every boundary — recon after design is archaeology. |
| "helix told me which skill; I know roughly what it does" | helix only pairs. Read the paired skill; the discipline lives there. |
| "This replaces the two routers" | It sits between them. Member-level routing stays in `using-superpowers` and `using-epistemic-skills`. |
| "Superpowers isn't installed, so none of this applies" | The pairings are stage-shaped. Map them to whatever workflow steps the session actually has. |
| "I basically already did this informally" | Informal ≠ the discipline. If the trigger matches, run the actual skill; "I already thought about it" is how recon-after-design smuggles itself back in. |

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the pairings to the local environment (which harness auto-fires which
stage, local workflow-layer names, fleet-specific gates). An overlay may add
bindings; it never overrides the pairing map.
