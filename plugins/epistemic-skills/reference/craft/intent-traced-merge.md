<!-- craft doctrine: intent-traced-merge — demoted from a standalone skill to reference doctrine (v4.0.0, 2026-08-04): a workflow/craft method, not an epistemic moment discipline; its battery and epoch results are archived in the sibling -evals directory -->


# intent-traced-merge — resolve hunks by provenance, not by pattern

A merge conflict is two claims about what the code should be. Resolving it by
staring at the text is pattern-matching under ignorance: the resolver picks
the side that *looks* right and silently destroys the intent of the other.
This is one of the places agents (and humans) most reliably destroy work,
because the destruction compiles.

The discipline: every non-trivial hunk is resolved by tracing **both sides to
their origin** — the commits that introduced them and the decision, spec,
ticket, or fix each origin served — and writing the resolution that preserves
both intents, or explicitly records which intent was dropped and why.

Provenance: distilled from the merge-conflict pattern in the Pocock-framework
community synthesis; re-derived here with the reversibility posture corrected
(see "Aborting is a tool").

## Protocol

1. **Classify hunks first.** Trivial (formatting, regenerable, disjoint
   semantics) → resolve or regenerate mechanically, no trace needed.
   Non-trivial → each gets a trace.
2. **Trace each side.** `git log/blame` the conflicting lines on both
   branches to their introducing commits; read each commit's message and its
   linked ticket/spec/fix. The unit of understanding is *what each side was
   for*, not what it says.
3. **Resolve to preserve both intents** where they compose (the common case:
   a bugfix on one side, a refactor on the other — the fix is re-expressed
   inside the refactored shape). Where they genuinely collide, the collision
   is a **decision, not a merge**: stop, name the two intents, and route to
   the decision's owner (or the decision process) before resolving. A merge
   resolution must never be where a design decision gets made silently.
4. **Verify against both origins.** After resolution, the test or observable
   behavior that motivated EACH side still holds (run the fix's test; run the
   refactor's suite). A resolution verified against only one side has a 50%
   blind spot by construction.
5. **Record provenance.** The merge commit message (or PR description) lists
   each non-trivial hunk's ruling: both-preserved / side-A-dropped-because /
   escalated. An undocumented non-trivial resolution is unsanctioned drift.

## Aborting is a tool

`git merge --abort` (and rebase --abort) is the return path, not a failure.
When a resolution goes sideways — traces got confused, the working tree state
is uncertain — abort, and restart the merge with the traces already learned.
"Never abort" absolutism trades reversibility for pride; this skill takes the
opposite side: preserve the return path until the resolution is verified.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| The collision is an open design decision | the decision's owner / gauntlet / open-questions | Step 3 routes it out — this skill resolves merges, it never silently decides designs |
| Verifying the resolution | workflow layer (tests) + verification-before-completion | Step 4's both-origins check is ordinary verification pointed at both parents |
| Recording dropped intent | decision-ledger | A deliberately-dropped intent is a consequential decision with a revisit condition |
| Isolation while resolving | workflow layer (worktrees) | Prefer resolving in an isolated worktree so aborting costs nothing |

## Falsifiable gate

A resolution passes when: every non-trivial hunk has a recorded ruling with
both origin references, and both sides' motivating checks run green on the
merged result. Wrong if either origin's test fails post-merge, or a hunk's
ruling cannot cite its two origins.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "Take theirs/ours and move on" | Bulk-side selection is intent destruction at scale — it resolves N distinct claims with one uninspected ruling. |
| "The newer change is probably right" | Recency is not intent. The newer commit may be the refactor that must *carry* the older fix, not replace it. |
| "It compiles and the suite is green" | The dropped intent's test may not exist. Green-on-the-surviving-side is the blind spot; step 4 requires both origins' checks. |
| "Aborting means losing my work" | The traces are the work, and they survive an abort. An uncertain working tree is the thing you cannot afford to keep. |

## Handoff boundaries

Ends at a merged result whose non-trivial hunks carry rulings and whose both-
origin checks pass. Upstream: any merge/rebase with non-trivial conflicts.
Downstream: decision-ledger for dropped intents; the decision process for
collisions that turned out to be open designs; normal review for the merge
itself.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (merge-commit message
conventions, escalation owners, worktree norms). An overlay may add bindings
and examples; it never overrides the protocol.
