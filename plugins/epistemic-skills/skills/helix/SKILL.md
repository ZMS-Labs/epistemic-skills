---
name: helix
description: "Use when both a workflow-skill layer (such as superpowers) and the epistemic-skills collection are installed, the task has not cleared the routine-work fast path, and a workflow stage has a positive epistemic pairing trigger; when a resumed workflow depends on summary, handoff, or remembered state; when work is crossing to an external model, agent, or process; or when sequencing the two collections is ambiguous. Not for single-collection routing, fresh routine reversible work, or emitting inventories of absent pairs."
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
remain the routers; read every skill this map pairs you to.

## Entry order: resumption, then routine path

A resumed task is not yet eligible for the routine fast path when its next
action depends on a compaction summary, handoff note, or remembered prior-session
state. Run **continuity-verify first**, before routine-path classification or any
resumed workflow stage. Its live state digest feeds `using-epistemic-skills`,
which then applies the routine gate and routes the verified task. When unfamiliar
territory also has a positive reconnaissance trigger, the order is
**continuity-verify → blindspot-pass**; continuity verifies remembered state,
then recon maps the present territory.

For a fresh task, or after the resumption digest exists, apply
`using-epistemic-skills/reference/routine-fast-path.md` before ordinary pairing.
A reversible, local, directly checkable, non-precedential task proceeds through
ordinary workflow with no epistemic pair, no `helix-check` line, and no process-
only artifact. Unfamiliar routine-looking work gets the two-read micro-recon;
unfamiliarity alone is not a positive pairing trigger.

## The governing rule

Once a positive pairing trigger exists, **the epistemic member fires first,
then the workflow member carries the stage out.** The epistemic skill decides
whether you are solving the right problem, with real evidence, before effort is
spent; the workflow skill then structures the effort. Never run a workflow
stage first and bolt its required epistemic pair on afterward — recon after
design is archaeology, and evidence after the verdict is rationalization.

This rule does not require proving the absence of every other pair. Non-events
are silent.

## The pairing map

| Workflow stage | Epistemic pair | Position |
|---|---|---|
| session start/resumption whose next action depends on summary, handoff, or remembered state | **continuity-verify** | *pre-arc* — before routine-path classification and every resumed workflow stage; its digest feeds the epistemic router |
| task start after routine micro-recon reveals a material map/territory mismatch, unresolved hidden coupling, or costly fan-out risk | **blindspot-pass** | *before* brainstorming — full recon the territory, then design |
| brainstorming (a material ≥2-option design choice) | **applying-formal-rigor** | *inside* — the choice is derived from named theory, not asserted |
| any stage (a premise leans on "research says…", or any scholarly-tool call) | **evidence-research** | *cross-cutting* — reception-check the literature before the premise bears load |
| brainstorming approval / writing-plans (per gauntlet's own positive trigger list) | **gauntlet** | *at approval* — after the design doc is written and committed, before writing-plans is invoked; freeze the committed design doc as the gauntlet subject |
| persistent or long-horizon goal-mode runs (explicit goal-authoring intent only — plan execution alone is not intent) | **write-goal** | *before* persistent execution — bind the outcome to proof and stop rules |
| subagent-driven-development / dispatching-parallel-agents (first material dispatch) | **blindspot-pass** | *before* the first dispatch — recon when a wrong premise could multiply across isolated agents |
| external delegation / model handoff | **outsource** | *before* sending — commit a context-complete GitHub packet and emit only its short pointer; returned relay claims are re-verified by the origin |
| test-driven-development / implementation | (none mandatory) | epistemic disciplines fire only on their own positive triggers; clean implementation needs no ceremony |
| implementation of an interface another agent will consume (tool/function schema, MCP surface, structured-output or dispatch contract) | **agent-interface-design** | *inside* the build — constraints move into structure, examples pass the example-lint, and the cold-consumer test gates the interface before it ships |
| writing-skills / instruction-layer maintenance (explicit audit request, a detected cross-layer instruction conflict, or a model-generation upgrade) | **context-audit** | *outside the per-task arc* — audit the assembled instruction context as one set; report before apply, one version-controlled commit per cut class |
| writing-plans (the effort is large and material decisions are still unresolved) | **wayfinding** | *before* planning — decompose by decisions, resolve the frontier, and plan only fog-free regions; tickets minted from fog are the failure the pairing prevents |
| brainstorming (a live option is cheaper to build thin than to keep debating) | **throwaway-prototyping** | *inside* — instantiate the option as a disposable probe under the four-clause contract; the answer returns to the design dialogue, the code does not |
| any stage, immediately after a consequential decision, load-bearing assumption, or recurrent/operator correction (per decision-ledger's own positive and no-op gates) | **decision-ledger** | *retrospective cross-cutting* — reuse an adequate durable artifact or append only the uncovered persistence gap; never log before the moment exists |
| finishing-a-development-branch / any merge or rebase with non-trivial conflicts | **intent-traced-merge** | *at integration* — resolve hunks by tracing both origins, verify against both sides' motivating checks, record rulings in the merge commit |
| receiving-code-review (acceptance about to be signed on a change the acceptor has not restated) | **evidence-locked-uat** acceptor comprehension gate | *at acceptance* — the acceptor states what changed and what breaks first if it's wrong, or the state is recorded `ACCEPTED-UNREVIEWED`, never silently upgraded |
| systematic-debugging (fix rests on a complexity or correctness claim) | **applying-formal-rigor** | *inside* — "this is O(n log n) now" and "this can't race" are derived, not asserted |
| verification-before-completion (material UI-facing acceptance surface) | **evidence-locked-uat** | *is* that skill's UI-facing instance — blinded verifier, never self-certification; routine directly checkable presentation changes use the bounded check instead of a full packet |
| finishing-a-development-branch (per gauntlet's own positive trigger list) | **gauntlet** | *pre-merge* — after the user selects merge or push+PR, before the merge/push executes |
| receiving-code-review (feedback asserts a material design claim or proposes an alternative) | **applying-formal-rigor** | *inside* — derive the claim from named theory before implementing it or pushing back on it |
| any gated stage outside active design dialogue (per open-questions' member-authoritative trigger) | **open-questions** | *before* the gated stage — explicit invocation uses full-exhaustion mode; the narrow automatic trigger uses fork-scoped mode; while a design skill is running, that skill owns its own questioning |
| any workflow stage not listed above | *(none mandatory)* | disciplines still fire on their own standalone positive triggers — the member skill, not helix, remains authoritative |

Positions mean exactly what they say: *pre-arc* = before the routine gate and
any resumed-work stage; *before* = the epistemic output is an input to the
stage; *inside* = the stage pauses at the decision point, runs the discipline,
and resumes with its verdict; *retrospective cross-cutting* = the discipline
fires immediately after the qualifying moment, never as a prerequisite;
*at approval* / *pre-merge* = the stage's exit gate; *cross-cutting* = called
at the moment a qualifying premise appears, at any stage; *is* = the workflow
stage and the discipline are the same act for that surface — running the stage
under that surface condition means running the discipline.

## Composition contract: route the whole set

The machine-checkable registry at
[`reference/composition-contract.json`](reference/composition-contract.json)
classifies every packaged discipline by composition moment and position without
copying its member trigger. **The member skill owns its trigger.**
`using-epistemic-skills` selects the complete **zero, one, or ordered set** of
positive epistemic fires; Helix positions that whole set around the workflow
stage and carries order custody. A table row is never permission to choose one
pair and discard another positive member trigger.

When multiple disciplines fire, follow the router's arc and the registry's
context-bound order rules. The most important combined paths are:

- `continuity-verify → blindspot-pass` when resumed state and unfamiliar
  territory both bear load;
- formal rigor names an empirical premise, evidence research qualifies it,
  then formal rigor closes the derivation;
- `intent-traced-merge → gauntlet` when a high-risk branch first needs semantic
  conflict resolution and then a frozen pre-merge verdict; and
- `gauntlet → evidence-locked-uat` when the same change needs both a high-risk
  gate and material UI proof.

The registry is a composition contract, not a second trigger table. If its
classification and a member skill ever appear to conflict, the member owns
whether it fires; the router owns the full selected set; Helix owns only where
that set sits relative to workflow execution.

The cross-cutting epistemic-flexibility controls do not add rows to the pairing
table or registry. They are checked **inside the existing pair** that consumes
them: claim/source separation in recon and resumption; priority/proxy separation
in goal authoring; preregistration in formal claims and UAT; failure chains when
a recurring correction is persisted; closure control wherever evidence remains
insufficient.

## Co-fire record

When a positive pair fires, emit:

`helix-check: <stage> → <pair> → fired(<artifact-ref>)`

When an authorized operator explicitly overrides a positive trigger, emit:

`helix-check: <stage> → <pair> → overridden(<authority-ref>: <bounded reason>)`

Do **not** emit a line for an absent trigger, a `(none mandatory)` row, or a task
that cleared the fresh routine path. The member skill's own output is the record
for a single fired pair; `helix-check` carries stage-order custody where that
relationship matters.

- **A resumed workflow depends on remembered state.** Run continuity-verify
  before the routine gate or any resumed workflow skill. If recon also fires,
  record both artifacts in `continuity-verify → blindspot-pass` order.
- **A workflow stage has a positive epistemic trigger.** Run the member in its
  position and reference its output. Do not re-implement or soften the member's
  trigger here.
- **More than one epistemic member has a positive trigger.** Ask the epistemic
  router for the complete ordered set; do not select a single favorite pair.
- **brainstorming is starting after routine micro-recon exposed a mismatch** →
  run blindspot-pass before design.
- **a material design choice is being argued** → applying-formal-rigor owns the
  derivation.
- **a plan is about to be approved** → use gauntlet's own trigger list; do not
  narrow it to one adjective.
- **a persistent goal is being created** → only explicit goal-authoring intent
  fires write-goal; task length alone is not intent.
- **a fix rests on a complexity or correctness claim** → applying-formal-rigor
  fires inside systematic-debugging.
- **subagents are about to receive a material fuzzy brief** → blindspot-pass
  runs before fan-out. A local bounded dispatch whose target and check are
  already explicit does not need a report merely because another agent exists.
- **work crosses to an external model, agent, or process** → run `outsource`
  before sending; the packet must exist at a target-readable immutable ref, and
  every return relay re-enters through the repository.
- **an empirical test is about to run** → record the belief, prediction, and
  disconfirming observation before the result exists; the consuming epistemic
  skill owns that preregistration.
- **a material UI acceptance claim is about to be made** → the stage is
  evidence-locked-uat. A routine directly checkable presentation edit records
  its bounded preview/test result without constructing the full UAT container.
- **a consequential decision, load-bearing assumption, or recurrent/operator
  correction was just made and future work will rely on it** → decision-ledger
  reuses the existing durable record when adequate or persists only the gap.
- **evidence is insufficient at a load-bearing boundary** → choose hold,
  escalate, or a reversible probe; do not continue reasoning merely to
  manufacture `proceed`.
- **a branch is about to merge** → use gauntlet's own trigger list; the member
  gate, not Helix shorthand, decides.
- **open-questions fires** → preserve its **explicit full-exhaustion mode and
  automatic fork-scoped mode**. Blindspot-pass's Questions section may seed the
  ledger, but its presence alone never fires an interview; while active design
  dialogue owns questioning, open-questions defers.
- **An epistemic discipline fired standalone.** Ask which workflow stage
  consumes its output. An epistemic output no workflow stage consumes is a
  report no one reads.

Fire-nothing is a valid outcome. A fresh routine task pairs zero disciplines
with zero ceremony and emits no proof that it did so.

Collection is downstream of the paired stage, never a prerequisite for it. Eligible paired-stage
events use the shared epistemic data collection map; adapter absence or failure cannot change
either strand's result.

## Any harness, any layer

This file is plain markdown and assumes no harness. "Read/load the skill"
means whatever your harness does — description-triggered skill loading,
a context-file include, or pasting the file into the loop.

- **If your harness auto-triggers by description** (Claude Code, Cursor,
  Codex): the entry-order rule prevents both layers from turning fresh task
  start into ceremony while still making resumption verification pre-arc.
- **If your harness loads one context file** (Gemini CLI via GEMINI.md, or
  similar): the collection's context file names Helix as the tandem entry
  point; apply resumption verification first, then the routine gate and map.
- **If nothing auto-triggers**: the path in is `using-epistemic-skills`,
  which points here whenever a workflow layer and a positive pair are present.
- **If your workflow layer is not superpowers** (Kimi, agy, a house style,
  or beyond): map the stage names — every layer has a design step, a planning
  step, an implementation step, an external-handoff step, a debugging step,
  and a "done?" step; bind them to your layer's equivalents without inventing
  skip records.

## Anti-patterns

| Thought | Reality |
|---|---|
| "Both layers are installed — check every pair at every stage" | Ceremony. Resumption state, the routine gate, and positive member triggers govern; absent pairs are silent. |
| "The routine gate comes before continuity verification" | Not on resumption. You cannot classify remembered work as routine until the load-bearing state is re-anchored. |
| "The table gave me one pair, so I can ignore the other positive triggers" | The router selects the complete ordered set; Helix positions every member that actually fires. |
| "I'll emit skipped lines so reviewers know I was rigorous" | A skip inventory is process as proxy. Record fired pairs and authorized overrides only. |
| "I'll do the workflow stage first and add the epistemic check after" | Backwards when a positive pair exists. Recon after design is archaeology. |
| "Helix told me which skill; I know roughly what it does" | Helix only pairs. Read the paired skill; the discipline lives there. |
| "This replaces the two routers" | It sits between them. Member-level routing stays in `using-superpowers` and `using-epistemic-skills`. |
| "Superpowers isn't installed, so none of this applies" | The pairings are stage-shaped. Map them to whatever workflow steps the session actually has. |
| "A short prompt is enough for an external model" | Only after `outsource` makes the repository packet complete, pushed, and reachable. Shortness belongs in the pointer, not the context. |
| "I basically already did the triggered discipline informally" | Informal is not the discipline when its positive trigger is present. This does not turn routine non-events into formal invocations. |

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the pairings to the local environment (which harness auto-fires which
stage, local workflow-layer names, fleet-specific gates). An overlay may add
bindings; it never overrides the pairing map, the composition contract, or
require absent-trigger records.
