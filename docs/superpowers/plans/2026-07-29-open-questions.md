# open-questions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `open-questions` as the tenth discipline in the epistemic-skills collection, release v3.1.0, then bring the zms-homelab fleet layer up to date with all six missing skills.

**Architecture:** Three sequential phases. Phase A (feature PR, this repo): author the skill core and update every count-asserted integration surface, driven by the package integration test. Phase B (release PR, this repo): version bump per RELEASING.md. Phase C (fleet PR, zms-homelab): worktree-isolated core sync + LOCAL.md overlays + status table.

**Tech Stack:** Plain markdown skill cores; Python stdlib integration test (`plugins/epistemic-skills/skills/outsource/tests/run_tests.py`); GitHub Actions CI (`.github/workflows/epistemic-flexibility.yml`); git worktrees for the fleet repo.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-29-open-questions-design.md` (approved 2026-07-29) — the skill's content authority.
- All files authored **LF** (`.gitattributes` is `* text=auto eol=lf`); verify no CRLF before commit.
- Canonical tree ONLY: `plugins/epistemic-skills/skills/...`. Root `skills/` and `agents/` are git symlinks (mode 120000) — NEVER create real root directories.
- Every commit: `git commit --signoff`, author `SternOne <zachstern@gmail.com>` (DCO-enforced).
- Frontmatter: exactly two keys (`name`, `description`), trigger-only SDO style, single-quoted YAML.
- The skill core MUST end with the standard `## Local overlay` section.
- Count literals are CI-asserted as exact substrings including markdown emphasis (`**eleven** skills` and `eleven skills` are distinct assertions). Update the test FIRST, then edit prose until the test passes.
- Version numbers change ONLY in Phase B (RELEASING.md: version alignment happens in the release PR, not the feature PR). Count text inside manifest descriptions changes in Phase A.
- zms-homelab currently has uncommitted work on `feat/pm-corpus-github-cutover`. Phase C uses `git worktree add` off `origin/main` — never stash, checkout, or pull in the existing working tree (RULE-028).

---

## Phase A — Feature PR (epistemic-skills)

### Task A1: Branch + integration test expectations (test-first)

**Files:**
- Modify: `plugins/epistemic-skills/skills/outsource/tests/run_tests.py`

**Interfaces:**
- Produces: the failing test that defines "done" for Tasks A2–A7. All later tasks run `python plugins/epistemic-skills/skills/outsource/tests/run_tests.py` as their oracle.

- [ ] **Step 1: Create branch**

```bash
cd /y/dev/epistemic-skills && git checkout -b feat/open-questions main
```

- [ ] **Step 2: Update test expectations**

In `run_tests.py`, make these changes (locate by searching the quoted literals):
- `require(len(skill_dirs) == 11, ...)` → `== 12` (update the message string too).
- Every count-literal assertion updates one word: `"These nine disciplines"` → `"These ten disciplines"`, `"why these nine"` → `"why these ten"`, `"**eleven** skills"` → `"**twelve** skills"`, `"**nine** disciplines"` → `"**ten** disciplines"`, `"all eleven skills"` → `"all twelve skills"`, `"canonical skill cores (eleven)"` → `"canonical skill cores (twelve)"`, `"eleven skills"` → `"twelve skills"`, `"nine disciplines"` → `"ten disciplines"`.
- If the test asserts a negative (e.g. that the old count is absent), point the negative at the previous count (`eleven`/`nine`).
- If the test enumerates skill directory names, add `open-questions` to the list.

Read the whole test file first — my literal list comes from recon and may be incomplete; the file is the authority.

- [ ] **Step 3: Run test to verify it fails**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
```
Expected: FAIL — "expected 12 skill directories, found 11" (and/or count-literal failures).

- [ ] **Step 4: Commit**

```bash
git add plugins/epistemic-skills/skills/outsource/tests/run_tests.py
git commit --signoff -m "test(package): expect twelve skills / ten disciplines for open-questions"
```

### Task A2: Author the skill core

**Files:**
- Create: `plugins/epistemic-skills/skills/open-questions/SKILL.md`

**Interfaces:**
- Produces: the skill core whose name (`open-questions`), boundary vocabulary ("emptied-or-parked ledger", "4-field stamp", "closing probe"), and Do-NOT-fire attributions Tasks A3–A5 reference verbatim.

- [ ] **Step 1: Write SKILL.md with exactly this content**

````markdown
---
name: open-questions
description: 'Use when the operator asks to be interviewed about open questions or decisions — "ask me open questions one by one until none remain", "walk me through the open decisions", "interview me until nothing is left" — or when a load-bearing fork is irreversible or high-blast-radius, cannot be safely best-guessed, and the operator is interactively present. Do NOT fire for design-stage dialogue while a workflow design skill is running (that skill owns its own questioning), for producing the initial question list on a fuzzy brief (blindspot-pass owns recon; this skill consumes its Questions output), for goal-shaping (write-goal owns that), or when the operator is absent — park on best-guess defaults and proceed instead.'
---

# open-questions — walk the ledger to empty

An exhaustive serial clarification interview that gates work. Enumerate every
open question whose answer could change the work, walk them with the operator
one at a time, and resume only when the ledger is empty and a closing probe
surfaces nothing new — or the operator releases the gate.

Every sibling discipline terminates on something other than exhaustion:
sufficiency, approval, a recon ceiling. This skill exists for the case where
the operator wants the question set *emptied* — no silent best-guessing, no
"I believe I understand," no deferral. Its posture is the inverse of
blindspot-pass: where that skill converts questions into falsifiable
best-guesses so work can proceed *without* the operator, this one converts
best-guesses back into questions because the operator is present and has
asked to decide.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| Pre-work recon on a fuzzy request | blindspot-pass | Produces the seed question list ("Questions you should be asking"); this skill consumes it and conducts the interview blindspot-pass deliberately refuses to |
| Design-stage dialogue | the workflow layer's design skill | Owns its own one-question-at-a-time refinement; this skill defers while it is active |
| Durable objective authoring | write-goal | Owns goal-shaping questions; this skill may surface that a goal is needed, never writes one |
| Persisting the answers | decision-ledger | Answers that are decisions worth keeping flow onward; this skill's ledger is an interview artifact, not the durable record |

## Two modes, one ledger

Choose by situation shape at entry; switch mid-run when the shape changes.

**Docket mode** — the open-question set is known and finite. Present the full
enumerated docket upfront: numbered items, each carrying (a) one-sentence
context, (b) impact-if-unanswered, (c) your best-guess default. The operator
triages: reorders, answers in any order, strikes items, accepts defaults
wholesale. Walk the remainder serially, highest-impact first — response
quality measurably degrades late in long question batteries, so the questions
that gate the most work go first.

**Cascade mode** — answers beget questions. A serial laddering interview: one
question per message; each answer may append follow-ups to the ledger.
Announce every append ("your answer opened two new questions — added as #7,
#8"); the ledger never grows silently. Probe with intent: clarify, elaborate,
explain, or trace a concrete instance — not "anything else?" filler.

A docket answer can open a cascade; a cascade can surface a batch worth
docketing. The ledger is continuous across the switch.

## The ledger

- Numbered, append-allowed, visible to the operator at all times.
- Entry bar: a question enters if its answer could change the work.
  Materiality gates *entry*, never silent skipping — once in, an item is
  asked or explicitly parked.
- Every item carries a best-guess default. An unanswered question is a
  deferral; a best-guess is a falsifiable claim the operator can correct in
  one word.
- One question per message. Prefer a closed choice when the alternatives are
  known; open-ended when they are not. Never batch answers-due into a single
  message — the docket view is for triage, not for answering.

## Termination

Work resumes when any ONE of these holds:

1. **Exhaustion + closing probe.** The ledger is empty AND one closing probe
   ("anything material I haven't asked about?") yields nothing new. An empty
   ledger alone is necessary, not sufficient.
2. **Operator release.** The operator says "proceed" (or equivalent) at any
   point. Park every remaining item: apply its best-guess default, list the
   parked items in the exit stamp. Parked is announced, never silent.

Exit emits a 4-field stamp: `mode(s) used · asked/answered count · parked
items (with applied defaults) · the stage this interview gated`.

## Anti-patterns

| Thought | Reality |
|---|---|
| "I'll batch three quick questions in one message" | Serial is the discipline. One per message; the docket view is for triage, not answering. |
| "This question is minor, I'll skip it" | Materiality gates entry, not skipping. Ask it or park it explicitly. |
| "The ledger is empty, work continues" | Not until the closing probe. Empty is necessary, not sufficient. |
| "The operator seems busy, I'll just decide" | Release is the operator's word, not your inference. Park with defaults and announce. |
| "Every fuzzy task needs this interview" | No. Explicit invocation or the narrow auto-trigger only. Best-guess-and-proceed remains the default posture. |
| "My follow-up doesn't need to enter the ledger" | Silent growth breaks the exhaustion contract. Append and announce. |

## Provenance

The two-mode structure, serial one-per-message walk, and stopping criterion
are grounded in the elicitation and saturation literature (structured
interviews as the most effective elicitation technique; laddering/probing for
answer-begotten questions; run-length stopping criteria in place of naive
exhaustion; late-battery quality decay motivating triage order). See the
design spec in the repository's `docs/superpowers/specs/` for the cited
evidence run.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (harness question tooling,
operator autonomy preferences, parked-item logging paths, sibling-skill
integrations). An overlay may add bindings and examples; it never overrides
the protocol.
````

- [ ] **Step 2: Verify LF and run the test**

```bash
file plugins/epistemic-skills/skills/open-questions/SKILL.md   # must NOT say CRLF
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
```
Expected: directory-count assertion now passes; count-literal assertions on router/README/GEMINI still FAIL.

- [ ] **Step 3: Commit**

```bash
git add plugins/epistemic-skills/skills/open-questions/SKILL.md
git commit --signoff -m "feat(open-questions): tenth discipline — exhaustive serial clarification interview"
```

### Task A3: Router integration (using-epistemic-skills)

**Files:**
- Modify: `plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md`
- Check: `plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md`

**Interfaces:**
- Consumes: skill name and boundary vocabulary from Task A2.

- [ ] **Step 1: Read the whole router file, then make these edits**

1. Frontmatter `description`: add `open-questions` to the member list.
2. `"These nine disciplines"` → `"These ten disciplines"`; the `## Shared invariants (why these nine…)` heading → `why these ten`; sweep any other `nine disciplines` occurrences.
3. **Handoff-boundary table** — add row:
   `| open-questions | blindspot-pass Questions section (when present); operator-named open decisions | an emptied-or-parked question ledger (its boundary) | the stage the interview gated | session-continuous | 4-field stamp |`
4. **Order-of-ops arc**: add `open-questions` as cross-cutting (callable at any stage boundary when its trigger fires), alongside the arc bullets — do not insert it as a fixed stage.
5. **Routing table** — add row:
   `| ask the operator to decide the open questions before work continues | open-questions | exhaustion is the termination contract; brainstorming ends at sufficiency, blindspot-pass ends at understanding |`
6. Anti-patterns table — add:
   `| "The operator is present, so I should interview them about everything" | open-questions fires on its explicit phrase or an un-best-guessable irreversible fork — not on presence. Best-guess-and-proceed stays the default. |`
7. `reference/routine-fast-path.md`: add `open-questions`' ledger/stamp to the must-not-manufacture list (the skill emits a named process artifact).

- [ ] **Step 2: Run test**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
```
Expected: router-literal assertions pass; README/GEMINI assertions still FAIL.

- [ ] **Step 3: Commit**

```bash
git add plugins/epistemic-skills/skills/using-epistemic-skills/
git commit --signoff -m "feat(router): wire open-questions — handoff row, routing row, ten-discipline counts"
```

### Task A4: helix pairing row

**Files:**
- Modify: `plugins/epistemic-skills/skills/helix/SKILL.md`

- [ ] **Step 1: Add pairing-map row (position vocabulary is closed: before/inside/at approval/pre-merge/cross-cutting/is)**

`| any gated stage (operator explicitly asks to be interviewed until no open questions remain) | **open-questions** | *before* the gated stage — the ledger empties (or parks on operator release), then the stage proceeds |`

- [ ] **Step 2: Add co-fire bullet**

`- **the operator asks to answer the open questions one by one** → open-questions conducts the interview before the gated stage resumes; blindspot-pass's Questions section, when present, seeds the ledger. Presence alone never fires it.`

- [ ] **Step 3: Run test (expect no helix assertions to fail), commit**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
git add plugins/epistemic-skills/skills/helix/SKILL.md
git commit --signoff -m "feat(helix): pairing row for open-questions"
```

### Task A5: README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read README fully, then update every surface**

1. Count literals: `**eleven** skills` → `**twelve** skills`, `**nine** disciplines` → `**ten** disciplines`, `all eleven skills` → `all twelve skills`, `canonical skill cores (eleven)` → `(twelve)`, per-harness install "verify eleven skills" cells → twelve. Sweep with `grep -n "eleven\|nine" README.md` and update each hit that refers to counts (leave non-count uses alone).
2. `## Contents` nav: add open-questions.
3. `## Choose by task` table: add `| Get every open decision answered by the operator before work continues | open-questions |`.
4. Epistemic-arc mermaid diagram: add open-questions as a cross-cutting node (mirror how other cross-cutting skills are drawn).
5. `## Eleven-skill catalog` heading → `## Twelve-skill catalog`; update any in-page anchor links (`#eleven-skill-catalog` → `#twelve-skill-catalog`); add catalog row: `| open-questions | Operator asks to be interviewed until no open questions remain; un-best-guessable irreversible fork with operator present | Exhaustive serial clarification interview (docket + cascade modes) | Emptied-or-parked ledger + 4-field stamp |` (match the existing row format and wiki-link style).
6. Repo-layout tree block: add `open-questions/` in alphabetical position.

- [ ] **Step 2: Run test, commit**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
git add README.md
git commit --signoff -m "docs(readme): twelve-skill catalog + open-questions surfaces"
```

### Task A6: GEMINI.md + manifest count text

**Files:**
- Modify: `GEMINI.md`, plus any manifest whose *description text* carries a count: `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `.kimi-plugin/plugin.json`, `.kimi-plugin/marketplace.json`, `gemini-extension.json`, `plugins/epistemic-skills/.claude-plugin/plugin.json`, `.codex-plugin`/`.cursor-plugin`/`.kimi-plugin` under `plugins/epistemic-skills/`, root `plugin.json`, `.agents/plugins/marketplace.json`

- [ ] **Step 1: GEMINI.md**

`"eleven skills: router + nine disciplines + the helix tandem entry point"` → `"twelve skills: router + ten disciplines + the helix tandem entry point"`; sweep remaining count literals.

- [ ] **Step 2: Manifests — count text only, versions untouched**

```bash
grep -rn "eleven\|nine disciplines" --include="*.json" .
```
Update each description hit (`eleven self-triggering skills` → `twelve self-triggering skills`, `nine disciplines` → `ten disciplines`). Do NOT change any `version` field. Validate: `python -c "import json,glob; [json.load(open(p)) for p in glob.glob('**/*.json', recursive=True) if '.git' not in p]"`.

- [ ] **Step 3: Run test, commit**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
git add -A
git commit --signoff -m "docs: twelve-skill counts in GEMINI.md and manifest descriptions"
```

### Task A7: CI workflow + full local pass

**Files:**
- Modify: `.github/workflows/epistemic-flexibility.yml`

- [ ] **Step 1: Check whether the workflow needs a change**

open-questions ships no `.py` and no `evals/`, so likely no new step. But `run_tests.py` self-asserts workflow parity — read the test's workflow assertions; if it requires a named step per skill or lists skill paths, add the matching entry for open-questions.

- [ ] **Step 2: Full local verification**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
grep -rIl $'\r' plugins/epistemic-skills/skills/open-questions/ README.md GEMINI.md || echo "LF clean"
```
Expected: ALL assertions PASS; "LF clean".

- [ ] **Step 3: Commit (if workflow changed), push, open PR**

```bash
git push -u origin feat/open-questions
gh pr create -R ZMS-Labs/epistemic-skills --title "feat: open-questions — tenth discipline (exhaustive serial clarification interview)" --body "Implements docs/superpowers/specs/2026-07-29-open-questions-design.md. Two modes (docket/cascade), append-allowed ledger, falsifiable exhaustion termination. Counts: ten disciplines / twelve skills; integration test updated first (TDD). Version bump follows in the release PR per RELEASING.md.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011L3kh3mNct92BFDrfWKD5G"
```

- [ ] **Step 4: Wait for CI green (all checks incl. DCO, gitleaks), then merge**

```bash
gh pr checks --watch && gh pr merge --squash
```

## Phase B — Release PR (v3.1.0)

### Task B1: Version bump per RELEASING.md

**Files:**
- Read FIRST: `RELEASING.md` (it is the authority; steps below are the recon-derived floor)
- Modify: all 10 version surfaces — `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `.kimi-plugin/plugin.json`, `.kimi-plugin/marketplace.json` (version hidden in a `/tree/v3.0.0` URL — easiest to miss), `gemini-extension.json`, `plugins/epistemic-skills/.claude-plugin/plugin.json`, `plugins/epistemic-skills/.codex-plugin/plugin.json`, `plugins/epistemic-skills/.cursor-plugin/plugin.json`, `plugins/epistemic-skills/.kimi-plugin/plugin.json`

- [ ] **Step 1: Branch off updated main; bump every `3.0.0` → `3.1.0`**

```bash
git checkout main && git pull && git checkout -b release/3.1.0
grep -rn "3\.0\.0" --include="*.json" . | grep -v node_modules
```
Update every version hit including the `.kimi-plugin/marketplace.json` URL. Follow any additional RELEASING.md steps (changelog, tag).

- [ ] **Step 2: Verify parity, push, PR, merge, tag per RELEASING.md**

```bash
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py   # asserts version parity across manifests
git add -A && git commit --signoff -m "release: v3.1.0 — open-questions"
git push -u origin release/3.1.0 && gh pr create -R ZMS-Labs/epistemic-skills --title "release: v3.1.0" --body "Version alignment for open-questions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011L3kh3mNct92BFDrfWKD5G"
gh pr checks --watch && gh pr merge --squash
```

## Phase C — Fleet-layer catch-up (zms-homelab)

### Task C1: Safety gate + worktree

- [ ] **Step 1: RULE-028 gate — report, never touch**

```bash
cd /y/dev/zms-homelab && git status --short | head -20
```
Expected: uncommitted work on `feat/pm-corpus-github-cutover`. Do NOT stash/checkout/pull. Proceed via worktree only.

- [ ] **Step 2: Worktree off fresh origin/main**

```bash
git fetch origin && git worktree add /y/dev/zms-homelab-wt-fleet-catchup -b feat/epistemic-fleet-catchup origin/main
```

### Task C2: Sync the six missing cores byte-identical

**Files (in the worktree):**
- Create: `skills/{helix,write-goal,outsource,continuity-verify,decision-ledger,open-questions}/SKILL.md` — byte-identical copies from the epistemic-skills checkout at the v3.1.0 merge commit
- Note: the canonical sync tool is `skills/gauntlet/scripts/sync-epistemic-cores-from-oss.ps1` but PowerShell is blocked on this device — replicate in bash. Also copy any `reference/` dirs those skills ship (check each skill dir in the source; copy the whole dir minus tests/evals if the existing layered skills' convention does so — inspect how `blindspot-pass/` is layered fleet-side and match it).

- [ ] **Step 1: Copy + drift-check all cores (the six new AND the existing ones)**

```bash
SRC=/y/dev/epistemic-skills/plugins/epistemic-skills/skills
DST=/y/dev/zms-homelab-wt-fleet-catchup/skills
for s in helix write-goal outsource continuity-verify decision-ledger open-questions; do
  mkdir -p "$DST/$s" && cp "$SRC/$s/SKILL.md" "$DST/$s/SKILL.md"
done
for s in $(ls "$SRC"); do
  [ -f "$DST/$s/SKILL.md" ] && { cmp -s "$SRC/$s/SKILL.md" "$DST/$s/SKILL.md" && echo "OK $s" || echo "DRIFT $s"; }
done
```
Expected: `OK` for all twelve; any `DRIFT` on a pre-existing core means the fleet copy is stale — refresh it in this same PR (drifted core = declared bug).

### Task C3: LOCAL.md overlays (six new skills)

**Files (in the worktree):**
- Create: `skills/<name>/LOCAL.md` for each of the six

- [ ] **Step 1: Author each LOCAL.md following the existing pattern (read `skills/evidence-research/LOCAL.md` as the template: Bindings / Durability / Harness bindings sections)**

Required bindings per skill (keep each file short — pointers, not prose):
- **open-questions**: harness question tool = AskUserQuestion (one question per message; closed-choice preferred); operator autonomy standing feedback means the narrow auto-trigger is read strictly (no permission-pause generation); parked items are logged to the session log via the standard `[DECISION]` tag; blindspot-pass fleet overlay is the seed-source sibling.
- **helix**: workflow layer on this fleet = superpowers (plugin); harness auto-fire via using-superpowers; helix-check lines land in session logs.
- **write-goal**: goals feed `/goal` dispatches and write-goal command alias if present; durable sink = GitHub issues (ADR-171).
- **outsource**: packet host = GitHub (ZMS-Labs), pointer style per RULE-012 tiers; ChatGPT relay boundary lesson (clean-boundary standalone only).
- **continuity-verify**: durable anchors on this fleet = GitHub issues/PRs, session logs, memory directory; compaction summaries are the primary trigger.
- **decision-ledger**: the fleet's durable sinks = ADRs (`/decide`), GitHub issues, session-log `[DECISION]` lines; do not duplicate rules.json content.

Each ends with a `## Durability` section naming zms-homelab as canonical and the deploy cache path.

### Task C4: Status table + PR

**Files (in the worktree):**
- Modify: `skills/README.md` — status table gains six rows (`Skill | Layered? | Public plugin`), and existing rows' public-version column updates to v3.1.0 (the table still references v1.0/v1.1 — stale).

- [ ] **Step 1: Update table, verify LF, commit, push, PR**

```bash
cd /y/dev/zms-homelab-wt-fleet-catchup
git add skills/ && git commit --signoff -m "feat(skills): fleet-layer catch-up — six epistemic-skills cores + LOCAL.md overlays (v3.1.0)"
git push -u origin feat/epistemic-fleet-catchup
gh pr create -R ZMS-Labs/zms-homelab --title "feat: epistemic-skills fleet-layer catch-up (helix, write-goal, outsource, continuity-verify, decision-ledger, open-questions)" --body "Brings skills/ to parity with public v3.1.0. Byte-identical cores + fleet LOCAL.md overlays + status table refresh. Worktree-isolated; primary working tree untouched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011L3kh3mNct92BFDrfWKD5G"
gh pr checks --watch && gh pr merge --squash
```

- [ ] **Step 2: Clean up worktree**

```bash
cd /y/dev/zms-homelab && git worktree remove /y/dev/zms-homelab-wt-fleet-catchup
```

### Task C5: Operator handoff notes

- [ ] **Step 1: Report these operator actions (cannot be done by the agent):**

1. `/plugin refresh` (or Claude Code restart) on each device to materialize the v3.1.0 plugin cache — the cache snapshot lags until refreshed (known: it sat at 2.5.0 after the 2.6.0 release).
2. Marketplace checkout `~/.claude/plugins/marketplaces/epistemic-skills` needs a `git pull` to the v3.1.0 commit.
3. Optional: an eval harness for open-questions (fixed `evals/` shape) as a follow-up PR.
