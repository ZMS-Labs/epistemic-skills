# Epistemic Skills 7.1.0

> **STATUS: DRAFT — PRE-CANDIDATE.** This note is prepared with the content
> change and is not a release record. Every gate row below is `PENDING` until
> the release PR freezes an exact candidate and binds evidence to it, per
> [RELEASING.md](../../RELEASING.md). No tag, Release, or authorization exists
> at this stage. The release PR must finalize this file, not publish it as-is.

V7.1 adds a **transfer mode** to `outsource`: alongside delegating a bounded
workload for a verified return, the skill can now hand full ownership of a body
of work to a receiving agent — inventoried responsibilities, recorded custody
acceptance, and origin divestiture. The delegate path is unchanged; this is a
backward-compatible minor version.

## What changed

- **Two named modes.** Every outbound request is `delegate` or `transfer`,
  chosen by operator intent, recorded in the packet header, and shown in the
  readiness receipt's packet line. Ambiguous intent asks before publishing.
- **Transfer packets** (`outsource-transfer@1`, new
  `reference/TRANSFER_TEMPLATE.md`) replace the bounded outcome with a
  responsibility inventory — in-flight work, standing obligations and
  watchers, authority with provenance, open loops, escalation paths — swept
  from the durable sources that hold obligations, not just the current task's
  context. An obligation that cannot be inventoried is surfaced as a named
  gap, never silently transferred.
- **Custody acceptance contract.** The terminal event is the receiver's
  explicit read-back of what it now owns (`outsource-acceptance@1` envelope),
  verified by the origin for coverage. `ACCEPTED` transfers the work;
  `TRANSFERRED` requires the origin's divestiture checklist to reach residual
  `NONE` (watchers stopped or handed over, credentials handed over or
  revoked, loops left, steward change recorded in affected missions and
  ledgers). A read-back proves comprehensibility, not competence — the note
  saying so is in the skill, and consequential work is directed to a custodied
  mission before transfer.
- **Extended trigger battery.** The trigger-and-scope scorer's closed action
  vocabulary gains `transfer-packet` and `verify-acceptance` with full field
  contracts; four new fixtures distinguish a full-custody handover from a
  retained-ownership delegation and exercise the acceptance and gap branches;
  the completion battery adds a synthetic acceptance closure with mutation
  checks (acceptance without divestiture, residual obligations, and
  post-acceptance outbound prompts all fail).
- **Pinned projections.** The package-integration suite pins the new contract
  phrases, both templates, and the mode declarations. README, handbook
  (Skill-Outsource, catalog, how-the-pieces-fit), and the root plugin
  manifest describe both modes.
- **Description budget.** The `outsource` description grows by 78 bytes
  (7,153 → 7,231) to name both modes so full-handover requests can fire;
  `CEILING_BYTES` tightens from 8,636 to the measured 7,231 so the v7.0.0
  slack cannot silently refill.

## Migration and compatibility

No consumer-visible contract changes to existing delegate behavior: the same
repository layout, prompt shape, publication discipline, and
`outsource-relay@1` envelope. Existing `docs/outsource/<work-id>/` packets
written before 7.1 carry no `Mode` row; they are delegate packets by
construction and remain valid. New transfer packets opt in per work ID.
Agents that only ever delegate need no change.

## Evidence and limits

| Gate | Status | Exact subject | Evidence | Limits |
|---|---|---|---|---|
| version/link alignment | `PENDING` | release candidate commit | release PR rotation checklist below | none of these rows are `MET` pre-candidate |
| deterministic + CodeQL | `PENDING` | release candidate commit | required workflow run IDs recorded in the annotated tag object | dispatch every gating workflow explicitly on the merge commit |
| security + public content | `PENDING` | candidate and history range | `check_public_content.py --self-test` + full run, secret scan with positive control | local runs on this branch passed pre-candidate; they are not exact-commit evidence |
| description-byte delta | +78 vs v7.0.0 (7,153 → 7,231); ceiling tightened 8,636 → 7,231 | this branch | `check_description_budget.py --report` at both releases | package-local only |
| harness evidence | `PENDING` | tag/commit | live run or tier record per supported host | none recorded pre-candidate |
| designated-reviewer publication judgment | `PENDING` | frozen candidate | designated-reviewer record | reviewer identity and separation stated at release |
| publication identity | `PENDING` | tag + release | API identity receipt | none exists pre-candidate |

Pre-candidate local evidence on this branch (not exact-commit evidence):
outsource trigger-and-scope suite PASS (18 fixtures), synthetic terminal
return PASS including the new acceptance mutations, outsource package
integration PASS, skill surfaces in sync, wiki gate PASS, public-content gate
PASS (1,779 files), description budget at ceiling, JSON artifacts 307 checked.

## Release-PR rotation checklist

The content change rides a normal PR to `main`. The release PR (from final
intended `main`, per RELEASING.md procedure) then:

1. Rotate `EXPECTED_VERSION` and `INSTALL_REF_PIN` in
   `plugins/epistemic-skills/skills/outsource/tests/run_tests.py` to
   `7.1.0` / `v7.1.0`.
2. Rotate every version-bearing manifest (`gemini-extension.json`,
   `.claude-plugin/marketplace.json`, `.cursor-plugin/*`,
   `.kimi-plugin/*`, `plugins/epistemic-skills/.codex-plugin/plugin.json`,
   and siblings) and every install ref to `v7.1.0`.
3. Rewrite `docs/INSTALLATION.md` for v7.1.0 (tag URLs, clone paths, cache
   path pin, count statements — still seventeen skills / sixteen
   disciplines).
4. Rotate the 29 handbook `Applies to` pins and canonical tag links from
   `v7.0.0` to `v7.1.0` (the Skill-Outsource page already describes the
   transfer mode; its pin is the last stale surface after merge).
5. Update the README version statement and published-release link.
6. Commit `docs/release/PREAUTH-7.1.0.md` naming this release PR, the
   version, the gate that must return GO, and the firing condition — before
   the candidate is minted.
7. Finalize this file: replace every `PENDING` row with exact-commit
   evidence, drop the DRAFT banner, and freeze.
8. Then follow RELEASING.md steps 4–11 (merge commit as candidate, explicit
   workflow dispatches, run IDs in the annotated tag object, designated
   review, ruleset disarm → tag → re-arm with seeded probe, GitHub Release
   from this file, identity verification).
