# Release 5.0.0 — the loop release

**Date:** 2026-08-06. **Breaking.** Fourteen skills: one entry point,
`metacognate`, and thirteen disciplines.

> **PUBLISHED.** Release-gate items 4, 5 and 6 are met on the exact tagged commit —
> the deterministic suite, CodeQL, and the full-history secret scan all passed there,
> verified at job and step level.
>
> **Item 8 — an independent Gauntlet publication review reaching GO — was WAIVED by
> the repository owner and was never run.** There is no GO verdict for 5.0.0. This is
> stated here rather than in a footnote because the alternative is a release record
> that reads as though the gate passed.

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
all fourteen skills: **8,200 bytes**, measured as the harness resolves them, so a
quoted description is charged for its content and not its delimiters.

This is why consolidation here is a resource constraint rather than a preference.

### Known limitation — this release shipped over its own budget

v5.0.0 is net **+1,389 description bytes**. Each individual description was held
inside sibling range; **the sum was never checked against the live budget.** The
result was that `triage` and `watch` — two of the four skills this release adds —
could not fire at all until unrelated slash-commands were deleted elsewhere on the
installing machine. No error was raised anywhere, because there is no error to
raise: a dropped description simply stops matching.

That is per-item discipline with no aggregate check, which is precisely the defect
class this package exists to catch, committed by the package itself.

The gap is now closed at the artifact boundary:
`.github/scripts/check_description_budget.py` fails CI if the packaged total
exceeds a recorded ceiling, so any increase must be paid for in the same diff.
It does not and cannot observe the harness cap — that is a property of the whole
installed estate — but it does make this package's own contribution a number that
was chosen rather than one that drifted.

**If you install this alongside a large existing skill collection, budget for it.**
The measured figures below are the only ones we have; the exact ceiling was bounded,
never bisected.

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

## Release gate status

Per `RELEASING.md` §Release gate. Items 5 and 6 were satisfied on 2026-08-06 against
the exact commit `3a18cd3`, verified at job and step level rather than by run label:

| Item | Status |
|---|---|
| 4 — version surfaces aligned, link-existence checked | **met.** All ten surfaces agree on 5.0.0. Version-pinned URLs were checked individually: `.../using-epistemic-skills/reference/routine-fast-path.md` does not exist in the v5 tree, so that link was repointed to the file's new home rather than blind-bumped — the P1 class caught in v3.2.0. |
| 5 — deterministic suite, DCO, manifest parity, committed-JSON, CodeQL | **met** on `3a18cd3`. `epistemic-flexibility` job `stdlib-checks` succeeded across 45 steps — 44 success and one correctly skipped (`Durable ledger append-only against merge base`, which needs a PR merge base and has none on a dispatch run). CodeQL `Analyze (actions)`, `(javascript-typescript)` and `(python)` all succeeded on the same commit. |
| 6 — redacted full-history secret scan | **met** on `3a18cd3`. `release-security` job `full-history-secret-scan` succeeded, including its own positive control step *"Prove the scanner detects a planted secret"* — so the clean result is a measurement, not a scanner that finds nothing. |
| 8 — independent Gauntlet publication review reaching GO | **WAIVED, not met.** Explicitly waived by the repository owner on 2026-08-06 ("i approve the release and we don't need the full gauntlet"). No Gauntlet publication review was run for 5.0.0, and no GO verdict exists. Recorded as waived rather than satisfied, because a release record that reads as if a gate passed when it was skipped is worse than no record. |

### How items 5 and 6 became reachable

Neither gate could be run on demand. Both were reachable only as a side effect of
pushing a commit or opening a pull request — which cannot satisfy a gate that asks for
a result **on the exact release commit**. `workflow_dispatch` was added to both (#99),
and the first dispatched run immediately failed on a real defect this session had
introduced into `README.md` (#101). The gate earned its keep within twenty seconds of
becoming reachable.

That defect is also why `README.md` is now in the workflow's path filters: one of the
gate's checks asserts a required count phrasing *in README.md*, so a README-only edit
could break the gate without triggering the workflow that enforces it. A check's inputs
belong in its trigger.

Runner assignment was intermittently failing throughout — jobs auto-cancelled at the
15-minute assignment timeout with no runner ever assigned, which GitHub reports as a
run-level `failure`. **Re-dispatching succeeds**; that, not waiting, is the lever. Quota
was never the cause (29,752 of 50,000 included minutes, $0 billable) and neither was
queue depth (3 runs in flight org-wide). Diagnosis in issue #95.

### On the waiver of item 8

`RELEASING.md` §Procedure step 5 requires the Gauntlet publication gate to be run and
recorded. For 5.0.0 it was **not run**. The repository owner waived it explicitly on
2026-08-06 and authorized publication.

That is the owner's call to make — the gate is theirs. What is not discretionary is the
record. So, stated plainly for anyone auditing this release later:

- **No adversarial publication review was performed on 5.0.0.** No lens panel, no
  arbitrator, no Conflict Ledger, no GO verdict. There is no artifact to point at
  because none exists.
- The evidence backing this release is therefore: the deterministic suite, CodeQL, the
  full-history secret scan, and a clean-room run — **all of which check the artifact,
  and none of which check the judgment.** They establish that the package builds, scans
  clean, and passes its own tests on the tagged commit. They do not establish that the
  design decisions in it are sound.
- **Behavioural superiority remains UNESTABLISHED** (`p=0.875`, no arm separation), and
  nothing about publishing changes that.

A future release wanting a GO on record must run the gate then. Item 8 cannot be
retroactively satisfied for 5.0.0, and this section exists so nobody later mistakes an
unrun gate for a passed one.
