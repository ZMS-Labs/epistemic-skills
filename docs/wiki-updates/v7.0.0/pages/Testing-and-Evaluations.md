> **Applies to:** epistemic-skills v7.0.0 candidate (unreleased).
> Source checks, loaded context, exercised workflows and comparative benefit are distinct.

# Testing and evidence

The [current evidence packet](../../../release/v7-evidence.md) records R01-R22,
implementation revisions, affected checks, runtime coverage and unresolved limits.
Source checks validate contracts; loaded-context evidence establishes what the
host received; exercised workflows test behavior; comparative results evaluate
bounded benefit. None implies the next tier automatically.

Run the current snapshot check with:

```text
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.0.0/pages
```

Preserve v6 validation independently:

```text
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v6.0.0/pages --source-ref v6.0.0
```

Use existing inventory, phantom-skill, description-budget, public-content and bundle
checks. For a candidate bundle pass the actual committed revision through the
builder's `--source-revision` option; do not label a dirty tree as a released tag.
Comparisons freeze candidate, baseline, cases, model/configuration, provider
availability, discovery context, repetition budget and scoring before dispatch.
Failures and uncertainty remain visible; raw private telemetry stays outside the
public repository.

Workflow completion and UAT parity checks execute the shipped JavaScript templates
with synthetic role returns and require Node.js in addition to Python. They do
not launch agents or establish live acceptance.
