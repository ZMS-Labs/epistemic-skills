# Portable skill projections — Phase 1

Phase 1 produces a local structural record and a complete canonical-package
projection. It is a compiler walking skeleton, not a host package, installer,
release artifact, or runtime capability attestation.

## Build from the current working tree

Choose an output path outside `plugins/epistemic-skills` that does not already
exist:

```bash
phase1_parent="$(mktemp -d)"
python .github/scripts/build_portable_skill_projection.py \
  --working-tree \
  --out-dir "$phase1_parent/portable-phase1"
```

Working-tree output records `working-tree+<HEAD>`, whether the checkout is
dirty, `mutable: true`, and `non_release: true`. It cannot be relabeled stable
or release.

## Build from a committed local revision

Use a full 40-hex commit already present in the local Git object store:

```bash
phase1_parent="$(mktemp -d)"
revision="$(git rev-parse HEAD)"
python .github/scripts/build_portable_skill_projection.py \
  --source-revision "$revision" \
  --out-dir "$phase1_parent/portable-phase1"
```

The builder extracts the named commit from local Git objects. It performs no
fetch and does not read dirty working-tree bytes for the projection.

## Output

```text
portable-phase1/
├── PORTABILITY-IR.json
├── PROJECTION-RESULT.json
└── projection/
    └── plugins/epistemic-skills/...
```

`PORTABILITY-IR.json` is generated `zms-skill-ir@1`. It records source,
profile, filesystem-derived skill membership, member/dependency digests, and
standalone eligibility/refusal. It contains no independently authored skill
procedure or custody implementation.

`PROJECTION-RESULT.json` binds the source, profile, IR, and projected package
tree. Both JSON files use canonical compact serialization with a final newline.
Portable tree hashes bind the `zms-portable-tree-v1` domain, sorted normalized
paths, normalized `0644`/`0755` file modes, and exact content digests.

## Deliberate refusal

No standalone artifact is emitted in Phase 1. `manifest` is the package-bound
negative control:

```bash
python .github/scripts/build_portable_skill_projection.py \
  --working-tree \
  --standalone-skill manifest \
  --out-dir "$phase1_parent/manifest"
```

This exits non-zero with
`PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER` and creates no output. Other
skills remain `STANDALONE_UNVERIFIED` until a later approved phase proves a
callable standalone layout.

## What Phase 1 never attests

The output is always `structural_only: true` and `non_release: true`. It does
not attest:

- host installation or discovery;
- skill callability or useful model behavior;
- `manifest` mission custody;
- guard enforcement;
- producer authorization or remote provenance;
- transactional update/uninstall behavior; or
- acceptance by an independent reviewer.

The builder creates no ZIP, uses no network client, executes no skill or
artifact code, writes no host root or user state, and does not alter
mission-custody sources.

## Focused verification

```bash
python .github/scripts/test_build_portable_skill_projection.py
python .github/scripts/test_skill_artifact_lib.py
python .github/scripts/test_build_openai_bundles.py
python .github/scripts/check_skill_inventory.py
python .github/scripts/sync_skill_surfaces.py --check
git diff --check
```

Passing these commands establishes the local structural and refusal behavior
they exercise. It is not evidence for any live harness tier.
