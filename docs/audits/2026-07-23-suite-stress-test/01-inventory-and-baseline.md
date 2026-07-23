# 01 — Inventory and baseline

## Provenance and resumed-state digest

This continuation was anchored to the immutable outsource packet
`532a0ce86fea908113cbca2a600fb21238e473f1`, not to remembered chat state or to the prose of the handoff alone. The packet names subject baseline
`9532a57199fc8d4747a91916d59d1ea86c34d838` and requires re-resolution of draft PR #43 before its claims bear load.

| Load-bearing claim | Direct re-anchor | State |
|---|---|---|
| The governing packet is the `r2-pr43-continuation` handoff. | `532a0ce86fea908113cbca2a600fb21238e473f1:docs/outsource/epistemic-skills-suite-stress-test/HANDOFF.md`. | **verified** |
| PR #43 remained at the recorded stable snapshot. | GitHub PR metadata was re-read; head remained `03c16761d67f047b0ffb8a73b9d0b09b65045127`, draft/open and mergeable. | **verified; no drift observed** |
| PR #43 could be repaired in place without new authority. | The packet forbids history rewrite without operator approval. Every PR #43 commit failed DCO because the trailer identity did not match the commit-author identity. | **contradicted** |
| A clean non-main replacement is permitted. | Packet working instruction 9 explicitly authorizes a clean superseding branch/PR when rewrite authority is absent. | **verified** |
| The package version is 2.9.1 and the canonical inventory is eleven skills: router + nine disciplines + Helix. | `README.md`, all eleven directories under `plugins/epistemic-skills/skills/`, and the package-integration test at the packet commit. | **verified** |
| Existing deterministic checks were green on the reviewed PR tree. | PR #43 Actions run `30013228675`, job `89226443147`, clean `actions/checkout@v4` on Ubuntu/Python 3.12: all workflow steps succeeded. | **verified for the commands run** |
| The target can instantiate independent Gauntlet/UAT role contexts. | No available action exposes concurrent or sequential **context-isolated** exact-role invocation or a documented contract-equivalent separation primitive. | **unavailable; not accepted as verified** |
| Proprietary harnesses can be executed natively here. | No Claude Code, Codex plugin runtime, Cursor, Gemini CLI, Antigravity, Kimi Code, or third-party generic loader session was exposed. | **unavailable; source/deterministic tiers only** |
| The scholarly triad is wholly unavailable. | Consensus discovery executed live; Scite's canary returned a free-trial quota exhaustion/reset notice; no Zotero/durable-library action was exposed. | **contradicted as stated; partial capability only** |

`accepted_unverified`: none. Independence, native harness behavior, complete scholarly reception/holdings, and rendered acceptance remain limitations rather than inherited facts.

## Canonical skill inventory

Line/path coordinates below are relative to packet commit `532a0ce86fea908113cbca2a600fb21238e473f1`.

| Skill | Role and positive trigger | Output and boundary | References/tests/evals inspected | Baseline disposition |
|---|---|---|---|---|
| `using-epistemic-skills` | Router when more than one discipline, ordering, resumption, persistence, or external delegation may apply; it never performs member work. | Routing/skip record plus artifact coordinates; stops at routing. | `SKILL.md`; `reference/epistemic-flexibility.md`; protocol and behavioral fixtures; receipt contract. | **SOUND — deterministic/source;** native auto-trigger precision unmeasured. |
| `helix` | Tandem entry when a workflow-skill layer and this collection coexist or sequencing is ambiguous. | Stage↔discipline pairing and position record only; both routers and member triggers remain authoritative. | `SKILL.md`; complete pairing map; Superpowers v6.1.1 sources. | **CONDITIONAL;** source map coherent, live co-fire behavior unmeasured. |
| `blindspot-pass` | Before committing effort in unfamiliar, non-trivial territory; skip requires two concrete landmines and the canonical example from memory. | Four-part reconnaissance and rewritten request; no edits or verdict. | `SKILL.md`; `reference/blast-radius-quiz.md`; this suite reconnaissance. | **CONDITIONAL;** crisp boundary, no blinded trigger/skip rate battery. |
| `applying-formal-rigor` | A decision with two viable options, a correctness/comparative claim, or complexity question. | Seven-lens derivation with fired/not-applicable ledger; empirical claims remain conditional until tested. | `SKILL.md`; `reference/theory-battery.md`; worked examples; three correction derivations in report 08. | **CONDITIONAL overall; SOUND for the three audited decisions.** |
| `evidence-research` | A material scholarly claim or any Consensus/Scite/durable-library call. | Claim-evidence matrix, reception/holdings status, convergence label; never product or merge verdict. | `SKILL.md`; Consensus and Scite profiles; durable-library boundary; goal evidence basis; live capability probe. | **CONDITIONAL;** discovery live, reception quota-blocked, holdings unavailable. |
| `write-goal` | Explicit request to author or start a persistent goal. | Approved evidence-bound completion contract and optional host-adapter call; never executes or certifies the goal. | `SKILL.md`; templates; proof/anti-proxy guards; evidence-basis reference. | **CONDITIONAL; current non-invocation SOUND.** |
| `outsource` | External model/agent/process boundary or explicit durable GitHub handoff. | Committed `HANDOFF.md`, immutable pointer, relay chain; returned work is not certified. | `SKILL.md`; `reference/HANDOFF_TEMPLATE.md`; `tests/run_tests.py`; this exact packet and return path. | **SOUND for repo-backed handoff mechanics.** |
| `gauntlet` | Explicit stress-test or high-impact, irreversible, hard-to-verify decision. | Frozen dossier → deterministic selection → isolated reports → evidence verification → conflict/arbitration → computed/verified run record. | `SKILL.md`; roster; selector; evidence verifier; materializer; finalizer/run verifier; arbitrator battery; tests/example. | **CONDITIONAL;** deterministic core green, current isolated panel unavailable. |
| `evidence-locked-uat` | UI-facing acceptance with a reachable rendered target. | Actor packet, blinded verifier output, deterministic PASS/FAIL/INCONCLUSIVE judge; code reading cannot substitute. | `SKILL.md`; schemas/directive/workflow template; `scripts/judge.py --self-test`. | **CONDITIONAL; current skip SOUND** because no rendered target exists. |
| `decision-ledger` | Consequential decision/assumption/correction that a named downstream consumer will cite. | Append-only `ledger-entry@1` or stated skip; never authorization or verdict. | `SKILL.md`; JSON schema; validator; ordinary and recurrent-correction examples; this audit ledger. | **SOUND — structural/deterministic;** completeness remains best-effort. |
| `continuity-verify` | Handoff/summary/resumption whose next action depends on prior-state claims. | Re-anchored state digest; unresolved load-bearing uncertainty halts/rescopes; never performs resumed work. | `SKILL.md`; ten fixtures; deterministic scorer; skilled, baseline, and parody results. | **SOUND at smoke scale;** real-world catch rate unmeasured. |

## Manifest and discovery inventory

| Harness/surface | Packet-commit artifacts | Version/discovery claim | Current validation tier |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`; package `.claude-plugin/plugin.json` | 2.9.1; canonical `skills/` and `agents/`. | **DETERMINISTIC + SOURCE-ONLY** |
| Codex | `.agents/plugins/marketplace.json`; package `.codex-plugin/plugin.json` | 2.9.1; canonical skills; role renderer/materialized-role adapter. | **DETERMINISTIC + SOURCE-ONLY** |
| Cursor | root/package `.cursor-plugin` manifests and marketplace file | 2.9.1; one canonical tree; public listing not claimed. | **DETERMINISTIC + SOURCE-ONLY** |
| Gemini CLI | `gemini-extension.json`; `GEMINI.md`; root `skills/` link | 2.9.1; context entrypoint. Packet source had a stale eight/six statement. | **DETERMINISTIC + SOURCE-ONLY** |
| Antigravity | root `plugin.json`; root skills/agents links | Marker schema exposes name/description, not a version field. | **DETERMINISTIC + SOURCE-ONLY** |
| Kimi Code | root/package `.kimi-plugin/plugin.json` | 2.9.1; instructions map isolated roles to separate Agent calls. | **DETERMINISTIC + SOURCE-ONLY** |
| Generic Agent Skills | canonical `skills/<name>/SKILL.md`; root symlink | Eleven spec-shaped skill directories, one method tree. | **DETERMINISTIC + SOURCE-ONLY** |

## Baseline deterministic evidence

PR #43's final reviewed snapshot used a clean GitHub Actions checkout. Run `30013228675` / job `89226443147` succeeded on all named steps:

1. epistemic-flexibility protocol fixtures;
2. behavioral fixture scorer self-test;
3. outsource packet/package integration;
4. continuity committed-result scoring with expected skilled/baseline/parody polarity;
5. DCO policy unit tests;
6. Python compilation;
7. committed integration-JSON parsing;
8. decision-ledger example validation;
9. receipt verifier self-test;
10. UAT judge self-test; and
11. Gauntlet deterministic tests.

A green run proves those commands against that checkout. It does not prove native harness discovery, role independence, scholarly reception/holdings, rendered UAT, or real-world trigger/catch rates. The clean replacement branch's publication-head result is recorded in `09-final-verification.md` and PR checks.
