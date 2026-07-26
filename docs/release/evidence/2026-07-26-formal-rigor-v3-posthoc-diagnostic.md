# Formal-rigor V3 post-hoc diagnostic evidence

Status: **diagnostic only; no release credit; 3.0.0 remains HOLD**

This report records the preregistered materialized diagnostic view over the
excluded `noncursor-degraded-v3` epoch. It answers only what the retained model
content suggests under the diagnostic criteria. It does not qualify, repair,
resume, reuse, or promote V3 and cannot satisfy a release gate.

## Frozen provenance

| Coordinate | Value |
|---|---|
| Source root | `C:\tmp\formal-rigor-noncursor-v3-693c0fb` |
| Source commit | `693c0fb26fa4e0c4f54e63b52497783c4ce60131` |
| Source tree SHA-256, before and independently after | `87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1` |
| Diagnostic implementation commit | `a7c72933d2dc60979a1607a47cfe7e5747c84cbe` |
| Diagnostic root | `C:\tmp\formal-rigor-v3-posthoc-diagnostic-a7c7293` |
| Final diagnostic tree SHA-256 | `35283d05bc288271a7c963fecada9854f03336ff2985eed47cfb00f4c717f252` |
| Semantic plan canonical-JSON SHA-256 | `9b5e622811a22a0393eb21f3237d33b59088102f23c92390384016f7809d8e91` |
| Literal `semantic-plan.json` file SHA-256 | `b548df186062f0bbbf3a03ba5d1e89da8c611801aa4bb66557a7aaa4ccb99400` |
| Codex judge binding | Codex CLI 0.144.6, `gpt-5.6-sol`, high |
| AGY judge binding | AGY 1.1.7, `gemini-3.1-pro-high`, high |
| AGY timeout contract | `--print-timeout 10m`; outer subprocess 720 seconds |

The diagnostic root was verified nonexistent before preparation. Structural
preparation checked the source pin, and the source pin was independently
recomputed after all provider work. The diagnostic tree pin was computed only
after both harnesses and the summarizer had exited and the root was quiescent.

The sealed execution retained each prompt SHA-256 in `semantic-plan.json` and
the corresponding call identity, but it retained zero raw prompt files. A
read-only, no-provider reconstruction regenerated all 130 exact prompts from
the frozen views, rubric, schema, provider plan, and harness identity; all 130
matched the retained hashes. The sealed root was not changed or repinned. This
is an evidence-retention limitation, not a basis to repair the run or award
release credit.

## Population and structural results

| Population | Planned | Content-bearing | Normalized | Missing | Scorable | Passing |
|---|---:|---:|---:|---:|---:|---:|
| All arms, intent-to-test | 286 | 215 | 11 | 71 | 215 | 100 |
| Candidate | 66 | 65 | 3 | 1 | 65 | 49 |
| Candidate excluding normalized views | 62 | 62 | 0 | 0 | 62 | 47 |

The source classifications reconcile exactly as 204 `original_qualifying`, 11
`normalized_identical_repeated_frames`, and 71 `missing_no_content`. The
conditional-on-content structural pass rate is 100/215 (46.51%); the
intent-to-test rate is 100/286 (34.97%). Candidate passing is 49/65 available
(75.38%) or 49/66 planned (74.24%). Excluding the three normalized candidate
views yields 47/62 (75.81%); two of the three normalized candidate views pass.
The aggregate conclusion is therefore not driven by normalization, although
the normalized subset is too small for a strong sensitivity claim.

### Structural results by arm

| Arm | Planned | Content | Normalized | Missing | Passing/content |
|---|---:|---:|---:|---:|---:|
| `v2-candidate` | 66 | 65 | 3 | 1 | 49/65 |
| `neutral` | 44 | 43 | 4 | 1 | 5/43 |
| `v1-current` | 44 | 41 | 4 | 3 | 8/41 |
| `parody-always-cautious` | 22 | 22 | 0 | 0 | 1/22 |
| `parody-closed-taxonomy` | 22 | 22 | 0 | 0 | 18/22 |
| `parody-formal-only` | 22 | 22 | 0 | 0 | 19/22 |
| `parody-always-decide` | 22 | 0 | 0 | 22 | unavailable |
| `parody-full-ceremony` | 22 | 0 | 0 | 22 | unavailable |
| `parody-jargon-only` | 22 | 0 | 0 | 22 | unavailable |

The candidate separates from neutral, current-v1, and always-cautious, but it
does not separate from closed-taxonomy or formal-only; both observed parodies
have higher pass proportions. The three entirely absent AGY parody arms are not
imputed. Available structural controls therefore do not establish broad control
polarity or candidate-to-parody separation.

### Candidate structural subgroups

| Subgroup | Planned | Content | Normalized | Missing | Passing/content |
|---|---:|---:|---:|---:|---:|
| Repetition 1 / OpenAI origin | 22 | 22 | 0 | 0 | 19/22 |
| Repetition 2 / Google origin | 22 | 21 | 3 | 1 | 9/21 |
| Repetition 3 / OpenAI origin | 22 | 22 | 0 | 0 | 21/22 |
| OpenAI origin, combined | 44 | 44 | 0 | 0 | 40/44 |
| Google origin | 22 | 21 | 3 | 1 | 9/21 |

The provider-linked difference is large: 40/44 (90.91%) for OpenAI-origin
content versus 9/21 (42.86%) for available Google-origin content. Missingness
is non-random, so this is a subgroup observation, not a provider causal effect.
Within candidate content, P0 passes are 24/33, controls 8/12, and traps 41/53.
Provider and repetition are perfectly confounded: repetitions 1 and 3 are
OpenAI-origin, while repetition 2 is Google-origin. No provider effect can be
separated from repetition effects.

## Semantic results

Exactly 130 ordered seats were planned, attempted once, and terminally sealed.
There are 130 `attempt.json` records and 130 `call.json` seals. No terminal or
incomplete seat was retried.

| Judge / origin | Planned seats | Terminal | Valid seats | Seat verdicts | Candidate interpretation |
|---|---:|---:|---:|---|---|
| OpenAI Codex judging Google-origin candidate content | 42 | 42 | 42 | 38 `VALID`, 4 `INVALID` | 19 PASS, 2 genuine FAIL |
| Google AGY judging OpenAI-origin candidate content | 88 | 88 | 0 | 88 quota/transport failures | 44 inconclusive |

The aggregate report's `verdicts` map counts only the 42 valid parsed Codex
adjudications: 38 `VALID` and four `INVALID`. It omits the 88 sentinel
`INCONCLUSIVE` entries created for unavailable AGY judgments, so it is not a
130-seat verdict histogram.

Every AGY terminal record has exit code 1, `transport: failed`, a clean secret
screen, an `Individual quota reached` error, and zero input, output, and total
tokens. These are provider-availability failures, not timeouts, schema failures,
or semantic merit judgments.

| Frozen aggregate outcome | Candidates | Interpretation |
|---|---:|---|
| `PASS` | 19 | Both Codex seats returned `VALID` |
| `FAIL` | 24 | Two semantic invalidities plus 22 availability-driven P0 fail-closed cases |
| `ARBITRATION_REQUIRED` | 22 | P1 cases with two unavailable AGY judgments |
| Missing source candidate | 1 | Repetition 2, `um-02-external-regulatory-semantics` |

The two genuine semantic failures are repetition-2
`tm-02-isolation-name-is-not-semantics` and
`tm-03-consistency-is-not-one-chain`; both are P0 and both received paired
`INVALID/INVALID` Codex verdicts. The other 22 P0 findings are OpenAI-origin
cases with paired `INCONCLUSIVE/INCONCLUSIVE` entries because AGY returned no
judgment. Their mechanical `FAIL` label follows the preregistered fail-closed
rule and must not be read as semantic invalidity. The 22 P1 OpenAI-origin cases
are correspondingly `ARBITRATION_REQUIRED`. There was no paired-seat dissent.

Accordingly, the report's 24 `p0_findings` and aggregate 24 `FAIL` rows each
combine two genuine merit failures with 22 quota-driven fail-closed outcomes;
neither field is a semantic-invalid count.

The 19/21 pass result for Google-origin candidates is bounded positive evidence
for that observed subgroup. It is counterbalanced by two genuine P0 failures,
the absence of any valid AGY semantic judgment for 44 candidates, structural
provider divergence, incomplete control polarity, and non-random missingness.
No semantic control or parody response was judged, so semantic separation from
controls cannot be claimed.

All three normalized candidate views (`mt-03`, `ot-01`, and `tm-04`, repetition
2) received paired `VALID/VALID` judgments. Excluding them changes the available
genuine semantic subset from 19/21 passing to 16/18 passing. Neither genuine
failure is normalized, so normalization does not remove the two P0 failures.

## No-retry and integrity accounting

- Structural phase: 215 retained views and 215 structural score records.
- Codex phase: 42 attempts, 42 terminal seals, 42 valid adjudications.
- AGY phase: 88 attempts, 88 terminal seals, 88 quota/transport failures, zero
  tokens, zero valid adjudications.
- Total semantic phase: 130 attempts and 130 seals; no retry, replacement,
  repair, or hidden arbitration.
- Source pin after the run matches the preregistered source pin exactly.
- The final quiescent diagnostic root contains 1,039 files and is bound by the
  diagnostic tree SHA-256 above.

## Limitations and interpretation boundary

- This is post-hoc evidence over an excluded epoch and awards no release credit.
- Missingness is substantial and non-random: 71/286 arms lack model content and
  one of 66 candidate responses is unavailable.
- The two seats per candidate used isolated contexts but the same judge model
  and provider, so they are correlated observations, not independent model
  families.
- Origin provider, repetition, and judge availability are perfectly confounded:
  Codex judged only repetition 2 / Google-origin content, while AGY judged only
  repetitions 1 and 3 / OpenAI-origin content. The data do not identify a
  provider effect, repetition effect, or crossed judge-provider effect.
- AGY quota prevented all semantic judgments of OpenAI-origin candidate
  responses. Cross-provider semantic coverage is therefore one-sided.
- Three AGY parody arms are entirely missing, and no control/parody received
  semantic adjudication.
- Eleven structural views rely on byte-identical repeated-frame normalization;
  they remain diagnostic views and do not retroactively satisfy V3 transport.
- Structural conformance is not semantic correctness. The observed parodies
  demonstrate incomplete structural polarity.
- The local diagnostic root is external to Git; its tree pin identifies the
  retained root but does not turn it into committed release evidence.
- The sealed root retains prompt hashes rather than raw prompt files. Although
  all 130 prompts reconstruct to those hashes, the missing raw files remain a
  disclosed limitation of the already completed run.

These results neither close the formal-rigor behavioral gate nor justify a
numeric posterior or an all-286 merit rate. V3 remains excluded, and 3.0.0
remains **HOLD**.

## Independent review

Independent read-only review covered the frozen design, implementation diff
from `60d4ffc44ed06e0771f843273f7a04b942f41762` through
`a7c72933d2dc60979a1607a47cfe7e5747c84cbe`, diagnostic manifest, structural
and semantic aggregates, source and diagnostic pins, and this documentation.
It explicitly checked source-root mutation, normalization overreach, hidden
release promotion, provider/seat identity, rubric leakage, verdict consistency,
and unsupported confidence claims.

The review found no Critical issue and returned conditional approval after
requiring the valid-only verdict-map interpretation, the two-merit-versus-22-
availability P0 decomposition, perfect provider/repetition/judge confounding,
the canonical-versus-literal semantic-plan hash distinction, and normalized
semantic sensitivity. Those corrections are incorporated above. No reviewer
dissent remains unresolved; the provider confounding, missing AGY judgments,
correlated seats, and missing parody arms remain substantive limitations.
