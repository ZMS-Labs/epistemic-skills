---
name: agent-interface-design
description: 'Use when authoring or modifying an interface another agent will consume — a tool or function-call schema, an MCP server surface, a structured-output contract, a subagent dispatch contract, or a CLI/API whose caller is an agent — and when reviewing a change that adds one. Do NOT fire for human-facing interfaces (UI/UX and docs for people), for one-off throwaway scripts with a single known caller, for prose handoffs to another mind (outsource and write-goal own prose contracts), or for auditing the instruction context an agent receives (context-audit owns the inbound channel).'
---

# agent-interface-design — the interface IS the instruction

When work crosses to another agent through a tool, schema, or contract, the
interface is the instruction channel. Encode constraints in the interface's
**structure** — types, enums, named fields, required/optional with defaults,
structured error shapes — rather than in prose documentation or usage examples.
A `status` field typed `pending | in_progress | completed` plus one sentence
("keep exactly one item in_progress") teaches a whole state machine. Three
worked examples teach three paths and quietly deprecate every other path the
consumer might have explored.

This is the outbound twin of prose-contract skills: write-goal and outsource
govern intent crossing to another mind as *prose*; this skill governs it
crossing as *machine contract*. The failure it prevents is epistemic: an
under-specified parameter forces the consuming agent to guess, and an
example-driven doc makes it guess confidently and narrowly.

## Evidence-calibrated doctrine

State these as they are graded; do not overclaim (evidence run 2026-07-30,
reception-checked, no contrasting citations or notices on anchors):

1. **Structure buys contract adherence — supported.** Under identical
   semantics, schema-based contracts reduce interface misuse versus free-form
   documentation (Sigdel & Baral 2026, arXiv:2603.13404, controlled study).
   Parameter-fill failures and name hallucination dominate real toolchain
   breakage (Xiong et al. 2025, EMNLP Findings); most public tool docs are
   under-specified (ToolFuzz 2025).
2. **Structure does NOT buy semantic quality — same study.** Schema cut
   interface misuse, not semantic misuse. The description still carries the
   *why/when*, exactly once. A validated schema with no purpose sentence is
   half an interface.
3. **Examples bias consumers toward shown paths — directionally supported,
   capability-dependent.** For tool use, demonstrations can induce biased
   usage and docs-only prompting matches or beats few-shot (Hsieh et al.
   2023, arXiv:2308.00675); human-curated examples systematically
   under-cover the input space (ScatterShot, 2023); few-shot outputs bias
   toward prompt-frequent patterns (Zhao et al. 2021). But this is NOT a
   universal law: for small models, examples are the largest single
   performance lever, and in some regimes examples preserve rather than
   collapse diversity. Rule form: **frontier-consumer interfaces default to
   zero usage examples; examples are a deliberate, labeled compatibility
   feature for weaker consumers — never the specification.**
4. **The urge to write a usage example is a design lint.** It usually means a
   parameter is under-specified. Name the parameter better, tighten its type,
   or split it — then delete the example.
5. **Specification content outranks format religion.** Serialization format
   choice (JSON vs YAML vs markdown) is insignificant next to what the
   specification says and consumer-model capability. Argue semantics, not
   syntax.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| Prose contract to another mind | write-goal / outsource | They ship intent as goals and handoff packets; this skill ships it as schemas and typed contracts. Rich references (a failing test, a rubric) may ride either channel |
| Inbound instruction hygiene | context-audit | That skill prunes what this agent receives; this one designs what other agents receive. A DUPLICATE whose survivor belongs in a tool description lands here |
| Acceptance of the built surface | evidence-locked-uat | If the interface fronts an operator-facing surface, acceptance runs there; this skill's consumer test is not a UAT substitute |
| High-blast-radius interfaces | gauntlet | A control-plane or destructive-capability interface goes to adversarial review before it ships |

## Core moves

1. **Enumerate states and transitions first**; encode them as enums and typed
   fields, not prose. If a value set is closed, close it — every enum value is
   a promise, and an honest unbounded string beats a leaky enum.
2. **Let names carry semantics.** A parameter whose meaning needs a paragraph
   is misnamed or doing two jobs; split it. Name in the project's established
   domain vocabulary — the glossary, schema, or ubiquitous language its
   consumers already hold — and never mint a synonym for a concept the
   project already names: a second name for one concept is a conflict the
   consumer must reconcile on every call.
3. **Required/optional/defaults encode policy.** A default is the behavior you
   endorse; an optional field with no default is a question you are forcing
   every consumer to answer.
4. **Errors are structured diagnostics the consumer can act on** — a machine-
   readable reason and, where known, the corrective move — not strings to
   pattern-match.
5. **One purpose sentence per operation** — the why/when, stated once, in the
   interface itself. Never duplicated into a system prompt or a README (that
   duplicate is context-audit's DUPLICATE class waiting to happen).
6. **Example-lint:** every usage example must carry a written justification
   naming the weaker-consumer audience it serves, or be converted into a
   structural fix and deleted.
7. **Progressive disclosure is interface design:** if full reference material
   is large, the interface exposes a small always-visible surface and a named,
   on-demand path to depth — not everything inline.

## The consumer test (falsifiable gate)

An interface passes when a **cold consumer** — an agent given only the schema
and one-line descriptions, with no examples and no surrounding conversation —
produces a semantically correct first call for each of the top intended
operations. Run it before shipping and after any schema change. Fail → fix
structure; adding prose or examples to pass the gate is recorded as a
compatibility concession, not a fix. Keep the transcript as the gate evidence.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "I'll add an example just to be safe" | Examples narrow the consumer's explored space and rot silently. Safe is a tighter parameter. Run the example-lint. |
| "The description can clarify what the type doesn't" | Descriptions carry *why*; structure carries *how*. Prose patching a loose type is the documented dominant failure mode. |
| "More enum values make it flexible" | Each value is a contract you must honor forever. Flexibility you can't promise belongs in an open field, honestly typed. |
| "Schema validates, so the interface is done" | Contract adherence ≠ semantic correctness — the controlled study split exactly this. Run the consumer test. |
| "Our consumer is smart, it'll figure it out" | Then the interface is fine to test — the cold-consumer gate costs one dispatch. Guessing is the thing being prevented. |

## Handoff boundaries

Ends at a shipped interface plus its consumer-test evidence. Upstream:
write-goal/outsource when the crossing is prose; blindspot-pass if the
interface's domain is unrecognized. Downstream: evidence-locked-uat for
operator-facing acceptance; gauntlet for high-blast-radius surfaces;
decision-ledger records consequential interface decisions (a closed enum, a
breaking default) with revisit conditions.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (the estate's tool registries,
schema conventions, dispatch-contract patterns, consumer-test harnesses). An
overlay may add bindings and examples; it never overrides the protocol.
