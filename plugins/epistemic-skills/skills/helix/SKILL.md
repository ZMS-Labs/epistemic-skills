---
name: helix
description: "Use when both a workflow-skill layer (such as superpowers) and the epistemic-skills collection are installed and a task is about to begin; when a workflow stage has fired and its epistemic pair needs checking; when work is crossing to an external model, agent, or process; or when sequencing the two collections is ambiguous. Not for single-collection routing or trivial, fully-held-context work."
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
| any stage (a premise leans on "research says…", or any scholarly-tool call) | **evidence-research** | *cross-cutting* — reception-check the literature before the premise bears load |
| brainstorming approval / writing-plans (irreversible or one-way-door design) | **gauntlet** | *at approval* — after the design doc is written and committed (brainstorming step 6), before writing-plans is invoked; freeze the committed design doc as the gauntlet subject |
| persistent or long-horizon goal-mode runs (explicit goal-authoring intent only — plan execution alone is not intent) | **write-goal** | *before* persistent execution — bind the outcome to proof and stop rules |
| subagent-driven-development / dispatching-parallel-agents (first dispatch) | **blindspot-pass** | *before* the first dispatch — recon the territory before a wrong premise multiplies across isolated agents |
| external delegation / model handoff | **outsource** | *before* sending — commit a context-complete GitHub packet and emit only its short pointer; returned relay claims are re-verified by the origin |
| test-driven-development / implementation | (none mandatory) | epistemic disciplines fire only on their own triggers; clean implementation needs no ceremony |
| systematic-debugging (fix rests on a complexity or correctness claim) | **applying-formal-rigor** | *inside* — "this is O(n log n) now" and "this can't race" are derived, not asserted |
| verification-before-completion (UI-facing surface) | **evidence-locked-uat** | *is* that skill's UI-facing instance — blinded verifier, never self-certification |
| finishing-a-development-branch (irreversible / high-blast-radius change) | **gauntlet** | *pre-merge* — after the user selects merge or push+PR (finishing-a-development-branch Step 5), before the merge/push executes |
| receiving-code-review (feedback asserts a design claim or proposes an alternative) | **applying-formal-rigor** | *inside* — derive the claim from named theory before implementing it or pushing back on it |
| any workflow stage not listed above | *(none mandatory)* | disciplines still fire on their own standalone triggers — e.g. gauntlet's own trigger, not helix, governs a code-review approval |

Positions mean exactly what they say: *before* = the epistemic output is an
input to the stage; *inside* = the stage pauses at the decision point, runs
the discipline, and resumes with its verdict; *at approval* / *pre-merge* =
the stage's exit gate; *cross-cutting* = called at the moment a qualifying
premise appears, at any stage; *is* = the workflow stage and the discipline
are the same act for that surface — running the stage under that surface
condition means running the discipline.

The cross-cutting epistemic-flexibility controls do not add rows to this table. They are
checked **inside the existing pair** that consumes them: claim/source separation in recon
and resumption; priority/proxy separation in goal authoring; preregistration in formal
claims and UAT; failure chains when a recurring correction is persisted; closure control
wherever evidence remains insufficient.

## Co-fire checklist

When a strand fires, check its pair — in both directions. Make the check auditable: emit one
line per pairing row whose stage fired, in the form `helix-check: <stage> → <pair> →
fired|skipped(<reason>)` — at each stage boundary *and* at the moment a cross-cutting
trigger appears. Stages whose row is "(none mandatory)" emit no line — the map row itself
is the record.

- **A workflow stage just fired.** Ask: does its epistemic pair's own trigger
  match right now? If yes, run it in its position. If no, skip it **and say
  you skipped it** — an unfired pair is a stated decision, not an omission.
- **brainstorming is starting** → did blindspot-pass run, or was its trigger
  absent (its skip gate passed — the gate is defined in blindspot-pass, not here)?
- **a design choice is being argued** → is "better / cleaner / faster" being
  asserted? That is applying-formal-rigor's trigger.
- **a plan is about to be approved** → is anything in it irreversible? That
  is gauntlet's trigger, now — before effort is spent building on it.
- **a persistent goal is being created** → only on explicit goal-authoring
  intent does write-goal fire; length of task alone is not intent. The goal contract
  separates the operator-authorized priority from its success proxy and names proxy failure.
- **a fix rests on a complexity or correctness claim** → "this is O(n log n)
  now" / "this can't race" is applying-formal-rigor's trigger inside
  systematic-debugging.
- **subagents are about to be dispatched** → did blindspot-pass run on the
  brief being fanned out, or did its skip gate pass? A wrong premise in the
  dispatch is copied into every isolated context.
- **work is crossing to an external model, agent, or process** → run `outsource` before the
  operator sends anything; the packet must pass context erasure and exist at the pinned GitHub
  commit, and every returned relay re-enters through the repository.
- **an empirical test is about to run** → record the belief, prediction, and
  disconfirming observation before the result exists; the consuming epistemic skill owns
  that preregistration.
- **"it's done" is about to be claimed** → verification-before-completion is
  the stage; if the surface is UI-facing, the stage *is* evidence-locked-uat.
- **a recurring failure was just corrected** → decision-ledger persists the correction;
  recurrence risk requires the earliest interruptible link, replacement behavior, and a
  rehearsal fixture.
- **evidence is insufficient at a boundary** → choose hold, escalate, or a reversible
  probe; do not continue reasoning merely to manufacture `proceed`.
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
  planning step, an implementation step, an external-handoff step, a debugging step, and a "done?"
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
| "A short prompt is enough for an external model" | Only after `outsource` makes the repository packet complete, pushed, and reachable. Shortness belongs in the pointer, not the context. |
| "I basically already did this informally" | Informal ≠ the discipline. If the trigger matches, run the actual skill; "I already thought about it" is how recon-after-design smuggles itself back in. |

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the pairings to the local environment (which harness auto-fires which
stage, local workflow-layer names, fleet-specific gates). An overlay may add
bindings; it never overrides the pairing map.
