# Release 5.0.1 — the correction release

**Date:** 2026-08-06. **Patch.** Fourteen skills, unchanged from 5.0.0. No skill
content, trigger, or boundary is modified by this release.

> **What this fixes:** 5.0.0 shipped install metadata advertising two skills that
> release deleted, and a release record that claimed a gate item it had only half
> satisfied. Both are corrected here. The 5.0.0 tag is immutable and still carries
> the overclaim; this release is the correction of record.

## Why 5.0.1 exists

`RELEASING.md` is explicit: *"Never move or reuse a published version tag.
Corrections ship under a new semantic version."* Two defects in 5.0.0 required it.

### 1. The package advertised skills it had deleted

| Surface | Shipped in 5.0.0 saying |
|---|---|
| `.claude-plugin/marketplace.json` | `using-epistemic-skills + helix + recon + …` |
| `.cursor-plugin/marketplace.json` | the same member list |
| six plugin / extension manifests | "with the helix tandem layer for workflow-skill pairing" |
| `GEMINI.md` | **"Start with the `using-epistemic-skills` skill"**, "Read the `helix` skill" |

The marketplace listings are the worst of these: they advertised the install as
containing two deleted seats **and omitted all five skills 5.0.0 added**. `GEMINI.md`
is close behind — a fresh Gemini CLI session following its own instructions went
looking for two skills that are not in the package. It also carried the same
double-count the README did: *"fourteen skills: entry point + thirteen disciplines +
the helix tandem entry point"* is fifteen.

All corrected. The member list is now generated from the same fourteen skills the
package actually ships.

### 2. The guard against exactly this had drifted

`check_no_phantom_skills.py` exists to catch *"manifest advertises retired skill to
installers"*. It passed on the broken tree. Three compounding reasons:

- **Its `RETIRED` map is its own hand-maintained inventory, and it drifted.** The map
  listed the nine v4.0.0 retirements. 5.0.0 deleted `using-epistemic-skills` and
  `helix`, and nobody added them — so the guard had never heard of the two names it
  most needed to catch. *That is the disease this package documents, occurring inside
  the guard against it.*
- **`**/*plugin*.json` matches on filename**, so it never matched `marketplace.json`
  despite it living in `.claude-plugin/`. Both marketplace files went unscanned
  through every release the project has ever cut.
- **The `.md` scan matched `skills/<name>/` paths, not prose.** `GEMINI.md` was being
  read, and its instructions were invisible to it.

Now: the map carries the 5.0.0 deletions and states the obligation plainly — adding a
skill costs nothing here, deleting one requires an entry in the same commit. Manifest
scanning moved to an explicit glob tuple including `marketplace.json`. Root
instruction files are scanned as prose, with historical framing allowed.

**Verified by negative control.** The hardened guard was run against the tree that
shipped *before* anything was repaired: 16 surfaces flagged. Two proved false
positives — `README.md`'s "Craft doctrine (not disciplines) … v4.0.0 demotion" note
and a version-history line — both accurate. The historical vocabulary was widened
until those cleared while all four `GEMINI.md` defects were retained: **14 real, 0
false**. A guard that punishes accurate history teaches people to delete history.

### 3. The 5.0.0 release record overclaimed gate item 6

`RELEASING.md` item 6 reads, in full:

> A redacted full-history secret scan passes, **and public-content/provenance review
> covers the release diff.**

Only the first clause was ever checked. The gate row was written from the name of the
CI job that passed rather than from the text of the requirement, so a two-part item was
recorded as **met** on one part. **The provenance review was never performed.**

This is the oracle-adequacy failure — confirming that a check ran green rather than
that the check covers the claim — committed in the same document that defines it, on
the same day, by the agent writing that definition. An independent reviewer reading
`RELEASING.md` against the gate table caught it. Re-reading the work did not.

`RELEASE-5.0.0.md` now records item 6 as **partially met**, item 7 as **never assessed**
rather than silently omitted, and item 8 as the two-part requirement it actually is.

**The 5.0.0 tag cannot be corrected.** It is annotated, pushed, and immutable, and
`RELEASING.md` forbids moving or reusing a published version tag. Its annotation will
permanently assert that item 6 was met. This release is the correction of record.

## Release gate status for 5.0.1

| Item | Status |
|---|---|
| 4 — version surfaces aligned | met |
| 5 — deterministic suite, DCO, parity, JSON, CodeQL | met on the tagged commit |
| 6 — secret scan **and public-content/provenance review** | **partially met.** Scan passed, including its positive control. The provenance-review half was **not** performed for 5.0.1 either. Stated rather than implied. |
| 7 — harness surfaces exercised or assigned an honest tier | **not tracked as a gate row.** Unchanged from 5.0.0. |
| 8 — Helix routing recorded **and** independent Gauntlet review reaching GO | **waived, not run.** Waived by the repository owner for 5.0.0 and not revisited for this patch. Its first clause remains unsatisfiable as written — it requires recording "Helix routing" for a skill 5.0.0 deleted. |

## Known limitations, unchanged from 5.0.0

- **Behavioural superiority remains UNESTABLISHED.** Four-arm campaign, no arm
  separation, primary D>A `p=0.875`, A=5 B=4 C=7 D=4 of 18. Nothing in this patch
  touches that, and no release of this package has yet changed it.
- **The description-byte budget is a shared, rivalrous constraint.** Total across all
  fourteen skills: **8,200 bytes**, measured as the harness resolves them. If you
  install this alongside a large existing skill collection, budget for it.
- The exact harness description-byte ceiling was **bounded, never bisected**.

## Follow-up not in this release

`RELEASING.md` item 8 still requires that "Helix routing is recorded". Helix was
deleted in 5.0.0, so the clause is unsatisfiable as written. Replacing it needs a
judgment about what, if anything, takes its place — it is flagged rather than rewritten.
