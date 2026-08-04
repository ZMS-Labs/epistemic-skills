# context-audit trigger-and-scope fixtures

This battery tests the trigger discipline and the audit scope contract:
explicit invocation ("audit my context/CLAUDE.md/system prompt", "prune my
instructions"), a detected cross-layer instruction conflict, or a
model-generation upgrade each fire the full audit; single-document prose
editing, new-interface design, task-brief recon, and one-task prompt tuning
never fire — even when they are conflict-shaped or name a system prompt. A
firing audit inventories every loaded layer, runs the cross-layer merge, and
reports before applying; an estate without version control stops at the
report; a gotcha with an incident record is kept only after reading its
origin; a duplicate's most local copy survives; governance-projection
conflicts route upstream, never edited in place. Over-firing and under-firing
are defects, not extra rigor.

The battery is structural and trigger-level only: it scores declared
fire/no-fire decisions and audit-shape fields against fixtures, not whether a
live agent's actual audit was any good. Passing it is NOT behavioral proof.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- `action` names the **audit mode that fired**: `full-audit`,
  `report-only-audit` (an audit whose estate has no rollback path — it stops
  at the report), or `no-fire`.
- A `no-fire` response is **silent**: it carries no audit-shape fields at all
  (`layers_inventoried`, `cross_layer_merge`, `report_emitted`, `cut_list`,
  `applied` all absent).
- Any audit that runs reports `layers_inventoried`, `cross_layer_merge`, and
  `report_emitted` as booleans describing what actually happened; the report
  always precedes any apply.
- `applied` means cuts were actually applied — only true on a
  version-controlled estate (`version_control: true`) with the operator gate
  passed; `apply_order` lists the cut classes in the order applied
  (vocabulary: CONFLICT, DUPLICATE, OVER-VERIFY, OBVIOUS,
  MODEL-HANDLES-THIS-NOW).
- `classification` uses the cut/keep vocabulary (`KEEP:GOTCHA` etc.);
  `origin_read` is true only when the cited origin record was actually
  opened this audit, not remembered. `survivor` names the location whose
  copy of a duplicate survives. `routed_upstream`/`projection_edited`
  describe governance-projection handling.

First live behavioral epoch: 2026-08-04, FAIL 8/14 — see
`results/2026-08-04/RESULTS.md`. Trigger discipline scored clean (all six
hard negatives silent, every expected fire fired); all six failures are one
diagnosed battery-design divergence (register: issue #77).
