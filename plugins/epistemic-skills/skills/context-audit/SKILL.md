---
name: context-audit
description: 'Use when auditing the instruction context an agent actually receives — on explicit request ("audit my context/CLAUDE.md/system prompt", "context audit", "prune my instructions"), when a cross-layer instruction conflict is detected mid-task (two active layers direct incompatible behavior), or after a model-generation upgrade invalidates guardrails written for a weaker model. Do NOT fire for auditing the prose quality of one document (ordinary editing), for designing NEW tool/agent interfaces (that is interface craft doctrine, not context hygiene), for pre-work recon on a task brief (recon owns the territory; this skill audits the map), or for tuning a prompt to improve the output of one specific task (that is prompt engineering, not context hygiene).'
metadata:
  event-kinds: [audit-cut-decision]
  eligible-when: [preregistered-prediction, correction-or-supersession]
  outcome-sources: [field-observation, supersession-chain]
  collection-mode: conditional
  sentinel-fixture: audit-cut-regression.json
---

# context-audit — audit the assembled context, not a file

Every layer an agent harness loads — system prompt, project/user instruction
files, memory indexes, skill descriptions, command definitions, hook output,
tool and MCP server instructions — reaches the model as **one assembled
context**. Instructions age at different rates in different layers, so the
assembly accumulates three kinds of debt no single-file review can see:
**conflicts** between layers, **duplicates** across layers, and **dead weight**
— guardrails written for a weaker model that now only cost tokens and
reconciliation reasoning. This skill audits the assembly as the model receives
it and emits a cut list as a diff, a conflict ledger, and a falsifiable
re-baseline gate.

Historical motivation: stronger models may make some accumulated instructions
redundant; this is a hypothesis to test, not a presumption favoring deletion. Anthropic reports removing over 80% of Claude Code's
system prompt for its 2026 models with no measurable eval loss (Shihipar,
"The new rules of context engineering for Claude 5 generation models",
2026-07-24). Direction is independently supported — long, complex agentic
instruction sets measurably degrade adherence (AgentIF, arXiv:2505.16944), and
moderate prompt compression can *improve* long-context performance (Zhang et
al. 2025, "An Empirical Study on Prompt Compression for Large Language
Models") — but the magnitude is vendor-reported, unreplicated. Treat every cut as a cheap,
reversible experiment under version control, never as a proven win.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| Recon of the territory before work | recon (brief mode) | Audits the *task's* unknowns; this skill audits the *instruction map* the agent carries into every task |
| Designing the outbound channel | agent-interface-design craft doctrine in reference/craft/, not a suite skill | That doctrine shapes interfaces this agent authors for other minds; this one prunes the inbound instruction channel this agent consumes |
| Persisting what the audit decides | decision-ledger | Every applied cut class and every conflict resolution is a recorded decision with a revisit condition |
| Judging a high-stakes cut | gauntlet | Use the owner-designated review when needed for a consequential cut; audit alone grants no edit authority |

## Entry, observation and authority

Visibly acknowledge the scoped audit actually performed. Start with the
affected instruction/load/version or precedence question and reusable evidence.
Expand to interacting layers when needed; a full assembly inventory is for a
full audit, not a prerequisite to resolving one mid-task conflict. Apply the
actual instruction hierarchy immediately and continue authorized work. That
operative resolution does not authorize a persistent source edit.

Distinguish source bytes, installed copy/version/path, observed loaded
description/body, and actual application. A correct source is not proof it
loaded. Verify the consuming path before replacing a stale copy and preserve
customizations. If assembled context or load order is unavailable, state the
unobserved layers and audit only the accessible scope; never certify the unseen
assembly. Maintain sources and regenerate projections only within authority.

## Protocol

### 1. Inventory the assembly

For the selected scope, enumerate observed layers and their source/install/load
identity, precedence and versions where observable. Use hashes or token counts
when they answer the question. For full audits, inventory the accessible assembly
and explicitly name skipped or unavailable layers; do not certify unseen conflicts.

Mark **generated and governance layers** (compiled rule projections, safety
policy, consent text) as *report-only*: conflicts found there are routed
upstream to their source of truth as findings, never edited in the projection.

### 2. Classify every instruction

Cut classes:

- **CONFLICT** — contradicts an instruction in another active layer. Must cite
  both locations verbatim. Costliest class: the model spends reasoning
  reconciling its operator before the task starts.
- **DUPLICATE** — the same directive in two or more layers. Nominate an
  authoritative survivor only after verifying it is reachable and loaded
  whenever needed, including recovery and resume. Locality alone cannot
  justify deleting the only reliably loaded protection.
- **OBVIOUS** — restates strong-model default behavior: persona theater,
  restated general knowledge, emphasis scaffolding (all-caps, "CRITICAL",
  emoji-as-emphasis), generic care/quality exhortations.
- **MODEL-HANDLES-THIS-NOW** — a guardrail for an older model's failure mode
  with no documented incident behind it. This is a candidate hypothesis,
  not evidence of redundancy. Read origins and test the triggering condition;
  missing incident records do not establish that a protection is unnecessary.
- **OVER-VERIFY** — verification and self-check demands duplicated across
  layers. Vendor-reported for current frontier models (Shihipar 2026):
  explicit verification instructions cause over-verification — wasted tokens
  and reduced output quality, not more correctness. Direction untested
  outside that report; the class is still worth cutting as DUPLICATE-grade
  debt even where the over-verification effect is unconfirmed.

Keep classes — never cut, and classification into them requires reading the
cited origin, not remembering it:

- **KEEP:GOTCHA** — a documented failure mode with an incident record behind
  it. An instruction whose origin record exists may not be reclassified to a
  cut class without reading that record.
- **KEEP:OPERATOR-PREFERENCE** — genuine taste or policy the model cannot
  infer.
- **KEEP:ROUTING+THRESHOLD** — real numbers, real routing rules.
- **KEEP:NAMED-INTEGRATION** — facts about this environment: paths, services,
  hostnames, registries.
- **KEEP:GOVERNANCE** — safety, consent, and policy text. Conflicts here are
  still *reported*; the text is never cut by this skill.

### 3. Cross-layer merge

Per-layer readers can only nominate. CONFLICT and DUPLICATE are decided only
after merging findings across all layers — this cross-layer pass is the reason
the skill exists; a per-file audit that skips it is ordinary editing wearing
this skill's name. For each conflict, distinguish immediate precedence resolution from proposed
persistent maintenance, with source authority and a one-line rationale.

### 4. Report before apply

Return observed scope, conflicts and limits, inline for a bounded check. For
authorized persistent maintenance, provide a reviewable diff with the relevant
source/load identities, rationale, rollback path and regression conditions;
reuse the task's existing record. Full audits may include a baseline table
and conflict ledger. Token savings and cut ratios are costs, not proof of benefit.

### 5. Apply within existing authority

Prioritize consequential conflicts, then justified duplication and simplification.
Apply only authorized edits with a verified rollback path, grouping changes
coherently rather than requiring one commit per class. Assessment-only requests
end at findings. Preserve governance and consent protections; route source-owned
changes upstream instead of editing generated projections in place. Existing
maintenance authorization need not be requested again; a scope or authority gap
holds only the affected edit.

### 6. Re-baseline gate (what makes the cut list falsifiable)

Record the removed instruction's trigger, expected behavior, regression check
and actual exercised coverage. A regression attributable to a cut restores
the protection as **KEEP:GOTCHA citing the new incident**. Report only `no
regression observed under stated coverage`; unexercised recovery or safety
conditions remain untested. A quiet period does not confirm dead weight.
Do not promise a persistent observer unless one is actually commissioned.

## Extraction sub-mode

For content that is *needed but oversized* in an always-loaded layer: move it
to an on-demand artifact (a skill reference file, a command, a doc) and leave a
pointer. Fidelity rules: the target exists before the source line is trimmed;
pointers are verified to resolve and load when needed after the move; preserve
recoverable before/after states under the authorized version-control workflow. Extraction relocates cost; it does not remove conflict —
classify first, extract only what survives classification.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "No recent incident means this protection is dead weight" | Neither age nor silence proves usefulness or redundancy. Read its origin and exercise its triggering condition; otherwise mark it untested. |
| "I'll just audit the main instruction file" | Conflicts live BETWEEN layers. A scoped pass must name unobserved interactions; expand when those interactions bear on the finding. |
| "More verification instructions can't hurt" | Vendor-reported evidence says they do on frontier models — over-verification burns tokens and degrades output — and duplicated demands are debt regardless. OVER-VERIFY is a cut class, not a virtue. |
| "Deleting is risky, better to keep everything" | Evaluate the protection and the proposed cut. Rollback reduces recovery cost, but does not prove a cut safe or a rare trigger exercised. |
| "The 80% figure means we should cut 80%" | The magnitude is vendor-reported and estate-specific. The method is classify-and-watch, not a quota. |

## Handoff boundaries

Ends at scoped observed findings and any authorized maintenance results, with
coverage limits and regression conditions. Resume the original permitted task. Upstream: a model-generation upgrade or detected conflict triggers
entry. Downstream: decision-ledger persists the cut decisions and revisit
conditions; the owner-designated review handles consequential proposed cuts;
the agent-interface-design craft doctrine in reference/craft/ (not a suite
skill) owns fixing the tool-description side of any DUPLICATE
whose surviving copy belongs in an interface.

## Evidence emission

Only when authorized evaluation or an existing task evidence contract calls for it,
append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

Ordinary engagements require no separate run ledger. This optional telemetry
records engagement, not successful application or task benefit. It is not an
external calibration call or a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (the concrete layer enumeration,
paths, incident-record locations, report destinations). An overlay may add
bindings and examples; it never overrides the protocol.
