# epistemic-skills 3.3.0

**Release record date:** 2026-07-30
**Intended channel:** stable
**Release type:** minor — two new disciplines, four targeted amendments, router/helix
ripple, backward compatible
**Validity contract:** this record is authoritative only when the exact-commit
gates pass and the annotated tag plus non-draft GitHub Release satisfy the
publication-identity checks in RELEASING.md.

## What's new

- **`context-audit` (new discipline):** audits the *assembled* instruction
  context — every layer the harness loads, as one set — and classifies each
  instruction (CONFLICT / DUPLICATE / OBVIOUS / MODEL-HANDLES-THIS-NOW /
  OVER-VERIFY vs. five KEEP classes). Output: cut list as diff + conflict
  ledger + re-baseline watch note; apply is operator-gated, class-by-class,
  one version-controlled commit per class. Maintenance-triggered (explicit
  request, detected cross-layer conflict, model-generation upgrade) — never a
  per-task stage. Extraction (progressive disclosure) is a sub-mode.
- **`agent-interface-design` (new discipline):** when work crosses to another
  agent as a machine contract (tool/function schema, MCP surface,
  structured-output or dispatch contract), constraints are encoded in
  interface *structure* — types, enums, named fields, defaults, structured
  diagnostics — not prose or usage examples. Falsifiable gate: the
  cold-consumer test. Examples survive only as labeled compatibility
  concessions for weaker consumers. Doctrine is evidence-graded, including
  its own boundary conditions (schema buys contract adherence, not semantic
  quality; example-avoidance is capability-dependent).
- **Amendments (four):** `write-goal` — prefer executable references (failing
  test, rubric, schema, exemplar) over prose proof criteria; `outsource` —
  ship rich references in the packet, not descriptions of them;
  `gauntlet-generator` — instantiate options as disposable prototypes when
  build-cost < debate-cost (a built option is evidence); `evidence-locked-uat`
  — acceptor comprehension gate (anti-rubber-stamp): acceptance without the
  acceptor's own-words restatement is recorded `ACCEPTED-UNREVIEWED`, never
  silently upgraded.
- **Router + helix ripple:** both new disciplines added to the handoff table,
  routing table, arc notes, and pairing map; collection counts updated
  (fourteen skills: router + helix + twelve disciplines).

## Provenance and evidence posture

Technique provenance: Thariq Shihipar (Anthropic), "The new rules of context
engineering for Claude 5 generation models" (2026-07-24), independently
re-derived and evidence-graded. Scholarly anchors were reception-checked
(Scite, authenticated; no retractions, no contrasting citations on anchors)
on 2026-07-30; the vendor-reported 80%-cut magnitude is cited as direction
only, marked unreplicated, inside `context-audit` itself.

**Honest limits:** the two new skills ship with NO eval battery or behavioral
epoch of their own. The 3.2.0 evaluation posture (deterministic checks,
proportionality campaign, known P0 failures, AGY availability gaps) is
inherited, not extended. First-use field evidence should be captured before
any behavioral claim is made for either new discipline.

## Migration from 3.2.0

No action beyond updating the install coordinate to `v3.3.0` and reloading the
harness. No existing trigger, contract, schema, or output shape changed;
amendments are additive clauses inside existing sections. Wiki pages for the
two new skills may lag the tag — the catalog links them to in-repo SKILL.md
paths, which are the authoritative contracts.

## Harness verification tiers

Unchanged from 3.2.0: Claude Code primary; Codex/Gemini/Kimi
manifest-validated (all ten version manifests bumped and JSON-validated);
Cursor packaged but not publicly listed.
