# 08 — Changes and verification

## Change policy

The packet requires observed RED before behavior-changing fixes, the smallest coherent correction, focused GREEN, then full-suite GREEN. Existing PR #43 was independently reviewed rather than trusted. Its source fixes were retained only where their failing and passing evidence could be re-derived. PR #43 history was not rewritten because the packet makes rewrite ask-first and no approval was supplied.

## Verified RED → GREEN cycles

### 1. Gemini context inventory drift

**Observation.** At subject baseline `9532a57199fc8d4747a91916d59d1ea86c34d838`, `GEMINI.md` said “eight packages: router + six disciplines + the helix tandem entry point,” contradicting README, router, manifests, and eleven skill directories.

**Violated contract.** One canonical skills tree and accurate harness context; Gemini may adapt discovery, not redefine package cardinality.

**RED.** Commit `276a18592d675346e6b5e755fa7762e94c28c4f9` added package-integration assertions requiring `eleven skills` and `nine disciplines`. GitHub Actions run `30010658087` failed at “Outsource packet and package integration.”

**First fix still RED.** A source correction split `nine disciplines` across a line break, so the exact regression-readable invariant still failed in run `30010732005`. The assertion was not weakened.

**Smallest fix.** Keep the corrected cardinality and make the phrase contiguous in `GEMINI.md`.

**GREEN.** Commit `c5cc63757b2bed8576be445181f03fae031329d0`; run `30010788937` succeeded. The replacement branch carries the same corrected blob `692bd2421770e8cd67f9cf456dcba1bd3578510f` and same regression assertions.

**Residual.** Native Gemini extension validation/discovery remains source-only.

### 2. Canonical CI omitted deterministic suites

**Observation.** `.github/workflows/epistemic-flexibility.yml` did not execute continuity committed-result scoring or `.github/scripts/test_check_dco.py`, although both were load-bearing to the full-suite and contribution-policy claims.

**Violated contract.** One canonical clean-checkout verification path for deterministic repository checks; OUT-010 may not rely on commands absent from that path.

**RED.** Commit `2a28035aeb90fd6455d3497659e839da94fb7133` added integration assertions requiring both workflow commands. Run `30011093669` failed.

**Smallest fix.** Extend the existing workflow with:

- continuity scorer runs for skilled 1–3, baseline 1–3, and parody 1 with expected pass/fail polarity; and
- `python .github/scripts/test_check_dco.py`.

No second runner or weakened assertion was introduced.

**GREEN.** Commit `16e633edbc1b945a846ab5d71af7d8662d87edf6`; run `30011183031` succeeded. The replacement branch carries the same workflow blob `79abd76cd1774fd00bcdb9e9353842db9cffcee5`.

**Residual.** Deterministic CI still cannot prove native harness execution or independent judgment.

### 3. README canonical-core count drift

**Observation.** README's layout comment said “canonical skill cores (ten)” while the package had eleven directories and product prose said eleven.

**Violated contract.** Documentation inventory must match the canonical tree and package integration.

**RED.** Commit `67a975bec8b5e263af7a4f14c92d952274939130` added assertions requiring `canonical skill cores (eleven)` and forbidding `(ten)`. Run `30011818244` failed.

**Smallest fix.** One word in README: ten → eleven.

**GREEN.** Commit `ccd584a50d7179024619cfff134a9962e57c486e`; run `30012138873` succeeded. The replacement branch carries the same README blob `faee029c8352ca75086d8b7a898f47c54f70526b`.

**Residual.** Native loader enumeration remains untested.

## Publication-integrity defects found during continuation

These are report/completeness corrections, not new runtime behavior; they were verified by direct repository inspection and did not justify edits to skill semantics.

| Finding in PR #43 head `03c167...` | Direct proof | Smallest correction in replacement |
|---|---|---|
| Index linked `08-changes-and-verification.md`, `09-final-verification.md`, `decision-ledger.jsonl`, and a blocked Gauntlet record that did not exist. | Exact-path fetches at PR head returned 404. | Publish the missing files and remove broken completion implications. |
| Superpowers matrix claimed stage coverage but omitted pinned `writing-skills`. | Set comparison: fourteen relevant v6.1.1 skills vs thirteen rows. | Add the missing row and explicit non-use rationale; no workflow behavior edit. |
| Audit prose called `9532a...` the packet commit. | Immutable prompt packet is `532a0...`; handoff labels `9532a...` as baseline parent. | Separate packet, subject baseline, and prior-PR head in every report. |
| Audit prose said Consensus/Scite/library execution was unavailable. | Consensus discovery executed; Scite returned quota exhaustion; no library action existed. | Report exact per-layer capability and keep incomplete triad open. |
| PR #43 was described as reviewable despite DCO failure on every commit. | PR checks and handoff independently record author/signoff mismatch. | Preserve #43, build clean replacement from packet/main with author-matching dual sign-offs, open superseding PR. |

## Replacement branch construction

Branch `audit/epistemic-suite-stress-test-2026-07-23-r2` was created from exact packet/main commit
`532a0ce86fea908113cbca2a600fb21238e473f1`. Source changes were reapplied without rewriting #43:

| Replacement commit | Content |
|---|---|
| `a56d77fdf274a8a37e3510cd0017830172abbce8` | Correct Gemini inventory. |
| `20af767e8caf67475379e869d720230e08216d17` | Add continuity/DCO deterministic workflow steps. |
| `5dda6424f84037f5392deb9537624c2721db0c31` | Consolidate verified integration assertions. |
| `9642ef8b705370ca6d1ceebd6e812a82744bcff4` | Correct README canonical-core count. |

Every replacement commit carries sign-offs for both the GitHub noreply identity
`SternOne <89846440+SternOne@users.noreply.github.com>` and the public profile email
`SternOne <zachstern@gmail.com>`. DCO result for the opened replacement PR is recorded in report 09.

## Scope control

No `SKILL.md` semantics, schemas, manifests, versions, releases, settings, or main history were changed. The replacement retains the three independently verified source fixes and adds only the audit/verification artifacts needed to satisfy the packet as far as current capabilities allow.

## Remaining risk

- OUT-009 has no valid independent panel or verified run record.
- Native behavior across all seven harness surfaces is source-only.
- UAT has no rendered target.
- Evidence-research has live discovery but not reception/holdings closure.
- Fixture and deterministic batteries are narrow smoke/calibration evidence, not real-world rates or universal judgment truth.
