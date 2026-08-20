# Redactions applied when this record was committed into the tree

This run's verdict was originally recorded on the mutable branch
`claude/epistemic-skills-v6-completion-nwptmc`. Bringing it into the tree
(publication-gate finding PG-03) required three redactions, disclosed here so
the record stays verifiable.

## What was changed

Three occurrences of the private fleet repository's literal name were replaced
with the placeholder `<private-fleet-repo>`:

| File | Occurrences |
|---|---|
| `arbitration.md` | 1 (ruling justification, quoting PR #192's detected violation) |
| `evidence/dossier-challenge-2026-08-18.json` | 2 (challenge text and its `evidence_checked` field) |

Nothing else was altered: no verdict, severity, ruling, or finding text changed,
and the dossier JSON parses identically apart from those three string values.

## Why

The name is one of the seven patterns `check_public_content.py` fails closed on.
The irony is the point and worth stating plainly: this panel's finding was *about*
that string being allowlisted rather than remediated, and stating the finding
reproduced the string. Quoting a detector's trigger re-arms it. The placeholder
matches the convention already used in this repository's README estate block.

## Verifying the unredacted original

The original bytes remain immutable at the branch this was taken from. Compare:

```bash
git diff origin/claude/epistemic-skills-v6-completion-nwptmc -- \
  docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/
```

Every difference that command reports should be one of the three above, plus
this file.
