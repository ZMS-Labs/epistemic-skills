# Independent post-release review — v5.0.0

**Review date:** 2026-08-06  
**Repository:** `ZMS-Labs/epistemic-skills`  
**Compared support points:** `v4.1.0` (`315e4ea50edb0f1080f45b2b430f3d2994a6f5fe`) → `v5.0.0` (`9c8d8dbb72418cedb1e4a617b2805bee0a0c4525`)  
**Review subject:** the immutable `v5.0.0` tree, its release record, and the architectural judgment embodied by the change from `v4.1.0`  
**Reviewer:** GPT-5.6 Pro, independent of the Claude Opus 5 implementation session  
**Axis:** fixed-artifact post-release judgment audit  
**Docket mode:** manual, degraded  
**Role binding:** materialized review roles in one model context  
**Independence:** cross-family but not panel-isolated; no claim of full Gauntlet procedural independence

## Status and non-retroactivity

This review was performed **after** `v5.0.0` had been tagged and published. It therefore does **not** satisfy release-gate item 8 retroactively and must never be cited as though it did.

The correct historical statement remains:

- item 8 was waived by the repository owner;
- no pre-publication Gauntlet panel, independent arbitrator, Conflict Ledger, or GO verdict existed when `v5.0.0` was published; and
- publication under an explicit exception did not convert the gate into a pass.

This document supplies the missing **judgment analysis** for future maintainers and successor releases. It is a post-release audit of the immutable tag, not a reconstruction of an event that did not happen.

## Executive verdict

**Computed post-release verdict: `NO-GO` for a retrospective GO or a claim that `v5.0.0` fully realizes its approved design.**

This is **not** a recommendation to move, delete, or rewrite the published tag. The release record honestly discloses its exception, and immutable releases must remain immutable. The verdict means:

1. `v5.0.0` should continue to be described as **published under an explicit item-8 exception**, not as publication-gate compliant;
2. the architectural direction is substantially better than `v4.1.0`, but the released implementation is incomplete against its own design contract; and
3. a successor release should not receive GO until the P1 finding is corrected, the P2 conditions are either implemented or explicitly removed from the governing design, and a real independent publication gate is run on the successor's exact commit.

The deterministic suite, CodeQL, full-history secret scan, and clean-room run are meaningful positive evidence about the artifact. They do not answer the judgment question this review addresses.

## Scope and method

The review inspected:

- the tag-to-tag change from `v4.1.0` to `v5.0.0`;
- the deleted `using-epistemic-skills` and `helix` seats;
- the added `metacognate`, `health`, `triage`, `did-it-land`, and `watch` skills;
- the approved v5 design document and its acceptance criteria;
- event schemas, event maps, inventory checks, description-budget controls, CI workflows, and release-security evidence;
- `RELEASING.md`, the committed release notes, the published GitHub Release, README surfaces, and repository metadata; and
- the exact-commit workflow results for the published tag.

Five review roles were materialized sequentially:

1. **Architecture:** whether the new boundary and routing model is an improvement.
2. **Verification:** whether the stated oracles are executable and actually enforced.
3. **Operational safety:** whether the new running-system disciplines are internally coherent and safe to follow.
4. **Release governance:** whether the release record and procedure accurately describe what happened.
5. **Documentation integrity:** whether live user-facing surfaces agree with the released architecture.

Because these roles shared one model context and no independent arbitrator was available, this is a **manual degraded docket**. Findings are evidence-backed, but the procedural limitations are part of the result.

## What v5.0.0 gets right

### 1. Deleting the enumerating router addresses a real shipped defect

In `v4.1.0`, the live `using-epistemic-skills` firing description named `agent-interface-design` and `intent-traced-merge` even though both had already ceased to exist as skills. That is not merely aesthetic drift: descriptions are the firing surface, so the router could direct an agent into a nonexistent seat.

Replacing the enumerating router with a procedure that does not carry a member inventory is therefore a sound architectural correction. It removes a high-churn projection from the most sensitive surface in the package.

### 2. Replacing Helix's pair table is directionally correct

The old Helix table duplicated workflow-stage-to-discipline relationships and imposed a static order. The v5 design correctly identifies two cases a table models poorly:

- either the workflow strand or the epistemic strand may interrupt the other; and
- control must return to the point of interruption after bounded epistemic work.

`metacognate` expresses that control pattern more naturally than a fixed pair registry.

### 3. The evidence corpus was preserved before deleting its former seat

The change correctly distinguished a capability from the directory that happened to contain collection-level evidence. The `epistemic-flexibility`, proportionality, and composition materials were relocated before the router and Helix directories were removed. Results whose subjects disappeared were retired rather than silently reinterpreted.

That is exemplary evidence hygiene. In particular, the null behavioral result remains visible rather than being erased by the architectural rewrite.

### 4. The new disciplines encode honest non-success states

`UNKNOWN`, `UNVERIFIED`, `NARROWED`, and `SUSPECT` are useful first-class outcomes. The skills repeatedly refuse to convert missing observation into success. This is the strongest common design idea in the release.

### 5. Exact-commit artifact verification did occur

Although the release-note table contains a stale intermediate SHA, the final tagged commit itself received the claimed checks:

- `epistemic-flexibility` run `31128924884`: `stdlib-checks` succeeded, with the merge-base-only step correctly skipped;
- CodeQL run `31128924306`: the Actions, JavaScript/TypeScript, and Python analyses all succeeded; and
- `release-security` run `31128925378`: the planted-secret positive control and complete-history scan both succeeded.

The stale SHA is a record defect, not evidence that the final tag escaped verification.

### 6. The release is unusually honest about efficacy

The release does not convert architectural tidiness into an outcome claim. The four-arm result remains `p=0.875`, with no arm separation, and behavioral superiority remains **UNESTABLISHED**. This review affirms that status.

## Findings

### P1 — `watch`'s proof state machine is not executable as written

`watch` declares that a new watcher:

1. ships inert;
2. must remain inert until its kill switch has been exercised;
3. becomes `PROVEN` only after a deliberately crossed bound produces an alert at the destination; and
4. may not be called installed before `PROVEN`.

Its method then says:

1. install inert;
2. exercise the kill switch;
3. confirm the watcher is still inert;
4. cross the bound and confirm the alert arrives.

The required **enable transition is missing**. A watcher that is still disabled cannot observe the crossed bound or deliver the proof alert. The state table also defines `INERT` as "installed, deliberately disabled" while separately prohibiting the word "installed" before `PROVEN`.

This is release-blocking for a GO because it sits inside the skill's iron safety constraints and makes literal compliance impossible. A reader must invent an unstated transition at the exact point where the skill says improvisation is unsafe.

**Required correction:** distinguish `PREPARED`/`INERT` from installed; explicitly authorize and perform an enable step after the kill-switch exercise; confirm active observation; deliberately cross the bound; observe delivery; then assign `PROVEN`. Add an executable negative control showing that the pre-fix sequence cannot alert while disabled.

### P2 — the released tree does not fully implement the approved v5 design

The approved design requires all of the following:

- generated `ROUTING.md` from `metadata.hands-to`, hash-verified in CI;
- intrinsic per-skill run records;
- an executable eval corpus for each new skill, derived from the failure modes it replaces; and
- inventory drift made structurally impossible rather than merely checked after duplication.

The released tree does not contain the generated routing artifact. The four operational skill directories contain only `SKILL.md`; `metacognate` adds only the routine-fast-path reference. No new skill carries the promised eval corpus or intrinsic run ledger.

The implementation instead duplicates skill and event inventories across JSON and Python and runs a consistency check. That is useful, but it is **detection**, not structural impossibility.

**Required disposition:** either implement these design commitments or amend the design and release claims so they no longer say they exist. Silent partial implementation is the unacceptable middle state.

### P2 — sentinel fixture names are placeholders, not verified fixtures

The skill event map names fixtures such as:

- `health-unknown-not-ok.json`;
- `triage-plausible-not-observed.json`;
- `did-it-land-source-read-as-landed.json`;
- `watch-silence-read-as-healthy.json`; and
- `metacognate-over-under.json`.

Those files are not present in the released contract examples or the new skill directories. `check_skill_inventory.py` checks only that the `sentinel_fixture` field is a non-empty string. Its success message therefore means "each map row contains a fixture name," not "each fixture exists and passes."

**Required correction:** bind each map entry to a repository path, require existence, execute the fixture, and include a seeded RED control proving that absence-as-success behavior is rejected.

### P2 — the release procedure is obsolete and internally impossible for v5

`RELEASING.md` remains hard-coded to `3.0.0`, a release branch named for 3.0.0, and a Helix/Gauntlet publication step. `v5.0.0` deletes Helix, so the governing procedure refers to an artifact that cannot be run.

The document also contains no explicit exception model. The owner can authorize publication despite an unmet gate, but that authority must not be confused with the gate being met. A conforming release and an exception release need distinct, explicit records.

**Required correction:** make the procedure version-neutral; replace Helix-specific language with the current publication-judgment gate; define which gates are non-waivable; and define an exception release as published-but-nonconforming, with the unmet gate and owner authorization recorded before tag creation.

### P2 — the release record has stale and incomplete gate accounting

The release-note table repeatedly says items 5 and 6 were satisfied on `3a18cd3`. The immutable tag and final GitHub Release target `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525`, and the final-commit workflows did pass. The table should cite the final commit and run IDs.

The table also omits gate item 7 entirely. Gate item 6 includes both the secret scan **and** public-content/provenance review, but the release record demonstrates the former and does not identify a v5-specific artifact for the latter.

**Required correction:** publish an erratum that distinguishes:

- what is verified on the final tag;
- what is recorded elsewhere with an immutable reference;
- what is unestablished; and
- what was explicitly waived.

Do not silently promote missing records to passes.

### P2 — live user-facing surfaces still describe the deleted architecture

At the released tag:

- the README's `metacognate` diagram says "entry point and twelve disciplines" although the package declares thirteen;
- the epistemic arc still labels a node "Epistemic router";
- the README still says "Agent Interface Design fires inside the build stage" although that skill is retired into reference doctrine; and
- the GitHub repository description still says the collection is tied together "with a router."

These are not historical archives; they are live navigation surfaces. The phantom-skill check misses them because it permits retired names in prose and broadly excludes `docs` from path scanning.

**Required correction:** align the live README and repository metadata, and extend the check to distinguish historical evidence from live routing prose rather than treating all prose as exempt.

### P2 — the description-budget guard counts characters, not UTF-8 bytes

`check_description_budget.py` calls `len(value)` while naming its unit bytes. This is equivalent only for ASCII. A future non-ASCII description would consume multiple UTF-8 bytes in the harness while the guard counted one character.

**Required correction:** use `len(value.encode("utf-8"))` and add a non-ASCII self-test.

### P3 — the new operational loop is described too literally

The release says "watch notices." The package ships a Markdown discipline that instructs an agent how to specify, install, and prove an **external watcher**. The skill itself is not a scheduler or unattended process.

This distinction matters because the same skill correctly insists that a configuration file is not a watcher. The release should not make the parallel mistake of treating a skill specification as the running observer.

**Required correction:** say that `watch` specifies and proves the external observer that notices; `health` reads state; `triage` diagnoses; and `did-it-land` verifies runtime effect.

### P4 — editorial defect in `health`

The Oracle section contains the sentence "A control that passes on a path production does not take proves nothing either." Correct the grammar without changing the rule: a positive control must exercise the same path production uses.

## Conflict Ledger

### Conflict 1 — deletion of the router versus loss of an inspectable map

- **Architecture position:** the enumerating router was a drift-prone projection and should be deleted.
- **Verification position:** the design still needs a generated, non-authoritative view of handoffs so the system can be audited.
- **Ruling:** **SPLIT.** Deleting the live enumerating firing surface is upheld. The design's promised generated routing projection must be implemented or explicitly withdrawn; hand-authored duplication must not return.

### Conflict 2 — owner authority versus gate integrity

- **Owner-authority position:** the repository owner may decide to publish despite an unmet process gate.
- **Governance position:** a hard gate cannot be both waived and described as satisfied.
- **Ruling:** **UPHELD-WITH-QUALIFICATIONS.** The owner may authorize an exception release. That decision changes the publication decision, not the historical truth value of the gate. The release remains nonconforming on that item and has no GO.

### Conflict 3 — artifact verification versus design judgment

- **Release position:** deterministic checks, CodeQL, secret scanning, and clean-room execution passed.
- **Adversarial position:** none of those checks evaluates whether the architecture is sound.
- **Ruling:** **SPLIT.** Both statements are true. Artifact integrity is positively supported; design judgment was absent at publication and receives a negative post-release verdict here.

### Conflict 4 — operational capability versus specification

- **Product position:** the release adds a closed operational loop.
- **Implementation position:** the package adds disciplined instructions, not deployed probes, schedulers, destinations, or runtime observers.
- **Ruling:** **UPHELD-WITH-QUALIFICATIONS.** The conceptual loop is coherent, but the release must describe it as a protocol for building and proving external operational mechanisms.

### Conflict 5 — preserved historical evidence versus evidence for the new architecture

- **Evidence position:** the old evaluation corpus and null result were preserved correctly.
- **Verification position:** the new entry point and four new operational skills have no dedicated executable corpus.
- **Ruling:** **SPLIT.** Preservation is upheld. The historical result cannot be treated as validation of the newly introduced behavior.

### Conflict 6 — package budget control versus installed availability

- **Control position:** the new 8,200-byte ceiling prevents this package from drifting upward silently.
- **Runtime position:** the live harness cap is estate-wide, and the package cannot guarantee that all descriptions survive alongside other installed skills.
- **Ruling:** **UPHELD-WITH-QUALIFICATIONS.** The package-local guard is valuable. Installation documentation must continue to label live availability as estate-dependent until a harness-level inventory check proves otherwise.

## Decision matrix

| Priority | Finding | Required owner | Status on immutable `v5.0.0` |
|---|---|---|---|
| **P1** | `watch` cannot reach `PROVEN` by following its written state transitions | successor-release implementer | **OPEN** |
| **P2** | generated routing, intrinsic run records, and new-skill eval corpora absent against approved design | maintainer | **OPEN** |
| **P2** | sentinel fixtures named but nonexistent/unexecuted | maintainer | **OPEN** |
| **P2** | `RELEASING.md` hard-coded to 3.0.0 and deleted Helix | maintainer / owner | **OPEN** |
| **P2** | stale SHA and incomplete item 6/7 accounting in release record | release maintainer | **OPEN** |
| **P2** | README and repository metadata retain deleted architecture | documentation owner | **OPEN** |
| **P2** | description-budget unit is characters, not UTF-8 bytes | maintainer | **OPEN** |
| **P3** | release overstates the skill itself as an unattended observer | documentation owner | **OPEN** |
| **P4** | `health` Oracle grammar defect | maintainer | **OPEN** |

## Conditions for a successor release to seek GO

```json
[
  {
    "condition": "Correct watch's inert-enable-prove state machine and add an executable negative control that fails against the v5.0.0 sequence.",
    "falsifier": {
      "method": "run the watcher fixture from an inert state through kill-switch exercise, explicit enable, deliberate crossing, delivery observation, and verdict assignment",
      "threshold": "the fixed sequence reaches PROVEN only after delivery; the v5.0.0 sequence cannot produce a false PROVEN",
      "timeframe": "before the successor tag"
    },
    "owner": "successor-release implementer"
  },
  {
    "condition": "Resolve every approved-design commitment that is absent from the tree: implement it or amend the design and all release claims explicitly.",
    "falsifier": {
      "method": "diff the successor tree against the v5 design acceptance criteria",
      "threshold": "zero silent partial-implementation rows",
      "timeframe": "before publication review"
    },
    "owner": "maintainer"
  },
  {
    "condition": "Create and execute real sentinel fixtures for all five v5 entry/replacement skills, with seeded RED controls and CI existence checks.",
    "falsifier": {
      "method": "delete or corrupt one fixture and run CI; run each fixture against an absence-as-success implementation",
      "threshold": "CI fails on missing/corrupt fixtures and every seeded bad implementation is rejected",
      "timeframe": "before the successor release commit is frozen"
    },
    "owner": "maintainer"
  },
  {
    "condition": "Replace the hard-coded release procedure with a version-neutral procedure and explicit exception semantics.",
    "falsifier": {
      "method": "walk the written procedure against the successor release without improvisation",
      "threshold": "every step is executable with current artifacts; every unmet gate is recorded as unmet or waived, never passed",
      "timeframe": "before release preparation begins"
    },
    "owner": "repository owner"
  },
  {
    "condition": "Align all live navigation and release surfaces, including the exact final commit and gate items 6 and 7.",
    "falsifier": {
      "method": "machine-check live README/metadata/version surfaces and manually reconcile the gate evidence table",
      "threshold": "zero stale skill/router claims and every gate row points to an immutable artifact or says UNESTABLISHED/WAIVED",
      "timeframe": "on the exact successor release commit"
    },
    "owner": "release maintainer"
  },
  {
    "condition": "Run the real independent Gauntlet publication gate on the exact successor release commit.",
    "falsifier": {
      "method": "isolated lens passes, independent arbitration, Conflict Ledger, and recorded verdict",
      "threshold": "GO with no unresolved P1/P2; otherwise publication is held or explicitly recorded as another exception release",
      "timeframe": "before tag creation"
    },
    "owner": "independent reviewer and repository owner"
  }
]
```

## GO coverage statement

- **Capability families exercised:** routing architecture, operational-state semantics, verification contracts, event/inventory machinery, release governance, documentation integrity, and exact-commit CI evidence.
- **Material assumptions reviewed:** descriptions are the firing surface; removing enumerated routing reduces drift; new operational disciplines form a loop; unknown states prevent false success; release gates bind publication claims; preserved evidence remains relevant only to its original subject.
- **Known unknowns / untested behavior:** live firing behavior across every supported harness; installed-estate description survival outside the measured Claude Code estate; real-world alert delivery and reversion windows; independent outcome effects of the new architecture.
- **Evidence freshness:** repository and GitHub release state observed on 2026-08-06 against immutable `v4.1.0` and `v5.0.0` coordinates.
- **Residual uncertainty:** the review is cross-family but not a formally isolated multi-agent Gauntlet. Findings are suitable as a corrective audit and successor-release docket, not as a retroactive item-8 certification.

## Bottom line

`v5.0.0` is not a failed release in the ordinary software-artifact sense. Its tagged artifact is internally coherent enough to build and pass its deterministic/security checks, it preserves contrary evidence, and its central architectural move—removing the enumerating router—is justified by a real defect in `v4.1.0`.

It is, however, **not entitled to a GO after the fact**. The most safety-sensitive new skill contains an impossible proof sequence, several approved design commitments are represented only in prose, and the release-governance/documentation surfaces were not fully migrated with the architecture. The correct durable record is therefore:

> **Published under an explicit item-8 exception; artifact checks passed; behavioral superiority unestablished; independent post-release judgment verdict NO-GO for retrospective certification; successor release conditions recorded above.**
