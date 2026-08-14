# Portable skill projections v2

**Status:** approved for the bounded local Phase-1 vertical slice on 2026-08-14  
**Supersedes for implementation:** `2026-08-14-portable-skill-artifacts-design.md` at SHA-256 `f2dc0409407dc100b0ff055d54611040807149c6c887c5d89163f2344b0aa076`  
**Resolve record:** `../../../../resolve-runs/portable-skill-architecture-2026-08-14/DECISION.md` in the authoring workspace  
**Authority boundary:** local, non-executing Phase 1 only; no live host, remote, installer, custody, guarded, release, or deployment authority

## Decision

Keep one authored canonical package, generate a procedure-free typed IR, and
compile deterministic one-way projections for versioned product/surface/release
profiles. Do not treat one folder or ZIP as a universal behavior contract and do
not maintain independent procedure forks.

```text
canonical authored package
        |
        | deterministic derive
        v
zms-skill-ir@1  (generated, procedure-free)
        |
        | deterministic compile(profile)
        v
native served projection
        |
        | native lifecycle + readback evidence
        v
skill x profile x cumulative-tier cell
```

The transformation is one-way. Neither the IR nor a served projection may
update canonical source. A mismatch is drift or conflict, not a merge
suggestion.

## Why this replaces the frozen design

The frozen design correctly separated structural conformance from discovery,
callability, custody, and guarding, but it used an underspecified
`harness/version` adapter boundary and moved too quickly from canonical source
to artifacts. The full resolve added three requirements:

1. profiles are keyed by product, surface, release or channel, and profile
   revision;
2. a generated typed IR separates source truth from native projection without
   becoming another authored procedure source; and
3. the first slice is mechanically unable to publish, install, execute, or emit
   a host capability tier.

Evil Martians remains useful repository, validation, CI, and marketplace prior
art. Its pinned tree does not prove multi-file dependency closure, package-bound
launchers, runtime/custody conformance, or cross-host equivalence.

## `zms-skill-ir@1`

The IR is generated from the sorted set of direct
`plugins/epistemic-skills/skills/<name>/SKILL.md` children and sparse dependency
metadata. It contains:

- schema and generator revision;
- canonical source kind, full source revision, dirty-state marker, and package
  root;
- canonical package tree digest;
- per-skill normalized identity, description digest, source tree digest,
  member paths and digests, declared dependency roots and digests,
  standalone eligibility or a machine-readable refusal code;
- target profile digest and transform identifier when compiled; and
- an explicit statement that the record attests only structural source and
  projection facts.

The IR must not contain independently authored procedure text, custody policy
or implementation, executable setup logic, secrets, credentials, achieved
capability tiers, or a second hand-maintained skill inventory.

## Sparse dependency contract

`packaging/portability/dependencies.json` is an exception map, not an
inventory. Its top-level keys are schema, package defaults, and per-skill
overrides. An override absent from filesystem discovery is stale and fails.

Local dependency roots are exact repository-relative files or directories.
Absolute paths, `..`, symlinks, missing roots, mount collisions, globs, and
duplicate normalized paths fail closed. Package-bound skills may declare
`suite_only` and a refusal code. For this slice, `manifest` is explicitly
`suite_only` with `PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER`.

## Profile contract

A production profile key is:

`product + surface + release_or_channel + profile_revision`

Profiles eventually record native manifest and skill roots, recursion and
parent rules, installation method, resource path base, trust/consent and reload
requirements, subagent visibility, hook event/schema/CWD/failure policy, exact
guard exclusions, official-source observation, and transform identity.

Phase 1 implements only one local non-host profile:

```json
{
  "product": "zms-local",
  "surface": "non-host-projection",
  "release_or_channel": "working-tree",
  "profile_revision": "phase1-v1",
  "transform": "preserve-canonical-package-layout@1"
}
```

It is not a claim that any external harness accepts the result.

## Phase-1 outputs

The builder writes only to an explicit local output directory:

```text
<out>/
├── PORTABILITY-IR.json
├── PROJECTION-RESULT.json
└── projection/
    └── plugins/epistemic-skills/...
```

`PROJECTION-RESULT.json` binds source, profile, IR, and served-tree digests and
records `structural-only`. It contains no runtime or host tier. Outputs carry
`non_release: true`.

The projection preserves the canonical package layout. No ZIP, installer,
ownership receipt, stable label, release manifest, remote coordinate, host
mutation, executable probe, generated setup script, or capability promotion is
part of this slice.

## Determinism and hashes

Canonical JSON is UTF-8, sorted keys, compact separators, and a final newline.
File digests cover exact bytes. Tree digests cover the domain
`zms-portable-tree-v1\0` followed by sorted normalized relative path, file mode,
and raw content digest records. A second clean run in the same recorded source
state must produce identical IR, result, and projection bytes.

The source record is honest:

- committed mode extracts the named full commit from local Git objects;
- working-tree mode records `working-tree+<HEAD>` and the dirty-state marker;
- working-tree bytes may never be labeled stable or release.

## `manifest`

`manifest` is the first package-bound negative control. Phase 1 includes it in
the complete suite projection but refuses any requested standalone projection
with `PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER`.

The work does not move, copy into a second authored home, execute, or modify
mission-custody code. A later design may add a skill-local path adapter only
after unrelated-CWD custody lifecycle tests exist.

## Failure behavior

The builder fails closed on malformed metadata, stale overrides, invalid or
missing dependency roots, symlinks, path escapes, duplicate projection paths,
frontmatter/name disagreement, empty inventory, an output directory inside the
source package, or a request for a suite-only standalone skill.

Failures occur before output replacement. The builder stages under the output
parent and atomically replaces only an absent or builder-owned prior Phase-1
directory. Foreign content is never pruned.

## Required tests

Tests are written and observed failing before production changes. They prove:

1. one shared discovery/parser/tree primitive feeds both OpenAI and portable
   builders;
2. skill addition/removal changes generated IR without builder inventory edits;
3. stale metadata, absolute/escaping/missing/symlinked dependencies and
   duplicate mounts fail;
4. IR contains digests and refusal data but no `SKILL.md` procedure bodies;
5. two clean fixture builds are byte-identical;
6. the suite projection preserves canonical package layout;
7. `manifest` standalone output is refused with the named code;
8. result evidence is `structural-only`, `non_release: true`, and contains no
   discovered/callable/custody/guarded tier;
9. the script exposes no network, installer, executable-probe, stable, release,
   or live-host path; and
10. existing OpenAI bundle behavior remains unchanged.

## Acceptance

- The filesystem remains the only authored skill inventory.
- IR and projection are deterministic, generated, one-way, and procedure-free.
- Sparse metadata contains only defaults and exceptions.
- `manifest` is present in the suite and refused standalone.
- No Phase-1 output can reasonably be mistaken for a release or host-capability
  attestation.
- Existing OpenAI builder tests and focused inventory checks pass.
- Independent acceptance is still required before merge, release, or any later
  phase.

## Explicit non-goals

- standalone skill archives;
- executable closure scanners or probes;
- live installation, discovery, callability, custody, or guarding;
- stable/remote resolution, signatures, provenance policy, or release;
- host hooks, trust prompts, reload tests, receipts, update, or uninstall;
- mission-custody contract changes;
- LLM-generated compilation or generated setup scripts;
- public catalog or `.well-known` publication; and
- any import or vendoring of Evil Martians skills.
