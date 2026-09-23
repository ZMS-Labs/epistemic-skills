# Epistemic Skills 7.1.0

V7.1 adds a **transfer mode** to `outsource`: alongside delegating a bounded
workload for a verified return, the skill can now hand full ownership of a body
of work to a receiving agent — inventoried responsibilities, recorded custody
acceptance, and origin divestiture. The delegate path is unchanged; this is a
backward-compatible minor version. There are seventeen canonical entries:
`epistemic` plus sixteen substantive methods, as in v7.0.0.

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
  ledgers). A read-back proves comprehensibility, not competence; consequential
  work is directed to a custodied mission before transfer.
- **Extended trigger battery.** The trigger-and-scope scorer's closed action
  vocabulary gains `transfer-packet` and `verify-acceptance` with full field
  contracts; four new fixtures (eighteen total) distinguish a full-custody
  handover from a retained-ownership delegation and exercise the acceptance
  and gap branches; the completion battery adds a synthetic acceptance
  closure with mutation checks.
- **Pinned projections.** The package-integration suite pins the new contract
  phrases, both templates, and the mode declarations. README, handbook
  (Skill-Outsource, catalog, how-the-pieces-fit), and the host manifests
  describe both modes.
- **Description budget.** The `outsource` description grows by 78 bytes
  (7,153 → 7,231) to name both modes; `CEILING_BYTES` tightens from 8,636 to
  the measured 7,231 so the v7.0.0 slack cannot silently refill.

## Migration and compatibility

No consumer-visible contract change to existing delegate behavior: the same
repository layout, prompt shape, publication discipline, and
`outsource-relay@1` envelope. Existing `docs/outsource/<work-id>/` packets
written before 7.1 carry no `Mode` row; they are delegate packets by
construction and remain valid. New transfer packets opt in per work ID.
Agents that only ever delegate need no change. The skill count is unchanged
(seventeen skills, sixteen disciplines); install one versioned copy per host
per the [installation guide](../INSTALLATION.md), replace the older tag,
reload, and verify the loaded source.

## Evidence and limits

The content change merged as PR #259 (`fc167ac`); the release candidate is
the merge commit of the version-rotation release PR. Exact-commit hosted
outcomes, the candidate SHA, and the check-run inventory are bound by the
annotated tag object and the attached publication receipt. These notes alone
do not assert that an unperformed publication step passed.

| Gate | Status record | Exact subject / evidence | Limit |
|---|---|---|---|
| Version, links and package | Final result in publication receipt | Annotated v7.1.0 target; source/bundle and post-tag URL checks | A manifest is not an installation receipt |
| Deterministic checks and CodeQL | Final hosted outcomes in tag and receipt | Required runs on the exact merge commit | Historical/local checks are retained separately |
| Security, public content and provenance | Final outcomes in tag and receipt | Exact candidate and reachable history; scan controls; matching sign-offs | Known patterns, not universal absence proof |
| Description bytes | 7,231; delta +78 from v7.0.0's 7,153; ceiling 8,636 → 7,231 | Canonical package descriptions; `check_description_budget.py --report` | Package-local, not total host context headroom |
| Host evidence | v7.0.0 tiers carry forward; no new host claims made in 7.1.0 | [v7 host coverage](v7-host-coverage.md) | Discovery/serialization does not prove automatic use |
| Designated review | Exact-candidate verdict in tag and receipt | Owner-designated implementing ZCode agent (GLM-5.3) | Shared implementation context; not blinded or independent |
| Publication identity | Final assertions in receipt | Annotated tag, release body and generated assets | Verify the actual tag and receipt, not this prose alone |

Pre-merge local evidence on the content branch (not exact-commit evidence):
outsource trigger-and-scope suite PASS (18 fixtures), synthetic terminal
return PASS including the acceptance mutations, outsource package
integration PASS, skill surfaces in sync, wiki gate PASS, public-content gate
PASS, description budget at ceiling, JSON artifacts checked. A mimosa static
scan completed with eight findings, none in files touched by this release;
the pre-existing findings (gauntlet scripts, cursor hook renderer, a
historical v6 wiki checker) are recorded on PR #259 and remain open for the
owner.

## Known limits carried forward

The [macOS custody limitation (issue #162)](https://github.com/ZMS-Labs/epistemic-skills/issues/162)
remains: do not rely on distinct-filename or exclusion guarantees on
case-insensitive POSIX filesystems. The v7 comparative-superiority boundary
also carries forward: no arm separation was ever demonstrated, and 7.1.0 adds
no behavioral-performance claim. The transfer mode's acceptance read-back
verifies coverage of the responsibility inventory, not the receiver's future
stewardship; that limit is stated in the skill itself.
