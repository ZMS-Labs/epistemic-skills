# Public release review addendum — 2026-07-21

Repository: `ZMS-Labs/epistemic-skills`

This addendum extends `PUBLIC-RELEASE-REVIEW-2026-07-17.md`, which scanned Git
history through baseline `d28a672`. Post-baseline commits accumulated new
tracked files that had not been through that review. This addendum covers
`d28a672..f0fcece` plus a full re-scan of the entire tracked tree at `f0fcece`.

## Scan scope

- Full `git grep` pattern sweep across every tracked file at `f0fcece`
  (not just the diff range), including `outputs/` and
  `plugins/epistemic-skills/skills/gauntlet/runs/` — directories a prior
  reviewer pattern-scanned but did not read file-by-file.
- Patterns swept: private-repo name (`zms-homelab`), local-checkout path
  forms (`Y:\dev`, `Y:/dev`, `C:\Users\zachs`, `C:/Users/zachs`), internal
  network ranges (`10.10.*`, `10.147.*`), internal domain suffix
  (`.internal.zms`), device hostnames (`zms-pc-2025`, `ZMS-PC-2025`),
  infrastructure vendor/product terms (`unas`/`UNAS`, `flashstor`,
  `jetson`, `ha-yellow`, `zimaboard`, `mele`), `H:\`, `secrets.env`,
  `Homelab`.
- A separate generic credential pass: `token`, `apikey`, `api_key`,
  `password`, `Bearer `, `ghp_`, `github_pat_`, `-----BEGIN`.
- Every hit was read in context and classified individually; no pattern
  match was auto-actioned without review.

## Findings and dispositions

Four files postdating `d28a672` contained fleet-internal topology with no
public value and were **relocated** (removed from public, preserved verbatim
in the private fleet repo — see companion PR there):

- `docs/superpowers/plans/2026-07-19-agentic-control-plane-phase-0.md` —
  step-by-step implementation plan for a private control-plane project
  (worktree names, `Y:\dev\zms-homelab*` paths, private-repo verification
  commands).
- `docs/superpowers/specs/2026-07-18-SESSION-HANDOFF.md` — session
  pause/resume notes with private worktree paths and no content describing
  the shipped plugin.
- `docs/superpowers/specs/2026-07-19-5f8a190-forward-classification.md` —
  internal audit of a specific commit's diff hunks, referencing private
  fleet paths and process.
- `outputs/gauntlet-runs/penecho-zms-integration-2026-07-18/` (17 files) —
  a real Gauntlet run evaluating a private infrastructure/product decision,
  referencing the private `ZMS-Labs/zms-k3s-gitops` repo and internal
  LiteLLM/secrets architecture. Confirmed as accidentally-committed fleet
  telemetry (the relocated `SESSION-HANDOFF.md` itself flagged the
  corresponding ledger line as "fleet telemetry" at capture time).

Two files with genuine public design value had private references
**scrubbed in place** (generic placeholders substituted; substantive content
retained):

- `docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md` —
  replaced two references to the private repo name/path with
  `<private-fleet-repo>` / `<local-checkout>` placeholders; updated the
  provenance pointer to the now-relocated session-handoff note.
- `docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md`
  — replaced four references to the private repo name/path/worktree with
  generic placeholders; updated the dangling link to the now-relocated
  session-handoff note.
- `.cursor/rules/evidence-zotero.mdc` — replaced two direct private-repo
  path references (org policy doc, CLI script path) with generic
  descriptions ("your organization's ... if one exists / if configured").

One file had specific entries **scrubbed** without removing the file itself,
since the mechanism is part of the shipped skill:

- `plugins/epistemic-skills/skills/gauntlet/runs/ledger.jsonl` — contained
  two real fleet Gauntlet run records (`penecho-zms-integration`,
  `fo-standards-interoperability`) added after baseline; both were fleet
  telemetry, not example data. Emptied back to its pre-baseline (absent)
  state.

## Intentional / not scrubbed

- `docs/superpowers/plans/2026-07-20-helix.md` references
  `Y:/dev/epistemic-skills` — this is the *public* repo's own local
  checkout path used in verification commands within its own implementation
  plan, not a private-infrastructure reference. Left as-is.
- The operator name/email in `PUBLIC-RELEASE-REVIEW-2026-07-17.md` remains
  intentional (GPL provenance record), per that document's own notes.

## Credential pass result

No real secret values were found. All `token`/`api_key`/`password`/`Bearer`
matches were generic environment-variable names (`OPENAI_API_KEY`,
`GITHUB_TOKEN`), LLM token-budget documentation, or code implementing
secret-redaction patterns (`plugins/epistemic-skills/skills/gauntlet/scripts/consult_packet.py`
detects `ghp_`, Slack tokens, PEM key blocks, and `password=`/`api_key=`
patterns as part of its own scrubbing logic — matched by the pass but not a
leak). No `-----BEGIN` private-key material was found.

## Verification

Re-running the full pattern sweep against the fix branch tree after
remediation returns zero matches for any private-topology pattern except the
one intentional self-reference noted above. A dangling-reference check for
the filenames of every removed document returned zero remaining links.

## History note

The removed/scrubbed content remains recoverable from public Git history
prior to the fix commit. See the companion PR description for the history-
exposure assessment and recommendation (no history rewrite performed as part
of this remediation; that action is operator-gated).
