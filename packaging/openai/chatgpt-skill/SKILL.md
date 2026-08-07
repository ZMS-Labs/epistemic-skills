---
name: epistemic-skills
description: Use when the approach itself is uncertain, when a claim about correctness/completion/deployment is about to bear load, when evidence quality or acceptance is disputed, when resuming from a summary or handoff, or when the user explicitly asks to use Epistemic Skills. This generated bridge selects the current packaged disciplines dynamically. Do NOT fire for routine, reversible, directly checkable work.
---

# Epistemic Skills — ChatGPT bridge

This is a generated adapter, not a second source of truth. The authoritative
methods are the bundled files under `package/skills/`.

## Invocation contract

1. Read `skill-index.json` before responding or acting. It is regenerated from
   direct `package/skills/<name>/SKILL.md` children on every build.
2. Compare the current task with every description in that generated index.
   Never use a remembered or hand-maintained inventory.
3. Load each applicable file at `package/<canonical_path>` and follow it exactly,
   including positive and negative triggers, ordering, gates, artifacts,
   degradation rules, stopping conditions, and handoffs.
4. If no current description applies, do ordinary work. Extra process earns no
   credit merely because this bridge was installed.
5. When several skills apply, obey their own ordering. A process or entry-point
   skill that applies runs before a narrower implementation discipline, and
   control returns to the interrupted work when the bounded engagement ends.
6. Never claim a runtime, independent actor, scheduler, persistent store, or
   other capability the current harness does not provide. Use the selected
   skill's degradation path and mark the limitation explicitly.
7. Treat the `source.revision` in `skill-index.json` as the bundle's provenance.
   An uploaded personal Skill is a snapshot; do not describe it as current after
   the repository has moved unless it has been rebuilt and re-uploaded.

## Pairing with workflow skills

When a workflow layer such as Superpowers is installed, use both as
complementary systems. Either may interrupt the other when its trigger becomes
true, hard gates remain binding across both layers, and the interruption must
return control to the point where it began.
