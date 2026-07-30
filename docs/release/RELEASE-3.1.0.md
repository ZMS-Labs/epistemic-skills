# epistemic-skills 3.1.0

**Release record date:** 2026-07-29
**Intended channel:** stable
**Release type:** minor — one new skill, backward compatible
**Validity contract:** this record is authoritative only when the exact-commit
gates pass and the annotated tag plus non-draft GitHub Release satisfy the
publication-identity checks in RELEASING.md.

Version 3.1.0 adds the collection's tenth discipline and is otherwise
contract-compatible with 3.0.0. No existing skill's trigger, output contract,
or schema changes beyond the integrations listed below.

## What's new

- **`open-questions`** — an exhaustive serial clarification interview that
  gates work. Two modes over one append-allowed question ledger: **docket**
  (enumerate all known open decisions upfront for operator triage, then walk
  serially, highest-impact first) and **cascade** (laddering interview where
  answers beget appended follow-ups). Falsifiable termination: the ledger is
  empty AND a closing probe yields nothing new, or the operator releases the
  gate (remaining items parked on announced best-guess defaults). An
  un-best-guessable irreversible fork with the operator absent is **held and
  escalated**, never defaulted through. Exit emits the collection's canonical
  4-field stamp.
- Design provenance: grounded in the elicitation and saturation literature
  (structured interviews, laddering/probing, run-length stopping criteria,
  late-battery quality decay). See
  `docs/superpowers/specs/2026-07-29-open-questions-design.md`.

## Integration changes (compatible)

- `using-epistemic-skills`: ten-discipline counts; handoff-boundary, routing
  (explicit + narrow auto-trigger), and anti-pattern rows for open-questions;
  routine-fast-path must-not-manufacture entry.
- `helix`: pairing row (any gated stage outside active design dialogue) and
  co-fire bullet.
- Package integration test: expects twelve skill directories and
  `EXPECTED_VERSION = "3.1.0"`.
- Manifest descriptions across Claude/Codex/Cursor/Kimi/Gemini surfaces:
  twelve skills / ten disciplines.
- `runs/ledger.jsonl` restored to the shipped example line only (a real run
  record and a stray private path had been appended on the rolling channel;
  removed in PR #56 — the never-publish-runs policy holds).

## Migration from 3.0.0

No action required beyond updating the install coordinate to `v3.1.0` and
reloading the harness. The pinned `v3.0.0` tag remains valid and ships eleven
skills; expect twelve only on `v3.1.0` and later. Replace, don't stack: one
install mechanism per harness.

## Harness verification tiers (honest support boundary)

Unchanged from 3.0.0 except where noted:

- **Claude Code:** primary development harness; deterministic suite exercised
  on the release commit; open-questions authored and reviewed here. Live
  behavioral exercise of the new skill's interview loop occurred during its
  design session (docket-style AskUserQuestion walk).
- **Codex / Gemini / Kimi:** manifest surfaces updated and validated
  (JSON-parse + count/version parity); no live 3.1.0 behavioral run recorded
  for the new skill on these harnesses.
- **Cursor:** packaging present; still **not publicly listed** — no qualifying
  public-install result exists (unchanged disclosure from 3.0.0).

## Known limitations

- open-questions ships no `evals/` harness in 3.1.0; a behavioral fixture set
  is a candidate follow-up.
- The 3.0.0 behavioral-diagnostic exclusions and risk-acceptance records are
  unchanged and are not retroactively credited to 3.1.0.
