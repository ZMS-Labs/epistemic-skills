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
