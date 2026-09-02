# epistemic-skills 7.0.0

**Status at the time this file was committed: NOT PUBLISHABLE.** The independent
publication-judgment gate (RG-8) has neither returned GO nor been waived on the
record, and the two acts that would resolve it cannot be performed by the
implementing agent. See [Before this may be tagged](#before-this-may-be-tagged).
Nothing below should be read as a publication decision.

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

Twenty-eight commits. Grouped by what a consumer can observe:

| Surface | Change |
|---|---|
| `epistemic-product-calibration@1` schema | Conditional supersession requirement (above) |
| `mission-manifest@1` schema | No-whitespace pattern on eight envelope lists (above) |
| `verify_calibration.py` | An unhashable `status` (`{}`, `[]`) now returns the named `UNKNOWN_STATUS` failure instead of raising `TypeError`. The self-test gained that case and a schema/verifier parity assertion, so its output string changed from `PASS (5/5)` to `PASS (6/6 cases + schema/verifier supersession parity)` |
| `continuity-report.schema.json` | New |
| Mission custody (es#173) | Concurrent missions are legal; the one-active-mission door is gone. Unreadable sibling directories require `--acknowledge-unreadable`. Containment, approval lineage and per-mission union degradation reworked |
| Custody instruments | Control characters escaped on display surfaces; absolute hook rendering for Cursor CLI; instruments refuse, escape, and admit what they could not read |
| Skills (`SKILL.md`) | **None.** Triggers, routing, entry point and the skill count are identical to 6.0.0 |

The last row is the one most likely to be misread. Fifteen skills at 6.0.0,
fifteen at 7.0.0, same names, same descriptions. This release is a contract
release, not a catalog release.

### Downstream effect already measured

`ZMS-Labs/epistemic-calibration` pins a skills release coordinate and compares
its product schema against skills `main`. That comparison currently fails —
correctly — because the release it pins predates the `allOf` addition:

```
xr-v5: e3e2fd459ce619a9b7c6cbf0cce23f668e294f54cfb9ba7fa2886e43d3a1f66a
main:  84f229c17732874db30bb4a0fd8a5580941a07d06ac182f1efacd468450189d4
EXIT=1
```

Pointed at this candidate the same run returns `EXIT=0` with the verifier
self-test passing at 6 of 6 cases plus the parity assertion. That is the
consumer-side confirmation that this release is the coordinate they need.

---

## Migration from 6.0.0

1. **Producers of `epistemic-product-calibration@1` envelopes.** If you emit
   `status: "superseded"`, emit `supersedes` with it. If you were already
   passing the bundled verifier you are already compliant; only schema-only
   validation changes verdict.
2. **Authors of `mission-manifest@1` manifests.** Remove empty and
   whitespace-only entries from the eight envelope lists. Existing persisted
   records are unaffected by design.
3. **Consumers pinning a skills release SHA.** Rotate to this tag and update
   whatever record declares the coordinate, in the same change.
4. **Everyone else.** Re-point install recipes at `v7.0.0`. No skill surface
   changed, so no trigger or routing behaviour changes.

---

## Gate record

Recorded against the release candidate. **The candidate SHA is not written in
this file**, because writing it would change the tree and produce a different
commit — the fixed point `RELEASING.md` step 7 describes. It is carried by the
annotated tag object.

| Gate | Status | Exact subject | Evidence | Limits |
|---|---|---|---|---|
| RG-4 version/link alignment | `MET` | release branch tip | Ten version-bearing manifests at `7.0.0`; every README install recipe and pinned URL at `v7.0.0`; all four referenced paths verified present in the candidate tree; `check_wiki.py` reports `47 pages, 27 banners, 16 counts, 224 versioned links` and `wiki gate: PASS` | Path existence verified in the candidate tree, not against the published tag, which does not yet exist |
| RG-5 deterministic + CodeQL | `UNMET — not yet run on a candidate` | — | The candidate is minted by merging this pull request; per step 4 the checks must be re-run on that exact commit | A pull-request run is not a candidate run |
| RG-6 security + public content | `PARTIAL` | release branch tip | `check_public_content.py --self-test` → `8 seeded RED controls passed`; `check_public_content.py` → `8 patterns, 38 allowlisted exact files digest-verified (0 dormant entries)` | The full-history secret scan with its planted-secret positive control has not been run on a candidate |
| description-byte delta | `0 bytes` | release branch tip vs `v6.0.0` | `check_description_budget.py --report` at both: `8636 TOTAL across 15 skills (ceiling 8636)` | Package-local only; the estate gate is retired |
| RG-7 harness evidence | `UNMET` | — | No harness exercised live against a candidate | Install recipes changed only in the version they pin; the package surface is unchanged from 6.0.0, which is a reason to expect parity, not evidence of it |
| RG-8 independent publication judgment | **`UNMET`** | — | **No gauntlet run, no GO, and no owner exception record exists** | This is the blocking row |
| RG-9 publication identity | `UNMET` | — | No pre-authorization committed; no tag; no Release | Requires the owner |

**No row above is `MET` on the strength of remembered work.** Where a check ran,
its output is quoted; where it did not, the row says so rather than borrowing
credibility from a neighbouring green.

---

## Before this may be tagged

Two acts remain, and **neither can be performed by the implementing agent**.
This section exists so that is unambiguous rather than discovered later.

### 1. Resolve RG-8

Either commission an independent Gauntlet publication review on the frozen
candidate and record a `GO`, **or** publish under the standing exception route,
which requires all five disclosures from `RELEASING.md` committed to **this
file** before the tag is created:

1. that the gate was not run or did not reach GO;
2. that no GO exists;
3. the owner's identity, date, scope, and exact authorization;
4. the evidence that remains available and what it cannot establish; and
5. any successor-release condition or revisit trigger.

Disclosure 3 is why an agent cannot write this section. An authorization the
owner did not give is not made real by an agent typing it, and a placeholder
here would be the precise artifact the exception route exists to prevent.

`CONDITIONAL` is not `GO`. `WAIVED` is never a synonym for `MET`.

### 2. Create the tag

`refs/tags/v*` is covered by the `protect-version-tags` ruleset, which carries
`creation`, `update` and `deletion` with `bypass_actors: []` and
`current_user_can_bypass: "never"`. Verified against the API on 2026-09-02.

That is deliberate, and `RELEASING.md` says why: this repository is pushed with
the same credential automation runs under, so an admin bypass would exempt
exactly the actors the rule exists to constrain. **Disarming the ruleset is
therefore the owner's authorization act**, not a mechanical step preceding it —
and an agent holding that credential disarming it would be the control failing
at the only moment it matters.

Disarm, tag, and re-arm in the same sitting, then verify the re-arm with a
seeded probe rather than by reading the configuration back. A release that ends
with the gate left open has removed the control it was meant to satisfy.

---

## Standing obligations carried forward

`KL-SELF-GO` remains unretired: a repository maintained by one operator and one
implementing agent lineage cannot manufacture the independence a conforming
release requires. 6.0.0 demonstrated that at length — nine reviews, four
publication NO-GOs, and an override at the end. Naming the limit is not
discharging it.

## Preparation provenance

The version bump, the handbook campaign, this file and the gate table above were
prepared by an agent steward session, from the actual diff between `v6.0.0` and
the release branch. Every quoted output in the table was produced by running the
named command; none is recalled. The gate rows that say `UNMET` say so because
the check has not run, not because its result was unfavourable.
