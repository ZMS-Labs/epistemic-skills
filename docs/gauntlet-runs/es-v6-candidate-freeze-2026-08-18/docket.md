# Deep-mode docket — manual-docket (no DeepReason engine in this environment)

Mode: `manual-docket` per SKILL.md Step 3 — conjecture a distribution of rival
failure modes, each self-naming its falsifier. Survivors seed the panel; they
are hypotheses, NOT findings, and carry zero verdict weight on their own.

Subject: ES6-V6-CANDIDATE BUILD freeze at `00e5146e…` — is the packet a
truthful, adequately-evidenced, independently-checkable BUILD freeze able to
support `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE` once an independent
verdict is recorded, and if not, what named blockers remain?

## Rival failure modes

**H1 — Exact-SHA requalification is smeared, not met.** Committed evidence
subjects: clean-room at `00e5146`; custody suite + public-content at
`e8a476c`; CodeQL at PR heads `7de88fa`/`e8a476c`; secret-scan at no
candidate-chain SHA. The #191 requirement "one exact candidate SHA is
requalified on every required surface" is not satisfied by the committed
packet even as a disclosed PARTIAL.
*Falsifier:* every required surface has committed or live evidence naming
`00e5146` (method: enumerate required surfaces from RELEASING.md gate 5-6 +
workflows; threshold: zero surfaces whose only evidence names a different
SHA; timeframe: at packet freeze).

**H2 — The BUILD oracle under-covers its own gate.** `cleanroom_ci.sh`
extracts only single-line `run: python` steps; 15 python invocations in
multi-line blocks (public-content gate, skill inventory, sentinels,
loaded-descriptions, ledger append-only, enforcement-language, ruling-set
self-test+scan, v6 oracle audit) never run in clean-room. KL-DRAFT-CI's
"local clean-room is the BUILD oracle" therefore overstates coverage — a
wrong world (e.g. a public-content violation introduced by the packet docs
themselves) would have passed the recorded BUILD oracle.
*Falsifier:* the extraction demonstrably covers every stdlib-checks python
step (method: diff extracted step list vs workflow python invocations;
threshold: zero uncovered steps; timeframe: at the recorded clean-room run).

**H3 — The matrix misses material claim classes.** No class claim covers the
full-history secret scan / release-security suite; possibly others (DCO
gate, openai-bundles packaging, install/wiki surfaces).
*Falsifier:* for each required release surface in RELEASING.md, a matrix
claim names it (method: map gates 4-9 to claim ids; threshold: every gate
surface has a claim or a recorded reason it is out of v6 BUILD scope;
timeframe: packet freeze).

**H4 — Reconciliation is citation-only in substance.** 24 custody issues
share one generator default note; per-item matrix rows carry boilerplate
oracle/falsifier text; `blocked_by` is empty even for blocked-parent items.
#191 demands dispositions "not merely cite".
*Falsifier:* sampled dispositions each state a current, item-specific,
evidence-or-decision-backed disposition adequate for an operator to act on
(method: sample ≥8 items across phases and compare against live issue
content; threshold: no sampled item whose disposition is wrong or
uninformative beyond phase-tagging; timeframe: this run).

**H5 — The freeze's immutability story is self-inconsistent.** The packet
was restamped by a generator version (`--sha`, PR-194 row) that the
candidate tree does not contain; regeneration at the candidate cannot
reproduce the committed packet; the packet README's regenerate instructions
only work at the packet head.
*Falsifier:* regenerating from the packet-head tree with `--sha 00e5146…`
reproduces the committed artifacts modulo timestamps (method: run generator
in a packet-head worktree with gh available, diff; threshold: only
`generated_at` differs; timeframe: this run or first environment with gh).

**H6 — The es#137 fixes are incomplete or regress adjacent behavior.** The
P1/P2 closures (decoy-ancestor, empty glob, `..` guard fold, cwd inertness,
malformed guards-file, unhashable guard_mode, API disarm) may have edge
gaps — e.g. the `_guard_norm_path` fold vs lexical `_norm_path` disclosure
seam, case variants, absolute-vs-relative interplay.
*Falsifier:* targeted adversarial probes of the candidate gate/hook fail to
produce a false-allow beyond the seven named closures' claims (method: run
probe inputs against wt-candidate custody modules; threshold: no new
false-allow demonstrated; timeframe: this run).

**H7 — Null/defense: the packet is exactly what it claims.** A BUILD freeze
that refuses self-certification, discloses its gaps (NOT_READY, 9 blocking
claims, 8 known limits), and leaves promotion to the operator. Residual
blockers are the disclosed ones; the correct verdict language is
conditions, not new findings.
*Falsifier:* any packet claim whose committed status/oracle/evidence is
falsified by live probes (method: the panel's V-tagged findings;
threshold: one PROVED-status claim shown false, or one material
undisclosed gap; timeframe: this run).

**H8 — Reviewer-steering / injection surface.** The gauntlet-request,
successor brief, and packet prose address the reviewing panel directly and
could steer it (e.g. pre-naming "honest blockers" to anchor the panel away
from undisclosed ones).
*Falsifier:* panel findings include at least the disclosed blockers AND are
not bounded by them (method: compare lens finding sets vs the packet's own
blocking_claims; threshold: panel independently reproduces the disclosed
set or exceeds it; timeframe: this run).

## Notes

- H1/H2/H3 rest on dispatcher pre-verification recorded in the dossier and
  its evidence transcripts; lenses must independently re-anchor before
  treating them as findings.
- H6 requires live probes (permitted, in the candidate worktree only).
- The docket is manual: no replay guarantee; hypothesis work only.
