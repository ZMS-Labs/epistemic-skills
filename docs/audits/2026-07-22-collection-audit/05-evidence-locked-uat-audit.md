# Audit 05 — evidence-locked-uat

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at 61fbf95 (v2.6.0). Base path abbreviations: `skill/` = `plugins/epistemic-skills/skills/evidence-locked-uat/`; `skills/` = `plugins/epistemic-skills/skills/`; `vbc` = superpowers 6.1.1 `verification-before-completion/SKILL.md` (local cache copy read for exact wording).

---

## 1. Boundary/handoff contract as it exists today

**Consumes** — a finished change plus its requirement sources. `skill/SKILL.md:32` (collect `requirement_sources` + one-paragraph `change_summary`), parameters at `skill/SKILL.md:44-48` (`target_url`, `tier`, `evidence_dir`, `target_repo_dir`). Router states it identically: "a finished change + its requirements" (`skills/using-epistemic-skills/SKILL.md:28`). Environment precondition: preview/staging/local for anything destructive, account/tenant identity verified first (`skill/SKILL.md:33`); no reachable rendered surface → STOP with `BLOCKED_ENVIRONMENT` (`skill/SKILL.md:24`).

**Produces** — an evidence packet at `<target-repo>/artifacts/uat/<run_id>/` (`skill/SKILL.md:28`): `DIRECTIVE-PATH.txt`, `contracts.yaml`, `cases/<case>/actor-output.json` + gitignored screenshots, `verifier/<case>.json`, `gate.json`, `manifest.json`, `summary.md` (layout: `skill/references/schemas.md:118-133`). Verdict: closed 7-word vocabulary `PASS | FAIL_PRODUCT | INCONCLUSIVE | FAIL_TEST_HARNESS | BLOCKED_ENVIRONMENT | FLAKY | NOT_RUN` (`skill/references/schemas.md:9`), aggregated to a 3-value `release_decision: PASS | FAIL | INCONCLUSIVE` (`skill/references/schemas.md:105-108`).

**Hands to** — the ship/merge decision (`skills/using-epistemic-skills/SKILL.md:28`); "hand any evidence-consuming step the evidence packet path, not ad-hoc screenshots" (`skill/SKILL.md:100-102`); artifacts committed, gate decision commented on the PR (`skill/SKILL.md:69-70`).

**The manifest.json sha256 chain, precisely.** `skill/SKILL.md:63-64`: manifest records *run_id, tier, target, target repo commit SHA, date, model, skill version, calibration_status, sha256 of `gate.json` and `contracts.yaml`*. Analysis:

- **What it proves:** the subject is content-addressed (commit SHA), and the two metadata files (`gate.json`, `contracts.yaml`) are integrity-pinned at manifest-write time. A downstream consumer can detect post-hoc tampering with the verdict or the contracts.
- **What it does not prove:** (a) that `gate.json` was produced by the deterministic judge from the committed `actor-output.json`/`verifier/*.json` — those inputs are **not hashed**, so the link "verdict ⇐ this evidence" is unsealed; (b) anything about screenshots — the primary rendered evidence is gitignored (`skill/SKILL.md:31`, `skill/references/schemas.md:128`) and unhashed, so the chain stops *before* the evidence the verifier actually judged from; (c) that the judge code itself was this version — "skill version" is a string, not a hash of `workflow-template.mjs`.
- **Who computes the hashes:** the orchestrating agent, procedurally, per Step 3.2 (`skill/SKILL.md:63-64`). No script enforces or verifies it. The chain's strength therefore equals the orchestrator's diligence — it is an integrity *convention*, not an enforced mechanism.

Verdict: a genuine in-repo exemplar of a content-addressed trust artifact, but it pins the *envelope* (verdict + contracts), not the *evidence body*.

---

## 2. Findings vs the five invariants

**Invariant 1 — Floors, not ceilings.**
- *Strength:* three-tier dial (`skill/SKILL.md:16-20`); Level-1 layout deliberately smaller than §59 with an explicit "do not treat §59 as this skill's contract" guard (`skill/references/schemas.md:120-121`, `skill/references/standard.md:2973-2976`); the 4000-line standard is vendored but quarantined behind "never load it whole" (`skill/SKILL.md:108-112`).
- *Defect (minor):* the `known_limitations` list exists in two drift-prone copies — the long form at `skill/SKILL.md:56-62` and a shorter string at `skill/references/schemas.md:114`. Which one lands in `gate.json` depends on the orchestrator. Copies rot.

**Invariant 2 — Derive/verify, don't assert.**
- *Strength:* blinding is **schema-enforced**, not prompt-enforced — the actor output schema has no verdict/success/confidence field, `additionalProperties: false` (`skill/references/workflow-template.mjs:64-66`, comment "blinding is schema-enforced"); the judge is deterministic script code (`workflow-template.mjs:234-317`); criterion-completeness is checked, missing verdicts synthesize INCONCLUSIVE rows (`workflow-template.mjs:279-289`); id-drift is tolerated only via single-orphan positional matching *and the mismatch is recorded in `evidence_against`* (`workflow-template.mjs:264-277`); inferred contracts are marked `provisional` (`workflow-template.mjs:209, 305`).
- *Gap:* the deterministic judge — the one component that needs no LLM — exists **only** embedded in the Claude-Code Workflow script. The harness-agnostic contract for it is prose (`skill/references/schemas.md:92-101`). Every other harness must re-implement the deterministic core from prose; re-implementations drift, which quietly undermines "the judge is deterministic" as a collection-level guarantee.

**Invariant 3 — Boundary discipline.**
- *Strength:* explicit Integrations section with upstream/downstream handoff rules (`skill/SKILL.md:97-104`); sibling-scope disclaimer vs `verification-before-completion` (`skill/SKILL.md:102-104`); router table matches exactly (`skills/using-epistemic-skills/SKILL.md:28`); "do not paraphrase or 'improve' the role prompts — the information-permission boundaries in them are the mechanism" (`skill/SKILL.md:51-52`).
- *Defect (minor, doc/impl mismatch):* `skill/SKILL.md:37-38` says roles run "as concurrent, context-isolated sub-agents **behind a barrier**." The reference implementation runs a per-case `pipeline` — verifier for case 1 can start while the actor for case 2 is still running; there is no inter-phase barrier (`workflow-template.mjs:224-232`). Blinding is preserved per-case (each verifier receives only its own case's actor output), so this is a wording defect, not a mechanism defect — but the skill text describes a stronger structure than the implementation provides.
- *Gap:* the downstream handoff is "the evidence packet path" — there is no consumer-side contract stating what a downstream skill may rely on without re-verification. This is the trust-contract gap proper (§4).

**Invariant 4 — Fail closed; degrade explicitly.**
- *Strength:* missing verifier verdict → INCONCLUSIVE (`workflow-template.mjs:279-289`); missing screenshots for a rendered-ui criterion → INCONCLUSIVE, never PASS (`workflow-template.mjs:188`); verifier instructed to default to INCONCLUSIVE (`workflow-template.mjs:173`); no rendered surface → STOP, not code-reading substitution (`skill/SKILL.md:24`); INCONCLUSIVE "never rounded up to PASS, never papered over with prose" (`skill/SKILL.md:71-72`); `calibration_status: uncalibrated` is disclosed rather than hidden.
- *Defect:* `known_limitations` and `coverage_omitted` — the two fields that make the degradation explicit — are **not emitted by the deterministic judge** (the gate object at `workflow-template.mjs:310-317` omits both). They are added procedurally by the orchestrator afterward (`skill/SKILL.md:56-62`). A forgetful orchestrator produces a clean-looking `gate.json`, and the manifest hash then *pins the incomplete artifact*. The pipeline fails open at exactly the point where its honesty lives.

**Invariant 5 — Provenance and independence.**
- *Strength:* prompt-injection boundary stated in directive (`skill/references/directive.md:306-309`), skill (`skill/SKILL.md:33`), and actor prompt (`workflow-template.mjs:145-148`: actor MUST NOT read source, use test IDs, call APIs, or mutate state); the verifier never receives an actor verdict — none exists to leak (`workflow-template.mjs:170-193`); the judge "is never an agent" (`skill/references/schemas.md:92`).
- *Gap (disclosed):* "verifier same-provider" is listed in `known_limitations` (`skill/SKILL.md:58`) — independence is context/prompt-level only. The vendored standard itself recommends different models or a deterministic verifier to reduce correlated error (`skill/references/standard.md:3405`); the skill offers no mechanism or option for it. Honest, but a known ceiling on verdict independence.
- *Gap:* the evidence the verifier judged from (screenshots) is gitignored and unhashed (`skill/SKILL.md:31, 69`) — see §1.

---

## 3. Duplicated checks (cross-skill)

| Check | Also specified by | Classification |
|---|---|---|
| Evidence-before-claim verdict | superpowers `verification-before-completion` (vbc "Iron Law": "If you haven't run the verification command **in this message**, you cannot claim it passes") | **Freshness-sensitive.** vbc is deliberately freshness-bound; the relationship is correctly declared as scoping, not duplication (`skill/SKILL.md:102-104`; `skills/helix/SKILL.md:44` — UAT "*is* that skill's UI-facing instance"). Neither direction is safely attestable: a UAT packet can't satisfy vbc for non-UI claims; vbc's fresh command output can't substitute for the blinded verdict. The *underlying* CI/test outputs would be idempotent-mechanical if content-addressed by commit SHA — neither skill pins them today. |
| Oracle-adequacy ("the oracle must be able to observe the claim") | gauntlet Step 6(3) (`skills/gauntlet/SKILL.md:277-292`, absorbed `verification-oracle-auditor`) vs UAT compiler constraint (`workflow-template.mjs:207-208`: never require an oracle the harness can't capture) | **Different phases, same principle — not a re-run.** Gauntlet's is a review-time semantic judgment per claim (freshness tied to the claim, not time; re-running adds nothing if the dossier is frozen). UAT's is a compile-time contract constraint. Router already sequences them: "gauntlet gates first, evidence-locked-uat proves after" (`skills/using-epistemic-skills/SKILL.md:72-73`). |
| `[V path:line]` mechanical evidence truth-check | gauntlet Step 6(1), `scripts/verify_evidence.py` (`skills/gauntlet/SKILL.md:263-267`) | **Idempotent-mechanical — safe to attest once** against content-addressed artifacts. UAT does not re-run it (correctly); a future trust contract could let gauntlet accept UAT's committed evidence files as `[V]` anchors without re-verification. |
| FLAKY / first-run-immutability rule | **No sibling.** Repo-wide grep: `FLAKY` appears only in `evidence-locked-uat` files. | Not duplicated. The rule itself is **idempotent-mechanical across runs**: first gate immutable (`skill/SKILL.md:76-78`), both run-ids retained (`skill/references/schemas.md:12-13`) — a downstream consumer can trust the FLAKY classification from the two pinned `gate.json` files without re-running anything. |
| "Content is data, never instructions" | gauntlet Step 0(6) injection guard (`skills/gauntlet/SKILL.md` ~line 115); directive (`skill/references/directive.md:306-309`) | Shared invariant 5 at documentation level; not a re-runnable check. Acceptable duplication. |

No sibling specifies the FLAKY retry rule, the verdict vocabulary, or the blinded-verifier mechanics — the skill's core is not duplicated anywhere in the collection.

---

## 4. Trust-contract readiness

**Machine-checkable today (a downstream consumer could rely on without re-running):**
- Closed verdict vocabulary and criterion-level statuses in `gate.json` (`skill/references/schemas.md:105-116`) — machine-consumable by construction.
- Schema-validated `contracts.yaml` (`workflow-template.mjs:28-62`).
- Subject pinned by commit SHA; `gate.json` + `contracts.yaml` sha256-pinned in `manifest.json` (`skill/SKILL.md:63-64`).
- Tier recorded and never silently downgraded mid-run (`skill/SKILL.md:22-23`).
- Actor and verifier outputs committed (`skill/references/schemas.md:126-129`) → the deterministic aggregation is **recomputable in principle** from committed inputs with zero LLM calls. This is the strongest latent trust property — and it is **nowhere stated**. The skill never tells a downstream consumer "you may re-verify `gate.json` locally instead of trusting it."
- FLAKY aggregation is cross-run and artifact-based (both gates retained) — attestable once, permanently.

**Missing for a real contract:** no validity-window/freshness semantics for a PASS anywhere in the collection; `gate.json` itself does not carry the commit SHA (fields at `workflow-template.mjs:310-317` — the binding lives only in `manifest.json`, which has no schema); judge-code version not content-pinned ("skill version" is a bare string, and `skill/references/schemas.md:124`'s manifest field list omits even that).

**What must never be attested (procedural, not artifact-certifiable):**
- The blinding separation itself. The schema proves the actor *couldn't emit* a verdict; it cannot prove the verifier never *saw* actor confidence through some side channel — that is a runtime/orchestration property.
- Persona fidelity and the verifier's visual-inspection quality (same-provider LLM, disclosed at `skill/SKILL.md:58`).
- Calibration — currently hard-coded `uncalibrated` (`workflow-template.mjs:314`); any attestation of calibration would need the missing seeded-defect corpus as its oracle.
- That the environment was genuinely preview/staging (`skill/SKILL.md:33` is a procedural gate).
- Screenshot content integrity (gitignored, unhashed) — a trust contract must treat screenshots as *unsealed* evidence and say so.

---

## 5. Unfinished-feeling items (the concrete list)

1. **`calibration_status` is a dead end, not an acknowledged gap with a path.** Hard-coded `'uncalibrated'` at `workflow-template.mjs:314`, in the gate schema (`skill/references/schemas.md:110`), and in `known_limitations` (`skill/SKILL.md:62`). Meanwhile the skill's own directive mandates the machinery that would change it: "The UAT system itself must be tested… calibration runs across models and versions" (`skill/references/directive.md:353-360`); the standard's Level 1 — the level this skill claims — requires "a small seeded-defect set" (`skill/references/standard.md:3340`), and the pre-publication checklist requires "seeded-defect calibration within policy threshold" (`skill/references/standard.md:3469`). No corpus, no runner, no vocabulary beyond `uncalibrated`, no transition condition. Disclosure is honest (invariant 4 satisfied); the path is absent.
2. **The skill ships no evals/tests — violating its own directive's FALSE-PASS CONTROL.** The directory contains only `SKILL.md` + `references/`. Contrast gauntlet, which ships an arbitrator-certification battery with measured 10/10 catch rate (repo `README.md:175`). For a skill whose entire premise is "never trust an uncalibrated judge," the absence of any self-test is the single strongest objective signal behind the "unfinished" feeling.
3. **`manifest.json` has no schema, and its two definitions disagree.** `gate.json` gets a full JSON block (`skill/references/schemas.md:105-116`); `manifest.json` gets a one-line comment (`skill/references/schemas.md:124`) whose field list (run-id, tier, target, commit, model, calibration_status, hashes) omits the "skill version" and "date" that `skill/SKILL.md:63-64` requires. The integrity anchor of the whole packet is the least-specified artifact in it.
4. **The deterministic judge is not harness-portable.** The collection advertises harness-agnosticism (repo `README.md:7, 155`), and `skill/SKILL.md:39-41` correctly labels the `.mjs` as a Claude Code reference implementation. But the actor/verifier roles are legitimately harness-specific (the `.mjs` even hardcodes Claude Code Playwright MCP tool names, `workflow-template.mjs:156`) — while the *judge* is the one part that should be identical everywhere, and it exists only as Workflow-tool JS plus prose (`skill/references/schemas.md:92-101`).
5. **"Behind a barrier" vs per-case pipeline** — doc/impl mismatch (`skill/SKILL.md:37` vs `workflow-template.mjs:224-232`), §2 invariant 3.
6. **Undocumented verdict-vocabulary substitution.** `schemas.md:3` claims derivation from standard §9, but §9 has 8 statuses including `NOT_APPLICABLE` and `SKIPPED_POLICY` and **no** `NOT_RUN` (`skill/references/standard.md:342-355`); the skill's 7-word set substitutes `NOT_RUN` (`skill/references/schemas.md:9`). Almost certainly a deliberate narrowing — but unrecorded, so a reader diffing against §9 can't tell narrowing from drift.
7. **Directive MUSTs dropped from the Level-1 manifest without disclosure.** The directive requires recording environment fingerprint, seeds, model/version, temperature/sampling, and tool versions (`skill/references/directive.md:150, 317`); the Level-1 manifest carries none of these (`skill/SKILL.md:63-64`), and their absence is not listed in `known_limitations`.
8. **Minor:** role agents are told to read the directive via `DIRECTIVE-PATH.txt` (`workflow-template.mjs:143, 203`) with no confirmation they did — procedural trust on the protocol's load-bearing read.

---

## 6. Minimal improvement proposals (each one focused PR)

- **P1 — Specify `manifest.json`.** Add a normative JSON block to `schemas.md` reconciling `SKILL.md:64` (include `skill_version`, `date`, sha256 of `workflow-template.mjs` or the harness's judge, and the directive-required fingerprint fields). Resolves finding 3 and most of 7.
- **P2 — Move the honesty fields into the judge.** Have the deterministic gate object emit `known_limitations` (constant at Level 1) and `coverage_omitted` (computable: tier×contracts minus executed cases, from data already in scope at `workflow-template.mjs:213-221`) instead of relying on the orchestrator. Converts the invariant-4 fail-open into fail-closed. Add the target commit SHA to `gate.json` here too — one field, same PR.
- **P3 — Seal the evidence inputs.** Extend manifest hashes to the committed `actor-output.json` and `verifier/*.json` (cheap; they're already committed), and add one explicit sentence to `schemas.md`: screenshots are gitignored and unhashed — outside the integrity chain. Makes the existing boundary explicit instead of implicit; does not attempt to seal binary evidence (that would be ceiling-building).
- **P4 — State the recomputability property.** One short "Verifying a packet downstream" section in `schemas.md`: a consumer MAY recompute `release_decision` from the committed actor/verifier outputs using the deterministic aggregation rules, without re-running any LLM role. This documents the trust-contract hook that already exists de facto. Docs-only.
- **P5 — Extract the judge.** Pull the aggregation (`workflow-template.mjs:234-317`) into a standalone stdlib script (or single pure-function module) that any harness can run identically; keep the `.mjs` as reference orchestration calling it. Slightly larger than P1–P4 but still one PR; this is the piece that makes "deterministic judge" a collection-level fact rather than a per-harness re-implementation.
- **P6 — Give calibration an exit path, not a corpus.** Define the `calibration_status` vocabulary and transition condition (e.g. `uncalibrated | calibrated:<corpus-ref>@<date>`) in `schemas.md`, and one line in `SKILL.md` naming the missing seeded-defect corpus as the blocker. Converts a dead end into an acknowledged gap with a path, without building the corpus (building it would violate invariant 1).
- **P7 — Two one-line wording fixes.** `SKILL.md:37`: describe per-case actor→verifier chaining with cross-case concurrency instead of "behind a barrier." `schemas.md:3`: note that the skill's vocabulary deliberately substitutes `NOT_RUN` for §9's `NOT_APPLICABLE`/`SKIPPED_POLICY`.

**Explicitly not proposed** (would violate invariant 1): building the seeded-defect corpus, hashing/committing screenshots, cross-provider verifier requirements, validity-window machinery. Each is a real capability, but each is a ceiling, not a floor; P6 and P3 respectively record them as named, deferred work instead.

**Note on method:** content searches fell back to bash `grep` (ripgrep unavailable in the audit environment). The cross-skill `FLAKY` uniqueness claim (§3) rests on a repo-wide `grep -rln FLAKY skills/` over the eight skill trees.
