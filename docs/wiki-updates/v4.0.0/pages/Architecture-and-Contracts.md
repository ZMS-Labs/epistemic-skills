> **Maintainer handbook:** current development
>
> **Released baseline:** [epistemic-skills v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0)
>
> **Current development source:** [`main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main) is mutable. Use it to understand work in progress, never as an unlabeled definition of released behavior.
>
> **v4.0.0 note:** the v4.0.0 consolidation (2026-08-04) renamed several runtime-dependency owners referenced below: evidence-research's Consensus + Scite + durable-library triad now belongs to [resolve](Skill-Resolve)'s literature instrument. The eleven-skill inventory statements below remain numerically correct for v4.0.0; see the [Skill Catalog](Skill-Catalog) for the current names and mapping.

# Architecture and Contracts

epistemic-skills is one canonical collection of method files exposed through thin harness adapters. The architecture is deliberately asymmetric: skills define portable behavioral contracts; manifests and runtime adapters translate a host's tools into those contracts. There is no independent implementation per harness.

## System boundary

The collection sits beneath ordinary engineering workflow. It controls how an agent establishes, carries, challenges, and proves claims; it does not replace coding, testing, debugging, or planning workflows.

```text
workflow-skill layer  <->  Helix central passage  <->  epistemic router and disciplines
```

- [`using-epistemic-skills`](Skill-Using-Epistemic-Skills) is the router inside the epistemic collection. It applies the routine gate, selects positive triggers, sequences disciplines, and defines handoffs.
- [Helix](Helix-Central-Passage) is the central passage when a workflow-skill layer is also active. It pairs workflow stages with positively triggered epistemic disciplines.
- The nine disciplines each own a bounded epistemic moment: recon, derivation, research, goal contract, resumption, persistence, delegation, adversarial gating, or material acceptance.
- Routine work exits before either layer creates process artifacts. An absent pairing remains silent.

This separation prevents Helix from becoming a second router and prevents the collection from becoming mandatory ceremony.

## One canonical skills tree

The released tree is [`plugins/epistemic-skills/skills/`](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills). It contains all eleven `SKILL.md` cores and their references, scripts, examples, and evaluations.

```text
plugins/epistemic-skills/
├── skills/                      canonical skill implementations
├── agents/                      five canonical Gauntlet role definitions
├── contracts/                   shared handoff-receipt schema and verifier
├── .claude-plugin/plugin.json   package-local Claude metadata
├── .codex-plugin/plugin.json    package-local Codex metadata
└── .cursor-plugin/plugin.json   package-local Cursor metadata

skills  ───────────────────────> plugins/epistemic-skills/skills
agents  ───────────────────────> plugins/epistemic-skills/agents
```

The root `skills` and `agents` entries are repository symlinks. They let scanners and harnesses that expect root-level directories see the canonical content without copying it. A change to a skill belongs in the canonical tree only; a second harness-specific skill tree is an architecture defect.

## Thin harness surfaces

Root manifests tell a harness where the canonical tree lives and supply only the metadata or tool mapping that the harness requires.

| Surface | Entrypoint | Responsibility |
|---|---|---|
| Claude Code | [root marketplace](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.claude-plugin/marketplace.json) + [package manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/.claude-plugin/plugin.json) | Discover one package and load the canonical skill tree. |
| Codex | [marketplace index](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.agents/plugins/marketplace.json) + [package manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/.codex-plugin/plugin.json) | Load skills; the separate renderer binds Gauntlet roles into the user-agent registry. |
| Cursor | [whole-repo manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.cursor-plugin/plugin.json), [team marketplace](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.cursor-plugin/marketplace.json), package-local manifest | Expose canonical skills and agents. Public marketplace listing is not part of v3.0.0. |
| Gemini CLI | [`gemini-extension.json`](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/gemini-extension.json) + [`GEMINI.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/GEMINI.md) | Load root context and canonical symlinked skills. |
| Antigravity | [`plugin.json`](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugin.json) | Mark the repository as a native plugin; consume the shared root tree. |
| Kimi Code | [`.kimi-plugin/plugin.json`](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.kimi-plugin/plugin.json) | Load the canonical tree and translate user-question and isolated-agent operations to Kimi tools. |
| Generic Agent Skills host | canonical `skills/` tree | Use frontmatter `description` as trigger and the body as method. |

See [Cross-Harness Packaging](Cross-Harness-Packaging) for maintainer checks and [Installation and Harness Compatibility](Installation-and-Harness-Compatibility) for user-facing installation.

## Contract layers

### 1. Skill contract

Each released `SKILL.md` defines:

- its positive trigger and contraindications;
- required inputs and preconditions;
- method and ordering rules;
- output and stopping boundary;
- explicit degradation or fail-closed behavior; and
- handoff to the next consumer.

Frontmatter is not merely catalog copy. A harness uses `description` to decide when the skill is discoverable, so trigger edits are behavioral changes and must receive the same care as method edits.

### 2. Artifact contract

Machine-readable outputs carry a versioned schema, for example `formal-rigor-record@2`, `ledger-entry@1`, `gauntlet-run-record@1`, or a UAT packet. Schema conformance proves that a record has the required shape. It does not prove that its conclusion is true.

### 3. Handoff receipt contract

The shared [`handoff-receipt@1`](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/contracts/README.md) is a **producer self-issued declaration** carrying identity and provenance metadata, artifact and producer hash bindings, and a validity window. Its stdlib verifier establishes schema/hash binding and envelope well-formedness only. It does **not** authenticate origin, certify authorship, or establish the truth of self-reported provenance or other declared fields.

A receipt never attests:

- verdict truth;
- independence achieved; or
- freshness beyond the declared validity window.

Unknown predicates fail closed. A stale judgment-bearing artifact becomes envelope-only until the freshness-sensitive judgment is re-established. Hash-binding declared provenance is not provenance authentication; the receipt remains intentionally weaker than a signature or third-party attestation.

### 4. Runtime contract

A skill can require a capability without prescribing one vendor tool. Examples:

- Gauntlet needs context-isolated exact-role evaluators and an independent arbitrator. Sequential isolated calls are the stated degradation when concurrent barrier execution is unavailable.
- Evidence-Locked UAT needs separate actor and blinded-verifier contexts plus deterministic judging for a material run.
- Evidence Research needs discovery, reception checking, and a durable library; a missing layer must be labeled.
- Outsource needs a committed, pushed, target-readable packet before returning a ready prompt.

An adapter is correct when it preserves the contract, including independence, ordering, visibility, and failure behavior—not when it happens to invoke similarly named tools.

## Change discipline

Before changing a contract-bearing surface:

1. Identify whether the change affects a trigger, method, output schema, runtime precondition, or package path.
2. Update the canonical skill or contract first; keep harness manifests thin.
3. Add or adjust the smallest deterministic test that distinguishes the new behavior from the old one.
4. Keep every version-bearing manifest aligned when the release version changes.
5. Preserve routine exits, silent absent triggers, authority boundaries, and record-free outcomes.
6. Treat schema vocabulary additions as versioned changes; unknown values are designed to fail closed.
7. Link documentation claims to an immutable release for stable behavior and label mutable `main` links as current development.

## Canonical and current-development sources

- [Released architecture and layout in v3.0.0 README](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/README.md#layout)
- [Released shared receipt contract](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/contracts/README.md)
- [Released Helix contract](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/helix/SKILL.md)
- **Current development:** [canonical skills tree on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills/skills)
- **Current development:** [contracts on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills/contracts)
