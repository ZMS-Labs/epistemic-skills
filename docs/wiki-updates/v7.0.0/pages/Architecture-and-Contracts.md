> **Maintainer handbook:** current development
>
> **Released baseline:** [epistemic-skills v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0)
>
> **Current development source:** [`main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main) is mutable. Use it to understand work in progress, never as an unlabeled definition of released behavior.
>
> **v5.0.0 architecture:** `metacognate` is the sole named entry point; disciplines fire on their own descriptions. The deleted `using-epistemic-skills` and `helix` seats are historical only. See the [Skill Catalog](Skill-Catalog).

# Architecture and Contracts

epistemic-skills is one canonical collection of method files exposed through thin harness adapters. The architecture is deliberately asymmetric: skills define portable behavioral contracts; manifests and runtime adapters translate a host's tools into those contracts. There is no independent implementation per harness.

## System boundary

The collection sits beneath ordinary engineering workflow. It controls how an agent establishes, carries, challenges, and proves claims; it does not replace coding, testing, debugging, or planning workflows.

```text
workflow-skill layer  <->  metacognate (entry / pairing judgment)  <->  fourteen disciplines
```

- [`metacognate`](Skill-Metacognate) is the only skill you invoke by name. It applies the routine gate, names the unanswerable condition when process is warranted, and hands control back. It never enumerates members.
- Each discipline fires on its own frontmatter `description`. Selection belongs to those descriptions, not to an inventory-holding router.
- Pairing with a workflow layer is a `metacognate` Tier 2 judgment at a moment — not a Helix pair table.
- Routine work exits before either layer creates process artifacts. Absent triggers remain silent.
- Generated [`ROUTING.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/ROUTING.md) is derived from `metadata.hands-to` and is not a firing surface.

## Contract layers

| Layer | What it establishes | What it does not establish |
|---|---|---|
| Skill contract | Trigger, method, output, boundary, degradation, handoff | That a particular run followed the contract correctly |
| Artifact/schema contract | Shape, vocabulary, required fields, machine-verifiable invariants | Truth of the conclusion or quality of judgment |
| `handoff-receipt@1` | Producer-declared identity/provenance fields, hash binding, validity envelope | Authenticated origin, authorship, verdict truth, or independence |
| Runtime contract | Required isolation, tool, storage, ordering, and failure semantics | Equivalent behavioral quality across providers or harnesses |
| `skill-run@1` ledger | Intrinsic per-skill run record when a skill fires | That silence (routine exit) should invent a ledger row |

## Packaging surfaces

One canonical tree under `plugins/epistemic-skills/`; root symlinks and harness manifests are thin. See [Cross-Harness Packaging](Cross-Harness-Packaging) and the [README architecture section](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/README.md#architecture-and-source-policy).

| Harness | Surface | Note |
|---|---|---|
| Claude Code | marketplace + plugin | Package discovery from one immutable checkout |
| Codex | plugin marketplace + Gauntlet role renderer | Manifest does not itself register custom collaboration-agent types |
| Cursor | local/team marketplace | Public listing unavailable; retained behavioral epoch `BLOCKED_EXTERNAL` |
| Gemini CLI | extension + root context | Uses root context and canonical symlinked tree |
| Antigravity | native plugin marker | Choose native, Gemini link, or import — only one |
| Kimi Code | repository plugin | Plugin instructions map isolated-agent primitives |
| Generic | Agent Skills URL | Host must supply runtime primitives the selected skill requires |

## Source precedence

1. Immutable released `SKILL.md`, contract, schema, or executable check.
2. Released references, records, and evidence at the same tag.
3. README and Wiki explanations.

## Canonical references

- [Released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)
- [v5.0.0 design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md)
- [RELEASING.md](https://github.com/ZMS-Labs/epistemic-skills/blob/main/RELEASING.md) (version-neutral procedure on `main`)
