> **Applies to:** epistemic-skills v5.0.0
>
> **Canonical source:** [released Outsource source](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/outsource/SKILL.md)
>
> **v5.0.0 note:** outsource remains a live skill. Sibling names consolidated at v4.0.0 still appear as vocabulary: blindspot-pass → [recon](Skill-Recon) brief mode; continuity-verify → [decision-ledger](Skill-Decision-Ledger) resume mode. See the [Skill Catalog](Skill-Catalog).

# Outsource

## What it does

Outsource moves a bounded workload across an execution boundary without making the originating chat the hidden source of truth. The complete context and completion contract live in a repository packet at an immutable, target-readable GitHub commit; the operator-facing prompt is only a short pointer. Every returned relay is stored verbatim, verified at origin, and incorporated into the next committed packet.

The context-erasure test is decisive: if the originating conversation vanished, the target could still execute and report correctly from the prompt plus pinned commit.

## Use it when

- The workload should go to a different, superior, specialized, or operator-selected model, agent, or process.
- The user asks to outsource, ask another model, prepare a copy/paste handoff, or create a repo-backed external relay.
- A durable GitHub handoff is explicitly wanted even for an otherwise ordinary dispatch.

## Do not use it when

- Dispatching an ordinary same-harness subagent with no requested durable external relay.
- The target is expected to infer context by browsing the repo without a map.
- You intend to perform or certify the outsourced work yourself inside this skill.

## Inputs and prerequisites

You need one bounded outcome, the authoritative repository, a stable work ID, the operator's target choice or capability requirements, source-of-truth paths, constraints and non-goals, authority boundaries, individually identifiable requirements, direct completion evidence, and the relay response contract.

Verify repository root, branch, status, remote, live remote head, publication authority, and intended target access. Preserve unrelated work and exclude secrets. For private repositories, record target access as an operator assertion unless independently verified.

## Normal workflow

1. Anchor live source state and distinguish working-tree, local-commit, and pushed GitHub state.
2. Bound one outcome and target. Split unrelated outcomes into separate work IDs.
3. Build a context map from actual code, docs, tests, decisions, and live state. For each required path, explain the load-bearing fact it supplies.
4. Fill `docs/outsource/<work-id>/HANDOFF.md` using the released template. Define allowed, forbidden, and ask-first actions; requirement IDs; direct evidence; non-proxy completion; and `COMPLETE`, `PARTIAL`, `BLOCKED`, and `QUESTION`.
5. Store the canonical outbound prompt template in the next append-only `relay/NNNN-origin.md` with literal `{packet_commit}`.
6. Commit and, when authorized, push the packet. Resolve the immutable 40-character commit and verify every linked path exists there.
7. Return only the short `PROMPT` and `PACKET` blocks. The prompt points at the pinned `HANDOFF.md`; the packet line reports `READY` or the single blocking condition.
8. On return, save the target response verbatim before interpretation, verify its commits/files/commands/tests, update the handoff, commit/push the next relay state, and issue the next immutable pointer.

## Outputs and durable artifacts

The repository contains `HANDOFF.md` plus alternating, append-only origin and target relay files. The operator receives exactly two blocks: a short prompt and readiness receipt. A Git commit cannot contain its own hash, so the committed relay stores `{packet_commit}` and the receipt's commit deterministically reconstructs the sent prompt.

The target returns `outsource-relay@1` with work ID, based-on commit, honest status, summary, work product, evidence, requirement state, decisions/assumptions, blockers/questions, and one recommended next action. A relay is claim data until the originating agent verifies it.

## Boundaries and failure modes

- A local, uncommitted, unpushed, or mutable-branch-addressed packet is a preparation state, not a do-not-use condition. Continue the workflow and do not emit `READY` until the packet exists at an exact pushed commit.
- `READY` requires committed, pushed, target-readable GitHub state at the exact commit.
- An inaccessible target, secret-bearing packet, hidden chat or attachments, credentials, local-only paths, conflicting requirements, or unobservable completion yields `BLOCKED`.
- Missing authority for destructive, publishing, financial, security-sensitive, or external action yields `BLOCKED`.
- A giant pasted prompt is not a substitute for a durable packet.
- Target-reported tests are not completion proof until origin re-verifies them.
- Unmet or unverified requirements produce `PARTIAL`, `BLOCKED`, or `QUESTION`, never “complete enough.”

## Example prompts

- “Prepare a repository-backed handoff for a specialized accessibility reviewer. The target must work from a pinned public commit and return only the relay envelope.”
- “Outsource this benchmark analysis to the model I named. Keep the complete dataset map and acceptance evidence in GitHub; give me only the short copy/paste pointer.”
- “The packet is committed locally but not pushed. Return a blocked receipt rather than a ready-looking prompt.”

## Related skills and handoffs

- [Blindspot Pass](Skill-Blindspot-Pass) can de-risk a fuzzy workload before it crosses the boundary.
- [Write Goal](Skill-Write-Goal) may supply the completion contract for long-running delegated work.
- [Continuity Verify](Skill-Continuity-Verify) re-anchors a returned or resumed relay state.
- [Helix: Central Passage](Helix-Central-Passage) places Outsource before an external handoff stage.
- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) treats delegation as cross-cutting; origin retains verification ownership.

## Canonical sources and evidence

- [Outsource source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/outsource/SKILL.md)
- [Handoff template at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/outsource/reference/HANDOFF_TEMPLATE.md)
- [Outsource contract tests at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/skills/outsource/tests)
