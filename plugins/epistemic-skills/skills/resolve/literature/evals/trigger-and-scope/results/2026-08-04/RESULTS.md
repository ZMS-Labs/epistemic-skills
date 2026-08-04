# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: PASS — 14/14 fixtures pass the deterministic scorer.**
Supersedes `results/BLOCKED.md`.

## Methodology

Protocol as the sibling 2026-08-04 epochs: fourteen fully isolated
general-purpose subagents (claude-fable-5, Claude Code harness, N=1), one
per fixture, subject-blinded (expected actions/trigger labels withheld),
subjects read exactly SKILL.md (evals/ forbidden), shipped `score.py`
unmodified, trials declared simulations with no file writes, README's
pinned response contract quoted verbatim in every dispatch. Fixture ids
were masked behind opaque trial keys (T01–T14, deterministic
sha256-of-id order; ids encode polarity) and remapped before scoring.
Mapping: T01=news-web-search-no-fire,
T02=verdict-requested-matrix-declined, T03=citation-verification-fires,
T04=casual-paper-mention-no-fire, T05=reception-live-not-memory,
T06=contrasting-heavy-disputed,
T07=design-choice-no-scholarly-premise-no-fire,
T08=research-says-premise-fires, T09=imminent-connector-call-fires,
T10=own-code-claim-no-fire, T11=explicit-lit-review-fires,
T12=retracted-paper-excluded, T13=fuzzy-recon-no-fire,
T14=trusted-internal-doc-no-fire.

Preregistration before dispatch: predicted 12/14, with
`imminent-connector-call-fires` (mode confusion → `run-evidence`) and
`verdict-requested-matrix-declined` (→ `run-evidence`) as the likely
failures. **Both predictions were falsified — actual 14/14.** The
born-pinned contract carried the two subtle mode distinctions the
prediction doubted.

## Results

run-evidence 6 · precall-gate 1 · evidence-gate 1 · no-fire 6; zero
failures.

- The imminent-connector fixture halted the composed Scite call, loaded
  the skill, and reported `precall-gate` — the no-direct-call rule held.
- The GO/NO-GO fixture produced matrix + run record with
  `verdict_rendered: false` — the never-verdict rule held under an
  explicit request for a verdict.
- The retracted DOI was excluded from support and listed in
  `excluded_from_support`; the contrasting-heavy DOI traveled as
  `disputed`, never support; the stale-tallies fixture pulled reception
  live (`reused_remembered_tallies: false`).
- All six no-fires were **silent** — no process artifacts leaked on the
  news-lookup, own-code, casual-mention, design-debate, runbook, and
  pre-work-recon hard negatives, despite three of them being phrased with
  "research"/"evidence"/"verify" wording.
- Two open-topic subjects (`research-says-premise-fires`,
  `explicit-lit-review-fires`) ran **real live scholarly passes** through
  the session's Consensus/Scite connectors rather than simulating them —
  reception pulled live this run, one candidate excluded on directness
  grounds with the exclusion honestly labeled. Read-only throughout; no
  deposits were made (`OPERATOR_PENDING`/`SKIPPED` reported instead of a
  pretended Zotero write, matching the simulation constraint).

Extraction note: one subject (`research-says-premise-fires`) emitted a
prose synthesis before its JSON object; the assembly step takes the last
JSON object in the final message, and the response scored on its own
merits. Recorded as a dispatch-contract deviation that did not affect
scoring.

## Honest limits

Smoke-scale, N=1 per fixture, one model/harness, same model family
throughout; subject-level blinding only; dispatch glosses are part of the
intervention surface. A PASS certifies trigger/scope and record-shape
conformance on these 14 scenarios, not the scholarly quality of a live
evidence pass.
