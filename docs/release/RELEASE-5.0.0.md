# Release 5.0.0 — the loop release

**Date:** 2026-08-06. **Breaking.** Fourteen skills: one entry point,
`metacognate`, and thirteen disciplines.

> **PUBLICATION HELD.** These notes are committed; the tag is not created. Two
> release-gate items cannot be satisfied while GitHub-hosted runners are
> unavailable — see *Release gate status* below. `RELEASING.md` forbids
> improvising around the gate, so publication waits rather than the gate bending.

## What changed and why

v4.0.0 consolidated eighteen skills into eleven. v5.0.0 does something different:
it **removes the routing layer entirely** and adds the four capabilities that
close an operational loop.

| v5.0.0 skill | Owns | Refuses |
|---|---|---|
| **`metacognate`** | how much process this deserves — usually none | enumerating its members, ever |
| **`health`** | is the subject within declared bounds — *and did we look?* | rendering `UNKNOWN` as `OK` |
| **`triage`** | what is the cause, and what observation rules out the alternatives | naming a cause it did not observe |
| **`did-it-land`** | is the change in effect *on the runtime* | a green check whose oracle only read source |
| **`watch`** | a bound was crossed *while nobody was looking* | claiming installed before it has fired once |

Together: **watch** notices, **health** assesses, **triage** diagnoses,
**did-it-land** verifies the fix took.

Each carries four-valued states where the third value is the point — `UNKNOWN`,
`UNVERIFIED`, `NARROWED`, `SUSPECT`. **Absence of evidence never renders as
success.**

## Removed

`using-epistemic-skills` (the router), `helix`, and
`helix/reference/composition-contract.json` (the pair table).

`metacognate` replaces both seats. A pair table maps stages; it cannot express
the two things that turned out to matter — that **either strand may interrupt the
other**, and that **control must come back** to the point of interruption.

### The check that deleted itself

`ROUTER_DESCRIPTION_DRIFT` required the router's frontmatter to enumerate every
discipline. It was the single largest source of the enumeration tax — adding any
skill forced an edit to *another skill's firing surface* — and it is precisely the
defect that shipped in v4.0.0, where the router's description named two skills
that no longer existed.

`metacognate` enumerates nothing, so the check had nothing left to check. **The
package's integration suite now asserts the inverse:** it globs the skills
directory and fails if the entry point names any member. Enumeration went from
*enforced* to *forbidden*.

## The measured constraint behind the release

The Claude Code harness applies a **total description-byte budget** to its
assembled skill listing. A skill whose description is dropped cannot fire on
description match — it is functionally uninstalled, with no error anywhere.

Confirmed by reversible manipulation and then by intervention:

```
108 skills             -> one description dropped
111 (+3 probe skills)  -> five dropped
108 (-3 probes)        -> back to one
100 (-8 commands)      -> zero; the dropped skill returned
```

**Adding a skill is a transfer, not an addition** — it silently uninstalls roughly
its own byte-weight of other skills' descriptions. Total description budget across
all fourteen skills: **8,208 bytes**.

This is why consolidation here is a resource constraint rather than a preference.

## Migration from 4.1.0

- **`using-epistemic-skills` and `helix` no longer exist.** Invoke `metacognate`
  instead. It is the only skill invoked by name; every other member fires on its
  own `description`.
- **Trigger vocabulary maps directly:** "route this", "which skills apply",
  "pair this with my workflow" → `metacognate`. Its Tier 2 replaces the router's
  routine gate, and *declining is its most common correct outcome*.
- **Install exactly one mechanism per harness**, as before. Replace the older
  copy; do not stack them.
- **Evaluation corpora moved** from `skills/using-epistemic-skills/evals/` and
  `skills/helix/evals/` to package-level `evals/`. Any local automation
  referencing those paths must be repointed.

## Evidence posture (honest status)

- **Deterministic suite:** the complete local gate passes on the release commit —
  0 non-usage failures across every step the workflow declares, at 14 skills /
  13 disciplines.
- **Clean-room verification:** run in a fresh Linux clone of the release ref, on a
  machine that did not author the change. It found two real defects on its first
  run that every Windows run had passed — an environment-dependent guard, and a
  broken relative link.
- **Behavioral superiority: UNESTABLISHED, unchanged.** The four-arm campaign
  found **no arm separation** (primary D>A `p=0.875`; A=5 B=4 C=7 D=4 of 18).
  Nothing in this release alters that. A tidier architecture is not evidence that
  the skills improve outcomes, and this release does not claim it is.
- **Two eval batteries were retired**, their subjects having been deleted:
  the composition contract battery, and the blinded-proportionality battery which
  asserted the router's enumerated routing content. **Results and experimental
  design were kept in full**; only the harnesses were retired. Each carries a
  `RETIRED.md`.

## Release gate status — two items unmet

Per `RELEASING.md` §Release gate:

| Item | Status |
|---|---|
| 4 — version surfaces aligned, link-existence checked | **met.** All ten surfaces agree on 5.0.0. Version-pinned URLs were checked individually: `.../using-epistemic-skills/reference/routine-fast-path.md` does not exist in the v5 tree, so that link was repointed to the file's new home rather than blind-bumped — the P1 class caught in v3.2.0. |
| 5 — deterministic suite, DCO, manifest parity, committed-JSON | **partially met.** Suite, DCO equivalence, manifest parity and JSON checks pass. **CodeQL has not run.** |
| 6 — redacted full-history secret scan | **not met.** gitleaks requires a runner. |
| 8 — independent Gauntlet publication review reaching GO | **not run.** |

GitHub-hosted runners stopped being allocated at 17:10 UTC on 2026-08-06; jobs
queue unassigned and are auto-cancelled at the 15-minute timeout, which GitHub
reports as a run-level `failure`. Tracked in issue #95.

**Publication resumes when items 5, 6 and 8 can be satisfied on the exact release
commit.** The notes ship held rather than the gate shipping bent.
