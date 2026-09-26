# Epistemic Skills 7.2.0

V7.2 expands `resolve → literature` with a research-gap coverage-map contract.
For questions about gaps or under-studied areas, the method now pre-registers a
coverage frame, records the papers and passages behind each cell, treats sparse
cells as `POTENTIAL GAP` rather than proof of absence, and requires a validation
search before handing a cell forward as a focused research question. This is a
backward-compatible expansion of one method, so the release is minor. The package
still contains seventeen skills: `epistemic` and sixteen substantive methods.

## What changed

- The literature method adds the coverage frame, cell record, validation gate,
  and focused-question handoff. A connector-native matrix is treated as tool
  data and must pass the same validation.
- `reference/research-gap-matrix.md` gives the cell fields and a worked record.
  Counts, paper IDs, classification rationale, exact passages, source locations,
  validation query results, and residual coverage limits remain inspectable.
- Four declared fixtures describe structural requirements. They have no scorer
  or live agent epoch; they are **not** evidence of agent behavior. The existing
  `resolve/literature` trigger-and-scope tests cover the prior trigger contract,
  not the quality of a produced coverage map.
- The package manifests, install instructions, and package integration version
  expectation move from 7.1.0 to 7.2.0. The skill inventory and description text
  are unchanged.

## Migration and compatibility

Replace an older install with one tagged `v7.2.0` copy, reload the host, and
verify its loaded source path. Existing literature records remain valid; the
coverage map applies when a new question carries a gap, landscape, under-studied,
or “what is missing” premise. A sparse cell remains an orientation signal until
validation is recorded. No new connector or host integration is promised.

## Evidence and limits

The content change merged as PR #262 (`de0531d`). The release candidate is the
merge commit of the version-rotation release PR. Exact-candidate check runs,
the designated review, annotated tag identity, and generated bundle hashes are
recorded in the tag message and attached release receipts. This committed note
does not claim that a later publication step has already passed.

| Gate | Status record | Exact subject / evidence | Limits |
|---|---|---|---|
| Version, links and package | Final result in publication receipt | Annotated v7.2.0 target; manifest and package checks; post-tag URL checks | A manifest does not prove an installation loaded |
| Deterministic checks and CodeQL | Final result in `exact-gates.json` | Required hosted jobs on the exact merge commit | A green source check does not show an agent using the method |
| Security, public content and provenance | Final result in `exact-gates.json` | Exact candidate and reachable history; planted scan controls and public-content review | Pattern checks cannot prove universal absence |
| Description bytes | 7,231, unchanged from v7.1.0 | `check_description_budget.py --report` on both versions | Package-local, not total host context capacity |
| Harness evidence | Tiers below; no new 7.2 live-behavior claim | Prior v7 host coverage and generated-bundle checks | Discovery, packaging and actual method use are different observations |
| Designated-reviewer judgment | Final verdict in `designated-review.json` | Frozen release candidate and reviewer record | Reviewer identity and shared context are disclosed there |
| Publication identity | Final result in `publication-receipt.json` | Tag object, Release, assets and Wiki | Verify actual published objects, not this prose alone |

### Harness verification tiers

| Harness | 7.2.0 verification tier and limit |
|---|---|
| Claude Code | Package structure and source checks; no 7.2 live model run |
| Codex CLI | Prior v7.0 discovery of all seventeen skills; 7.2 loaded-source and method use unverified |
| Codex desktop app | Current session loads a cached 7.0 skill copy; 7.2 installation and behavior unverified |
| Cursor | Package and installation instructions only; 7.2 model delivery unverified |
| Gemini CLI | Extension manifest and instructions only; 7.2 model delivery unverified |
| Antigravity | Plugin manifest and instructions only; 7.2 model delivery unverified |
| Kimi Code | Plugin manifest and instructions only; 7.2 model delivery unverified |
| ZCode | Tagged checkout procedure only; 7.2 discovery and behavior unverified |
| ChatGPT / OpenAI | Generated bundle validation on the release candidate; no live agent execution |
| Generic Agent Skills host | Canonical tagged skill tree and fallback instructions; host behavior unverified |

The coverage-map method follows the [Consensus Research Gaps Matrix
description](https://consensus.app/home/blog/introducing-new-research-gaps-matrix/),
including its warning that an empty cell concerns the retrieved papers, not all
research. This release adds a written validation contract, not a proven
improvement in research outcomes. The v7 comparative-superiority null and
unusable-pair results still stand; no 7.2 comparative trial has run.

The [macOS custody limitation (issue #162)](https://github.com/ZMS-Labs/epistemic-skills/issues/162)
also carries forward: do not rely on distinct-filename or exclusion guarantees
on case-insensitive POSIX filesystems. The dispatch-only macOS diagnostic is
disclosed separately from required Ubuntu custody results in the exact gate
receipt.
