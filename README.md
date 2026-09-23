<picture>
  <source media="(max-width: 600px)" srcset="docs/assets/epistemic-cover-mobile.svg">
  <img src="docs/assets/epistemic-cover.svg" alt="Epistemic Skills. Check the cause before naming it. Confirm the change before calling it done." width="1280">
</picture>

# Epistemic Skills

<!-- ZMS-ESTATE:BEGIN -->

Status: In development.

<!-- ZMS-ESTATE:END -->

Epistemic Skills is a set of written methods for AI agents, the AI tools that
carry out a multi-step task on their own. The methods help an agent investigate
a failure, compare options and check whether a change worked. *Epistemic* means
concerned with what we know and how we know it.

I'm [Zach Stern](https://github.com/SternOne). I don't want an agent guessing
when the answer can be looked up, or patching a symptom without finding the
cause. AI tools write the code. I decide what each project is for and check what
comes back. A Codex agent built version 7 and reviewed it at my direction, so
that review was not independent.

Each method defines when it helps, what useful result it returns, and when to stop.
No benefit has been shown yet: a comparison of versions 6 and 7 produced no
usable pairs of runs, and an earlier exploratory experiment of 72 trials across
four groups found no measurable difference between them. [Evidence and limits](#trust-evidence-and-known-limits)
links the receipts, and the [case study](https://zms-labs.github.io/showcase/case-studies/epistemic-skills/)
shows one recorded use.

**[Start here](#five-minute-start)** · **[Explore the methods](#choose-by-task)** · **[Read the handbook](https://github.com/ZMS-Labs/epistemic-skills/wiki)** · **[Understand the design](docs/handbook/pages/Design-Rationale.md)** · **[Contribute](CONTRIBUTING.md)**

[![Release](https://img.shields.io/github/v/release/ZMS-Labs/epistemic-skills?display_name=tag)](https://github.com/ZMS-Labs/epistemic-skills/releases/latest)
[![Checks](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/epistemic-flexibility.yml/badge.svg)](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/epistemic-flexibility.yml)
[![License](https://img.shields.io/github/license/ZMS-Labs/epistemic-skills)](LICENSE)

**Version 7.1.0.** The package contains **seventeen** skills: the `epistemic`
usage guide and **sixteen** disciplines. The [published release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.1.0)
includes versioned source, generated bundles, and verification receipts.
*Discipline* is this project's word for one of the methods.

## Routine work first

Fixing a typo does not need a review panel. A local, reversible, directly
checkable change can finish with an ordinary targeted check. Use a substantive
method when the task exposes a question that the ordinary check cannot settle.

| A familiar failure | The question a method brings into focus |
|---|---|
| An explanation sounds plausible, but the bug keeps returning. | What observation distinguishes this cause from the alternatives? |
| The configuration changed, but the application behaves the same. | Which file does the program actually load? |
| A design review produces agreement without testing assumptions. | What would change the decision, and who examined that possibility? |
| Work resumes with a confident but stale summary. | Which remembered facts still hold, and what evidence supports them? |
| Process consumes more effort than the task. | What is the smallest check that could change the next action? |

## See it in use

### Illustrative scenario: a service still uses an old setting after a change

This example explains the method; it is not a recorded performance result.

> The request: "Fix the setting and verify that the service is using it."

| Moment | Useful work |
|---|---|
| Investigate | Triage compares the file you edited with the file the running service actually loads. In this example it uses the systematic-debugging method from [Superpowers](https://github.com/obra/superpowers), an open-source skills library. A startup log shows the service reading a different configuration file. |
| Repair | The agent fixes the cause it found, within what the original request allowed. When the request was to fix the problem, finding the cause doesn't end the job. |
| Verify | Did It Land checks how the service behaves after a reload. If the request also asked for the setting to survive a restart, it checks that separately. |
| Explain | "I used Triage to find the configuration the service loads and Did It Land to confirm the change took effect. The service now reports the expected value after a restart." |

Did It Land tells the agent to report only what it observed. If it can't reach
the running service, it should say so and leave the result unconfirmed.

The handbook has [three worked examples](docs/handbook/pages/Workflow-Recipes.md).

### One recorded use

When the ZMS Labs showcase was first published in full, on 19 September 2026,
the Codex agent publishing it checked whether the site matched the files it was
meant to contain. The task record names the method as Did It Land. The site then
had 28 files, and its file list disagreed with 14 of them because of a
line-ending mismatch between the working copy and the files Git stored. After
the fix none disagreed, and all 28 files fetched from the live site matched
their committed fingerprints (SHA-256 hashes). It is one task, not a measured improvement. The
[case study](https://zms-labs.github.io/showcase/case-studies/epistemic-skills/#walkthrough)
walks through it, and `python scripts/replay_manifest_case.py`, run in a full
clone of the [showcase repository](https://github.com/ZMS-Labs/showcase),
replays the 14 and the 0 with only Python and Git.

## Five-minute start

1. Install one copy for your host, meaning the AI tool the skills run in, such as Claude Code or Codex. Use the [installation guide](docs/INSTALLATION.md), and don't install the skills twice, once through the tool's own plugin system and again as a generic skills install.
2. Reload the tool or start a new task. Check the tag's full skill count, and that the tool loaded the skills from the copy you installed.
3. Load `epistemic`, or call the method you need directly. Nothing else has to be set up first.
4. Give it a real task. Say what outcome you want, give it the context it needs, and keep the control over scope and permissions you would normally keep.

For a tool without its own plugin system:

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/v7.1.0/plugins/epistemic-skills/skills
```

Example request after installation:

> Use Perspective to check whether this migration plan has a rollback blind
> spot. Explain what, if anything, should change, then continue the review.

How you call a skill differs from tool to tool, so use the mechanism your tool
provides. The [start guide](docs/handbook/pages/Start-Here.md) covers loading a
method by name, how the agent says it used one, and what to do when your tool
lacks a feature.

## Using Epistemic Skills

The `epistemic` usage guide asks an agent to do five things: find the method
that fits, load it, apply it, say briefly that it did, and carry on with the
task. The agent doing the task stays in charge of it.

Triage uses Superpowers' systematic-debugging method when it is installed and
fits the problem, and its own procedure otherwise. You don't need Superpowers
to install or use this package.

Metacognate checks the agent's own reasoning. Perspective looks at a problem
from one chosen angle. Gauntlet collects several reviews and weighs them
into one verdict.

The [glossary](docs/handbook/pages/Glossary.md) explains the project's other terms.

## Choose by task

The groups below help you find a method. They aren't steps to run in order, and
one task can use more than one method.

<picture>
  <source media="(max-width: 600px)" srcset="docs/assets/method-map-mobile.svg">
  <img src="docs/assets/method-map.svg" alt="Method map in four groups. Frame the question: Metacognate, Recon, Resolve, Open Questions. Examine a decision: Perspective, Gauntlet. Verify an outcome: Health, Triage, Did It Land, Watch, Evidence-Locked UAT. Carry work forward: Write Goal, Decision Ledger, Manifest, Outsource, Context Audit. Epistemic is the shared usage guide." width="1280">
</picture>

### Seventeen-skill catalog

| When you need to… | Method, and what you should get |
|---|---|
| Learn how to use the set | [Epistemic](plugins/epistemic-skills/skills/epistemic/SKILL.md): the right method used, a short note that it was used, and the task carried on |
| Check the reasoning or approach | [Metacognate](plugins/epistemic-skills/skills/metacognate/SKILL.md): a correction or confirmation backed by evidence, or an uncertainty that matters |
| Map unfamiliar or contradictory territory | [Recon](plugins/epistemic-skills/skills/recon/SKILL.md): a clearer request, a map of the decisions ahead, or an assessment of an outside project |
| Settle a question with evidence | [Resolve](plugins/epistemic-skills/skills/resolve/SKILL.md): a worked derivation, a review of published research, or a small, limited test |
| Settle decisions that need the user's judgment | [Open Questions](plugins/epistemic-skills/skills/open-questions/SKILL.md): each question answered, or set aside on purpose |
| Look at one concern or blind spot | [Perspective](plugins/epistemic-skills/skills/perspective/SKILL.md): an insight, an improvement, a finding, or a stated uncertainty |
| Put an important proposal through several reviews | [Gauntlet](plugins/epistemic-skills/skills/gauntlet/SKILL.md): a reasoned verdict with the findings, the disagreements and the limits |
| Find out what state a running system is in | [Health](plugins/epistemic-skills/skills/health/SKILL.md): the observed status, including what couldn't be checked |
| Find the cause of a failure | [Triage](plugins/epistemic-skills/skills/triage/SKILL.md): evidence for the cause, then the fix and its check when the request already allowed them |
| Confirm a change took effect where it is used | [Did It Land](plugins/epistemic-skills/skills/did-it-land/SKILL.md): the effect as observed, and a note on whether it lasts through a reload or restart |
| Arrange for something to be watched between sessions | [Watch](plugins/epistemic-skills/skills/watch/SKILL.md): a tested outside monitor and its alert; the skill itself does not stay awake |
| Decide whether a user-facing result is acceptable | [Evidence-Locked UAT](plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md) (user acceptance testing): what you expect to see, what would show it failed, the evidence, and an accept or reject verdict |
| Write down or start a lasting goal | [Write Goal](plugins/epistemic-skills/skills/write-goal/SKILL.md): a definition of done, fitted to your tool and to what you asked for |
| Record a decision, or recheck old notes when picking work back up | [Decision Ledger](plugins/epistemic-skills/skills/decision-ledger/SKILL.md): a record you already have that covers it, or the smallest new record that is missing |
| Run a long job with a formal record of who authorized it and what it may touch | [Manifest](plugins/epistemic-skills/skills/manifest/SKILL.md): the job's state kept in that record, which the project calls custody, under rules you opt into |
| Hand work to someone or something outside this session | [Outsource](plugins/epistemic-skills/skills/outsource/SKILL.md): a handoff the recipient can read on its own, a checked result when delegated work comes back, or a completed handover when ownership itself moves — acceptance on record and the giver divested |
| Sort out conflicting or overloaded instructions | [Context Audit](plugins/epistemic-skills/skills/context-audit/SKILL.md): a diagnosis of the instructions and proposed changes with a clear scope |

These summaries help you choose. Each method's `SKILL.md` is its canonical text,
meaning the one agreed version: it sets when the method applies, its limits and
its steps. The links above go to the development branch, which can include
changes made after v7.1.0; the [v7.1.0 tag](https://github.com/ZMS-Labs/epistemic-skills/tree/v7.1.0/plugins/epistemic-skills/skills)
holds the released text. The [handbook catalog](docs/handbook/pages/Skill-Catalog.md)
adds examples and comparisons for each method.

## Why the design looks this way

| Design choice | Reason | Tradeoff |
|---|---|---|
| One source for every method | Every tool's package is built from the same method files. | Each package still has to be checked against that source. |
| Each method says when to start and when to stop | Effort goes where it can change what happens next. | An agent still has to notice the moment and act on it. |
| Single-angle review and multi-review are two methods | The size of the review can match the question. | You need clear guidance on which one fits. |
| The agent says briefly which method it used | You can see what each method contributed. | Naming a method proves nothing on its own. |
| Repeatable automated tests, with their limits stated | Test what a machine can check without overstating how agents behave. | Important questions still need observed use or someone's judgment. |
| Reuse the decisions and records you already have | Keep continuity without copying records that already do the job, such as decision records (ADRs) and task notes. | Someone has to judge whether an old record is still good enough and current. |

The [design rationale](docs/handbook/pages/Design-Rationale.md) explains each
choice in more depth.

## Installation and compatibility

The methods use the [Agent Skills format](https://agentskills.io/specification).
The repository has packages for Claude Code, Codex, Cursor, Gemini CLI,
Antigravity, Kimi and ZCode, a generic install for other tools that read Agent
Skills, and fixed bundles to upload to ChatGPT and OpenAI.

Pick your tool in the [installation guide](docs/INSTALLATION.md). Install from a
release tag, which never changes, keep any customizations you have made, reload,
and check which copy the tool actually loaded.

The tools were not all checked to the same depth. For v7, the
[host coverage report](docs/release/v7-host-coverage.md) records:

| Tool | How far it was checked for v7 |
|---|---|
| Codex CLI | A live test saw it find all 17 skills. Whether the model then used them was not tested. |
| Codex desktop app | It showed an older installed copy, not v7. It offered tools for setting goals, but no goal was tested. |
| Claude Code | Source files and simulated tests only; no live model run. |
| Cursor, Antigravity and Kimi | Installed version observed; delivery of the methods to the model not tested. |
| Gemini CLI | Installed version and extension settings observed; delivery to the model not tested. |
| Cursor CLI | Not found on the test machine; covered only by the tests of Manifest's add-on scripts. |
| ZCode | Not available when the check ran. |
| ChatGPT and OpenAI bundles | Packaging only. |
| Other Agent Skills tools (generic install) | A fallback install path; not tested. |

## Architecture and source policy

```text
plugins/epistemic-skills/
├── skills/<name>/SKILL.md    canonical skill cores (seventeen)
├── reference/               shared methods and lens library
├── agents/                  Gauntlet role definitions
└── contracts/               schemas, validators, and runtime mechanics

docs/handbook/pages/         current explanatory handbook
docs/wiki-updates/           historical release handbook snapshots
docs/release/                versioned evidence and release records
packaging/                  generated host bundles
.github/                    checks and publication workflows
```

A release is defined by its tag, which never changes. The README and handbook on
the main branch explain the current state and can change after a release, and so
can the skill files: main can hold skill changes that no release contains yet.

For contributors, the [maintainer guide](docs/MAINTAINING.md) says where to make
each kind of change, which files are generated from it, and which checks to run.

## Trust, evidence, and known limits

| Claim | Evidence and boundary |
|---|---|
| v7.1.0 was published from the exact commit that was checked | The [publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/publication-receipt.json) records the merge commit, the dispatched exact-commit runs, the tag control with disarmed-and-restored protection, and the seeded-probe rejections. |
| Required checks passed on the v7.1.0 release candidate | The [hosted gate receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/exact-gates.json) records the dispatched gate workflows, CodeQL, and the required Ubuntu custody job passing on that commit; the macOS custody diagnostic failed the two known case-insensitive assertions and is disclosed there, not gating. |
| The ZCode agent that built v7.1.0 also reviewed and approved it | I designated it as the reviewer ([review receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/designated-review.json)). It reviewed from the same context it built the release in, so the review was neither independent nor blind. |
| v7 was published from the exact commit that was checked | The [publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/publication-receipt.json) records that commit, the required checks, the tag, the release files and the handbook version. |
| Required checks passed on the v7.0.0 release candidate | The [hosted gate receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/exact-gates.json) records 10 required jobs and 155 steps passing on that commit: automated tests, security scans, packaging checks and CodeQL, GitHub's code scanner. |
| The Codex agent that built v7 also reviewed and approved it | I designated it as the reviewer ([review receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/designated-review.json)). It reviewed from the same context it built the release in, so the review was neither independent nor blind. |
| Host support has observed limits | The [coverage report](docs/release/v7-host-coverage.md) records how far each tool was checked; see the table under [Installation and compatibility](#installation-and-compatibility). |
| Comparative superiority is unproved | The [v6 to v7 comparison](plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-09-18-v7/RESULTS.md) stopped after its first run because the test environment loaded outside skills and blocked some commands, so there are no matched v6 and v7 runs to compare. An earlier exploratory experiment ran 72 blinded trials across four groups, with its main prediction registered in advance, and [found no measurable difference between the groups](plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-08-04-four-arm/RESULTS.md). |
| Some methods have no test of when they should be used | On the development branch, not yet in a release, eight methods carry a note that the rule for when to use them is argued from the design, with no shipped test that checks it: Epistemic, Metacognate, Perspective, Did It Land, Health, Triage, Watch and Manifest. |

One known problem is still open ([issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162)).
On a Mac, or any other non-Windows system where file names ignore upper and
lower case, Manifest can treat `Secrets/` and `secrets/` as two different
places while the system treats them as one. A job told to stay out of one
spelling can then change the same files through the other without Manifest
noticing. Don't rely on Manifest's keep-out rules or its file-name distinctions
there. The failing test is kept in the release evidence.

Earlier failures and null results stay available in the
[evidence guide](docs/handbook/pages/Testing-and-Evaluations.md).

## Developing and contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the
[maintainer guide](docs/MAINTAINING.md). Change the canonical source, run the
checks that fit what you are claiming, keep historical evidence, and keep private
local output out of the public tree. Each commit needs a DCO (Developer
Certificate of Origin) sign-off: a `Signed-off-by` line that matches the
commit's author, added with `git commit --signoff`.

```bash
# Discover and verify canonical skill metadata
python .github/scripts/sync_skill_surfaces.py --check

# Check the current handbook and public documentation
python docs/handbook/stage_wiki.py --check
python .github/scripts/check_public_content.py
```

These are the first checks to run, not the full release gate. The
[automated check coverage](docs/actions-tier.md) and [RELEASING.md](RELEASING.md)
describe the rest.

## Explore further

- Using it: [Worked examples](docs/handbook/pages/Workflow-Recipes.md) · [Skill catalog](docs/handbook/pages/Skill-Catalog.md) · [Troubleshooting](docs/handbook/pages/FAQ-and-Troubleshooting.md)
- Understanding it: [How the pieces fit](docs/handbook/pages/How-the-Pieces-Fit.md) · [Design rationale](docs/handbook/pages/Design-Rationale.md) · [Glossary](docs/handbook/pages/Glossary.md)
- Maintaining it: [Maintainer guide](docs/MAINTAINING.md) · [Documentation map](docs/README.md) · [Testing and evidence](docs/handbook/pages/Testing-and-Evaluations.md)

## License and support

[GPL-3.0-or-later](LICENSE). Bundled documentation typography retains its
[SIL Open Font License](docs/assets/fonts/OFL.txt).

[Releases](https://github.com/ZMS-Labs/epistemic-skills/releases) · [Issues and questions](https://github.com/ZMS-Labs/epistemic-skills/issues) · [Handbook](https://github.com/ZMS-Labs/epistemic-skills/wiki)
