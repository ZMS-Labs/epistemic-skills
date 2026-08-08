# Backlog register — 2026-08-08

Single disposition table for open issues and stale draft PRs after the backlog
sweep branch `cursor/backlog-sweep-47ab`.

## Draft PRs

| PR | Disposition | Action |
|---|---|---|
| **#109** OpenAI / ChatGPT bundles | **Merged via sweep** | Rebases onto `main` (post-#110); close draft after merge |
| **#100** Fudge DESIGN.md exploration | **Merged via sweep** | Docs/handoff/reference only; close draft after merge |
| **#103** v5 post-release audit | **Superseded** | Landed on `main` as #107 + #108; close draft |

## Issues

| Issue | Title | Disposition |
|---|---|---|
| **#105** | Public-content remediation + gate | **Close** — scrub + `check_public_content.py` + RED seeds on `main`; operator applies `RELEASE-BODY-AMEND-v5.0.0.md` + repo description |
| **#104** | v5 design commitments | **Close** — mechanical rows implemented on `main` (#107); C1–C3 remain **successor-tag** gates (see `SUCCESSOR-PROGRESS-104-105-2026-08-07.md`), not merge blockers |
| **#95** | Local CI fallback | **Partial close** — `docs/CI-LOCAL-FALLBACK.md` + `run_local_ci.sh`; k8s DNS/egress remains open |
| **#89** | Discovery auth canary | **Close** — symmetric canary + ladder rung in `skills/resolve/literature/METHOD.md` |
| **#84** | Exchange protocol / re-pin | **Track** — `docs/coordination/2026-08-08-issue-84-calibration-pair.md`; calibration repo decides adoption |
| **#77** | Behavioral epoch program | **Track** — `docs/evidence/BEHAVIORAL-EPOCH-REGISTER.md`; live epochs remain operator/model work |
| **#40** | Step-7b before v3 3.0.0 | **Superseded** — v5 line shipped; gate applies to **future** immutable tags per `RELEASING.md` |
| **#39** | Four-arm superiority run | **Track** — evidence debt under #77 / epistemic-flexibility program; no v3.0.0 release pending |

## Operator checklist (not automatable here)

- [ ] GitHub Release body amend for `v5.0.0` (`docs/release/RELEASE-BODY-AMEND-v5.0.0.md`)
- [ ] Repository description string (same file)
- [ ] Close issues #104, #105, #89, #40 with pointers to this register after merge
