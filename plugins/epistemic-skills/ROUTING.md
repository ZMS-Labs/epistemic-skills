# ROUTING — generated from metadata.hands-to

<!-- GENERATED FILE. Do not hand-edit. Regenerate with:
     python .github/scripts/sync_skill_surfaces.py --write
     Hash-verified in CI via sync_skill_surfaces.py --check. -->

Each skill declares its consumers in portable frontmatter:

```yaml
metadata:
  hands-to: [consumer-a, consumer-b]
```

This file is the only aggregate routing surface. Hand-authored routing
tables are forbidden. Adding a skill costs this file nothing beyond the
regeneration that CI already requires.

| Skill | hands-to |
|---|---|
| `context-audit` | _(none)_ |
| `decision-ledger` | _(none)_ |
| `did-it-land` | `decision-ledger` |
| `evidence-locked-uat` | _(none)_ |
| `gauntlet` | _(none)_ |
| `health` | `triage`, `decision-ledger` |
| `metacognate` | _(none)_ |
| `open-questions` | _(none)_ |
| `outsource` | _(none)_ |
| `recon` | _(none)_ |
| `resolve` | _(none)_ |
| `triage` | `decision-ledger` |
| `watch` | `triage`, `decision-ledger` |
| `write-goal` | _(none)_ |
