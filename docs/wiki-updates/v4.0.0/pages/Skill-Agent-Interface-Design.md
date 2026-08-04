> **Applies to:** epistemic-skills v3.3.0
>
> **Canonical source:** [released Agent Interface Design source](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.3.0/plugins/epistemic-skills/skills/agent-interface-design/SKILL.md)
>
> **v4.0.0 consolidation:** agent-interface-design became **reference craft doctrine** at v4.0.0 (2026-08-04) — no longer a routed skill. The method moved verbatim, with its archived batteries and epoch results, to [`reference/craft/agent-interface-design.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/reference/craft/agent-interface-design.md), read on demand when building an interface another agent consumes. This page is retained as a historical guide; the tagged v4.0.0 sources are the sole contract.

# Agent Interface Design

## What it does

When work crosses to another agent through a tool schema, MCP surface, structured-output contract, dispatch contract, or agent-consumed CLI/API, the interface **is** the instruction channel. This skill encodes constraints in the interface's structure — types, enums, named fields, required/optional with defaults, structured error diagnostics — rather than in prose documentation or usage examples. A `status` field typed `pending | in_progress | completed` plus one sentence teaches a whole state machine; three worked examples teach three paths and quietly deprecate the rest.

It is the outbound twin of the prose-contract skills: Write Goal and Outsource govern intent crossing to another mind as prose; this skill governs it crossing as machine contract.

## The evidence-graded doctrine

The skill states its claims at the grade the literature supports (anchors reception-checked 2026-07-30, no contrasting citations or notices):

1. **Structure buys contract adherence — supported.** Schema-based contracts reduce interface misuse versus free-form docs under identical semantics; parameter-fill failures dominate real toolchain breakage.
2. **Structure does not buy semantic quality — same controlled study.** The one-sentence *why/when* per operation still matters, stated once, in the interface.
3. **Examples bias consumers toward shown paths — directionally supported, capability-dependent.** Not a universal law: small models still need examples, and some regimes show examples preserving diversity. Rule form: frontier-consumer interfaces default to zero usage examples; examples are a deliberate, labeled compatibility feature for weaker consumers — never the specification.
4. **The urge to write a usage example is a design lint** — it usually means a parameter is under-specified. Fix the parameter, delete the example.
5. **Specification content outranks format religion.** JSON vs YAML is not the argument; what the specification says is.

## The falsifiable gate: the cold-consumer test

An interface passes when a cold consumer — an agent given only the schema and one-line descriptions, no examples, no surrounding conversation — produces a semantically correct first call for each top intended operation. Fail → fix structure. Adding prose or examples to pass is recorded as a compatibility concession, not a fix. The transcript is the gate evidence.

## Use it when

- Authoring or modifying a tool/function schema, MCP surface, structured-output contract, subagent dispatch contract, or a CLI/API whose caller is an agent.
- Reviewing a change that adds one of those.

## Do not use it when

- The interface is human-facing (UI/UX and docs for people).
- The script is one-off and throwaway with a single known caller.
- The crossing is prose — Outsource and Write Goal own prose contracts.
- You are auditing the instruction context an agent *receives* — Context Audit owns the inbound channel.

## Boundary and handoffs

Ends at a shipped interface plus its consumer-test evidence. Evidence-Locked UAT runs acceptance when the surface is operator-facing; Gauntlet reviews high-blast-radius interfaces before they ship; Decision Ledger records consequential interface decisions (a closed enum, a breaking default) with revisit conditions.
