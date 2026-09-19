# v7 candidate evidence and requirement dispositions

Status: prepared source, not a release approval. Updated 2026-09-18.
Baseline design source: `9705f70aec1285597a6ef2a341cede80010c1dcb`.
Known implementation revisions: T1 `14cf3a1`, T2 `2011b68`, T3 `6a5901b`.
Later source work is not yet bound to the final candidate here. The assigned
reviewer must record its actual revision and final disposition before claiming
completion. No v7 tag, installed release or publication is asserted.

The [accepted requirements](../superpowers/specs/2026-09-18-epistemic-skills-v7-design.md)
control scope. This table is a disposition skeleton, not 22 passing assertions.

| Requirement | Source | Implementation coordinate | Disposition / check status | Evidence limit |
|---|---|---|---|---|
| R01 | [epistemic](../../plugins/epistemic-skills/skills/epistemic/SKILL.md) | 14cf3a1 (usage entry); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R02 | [metacognate](../../plugins/epistemic-skills/skills/metacognate/SKILL.md) | 2011b68 (method source); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R03 | [recon](../../plugins/epistemic-skills/skills/recon/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R04 | [resolve](../../plugins/epistemic-skills/skills/resolve/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R05 | [health](../../plugins/epistemic-skills/skills/health/SKILL.md) | 2011b68 (method source); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R06 | [triage](../../plugins/epistemic-skills/skills/triage/SKILL.md) | 2011b68 (method source); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R07 | [did-it-land](../../plugins/epistemic-skills/skills/did-it-land/SKILL.md) | 2011b68 (method source); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R08 | [watch](../../plugins/epistemic-skills/skills/watch/SKILL.md) | 2011b68 (method source); final integration pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R09 | [write-goal](../../plugins/epistemic-skills/skills/write-goal/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R10 | [manifest](../../plugins/epistemic-skills/skills/manifest/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R11 | [decision-ledger](../../plugins/epistemic-skills/skills/decision-ledger/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R12 | [outsource](../../plugins/epistemic-skills/skills/outsource/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R13 | [gauntlet](../../plugins/epistemic-skills/skills/gauntlet/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R14 | [perspective](../../plugins/epistemic-skills/skills/perspective/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R15 | [evidence-locked-uat](../../plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R16 | [open-questions](../../plugins/epistemic-skills/skills/open-questions/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R17 | [context-audit](../../plugins/epistemic-skills/skills/context-audit/SKILL.md) | Working-tree implementation; final revision pending | Source disposition prepared; relevant checks and final assigned review pending | Loaded/exercised/comparative credit not implied |
| R18 | [Shared lens library](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json) | 6a5901b; 102 historical IDs retained and three approved additions | Pending integrated validation and reviewer disposition | No release or benefit claim |
| R19 | [Host delivery](../../GEMINI.md) | Working-tree adapters; [T7 coverage](v7-host-coverage.md) recorded | Pending integrated validation and reviewer disposition | No release or benefit claim |
| R20 | [Review, authority and closure](../../RELEASING.md) | Current policy alignment pending root review | Pending integrated validation and reviewer disposition | No release or benefit claim |
| R21 | [Bounded evaluation](../superpowers/specs/2026-09-18-epistemic-skills-v7-design.md#r21-evidence-and-bounded-evaluation) | T9 campaign and comparative findings pending | Pending integrated validation and reviewer disposition | No release or benefit claim |
| R22 | [Public packaging and release presentation](RELEASE-7.0.0.md) | T8 candidate source; final committed revision pending | Pending integrated validation and reviewer disposition | No release or benefit claim |

## Check receipts

T8 checks on the candidate **working tree**, 2026-09-18; the committed base at
check time was `6a5901b38fe024d443574c5002f97892526c6c8e`. These results do not
certify that base as the final v7 source or replace exact-candidate checks.

| Check | Observed result | Limit |
|---|---|---|
| Surface sync self-test/check; inventory self-test/check | PASS, 17 canonical entries | Source consistency |
| Description budget; JSON artifact validation | PASS | Package-local / parse validity |
| Phantom-skill self-test/check; outsource integration | PASS | Navigation negative controls preserve retired-invocation rejection; canonical marketplace list now generated |
| Public-content self-test and scan | PASS | Known patterns; not universal privacy proof |
| OpenAI bundle builder and workflow test suites | PASS | Deterministic fixture/build contracts; no upload/install claim |
| Handbook checker self-test, v7 snapshot, v6 snapshot with `--source-ref v6.0.0`, historical applier self-test | PASS | 24 current pages and 47 historical pages; offline |
| New local documentation links | PASS, 112 links | Local path existence; no live Wiki publication |
| Gitleaks 8.30.1 full-history `--log-opts=--all` | PASS, 820 commits, no findings | History at check time; not later commits |
| Gitleaks public working-tree copy | PASS, 1722 Git-visible files, no findings | Ignored private task files and symlinks excluded |
| Existing release-security planted-secret, digest-field, neighboring-field and record-path controls | PASS | Local execution of workflow fixtures; not GitHub Actions execution |

Initial Windows output encoding prevented one test wrapper from finishing;
rerun used UTF-8. The phantom checker exposed local-heading navigation and
historical-alias wording false positives; the navigation fix includes a negative
control retaining rejection of actual retired-skill invocation. The digest-field
security control first used a fixture shape different from the workflow and
failed; the exact workflow fixture passed. These are retained diagnostics, not
candidate behavior passes. Final phantom and outsource integration reruns passed; exact-candidate
release credit still requires the reviewer's final receipt.

The actual committed-candidate bundle build remains pending root freeze: use
`python .github/scripts/build_openai_bundles.py --check --source-revision <actual-commit>`
after committing the intended candidate. No invented release tag is used.

## Host coverage

T7 [host coverage](v7-host-coverage.md) and the sanitized
[Codex 0.149.0 discovery receipt](v7-host-evidence/codex-0.149.0-skills.json)
record actual discovery of 17 matching descriptions. Startup/model consumption,
native goal readback and ordinary-prompt method use remain unexercised.
Claude Code/Codex hook source, Gemini usage context and
other package adapters do not alone establish live startup injection, native
alias activation or task completion. For each host record source, installed copy,
loaded context and exercised workflow separately, including unavailable surfaces.
No native goal/loop support is inferred from a host name or package manifest.

## Comparative findings

T9 evidence is pending. No comparative benefit claim is made. Preserve cases,
configuration, actual discovery, baseline/candidate revisions, outcomes, failures,
scorer corrections and costs. Historical campaigns retain their original limits.
Private transcripts, paths, network/account details and raw telemetry are excluded
from this public packet; publish only sanitized evidence sufficient to assess claims.

## Unresolved limits and release judgment

Final candidate revision, complete check receipts, host evidence, comparative
findings and the assigned reviewer's bounded release judgment remain pending.
Material unresolved failures must be fixed or the affected support claim withdrawn.
Publication authorization, tag creation, GitHub Release and live Wiki publication
are separate actions and have not occurred as part of candidate preparation.
