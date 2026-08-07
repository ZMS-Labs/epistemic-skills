# context-audit Firing-Defect Release Gate — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine, by controlled observation rather than by reading loader source, why `epistemic-skills:context-audit` renders with no description in the live skill listing — then fix it and make the failure class impossible to reintroduce.

**Architecture:** Three disposable probe skills are authored with descriptions differing in exactly one variable (count of YAML `''` apostrophe escapes: 0, 1, 2). A single session restart renders all three at once. A zero-escape probe acts as the **positive control**: if it fails to render, the probe apparatus itself is invalid and no conclusion may be drawn. Predictions are written down *before* observation so the result cannot be rationalised after the fact.

**Tech Stack:** Markdown SKILL.md files with YAML frontmatter; Python 3.11 stdlib for the guard check; the repo's existing `.github/scripts/` check convention and `epistemic-flexibility.yml` CI workflow.

## Global Constraints

- **Portable frontmatter only.** Exactly six keys are legal in a shipped `SKILL.md`: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Anything else hard-fails packaging.
- **No hostnames, IPs, credentials, or share paths in any `SKILL.md`.** Site specifics belong in `LOCAL.md`.
- **Windows/MSYS2 shell.** Set `PYTHONIOENCODING=utf-8` before running any Python that prints non-ASCII, or emoji/em-dash output raises `UnicodeEncodeError`.
- **`cmd | tail` makes `$?` the pipe's exit status, not the script's.** Capture exit codes before piping.
- **Probe skills live under `<user-home>/.claude/skills/`.** This is Claude's own config directory and is the one C:-drive write permitted by RULE-PC-004. All probes are deleted in Task 4.
- **No check ships on its author's reading of its own green** (ADR-184). Every check in this plan is proven RED against a seeded defect before its green is trusted.

## File Structure

| File | Responsibility | Lifetime |
|---|---|---|
| `<user-home>/.claude/skills/probe-charlie\SKILL.md` | positive control — 0 apostrophe escapes; proves the probe apparatus renders descriptions at all | disposable |
| `<user-home>/.claude/skills/probe-bravo\SKILL.md` | 1 apostrophe escape — mirrors `decision-ledger`, which renders | disposable |
| `<user-home>/.claude/skills/probe-alpha\SKILL.md` | 2 apostrophe escapes — mirrors `context-audit`, which does not render | disposable |
| `docs/evidence/2026-08-06-context-audit-firing-probe.md` | predictions written before observation; results written after | permanent |
| `plugins/epistemic-skills/skills/context-audit/SKILL.md` | the fix, if the hypothesis is confirmed | permanent |
| `.github/scripts/check_description_renders.py` | guard preventing reintroduction | permanent |
| `.github/workflows/epistemic-flexibility.yml` | CI wiring for the guard | permanent |

---

### Task 1: Record predictions before observing anything

**Files:**
- Create: `docs/evidence/2026-08-06-context-audit-firing-probe.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a committed prediction record that Task 3 reads. Committing *before* observation is what makes the result falsifiable rather than narrated.

- [ ] **Step 1: Write the prediction record**

Create `docs/evidence/2026-08-06-context-audit-firing-probe.md`:

```markdown
# context-audit firing probe — predictions

**Written before any observation, 2026-08-06.**

## Question

Why does `epistemic-skills:context-audit` render with no description in the live
skill listing while its `SKILL.md` carries a correct one?

## Already eliminated (measured 2026-08-06)

| hypothesis | why it is dead |
|---|---|
| file content wrong | dev checkout and installed 4.1.0 cache both carry a correct description |
| YAML quoting style | open-questions, recon, resolve, decision-ledger are also single-quoted and render |
| description length | open-questions (832 chars) and recon (878) are longer and render; context-audit is 762 |
| colons in the value | recon has 2, resolve and decision-ledger have 1; all render |
| shadowing SKILL.md | only cache, marketplace, and dev copies exist, all legitimate |
| skillOverrides | settings.local.json contains only {"goal": "off"} |

## Surviving hypothesis

`context-audit` is the only skill whose description contains **two** YAML `''`
apostrophe escapes (`document''s`, `task''s`). `decision-ledger` contains exactly
one and renders. A loader that unescapes the first and mishandles the second
produces exactly this symptom.

## Predictions

| probe | `''` escapes | prediction |
|---|---|---|
| `probe-charlie` | 0 | description **renders** |
| `probe-bravo` | 1 | description **renders** |
| `probe-alpha` | 2 | description **does NOT render** |

## Validity condition (positive control)

`probe-charlie` is the control. **If `probe-charlie` does not render its
description, the probe apparatus is invalid and NO conclusion may be drawn from
`probe-alpha` or `probe-bravo`.** A blank `probe-alpha` would then be
indistinguishable from "locally-authored probe skills never show descriptions."

This condition exists because this estate has already been burned once by a
positive control that passed while production was broken: `Path.symlink_to()`
created a real symlink, but all 18 production projection links were Windows
junctions, for which `is_symlink()` returns False.

## Outcome

(To be filled in by Task 3. Do not edit anything above this line.)
```

- [ ] **Step 2: Commit the predictions before authoring any probe**

```bash
cd /y/dev/epistemic-skills
git add docs/evidence/2026-08-06-context-audit-firing-probe.md
git commit -m "test: record context-audit firing-probe predictions before observing

Predictions and the positive-control validity condition are committed before any
probe exists, so the result cannot be rationalised after the fact."
```

---

### Task 2: Author the three probes

**Files:**
- Create: `<user-home>/.claude/skills/probe-charlie\SKILL.md`
- Create: `<user-home>/.claude/skills/probe-bravo\SKILL.md`
- Create: `<user-home>/.claude/skills/probe-alpha\SKILL.md`

**Interfaces:**
- Consumes: the predictions from Task 1.
- Produces: three skills whose descriptions differ in exactly one variable. Task 3 reads their rendering.

The three descriptions are matched for length (within ~40 characters) and are
identical in structure, quoting, punctuation, and em-dash usage. **Only the count
of `''` escapes varies.** Any other difference invalidates the experiment.

- [ ] **Step 1: Write the positive control (0 escapes)**

Create `<user-home>/.claude/skills/probe-charlie\SKILL.md`:

```markdown
---
name: probe-charlie
description: 'Disposable diagnostic probe charlie — this description contains zero YAML apostrophe escapes and exists only to prove that a locally authored skill renders its description in the live listing at all. It is padded to approximately the same length as the description under investigation so that length is held constant across all three probes in this experiment. Do NOT fire this skill for any real work, do NOT route to it, and do NOT treat it as a capability; it is deleted as soon as the observation is recorded.'
---

# probe-charlie

Positive control for the context-audit firing probe. Zero apostrophe escapes.

If this probe's description does not render in the live skill listing, the probe
apparatus is invalid and no conclusion may be drawn from probe-alpha or
probe-bravo.

Delete after observation.
```

- [ ] **Step 2: Write the one-escape probe**

Create `<user-home>/.claude/skills/probe-bravo\SKILL.md`:

```markdown
---
name: probe-bravo
description: 'Disposable diagnostic probe bravo — this description contains exactly one YAML apostrophe escape, here in the phrase the gauntlet''s telemetry, matching the pattern of a shipped skill that renders correctly today. It is padded to approximately the same length as the description under investigation so that length is held constant across all three probes. Do NOT fire this skill for any real work, do NOT route to it, and do NOT treat it as a capability; it is deleted as soon as the observation is recorded.'
---

# probe-bravo

One apostrophe escape. Mirrors decision-ledger, which renders correctly.

Delete after observation.
```

- [ ] **Step 3: Write the two-escape probe**

Create `<user-home>/.claude/skills/probe-alpha\SKILL.md`:

```markdown
---
name: probe-alpha
description: 'Disposable diagnostic probe alpha — this description contains two YAML apostrophe escapes, one here in the phrase a document''s prose quality and one here in the phrase one task''s output, matching the pattern of the skill under investigation. It is padded to approximately the same length as that description so that length is held constant across all three probes. Do NOT fire this skill for any real work, do NOT route to it, and do NOT treat it as a capability; it is deleted as soon as the observation is recorded.'
---

# probe-alpha

Two apostrophe escapes. Mirrors context-audit, which does not render.

Delete after observation.
```

- [ ] **Step 4: Verify the probes differ in exactly one variable**

Run:

```bash
cd "<user-home>/.claude/skills" && export PYTHONIOENCODING=utf-8 && python -c "
import re,pathlib
for n in ['probe-alpha','probe-bravo','probe-charlie']:
    t=pathlib.Path(n,'SKILL.md').read_text(encoding='utf-8')
    d=re.search(r'description:\s*(.*)',re.match(r'---\n(.*?)\n---',t,re.S).group(1),re.S).group(1)
    print(f'{n:15} len={len(d):4} escapes={d.count(chr(39)*2)} quote={d[:1]} emdash={d.count(chr(8212))} colons={d.count(\":\")}')
"
```

Expected: all three report `quote='`, `colons=0`, `emdash=1`, lengths within ~40
of each other, and `escapes=` 2, 1, 0 respectively.

**If any variable other than `escapes` differs, fix the descriptions and re-run
before proceeding.** A confounded experiment yields no information.

---

### Task 3: Observe and record

**Files:**
- Modify: `docs/evidence/2026-08-06-context-audit-firing-probe.md` (Outcome section only)

**Interfaces:**
- Consumes: the three probes from Task 2 and the predictions from Task 1.
- Produces: a confirmed or refuted hypothesis, which decides whether Task 4 or Task 5 runs.

- [ ] **Step 1: Restart the session**

This is a manual operator gate. The skill listing is assembled at session start;
there is no in-session reload. Ask the operator to restart Claude Code, then
continue in the new session.

- [ ] **Step 2: Read the live skill listing and record all four observations**

In the new session, inspect the available-skills listing and record, verbatim,
whether a description appears for each of:

- `probe-charlie` (control)
- `probe-bravo`
- `probe-alpha`
- `epistemic-skills:context-audit`

- [ ] **Step 3: Check the validity condition FIRST**

If `probe-charlie` shows **no** description: the apparatus is invalid. Write
`APPARATUS INVALID` into the Outcome section, stop, and escalate — do not proceed
to Task 4 or Task 5, and do not conclude anything about apostrophes.

- [ ] **Step 4: Write the outcome**

Append to the Outcome section of
`docs/evidence/2026-08-06-context-audit-firing-probe.md`:

```markdown
## Outcome

Observed <DATE>, session restarted.

| probe | escapes | predicted | observed |
|---|---|---|---|
| probe-charlie (control) | 0 | renders | <RENDERS / BLANK> |
| probe-bravo | 1 | renders | <RENDERS / BLANK> |
| probe-alpha | 2 | blank | <RENDERS / BLANK> |
| context-audit (production) | 2 | blank | <RENDERS / BLANK> |

Validity condition: <MET / NOT MET>

Verdict: <CONFIRMED — two escapes break description rendering /
          REFUTED — escapes are not the cause /
          APPARATUS INVALID>
```

- [ ] **Step 5: Commit the outcome**

```bash
cd /y/dev/epistemic-skills
git add docs/evidence/2026-08-06-context-audit-firing-probe.md
git commit -m "test: record context-audit firing-probe outcome"
```

---

### Task 4: If CONFIRMED — fix and guard

Run this task **only** if Task 3's verdict is CONFIRMED.

**Files:**
- Modify: `plugins/epistemic-skills/skills/context-audit/SKILL.md` (description line only)
- Create: `.github/scripts/check_description_renders.py`
- Modify: `.github/workflows/epistemic-flexibility.yml`

**Interfaces:**
- Consumes: the CONFIRMED verdict.
- Produces: `check_description_renders.py`, exit 0 clean / exit 1 with one named defect per line — matching the convention of `check_no_phantom_skills.py`.

- [ ] **Step 1: Write the guard, RED first**

Create `.github/scripts/check_description_renders.py`:

```python
#!/usr/bin/env python3
"""Fail when a SKILL.md description uses a construct that breaks rendering.

A skill whose description does not render in the harness listing cannot fire on
description match — it is, functionally, not installed. Measured 2026-08-06:
context-audit carried two YAML '' apostrophe escapes and rendered blank, while
decision-ledger carried one and rendered correctly. See
docs/evidence/2026-08-06-context-audit-firing-probe.md for the controlled
observation, including the positive control that validates it.

The rule is deliberately stricter than the measured threshold: ZERO apostrophe
escapes, not "at most one". The boundary between one and two is an artifact of
someone else's parser and may move without notice; zero is stable and costs
nothing, because every affected phrase can be reworded.

Stdlib only. Exit 0 clean, 1 with a named defect per line.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO / "plugins" / "epistemic-skills" / "skills"


def description_of(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    match = re.search(r"^description:(.*?)(?=^\w+:|\Z)", text[3:end], re.S | re.M)
    return match.group(1) if match else ""


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 2

    defects: list[str] = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        description = description_of(skill_md.read_text(encoding="utf-8"))
        escapes = description.count("''")
        if escapes:
            defects.append(
                f"{skill_md.relative_to(REPO)}: description contains {escapes} "
                f"YAML apostrophe escape(s); reword to remove the possessive. "
                f"Two escapes measured to blank the listing entry entirely."
            )

    if defects:
        for defect in defects:
            print(f"description-render: {defect}", file=sys.stderr)
        print(f"\n{len(defects)} description(s) risk not rendering", file=sys.stderr)
        return 1

    count = len(list(SKILLS_DIR.glob("*/SKILL.md")))
    print(f"all {count} descriptions free of apostrophe escapes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the guard and verify it FAILS against the current tree**

Run:

```bash
cd /y/dev/epistemic-skills && export PYTHONIOENCODING=utf-8 && python .github/scripts/check_description_renders.py; echo "EXIT=$?"
```

Expected: `EXIT=1`, with `context-audit` reported for 2 escapes and
`decision-ledger` reported for 1.

**If this exits 0, the guard is broken — it must fail before it is trusted.** Do
not proceed until it reports both files.

- [ ] **Step 3: Fix `context-audit`'s description**

In `plugins/epistemic-skills/skills/context-audit/SKILL.md`, replace both
possessives on the `description:` line:

- `a single document''s prose quality` → `the prose quality of one document`
- `one specific task''s output` → `the output of one specific task`

Change nothing else on the line. Leave the body untouched.

- [ ] **Step 4: Fix `decision-ledger`'s description**

In `plugins/epistemic-skills/skills/decision-ledger/SKILL.md`, replace:

- `that is gauntlet''s runs/ledger.jsonl` → `that is the gauntlet runs/ledger.jsonl`

It renders correctly today, but the one-versus-two boundary belongs to a parser
we do not control. Zero is the stable rule.

- [ ] **Step 5: Run the guard and verify it PASSES**

Run:

```bash
cd /y/dev/epistemic-skills && export PYTHONIOENCODING=utf-8 && python .github/scripts/check_description_renders.py; echo "EXIT=$?"
```

Expected: `EXIT=0`, `all 11 descriptions free of apostrophe escapes`.

- [ ] **Step 6: Verify no other check regressed**

Run:

```bash
cd /y/dev/epistemic-skills && export PYTHONIOENCODING=utf-8 && \
python .github/scripts/check_skill_inventory.py; echo "INVENTORY=$?"; \
python .github/scripts/sync_skill_surfaces.py --check; echo "SURFACES=$?"; \
python .github/scripts/check_no_phantom_skills.py; echo "PHANTOM=$?"
```

Expected: all three report `=0`.

- [ ] **Step 7: Wire the guard into CI**

In `.github/workflows/epistemic-flexibility.yml`, after the
`No phantom skill references in routing surfaces` step, add:

```yaml
      - name: Descriptions render in the skill listing
        run: python .github/scripts/check_description_renders.py
```

And add to the `Compile new Python` list, after
`.github/scripts/check_no_phantom_skills.py \`:

```yaml
            .github/scripts/check_description_renders.py \
```

- [ ] **Step 8: Commit**

```bash
cd /y/dev/epistemic-skills
git add plugins/epistemic-skills/skills/context-audit/SKILL.md \
        plugins/epistemic-skills/skills/decision-ledger/SKILL.md \
        .github/scripts/check_description_renders.py \
        .github/workflows/epistemic-flexibility.yml
git commit -m "fix: context-audit description never rendered in the skill listing

Measured by controlled observation, not by reading the loader: three probe skills
differing only in YAML apostrophe-escape count, one session restart, with a
zero-escape positive control validating the apparatus. Two escapes blank the
listing entry; one renders. Evidence and predictions (committed before observing)
in docs/evidence/2026-08-06-context-audit-firing-probe.md.

A skill with no listed description cannot fire on description match, so
context-audit has been functionally uninstalled since it shipped.

Guard bans apostrophe escapes outright rather than allowing one: the one-versus-
two boundary belongs to a parser we do not control. Proven RED against both
affected files before the fix."
```

- [ ] **Step 9: Verify the fix by observation, not by the guard's green**

The guard proves the *text* changed. It does not prove the listing renders.
Restart the session again and confirm `epistemic-skills:context-audit` now shows
its description. Record the result in the evidence file and commit.

This step is not optional. The guard's green and the listing's behaviour are two
different claims, and this estate's entire failure pattern is promoting the first
into the second.

---

### Task 5: If REFUTED — escalate with the eliminated set

Run this task **only** if Task 3's verdict is REFUTED.

**Files:**
- Modify: `docs/evidence/2026-08-06-context-audit-firing-probe.md`
- Modify: `docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md`

**Interfaces:**
- Consumes: the REFUTED verdict.
- Produces: an updated release-gate section naming seven eliminated hypotheses, and a HOLD on v5.0.0.

- [ ] **Step 1: Record the refutation and what remains**

Append to the evidence file the full eliminated set (now seven hypotheses) and
state plainly that the cause is unknown.

- [ ] **Step 2: Place v5.0.0 on hold in the spec**

In the "Blocking requirement" section of the design spec, replace the leading
hypothesis paragraph with a HOLD notice: the firing surface fails in a way seven
hypotheses do not explain, and the v5.0.0 architecture assumes descriptions are
the firing surface. Do not begin `health` until this is understood.

- [ ] **Step 3: Commit and stop**

```bash
cd /y/dev/epistemic-skills
git add docs/evidence/2026-08-06-context-audit-firing-probe.md \
        docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md
git commit -m "test: apostrophe hypothesis REFUTED; v5.0.0 on hold

Seven hypotheses eliminated and the firing surface still fails. The v5.0.0 design
assumes descriptions are the firing surface, so no further work proceeds until
this is understood."
```

---

### Task 6: Clean up the probes

Runs after Task 4 or Task 5, whichever executed.

**Files:**
- Delete: `<user-home>/.claude/skills/probe-alpha\`, `probe-bravo\`, `probe-charlie\`

**Interfaces:**
- Consumes: a completed Task 4 or Task 5.
- Produces: a clean skill listing with no diagnostic artifacts.

- [ ] **Step 1: Remove the three probe directories**

Deletion is a consented act. Ask the operator to confirm, then remove the three
directories. They contain nothing but the probe files authored in Task 2, and the
evidence they produced is already committed to the repo.

- [ ] **Step 2: Confirm they are gone from the listing**

At the next session start, verify no `probe-` skills appear. If any remain,
the deletion did not take effect — report it rather than assuming.

---

## Self-Review

**Spec coverage.** This plan implements step 0 of the design spec's sequencing —
the `context-audit` release gate — and nothing else. Steps 1 through 7 of that
sequencing (`health`, `metacognate`, deleting the router and helix, `triage`,
`did-it-land`, `watch`) are deliberately out of scope and require their own plans,
each gated on this one clearing. This is stated in the spec itself: nothing else in
v5.0.0 is worth building until the firing surface is proven sound.

**Placeholder scan.** No TBD, TODO, or "handle edge cases". Every file has exact
content. The `<RENDERS / BLANK>` and `<DATE>` markers in Task 3 Step 4 are
observation slots to be filled at runtime, not deferred design decisions — the
table structure and every alternative value are fully specified.

**Type consistency.** `check_description_renders.py` follows the exact structure of
the existing `check_no_phantom_skills.py`: `REPO`/`SKILLS_DIR` resolved via
`parents[2]`, a `description_of` helper matching that file's
`frontmatter_description`, a `defects: list[str]`, one named defect per stderr
line, exit 0/1/2. The CI step name and `Compile new Python` entry match the
workflow's existing formatting.

**Branch coverage.** All three outcomes of Task 3 are handled: CONFIRMED → Task 4,
REFUTED → Task 5, APPARATUS INVALID → stop at Task 3 Step 3. Task 6 runs after
either terminal branch.
