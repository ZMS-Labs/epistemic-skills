# Publication record — v6.0.0

Written **after** the tag existed, which is the only time it can be written.
`docs/release/RELEASE-6.0.0.md` is immutable inside `v6.0.0` and is not edited by
this file; everything here is a post-publication fact that no pre-tag document
could have contained.

## What was published

| Coordinate | Value |
|---|---|
| Tag | `v6.0.0`, **annotated**, object `b4bc8dff0d07a7535c24905af7fb97cc85e01037` |
| Peeled target | `9a37a21faeee9f44bd63b0e43ec86b56c7f0ab1c` |
| Release | non-draft, not pre-release, targets the annotated tag |
| Release published | 2026-08-21T04:08:38Z |
| Release class | **exception release** — RG-8 overridden under D24; not conforming |

## The disarm/re-arm sitting (RG-9)

`protect-version-tags` (ruleset id **20090781**) carries `creation` on
`refs/tags/v*` with **no bypass actors**, so no actor can create a version tag
while it is armed. Disarming it is therefore the authorization act, and the tag
message records the disarm beside the authorization line. The re-arm is recorded
here, because a tag cannot contain an event that follows it.

| Event | Time (UTC) |
|---|---|
| Disarm — enforcement `active` → `disabled` | 2026-08-21T03:55:43Z |
| Annotated tag `v6.0.0` written | 2026-08-21T04:00:19Z |
| **Re-arm — enforcement `disabled` → `active`** | **2026-08-21T04:01:20Z** |

Open window: **5 minutes 37 seconds**, one sitting, no other push accepted in it.

**Re-arm proven by seeded probe, not by reading the config back.** A version-shaped
tag was pushed at the candidate after re-arming and had to be rejected:

```
remote: error: GH013: Repository rule violations found for refs/tags/v0.0.0-armprobe.
remote: - Cannot create ref due to creations being restricted.
 ! [remote rejected] v0.0.0-armprobe -> v0.0.0-armprobe
```

`GET /git/ref/tags/v0.0.0-armprobe` returns **404** — the probe never landed.
Post-state re-read: `enforcement: active`, `bypass_actors: None`, rules
`[creation, deletion, update]` all intact.

## Step-10 verification, executed

| Check | Result |
|---|---|
| Tag exists and is annotated | PASS — object type `tag` |
| Peeled tag target == candidate SHA | PASS — `9a37a21faeee` |
| Release targets that tag | PASS — `tag_name=v6.0.0` |
| Release is non-draft | PASS |
| **Committed note body == Release body** | PASS — sha256 `3468a86b845fee91…` on both sides, 35,102 chars, compared after CRLF normalization |
| `main` contains the release commit | PASS — `main` *is* the candidate |

## Post-tag commits this release owed, and why they are commits rather than gaps

The tagged tree deliberately shipped two things it could not correctly contain.
Both are discharged by the commit carrying this file.

1. **Install-ref pin.** The tagged tree pins install recipes at `v5.1.0`, because
   at tag time that was still the newest *published* tag and pinning an
   unpublished one ships dead links — publication-gate finding **PG-18**. Now
   that `v6.0.0` exists, the pin and all five live URL surfaces move to it. The
   move was gated on measurement, not on the tag's existence alone: all four
   install/reference URLs were re-probed and returned **HTTP 200** before any
   ref was rewritten. Prose references to `v5.1.0` (rollback guidance,
   "supersedes") are untouched — only URL-shaped refs moved.

2. **Wiki handbook — ERRATUM, window missed.** The release note set the revisit
   trigger as "the window between tag creation and the GitHub Release" and said
   plainly that if the window were missed this becomes a shipped documentation
   defect rather than a pending task. **The window was 04:00:19Z to 04:08:38Z
   and it was not used.** Recording that as an erratum under `RELEASING.md`
   step 11 rather than restyling it as an open intention, because the note's
   own text forbids the restyling and because "we will fix it after the tag"
   now has a 0-for-2 record in this repository.

   What is true and useful: the applier is no longer *blocked*. Its tag-existence
   guard was the reason it refused to run before, and `v6.0.0` now exists, so
   `apply_v6_updates.py <wiki-clone> --check-paths` then `--apply` will run. The
   defect is that the public handbook advertised a v5.0.0-era package at the
   moment 6.0.0 published, and no later fix un-ships that.

## Obligations that survive publication

- **D8 cross-family consult** — owed, undischarged, carried to 6.1.0 as a
  blocking obligation. Publishing 6.1.0 under a second RG-8 exception without
  first discharging D8 would convert an exception into a practice.
- **`KL-SELF-GO`** — unretired.
- **Four NO-GO verdicts** — none discharged by publication. The owner overrode
  the gate; overriding is not answering.
