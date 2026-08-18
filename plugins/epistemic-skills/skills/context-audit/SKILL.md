---
name: context-audit
description: 'Use when auditing the instruction context an agent actually receives — on explicit request ("audit my context/CLAUDE.md/system prompt", "context audit", "prune my instructions"), when a cross-layer instruction conflict is detected mid-task (two active layers direct incompatible behavior), or after a model-generation upgrade invalidates guardrails written for a weaker model. Do NOT fire for auditing the prose quality of one document (ordinary editing), for designing NEW tool/agent interfaces (that is interface craft doctrine, not context hygiene), for pre-work recon on a task brief (recon owns the territory; this skill audits the map), or for tuning a prompt to improve the output of one specific task (that is prompt engineering, not context hygiene).'
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

The prior it operates under: as models strengthen, most accumulated instruction
is deletion-eligible. Anthropic reports removing over 80% of Claude Code's
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
| Recon of the territory before work | blindspot-pass | Audits the *task's* unknowns; this skill audits the *instruction map* the agent carries into every task |
| Designing the outbound channel | agent-interface-design | That skill shapes interfaces this agent authors for other minds; this one prunes the inbound instruction channel this agent consumes |
| Persisting what the audit decides | decision-ledger | Every applied cut class and every conflict resolution is a recorded decision with a revisit condition |
| Judging a high-stakes cut | gauntlet | A cut touching governance or safety-critical instruction layers escalates to adversarial review before apply |

## Protocol

### 1. Inventory the assembly

Enumerate every layer the harness loads for this agent, in load order, with an
approximate token count and a content hash per layer. The unit of audit is the
assembled set — a layer you skip is a layer whose conflicts you certify
blindly, so name skipped layers explicitly in the report.

Mark **generated and governance layers** (compiled rule projections, safety
policy, consent text) as *report-only*: conflicts found there are routed
upstream to their source of truth as findings, never edited in the projection.

### 2. Classify every instruction

Cut classes:

- **CONFLICT** — contradicts an instruction in another active layer. Must cite
  both locations verbatim. Costliest class: the model spends reasoning
  reconciling its operator before the task starts.
- **DUPLICATE** — the same directive in two or more layers. Keep exactly one
  authoritative location (prefer the most local, load-on-demand one — a tool
  description over a system prompt); cut the copies.
- **OBVIOUS** — restates strong-model default behavior: persona theater,
  restated general knowledge, emphasis scaffolding (all-caps, "CRITICAL",
  emoji-as-emphasis), generic care/quality exhortations.
- **MODEL-HANDLES-THIS-NOW** — a guardrail for an older model's failure mode
  with no documented incident behind it. The one test, applied line by line:
  *"Would a strong model behave worse without this line?"*
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
this skill's name. For each conflict, propose a surviving text and location
with a one-line rationale.

### 4. Report before apply

Emit a durable report: baseline table (per-layer tokens before/after), the
conflict ledger (both texts, both locations, proposed survivor), the cut list
as a unified diff grouped by class, and the calibration ratio — instructions
kept as gotchas versus instructions cut. The report is the artifact; the
inline summary is a pointer to it.

### 5. Apply class-by-class, operator-gated

Order by value: CONFLICT → DUPLICATE → OVER-VERIFY → OBVIOUS →
MODEL-HANDLES-THIS-NOW. One version-control commit per class, each cut batch
carrying a one-line rationale. Never edit generated projections in place.
An audit without version control has no rollback path and MUST stop at the
report — apply is forbidden.

### 6. Re-baseline gate (what makes the cut list falsifiable)

Record a watch note: for the following sessions, any behavioral regression
attributable to a cut line returns that line as **KEEP:GOTCHA citing the new
incident**. A cut that survives the watch window is confirmed dead weight; a
cut that comes back has minted a documented gotcha where an undocumented
guardrail used to be — strictly better than before, either way.

## Extraction sub-mode

For content that is *needed but oversized* in an always-loaded layer: move it
to an on-demand artifact (a skill reference file, a command, a doc) and leave a
pointer. Fidelity rules: the target exists before the source line is trimmed;
pointers are verified to resolve after the move; the move is committed with
before/after states. Extraction relocates cost; it does not remove conflict —
classify first, extract only what survives classification.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "This rule has always been here, it must be load-bearing" | Age is not evidence. If no incident record backs it, it is MODEL-HANDLES-THIS-NOW until reading its origin proves otherwise. |
| "I'll just audit the main instruction file" | Conflicts live BETWEEN layers. A single-file pass certifies the cross-layer conflicts unseen — that is the one failure this skill exists to prevent. |
| "More verification instructions can't hurt" | Vendor-reported evidence says they do on frontier models — over-verification burns tokens and degrades output — and duplicated demands are debt regardless. OVER-VERIFY is a cut class, not a virtue. |
| "Deleting is risky, better to keep everything" | Cuts are version-controlled, watched, and reversible; permanent reconciliation cost on every future task is the unbounded risk. |
| "The 80% figure means we should cut 80%" | The magnitude is vendor-reported and estate-specific. The method is classify-and-watch, not a quota. |

## Handoff boundaries

Ends at an applied (or report-only) audit with its re-baseline watch note
recorded. Upstream: a model-generation upgrade or detected conflict triggers
entry. Downstream: decision-ledger persists the cut decisions and revisit
conditions; gauntlet takes any governance-adjacent cut before apply;
agent-interface-design owns fixing the tool-description side of any DUPLICATE
whose surviving copy belongs in an interface.

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (the concrete layer enumeration,
paths, incident-record locations, report destinations). An overlay may add
bindings and examples; it never overrides the protocol.
