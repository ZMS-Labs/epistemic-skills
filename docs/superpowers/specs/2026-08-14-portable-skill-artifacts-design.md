# Portable skill artifacts and honest harness capability

**Status:** proposed; quarantined design artifact awaiting operator review  
**Subject baseline:** `af7b72fe0460876fb96a458daaa44c7b008449cf`  
**External comparison:** Evil Martians `agent-skills` at `a2a83b280a2c5b9a6176c5934298fad0224bbce4`  
**Implementation authority:** none until this design is approved

## Decision

Add a capability-typed, dependency-closed distribution layer around the one
canonical `plugins/epistemic-skills/` package. Reuse the repository's existing
deterministic discovery, hashing, and archive primitives. Generate inventories
and artifacts from source; never add another hand-maintained skill list.

The layer will make four claims separately:

1. what source bytes belong to a skill or suite artifact;
2. whether the artifact is structurally installable;
3. what execution capability has actually been proved in a named harness; and
4. whether a live harness guard has actually blocked a seeded denied action.

The design does **not** make one universal folder synonymous with universal
behavior. Support is always a claim about a frozen tuple of skill, artifact
digest, harness and version, environment, and evidence.

The first implementation slice is deliberately packaging-only: a sparse
dependency contract, generated truth index, deterministic complete-suite
artifact, and fail-closed standalone eligibility checks. It does not move or
modify mission-custody runtime code.

## Problem

The repository already has a strong canonical-package model and deterministic
OpenAI/ChatGPT bundles. Those archives include all of
`plugins/epistemic-skills/`, so package-external skill dependencies remain
present.

The documented generic install rooted at
`plugins/epistemic-skills/skills/` is different. A generic installer may copy
only one skill subtree. Several skills depend on package siblings:

- `manifest` invokes the mission-custody CLI under
  `contracts/mission-custody/`;
- `watch` uses the watch-commission contract and verifier;
- Gauntlet scripts load canonical roles under `agents/`;
- other methods refer to package-level contracts or the shared run-ledger
  schema.

A copied `SKILL.md` can therefore be discovered while its promised procedure is
not executable. File-format compatibility, discovery, advisory execution,
custody, and runtime enforcement are different facts and need different
oracles.

The Evil Martians repository is useful prior art for simple, multi-file, and
bundle-shaped skills, validation, and publication visibility. It is not an
implementation dependency. Its packaging model assumes the needed files are in
the exported unit; this repository must first make its own package-external
closures explicit.

## Options considered

| Option | Description | Strength | Limitation | Decision |
|---|---|---|---|---|
| A. Projection cleanup only | Generate inventory and installer lists while preserving existing link-based deployment | Quickly eliminates list drift | Leaves mutable, non-atomic, package-incomplete installs | Use only as an early slice of B |
| B. Capability-typed, dependency-closed artifacts | Generate source truth, deterministic artifacts, stable/development channels, and evidence-bound harness tiers | Separates packaging truth from runtime truth and supports thin adapters | Requires staged implementation and harness-specific proof | **Selected** |
| C. Universal runtime or broker | Put execution, custody, and guards behind one runtime API | Could eventually improve behavior parity | Blocked by real hook, custody-epoch, effect-envelope, and concurrency limits | Defer |

## Vocabulary

### Source shape

- `single-file`: only `SKILL.md` is required.
- `multi-file`: all required bytes already live under the skill directory.
- `package-bound`: the method requires one or more paths outside its skill
  directory or a harness-native adapter.

Source shape is derived from the declared closure plus the bounded reference
scan defined below, not selected for marketing. It is a packaging claim, not a
proof that every possible execution path has been exercised.

### Artifact form

- `native-suite`: the full canonical plugin/extension package in its existing
  layout.
- `portable-suite`: a deterministic, revision-bound archive containing the
  complete canonical package plus its generated index.
- `standalone-skill`: one standard Agent Skills directory whose required local
  files are present at paths the installed `SKILL.md` can actually invoke.

A `package-bound` source may become a `standalone-skill` only after a tested
path binding or skill-local launcher makes the assembled closure callable.
Copying extra bytes into an unreachable directory does not qualify.

### Artifact conformance

Artifact conformance is an independent evidence object, not an execution tier.
An `epistemic-artifact-conformance@1` result binds an artifact digest, parent
index digest, embedded metadata digest, expected artifact form, actual unpacked
member manifest, verifier revision, layout/path-binding probes, and `PASS` or
named failures. A PASS says the frozen bytes match their declared package
contract. It says nothing about a harness discovering them or a method behaving
correctly.

### Execution tier

Tiers are cumulative evidence claims, not source labels. Tier `N` requires a
passing artifact-conformance result and every lower tier:

1. `discovered` — the named harness loaded the conforming artifact with the
   expected source and digest.
2. `advisory-capable` — the method completed or entered its declared supported
   degradation without a missing, undeclared file, tool, or capability.
3. `custody-capable` — the named runtime proved durable persistence, receipts,
   resume/drift behavior, and independent acceptance for the frozen artifact.
4. `guarded` — the exact installed adapter blocked a seeded call because the
   expected guard rule matched, while a neighboring allowed control traversed
   the same boundary successfully. Evidence binds the artifact, hook/adapter,
   harness, tool class, matched rule ID, deny and allow payloads, and independent
   readback.

A parser error, unrelated policy denial, or block-all adapter cannot establish
`guarded`. An unavailable live harness is `BLOCKED_EXTERNAL` or `unverified`;
it is never promoted by static inspection. Cursor IDE and Cursor CLI are
separate harness surfaces because their hook behavior differs.

### Stable and development channels

- `stable` resolves only an immutable tag or full commit SHA, builds from that
  Git object tree rather than current working-tree bytes, verifies artifact and
  member digests, materializes copied bytes, and writes an ownership receipt.
  Later source-checkout edits cannot change installed bytes.
- `development` is explicit opt-in. It may link a named checkout or worktree,
  records the resolved path and HEAD SHA, and is labeled mutable.

Mutable default-branch tracking is never called stable.

## Source of truth

### Filesystem inventory

The only skill inventory authority remains the sorted set of direct
`plugins/epistemic-skills/skills/<name>/SKILL.md` children. The existing
frontmatter parser and validation rules remain authoritative. A new skill,
rename, or deletion changes the generated inventory without editing builder
code, documentation tables, workflows, or manifests.

### Sparse dependency metadata

Add `packaging/portability/dependencies.json`. It is an exception map, not an
inventory. Its schema has:

- package-wide defaults that apply to every discovered skill, such as the
  shared run-ledger contract when required by the output contract;
- per-skill package-external roots;
- the intended artifact-relative mount point;
- any required source-level launcher or path binding;
- safe artifact-conformance probe entry points and their expected results;
- external environmental capabilities that cannot be packaged;
- attainable tiers and adapter requirements; and
- the applicable custody contract epoch, where relevant.

Each local dependency is an exact repository-relative file or directory root.
Directory roots include their regular-file descendants in sorted order. Globs,
absolute paths, `..` escapes, symlinks, missing paths, duplicate archive paths,
and mount collisions are rejected. An override naming a skill absent from the
filesystem inventory is stale and fails CI.

The metadata may declare a skill `suite-only` until a callable standalone path
exists. That is a supported honest state, not a build failure. Requesting a
standalone artifact for such a skill is a named refusal and non-zero exit.

Dependency declaration is not allowed to certify itself. A versioned reference
scanner supplies a second, bounded oracle over every Markdown, Python, JSON,
TOML, and YAML file in the skill subtree and its declared local dependencies.
It classifies:

- Markdown links and inline/code-block path tokens rooted at
  `plugins/epistemic-skills/`, `skills/`, `contracts/`, `agents/`,
  `reference/`, or `evals/`;
- constant Python path strings rooted at those locations and statically
  resolvable constant `Path(__file__)` joins;
- path-bearing manifest values under the closed key set `path`, `source`,
  `skills`, `agents`, `hooks`, and `commands` when they resolve into the
  canonical package; and
- explicitly declared runtime-output roots and environmental paths, which are
  not package dependencies.

Every recognized package reference must land inside the assembled closure.
Every package-root-like token the scanner cannot classify is an
`UNCLASSIFIED_REFERENCE` failure until metadata or the scanner grammar is
corrected. Runtime outputs such as `missions/` are allowed only through the
separate runtime-output declaration; they never silently enter the artifact.

This scanner is intentionally not described as a complete semantic analysis of
arbitrary prose or Python. Each standalone-eligible skill also declares a
closed set of safe conformance probe entry points. Those probes execute from an
unpacked artifact with the current source checkout absent from import/search
paths and with a working directory outside the artifact. The closure claim is
therefore bounded and explicit: all declared dependencies and all references
recognized by scanner version `v1` resolve, and the declared entry points run
from the frozen artifact. Unexercised behavior remains a runtime-evidence
limit, not an artifact PASS.

### Generated portability index

Every build emits `PORTABILITY-INDEX.json` with schema
`epistemic-portability-index@1`. It contains:

- source repository, source kind (`git-commit` or explicit `working-tree`), full
  commit revision, and dirty-state marker when applicable;
- canonical package root and inventory rule;
- builder/schema revision;
- reference-scanner revision and any bounded residual coverage statement;
- each discovered skill's name, description digest, source shape, source-tree
  digest, resolved local dependency roots, closure digest, standalone
  eligibility, external requirements, attainable tiers, adapter requirements,
  and custody contract epoch when applicable;
- canonical-package content digest (computed only from source members, never
  from generated index/checksum files); and
- an explicit statement that attainable tiers are not achieved-tier evidence.

The index is generated only. The suite archive embeds these exact index bytes.
Each standalone archive instead embeds `PORTABILITY-ENTRY.json` inside its one
top-level skill directory; that file contains the exact generated entry for the
skill plus the parent index digest and source identity. No README, installer,
or harness adapter may own a second list of skill names.

## Build architecture

Extract the generic discovery, frontmatter, regular-file, tree-hash, and
deterministic-ZIP helpers from `.github/scripts/build_openai_bundles.py` into
`.github/scripts/skill_artifact_lib.py`. Both the existing OpenAI builder and
the new portable builder consume that stdlib-only module. This is one inventory
engine with multiple artifact projections, not two implementations that happen
to agree today.

Production builds resolve a full 40-hex commit and extract the relevant source
from Git objects into a temporary tree. They never label current working-tree
bytes with `git rev-parse HEAD`. An explicit `--working-tree` development mode
is allowed only with a `working-tree+<HEAD>` source label and dirty-state field;
it cannot emit a stable artifact. Unit tests may pass an isolated fixture root.

The new builder produces:

```text
dist/portable/
├── ARTIFACT-MANIFEST.json
├── PORTABILITY-INDEX.json
├── epistemic-skills-suite-<revision>.zip
├── skills/
│   └── <name>-<revision>.zip     # only for standalone-eligible skills
├── conformance/
│   └── <artifact-digest>.json
└── SHA256SUMS
```

Generated archives remain CI or release artifacts and are not committed.
Member order, timestamps, permissions, line endings, archive roots, and JSON
serialization are deterministic. Two clean builds of the same revision must
be byte-identical. The index is copied into the suite archive but never
contains the digest of that archive or any digest whose input includes the
index itself. After archives are closed and independently verified, the
external `ARTIFACT-MANIFEST.json` binds the index digest to every final archive
digest and artifact-conformance-result digest; `SHA256SUMS` is its plain-text
checksum projection. Neither external file is embedded. This ordering avoids a
self-referential build contract.

All hashes use SHA-256 with explicit domains:

- a file digest covers exact file bytes;
- a tree/closure digest covers
  `UTF8("epistemic-closure-v1\0")` followed by sorted records of normalized
  artifact-relative path, normalized file mode, source role/mount, and raw file
  digest; changing a mount point or mode changes the digest;
- the index and artifact-manifest digests cover their canonical UTF-8 JSON
  bytes (sorted keys, fixed separators, final newline); and
- an archive digest covers the final ZIP bytes.

Conformance results are generated by a separate verifier after unpacking and
are never inputs to the artifact they assess. Build-time conformance results
contain no wall-clock field and are deterministic for identical artifact and
verifier digests; later live harness evidence carries its own observation time.

The complete-suite archive preserves the canonical package layout. This proves
byte/layout closure only; it does not prove a harness working directory or
installed call path. Standalone archives have exactly one top-level skill
directory containing `SKILL.md` and supporting files. They are emitted only
when every declared and recognized local dependency is inside that directory
at a path exercised by the artifact-conformance probes.

## `manifest` treatment

`manifest` is the first load-bearing closure test.

At the design baseline, it is `package-bound` and `suite-only`: its skill
directory contains instructions and run-ledger examples, while its executable
custody core lives under `contracts/mission-custody/`. A generic build that
copies only the skill directory must fail the completeness test. It may claim
no execution tier. A later harness record may reach `discovered` for those
bytes, but never custody capability from that SKILL-only artifact.

The staged standalone design is:

1. add a skill-local launcher under `skills/manifest/scripts/` that is the one
   path named by `SKILL.md`;
2. make every supported native and portable adapter resolve that launcher from
   the installed skill root rather than assuming a repository working
   directory;
3. keep the mission-custody implementation canonical in its current contract
   directory for this workstream;
4. during standalone assembly, mount the frozen custody core beneath the
   launcher at a deterministic skill-local path;
5. test the launcher from the native-suite layout and from an unpacked
   standalone artifact with CWD outside both trees; and
6. emit the standalone artifact only after the custody CLI, resume/drift,
   receipt, and acceptance probes pass from the unpacked tree.

The launcher is path adaptation only. It must not change record schemas,
contract behavior, guard behavior, or contract epoch.

Suite-byte presence alone is not callability. Each achieved execution tier must
record how the harness resolved the absolute installed launcher path. An
unresolved plugin-hook CWD or skill-root location keeps execution unverified
even when artifact conformance passes.

Packaging conformance and guarding remain separate:

- `custody-capable` requires the installed CLI and custody lifecycle probes;
- `guarded` additionally requires a live harness hook, exact matched rule, and
  paired deny/allow probes through the same boundary for the exact harness and
  tool class;
- Antigravity remains below `guarded` until its adapter is implemented and
  live-fired;
- Cursor CLI remains below the Cursor IDE result while marketplace hooks are
  ignored there.

## Custody evolution boundary

This distribution workstream records and preserves mission-custody contract
epoch 1. It does not implement or write contract@2 records, add an external
tail anchor, migrate mission stores, or enable concurrent active missions.

The reader-before-writer, stale-reader, anchor, rollback, effect-envelope, and
concurrency questions remain governed by the custody evolution work referenced
in issues #118, #166, and #173. This packaging design neither restates nor adds
future runtime requirements. If that governing design changes epoch or rollout
rules, a separate reviewed portability change may teach the index about the new
frozen contract; the artifact layer must not initiate the transition.

## Installer and adapter contract

Native package installation, portable artifact installation, and runtime
behavior are tested independently.

An installer must:

- consume the generated index rather than enumerate skills;
- accept exactly one channel, `stable` or `development`;
- reject an unpinned stable source;
- verify artifact and member digests before mutation;
- detect native-plus-generic duplicates;
- detect a wrong existing link, stale owned skill, partial inventory, and
  unsupported harness;
- update add/change/remove/repoint cases rather than report `exists, skipped`;
- prune only paths named in its prior ownership receipt; and
- preserve foreign harness content.

An ownership receipt records source revision, index and artifact digests,
channel, target harness and version, installed paths, install time, and adapter
revision. It is local/private state: Unix-like systems store it below
`$XDG_STATE_HOME/epistemic-skills/install-receipts/` (falling back to
`~/.local/state/...`), and Windows stores it below
`%LOCALAPPDATA%\epistemic-skills\install-receipts\`. It persists while any owned
path remains and for 30 days after a verified uninstall. It is never committed
or uploaded. The receipt proves what the installer owned; it does not prove an
execution tier.

Public conformance/runtime evidence is a minimized projection with a closed
schema: artifact/index/adapter digests, harness and version, OS family,
environment-class identifier, probe IDs, timestamps, verdicts, and evidence
references only. It excludes usernames, absolute paths, hostnames, private
repository coordinates, environment variables, payload content, and
credentials. Public-content and secret scans include positive leakage controls.
Detailed local probe receipts remain in the local/private evidence store for
the lifetime of the supported artifact; their public projection may be retained
with the immutable release evidence.

Official `gh skill` commands may be piloted as one backend while preview
semantics are monitored. They are not the sole installation authority in this
design. The existing `npx skills` route is not called complete for
package-bound skills until an end-to-end dependency-closed probe passes.
Public `.well-known/agent-skills` publication is outside scope.

## Downstream repository boundary

Each source repository owns its canonical skills, sparse source metadata,
generated index, and artifact digests. A downstream private fleet repository
may own machine paths, selected harness profiles, and rollout policy. Consumer
conformance requires it to consume a source-owned index rather than enumerate
skill names.

This keeps the dependency graph acyclic:

```text
source repo filesystem + sparse metadata
                    |
                    v
      generated index + immutable artifacts
                    |
                    v
       thin harness / fleet consumer adapters
                    |
                    v
       separate runtime conformance evidence
```

Private package content, private source coordinates, credentials, and local
topology are never copied into this public repository or a public catalog.
This repository proves only the consumer interface, fixtures, and adapters it
ships. A downstream repository proves its own conformance with a versioned CI
attestation bound to source-index and adapter digests; absence of that
attestation is `unverified`, not a public-build failure or an inferred pass.

## Implementation phases

### Phase 1 — truth index and suite artifact

- Refactor shared deterministic builder primitives without behavior change.
- Add sparse dependency schema and metadata.
- Build immutable artifacts from Git object trees.
- Generate `PORTABILITY-INDEX.json`, external `ARTIFACT-MANIFEST.json`, a
  complete-suite archive, and independent artifact-conformance results.
- Refuse standalone output for every unresolved package-bound skill.
- Correct documentation that currently describes the raw skills subtree as a
  complete generic install.

### Phase 2 — safe standalone subset

- Emit standalone archives only for already self-contained skills.
- Add omission, path-escape, wrong-nesting, and determinism negative controls.
- Prove an unpacked artifact, not merely the source tree.

### Phase 3 — package-bound path adapters

- Add source-level path launchers one skill at a time, beginning with
  `manifest`.
- Assemble declared closures into standalone artifacts.
- Run the skill's existing contract suites from each unpacked artifact.
- Do not combine path adaptation with contract behavior changes.

### Phase 4 — stable/development installer

- Add receipt-backed copy installs for stable artifacts.
- Add explicit mutable link installs for development.
- Test adapters in temporary homes and detect duplicate/native collisions.

### Phase 5 — runtime evidence

- Record achieved tiers per artifact, harness/version, environment, and probe.
- Keep unavailable live surfaces blocked/unverified.
- Promote to `guarded` only from a matched-rule denial plus a neighboring allow
  control through the same exact installed adapter and tool boundary.

## Required tests

The implementation plan must introduce failing tests before production changes.
At minimum it covers:

1. filesystem discovery adds and removes skills without builder edits;
2. stale override names and phantom skills fail;
3. every reference recognized by scanner `v1` is classified and resolves;
   unclassified package-root-like tokens and omitted declared dependencies fail;
4. absolute, escaping, symlinked, missing, or colliding paths fail;
5. two clean Git-object builds of one revision are byte-identical, while a
   dirty working tree cannot forge that revision label;
6. archive member order, roots, permissions, and timestamps are fixed;
7. a `manifest` SKILL-only artifact is refused;
8. an unpacked complete-suite artifact passes layout conformance without being
   promoted to custody-capable;
9. a later native-layout and standalone `manifest` launcher runs custody
   lifecycle tests from an unrelated CWD and without the source checkout on
   import/search paths;
10. native and portable OpenAI builders use the same discovered inventory;
11. duplicate native plus generic installation fails;
12. partial expected inventory fails even when other skills remain;
13. stable source mutation cannot change installed bytes;
14. development source mutation is reflected and labeled mutable; and
15. presence-only checks cannot produce `advisory-capable`,
    `custody-capable`, or `guarded` evidence;
16. a parser error, unrelated deny, and block-all adapter cannot establish
    `guarded`, while the matched deny plus neighboring allow control can; and
17. public evidence rejects absolute paths, usernames, private coordinates,
    environment values, and seeded secret patterns while retaining the minimal
    allowed fields.

The focused public-repository verification set is expected to include:

```bash
python .github/scripts/test_build_portable_skill_exports.py
python .github/scripts/build_portable_skill_exports.py --check --source-revision "$(git rev-parse HEAD)"
python .github/scripts/verify_portable_skill_artifacts.py dist/portable/ARTIFACT-MANIFEST.json
python .github/scripts/test_portable_skill_workflow.py
python .github/scripts/test_build_openai_bundles.py
python .github/scripts/check_skill_inventory.py
python .github/scripts/sync_skill_surfaces.py --check
python plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
```

The full clean-room suite remains the final deterministic gate.

## Acceptance criteria

- One filesystem-derived inventory feeds every generated artifact.
- Sparse metadata contains exceptions and dependencies, never a duplicate full
  skill list.
- Stable artifacts are built from the named Git object tree, deterministic,
  and bound by the external artifact manifest and checksums.
- Every declared dependency and every reference recognized by the pinned
  scanner resolves inside the artifact or is classified as runtime output or
  an environmental dependency; residual semantic coverage is stated rather
  than promoted to proof.
- Artifact conformance is a separate, digest-bound result and does not imply
  discovery or behavior.
- Standalone generation refuses skills whose closure is incomplete or whose
  installed paths are not callable.
- The complete-suite artifact preserves all current canonical paths.
- `manifest` is never called custody-capable from a SKILL-only install.
- Package conformance never implies a hook fired.
- Cumulative achieved execution tiers are bound to artifact digest,
  artifact-conformance result, harness/version, minimized environment class,
  and evidence.
- Stable and development installs cannot be confused.
- The public consumer interface and shipped adapters reject manual inventory;
  downstream repositories establish their own status only through a
  digest-bound consumer-conformance attestation.
- No contract@2, concurrency, live hook activation, public catalog, or private
  source disclosure enters this workstream.

## Explicit non-goals

- Vendoring or importing Evil Martians skills.
- Replacing Superpowers or creating a universal runtime broker.
- Claiming equivalent judgment quality across models or providers.
- Treating `.agents/skills` as a universal discovery guarantee.
- Publishing private skills or a public private-package catalog.
- Default-branch tracking for stable installs.
- Contract@2 implementation, anchor migration, or mission-store migration.
- Concurrent active missions.
- Antigravity custody-adapter implementation.
- Live harness activation, global configuration mutation, merge, release, or
  deployment.

## Provenance

- Existing architecture and release policy in this repository.
- Existing deterministic OpenAI bundle implementation and tests.
- Evil Martians `skills-visibility` packaging guidance at the frozen external
  comparison commit.
- Public mission-custody issues #118, #129, #166, and #173.
- Read-only cross-repository reconnaissance performed on 2026-08-14; private
  implementation details intentionally omitted from this public artifact.
