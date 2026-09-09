> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released Write Goal source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/write-goal/SKILL.md)
>
> **v4.0.0 note:** write-goal remains one of the eleven v4.0.0 skills, but sibling names this v3.0.0 guide references were consolidated at v4.0.0 (2026-08-04): blindspot-pass → [recon](Skill-Recon)'s brief mode; applying-formal-rigor and evidence-research → [resolve](Skill-Resolve)'s derivation and literature instruments; continuity-verify → [decision-ledger](Skill-Decision-Ledger)'s resume mode (the mode name survives). See the [Skill Catalog](Skill-Catalog) for the full mapping; the tagged v4.0.0 sources are the sole contract.

# Write Goal

## What it does

Write Goal turns explicit goal-authoring intent into a completion contract another agent can execute without silently changing the target or declaring victory on an easy proxy. It separates the authorized priority from progress signals, requires direct completion evidence and anti-gaming guards, and preserves boundaries, blocker policy, stop conditions, and user interrupt authority.

It drafts and, with explicit consent, may start a persistent goal. It does not execute the work, judge the result, or certify completion.

## Use it when

- The user explicitly asks to create, define, refine, write, or start a goal.
- The user asks what would count as done or requests a durable objective, proof standard, scope boundary, blocker policy, stop rule, or optional budget.
- The user explicitly asks to define a persistent completion contract for extended work before execution.

Classify the goal as `performance` when the path and outcome are sufficiently understood, `learning-first` when investigation must unlock a later performance goal, or `not goal-ready` when materially different outcomes remain unresolved.

## Do not use it when

- The user simply asks to fix, build, inspect, or explain something; ordinary tasks do not imply permission to create a persistent goal.
- You want to hide an ordinary deliverable behind open-ended research.
- You want to force a performance target onto genuinely uncertain exploration.
- You intend to start a goal before explicit start/create intent or approval.
- You intend to weaken the completion contract to fit a host tool.

## Inputs and prerequisites

Inputs are explicit user intent, de-risked context, relevant evidence or design artifacts, and the runtime's current goal state. If an unfinished goal may exist, inspect it before proposing replacement.

Identify the observable end state, intended observer, protected state, authorized priority, success proxy, a concrete proxy failure, acceptable cost, proof sources, canonical identities and environments, uncertainty, authority boundaries, and the runtime's real blocked semantics. Set a token budget only when the user explicitly requests one.

## Normal workflow

1. Classify the goal type. Ask the smallest blocking question only if the objective is not goal-ready.
2. Draft the completion contract in executable language: end state, protected state, goal controls, proof bundle, boundaries, execution loop or queue, uncertainty and blocker policy, and stop/interrupt rule.
3. Require all three proof layers: primary proof, integrity guards, and scope/provenance proof. State why a layer is not applicable rather than silently omitting it.
4. Check proxy resistance: could every word be satisfied while missing the real intent? Could the metric improve while the protected outcome worsens?
5. Present the draft for approval whenever any material field was inferred. Skip review only when the user's request already states the end state, proof bundle, boundaries, and stop rule verbatim.
6. Start the goal only after explicit activation intent. Preserve the entire approved contract in the host objective. If no persistent-goal primitive exists, return the approved contract without pretending it was started.

Queue-shaped goals additionally define discovery, per-item processing, recording, retries, and exhaustion. Learning-first goals name the decision they unlock, the evidence threshold, and the conversion to an approved performance goal or bounded no-decision result.

## Outputs and durable artifacts

The normal output is an approved completion contract. When activation is authorized and supported, the second output is the runtime's persistent goal carrying that contract unchanged. When activation is unsupported, the contract itself is the honest final artifact; no started-goal claim is made.

The contract records direct proof, anti-proxy integrity, provenance, scope, protected state, blocker semantics, and user interruptibility. Completion is not authorized by activity, a plan, budget exhaustion, or one convenient metric.

## Boundaries and failure modes

- Drafting and activation are separate state changes.
- “Tests pass,” “file exists,” or “deployment green” is insufficient when it does not establish behavior, canonical provenance, and anti-spoof guards.
- Difficulty, uncertainty, elapsed time, and low budget do not prove complete or blocked.
- A fallback never silently narrows the proof bundle; re-check the original contract.
- Existing active goals must not be replaced silently.
- The skill hands execution to the runtime and later verification to the appropriate independent gate.

## Example prompts

- “Write a performance goal for eliminating unexplained nightly backup failures. Preserve retention policy and define proof that cannot be satisfied by manual retries.”
- “Define a learning-first goal that distinguishes two editor architectures, records counterevidence, and ends by converting the result into an approved implementation goal.”
- “Draft what done means for this release, but do not create the persistent goal until I approve the contract.”

## Related skills and handoffs

- [Blindspot Pass](Skill-Blindspot-Pass), [Applying Formal Rigor](Skill-Applying-Formal-Rigor), and [Evidence Research](Skill-Evidence-Research) can de-risk inputs before the goal is written.
- [Continuity Verify](Skill-Continuity-Verify) re-anchors active-goal state on resumption.
- [Decision Ledger](Skill-Decision-Ledger) may reuse an adequate goal contract instead of duplicating it.
- [Evidence-Locked UAT](Skill-Evidence-Locked-UAT) independently tests material UI-facing completion; [Gauntlet](Skill-Gauntlet) may gate irreversible commitments.
- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) routes explicit goal-authoring after intent is de-risked.

## Canonical sources and evidence

- [Write Goal source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/write-goal/SKILL.md)
- [Evidence basis and limits at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/write-goal/reference/evidence-basis.md)
- [Router handoff contract at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md)
