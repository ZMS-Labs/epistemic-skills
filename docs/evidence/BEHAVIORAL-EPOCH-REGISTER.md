# Behavioral epoch register (issue #77)

Successor to closed #70. Every skill must have either (a) a dated live epoch under
its eval battery, or (b) a current `results/BLOCKED.md` reviewed at a release gate.

## A. CI-wired trigger-and-scope batteries (BLOCKED.md today)

| Skill | Battery path | Live epoch | Notes |
|---|---|---|---|
| open-questions | `evals/open-questions/` | — | also #61 |
| context-audit | `evals/context-audit/` | — | |
| agent-interface-design | `evals/agent-interface-design/` | — | retired skill; battery may archive |
| wayfinding | `evals/wayfinding/` | — | |
| throwaway-prototyping | `evals/throwaway-prototyping/` | — | |
| intent-traced-merge | `evals/intent-traced-merge/` | — | |

## B. Core skills without house-shape batteries

| Skill | Status |
|---|---|
| blindspot-pass | no eval surface |
| evidence-research / resolve literature | method + connectors; no scored epoch |
| write-goal | no eval surface |
| outsource | no eval surface |

## C. Linked campaigns

- **#39** — valid four-arm superiority run (epistemic-flexibility Phase 4)
- Amended arbitrator-certification battery — `NOT_RUN` per skill honest limits

## How to close #77

Commit `results/<YYYY-MM-DD>/` (or updated BLOCKED.md) per row, then update this
table with the evidence path. Release notes cite this register, not #70.
