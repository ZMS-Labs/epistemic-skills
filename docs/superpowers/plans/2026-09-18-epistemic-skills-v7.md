# Epistemic Skills v7 Implementation Plan

> For agentic workers: use superpowers:executing-plans to execute these scoped tasks. The current agent is the owner-designated reviewer. No mandatory independent model-family review, fresh reviewer per task or repeated design approval is introduced. Preserve existing authorization and user corrections.

**Goal:** Deliver the accepted v7 skill refinements, usage entry and shared lens methods with truthful activation, continuation and public evidence.

**Architecture:** One portable canonical skill tree, one usage entry, sixteen substantive methods and one shared lens repertoire. Thin verified host integrations supply instructions and adapt native goals; the task-owning agent retains execution responsibility.

**Tech stack:** Markdown Agent Skills, existing JSON/YAML contracts and Python standard-library validators, current package/build surfaces and available host integrations. No new background service or required external skill package.

**Spec:** [Consolidated v7 design](../specs/2026-09-18-epistemic-skills-v7-design.md). Read it with the [per-skill assessment](../../audits/2026-09-18-v7-skill-assessment.md) and [member inventory](../../audits/2026-09-18-v7-lens-members.json).

**Execution state:** IN PROGRESS on `codex/v7-implementation`. This plan consolidates accepted requirements. File layout and pilot sizing below are conservative engineering defaults, not tested benefits. Checkboxes record implementation work, not design acceptance.

## Global constraints

- Seventeen intended canonical entries; `epistemic` is the usage entry, `using-epistemic-skills` its host-dependent historical alias, and `perspective` the new focused method.
- Metacognate retains substantive reasoning. Epistemic has no separate planner, dispatch engine, substantive verdict or task ledger. Helix is not revived as a coordinator.
- Prefer available applicable Superpowers systematic-debugging; retain an adequate standalone method and truthful provider reporting. No hard dependency on another skill package.
- Every skill actually used is visibly acknowledged; ordinary work does not acquire absent-trigger reports or mandatory process artifacts.
- Preserve current user scope and authorization, unrelated work, customized installations, historical IDs, Git history and existing release tags.
- No mandatory independent/cross-family release review. Do not fabricate blinding or weaken legitimate mission integrity and authorization requirements.
- Native goal/loop activation requires relevant user intent; budgets remain opt-in. Discover actual limits and state. Do not create a second runner.
- All 102 existing lens IDs receive their accepted disposition; add only the three approved queued capabilities. Remaining queue candidates stay deferred.
- Distinguish source checks, loaded-context evidence, exercised workflows and comparative benefit. Preserve failures and limits. Private telemetry never enters public artifacts.
- Use focused meaningful regression checks for changed behavior. Reuse existing suites; do not add tests that merely assert new prose is present.

## Start and dependency order

Before editing implementation, check root, branch, status, remotes and worktrees. At planning time the source checkout is on main at `9705f70aec1285597a6ef2a341cede80010c1dcb`; an existing stabilization worktree is unrelated to this implementation. Preserve it. The v6.0.0 release resolves locally to `b4bc8dff0d07a7535c24905af7fb97cc85e01037`. Refresh operational facts before using them.

Create a `codex/` implementation branch when execution begins, carrying the current design artifacts safely. Inspect any subsequently discovered v7 PR/branch before creating a duplicate. No reset, cleanup of unrelated worktrees, forced push or tag rewrite is required. Make scoped commits after each coherent verified bundle; record which checks ran. A local commit is not publication.

Dependency order:

1. T1 establishes the usage entry and accurate discovery checks.
2. T2-T6 refine the method groups; T4 consumes the shared-library work in T3. They have distinct source ownership except shared inventory surfaces, which T1/T8 own.
3. T7 exercises host delivery and native-goal paths using T1 and T5.
4. T8 aligns current public/package/release surfaces after all canonical entries exist.
5. T9 performs the frozen bounded comparison and assigned-reviewer release judgment.

The recommended first implementation slice is T1. Its done condition is a usable entry and an honest description check, not a new design document. No task waits for another general brainstorm.

## T1: usage entry, metacognate boundary and discovery checks

**Requirements:** R01, R02, R19; shared visibility and return contract.

**Files:** Create `plugins/epistemic-skills/skills/epistemic/SKILL.md`. Modify `plugins/epistemic-skills/skills/metacognate/SKILL.md`, `.github/scripts/check_loaded_descriptions.py`, `.github/scripts/sync_skill_surfaces.py`, `.github/scripts/check_skill_inventory.py`, `.github/scripts/check_no_phantom_skills.py` and the directly affected generated inventory/event surfaces. Keep `.github/scripts` as owner of package membership checks.

**Interface:** Current discovery descriptions identify applicability. The usage body establishes rules for reading and applying those methods; it produces no routing record or execution engine. `compare(packaged: dict[str, str], loaded: dict[str, str]) -> list[str]` retains its existing checker interface. Historical aliases resolve to one canonical identity only on verified host paths.

- [x] Add a failing regression to the existing loaded-description self-test, using the following cases. A one-word fragment must fail; intact and harmlessly wrapped text must pass under documented normalization.

```python
expected = {"sample": "Use when investigating a reproducible failure."}
assert compare(expected, {"sample": "Use"})
assert compare(expected, {"sample": "Use when investigating a failure."})
assert compare(expected, expected) == []
assert compare(expected, {"sample": "Use when investigating a\nreproducible failure."}) == []
```

- [x] Replace substring acceptance with comparison after narrowly justified presentation normalization. Preserve words, punctuation and applicability/exclusion clauses; do not normalize away semantic differences. Keep missing/empty descriptions as failures. Include Unicode text and duplicate conflicting capture identities in the changed parser checks where they affect truthful comparison.
- [x] Author the usage skill from the accepted guide: discovery, current method loading, applicability, visible use, provider preference/fallback and return to the task owner. Explicit invocation is honored; routine response handling is not a new planner or checklist. Include canonical metadata for the new entry.
- [x] Refine metacognate's substantive method and remove sole-entry wording, mandatory dispatch and blanket policy conflicting with the owner's release-review decision. Preserve meaningful task-specific evidence and authorization requirements.
- [x] Update source inventory arithmetic so the usage entry is the non-discipline and metacognate is a substantive method. In `sync_skill_surfaces.py`, the intended final classification is `NON_DISCIPLINES = {"epistemic"}`. Preserve dynamically computed counts as Perspective is added in T4. Generate existing projections with the existing `--write` interface; do not hand-edit generated membership.
- [x] Adjust retired-name checks to distinguish the documented compatibility alias from a claimed second live implementation. Keep historical producer IDs/version validation intact.
- [x] Run the commands below, inspect the actual diff, and commit this coherent bundle. Text/source conformance does not establish natural activation; that is exercised in T7/T9.

```text
python .github/scripts/check_loaded_descriptions.py --self-test
python .github/scripts/sync_skill_surfaces.py --write
python .github/scripts/sync_skill_surfaces.py --check
python .github/scripts/check_skill_inventory.py --self-test
python .github/scripts/check_skill_inventory.py
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/check_description_budget.py
python plugins/epistemic-skills/contracts/epistemic-events/test_epistemic_events.py
```

**Done:** The usage entry is directly readable/invocable, metacognate has a distinct contract, membership agrees with actual files, and a damaged description cannot pass as intact. No host startup coverage is claimed yet.

Implementation receipt (T1): the new checker regression failed on truncated and
conflicting captures before repair, then passed. Loaded-description, alias,
generator, inventory, event (17 tests), sentinel and ledger checks passed; source
descriptions total 8,561 bytes against the unchanged 8,636-byte ceiling. Current
entry documentation and generated projections agree on 16 entries pending
Perspective. The usage guide is exempt from mandatory run ledgers; canonical
membership uses SKILL.md files so retired cache directories cannot invent skills.
Public-content and diff checks passed. This is source/contract evidence only;
host delivery and comparative application remain T7/T9 work.

## T2: debugging and operational methods

**Requirements:** R05-R08.

**Files:** Modify `skills/health/SKILL.md`, `skills/triage/SKILL.md`, `skills/did-it-land/SKILL.md` and `skills/watch/SKILL.md` under `plugins/epistemic-skills/`. Create `skills/triage/reference/standalone-debugging.md` there. Modify `contracts/watch-commission/verify_watch_commission.py`, `contracts/watch-commission/test_watch_commission.py` and relevant sentinel fixtures/tests in the existing surfaces.

**Interface:** Triage either incorporates the actual preferred provider or uses the standalone procedure. Both preserve one investigation and the original repair scope. Watch retains `validate_record(record: dict) -> list[str]`, with proof history absent or complete in every applicable state. Present landing, observed reversal and future persistence risk remain separate outputs.

- [x] Extend the existing watch test with these two corruptions of `valid-suspect-observed-failure.json`; confirm failure before repairing the validator.

```python
import copy
import json
import runpy
from pathlib import Path
root = Path("plugins/epistemic-skills/contracts/watch-commission")
validate_record = runpy.run_path(str(root / "verify_watch_commission.py"))["validate_record"]
valid_suspect = json.loads((root / "examples/valid-suspect-observed-failure.json").read_text(encoding="utf-8"))
valid_suspect.pop("_expected")  # Fixture annotation is not a contract field.
assert validate_record(valid_suspect) == []
bad_crossing = copy.deepcopy(valid_suspect)
bad_crossing["proof"]["bound_crossed"] = False
assert validate_record(bad_crossing)
bad_history = copy.deepcopy(valid_suspect)
bad_history["reprove_after"] = None  # Missing key was already structurally rejected.
assert validate_record(bad_history)
```

- [x] Apply the absent-or-complete proof-history invariant across applicable states without promoting SUSPECT to PROVEN. Retain valid absent history, complete history and receipted failure cases as controls.
- [x] Write the standalone investigation procedure: establish the failure/reproduction limit; separate observations from hypotheses; obtain a discriminating observation; apply the authorized repair; check the original failure and relevant regression. Integrate causal standards into an available adequate provider investigation. Do not duplicate it merely to produce a triage report.
- [x] Rewrite did-it-land's predicted reversal wording into explicit current effect and future-risk statements. Retain REVERTED only for observed undo. Tighten health coverage/unknowns and watch's real external-observer boundary.
- [x] Exercise the original-failure, known-diagnosis reuse, healthy-but-stale-consumer and predicted-versus-observed-reversal cases through the existing sentinel/scenario framework. Treat manual prose review and executed observations as different evidence.

```text
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
python .github/scripts/score_sentinels.py --self-test
python .github/scripts/score_sentinels.py
```

**Done:** The proof-history defect has regression coverage, operational verdicts preserve their distinct meaning, and provider-present/provider-absent instructions lead to one adequate investigation with continuation.

Implementation receipt (T2): two new watch regressions failed before repair;
all 31 watch tests now pass, including complete and absent SUSPECT history and
rejected partial history. A null/blank re-proof boundary was the reproduced gap;
a missing top-level key was already structurally rejected. Ten synthetic
operational response controls cover original-failure verification, diagnosis
reuse, diagnosis-only scope and observed versus predicted reversal. Five negative
controls failed before the scorer change; all now pass alongside the existing
sentinel corpus. These are contract checks, not an agent-behavior trial. The four
method edits passed description-budget, evidence-format, inventory-generation,
public-content and diff checks. No live external observer was commissioned.

## T3: shared lens methods and complete disposition coverage

**Requirements:** R18; shared input to R13/R14.

**Files:** Modify `plugins/epistemic-skills/skills/gauntlet/roster/registry.json`, its `lens.schema.json`, `scripts/validate_roster.py`, `scripts/render_roster.py`, `reference/lens-registry.md` and generated roster views as needed. Create `plugins/epistemic-skills/reference/lenses.md` as shared selection/consumption guidance. Read the accepted `docs/audits/2026-09-18-v7-lens-members.json` as the per-ID source of work.

**Interface:** Both consumers read one canonical repertoire. Keep the existing physical registry location initially to avoid an unnecessary path migration. Generation, evaluation, gate and adjudication roles remain distinct; changed entries receive appropriate version/provenance updates. No separate copy of a card is created for Perspective.

- [x] Iterate all 102 assessed IDs and implement their `concrete_edits`, preserving original assessment evidence. Account for every retain/refine/combine/relocate/retired disposition in the task result with registry ID/version and source diff. Do not infer completion from counts alone.
- [x] For combined modes, preserve lookup identity, distinct mode questions and truthful diversity accounting. For historical retired entries, preserve replay and successor references. Resolve dialectical-synthesizer's contradictory ruling role and relocate adjacent-possible generation as assessed.
- [x] Add the three accepted methods with executable evidence procedures and honest limits: evidence-synthesis-auditor, stakeholder-representation-auditor, hermetic-reproducibility-auditor. Keep the other queued candidates unavailable.
- [x] Write the shared reference around question, evidence, procedure, possible result, revision condition, limits and stopping. Functional descriptions lead; persona aliases cannot imply authority, participation or independent evidence.
- [x] Update necessary schema/selector checks for role/mode boundaries. Add concrete controls: a generator cannot satisfy evaluator diversity; two modes of one mechanism do not become two independent confirmations; no material finding is a valid method outcome. Preserve historical schema interpretation where compatibility is claimed.
- [x] Verify that every source ID remains represented, then render and validate existing views. Inspect the actual semantic edits against the inventory; this code checks only ID retention.

```python
import json
from pathlib import Path
assessment = json.loads(Path("docs/audits/2026-09-18-v7-lens-members.json").read_text(encoding="utf-8"))
registry = json.loads(Path("plugins/epistemic-skills/skills/gauntlet/roster/registry.json").read_text(encoding="utf-8"))
expected = {row["id"] for row in assessment["members"]}
actual = {row["id"] for row in registry["entries"]}
assert len(expected) == 102
assert expected <= actual
assert len(actual) == len(registry["entries"])
```

```text
python plugins/epistemic-skills/skills/gauntlet/scripts/render_roster.py
python plugins/epistemic-skills/skills/gauntlet/scripts/render_roster.py --check
python plugins/epistemic-skills/skills/gauntlet/scripts/validate_roster.py
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
```

**Done:** All 102 dispositions are accounted for, the three additions have usable methods, both consumers can share one library, and structural success is not represented as empirical validation of every lens.

Implementation receipt (T3): all 102 original IDs are accounted for in the
versioned implementation audit; 96 available methods were refined, six retired
records preserve their original fields, and the three approved additions are
available. Root reviewed procedures and revision conditions against the accepted
member edits. Schema, generated views, 1,000 deterministic selection controls,
role/mode boundaries and the full Gauntlet suite pass. The historical synthetic
example retains its original registry pin and reports named registry drift; a
temporary synthetic control exercises current replay without changing history.
These checks establish structure and contract behavior, not empirical benefit
of the 99 available methods. Public-content and diff checks passed.

## T4: Perspective, Gauntlet and evidence-locked acceptance

**Requirements:** R13-R15, R20; depends on T3's shared contract.

**Files:** Create `plugins/epistemic-skills/skills/perspective/SKILL.md`. Modify Gauntlet's `SKILL.md`, `reference/execution-model.md`, `reference/roadmap.md`, relevant selection/adjudication scripts and `tests/run_tests.py`. Modify evidence-locked-uat's `SKILL.md`, `references/directive.md`, `references/schemas.md`, `references/standard.md` and `scripts/judge.py`. Use existing inventory generation for Perspective membership.

**Interface:** Perspective returns a bounded insight/finding/improvement/uncertainty. Gauntlet returns reasoned adjudication of plural scrutiny. UAT's compiled criteria and verifier/judge evidence must carry expected and disconfirming observations. Historical contracts remain interpretable by their original version.

- [x] Author Perspective's method using the shared lens contract. Allow adaptation and several lenses for the scoped concern without silently escalating to Gauntlet. Return the result to the task owner and show actual use.
- [x] Update Gauntlet for existing proposals and open decisions, separate initial examinations where available, constructive revision, factual checks versus value tradeoffs, preservation of dissent, and targeted rechecks. Report actual shared context/model/reviewer limitations. Remove any universal different-family release prerequisite while preserving task-specific honest evidence distinctions.
- [x] Resolve the public-telemetry contradiction and stale roadmap claim identified in the assessment. Real private run telemetry stays private; sanitized public evidence retains meaningful coverage limits and the actual historical outcomes.
- [x] Add explicit expected/disconfirming observation fields to the current UAT compiler contract and evidence interpretation. Use an explicit contract version or compatibility path if historical inputs lack them; do not rewrite historical packets as newly compliant. Extend the judge's meaningful self-tests with a persistence failure that contradicts a visible success state, a missing disconfirmation observation and a routine presentation case.
- [x] Exercise a focused concern, a multi-consideration decision, and a revised candidate. Check that each gets the intended method and that material dissent survives. Validate the source/contract behavior with existing checks below; natural selection is separately evaluated in T9.

```text
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
python plugins/epistemic-skills/skills/gauntlet/scripts/validate_ruling_set.py --self-test
python plugins/epistemic-skills/skills/evidence-locked-uat/scripts/judge.py --self-test
python plugins/epistemic-skills/skills/evidence-locked-uat/evals/triage/tests/run_tests.py
python .github/scripts/sync_skill_surfaces.py --write
python .github/scripts/check_skill_inventory.py
```

**Done:** Perspective and Gauntlet have distinct exercised contracts; UAT can represent and evaluate contrary observations; exact history and actual review separation are preserved.

Implementation receipt (T4): Perspective now consumes the shared library and
returns bounded findings without a lens-count escalation. Gauntlet keeps plural
adjudication, targeted revision, dissent and actual separation limits. Three
synthetic Workflow regressions first reproduced false GO paths (missing panel,
missing gate, dropped malformed material finding); all now pass with the clean
control and full Gauntlet suite. Existing ruling-set controls preserve dissent
kernels. UAT has an explicit v2 observation contract; ten Python/Workflow parity
cases plus nineteen historical judge controls and routine triage pass. Historical
packets remain labeled legacy. Root reviewed the focused, plural and revised-case
contracts; natural method choice remains a T9 claim, not established here.

## T5: native goals and continuity ownership

**Requirements:** R09-R12.

**Files:** Modify `plugins/epistemic-skills/skills/write-goal/SKILL.md`, `skills/manifest/SKILL.md`, `skills/decision-ledger/SKILL.md` and `skills/outsource/SKILL.md` under the same package. Create `skills/write-goal/reference/harness-contract.md` and extend its existing `evals/trigger-and-scope` cases. Modify existing mission-custody contracts only where a discovered implementation defect contradicts the accepted behavior; document already-correct machinery accurately. Extend existing outsource completion tests and decision-ledger resume/proportionality cases.

**Interface:** Goal authoring produces outcome, proof, scope, authority, inspect/act/verify loop and stop conditions. An authorized activation additionally yields the native identity/state and observed acknowledgment/readback limits. Existing mission/decision/relay artifacts retain authority over their respective facts. No generic goal runner or replacement global task schema is created.

- [x] Write the harness-contract procedure: inspect actual tool schema or installed help, existing goal state and capability surface; consult current official documentation only for unresolved facts; record scoped source/version and uncertainty. Cached profiles must be revalidated when relevant facts change.
- [x] Specify and exercise these synthetic adapter cases using the existing fixture machinery: character/byte/code-unit distinctions; counted serialization wrappers; separate completion fields; inaccessible external contract; draft-only instruction; existing active goal; validation rejection; ambiguous submission; stored truncation; unsupported persistence; omitted optional budget. Mark simulation separately from a live native tool run.
- [x] Use this concrete counting control in the payload tests, together with profile-specific limits; no test number becomes a claim about a real host.

```python
payload = "A" + chr(0x1F680)
assert len(payload) == 2
assert len(payload.encode("utf-16-le")) // 2 == 3
assert len(payload.encode("utf-8")) == 5
```

- [x] Preserve essential goal terms during compression. If a fuller contract is referenced, verify executor access now and on the claimed resume path. After ambiguous submission inspect state before retry; after a definite validation error correct representation within existing scope. Preserve actual pause/cancel/block/complete semantics and user opt-in budget rules.
- [x] Align manifest documentation with existing custody enforcement. Preserve next-action authority and evidence while avoiding ordinary-task mission creation. A bounded method return cannot silently close the caller's remaining work.
- [x] Make decision-ledger's persist/resume/outcome modes discoverable and preserve predictions separately from outcomes. Qualify reused ADRs by the information and provenance they actually hold.
- [x] Implement outsource's COMPLETE relay path in the existing workflow and tests; retain caller-owned integration work. Exercise interrupted authorized repair, stale relevant state, preserved prior answers/authority and completed external return. Ordinary local delegation remains available.

```text
python plugins/epistemic-skills/skills/write-goal/evals/trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/decision-ledger/reference/validate_examples.py
python plugins/epistemic-skills/skills/decision-ledger/evals/proportionality/tests/run_tests.py
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
python plugins/epistemic-skills/skills/outsource/evals/trigger-and-scope/tests/run_tests.py
```

If custody code changes, run the affected existing `test_custody_*.py` modules and then the current mission-custody workflow's relevant platform checks. Do not change custody code just to make its documentation sound simpler.

**Done:** Native goal/loop behavior remains central and surface-aware; continuity records preserve their distinct purposes; a resumed task continues the right authorized step; a completed relay can actually terminate.

Implementation receipt (T5): four scoped suites pass, including synthetic
Unicode/encoding/wrapper boundaries, activation/readback states, continuity and
COMPLETE relay controls. Root reviewed authority and termination semantics and
clarified that draft wording approval alone does not authorize activation.
Existing mission-custody enforcement already unions usable missions; the stale
README now describes it. No native goal or external relay was activated. The
broad package integration check's old metacognate tier assertions were removed;
its final version/count checks are recorded with T8 integration. Historical
resume trial outcomes, including the older failed corpus, remain unchanged.

## T6: framing, evidence, interviews and instruction context

**Requirements:** R03, R04, R16, R17.

**Files:** Modify each corresponding `SKILL.md` under `plugins/epistemic-skills/skills/`; recon's `reference/mode-brief.md`, `reference/mode-initiative.md` and `reference/mode-candidate.md`; resolve's `derivation`, `literature` and `probe` instructions as implicated by the assessment; and the existing trigger/scope fixtures and scorers for these methods.

**Interface:** Recon returns the corrected map or scope; Resolve returns the evidence-supported answer/limit; open-questions returns resolved/deferred user decisions; context-audit returns observed instruction/load findings and authorized maintenance results. None creates a compulsory four-stage sequence.

- [x] Remove mandatory filler counts from recon while retaining decision-relevant context. Add a zero-residual-question control, preserve the candidate-harvest alternative to adopting an entire package, and correct stale historical evidence labels.
- [x] Replace Resolve's contradictory fixed cost ordering with question/evidence-based instrument selection. Add single-citation verification with primary content and relevant reception/notices. Preserve research breadth where needed; keep artifact persistence and external library deposit distinct.
- [x] Retain experimental artifacts as evidence where useful while preserving the authorized promotion boundary. Do not claim a stub probe or deposited paper settles a production or scientific claim.
- [x] Exercise open-questions with prior answers, explicit exhaustive interview, a released interview with a still-unresolved consequential action, and a factual unknown the agent can investigate. It must resume permitted work without inventing consent or asking routine reversible choices.
- [x] Exercise context-audit with a stale installed copy, a precedence conflict, unavailable assembled context and removal of a rarely used protection. Preserve the distinction between an immediate precedence resolution and an authorized persistent edit; state observed regression coverage accurately.
- [x] Update the existing scorers only where they enforce superseded format quotas or requirements. Keep old run outputs and explain why new scoring applies to new cases; do not rescore old failures as successes without a separately labeled analysis.

```text
python plugins/epistemic-skills/skills/recon/evals/brief-trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/recon/evals/initiative-trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/recon/evals/candidate-trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/resolve/derivation/evals/formal-rigor-v2-fixtures/tests/run_tests.py
python plugins/epistemic-skills/skills/resolve/literature/evals/trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/resolve/probe/evals/trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/open-questions/evals/trigger-and-scope/tests/run_tests.py
python plugins/epistemic-skills/skills/context-audit/evals/trigger-and-scope/tests/run_tests.py
```

**Done:** Each method preserves its distinct work while reducing manufactured questions, reports, research breadth and unsupported context claims. Existing authorizations and protected instructions remain intact.

Implementation receipt (T6): root reviewed the scoped method changes and worker
evidence against R03/R04/R16/R17. All eight requested suites pass. Synthetic
regressions discriminate zero-question framing, recovered answers and interview
release, bounded citation verification, archived experimental evidence, and
source-versus-loaded context limits. Historical run files and their failed
outcomes remain unchanged. These are method and scorer checks; no host loading,
scholarly connector exercise or comparative benefit is claimed here.

## T7: verify and implement actual host delivery

**Requirements:** R19 and the live integration part of R09; depends on T1/T5.

**Files:** Existing `plugins/epistemic-skills/hooks/hooks.json`, `codex-hooks.json`, `cursor-hooks.json`, `render_cursor_cli_hooks.py`, host manifests and `GEMINI.md`. Create `plugins/epistemic-skills/hooks/usage_context.py` only if a shared renderer is needed by the verified hook interfaces; use `test_usage_context.py` beside it for meaningful delivery tests. Create `docs/release/v7-host-coverage.md` for the actual per-surface evidence and limitations.

**Interface:** One canonical body is read and emitted through a verified host context-loading mechanism. A shared loader can have this simple interface; host-specific framing is implemented only after its actual API contract is observed.

```python
from pathlib import Path

def load_usage_context(plugin_root: Path) -> str:
    return (plugin_root / "skills" / "epistemic" / "SKILL.md").read_text(encoding="utf-8")
```

- [x] Inventory the host surfaces already advertised by the repository. Record actual product/surface/version, installation path class, available entry hooks, context/reset semantics, native alias capability and observed native goal support. Use local authoritative schemas/help first and current official documentation for unresolved facts. No personal absolute paths or private machine details go into the public table.
- [x] Select the available current host as the first live exercise. For other advertised surfaces, implement only verified interfaces and label source-only, simulated, unavailable or actually exercised support accurately. Do not infer one host's support from another.
- [x] Implement supported early delivery and explicit fallback from the canonical source. Keep mission-custody hooks unchanged in meaning. Ensure duplicate copies/injections and missing entry files have observable, bounded outcomes; unsupported alias paths retain documentation-only mappings.
- [x] Test canonical body round-trip including Unicode/escaping, missing file behavior, source version disagreement, duplicate injection handling and startup/resume routing appropriate to the actual host. A synthetic hook payload test proves serialization and routing logic, not live context delivery.
- [x] Capture a live skill listing/context evidence where available and run the repaired checker with that capture. Separately observe an ordinary prompt invoking a relevant method and reporting its contribution. If full context is not visible, report the narrower observation.
- [x] Exercise native goal representation/readback through an explicitly authorized isolated test context, or report it as simulated/unavailable. This plan does not authorize creating persistent goals in the owner's active work merely to get a passing test.

```text
python .github/scripts/check_loaded_descriptions.py --self-test
python .github/scripts/check_description_budget.py --report
python plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py
python plugins/epistemic-skills/reference/runtime-gate/test_hook.py
```

For the live comparison, call the existing `check_loaded_descriptions.py --capture` interface with the actual capture file recorded for that run. Never substitute the generated package list as evidence of host loading.

**Done:** The support table names what was actually delivered and exercised. Unsupported paths have usable truthful fallback guidance. No capability is advertised from a snippet, mock or startup banner alone.

Implementation receipt (T7): documented Codex/Claude SessionStart interfaces
now read one canonical usage body; six loader tests cover lifecycle, Unicode,
fingerprint/missing-source and version-disagreement boundaries. Existing custody
and runtime suites pass. A real credential-free Codex CLI app-server listing
exposed all 17 canonical descriptions intact, plus six nested methods; the actual
sanitized capture passes the repaired checker. Other hosts and native goals are
labeled by observed capability and evidence tier. Model consumption at startup,
ordinary-task application and native-goal readback were not exercised here; those
support claims are withdrawn rather than inferred from source checks.

## T8: current documentation, packaging and release authority

**Requirements:** R20, R22; integrates T1-T7.

**Files:** `README.md`, `GEMINI.md`, `plugin.json`, `gemini-extension.json`, applicable `.claude-plugin`, `.codex-plugin` and `.cursor-plugin` manifests/marketplaces; `plugins/epistemic-skills/ROUTING.md`; `.github/scripts/sync_skill_surfaces.py`, inventory/phantom/privacy/bundle checks and affected workflows. Create `docs/release/RELEASE-7.0.0.md`, `docs/release/v7-evidence.md` and the current v7 handbook snapshot under `docs/wiki-updates/v7.0.0/` using the existing handbook machinery. Preserve versioned prior release evidence.

**Interface:** Canonical skill metadata drives live inventory/count surfaces. The current release packet points to actual source revisions, checks, host coverage and limitations; it does not reinterpret historical assurance records as current.

- [ ] Replace current sole-metacognate-entry guidance with the accepted usage entry, direct access and visible-use behavior. Present functional labels, ordinary examples and tested host coverage. Verify counts after both additions; alias documentation does not create a duplicate canonical entry.
- [ ] Remove current policy dependencies on mandatory independent/cross-family release review. Keep historical v6 reviews, exception records, assurance packets and tests meaningful for their original subjects. A versioned old requirement can remain historical without gating v7.
- [ ] Align README, package/host metadata, generated event surfaces, current handbook and release notes. Reuse handbook checker logic with the needed version awareness; do not edit old snapshots to make them describe v7. Check current links to actual source paths/tags instead of blindly replacing version strings.
- [ ] Add current release evidence with requirements R01-R22, implementation revisions, affected checks, host exercise level, comparative findings and unresolved limitations. Preserve private telemetry outside public artifacts; publish sanitized evidence sufficient to assess each claim.
- [ ] Run affected package/build checks, current handbook checks and the existing privacy/security workflow. Resolve misleading current claims before release; unrelated historical content is not a broad rewrite project.

```text
python .github/scripts/sync_skill_surfaces.py --self-test
python .github/scripts/sync_skill_surfaces.py --check
python .github/scripts/check_skill_inventory.py --self-test
python .github/scripts/check_skill_inventory.py
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/check_description_budget.py
python .github/scripts/check_json_artifacts.py
python .github/scripts/check_public_content.py
python .github/scripts/test_build_openai_bundles.py
python .github/scripts/test_openai_bundle_workflow.py
```

Use the bundle builder's existing revision argument with the actual committed candidate. A test-only build must not claim a released tag exists. Check the current handbook snapshot with the version-aware interface implemented in this task, preserving the previous snapshot's validation.

**Done:** The public product description matches the candidate, current policy reflects the assigned reviewer, packaging is coherent, and historical records/private data are handled honestly.

## T9: bounded behavioral comparison and release judgment

**Requirements:** R21 plus integration evidence for R01-R22; depends on the relevant completed bundles.

**Files:** Reuse `plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/` fixtures and runner/scorer conventions. Create `v7-campaign.md` there for preregistration; add only changed-behavior fixtures missing from existing coverage. Put sanitized results under its existing `results/` layout and summarize in `docs/release/v7-evidence.md`.

**Interface:** Capture raw observable responses, tool actions and artifacts without giving both arms an intervention-shaped trace template. A private run record binds candidate, baseline, scenario, actual model/configuration, exposure, tools, time/cost and outcome evidence. Public summaries remove private context while preserving the comparison's limits.

- [ ] Freeze the committed candidate and immutable v6.0.0 baseline, matched model/configuration and providers, actual entry/discovery exposure, inputs, outcome rubric and run budget. Record the actual runner and supported isolation mechanism. Provider and host selection must be grounded in availability; do not invent access or claim a forced load is natural activation.
- [ ] Use the twelve core scenarios below, adapting existing artifacts rather than manufacturing a second evaluation framework. Prompts for natural activation must not name the desired method. Explicit skill/alias invocation and mechanical boundary checks remain separate.

| Case | Task and primary observation |
|---|---|
| B01 | Repair a reproducible failure; discriminate cause, complete authorized repair and check the original failure. |
| B02 | Complete a routine reversible edit with an adequate direct check and little process. |
| B03 | Report bounded current health, including coverage/unknowns, without inventing diagnosis or persistent monitoring. |
| B04 | Detect a stale consumer after a successful change command; separate observed effect from future persistence risk. |
| B05 | Correct an inadequate success proxy or mistaken approach without treating metacognate as a generic dispatcher. |
| B06 | Examine one bounded proposal concern through Perspective and return a useful result. |
| B07 | Adjudicate a consequential choice with competing considerations, preserving material dissent and scoped follow-up. |
| B08 | Adapt a requested native goal to a synthetic surface contract with limits, existing state and ambiguous-response controls. |
| B09 | Resume interrupted authorized work, reuse valid decision/custody evidence and close a completed relay appropriately. |
| B10 | Verify a specific citation with adequate evidence and bounded research; do not manufacture a review quota. |
| B11 | Resolve a scoped instruction conflict and recover prior user decisions without a redundant interview or full-context overhaul. |
| B12 | Reject visible success that fails persistence/acceptance; keep a routine presentation control appropriately bounded. |

- [ ] Working pilot cap: 24 first runs (12 cases x two versions), plus one predetermined repeat of B01, B02, B08 and B09 in each version (eight runs), for at most 32 planned subject runs. Freeze the schedule before outcomes are observed. This is an exploratory bounded pilot, not a population reliability estimate or proof of all lenses/hosts. No automatic extra arms or repeated favorable-run search.
- [ ] State existing runner per-run limits and capture actual completion/failure/timeout. If isolation, exposure or result capture is unavailable, stop that claim at its true evidence level and continue other verification. Keep native-goal cases simulated unless test-scoped real activation is explicitly authorized; never label simulation as live.
- [ ] Score outcomes, method application, visible acknowledgment, unnecessary process, authorization/scope and continuation separately. Root reviews ambiguous evidence with the frozen rubric. Preserve all failures and scorer changes; apply a justified scorer correction consistently to both arms.
- [ ] For a material failure, diagnose and repair the affected candidate or withdraw the affected claim. Record targeted corrected-candidate reruns separately and within the available campaign budget; do not replace unsuccessful unchanged-candidate trials with successful retries. Broader work requires a concrete new decision, not automatic evaluation expansion.
- [ ] Run affected existing conformance tests and required hosted checks at the candidate revision. Summarize actual benefit or inconclusive results, remaining limitations and support claims. Do not claim all seventeen methods naturally activate based solely on this pilot.

```text
python plugins/epistemic-skills/evals/epistemic-flexibility/run_tests.py
python plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/run_tests.py
python plugins/epistemic-skills/evals/proportionality/run_tests.py
python .github/scripts/check_public_content.py
```

- [ ] Make the assigned-reviewer release judgment against the spec and evidence. No new mandatory reviewer family is needed. Respect applicable existing publication authority, preserve tags/history and distinguish prepared, committed, pushed, merged and released states. Attach any created PR to the task. Publication is not complete until the relevant hosted checks and actual published artifacts are verified.

**Done:** V7 has a traceable requirement disposition, honest scoped outcome evidence and a finite release judgment. Passing source tests alone cannot satisfy an unproved behavioral claim. A remaining limitation is not silently converted into success or a request for an endless new panel.

## Coverage and stopping record

| Requirements | Owning task |
|---|---|
| R01, R02 | T1 |
| R03, R04, R16, R17 | T6 |
| R05, R06, R07, R08 | T2 |
| R09, R10, R11, R12 | T5; actual host facts/exercise in T7 |
| R13, R14, R15 | T4 |
| R18 | T3 |
| R19 | T1 and T7 |
| R20 | T4 and T8 |
| R21 | T9, with per-task regression evidence |
| R22 | T8 and publication verification in T9 |

Every accepted skill and library decision maps to a task. Deferred queue entries and rejected coordinator behavior have no implementation task. No unresolved product decision currently requires another general brainstorming round. A newly discovered material contradiction is resolved at the affected requirement and recorded; unchanged decisions remain settled.

Stop each bundle at its defined done condition. Stop the overall work only when implemented behavior, relevant checks, actual coverage and the publication state satisfy the requested release outcome, or when a specific external limitation is accurately reported. Do not confuse this complete plan with completed implementation.
