# epistemic-skills 3.2.0

**Release record date:** 2026-07-30
**Intended channel:** stable
**Release type:** minor — one contract change, one new eval battery, backward compatible
**Validity contract:** this record is authoritative only when the exact-commit
gates pass and the annotated tag plus non-draft GitHub Release satisfy the
publication-identity checks in RELEASING.md.

## What's new

- **open-questions auto-fire is now fork-scoped** (operator-decided resolution
  of the v3.1.0 publication review's preserved dissent): the narrow
  auto-trigger walks only the triggering fork and the questions its answers
  directly open; exactly one closing offer covers other surfaced material
  questions; a declined **or unanswered** offer defers them — each recorded in
  the exit stamp's coverage limits AND captured in the environment's durable
  tracker with its best-guess default, never memory-only. The full
  walk-everything-to-empty contract is explicit-invocation-only. The router's
  auto-trigger row states the scoped contract.
- **First eval battery for open-questions**: `evals/trigger-and-scope/` in the
  house shape — 10 fixtures (explicit/full, no-fire, park, hold-escalate,
  fork-scoped, offer accepted/declined/unanswered, operator-release), stdlib
  deterministic scorer, balanced example plus three parody polarity controls
  (overfiring, scope-creep, lost-deferral), wired into CI and asserted by the
  package integration test. `results/BLOCKED.md` records that no live
  behavioral epoch has run.

## Migration from 3.1.0

No action beyond updating the install coordinate to `v3.2.0` and reloading the
harness. Explicit-invocation behavior is unchanged; only auto-fire scope is
newly specified (it was previously ambiguous, flagged at P3 in the v3.1.0
publication review).

## Harness verification tiers

Unchanged from 3.1.0: Claude Code primary (deterministic suite on the release
commit); Codex/Gemini/Kimi manifest-validated; Cursor packaged but not
publicly listed. The trigger-and-scope battery is deterministic-only — no
live behavioral epoch on any harness yet.

## Known limitations

- Behavioral epoch for trigger-and-scope remains BLOCKED (fixtures + scorer +
  polarity controls only).
- The 3.0.0 behavioral-diagnostic exclusions and risk-acceptance records are
  unchanged and not retroactively credited.
