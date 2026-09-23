# Documentation

Start with the [project overview](../README.md) for the purpose and a first
example, or the [current handbook](handbook/pages/Home.md) for practical use.
The [published wiki](https://github.com/ZMS-Labs/epistemic-skills/wiki) presents
the handbook as connected pages. The editable source is `docs/handbook/pages/`.

## Choose your next step

| You want to… | Start here |
| --- | --- |
| Use the methods on a real task | [Current handbook](handbook/pages/Home.md) |
| Understand exactly what an agent is instructed to do | [Canonical skill tree](../plugins/epistemic-skills/skills) |
| Make your first contribution | [Contributor guide](../CONTRIBUTING.md) |
| Change a skill, adapter, contract, or documentation page | [Maintainer change map](MAINTAINING.md#change-map) |
| Understand what validation can establish | [CI coverage](actions-tier.md) and [local checks](CI-LOCAL-FALLBACK.md) |
| Inspect schemas and executable checks | [Contract guide](../plugins/epistemic-skills/contracts/README.md) |
| Build the ChatGPT and OpenAI distributions | [Packaging guide](CHATGPT-AND-OPENAI-PACKAGING.md) |
| Publish a version | [Release procedure](../RELEASING.md) |
| Verify the released v7.1 source and outcomes | [Release notes](release/RELEASE-7.1.0.md) and [completed publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/publication-receipt.json) |

## Current guidance and release records

The current handbook can improve between releases. The
[v7.1.0 handbook snapshot](wiki-updates/v7.1.0/pages/Home.md) records the pages
published for that release; the [v7.0.0 snapshot](wiki-updates/v7.0.0/pages/Home.md)
and the [v6.0.0 snapshot](wiki-updates/v6.0.0/pages/Home.md)
serve the same historical purpose. Edit current guidance in the handbook,
not in a released snapshot.

Release records answer a different question: what was checked on a particular
candidate, and what eventually shipped? The [v7 requirement packet](release/v7-evidence.md)
retains its pre-publication verdict. Use the completed publication receipt above
for the final tagged commit and hosted outcomes. New evidence supplements that
history instead of changing what an earlier run reported.

## Historical material

Dated plans, audits, review runs, experiments, and evaluation receipts record
what was proposed or observed at the revision they name. A draft or open item
in a historical record is not a statement of current project status. Use the
current source, release notes, and issue tracker for that purpose.

Public copies of some records replace personal identifiers, local paths, and
network coordinates with synthetic values. The
[redaction index](public-content-redactions.json) records the source revision,
original file hashes, and the hashes of those public copies. Findings, review
outcomes, and original digest references were retained. Redacted copies are not
byte-identical original receipts; original digest claims apply to the named
historical revision. Existing Git history and release tags were not rewritten.

Live session output, private configuration, and working checkouts belong in
ignored local directories. The public-content check scans current publishable
text without whole-file exemptions. It complements credential scanning and
human review; it cannot prove that arbitrary text contains no private facts.
