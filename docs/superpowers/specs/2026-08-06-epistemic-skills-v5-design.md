# epistemic-skills v5.0.0 — design

**Date:** 2026-08-06
**Status:** design approved in brainstorming; not yet planned or implemented
**Supersedes the assumption of:** a third "fleet/estate" skill package

## Why this exists

The operator's goal, in his words: *"improve my skill usage by improving my skill
library and toolkit to its full potential"* and *"lets get them to be coherent and
consistent and refined."*

A prior program assumed the answer was a **third package** holding world-facing
capabilities, and spent multiple sessions trying to name it. This design rejects
that assumption. The third package was never derived — it was inherited. Once its
intended members were written down, they turned out to satisfy `epistemic-skills`'
own stated thesis verbatim, and the separation had no non-circular justification.

Consolidation, not proliferation, was the actual request.

## Decisions of record

| # | Decision | Why |
|---|---|---|
| D1 | **No third package.** The four wanted capabilities merge into `epistemic-skills` as v5.0.0. | Its thesis already covers them; a second package costs two routers, two CI suites, ~24 manifests, and a permanent boundary dispute. ADR-185 already established that capability identity induces no partition; three independent admission tests had already failed on the same two rows. |
| D2 | **`fleet-health` → `health`.** | "Fleet" was the operator's context, not the capability. The subject is any running system with declared bounds. |
| D3 | **Delete `using-epistemic-skills` and `helix`.** | The router is a hand-maintained projection of its own members and shipped a firing defect (PR #91). `helix` is a pair table that cannot hand control back. |
| D4 | **Add `metacognate`** as the single entry point, enumerating nothing. | The operator wants one way to say "apply the discipline here." A seat that carries a *procedure* rather than an *inventory* has no drift surface. |
| D5 | **Pairing is two-tier:** iron laws + question-driven. | Iron where being wrong is irreversible; judgment everywhere else. No table of stage→skill pairs. |
| D6 | **Portable core + `LOCAL.md` is kept as self-imposed discipline**, not for distribution. | The portability constraint is what produced a 9/9 skill. A hostname in `SKILL.md` is a defect regardless of audience. |
| D7 | **Evidence emission is intrinsic**, never a call to an external service. | ECS has 290 claims, 86% unverified, and **zero** skills have ever called `register_claim`. The loop fails open by construction. Intrinsic records cannot be skipped. |

### On the name `metacognate`

The operator previously proposed renaming the package to `metacognition-skills`.
That was refused as a *package* name on migration cost — 465 load-bearing
references across 87 files, 12 manifests, a skill whose own name contains the
package name — and refused as a *sibling* package because it induced no usable
boundary against `epistemic-skills`.

It was **not** refused on fit. The literature the operator gathered calls this
artifact class a *metacognitive harness* (Wang 2026; "LLMs Know When They Know",
2026), and MIRROR calls the winning intervention *external metacognitive control*.
Nelson & Narens never require the meta-level to sit inside the object-level.

An invoked verb is a different slot from a package name: zero references, zero
manifests, zero rename. The fit is right and the cost is nothing.

## Architecture

### Thesis

The package's thesis widens by one clause it already implied:

> What would make the target, decision, evidence, handoff, or acceptance claim
> trustworthy enough to bear load — **including when the claim is about a running
> system that does not report itself honestly.**

### Membership: 11 → 14

| Group | Skills |
|---|---|
| entry | `metacognate` |
| before effort | `recon` · `write-goal` · `open-questions` |
| settling | `resolve` · `gauntlet` |
| claims | `evidence-locked-uat` · **`did-it-land`** |
| running systems | **`health`** · **`triage`** · **`watch`** |
| carrying forward | `decision-ledger` · `context-audit` |
| crossing out | `outsource` |

Removed: `using-epistemic-skills`, `helix`.
Added: `metacognate`, `health`, `triage`, `watch`, `did-it-land`.

### Subject test (the boundary that holds)

| package | subject |
|---|---|
| a workflow layer (e.g. superpowers) | the work being produced |
| **epistemic-skills** | **claims that must bear load — about the work, the reasoning, or a running system** |

This is deliberately *one* boundary, not two. Prior attempts to split "reasoning"
from "running systems" reproduced the partition failure documented in ADR-185.

## Components

### `metacognate`

Carries a procedure. **Never carries a member list.**

```
TIER 1 — IRON. No judgment, no waiver. Holds regardless of which strand
                has control, including a workflow layer's own gates.
  · no irreversible act without prior scoped consent
  · no completion claim without an oracle adequate to the claim
  · no acceptance certified by the actor that performed the work
  · a hard gate from either layer is not overridable by the other

TIER 2 — WISE. Judgment, bidirectional, bounded.
  1. does this clear the routine fast path?  -> YES: do the work, say
     nothing, STOP. Silence is a success state.
  2. what would have to be true for this to be right?
  3. which of those can I not currently answer?
       <- the unanswerable one names the discipline
  4. that discipline runs BOUNDED, then hands control BACK to the point
     of interruption
  5. all answerable -> engage nothing
```

**Trigger width: wide, with the decline test stated in the `description` itself.**

Skills fire on their `description`, which is always resident in context; the body
loads only once fired. Therefore a wide trigger is affordable **if and only if**
routine work can be declined from the description alone — a false fire then costs
zero context. If the decline requires reading the body, the trigger must narrow.

Fires when any is observably true:

- the act is irreversible, one-way, or high blast radius;
- a claim is about to bear load ("it's fine", "it's done", "it works", "it's deployed");
- the *approach* is uncertain, not merely the answer;
- an observation contradicts what a tool or document just asserted;
- resuming from a summary, handoff, or remembered state.

Does not fire — decidable from the description alone:

- routine, reversible, local, directly-checkable work;
- lookups and mechanical edits;
- a call the operator has already made;
- inside a discipline this would route to (no recursion).

### The four new members

| skill | owned decision | refusal |
|---|---|---|
| `health` | is the subject within its declared bounds — **and did we look?** | rendering `UNKNOWN` as `OK`; judging against a bound nobody declared |
| `triage` | this specific thing is broken — what is the **cause** | re-probing blind; performing the fix (a separate consented act) |
| `watch` | a bound was crossed **while nobody was looking** | claiming installed before it has fired once on a deliberately crossed bound |
| `did-it-land` | the change is real **on the runtime**, not in the repo | a green check whose oracle only read source |

States are four-valued, not binary, and the third value is the point:

- `health` → `OK` / `WARN` / `CRITICAL` / **`UNKNOWN`**
- `did-it-land` → `LANDED` / `REVERTED` / **`UNVERIFIED`**

Absence of evidence never renders as success. A roll-up containing any `UNKNOWN`
is at best `UNKNOWN` for that branch.

`health` takes `scope` and `depth` as **arguments, not siblings** — this is what
allowed one skill to absorb six commands. Subjects resolve from a registry
declared in `LOCAL.md`, never hardcoded.

`watch` is the only member that acts unattended and therefore carries extra load:
ships **inert** (SAFETY-1), has a **verified kill switch** (SAFETY-8), and is not
called installed until it has actually fired.

## Data flow

```
watch ──bound crossed──▶ health ──ordered subjects──▶ triage ──cause──▶ [consented fix]
                           ▲                                                    │
                           └──────────── did-it-land ◀───────────── verify ─────┘
                                              │
                                    decision-ledger (if consequential)
```

### Routing is generated, never authored

Each skill declares its consumer inside the `metadata` frontmatter key — one of
the six portable keys, so this stays packaging-legal:

```yaml
metadata:
  hands-to: [triage, decision-ledger]
```

`ROUTING.md` is **generated** from those declarations and hash-verified in CI,
exactly as `sync_skill_surfaces.py` already does for count words. Hand-authored
routing is deleted, not relocated. This applies ADR-182 to the surface that was
violating it.

Consequence: a new skill costs **zero** routing-enumeration surfaces. Previously
each new skill cost roughly twelve hand-synced surfaces.

## Evidence emission (intrinsic)

Every skill appends its own run record as part of its own procedure:

```
fired | declined | discipline engaged | did the action change
```

**Where:** each skill's own `runs/ledger.jsonl`, following the convention
`gauntlet` already establishes (`skills/gauntlet/runs/ledger.jsonl`, tracked).
Explicitly **not** `.ledger/entries.jsonl` — that holds `ledger-entry@1` *decision*
records, and `decision-ledger`'s own description already rules run telemetry out of
it. This adds no new convention; it generalises an existing one.

The append is **part of the skill's own procedure**, not a call to an external
service.

Rationale is measured, not theoretical: ECS holds 290 claims, 250 unverified
(86.2%), 207 attributed `claude-unknown` (71.4%), zero `ECS:CALIBRATION` markers
ever written to CLAUDE.md, and zero skills that have ever called `register_claim`.
The MCP server is not always loaded. A loop whose evidence step depends on an
external service fails open, silently, every time. ECS may consume this file when
it is up; the record exists either way.

## Degradation

Every degradation is named in output, never absorbed:

| condition | behaviour |
|---|---|
| `health` cannot reach the registry | whole run `UNKNOWN`; never falls back to a remembered subject list |
| `health` host unreachable / auth failure / tool absent / timeout / bound undeclared | `UNKNOWN` with the distinguishing reason — different reasons have different remedies |
| `did-it-land` cannot reach the runtime | `UNVERIFIED`; never `LANDED`, never inferred from source |
| `triage` has no `health` input | probes minimally itself **and says it did**; never pretends it consumed one |
| **`watch`'s own probe fails** | **that is itself an alert condition.** Silent watcher failure is the worst outcome in this design — it is indistinguishable from "nothing is wrong" |

## Verification

Each skill ships an eval corpus built from **the failure modes of the artifacts it
replaces**, made executable.

Governing rule: **a control must fail against a build that treats absence as
success.** RED before green.

**No check ships on its author's reading of its own green.** This is ADR-184's
finding — in all seven historical instances, the same agent wrote the check and
read its green. It recurred during this very session: a guard written for PR #91
contained a false-positive class (a bare `skills/(\w+)/` regex matches every
GitHub URL for this repo, because the repo name ends in "skills"). The check found
real defects *and* was broken. Only the RED run separated those.

### Acceptance criteria — deliberately not about efficacy

- hand-authored routing lines: **0** (currently: two full SKILL.md bodies)
- routing-enumeration surfaces a new skill must update: **0** (currently ~12)
- `check_no_phantom_skills.py`: green, and proven RED against a seeded stale reference
- membership drift between glob, schema enum, event map, verifier, and manifests:
  structurally impossible, not merely absent

### What v5.0.0 must not claim

The four-arm behavioral campaign found **no arm separation** (primary D>A
`p=0.875`; A=5 B=4 C=7 D=4 of 18). A tidier architecture is not evidence that the
skills improve outcomes. The README must continue to say **UNESTABLISHED**.

### Falsifiers, stated now so they cannot be rationalised later

- If invoking `metacognate` reliably engages disciplines but leaves the action
  unchanged, it is a tax — regardless of how often it declines.
- If `metacognate` auto-fires on routine, reversible, directly-checkable work, its
  description is too broad.
- If `watch` runs 30 days without producing one alert the operator acted on, the
  loop's most valuable member is decorative and the "largest measured hole" was
  mis-measured.

## Sequencing

0. **Solve the `context-audit` firing defect.** Release gate — see above. Nothing
   else in v5.0.0 is worth building until the firing surface is proven sound,
   because every other step assumes it.
1. **Land PR #91 first.** v5.0.0 must not sit on unmerged work.
2. **Build `health` alone, to the bar, and stop.** It already exists as
   `fleet-health` at 9/9, making it the cheapest way to prove the whole pipeline —
   rename, portable/`LOCAL.md` split, `metadata.hands-to`, generated `ROUTING.md`,
   eval corpus, CI — before repeating it four more times.
3. `metacognate` — required before router and helix can be removed.
4. Delete `using-epistemic-skills` and `helix`.
5. `triage`.
6. `did-it-land`.
7. `watch` **last**, because it is the only actuator.

Existing machinery already covers the mechanical half: `check_skill_inventory.py`
enforces glob ↔ schema enum ↔ event map ↔ verifier agreement, and
`sync_skill_surfaces.py --write` regenerates count words across all manifests.

## Out of scope for v5.0.0 (decided, tracked separately)

Command estate disposition — approximately 24 of 43 commands are superseded and
should be deleted, 5 evicted to project repos per ADR-183:

- **Harness-native** (the runtime now does it): `worktree-setup`, `run-all`,
  `parallelize`, `token-report`, `park`, `park-fast`, `wrap-up-fast`,
  `wrap-up-deep`, `sync`, `pull`.
- **Package-native** (already owned by a skill): `decide`, `incident`,
  `open-questions`, `red-team`, `report`.
- **Model-native** (never needed to be an artifact): `techdebt`, `command-audit`,
  `model-analytics`, `pihole-analytics`, `ecosystem-status`.
- **Evict per ADR-183:** `chunk-status`, `dispatch-check`,
  `add-failure-replay-case`, `mac-up`, `fo-repo-hygiene`.
- **Survivors become `reference/` material inside skills, not commands:**
  `nas-troubleshoot` (289 lines of site-specific diagnostics) into `triage`;
  device probes into `health`.

## Blocking requirement: the `context-audit` firing defect

**This is a release gate for v5.0.0, not a follow-up.** Operator decision,
2026-08-06: v5.0.0 does not ship until this is solved.

`epistemic-skills:context-audit` renders with **no description** in the live skill
listing while its file carries a correct one. Replicated in three independent
contexts. A skill with no listed description cannot fire on description match — it
is, functionally, not installed. The entire v5.0.0 design rests on descriptions
being the firing surface, so an unexplained failure of that surface invalidates the
architecture's central assumption.

**Eliminated** (measured 2026-08-06, across the dev checkout and the installed
4.1.0 cache):

| hypothesis | why it is dead |
|---|---|
| file content wrong | both dev and installed copies carry a correct description |
| YAML quoting style | `open-questions`, `recon`, `resolve`, `decision-ledger` are also single-quoted and render |
| description length | `open-questions` (832) and `recon` (878) are **longer** and render; `context-audit` is 762 |
| colons in the value | `recon` has 2, `resolve` and `decision-ledger` have 1; all render |
| a shadowing second `SKILL.md` | only the cache, marketplace, and dev copies exist — all legitimate |
| `settings.local.json` `skillOverrides` | contains only `{"goal": "off"}` |

**Leading hypothesis, and the only dimension not eliminated:** `context-audit` is
the sole skill whose description contains **two** YAML `''` apostrophe escapes
(`document''s`, `task''s`). `decision-ledger` contains exactly one and renders.
A loader that unescapes the first and mishandles the second would produce exactly
this.

**Test — by observation, never by reading the loader:** rewrite the description to
contain no apostrophes, reload, and inspect the live listing. If the description
appears, the cause is confirmed and the fix is a house rule: **no apostrophes in
`description` fields**, enforced by `check_no_phantom_skills.py` or a sibling check.
If it still does not appear, the hypothesis is refuted and the defect is escalated
before any further v5.0.0 work proceeds.

This follows the estate's own method lesson: every significant defect has been
found by an independent measurement disagreeing with a tool, never by reading
source.

## Known open items
- `helix` exists as an 18KB vendored `SKILL.md` in `zms-homelab-main/skills/`
  alongside the package copy. Disposition needed when `helix` is deleted.
- Whether `metacognate` should also be operator-invocable by name in addition to
  auto-firing (assumed yes; costs nothing).
