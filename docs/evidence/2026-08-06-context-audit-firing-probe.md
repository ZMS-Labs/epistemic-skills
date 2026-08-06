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

## Outcome — round 1: INCONCLUSIVE (control validated the wrong mechanism)

Observed 2026-08-06. **No session restart was required** — the harness hot-loaded
the three probes into the live skill listing as soon as the files existed. The
plan's restart gate was unnecessary.

| probe | escapes | path | predicted | observed |
|---|---|---|---|---|
| probe-charlie (control) | 0 | local (`~/.claude/skills/`) | renders | **RENDERS** |
| probe-bravo | 1 | local | renders | **RENDERS** |
| probe-alpha | 2 | local | blank | **RENDERS** |
| context-audit (production) | 2 | **plugin** | — | **BLANK** |

Validity condition: **MET for the local loader, NOT MET for the case under test.**

### Why this is inconclusive rather than a refutation

The three probes are **local** skills. `context-audit` is a **plugin** skill.
`probe-charlie` proves the *local* loader renders descriptions; it does not prove
the *plugin* loader renders a description carrying two escapes. The control
validated a different mechanism from the one production uses.

This is the same failure this estate has already paid for once: `Path.symlink_to()`
created a real symlink and the control passed, while all 18 production projection
links were Windows junctions, for which `is_symlink()` returns False. A control is
only as good as its match to the production path.

No free discriminating observation exists: a scan of every installed plugin
(`C:/Users/zachs/.claude/plugins/**/skills/*/SKILL.md`) found **`context-audit` is
the only plugin skill anywhere with two escapes**; all 11 others with any escape
have exactly one. There is nothing to compare it against.

### Established regardless

1. The harness hot-loads skills; observation does not require a restart.
2. The local loader unescapes `''` correctly — `probe-alpha` renders
   `document's` and `task's`.
3. The apostrophe hypothesis remains **untested on the plugin path**.

### What would decide it

A probe with two escapes placed on the **plugin** path — the same source
`context-audit` loads from — and observed in the live listing. Requires writing
into installed plugin files, which is an operator decision.
