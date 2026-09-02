> **Maintainer handbook:** current development
>
> **Released truth source:** [v3.0.0 risk-acceptance record](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json)
>
> This page summarizes accepted risk. The machine-readable release record controls if wording differs.
>
> **v4.0.0 update:** the risk-acceptance record remains the controlling document, append-only (accepted scopes are never rewritten). Per the [v4.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md): `G3-R1`'s exit criterion was met 2026-08-04 — the amended AC-07 planted-flaw battery ran blind, 10/10 catch, CERTIFIED at standard rigor (same-model-family caveat stands) — and is recorded in `revisit_history`; all other accepted scopes are unchanged. The four-arm behavioral campaign ran under its committed design (72/72 blinded seeded trials) and found **no arm separation** — behavioral superiority remains UNESTABLISHED, now with evidence. The 2026-08-04 trigger epochs predate the consolidation; the merged trigger surfaces of recon/resolve/decision-ledger are new subjects and re-arm per [`docs/policy/EVIDENCE-POLICY.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/policy/EVIDENCE-POLICY.md). The body below documents the v3.0.0-era record and retains its original status language.


> **v7.0.0 status.** v7.0.0 is **prepared and not yet published**: no tag, no Release, and the independent publication-judgment gate (RG-8) has neither returned GO nor been waived on the record. Nothing below is superseded by it, and every limit named here ships unretired into it.
>
> **v6.0.0 update.** v6.0.0 is an **exception release**: four independent publication reviews across three model families all returned NO-GO, and the owner overrode the judgment gate (RG-8) under a recorded exception. None of the four found a defect in the shipped skills — every P1 concerned the release process, its paperwork, or its authority chain. The integrity gates were met on their own terms and were not waived. Limits shipped unretired: `KL-SELF-GO` (the implementing lineage holds no acceptance seat), `KL-LIVE-ENV`, `KL-MACOS-162`, `KL-WINDOWS`, `KL-GUARD-LEXICAL`. The D8 cross-family consult remains **owed and undischarged**, carried to 6.1.0 as blocking. See the [verdict lineage](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/gauntlet-runs/V6-VERDICT-LINEAGE.md) for all nine reviews and who dispatched each.
>
> **v5.0.0 honesty:** publication item 6 was only PARTIALLY MET; item 8 was WAIVED. Read the [errata](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/RELEASE-5.0.0-ERRATA-2026-08-06.md) and [post-release independent review](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/POST-RELEASE-INDEPENDENT-REVIEW-5.0.0-2026-08-06.md) (NO-GO for retrospective certification) before treating v5.0.0 as gate-complete.
>
> Successor corrective work on `main`: [SUCCESSOR-PROGRESS-104-105-2026-08-07.md](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/SUCCESSOR-PROGRESS-104-105-2026-08-07.md).

# Evidence, Status, and Known Limitations

Version 3.0.0 is an immutable support point for packaged contracts and deterministic repository checks. It is **not** proof of universal behavioral superiority, cross-provider generality, or current Cursor compatibility.

The operator accepted a bounded set of behavioral and cross-provider confidence gaps for the first stable snapshot. That acceptance did not waive or satisfy deterministic, DCO, CodeQL, security, provenance, independent-review, or publication-identity gates.

## What the release does support

- One tagged source snapshot with aligned package manifests and immutable install coordinates.
- Deterministic contract, proportionality, schema, UAT-judge, Gauntlet-mechanics, DCO-policy, JSON, receipt, and package-integration checks.
- A completed blinded proportionality campaign with corrected over- and under-escalation controls at frozen coordinates.
- Explicit migration behavior: routine and absent-trigger paths may be silent; focused formal rigor is inline and record-free; standard/high-assurance work emits `formal-rigor-record@2`.
- A documented release identity linking the final `main` commit, annotated tag, GitHub Release target, and committed notes.

These are real claims, but none entails that every model, provider, harness, or future task will behave correctly.

## Accepted limitations

| ID | Exact released limitation | What must not be inferred | Exit condition recorded for v3.0.0 |
|---|---|---|---|
| `FR3-R1` | The post-hoc Codex semantic review found **two genuine P0 failures**, `tm-02` and `tm-03`. | Do not describe all observed formal-rigor candidates as correct. | A fresh preregistered campaign passes both scenarios under independent valid adjudication. |
| `FR3-R2` | Forty-four OpenAI-origin candidates received no valid semantic judgment because all **88 AGY adjudication attempts** ended as zero-token quota failures. | These are provider-availability failures, **not semantic merit failures** and not evidence that the candidates would pass. | Complete independent semantic judgments for every planned provider arm. |
| `FR3-R3` | Provider, repetition, and judge assignment are confounded; same-provider paired seats are correlated. | Do not attribute subgroup differences causally to provider or count paired seats as independent model families. | A preregistered balanced design separates provider, repetition, and judge family. |
| `FR3-R4` | The earlier Cursor epoch is **`BLOCKED_EXTERNAL`** because Fleet `stream-json` produced invalid terminal JSON and exposed no constrained-response schema. | Do not promote, normalize, or substitute a Cursor result; packaging readiness is not runtime behavioral proof. | A retained schema-valid Cursor campaign completes without transport normalization. |
| `FR3-R5` | Broad structural polarity is not established: closed-taxonomy and formal-only parody arms outperformed the candidate, and three AGY parody arms are absent. | Do not claim broad candidate-to-parody separation or universal scorer discrimination. | A complete balanced polarity battery rejects every over- and under-escalation parody while the candidate passes. |
| `FR3-R6` | The V3 post-hoc diagnostic remains exactly **`release_credit: none`**. | Do not cite it as satisfying or repairing the historical release gate. | A new qualifying campaign may supersede the gap; the diagnostic itself remains no-credit. |
| `G3-R1` | The historical Gauntlet arbitrator result of 10/10 predates amended AC-07. The amended arbitrator-certification battery is **`NOT_RUN`**. | Do not claim the current arbitrator is certified. | Run the amended battery and meet its declared threshold. |

These are accepted support risks, not passes.

## Merit versus availability

The post-hoc diagnostic planned 130 semantic seats:

| Judge path | Planned and terminal | Valid semantic judgments | Interpretation |
|---|---:|---:|---|
| Codex judging Google-origin candidate content | 42 | 42 | 38 `VALID`, 4 `INVALID`; paired results produced 19 passes and the two genuine P0 failures. |
| AGY judging OpenAI-origin candidate content | 88 | 0 | Every call ended with `Individual quota reached`, zero tokens, and failed transport. No merit judgment exists for 44 candidates. |

The aggregate's 24 `FAIL` labels combine 2 genuine semantic failures with 22 availability-driven P0 fail-closed cases. The latter are operational failures under the preregistered rule, but they are not 22 additional semantic invalidities. The 22 P1 cases with unavailable AGY judgments remain `ARBITRATION_REQUIRED`.

No evidence justifies predicting that all unavailable responses would have passed or failed. The correct status is inconclusive.

## Structural results are not semantic results

The diagnostic structurally scored 215 content-bearing views and found 100 passes. The candidate passed 49/65 available views, or 47/62 excluding normalized views. Closed-taxonomy and formal-only parodies had higher observed structural pass proportions, while three AGY parody arms were absent.

That means the structural scorer detected some desired form but did not establish broad polarity. A response can contain expected sections and still be wrong; a parody can satisfy surface cues. Structural checks remain useful guardrails, not semantic adjudication.

## Diagnostic evidence is not release credit

The V3 analysis was conducted post hoc over an excluded epoch. It retained 130 at-most-once semantic attempts and exact source/diagnostic pins, but it did not repair, retry, reuse, or promote the source run.

Its status remains:

```text
release_credit: none
```

Historical wording inside the diagnostic says the release was then on HOLD. The final v3.0.0 release record later documents the operator's bounded risk acceptance and the separate non-waivable gates. Risk acceptance changed the publication decision; it did not change the diagnostic into a pass.

## Cursor status has two layers

- **Packaging:** v3.0.0 contains Cursor manifests and supports a local tagged checkout or team marketplace import.
- **Behavioral evidence:** the recorded Cursor evaluation epoch is `BLOCKED_EXTERNAL`; no qualifying Cursor result exists.

Do not collapse packaging compatibility, public marketplace availability, runtime structured-output capability, and behavioral merit into one “Cursor support” claim.

## Gauntlet certification boundary

The historical arbitrator battery's 10/10 result was produced before the amended AC-07 contract. Deterministic Gauntlet tests still protect selector, role binding, evidence, and run-record mechanics, but the amended certification battery is `NOT_RUN`. This release therefore makes no current arbitrator-certification claim.

## Non-waivable gates

The v3.0.0 risk record explicitly preserves:

- version parity across the README, nine package manifests, immutable install references, and `EXPECTED_VERSION`;
- the complete deterministic repository suite;
- author-matching DCO on every release-PR commit;
- CodeQL success on the exact release-PR head;
- full-history secret scanning plus a positive control proving the scanner can fail;
- public-content and provenance review;
- independent publication review and final Gauntlet;
- an annotated `v3.0.0` tag targeting final `main`; and
- a stable GitHub Release whose target and body agree with the tag and committed notes.

No behavioral-risk record has authority to waive those gates.

## How to write status claims

Prefer bounded language:

- “The deterministic suite passed on commit `…`.”
- “The candidate passed this frozen proportionality campaign.”
- “No valid AGY semantic judgment was returned because quota was exhausted.”
- “The Cursor epoch is `BLOCKED_EXTERNAL`.”
- “The amended battery is `NOT_RUN`.”
- “The diagnostic is no-credit.”

Avoid:

- “The skills are proven better.”
- “All failed calls were wrong.”
- “Cross-provider behavior is validated.”
- “Cursor is fully supported.”
- “The arbitrator is certified.”
- “Risk acceptance waived the release gate.”

## Sources

- [v3.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/RELEASE-3.0.0.md)
- [Machine-readable v3.0.0 risk acceptance](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json)
- [Formal-rigor V3 post-hoc diagnostic](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/evidence/2026-07-26-formal-rigor-v3-posthoc-diagnostic.md)
- [Released proportionality campaign results](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/evals/proportionality/blinded/results/RESULTS.md)
- [Released Gauntlet skill status](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/gauntlet/SKILL.md)
- **Current development:** [release evidence on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main/docs/release)
