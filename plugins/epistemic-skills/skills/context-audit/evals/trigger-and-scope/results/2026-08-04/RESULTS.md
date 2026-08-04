# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: FAIL — 8/14 fixtures pass the deterministic scorer; 6 named
failures, all one class.** This record supersedes `results/BLOCKED.md`.

## Methodology

Same protocol as the open-questions 2026-08-04 epoch: one isolated
general-purpose subagent per fixture (claude-fable-5, Claude Code harness,
N=1), instructed to read exactly the skill's SKILL.md and nothing else
(evals/ forbidden), scenario restated with situational facts,
`expected_action`/`trigger` labels withheld (subject-level blinding),
responses returned as one JSON object under the README's pinned live-epoch
response contract, scored by the shipped `score.py` unmodified. Raw
responses in `responses.json` (verbatim, including the agents' full audit
reports), scorer output in `scorer-report.json`.

**Preregistration:** before scoring, the dispatching session recorded "8/14
pass; six failures, all `expected full-audit, got report-only-audit`
(prune-instructions, layer-conflict, model-upgrade, keep-gotcha, duplicate,
governance)" in the session transcript. The scorer confirmed exactly this
set.

## Results

Actions: full-audit 1 · report-only-audit 7 · no-fire 6.

- **PASS (8):** all six no-fire hard negatives (silent, zero audit-shape
  fields — no over-firing anywhere), `explicit-claudemd-audit` (full audit
  with version control, apply, correct class order), and
  `no-version-control-report-only`.
- **FAIL (6):** `explicit-prune-instructions`, `midtask-layer-conflict`,
  `model-upgrade-stale-guardrails`, `keep-gotcha-with-origin`,
  `duplicate-most-local-survives`, `governance-projection-conflict` — every
  one `expected full-audit, got report-only-audit`.

## Diagnosis — one systematic divergence, and it is a battery-design finding

The six failures share a single mechanism. The battery's action vocabulary
uses `full-audit` vs `report-only-audit` as a **trigger-mode pair** (the
audit fired on its full scope vs the degraded no-rollback mode). The
subject agents instead applied the **skill's own step-5 semantics**: apply
is forbidden without version control and operator gating, so an audit that
stops at the report is, in their honest words, report-only. Crucially, 12
of 14 fixtures do not state the estate's version-control status — so the
agents resolved it against their **real** environment (a harness-assembled
context with no rollback path) and answered truthfully for that estate.
The one fixture that stated version control (`explicit-claudemd-audit`)
got `full-audit` with a correct apply; the one fixture that stated its
absence got the expected `report-only-audit`. The scorer therefore
penalized honest real-environment resolution of a fact the fixtures left
open, six times.

Trigger discipline itself — the thing the battery is named for — was
clean: every expected fire fired, every hard negative stayed silent, and
within the fired audits the inner rulings matched doctrine (KEEP:GOTCHA
with the origin actually read; DUPLICATE with the most-local
load-on-demand survivor; governance conflict routed upstream, projection
untouched).

Upstream follow-ups for the battery (register: issue #77): (1) every
fixture states the estate's version-control status and whether operator
apply-approval exists; (2) either rename/redefine the action pair to match
the skill's mode semantics, or extend the pinned response contract to
state explicitly that `full-audit` means "the audit discipline fired on
its full scope," independent of whether apply happened. A second epoch
runs after those land; this record stands as-is.

## Qualitative observations (outside the scorer)

Two agents (`explicit-prune-instructions`, `model-upgrade-stale-guardrails`)
executed complete, genuine audits of their actual assembled harness
context, unprompted by any fixture requirement — layer inventories with
token estimates, verbatim conflict ledgers, cut nominations by class, keeps
with origin-read discipline. Their conflict ledgers contain real,
verifiable findings about this harness's instruction estate (a factual
contradiction between the agent-thread cwd claim and the Bash schema;
mutually incompatible end-of-response citation mandates from two literature
MCP servers; duplicated deferred-tool protocol statements). The discipline
demonstrably executes end-to-end on a real estate at first live contact.
Those findings belong to the harness's owners, not to this repo's scorer,
and are preserved verbatim in `responses.json`.

## Honest limits

N=1 per fixture, one model, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Subject-level blinding only.
The dispatch glosses are part of the intervention surface. Same model
family throughout.
