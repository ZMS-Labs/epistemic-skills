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

No live behavioral epoch has been run against this battery; see
`results/BLOCKED.md`.
