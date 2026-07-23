# 01 — Inventory and baseline

## Re-anchored state digest

This audit began from the outsource handoff, so `continuity-verify` fired before any resumed-work claim was trusted. The durable anchors are the public repository and immutable packet commit, not the handoff prose by itself.

| Load-bearing claim from the handoff | Re-anchor | State |
|---|---|---|
| The packet to audit is `9532a57199fc8d4747a91916d59d1ea86c34d838`. | The requested `HANDOFF.md` and every source citation in this audit were fetched with that exact ref. | **verified** |
| The package is version `2.9.1`. | `README.md:7`; versioned Claude/Codex/Cursor/Gemini/Kimi manifests at the packet commit. | **verified** |
| There are eleven skills: router + nine disciplines + Helix. | `README.md:13-20,44-58`; eleven directories under `plugins/epistemic-skills/skills/`; integration test enumerates eleven. | **verified** |
| The target can work off `main` and open a PR. | Branch `audit/epistemic-suite-stress-test-2026-07-23` was created from the packet commit; draft PR #43 is open against `main`. | **verified** |
| Existing deterministic checks pass. | Re-executed in GitHub Actions clean checkout. The expanded workflow passed at commit `16e633edbc1b945a846ab5d71af7d8662d87edf6`, run `30011183031`. | **verified for the commands in the workflow** |
| The target has isolated role contexts or equivalent. | No available tool exposes concurrent context-isolated role-agent invocation or a documented contract-equivalent separation primitive. | **(UNVERIFIED) / unavailable** |
| Proprietary harnesses can be exercised live. | No Claude Code, Codex plugin runtime, Cursor, Gemini CLI, Antigravity, or Kimi Code executable/session was available. | **(UNVERIFIED); source/deterministic tiers only** |
| A current final Gauntlet can be run. | Deterministic Gauntlet scripts/tests are available, but Step 5 requires isolated role calls; the run stops before panel execution. | **contradicted as an executable capability in this target** |

`accepted_unverified`: none. The unavailable independence and live-harness claims were not accepted as if verified; they remain limitations and force `PARTIAL`.

## Canonical inventory

All line citations below refer to the packet commit.

| Subject skill | Role and positive trigger | Produces / boundary | References, tests, or evals inspected | Baseline disposition |
|---|---|---|---|---|
| `using-epistemic-skills` | Router when multiple disciplines, ordering, resumption, or external work may apply; never performs the selected discipline (`SKILL.md:1-16,122-150`). | Auditable routing record plus pointers to member artifacts; ends at routing (`SKILL.md:23-42,113-120`). | `reference/epistemic-flexibility.md`; protocol fixtures; behavioral scorer fixtures; receipt contracts. | **SOUND — deterministic/source.** Live auto-trigger quality remains unmeasured. |
| `helix` | Fires when a workflow layer and epistemic layer coexist or sequencing is ambiguous (`SKILL.md:1-5`). | Pairing/position record only; neither routes within a collection nor executes the pair (`SKILL.md:19-33,67-115`). | Complete pairing table and co-fire checklist; Superpowers v6.1.1 sources. No dedicated behavioral harness. | **CONDITIONAL.** Mapping is coherent; live co-fire behavior is source-only. |
| `blindspot-pass` | Unfamiliar, non-trivial territory; concrete skip gate requires two landmines plus canonical example from memory (`SKILL.md:44-64`). | Four-section reconnaissance, rewritten request, and downstream handoff; edits are forbidden (`SKILL.md:66-121`). | `reference/blast-radius-quiz.md`; provenance statement; this suite reconnaissance. | **CONDITIONAL.** Boundary is crisp; no deterministic trigger/skip behavioral battery. |
| `applying-formal-rigor` | At least two viable options or a correctness/complexity justification; excludes pure preference and single-option mechanical work (`SKILL.md:18-25`). | Seven-lens derivation, explicit verdict, concession/synthesis; empirical facts remain conditional until preregistered test (`SKILL.md:42-89`). | `reference/theory-battery.md`; worked example; current inventory/CI alternative derivation. | **CONDITIONAL.** Strong method contract, no behavioral evaluation of under/overtriggering. |
| `evidence-research` | Scholarly claim or any Consensus/Scite/library call (`SKILL.md:1-5,61-90`). | Claim-evidence matrix, reception, holdings, and convergence state; never GO/NO-GO (`SKILL.md:36-59,92-114`). | Consensus/Scite/Zotero first-contact profiles and current mode/convergence rules. No live connector schemas were available. | **CONDITIONAL.** Source contract is coherent; triad execution untested here. |
| `write-goal` | Explicit goal-authoring/start intent only (`SKILL.md:28-36`). | Approved evidence-bound completion contract, optionally started by a host adapter; never executes or certifies (`SKILL.md:19-26,134-180`). | Goal types, proof bundle, proxy guard, host adapters, templates. | **CONDITIONAL.** No persistent-goal primitive or live consent flow was exercised. |
| `outsource` | External model/agent/process boundary or explicit durable GitHub handoff request (`SKILL.md:1-5,17-28`). | Committed `HANDOFF.md`, pointer prompt, readiness receipt; external result is not certified (`SKILL.md:50-84,125-174`). | `reference/HANDOFF_TEMPLATE.md`; `tests/run_tests.py`; this exact packet, branch, PR, and relay. | **SOUND — live repo-backed self-application plus deterministic checks.** |
| `gauntlet` | Explicit stress-test/gauntlet or high-impact, irreversible, hard-to-verify decision (`SKILL.md:43-65`). | Frozen dossier, isolated panel, mechanical evidence checks, Conflict Ledger, computed verdict, verified run record (`SKILL.md:77-149,177-386`). | Roster, selector, evidence verifier, role materializer, finalizer, run verifier, arbitrator certification, synthetic example, `tests/run_tests.py`. | **CONDITIONAL.** Deterministic core green; current isolated panel unavailable. |
| `evidence-locked-uat` | UI-facing acceptance with reachable rendered environment (`SKILL.md:1-5,16-26`). | Actor evidence packet, blinded verifier output, deterministic PASS/FAIL/INCONCLUSIVE judge (`SKILL.md:42-100`). | Directive, schemas, workflow template, canonical `scripts/judge.py --self-test`. | **CONDITIONAL.** Judge green; no UI target or isolated actor/verifier contexts. |
| `decision-ledger` | Consequential decision, assumption, or operator correction that a downstream consumer will cite (`SKILL.md:32-57`). | Append-only `ledger-entry@1` or stated skip; never verdict/authorization (`SKILL.md:59-105,121-152`). | JSON Schema, validator, ordinary and recurrent-correction examples; audit-local ledger. | **SOUND — schema/examples deterministic.** Completeness remains best-effort by design. |
| `continuity-verify` | Handoff/summary/resumption whose next step depends on prior-state claims (`SKILL.md:38-49`). | Re-anchored state digest; halts/rescopes on unaccepted uncertainty; never performs resumed work (`SKILL.md:50-101,113-131`). | Ten-fixture blinded smoke battery, deterministic scorer, three skilled runs, baselines, parody probe. | **SOUND at smoke scale.** Real-world catch rate is explicitly unmeasured. |

## Manifest and exposure inventory

| Surface | Packet-commit artifact | Declared version / discovery |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`; `plugins/epistemic-skills/.claude-plugin/plugin.json` | `2.9.1`; package points to the canonical skills and agents tree. |
| Codex | `.agents/plugins/marketplace.json`; `plugins/epistemic-skills/.codex-plugin/plugin.json` | `2.9.1`; `skills: "./skills/"`; custom Gauntlet roles require renderer/native registry bridge. |
| Cursor | `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json`, package manifest | `2.9.1`; local/team marketplace packaging; public listing not claimed. |
| Gemini CLI | `gemini-extension.json`, `GEMINI.md`, root `skills/` symlink | `2.9.1`; context entrypoint plus canonical tree. Packet source contained a stale eight-package statement, fixed on the audit branch. |
| Antigravity | `plugin.json`, root `skills/` and `agents/` links | Root marker declares name/description; its stated schema does not expose a version field. |
| Kimi Code | `.kimi-plugin/plugin.json` and package manifest | `2.9.1`; `skillInstructions` maps role isolation to separate `Agent` calls. |
| Generic Agent Skills | `plugins/epistemic-skills/skills/*/SKILL.md`, root `skills/` symlink | Canonical method files; no harness-specific copy. |

## Clean-checkout baseline commands

The PR workflow uses `actions/checkout@v4` on Ubuntu/Python 3.12, so these are clean-checkout observations rather than local-shell claims.

| Command / check | Observed at green run `30011183031` |
|---|---|
| `python plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/run_tests.py` | success |
| `python .../behavioral/run_tests.py` | success |
| `python plugins/epistemic-skills/skills/outsource/tests/run_tests.py` | success, including new Gemini and CI coverage assertions |
| Continuity scorer over skilled 1–3, baseline 1–3, parody 1 with expected pass/fail polarity | success |
| `python .github/scripts/test_check_dco.py` | success |
| `python -m py_compile ...` | success |
| Parse committed integration JSON | success |
| `python .../decision-ledger/reference/validate_examples.py` | success |
| `python plugins/epistemic-skills/contracts/verify_receipt.py --self-test` | success |
| `python .../evidence-locked-uat/scripts/judge.py --self-test` | success |
| `python .../gauntlet/tests/run_tests.py` | success |

The exact workflow is `.github/workflows/epistemic-flexibility.yml`. A green workflow proves these deterministic commands on its checkout; it does **not** prove live harness discovery, trigger quality, connector availability, rendered UAT, or panel independence.
