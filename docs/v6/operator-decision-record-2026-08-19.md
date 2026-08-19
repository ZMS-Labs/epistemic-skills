# Operator decision record — v6 program, 2026-08-19

Provenance: live operator rulings given in the session that produced the
rc4 BUILD freeze and the fourth independent Gauntlet panel. Four rulings,
recorded here in full wording. This file is the successor to
`operator-decision-record-2026-08-18.md` (D1–D15, echo-certified), which
lives on the v6 candidate branch `claude/v6-candidate-rc2`; this record
lands on `main` instead, for a reason the last section explains.

Status: recorded, not yet echo-certified. The 2026-08-18 record was
ratified by an exact SHA-bearing echo under D14. These four rulings were
given as direct answers to posed decisions rather than through that
protocol, and the fourth Gauntlet panel flagged exactly that gap
(finding R4-NF5, P4: the rulings were recorded by the party they
authorize). The operator discharges it by confirming these four in the
acceptance record, or by echo-certifying this file under D14.

## Decisions

- **D16 (rc4 repair shape).** The repair of the rc3 NO-GO's findings
  ships as **rc4, a full C/C+1 re-freeze**: a new candidate commit
  carries the ledger byte-restoration (R3-NF1) and the prose/derivation
  repairs (R3-NF2/NF3/NF4 plus the P4 sweep NF5–NF8), and the packet is
  regenerated at the new candidate and committed as its child. A
  sanctioned repair commit without a re-freeze was declined: several of
  those repairs edit digest-inventoried sources, which the RESTAMP
  discipline refuses to carry under a stale candidate SHA. Recorded
  durably as ledger entry `v6-rc4-repair-shape-full-refreeze-20260819-20`.
  Executed: candidate `7408a462b413d0ab41a08de1d37a10b9cdf2a6ea`, freeze
  `e46c2486535cf847dde05562399fd534f49b85d1`.

- **D17 (first lineage-cap extension).** The three-panel lineage cap,
  EXHAUSTED at the rc3 verdict, is **extended by exactly one panel**,
  scoped to a delta-plus-blast-radius review of the rc4 repair by a fresh
  seat, under the same mode as the rc3 panel. Opening a new lineage was
  declined: all ten substantive rc2 rulings were closed, the rc4 delta is
  narrow, and a new lineage would re-litigate closed rulings and discard
  the standing evidence chain the revision-loop doctrine preserves.
  Recorded durably as ledger entry
  `v6-lineage-panel-cap-extension-20260819-21`. **Spent** by the fourth
  panel's verdict (`docs/gauntlet-runs/es-v6-rc4-delta-review-2026-08-19/`
  on branch `claude/es-v6-rc4-delta-review`, NO-GO against the rc4
  candidate on one new P1).

- **D18 (R4-NF1 repair shape — the DCO red).** The fourth panel found
  that six commits in freeze PR #197's range carry no `Signed-off-by`
  line, so the DCO gating job lands red the moment the PR is marked
  ready. The repair is an **amendment to `check_dco.py` on `main`**, in
  two limbs:

  1. **Merge commits are exempt.** A merge commit joins two histories;
     its content is the mechanical result of that join and its author is
     whoever ran `git merge`. The DCO certifies authored contributions.
     This is the same default GitHub's own DCO app applies. Recorded
     limit, not hidden: content a merge commit genuinely does author —
     conflict resolutions — is uncertified by this exemption. Merges are
     to be kept clean, and `git merge --signoff` used where the sign-off
     matters.
  2. **Five inherited commits are attested by exact SHA.** The five
     unsigned commits authored by the repository owner's Cursor Agent
     tool run are certified under the Developer Certificate of Origin by
     the owner, who ran the tool against their own repository. The
     exemption is keyed on the full 40-hex SHA, which is content-bound:
     it certifies exactly those commits and nothing else, and any amend
     or rebase yields a different SHA that fails closed. **The list is
     closed.** A future unsigned commit is a defect to fix with
     `git commit --amend --signoff`, never a new entry.

  Declined alternatives: a recorded waiver leaving the job red (it would
  contradict `RELEASING.md` gate 5 and acceptance-procedure item 5 —
  precisely the accommodation this program exists to prevent), and
  re-parenting the candidate branch so the unsigned commits leave the PR
  range (it would cost a fifth candidate, new coordinates, and another
  panel to fix a policy-surface problem). History was not rewritten: the
  five SHAs are subjects and ancestors of verdicts of record, and
  rewriting them would invalidate three arbitrations and the pushed pin
  tags.

  Verified before proposal: `dco.yml` runs on `pull_request_target` and
  checks out the PR's **base** revision, so `main`'s copy of the script
  is what executes; PR #197's diff does not touch `check_dco.py`, so a
  main-side amendment survives the eventual promotion merge (proven by
  simulation, not assumed); and the amended checker takes PR #197 from
  six unsigned commits to zero against its live commit list.

- **D19 (second lineage-cap extension, narrow).** The cap is **extended
  by one further panel**, scoped narrowly to: whether R4-NF1 is
  discharged, whether the fourth panel's eight P4 findings are correctly
  dispositioned, and a GO/NO-GO on the **same** rc4 coordinates. The
  fourth panel closed the substance on evidence that can be re-read; the
  candidate does not change for this repair. A GO from that panel does
  not authorize promotion, and the standing D8 Step-7b cross-family
  consult remains owed **before** operator acceptance at any GO posture.

## Why this record is on `main` and not in the durable ledger

The v6 candidate is frozen, and `.ledger/entries.jsonl` is a
byte-append-only store checked against the freeze PR's **base**: main's
bytes must survive as an exact prefix of the candidate's file. Appending
to main's ledger while the candidate is frozen therefore makes main's
copy longer than the candidate's, and the required append-only check
fails closed on the freeze PR — the very defect class (R3-NF1) the rc4
repair exists to fix, reintroduced from the other side. Executed and
confirmed, not reasoned: appending one entry to main's ledger and
comparing against the frozen candidate returns `LEDGER-REWRITTEN`.

So, for the duration of a freeze: **do not append to main's ledger.**
Rulings are recorded in a dated decision record like this one; ledger
entries for D18 and D19 are appended after the freeze resolves, in the
candidate lineage or after promotion, whichever comes first. D16 and D17
are already in the candidate's ledger as entries 20 and 21 because they
were recorded before the rc4 freeze was cut.

## Addendum — the record-path secret-scan exemption on `main` (D18a)

Opening the DCO repair PR surfaced a second live defect on `main`, found
by CI rather than by reasoning: the required `full-history-secret-scan`
job scans **all refs**, so the two pushed gauntlet-record branches put
`main` in a state where every pull request goes red. Two findings, both
the same non-credential class — verifier prose in record reports quoting
an Actions run id beside the word "API"
— the shape is the literal word "API", a colon, then a run id joined by
`=` to a workflow name — which trips gitleaks' generic-api-key entropy
heuristic. The shape is described rather than quoted here on purpose:
quoting it verbatim reproduces the trigger, and this file sits outside
the record-path exemption. That is not hypothetical — the first version
of this document did quote it, and the scan caught it. Reproduced locally with the
pinned scanner version and read in full: public identifiers, no
credential. `main`'s own push runs were green because a push scans only
the pushed ref; the exposure appears on pull-request runs.

The rc4 candidate already carries a rule-scoped exemption for
`docs/gauntlet-runs/`. `main` takes that file's text **byte-identically**
rather than an improved variant, for a reason that was measured, not
assumed: merging the frozen candidate into a `main` that carries a
*different* allowlist block conflicts in `.gitleaks.toml` at promotion,
while an identical block merges clean and yields exactly the candidate's
file. A merge conflict on the promotion act is a landmine this program
should not lay for the sake of a P4 improvement.

The improvement itself is therefore **deferred, not dropped**: the fourth
panel's R4-NF2 asks for an anchored path regex and a refreshed falsifier,
and both copies of the file must change together, so that belongs to the
next freeze's P4 sweep (the arbitration's own Next-action 5 class). What
does land now is the part that needs no shared edit: an in-CI
**narrowness control** in `release-security.yml`, which plants one
high-entropy token inside and outside the record directory and fails the
job unless the exemption fires exactly where intended, plus a branded
credential inside the directory that must still be caught. Proven
locally against the pinned scanner: fires outside (exit 1), suppressed
inside (exit 0), branded credential still caught (exit 1), and the full
`--all` history scan clean.

`release-security.yml` is untouched by the rc4 delta, so this main-side
change survives the promotion merge by the same mechanism verified for
`check_dco.py`.
