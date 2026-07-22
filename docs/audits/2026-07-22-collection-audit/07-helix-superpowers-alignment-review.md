# Audit 07 — helix ↔ superpowers alignment review

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at 61fbf95 (v2.6.0). Read in full: helix SKILL.md (120 lines), the approved helix design spec, the epistemic router, all 14 superpowers skills, and the four epistemic member skills whose triggers helix touches. The approved design constraint: improve pairing PRECISION, never add coupling surface. No merged trigger tables, no duplicating either router's content.

---

## 1. Pairing-map coverage

**F1 — GAP: multi-agent fan-out stages are unpaired despite blindspot-pass's own trigger naming exactly that moment.** `blindspot-pass/SKILL.md:50-52` lists as a trigger "before a multi-agent fan-out where a wrong premise multiplies across agents." `subagent-driven-development/SKILL.md:8` is precisely that (fresh implementer subagent per task, plus reviewer subagents), and `dispatching-parallel-agents/SKILL.md:68-77` is fan-out in its purest form. Neither appears in the helix map (`helix/SKILL.md:35-46`); they fall into the catch-all row at line 46, which relies on disciplines self-firing — exactly the "co-firing is not automatic" failure the design doc (`2026-07-20-helix-design.md:12-15`) says helix exists to kill. Fan-out is the highest-leverage blindspot-pass moment: a wrong premise in the controller's brief is copied into N isolated contexts that cannot correct each other. SDD even has a natural consumption point — the Pre-Flight Plan Review (`subagent-driven-development/SKILL.md:85-97`). This is a missed pairing, and adding one row to the existing map is precision inside the single coupling point, not new coupling surface.

**F2 — GAP (weak, judgment call): receiving-code-review has a real formal-rigor moment; requesting-code-review is correctly unpaired.** `applying-formal-rigor/SKILL.md:21` explicitly scopes itself to "Reviewing someone else's design rationale for rigor — use the Red Flags list below as the review checklist." `receiving-code-review/SKILL.md:16-25` (READ → UNDERSTAND → VERIFY → EVALUATE) is that moment: review feedback frequently asserts "this is cleaner/better" or proposes an alternative design — a ≥2-option decision being argued. The catch-all covers it only if the agent spontaneously recognizes the trigger mid-feedback. A conditional row would make it precise. `requesting-code-review` is correctly unpaired: its independence discipline (fresh context, never session history, `requesting-code-review/SKILL.md:8`) is already built in, and gauntlet explicitly excludes ordinary code review (`gauntlet/SKILL.md:3`, `:52`).

**F3 — STRENGTH: the other unpaired stages are correctly unpaired.** `using-git-worktrees` is mechanical workspace setup with no decision point (its one judgment call — native tool vs git fallback — is resolved by detection, not theory). `writing-skills` embeds its own evidence discipline stronger than any generic pair: baseline-vs-skill RED/GREEN with a no-guidance control and 5+ reps (`writing-skills/SKILL.md:577-585`); formal-rigor would be weaker than what the stage already mandates. `test-driven-development`'s "(none mandatory)" row (`helix/SKILL.md:42`) matches TDD's self-contained iron law. `using-superpowers` is the router helix explicitly defers to.

**F4 — DEFECT (minor): executing-plans is missing from helix's frontmatter description.** `helix/SKILL.md:3` enumerates the stages "its epistemic pair needs checking" for as "brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, finishing-a-development-branch" — omitting executing-plans, which the map pairs with write-goal at line 41. In a description-triggered harness (Kimi included), the description is the discovery surface; the omission weakens firing exactly at the write-goal boundary.

## 2. Position precision

**F5 — DEFECT: gauntlet "at approval" is ambiguous between brainstorming's two approval gates.** `helix/SKILL.md:40` says "*at approval* — freeze the design as the subject." Brainstorming has two approval moments: the in-dialogue "User approves design?" gate (`brainstorming/SKILL.md:28`, step 5) and the written-spec review (step 8, `brainstorming/SKILL.md:31`). Gauntlet requires a *frozen* subject — "If the subject moves, restart" (`gauntlet/SKILL.md:137-138`) — which only exists after the design doc is written and committed (brainstorming step 6). Two agents will execute this row differently: one gauntlets the conversational design (subject still moving), one waits for the committed spec. The position is not executable-identical across agents.

**F6 — DEFECT: "pre-merge" doesn't say which side of the user's option choice.** `helix/SKILL.md:45` gates "the merge," but `finishing-a-development-branch/SKILL.md:66-79` presents 4 options, only two of which (local merge, push+PR) reach an irreversible point. Gating before Step 4 wastes a gauntlet run when the user picks "keep as-is" or "discard"; gating after the choice is the executable reading but is not stated.

**F7 — DEFECT (minor): "*is*" is an undefined sixth position.** The legend (`helix/SKILL.md:48-52`) defines *before / inside / at approval / pre-merge / cross-cutting* and says "Positions mean exactly what they say," but the UAT row (`helix/SKILL.md:44`) uses "*is* that skill's UI-facing instance." Identity is not in the legend's vocabulary.

**F8 — DEFECT (minor): the evidence-research row's stage binding contradicts its position.** `helix/SKILL.md:39` binds the row to the brainstorming stage but marks it *cross-cutting*, defined at line 51-52 as "at the moment a qualifying premise appears, at any stage." Worse, evidence-research's own trigger is far broader than premises-in-brainstorming: "immediately before ANY Consensus, Scite, or Zotero/library-substrate tool call (mandatory prerequisite)" (`evidence-research/SKILL.md:3`). An agent reading the stage column literally will under-fire. The systematic-debugging/formal-rigor row (`helix/SKILL.md:43`) is by contrast precise — "inside" with named claim shapes; naming the phase (Phase 3 Hypothesis / Phase 4 Implementation, `systematic-debugging/SKILL.md:145-198`) would make it exact, but it's executable as-is.

## 3. Co-fire checklist

**F9 — GAP: the checklist omits the systematic-debugging pair.** The map pairs systematic-debugging → applying-formal-rigor (`helix/SKILL.md:43`), but the checklist prompts (`helix/SKILL.md:62-73`) cover brainstorming, design choice, plan approval, persistent goal, done-claim, and merge — no debugging prompt. The checklist is the automaticity mechanism per the design doc (`2026-07-20-helix-design.md:64-71`); a paired stage with no prompt won't co-fire reliably.

**F10 — DEFECT: the audit-line protocol is unanswerable for unpaired stages and cross-cutting fires.** `helix/SKILL.md:56-57` mandates "at each stage boundary, emit one line in the form `helix-check: <stage> → <pair> → fired|skipped(<reason>)`." Two holes: (a) TDD/implementation has pair "(none mandatory)" — the format has no defined value for `<pair>` there, so an auditor can't tell a correctly-skipped unpaired stage from a forgotten check; (b) cross-cutting fires (evidence-research) don't happen at stage boundaries, so "at each stage boundary" never instructs emitting their line.

**F11 — DEFECT: the blindspot-pass skip reason invites a vibe where the member skill defines an observable gate.** `helix/SKILL.md:62-63` allows skip when "its trigger [was] absent (territory already fully held in context)" — self-assessed. blindspot-pass defines a checkable skip gate: name ≥2 concrete landmines (file:line) and the canonical example from memory (`blindspot-pass/SKILL.md:56-59`). The checklist should point at that gate rather than paraphrase "held in context," or the skip reason is not auditable from observable state. Every other checklist prompt (irreversibility in plan text, UI-facing surface, explicit goal intent) *is* observable.

## 4. Harness-portability claim (tested against Kimi Code)

**F12 — GAP: the write-goal pairing survives, but its stage anchor doesn't fit this harness.** Kimi Code has a native goal system (CreateGoal / goal mode), and write-goal already ships a Kimi adapter (`write-goal/SKILL.md:151-155`) — so the pairing itself holds. But helix anchors it to "executing-plans / persistent or long-horizon runs" (`helix/SKILL.md:41`). In Kimi, executing-plans is *not* the persistent-goal path — it's a same-session batch executor with checkpoints (`executing-plans/SKILL.md:3`). Anchoring write-goal to executing-plans both misleads (plan execution is not goal-authoring intent — write-goal's own consent rule, `write-goal/SKILL.md:28-30`) and misses the actual Kimi surface (a native goal-mode run). The parenthetical "explicit goal intent only" carries all the weight; the stage name carries noise.

**F13 — GAP: Kimi primitives with no epistemic pairing anywhere — cron and native subagents.** Kimi's cron/scheduled-task primitive creates recurring autonomous runs: persistent, proxy-optimization-prone, exactly write-goal-shaped (end state, proof bundle, stop rule) — but write-goal's trigger requires "explicit goal-authoring intent" and its adapters cover Codex `create_goal` and Kimi `CreateGoal` only, not scheduled jobs. Kimi's native subagent dispatch maps cleanly onto dispatching-parallel-agents/subagent-driven-development, which loops back to F1. Kimi's built-in skills (`update-config`, `check-kimi-code-docs`) are config/docs utilities with no workflow-stage shape — correctly nothing to pair.

**F14 — STRENGTH: the "map the stage names" claim (helix/SKILL.md:97-102) is otherwise sound for Kimi.** Superpowers is installed here as a managed plugin, so the superpowers stage names are literally present; absent it, Kimi's plan mode is the design/plan step, subagent dispatch is the fan-out step, and "run the verification, then claim" maps to verification-before-completion. The example mapping at lines 100-102 (plan→build→verify) is executable as written.

## 5. Duplicated-check surface between helix and the routers

**F15 — STRENGTH (with one accepted risk): helix does not restate trigger tables.** The map's position glosses ("reception-check the literature," "bind the outcome to proof and stop rules") are one-line pointers, not content copies; the catch-all row (`helix/SKILL.md:46`) attributes code-review gating to "gauntlet's own trigger" by reference rather than restating it. The router's restatement of the governing rule (`using-epistemic-skills/SKILL.md:96-102`) is explicitly sanctioned by the design doc (`2026-07-20-helix-design.md:46-48`). The one accepted risk: the checklist quotes trigger fragments that will rot if the member skills retune — "better / cleaner / faster" (`helix/SKILL.md:64` vs `applying-formal-rigor/SKILL.md:3,19`) and "length of task alone is not intent" (`helix/SKILL.md:69` vs `write-goal/SKILL.md:28-30`). These wordings are prescribed by the approved design (lines 66-69), so they're sanctioned duplication, not a defect — but F11's fix (point to the member skill's gate rather than paraphrase it) is the right pattern to apply when these phrases next drift.

---

## Minimal edit proposals (each one focused PR)

**PR-1 (F1, F9 partial): pair the fan-out stages.** Add one row to the map after the executing-plans row:

```
| subagent-driven-development / dispatching-parallel-agents (first dispatch) | **blindspot-pass** | *before* the first dispatch — recon the territory before a wrong premise multiplies across isolated agents |
```

And one checklist line after the brainstorming prompt (`helix/SKILL.md:63`):

```
- **subagents are about to be dispatched** → did blindspot-pass run on the
  brief being fanned out, or did its skip gate pass? A wrong premise in the
  dispatch is copied into every isolated context.
```

**PR-2 (F5, F6): pin the two gauntlet positions to executable moments.** Replace `helix/SKILL.md:40` position cell with:

```
*at approval* — after the design doc is written and committed (brainstorming step 6), before writing-plans is invoked; freeze the committed design doc as the gauntlet subject
```

Replace `helix/SKILL.md:45` position cell with:

```
*pre-merge* — after the user selects merge or push+PR (finishing-a-development-branch Step 5), before the merge/push executes
```

**PR-3 (F2): conditional formal-rigor row for receiving-code-review.** Add one row:

```
| receiving-code-review (feedback asserts a design claim or proposes an alternative) | **applying-formal-rigor** | *inside* — derive the claim from named theory before implementing it or pushing back on it |
```

**PR-4 (F12): re-anchor the write-goal row to intent, not plan execution.** Replace the stage cell at `helix/SKILL.md:41` with:

```
persistent or long-horizon goal-mode runs (explicit goal-authoring intent only — plan execution alone is not intent)
```

(This drops `executing-plans` from the stage cell; executing-plans then falls under the catch-all row, which is correct — it has no mandatory pair.)

**PR-5 (F9, F10, F11): checklist completeness + audit-line spec.** Three small edits in the Co-fire checklist section:
1. Add a debugging prompt: `- **a fix rests on a complexity or correctness claim** → "this is O(n log n) now" / "this can't race" is applying-formal-rigor's trigger inside systematic-debugging.`
2. Amend line 56-57 to: `at each stage boundary (and at the moment a cross-cutting trigger appears), emit one line per pairing row whose stage fired, in the form ` + backticked format + `; stages whose row is "(none mandatory)" emit no line — the map row itself is the record.`
3. Amend line 63's parenthetical from `(territory already fully held in context)?` to `(its skip gate passed — the gate is defined in blindspot-pass, not here)?`

**PR-6 (F4, F7, F8): description + legend hygiene.** (a) Add `executing-plans` to the stage list in the frontmatter description (`helix/SKILL.md:3`). (b) Add to the position legend (after line 52): `*is* = the workflow stage and the discipline are the same act for that surface — running the stage under that surface condition means running the discipline.` (c) Change the stage cell at line 39 from `brainstorming (a premise leans on "research says…")` to `any stage (a premise leans on "research says…", or any scholarly-tool call)`.

**Not proposed:** any cron/write-goal adapter (F13) — that's a write-goal member-skill change (a new host-adapter section), not a helix pairing-map change, and belongs in a separate piece of work scoped to that skill. Also not proposed: any change to the router, any merged trigger content, or any second coupling point — none of the findings require one.

**Residual ambiguity for the operator:** F2 and F3's writing-skills call are judgment calls. Requesting-code-review classified as correctly unpaired because its independence discipline is internal and gauntlet explicitly excludes ordinary review; if the operator wants helix to surface the *verification-before-completion delegation pattern* ("agent said success → check the diff") at the review stage, that would be a fourth row — but verification-before-completion fires on its own trigger there, so it was judged catch-all-covered.
