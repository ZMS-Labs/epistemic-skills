> **Historical page.** `continuity-verify` is not a live skill. Use **`decision-ledger (resume mode)`**. Consolidated in v4.0.0.
>
> Body text below is retained for method vocabulary and migration; where it conflicts with a tagged `v5.0.0` contract, the tagged source controls.

# Continuity Verify

## What it does

Continuity Verify treats a summary or handoff as a set of claims, not as current state. Before resumed work, it re-anchors the claims that downstream actions depend on to durable artifacts and emits one state digest. This prevents false-DONE declarations and actions based on stale remembered state.

The skill consumes prior-state narratives; it never performs the resumed task and never writes the decision ledger it may inspect.

## Use it when

- A session resumes from compaction and the next action depends on what the summary says is done, chosen, tested, or approved.
- A cross-session, cross-device, or cross-agent handoff carries load-bearing state.
- The next step cites remembered facts such as a branch being merged, tests passing, or an operator authorizing an action.

Use the `quick` dial only for a resumption within minutes on the same machine with low-stakes claims. Use `standard` by default. Use `deep` for a long gap, cross-device handoff, high stakes, or approval claims needing independence checks.

## Do not use it when

- This is a fresh task with no prior-state claims; use routine micro-recon or Blindspot Pass as triggered.
- You are checking premises of a frozen adversarial-review subject; Gauntlet owns that truth gate.
- You need to persist a new decision; Decision Ledger owns that moment.
- You want to trust a handoff because its prose is detailed or familiar.

## Inputs and prerequisites

Collect the summary or handoff plus live durable anchors: file content, Git status and log, remote or PR state, run records, receipts, stamps, goal state, and any decision artifacts. Identify the current source of truth before comparing claims.

Classify each load-bearing item as observation, interpretation, prediction, value, or authorization. If a ledger is present, its entries are leads only. If no ledger exists, say the check was skipped; absence does not prove that no decisions were made.

## Normal workflow

1. Enumerate only claims the next actions depend on. At `quick`, spot-check the top three by authorization, state, then decision risk.
2. Re-anchor each claim. Mark it `verified` with its anchor, `contradicted` with the live value, or `(UNVERIFIED)`.
3. Check receipt validity predicates. Re-run only the freshness-sensitive check when a receipt is stale.
4. Walk each decision-ledger `supersedes` chain to its unique head and honor `revisit_when`. Malformed or dangling chains are stale-by-construction.
5. Emit a digest with verified, contradicted, unverified, and `accepted_unverified` sections, plus the resulting action: proceed, halt, or rescope.
6. Hand the digest to the router. Resumed work proceeds only on verified state or authority-valid accepted-unverified state.

At `quick`, the agent may self-accept a low-stakes unverified claim and record the risk. At `standard` or `deep`, a load-bearing unverified claim needs a named non-self authority whose delegation is itself verifiable. Unverifiable approval always escalates; it never authorizes.

## Outputs and durable artifacts

The sole output is a state digest tied to the re-anchored revision. It records exact anchors, live contradictions, visible uncertainty, any acceptor and accepted risk, and whether the task must be re-scoped.

A trivial resumption with no load-bearing claim may close with a one-line check rather than a ceremony-heavy artifact. The digest is void as soon as the underlying state moves; a later resumption re-fires the skill rather than patching an old digest.

## Boundaries and failure modes

- Missing evidence stays `(UNVERIFIED)`; explanation cannot upgrade it.
- A contradicted or unverifiable core premise changes the task. Re-scope instead of repairing the summary's wording.
- No authority-valid acceptance path at `standard` or `deep` means halt or rescope.
- Ledger content informs but never authorizes.
- Stale receipts trigger the narrow freshness check, not an invented extension of validity.
- The shipped resume fixture battery is a deterministic smoke check, not a measured real-world catch rate or proof of proportionality.

## Example prompts

- “Resume from this handoff. Verify the claimed commit, clean status, passing test run, and approval before making the release change.”
- “The compaction says the migration was approved, but no approval link is present. Produce the state digest and do not treat the summary as authority.”
- “I resumed five minutes later on the same machine; spot-check the three load-bearing low-risk claims and record any self-accepted uncertainty.”

## Related skills and handoffs

- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) receives the digest and routes the resumed work.
- [Decision Ledger](Skill-Decision-Ledger) supplies prior judgment that this skill re-anchors rather than trusts.
- [Blindspot Pass](Skill-Blindspot-Pass) may fire next if live state exposes unfamiliar or mismatched territory.
- [Write Goal](Skill-Write-Goal) goal state is one claim class inside the digest, not a separate resumption pass.
- [Gauntlet](Skill-Gauntlet) remains authoritative for the frozen-subject truth gate.

## Canonical sources and evidence

- [Continuity Verify source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/continuity-verify/SKILL.md)
- [Resume-fixture smoke check at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills/continuity-verify/evals/resume-fixtures)
- [Trust contracts at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/contracts/README.md)
- [Decision-ledger consumption contract at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/decision-ledger/SKILL.md)
