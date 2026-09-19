# V7 candidate evidence and requirement dispositions

Evidence date: 2026-09-18. **Pre-publication evidence snapshot.**

This packet preserves the local state before release PR #250. Its conditional
publication disposition and unrun-hosted statements describe that stage. Final
exact-candidate checks, reviewer verdict and publication identity are recorded
in the annotated v7.0.0 tag and its attached publication receipt; they do not
retroactively change the observations below.

The integrated source is `42c467fbbf6d082910875e361f0d2fd2d2e530dd`.
The comparison froze the earlier `7b746681123b4fa6d5d85a0d26e58f38826faeb1`
against v6.0.0 (`b4bc8dff0d07a7535c24905af7fb97cc85e01037`). The later
integration commit clarifies Manifest enforcement, adds the existing UAT
regressions to CI, corrects historical-policy ambiguity, and preserves the failed
pilot setup. It is not silently substituted as the subject of that pilot.

The owner designated the implementing Codex agent as reviewer. This review shares
implementation context and is not independent or blinded. The
[accepted design](../superpowers/specs/2026-09-18-epistemic-skills-v7-design.md)
controls the following dispositions. Source instructions, executable contracts,
live host observations and comparative benefit are different evidence levels.

## Requirement dispositions

| Requirement | Implementation | Reviewed disposition and evidence | Limit |
|---|---|---|---|
| R01: usage entry | `251b09b`; [epistemic](../../plugins/epistemic-skills/skills/epistemic/SKILL.md) | Canonical usage guidance, direct access, visible acknowledgment and continuation; discovery/inventory contracts pass | Automatic application in ordinary tasks unproved |
| R02: metacognate | `251b09b`; [method](../../plugins/epistemic-skills/skills/metacognate/SKILL.md) | Substantive examination of reasoning retained; exclusive-entry and compulsory-dispatch framing removed | Source/conformance evidence, not measured reasoning improvement |
| R03: recon | `b71fc86`; [method](../../plugins/epistemic-skills/skills/recon/SKILL.md) | Existing modes retained; question quotas removed; scoped framing returns to task owner; scope fixtures pass | Synthetic response controls |
| R04: resolve | `b71fc86`; [method](../../plugins/epistemic-skills/skills/resolve/SKILL.md) | Bounded citation verification, evidence-cost selection and persistence/deposit boundaries; literature/probe controls pass | No live scholarly-connector or comparative claim |
| R05: health | `3549e36`; [method](../../plugins/epistemic-skills/skills/health/SKILL.md) | Observed bounds, coverage and unknowns separated from diagnosis and landing; operational controls pass | Synthetic response controls |
| R06: triage | `3549e36`; [method](../../plugins/epistemic-skills/skills/triage/SKILL.md) | Prefer applicable available systematic-debugging; one investigation, standalone fallback, authorized repair and original-failure verification | Actual preferred-provider handoff not established by the invalid pilot |
| R07: did-it-land | `3549e36`; [method](../../plugins/epistemic-skills/skills/did-it-land/SKILL.md) | Consumer evidence required; observed reversal separated from future overwrite risk | Synthetic response controls |
| R08: watch | `3549e36`; [method](../../plugins/epistemic-skills/skills/watch/SKILL.md) | SUSPECT proof history is absent or complete; blank/null reproof fields rejected; 31 watch checks pass | No external observer commissioned by this work |
| R09: write-goal | `559b143`; [method](../../plugins/epistemic-skills/skills/write-goal/SKILL.md) | Actual native surface/limit/lifecycle discovery, draft-only intent, opt-in budgets and ambiguous-response readback; adapter controls pass | Native goals deliberately not activated; profiles are synthetic |
| R10: manifest | `559b143`, `42c467f`; [method](../../plugins/epistemic-skills/skills/manifest/SKILL.md) | Reuse authority/frontier records; accurately name union gate, installed-hook prerequisite and individual degradation | Custody integrity is not outcome acceptance; platform test limits below |
| R11: decision-ledger | `559b143`; [method](../../plugins/epistemic-skills/skills/decision-ledger/SKILL.md) | Reuse adequate ADRs; preserve original predictions, resume checks and later outcomes; continuity controls pass | Historical resume trials retain their original dates/results |
| R12: outsource | `559b143`; [method](../../plugins/epistemic-skills/skills/outsource/SKILL.md) | Verified COMPLETE closes the relay without another prompt; caller integration continues; completion/integration controls pass | No real external relay executed |
| R13: gauntlet | `d2cf0ac`; [method](../../plugins/epistemic-skills/skills/gauntlet/SKILL.md) | Plural scrutiny, distinct mechanisms, constructive revision, dissent and scoped rechecks; actual JS template refuses unsupported GO | Template controls are mocked role outputs, not a live panel |
| R14: perspective | `d2cf0ac`; [method](../../plugins/epistemic-skills/skills/perspective/SKILL.md) | Focused/adaptive library use; multiple lenses do not force Gauntlet; return boundary and metadata checked | Natural activation unproved |
| R15: evidence-locked-uat | `d2cf0ac`, `42c467f`; [method](../../plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md) | Versioned expected/disconfirming observations; compiler/Python/JS parity; failed persistence prevents acceptance; 10 regressions now invoked in CI | Direct synthetic checks; no fabricated blinding |
| R16: open-questions | `b71fc86`; [method](../../plugins/epistemic-skills/skills/open-questions/SKILL.md) | Recover prior answers, investigate factual unknowns, preserve requested scoped interviews and release semantics | Synthetic scope controls |
| R17: context-audit | `b71fc86`; [method](../../plugins/epistemic-skills/skills/context-audit/SKILL.md) | Actual load/precedence/version evidence; scoped expansion; no removal of rare protections based on silence | Source presence does not establish runtime loading |
| R18: shared lenses | `d155234`; [accounting](../audits/2026-09-18-v7-lens-implementation.json) | All 102 original IDs accounted for; 96 available entries revised, six retired retained, three approved additions; schema, rendering and 1,000 selector constraints pass | 99 available entries are not 99 empirically validated effects; historical registry drift preserved |
| R19: host delivery | `bf547e2`; [coverage](v7-host-coverage.md) | One canonical usage body, bounded lifecycle loader and visible fallback; six loader tests; live Codex discovery of all 17 descriptions | Startup consumption, native aliases and native-goal readback unexercised; runtime isolation failed in pilot |
| R20: review/closure | `c133e57`, `42c467f`; [policy](../../RELEASING.md) | Designated reviewer governs v7; historical independence rules clearly scoped to v6; no new mandatory family or panel | Publication authority and integrity checks still apply |
| R21: bounded evaluation | `7b74668`, `42c467f`; [all outcomes](../../plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-09-18-v7/RESULTS.md) | Fixed cases/rubric/schedule preserved; one invalid baseline run retained and 31 slots undispatched; comparative claim withdrawn | Zero valid pairs and zero candidate subjects; no superiority inference |
| R22: public package | `c133e57`, `42c467f`; [candidate notes](RELEASE-7.0.0.md) | 17 canonical entries, consistent manifests, current handbook, historical snapshot validation and exact-source bundle build | Unreleased; v6 remains the published installation fallback |

## Local checks

The [sanitized command receipt](v7-local-checks.json) retains 86 executions
covering 81 unique workflow commands. The original pass had 77 expected outcomes,
one enforcement-wording failure and two 180-second timeouts. Three commands
crossing a local sign-off operation were repeated against stable source, and one
omitted compile-only command was added; all four passed. Each slow custody suite
received one 600-second bound: lifecycle passed in 366.14 seconds and CLI in
260.55 seconds, both with zero failures. The corrected enforcement audit passed
separately. All 81 checks therefore have an expected-outcome receipt, including
historical fixtures whose correct outcome is a nonzero exit.

Original failures, timeouts and source snapshots remain recorded. The receipt
separates corrective checks from original executions and maps earlier unpublished
commits to signed commits with identical trees. The custody subtree did not
change during its longer runs. This is Windows/Python 3.11 evidence; Linux/macOS,
Python 3.12 dependency parity and the POSIX clean-room workflow remain unexercised.
A loaded-description command returning LIVE_BLOCKED is not counted as delivery.

The three final review findings were resolved: name the actual Manifest control,
run the existing UAT parity regressions in CI, and clearly separate historical
v6 independence policy from the current designated-reviewer policy. No additional
mandatory review panel was introduced.

Already observed on the integrated candidate: both deterministic OpenAI archives
build with 17 discovered skills using `build_openai_bundles.py --check
--source-revision 42c467fbbf6d082910875e361f0d2fd2d2e530dd`. No archive was
uploaded. The enforcement-language audit passes after the concrete gate reference;
all 10 UAT observation tests and the workflow oracle/self-tests pass. The new CI
step requires Node explicitly instead of silently skipping JavaScript coverage.

The current 24-page handbook and historical 47-page v6 handbook were checked
against their appropriate source versions. Source/discovery alignment, JSON,
phantom-reference controls, package/bundle fixtures and scoped regressions have
passed. The live Wiki was not modified.

## Privacy, integrity and provenance

- Public-content self-test: nine seeded controls pass. The current public tree
  passes the same known-pattern scan; raw private task logs are excluded from
  publication, not treated as public-safe artifacts.
- Gitleaks 8.30.1 redacted full-history scan at `42c467f`: 836 commits scanned,
  no findings. The existing planted-secret and three allowlist-narrowness controls
  passed during T8; scanner configuration did not change afterward.
- Actual DCO validation: all 11 commits after the upstream base have matching
  author sign-offs; seven DCO policy tests pass.
- All four protected dependency tags were read from origin and match their
  registered commits. Origin/main was also read live as `9705f70`; the ledger
  append-only check against that exact base passes with zero appended lines.
- Historical release tags, public attribution, original review outcomes and the
  six retired lens records retain their meaning. No published history was rewritten.

These checks support their specific patterns and contracts, not universal proof
that sensitive content or every possible defect is absent. Later evidence-only
commits require their own publication checks; they do not become the unchanged
subject of an earlier scan by being described in this file.

## Host and comparison limits

[Host coverage](v7-host-coverage.md) records live Codex discovery separately from
source/serialization checks. The actual capture includes 17 canonical entries
and six nested methods. No candidate startup-model consumption or native-goal
readback was obtained. Each other host retains its explicit, limited tier.

The authorized pilot requested gpt-5.6-sol/medium through Codex CLI 0.149.0. Native
debug catalogues showed 15 isolated baseline entries and 17 candidate entries.
Actual inference nevertheless loaded three unrelated host skill resources and
rejected basic local commands as blocked by policy. The baseline subject exited
zero after 55.797 seconds with its task unfinished and artifacts unchanged.
Execution therefore failed the comparison preconditions. All six rubric scores
remain unknown; neither a baseline defect nor candidate benefit is inferred.

The [sanitized run evidence](../../plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-09-18-v7/T01-evidence.json)
and full 32-slot manifest preserve observations, failure and unrun status. Raw
transcripts remain private. Serving model confirmation and cost were unavailable.
The campaign stopped without credential copying, permission-policy bypass, real
goal activation, installation changes or favorable-run retries.

## Assigned-reviewer disposition

**Publication judgment: CONDITIONAL.** The designated review found no remaining
material source finding within R01-R22 after the three integration corrections.
Local implementation and verification are complete at the recorded scope.
Publication is held by outstanding hosted integrity checks and publication
identity/authorization steps, not by a demand for another reviewer or model
family. No independent review is owed under current v7 policy.

Comparative benefit, all-host automatic activation and unexercised native-goal
behavior remain withdrawn claims. The failed pilot is a disclosed evidence limit,
not a required endless rerun campaign. This judgment covers the named source and
recorded support tiers; it does not approve stronger claims.

Required hosted integrity checks, including CodeQL and exact-candidate CI, have
not run for this unpublished branch. A local check is not a GitHub check. No PR,
push, merge, v7 tag, GitHub Release, installed v7 upgrade or Wiki publication was
performed. Those states must remain distinct from local source preparation.
