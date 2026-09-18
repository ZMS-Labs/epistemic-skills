# epistemic-skills 7.0.0

**Publication is conditional on the exact-candidate evidence described below.**
Preparation is held: the selected Gemini reviewer is currently unavailable,
so PR #244 remains draft and no v7 tag is authorized yet. This file records the
release scope, migration boundary, verification tiers, and owner
pre-authorization before the candidate exists. It does not itself report
a completed publication. After publication, the annotated `v7.0.0` tag and its
linked receipt supply the exact SHA, check run IDs, independent verdict, and
publication verification. No exception release is authorized for v7.0.0.

Preceded by [6.0.0](RELEASE-6.0.0.md), an exception release. This document
governs 7.0.0 only; `RELEASING.md` governs the procedure.

---

## Why this is a major version

`RELEASING.md` makes an **incompatible schema change** a major, and two
published schemas were tightened **in place, at their existing contract
versions**, since 6.0.0.

### `epistemic-product-calibration@1`

The schema gained a conditional requiring `supersedes` when `status` is
`superseded`:

```json
"allOf": [{
  "if":   { "properties": { "status": { "const": "superseded" } },
            "required": ["status"] },
  "then": { "required": ["supersedes"],
            "properties": { "supersedes": { "type": "string" } } }
}]
```

The bundled stdlib verifier already refused those envelopes with
`MISSING_SUPERSESSION`. The **published schema** did not. A producer told to
validate against the schema therefore got a false PASS while the consumer
rejected the same bytes — two definitions of valid, which is one too many.

**The honest reading of the compatibility break.** No envelope the *system* ever
accepted becomes invalid, because the verifier was already the stricter of the
two. What changes is that a producer whose CI validates against the schema
**alone** can go from green to red. That is a real break for a schema consumer,
and it is why this is not a minor version. Reading it the other way — "the
verifier already did this, so nothing changed" — would be scoping the change to
the surface that was already correct.

### `mission-manifest@1`

Eight envelope string lists (`permissions`, `protected_state`,
`acceptable_costs`, `scope.in`, `scope.out`, `hold_if`, `stop_if`,
`escalate_if`) gained a pattern refusing whitespace-only and empty strings. **A
manifest carrying an empty-string permission validated at 6.0.0 and fails at
7.0.0.** No qualification is available for this one: it is a straightforward
narrowing of an accepted input set at an unchanged contract version.

The reader deliberately does not apply the pattern to records **already
persisted**. Refusing one there would make the Stage-C gate report an armed
mission as no mission and answer `allow` (es#217).

---

## Consumer-visible changes since 6.0.0

| Surface | Change |
|---|---|
| Calibration and mission-manifest schemas | The stricter supersession and nonblank declaration requirements described above |
| Calibration verifier | An unhashable `status` returns `UNKNOWN_STATUS` instead of raising `TypeError`; regression checks cover schema/verifier supersession parity |
| Mission custody | Concurrent missions, containment and approval-lineage repairs, and independent degradation of unreadable siblings; an unreadable store is not treated as proof that no mission exists |
| Custody instruments | Validated continuity-report shape, escaped control characters in displayed text, required-text validation, shared safe-display handling, and guard checks against the unresolved path spelling ([#246](https://github.com/ZMS-Labs/epistemic-skills/pull/246)) |
| Custody performance and portability | Linear scope-close work, shared receipt lookup indexes, Windows separator classification, and absolute Cursor CLI hook rendering |
| Public documentation | Current-tree private identifiers replaced with public examples, clearer source/evidence navigation, corrected publication claims, and preservation of historical outcomes and original digest references |
| Privacy checks | Historical files and new nonignored text are scanned without whole-file exemptions; narrow synthetic examples and seeded detection controls remain explicit |
| Release operation | Required main-branch CI contexts, a bounded tag-creation procedure, explicit candidate-versus-published install refs, and a complete v7 handbook snapshot |
| Skill catalog | Fifteen skills: one entry point and fourteen disciplines. Names, triggers, and routing remain the same; example text includes privacy corrections |

The preserved historical records do not become new efficacy evidence. The
current-tree privacy cleanup leaves Git history and existing release tags
unchanged; older published coordinates may retain previously published details.
Redaction provenance is recorded in `docs/public-content-redactions.json`.

## Migration from 6.0.0

1. **Calibration producers.** Supply `supersedes` whenever `status` is
   `superseded`. Producers already passing the bundled verifier meet this rule;
   schema-only validation can newly reject an incomplete envelope.
2. **Mission authors.** Remove empty or whitespace-only values from the eight
   declaration lists. Supply readable nonblank required-text values for new
   operations. Existing declarations carried forward unchanged remain readable;
   this release does not rewrite persisted mission records.
3. **Custody users.** Recheck local hook paths and reload the updated integration.
   Test affected guards against the paths the harness actually supplies. The
   package remains on the existing contract epochs; the unfinished contract@2
   work in issue #118 is not part of this release, and no @2 migration is implied.
4. **Pinned consumers.** Update the release coordinate and its provenance record
   together after the tag exists. Before publication, `v6.0.0` remains the
   installation target even though candidate manifests say `7.0.0`.
5. **Skill users.** Keep one installation mechanism per harness, reload it, and
   verify the loaded source and fifteen-skill catalog. A matching catalog does
   not prove custody behavior or native-harness execution.

## Owner pre-authorization (2026-09-18)

The repository owner, **SternOne**, approved the stabilization recommendation
with **"approve your reccomendation"**. That recommendation explicitly included
refreshing [PR #244](https://github.com/ZMS-Labs/epistemic-skills/pull/244),
finishing its release requirements, and completing a successor release. The
owner then selected the external review family with **"Select Gemini for the
independent review"**.

This records the approved execution scope: merge the reviewed and passing
**PR #244**, prepare **v7.0.0** using
**`docs/release/RELEASE-7.0.0.md`**, and have the implementing agent execute
publication on the owner's behalf **only when all of these conditions hold**:

- All required integrity checks and the release-diff privacy review pass on the
  exact merge candidate, with the DCO determination and required CodeQL matrices
  recorded. The secret scan includes its detection positive control.
- Supported harnesses retain the explicit limits below; packaging checks are not
  promoted to live execution evidence.
- The independent Gauntlet publication gate, including the selected Gemini
  cross-family review, judges that same candidate and returns **GO** with no
  unresolved P1 or P2 findings. Selecting Gemini does not itself establish that
  the review has run or passed.

The delegation includes the bounded creation-rule change, annotated tag and
GitHub Release, unconditional re-arming and its probe, and subsequent install-ref
and wiki publication checks. It authorizes no weakening of update/deletion
protection and no exception to an unmet gate. `CONDITIONAL`, `NO-GO`, missing
evidence, or a changed candidate holds publication until a corrected candidate
has been checked and independently judged.

The final candidate SHA, workflow run IDs, reviewer identities, verdict path and
hashes, and execution timestamps are post-candidate facts. Record them in the
annotated tag and linked publication receipt; do not invent them here or add
them to the candidate tree after it is frozen.

## Gate record and evidence locations

These rows describe the preparation state. Their pending entries are not
completed check claims. When the release is published, read the tag and receipt
for the immutable execution evidence; the tagged preparation file remains
unchanged.

| Gate | Status at preparation | Exact subject | Required evidence | Limits |
|---|---|---|---|---|
| RG-4 version/link alignment | Proposed version `7.0.0`; published install ref `v6.0.0` | PR #244 preparation; recheck exact merge candidate | Manifest/integration and snapshot checks; candidate paths for planned v7 links; reachable existing v6 install links | Rotate current installation refs only after the v7 tag resolves; preserve historical citations |
| RG-5 deterministic + CodeQL | Pending at preparation | Exact merge candidate, not yet minted | Full deterministic, package, custody and watch checks; committed-JSON checks; required CodeQL matrices; PR DCO run plus exact-merge determination | Record each required job result, and disclose any inapplicable diagnostic separately |
| RG-6 security + public content | Current-tree cleanup included; candidate scan pending | Exact merge candidate and scanned history range | Full-history secret scan with positive control, privacy self-test and scan, and release-diff review | History and old tags were not rewritten; pattern scanning is not proof against every possible private fact |
| Description-byte delta | Re-measure against `v6.0.0` | Exact merge candidate versus `v6.0.0` | `check_description_budget.py --report` at both coordinates, recorded in the receipt | Package-local measurement; no estate-wide loaded-context claim |
| RG-7 harness evidence | Explicit fallback tiers assigned below | Proposed v7 package; exact-candidate checks pending | Candidate packaging checks supporting those tiers | No new live-harness execution is claimed |
| RG-8 independent publication judgment | **HELD: selected Gemini reviewer unavailable; no review or verdict** | Frozen exact merge candidate | Isolated lens reports, cross-family review, arbitration, Conflict Ledger, and exact-candidate **GO** | No self-issued GO or owner exception is authorized |
| RG-9 publication identity | Pre-authorization recorded above; execution pending | PR #244 and proposed `v7.0.0`; final identity in tag | Annotated tag, peeled candidate, matching Release body, actual re-arm and probe result, then source/wiki publication receipt | Later artifact commits and install-ref rotation do not move the tag |

### Per-harness verification tiers (RG-7)

The following are the declared evidence ceilings for this candidate. The
candidate-bound packaging checks still have to pass before publication; older
release results do not transfer to it. No new native-harness live execution is
claimed in these notes.

| Harness | Declared tier | Required evidence and remaining limitation |
|---|---|---|
| Claude Code | Packaging and deterministic checks | Manifest/surface parity and integration tests; no candidate plugin install, reload, or live skill run |
| Codex | Packaging and role-renderer checks | Manifest parity and renderer tests; no candidate role registration or loaded-session verification |
| Cursor | Packaging; existing behavioral epoch `BLOCKED_EXTERNAL` | Manifest and hook-renderer tests; no new native session proof or public marketplace listing |
| Gemini CLI | Packaging | Extension manifest and canonical-tree checks; a Gemini review is not an extension-install test |
| Antigravity | Packaging | Native manifest and shared-tree checks; no candidate plugin installation or runtime validation |
| Kimi Code | Packaging | Manifest/integration checks and published install ref; no candidate reinstall or reload proof |
| ChatGPT / OpenAI | Generated-artifact checks | Deterministic bundle tests and build; no uploaded bundle or hosted execution proof |

## Installation and handbook publication order

`EXPECTED_VERSION` in the integration tests tracks the package version;
`INSTALL_REF_PIN` tracks the latest published tag. The README, Kimi marketplace
source, and current handbook source links keep the published coordinate during
preparation. This distinction is required by `RELEASING.md` RG-4 and prevents
users receiving links to a tag that does not yet exist.

After `v7.0.0` exists, verify its intended paths and install URLs, then rotate
`INSTALL_REF_PIN`, the README recipes, the Kimi source ref, and current handbook
links in one reviewed successor change. Publish the complete 47-page v7 snapshot
to the separate wiki and run its live link check. Historical version references
remain pinned to the evidence they describe.

The preceding v6 wiki publication is already live at
`4bfd64e4c26e9bee039cf3e56d8362d73986050f`, with the snapshot and live checks
passing in [run 35387408694](https://github.com/ZMS-Labs/epistemic-skills/actions/runs/35387408694).
That proves the v6 publication only. It is not v7 candidate or publication
evidence.

## Remaining publication conditions

**Reviewer availability hold, 2026-09-18.** The selected Gemini CLI returned
`IneligibleTierError` with the service explanation that the client is no longer
supported for Gemini Code Assist for individuals. No model review ran. The
browser fallback also failed before review. These are access failures, not
judgments of the candidate; no GO, NO-GO, or exception is inferred.

Keep PR #244 draft and v7.0.0 untagged while that review path is unavailable.
Once the selected reviewer can run, advance the reviewed PR with the preparation
record intact, merge it, freeze the resulting candidate, complete every required
integrity check, and obtain the independent exact-candidate GO described above. A changed candidate invalidates
earlier candidate-bound results. The implementing agent may carry out the
recorded delegation when its conditions hold; the owner need not repeat the
same approval.

During tag creation, retain update/deletion protection, re-arm creation on every
exit path, and record the verification. If a seeded probe unexpectedly creates
a tag, preserve the incident and follow the narrowly authorized recovery in
`RELEASING.md`; do not disable all tag protection to clean it up.

After publication, commit the reviewed evidence artifacts and receipt, binding
artifact hashes to their landing commit, and finish the install-ref and wiki
checks. The tagged tree does not contain its own later verdict or publication
receipt.

## Standing obligations

`KL-SELF-GO` remains a general limit: implementing agents cannot manufacture
independent judgment by reviewing their own work. Issue #211's cross-family
review obligation is discharged only by retained qualifying evidence and an
explicit disposition; choosing a provider is not completion. The v6 exception
release and its adverse verdicts remain historical facts. A conforming v7 review,
if obtained, does not retroactively change them.
