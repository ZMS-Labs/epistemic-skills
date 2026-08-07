> **Historical page.** `intent-traced-merge` is not a live skill in v5.0.0. Use **`reference/craft/intent-traced-merge.md`**. Demoted to craft doctrine in v4.0.0.
>
> Body text below is retained for method vocabulary and migration; where it conflicts with a tagged `v5.0.0` contract, the tagged source controls.

# Intent-Traced Merge

## What it does

A merge conflict is two claims about what the code should be. Resolving by staring at the text is pattern-matching under ignorance — it silently destroys the intent of one side, and the destruction compiles. This skill resolves every non-trivial hunk by **tracing both sides to their origin commits and the decision, spec, ticket, or fix each origin served**, then writing the resolution that preserves both intents — or explicitly records which intent was dropped and why.

## Protocol

1. **Classify** — trivial hunks (formatting, regenerable, disjoint) resolve mechanically; regenerate generated files instead of resolving them.
2. **Trace** both sides (`git log/blame` → introducing commits → linked ticket/spec/fix). The unit is what each side was *for*.
3. **Preserve both intents** where they compose. Where they genuinely collide, the collision is a **decision, not a merge** — stop and route to the decision's owner. A merge resolution is never where a design decision gets made silently.
4. **Verify against both origins** — each side's motivating test/behavior still holds on the merged result. One-sided verification has a 50% blind spot by construction.
5. **Record provenance** — per-hunk rulings (both-preserved / dropped-because / escalated) in the merge commit or PR.

## Aborting is a tool

`git merge --abort` is the return path, not a failure — the traces survive an abort, an uncertain working tree does not deserve to. This deliberately corrects the community "never abort" absolutism, which trades reversibility for pride.

## Use it when

- Any merge/rebase conflict where a hunk is non-trivial (both sides changed the same logic; semantics, not formatting).
- Reviewing a merge commit whose resolution provenance is undocumented.

## Do not use it when

- Conflicts are mechanically trivial — formatting, lockfiles, generated files (regenerate instead).
- The sides embody a genuinely open design decision — that is a decision to adjudicate, not a merge to resolve.

Provenance: distilled from the merge-conflict pattern in the Pocock-framework community synthesis; reversibility posture corrected here.
