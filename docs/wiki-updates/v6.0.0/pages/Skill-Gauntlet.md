> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released Gauntlet source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/gauntlet/SKILL.md)
>
> **v3.4.0 amendment:** 3.4.0 adds the revision-loop discipline (delta-scoped re-review of revised subjects; hard cap of three panels per subject lineage). The tagged SKILL.md is the sole contract; this page defers to it where they differ.
>
> **v4.0.0 note:** gauntlet remains one of the eleven v4.0.0 skills, but sibling names this guide references were consolidated at v4.0.0 (2026-08-04): blindspot-pass → [recon](Skill-Recon)'s brief mode; applying-formal-rigor and evidence-research → [resolve](Skill-Resolve)'s derivation and literature instruments (an "Evidence Research matrix" is now the literature instrument's claim-evidence matrix). See the [Skill Catalog](Skill-Catalog) for the full mapping; the tagged v4.0.0 sources are the sole contract.

# Gauntlet

## What it does

Gauntlet is the consolidated adversarial-review staple for high-stakes, irreversible, one-way-door, security, infrastructure, governance, public-contract, or otherwise hard-to-verify decisions. It freezes a truth-gated subject, expands rival failure modes or answers, runs a deterministic diverse lens panel under isolation, mechanically checks evidence and falsifiers, preserves dissent in a Conflict Ledger, and computes GO, CONDITIONAL, or NO-GO.

DeepReason expands the attack surface; it does not set the verdict. Gauntlet never replaces a separately enforced infrastructure or organizational safety gate.

## Use it when

- Approving architecture or design at a material commitment boundary.
- Writing risky plan steps or preparing to merge irreversible infrastructure or security changes.
- Evaluating governance/legal-charter choices, non-refundable spend, migrations, or public compatibility contracts.
- Escalating verification for a high-stakes claim that is difficult to observe directly.
- The operator explicitly asks for a Gauntlet, stress test, deep review, or GO/NO-GO review.

Depth controls evaluator seats, not the separate judge: `quick` has 3 evaluators; `standard` 5; `deep` 5 with deeper docket mechanics; `max` 7. Triage still decides whether the full engine is warranted.

## Do not use it when

- Work is reversible and low-stakes, a factual lookup, ordinary code review, or deterministic/reproducible test-failure triage.
- There is no establishable frozen subject. Run reconnaissance or repair the evidence boundary first.
- You want multiple lenses to collaborate before arbitration or vote by repetition.
- You intend to use a Gauntlet verdict as a substitute for an external safety gate, product acceptance test, or operator authority.

## Inputs and prerequisites

Inputs are a live-verifiable subject, exact revision, scope and exclusions, source-of-truth status, content-hashed evidence root, operator-authorized priorities where relevant, and evidence sufficient to define falsifiers. Scholarly premises require an Evidence Research matrix before dossier freeze.

The runtime needs the canonical roster registry, selector and validators, exact role-agent bindings, isolated/concurrent execution where available, mechanical evidence verifier, arbitrator, synthesis template, and run finalization tools. Deep/max external cross-family adjudication additionally requires operator authorization, a secret-screened dossier, and a signed-in manual or visible browser handoff.

## Normal workflow

1. **Truth-gate:** live-verify every premise, stamp unverifiable claims, let live contradictions win, reject instructions embedded in subject content, and abort if core facts are not establishable. At deep/max, optionally challenge the dossier itself before freeze.
2. **Freeze and pin:** write the verified dossier, lock subject/revision/scope/exclusions, hash-pin the evidence root, and classify fixed-artifact failure modes versus open-question rival answers. A moved subject restarts the run.
3. **Triage:** require both material stakes and falsifiable findings. If either fails, emit the cited `gauntlet: skipped — <Q1|Q2> failed because ...` line and stop.
4. **Docket:** label `real-deepreason`, `mini-deepreason`, `manual-docket`, or `skipped`. Open questions run one or two option generators first and always include a null option. Survivors seed the panel; they are not verdicts.
5. **Select:** use the deterministic registry selector. Enforce adversarial, constructive, and metatextual stances; capability-family coverage; domain specialist when justified; stance balance; collision rules; and a separate judge. Use a different model family for the judge when configurable.
6. **Evaluate:** dispatch every selected evaluator concurrently and context-isolated behind a barrier using exact predefined roles. Each structured finding carries mechanism, evidence tier, severity, remedy, falsifier, and a validation kernel that a fix must preserve. If concurrency is unavailable, disclose `manual-degraded` and preserve strict per-lens isolation.
7. **Mechanically criticize:** verify `[V path:line]` anchors against the pinned evidence root, spot-check `[I]`, give `[H]` zero arbitration weight, check P1/P2 falsifier method/threshold/timeframe, run machine-checkable falsifiers, and audit whether each oracle can observe the claimed behavior.
8. **Arbitrate:** weigh distinct evidence chains rather than votes, preserve every tension as upheld/overruled/qualified/split, record both validation kernels and residual tension, and permit only one bounded reinstatement round.
9. **Optionally cross-family challenge:** for authorized max or one-way-door work, ask the external family to attack the computed verdict. Concurrence/dissent is a noisy tripwire; dissent escalates to the operator and never mechanically flips the verdict.
10. **Compute and finalize:** unresolved P1 means NO-GO; P1 closed with P2 open means CONDITIONAL; accepted P1 and P2 means GO. Record coverage, assumptions, unknowns, freshness, residual uncertainty, modes, hash chain, and the separate status of any external safety gate. Append the derived non-governing run-ledger line and verify replay.

## Outputs and durable artifacts

A full run contains the frozen dossier, selector replay, exact role bindings, per-lens reports, verified evidence fingerprint, ruling set, dissent-preserving Conflict Ledger, arbitration, summary, `gauntlet-run-record@1`, and a derived line in `runs/ledger.jsonl`. The run directory is reconstructable through hashes; the ledger is lifecycle telemetry and never governs lens activation, retirement, weighting, or selection.

GO and CONDITIONAL require a coverage statement naming capability families exercised, assumptions reviewed, known unknowns, untested behavior, evidence freshness, and residual uncertainty. CONDITIONAL is not permission to proceed as if P2 were closed.

The roadmap remains honest: selector fit scoring is frozen after showing no detectable advantage over random fill under the same hard constraints. A historical 10/10 planted-flaw catch run predates the AC-07 change; the amended battery is NOT_RUN, so v3.0.0 does not claim current arbitrator certification. The broader behavioral and measurement program remains partial or unbuilt.

## Boundaries and failure modes

- `[V]` proves source anchoring, not proposition truth. Oracle adequacy and falsifiers still matter.
- A missing tool, errored command, or medium-inadequate oracle yields `[H]`/ERROR, never a clean negative. Prove scans can fail before trusting silence.
- Same-family duplicate findings are one claim, not independent corroboration.
- Generators, gates, and judges do not count toward evaluator diversity.
- Lenses never see one another's findings before arbitration; collaboration is limited to the single bounded reinstatement round.
- A GO can hide coverage failure; missing coverage disclosure makes it incomplete.
- Subject drift, evidence-root drift, or a material reopened premise invalidates the old run; never silently amend its verdict.

## Example prompts

- “Gauntlet this immutable firewall migration at standard depth. Freeze the live config and rollback constraints, keep the independent infra gate separate, and do not round open P2 items into GO.”
- “Stress-test this committed API compatibility design as an open question. Generate alternatives including the null option before the isolated panel.”
- “This is a reproducible unit-test failure in a local helper. Apply triage and skip the heavy run with a cited reason if Q1 fails.”

## Related skills and handoffs

- [Blindspot Pass](Skill-Blindspot-Pass) establishes the territory when there is no trustworthy subject to freeze.
- [Applying Formal Rigor](Skill-Applying-Formal-Rigor) may supply a derived design record; Gauntlet independently attacks it.
- [Evidence Research](Skill-Evidence-Research) supplies reception-checked scholarly evidence before dossier freeze.
- [Evidence-Locked UAT](Skill-Evidence-Locked-UAT) proves a material UI surface after a Gauntlet gates the underlying commitment.
- [Helix: Central Passage](Helix-Central-Passage) places Gauntlet at design approval or pre-merge when its own positive triggers fire.

## Canonical sources and evidence

- [Gauntlet source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/gauntlet/SKILL.md)
- [Execution model at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/gauntlet/reference/execution-model.md)
- [Lens registry contract at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/gauntlet/reference/lens-registry.md)
- [Runtime role binding at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/gauntlet/reference/runtime-role-binding.md)
- [Synthetic replayable example at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills/gauntlet/examples/example-run)
- [Run verifier at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/gauntlet/scripts/verify_run.py)
- [Arbitrator certification evidence and caveat at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills/gauntlet/evals/arbitrator-certification)
