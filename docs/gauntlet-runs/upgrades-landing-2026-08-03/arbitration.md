# Arbitration — landing the stranded upgrade PRs (#65, #54, #50)

Five lens reports entered arbitration (27 findings, 0 struck for malformed
falsifiers, 0 H-only). The subject-seeded wildcard was
`ecological-systems-analyst`; it used the same finding contract and
arbitration path as every other evaluator. The red-lines-arbitrator
categorical gate returned PASS-WITH-NOTES after executing the decisive
falsifier live: `git ls-remote` resolved all three pinned action SHAs to
exactly the claimed upstream tags (setup-python v5.6.0 = a26af69b…,
setup-go v5.0.2 = 0a12ed9d…, checkout v4.3.1 = 34e11487…), voiding the
panel's sole P1 mechanically. The integrating session independently
re-executed the same three ls-remote checks with identical results before
committing this record.

Correlated same-inference claims from multiple lenses were weighed as ONE
claim each (see the `lens` fields naming the merged sources). Dissent is
preserved verbatim-in-spirit in the conflict ledger inside the fenced
block. The ruling-set@1 block below is the writable home of the verdict;
the run record derives from it and never restates it.

Independence caveat, preserved from the judge's own ruling: all seats
(lenses, gate, judge) ran in the same model family (Claude); the skill's
different-family judge preference was not satisfiable in this harness and
Step 7b external adjudication was not run (operator-gated, operator absent).

```json
{
 "ruling_set": "ruling-set@1",
 "rulings": [
  {
   "id": "R1-action-pin-trust",
   "lens": "disgruntled-maintainer F1 (correlated: ECO-1, CM-1 pin arm, cloud-native F1 pin arm — ONE claim)",
   "priority": "P1",
   "basin": "supply-chain-trust",
   "ruling": "OVERRULED",
   "status": "resolved",
   "validation_kernel": "Immutable SHA pinning, persist-credentials:false, and the unscanned-path-to-main closure are genuine supply-chain hardening that must survive any future change; reverting to floating tags to dodge verification burden would be strictly worse. F1 was epistemically correct on the frozen record — an unverified SHA plus a benign version comment from the sole self-attesting actor deserved zero independent weight and was the canonical admin-shaped backdoor pattern — and it was discharged only by executing its own falsifier: git ls-remote (2026-08-03) matched setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 to refs/tags/v5.6.0 and setup-go@0a12ed9d6a96ab950c8f026ed9f722fe0da7ef32 to refs/tags/v5.0.2 exactly; checkout 34e11487 == v4.3.1 == the SHA main's dco.yml already trusts. The executed verification, not the version comments, is now the trust basis, and it must be durably recorded to keep this ruling discharged.",
   "acceptance_criteria": [
    {
     "condition": "The 2026-08-03 ls-remote verification (all three SHA-to-tag mappings) is recorded in the PR body or a ledger entry before merge, per the red-lines gate's boundary note; absence of the record at merge time reopens this ruling at P1.",
     "falsifier": {
      "method": "Inspect the merge PR body and .ledger/entries.jsonl for the three recorded SHA-to-tag mappings (setup-python v5.6.0, setup-go v5.0.2, checkout v4.3.1, verified 2026-08-03).",
      "threshold": "All three mappings present in at least one durable location at merge time.",
      "timeframe": "Before merge to main."
     },
     "owner": "operator"
    }
   ]
  },
  {
   "id": "R2-github-ci-execution",
   "lens": "chaos-monkey CM-1 + cloud-native F1 + ecological ECO-3 (ONE correlated claim; H3 residual)",
   "priority": "P2",
   "basin": "environment-verification",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "The local 31/31 per-step battery was the correct fail-closed substitute under the network scope limit and remains valuable pre-push practice; the defect is that it is structurally blind to uses: action resolution, runner labels, permissions blocks, timeout semantics, and trigger behavior — exactly the surface this diff changes most heavily. The fix is one delegated run on the managed substrate, never loosening the pins or re-narrowing release-security triggers.",
   "acceptance_criteria": [
    {
     "condition": "All three workflows (epistemic-flexibility, dco, release-security) run green on GitHub-hosted runners against exactly tree 4e49ba5f, with run URLs attached to the run evidence or PR body, closing the dossier's second UNVERIFIED label.",
     "falsifier": {
      "method": "Open a draft PR (or push) from branch head 4e49ba5f and observe GitHub check-run conclusions for all three workflow files.",
      "threshold": "3/3 workflows green with zero action-resolution, runner-label, or timeout failures; any red confirms the finding and blocks merge.",
      "timeframe": "First CI cycle (~30 minutes), before merge."
     },
     "owner": "operator"
    }
   ]
  },
  {
   "id": "R3-provenance-record",
   "lens": "disgruntled-maintainer F2 + decision-rights-auditor DRA-1 + ecological ECO-6 (ONE correlated claim)",
   "priority": "P2",
   "basin": "provenance-accountability",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "validation_kernel": "The squash shape was forced by the repo's own author-matching DCO policy — the original heads genuinely fail it [V evidence/dco-check.txt:5] — and content survived byte-identically with PR-granularity tracing intact in every commit subject. Any fix must keep every landed commit passing check_dco.py; the defect is a missing durable person-level record, not the integration shape. Qualification: DCO accountability is displaced, not destroyed — the originals are recorded in the evidence root, which only the integrator has attested.",
   "acceptance_criteria": [
    {
     "condition": "Original-head authorship (a51c77b — SternOne; da3e013) and the human certifying party for the six agent-signed commits are recorded in at least one durable location: Co-authored-by trailers, the PR body, or a ledger entry — outside the integrator-only evidence file.",
     "falsifier": {
      "method": "Inspect commit trailers on origin/main..HEAD, the PR body, and .ledger/entries.jsonl for the original heads and a human-traceable certifier.",
      "threshold": "Both original heads and a named human certifying party present in >=1 durable location.",
      "timeframe": "Before merge."
     },
     "owner": "operator"
    }
   ]
  },
  {
   "id": "R4-operator-merge-decision",
   "lens": "decision-rights-auditor DRA-2",
   "priority": "P2",
   "basin": "decision-rights",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "The re-scope itself was legitimate and evidence-anchored — PR #50's base stack is dead but its issues are live and unsatisfied on main (C10), and the operator authorized landing the upgrades (C12, verified live). What is missing is the operator-owned informed approval record; the fix preserves the ported content and the agent's documented re-scope trace in full.",
   "acceptance_criteria": [
    {
     "condition": "The merge is taken as an explicit operator decision: an operator-opened or operator-approved PR whose body names the re-scoped shape (workflows-only #65, #54, ported #50), surfaces the C9 override and the C13 scope interpretation, includes the R1 pin-verification record, and cites this gauntlet ruling; plus a durable ledger decision entry naming the operator as decider. Merge on harness authority alone fails this criterion.",
     "falsifier": {
      "method": "Check GitHub PR events for the operator-authored approval artifact and .ledger/entries.jsonl for the decision entry.",
      "threshold": "Artifact exists, explicitly acknowledges C9 and C13, names the operator as decider.",
      "timeframe": "At merge time; before the branch reaches main."
     },
     "owner": "operator (non-delegable)"
    }
   ]
  },
  {
   "id": "R5-kernel-gate-coverage",
   "lens": "disgruntled-maintainer F3",
   "priority": "P2",
   "basin": "gate-coverage",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "The validator and its fail-closed self-test discipline are sound — positive example and planted-negative both behave [V evidence/kernel-gate.txt:1-2]. The defect is a coverage/claim mismatch: the commit claims to 'require validation kernels for overruled findings (#37)' while CI invokes only --self-test on the shipped fixture, so real arbitration artifacts (including this run's own ruling set) are structurally outside gate coverage. Fix is coverage extension or written claim narrowing, never gate removal.",
   "acceptance_criteria": [
    {
     "condition": "Either (a) CI validates real arbitration/ruling-set artifacts (glob docs/gauntlet-runs/**) so a kernel-less OVERRULED ruling in a real artifact fails the battery, or (b) a committed scope statement narrows the #37 enforcement claim to fixture-only coverage in writing. The chosen path is named in the R4 merge-decision record.",
     "falsifier": {
      "method": "Path (a): commit a real arbitration file containing an OVERRULED ruling without validation_kernel on a scratch branch and execute the full per-step battery. Path (b): locate the committed scope statement in README/docs.",
      "threshold": "(a) any battery step exits non-zero naming the file, or (b) the scope statement exists.",
      "timeframe": "Before merge, or in the first follow-up PR if so recorded in the merge decision."
     },
     "owner": "operator / first follow-up PR"
    }
   ]
  },
  {
   "id": "R6-ledger-tamper-evidence",
   "lens": "disgruntled-maintainer F4",
   "priority": "P2",
   "basin": "ledger-integrity",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "validation_kernel": "The union-append itself was clean — 8 entries, 0 errors, unique ids, intact supersession [V evidence/store-validation.txt:8] — and putting the real durable store under CI validation is a genuine, correctly-scoped control that must survive. The validator's honesty about its structural-only scope [V evidence/diff.patch:1335] is a feature; the defect is that nothing else fills the gap it names: backdating and rewrites are undetectable by any gate on this tree, and this diff itself demonstrates the backdating move (a 2026-07-22 entry appended after 2026-07-26 entries).",
   "acceptance_criteria": [
    {
     "condition": "Either (a) a CI append-only/byte-identity check compares committed ledger lines against merge-base (existing lines byte-identical, new lines append-only), or (b) the tamper-evidence gap and the backdated 2026-07-22 entry's legitimacy as a port of the PR #35-era decision are explicitly accepted in a durable ledger entry.",
     "falsifier": {
      "method": "Path (a): mutate one existing line of .ledger/entries.jsonl (schema-valid) on a scratch branch and run the full battery. Path (b): locate the residual-risk acceptance entry.",
      "threshold": "(a) any battery step fails on the mutated store, or (b) the acceptance entry exists naming both the gap and the backdated entry.",
      "timeframe": "With merge or in the first follow-up PR."
     },
     "owner": "operator / first follow-up PR"
    }
   ]
  },
  {
   "id": "R7-ledger-concurrency",
   "lens": "chaos-monkey CM-2 (downgraded from lens P2; dissent preserved in conflict ledger)",
   "priority": "P3",
   "basin": "ledger-integrity",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "validation_kernel": "The single-head, uniqueness, dangling-supersedes, and acyclicity invariants are real store-integrity properties correctly mechanized for the first time and must be preserved exactly. The gap is merge-ordering protection: two individually-green .ledger-appending PRs can turn main red post-land. Detection, though late, is loud and recoverable — the invariant working late, not failing — which is why this sits at P3 with an explicit re-escalation trigger.",
   "acceptance_criteria": [
    {
     "condition": "Require-branches-up-to-date or a merge queue covers PRs touching .ledger/**, or the decision-ledger skill documents mandatory pre-merge union re-validation; re-escalate to P2 if concurrent .ledger-touching PRs become frequent.",
     "falsifier": {
      "method": "Replay test: two branches from this tree each append an entry superseding the same parent; merge the first; attempt the second under actual repo branch-protection settings.",
      "threshold": "Second merge is blocked or its re-run check fails before main contains the two-head union (main stays green throughout).",
      "timeframe": "First follow-up window, under an hour of replay testing."
     },
     "owner": "operator (repo settings)"
    }
   ]
  },
  {
   "id": "R8-audit-coverage-decay",
   "lens": "maintainer F5 + chaos-monkey CM-3/CM-4 + cloud-native F2 + DRA-5 + ECO-4 (ONE correlated claim family: coverage decay + marker precision)",
   "priority": "P3",
   "basin": "gate-coverage",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "Fail-closed ambiguity handling, auditing real skill texts rather than fixtures, and the pinned marker-precedence self-test are sound and must survive any fix; the frozen 10-file inventory was a defensible, documented v1 scope choice. The fix is inventory discovery/tripwire plus marker precision (word-boundary regexes), not classifier redesign or fuzzy auto-discovery — and the diff itself teaches the lesson: release-security.yml deleted a hand-curated path inventory precisely because curated lists create unscanned paths.",
   "acceptance_criteria": [
    {
     "condition": "A follow-up PR adds an out-of-inventory tripwire (fail when TERM_RE matches any plugins/epistemic-skills/skills/*/SKILL.md absent from SKILL_PATHS), converts markers to word-boundary regexes dropping bare 'test'/'check'/' ci', folds perturbation probes into the self-test, and names an owner/trigger for inventory maintenance in the new-skill checklist.",
     "falsifier": {
      "method": "Plant 'This skill enforces X.' in a non-inventoried SKILL.md and run the full battery; run the CM-3 perturbation property test (neutral and marker-bearing decoy edits) over the 17 recorded occurrences.",
      "threshold": "Planted file flagged by >=1 CI step; 0 category flips and 0 spurious ambiguity failures under neutral perturbation.",
      "timeframe": "First follow-up PR, before the next skill addition."
     },
     "owner": "first follow-up PR / operator"
    }
   ]
  },
  {
   "id": "R9-calibration-staleness",
   "lens": "cloud-native F3/F4 + decision-rights-auditor DRA-4/DRA-6 + ecological ECO-5 (correlated H5 family)",
   "priority": "P3",
   "basin": "calibration-contract",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "validation_kernel": "The freeze is deliberate and README-labeled ('frozen at its 2d66a27 v3.0.0-era baseline'), the fail-closed posture on calibration-side facts is exemplary, and the unilateral-proposal honesty must survive every fix — corrections append or supersede, never rewrite the frozen body. DRA-6's operative uncertainty (whether the refresh commit touched the charter) is H-tier and carries zero weight as fact; only the cheap mechanical check is ordered, not its conclusion. ECO-5's consts are deliberate fail-closed design; the remedy is verification and revision-pinning of the handoff, not loosening.",
   "acceptance_criteria": [
    {
     "condition": "Before merge: run `git diff da3e013 HEAD -- docs/coordination/epistemic-calibration.md`; an empty diff keeps the formal-rigor record's valid_while satisfied, any change forces a re-pin or supersession note in the same PR.",
     "falsifier": {
      "method": "One git command against the fetched PR #54 head (present in the live clone per the dossier).",
      "threshold": "Empty diff, or an appended re-pin/supersession note.",
      "timeframe": "Seconds, before merge."
     },
     "owner": "operator"
    },
    {
     "condition": "Follow-up: (a) the charter file gains a two-line frozen-at-2d66a27 banner (no body rewrite) and the 'update this charter before implementation' step gains a named owner; (b) any counterpart handoff references the schema at an immutable revision, treating the mutable main-branch $id as identity-only, with Phase 0 reconnaissance (canonical ZMS-Labs/epistemic-calibration coordinate verified) before any inbound record is accepted.",
     "falsifier": {
      "method": "Read the charter head-of-file; inspect handoff/README instructions for a revision-pinned schema coordinate and the Phase 0 exit criterion.",
      "threshold": "Banner plus named owner present; revision-pinned handoff documented; zero inbound records accepted pre-Phase-0.",
      "timeframe": "First follow-up PR; before any external counterparty contact."
     },
     "owner": "first follow-up PR / operator"
    }
   ]
  },
  {
   "id": "R10-accepted-gate-binding",
   "lens": "decision-rights-auditor DRA-3",
   "priority": "P3",
   "basin": "decision-rights",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "The closed status lifecycle, fail-closed unknown-value handling, and never_attests non-attestations (including release-readiness-by-envelope) are correct and must be preserved; the gap is a missing consumer-side acceptance binding for producer-writable 'accepted-gate' status, not an over-claiming schema. Non-urgent while no counterparty exists — the prose disclaimer plus the absent counterparty makes this a pre-Phase-4 obligation, not a merge condition.",
   "acceptance_criteria": [
    {
     "condition": "Before Phase 4 (gate promotion), either the schema gains a consumer acceptance/decision-record reference field (with version bump per the contracts README's own rule) or a committed procedure requires an epistemic-skills-side ledger decision before any accepted-gate record becomes operative.",
     "falsifier": {
      "method": "Trace where acceptance is bound in the schema or committed procedure; attempt to treat a producer-only accepted-gate record as operative for a release gate.",
      "threshold": "A producer-only accepted-gate record is demonstrably non-operative.",
      "timeframe": "Before Phase 4 of the charter's phased plan."
     },
     "owner": "operator / pre-Phase-4 follow-up"
    }
   ]
  },
  {
   "id": "R11-pin-gardening",
   "lens": "ecological-systems-analyst ECO-2 (downgraded from lens P2; dissent preserved in conflict ledger)",
   "priority": "P3",
   "basin": "maintenance-debt",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "validation_kernel": "Pinning is the correct, deliberate hardening and the release-security comment rightly forbids re-narrowing the triggers; the true defect — no owner, no refresh trigger, no dependabot surface for the pin inventory (runner label, action SHAs, Go 1.25.1, gitleaks) — is real and must be serviced. Its failure modes are slow and loud (simultaneous workflow failure on runner retirement; scanner aging), which places it in maintenance debt rather than merge-conditional execution safety.",
   "acceptance_criteria": [
    {
     "condition": "A dependabot github-actions config lands (updates arrive as reviewable SHA re-pin PRs) and a durable ledger entry names the pin-inventory owner with revisit_when tied to runner-label deprecation announcements and gitleaks rule releases.",
     "falsifier": {
      "method": "Check .github/dependabot.yml exists covering github-actions; grep .ledger/entries.jsonl for the pin-inventory revisit_when and owner.",
      "threshold": "Both artifacts exist.",
      "timeframe": "With merge or in the first follow-up PR."
     },
     "owner": "operator / first follow-up PR"
    }
   ]
  },
  {
   "id": "R12-validator-portability",
   "lens": "chaos-monkey CM-5 + cloud-native F5 (correlated)",
   "priority": "P4",
   "basin": "portability",
   "ruling": "UPHELD",
   "status": "open",
   "validation_kernel": "Defaulting to the real durable store (issue #36's entire point) and failing loudly when it is missing are correct behaviors that must remain the repo-CI default; only the discovery mechanism — counted parents[N] hops at two different depths, and an install-shaped default failure invisible to repo CI — needs a graceful message or marker-based root discovery. Partially self-falsified already: no documented invocation path currently hits the failing default.",
   "acceptance_criteria": [
    {
     "condition": "On the next touch of either script: a distinct 'no durable store at <path>; pass --ledger or --examples-only' message, or a shared walk-up-to-marker root helper replacing the parents[4]/parents[6] constants.",
     "falsifier": {
      "method": "Run validate_examples.py with no flags from a copied plugin tree outside the repository.",
      "threshold": "Clear actionable message (or successful marker-based resolution) instead of a bare 'missing' exit.",
      "timeframe": "Opportunistic; next modification of either script."
     },
     "owner": "opportunistic follow-up"
    }
   ]
  }
 ],
 "conflict_ledger": [
  {
   "parties": "disgruntled-maintainer F1 (P1 blocker) vs red-lines gate live falsifier execution; ECO-1, CM-1 pin arm, cloud-native F1 pin arm alongside at P2 — correlated same-inference, weighed as ONE claim",
   "conflict": "Whether the two unverified setup-* action-SHA pins (setup-python@a26af69b '# v5.6.0', setup-go@0a12ed9d '# v5.0.2') constitute a merge-blocking trust grant to unaudited third-party code.",
   "ruling": "OVERRULED",
   "evidence_weight": "V — the finding's own falsifier was executed live by the red-lines gate: git ls-remote matched setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 to upstream refs/tags/v5.6.0 and setup-go@0a12ed9d6a96ab950c8f026ed9f722fe0da7ef32 to refs/tags/v5.0.2 (exact 40-hex), and checkout 34e11487 == v4.3.1 == the SHA origin/main dco.yml already trusts. F1's stated threshold: 'both matches void it.' Both matched.",
   "justification": "The claim is decided by its own mechanical falsifier, executed post-freeze from a network-capable environment. With genuine pins, the diff strictly improves supply-chain posture on every axis it touches; no unverified trust grant remains.",
   "dissent_preserved": "F1 was epistemically correct on the frozen record: at freeze, the SHA-to-version mapping rested solely on comments written by the same single actor who produced every other piece of self-attested evidence, and the maintainer's rule that such comments carry zero independent weight stands undiluted. The overrule is contingent per the gate's boundary note — the 2026-08-03 ls-remote results must be durably recorded (PR body or ledger entry) before merge; an unrecorded verification reopens this ruling at P1 (see R1 acceptance criterion and R4)."
  },
  {
   "parties": "chaos-monkey ('H4 killed outright') vs disgruntled-maintainer F2 + decision-rights-auditor DRA-1 + ecological ECO-6 (provenance arm supported)",
   "conflict": "Whether H4 (the DCO-clean history rewrite lost content or provenance) is dead.",
   "ruling": "SPLIT",
   "evidence_weight": "V in both directions. Content arm: branch tree byte-identical to the pre-rebuild integration tree, 6/6 author-matching sign-offs [V evidence/commits.txt:1; V evidence/dco-check.txt:1,4]. Provenance arm: all six commits authored AND self-signed by 'Claude <noreply@anthropic.com>', with SternOne (a51c77b) and the mixed sign-off history stripped from git parentage [V evidence/commits.txt:2; V evidence/dco-check.txt:5-6].",
   "justification": "The two arms of H4 separate cleanly on verified evidence: content loss is refuted by tree identity; provenance thinning is verified fact. Chaos-monkey's outright kill conflated mechanical DCO satisfaction with accountability traceability — the gate passes precisely because one actor writes both the author and sign-off fields, which is the finding, not its refutation.",
   "dissent_preserved": "Chaos-monkey's qualification survives as the reason this is P2 rather than P1: commit subjects trace every source PR/issue (#65, #54, #36-#38), so provenance survives at PR granularity, and the fix is a cheap durable record (trailers/PR body/ledger), not a history rebuild. Recorded in R3's qualifications."
  },
  {
   "parties": "docket H2 + chaos-monkey CM-3 (brittleness arm) vs cloud-native F2, DRA-5, ECO-4, maintainer F5 (inversion: silent under-coverage) — five lenses' correlated claims weighed as ONE",
   "conflict": "Whether the ported #50 enforcement-language gate is brittle-over-firing (literal H2: fails on the first innocent SKILL.md edit) or silently under-covering (inverted H2: frozen inventory decays as the catalog grows).",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "evidence_weight": "V — literal H2 refuted by live corpus state: 17/17 occurrences classified, zero ambiguous [V evidence/audit-report.ndjson:18], and fail-on-ambiguity is documented design [V evidence/diff.patch:1807]. Inverted mechanism verified: frozen 10-file SKILL_PATHS [V evidence/diff.patch:1835] against a 17-skill catalog [V evidence/diff.patch:191,220]; substring markers including bare 'test'/'check'/' ci' with a ±2-line window [V evidence/diff.patch:1891-1899,1998-2000].",
   "justification": "Five independent lenses converge on the same inversion — one correlated claim, weighed once: the realistic failure is silent coverage decay on skill growth plus latent marker-collision misclassification, not first-edit breakage. Upheld in inverted form at P3 (R8); literal H2 is overruled — failing closed on genuinely ambiguous edits is the gate working as designed, and the surviving sliver (renames of listed files hard-fail) is asymmetric drift, not staleness.",
   "dissent_preserved": "CM-3's brittleness arm is retained in full: an innocent adjacent-prose edit can flip an occurrence to AMBIGUOUS and red CI (action at a distance), and marker collisions ('attest', 'latest', 'checkout') can silently upgrade policy claims to 'mechanical' — the precise dishonesty the audit exists to prevent. Both failure modes are wired into R8's acceptance criteria (word-boundary regexes, perturbation probes)."
  },
  {
   "parties": "disgruntled-maintainer F4 (tamper evidence, lens P2) and chaos-monkey CM-2 (concurrent-append hazard, lens P2) vs the unanimous H6 kill (store validates 8/8)",
   "conflict": "What of the ledger surface remains open after H6's death, and at what severity.",
   "ruling": "SPLIT",
   "evidence_weight": "V — H6 dead: 8 entries, 0 errors under the strict validator including uniqueness, dangling-supersedes, cycle, and single-head checks [V evidence/store-validation.txt:8]. F4's mechanism verified: the validator disclaims truth/authorization/freshness by design [V evidence/diff.patch:1335] and this very diff appends a backdated 2026-07-22 entry after 2026-07-26 entries [V evidence/diff.patch:185]. CM-2's mechanism verified [V evidence/diff.patch:1535-1539] but its failure mode is loud and post-land.",
   "justification": "F4 upheld at P2 (R6): silent, insider-shaped, and demonstrated by the subject itself — a structurally-valid rewrite or backdate passes every gate on this tree, and the backdated entry's legitimacy currently rests on the same single actor's word as everything else. CM-2 downgraded to P3 (R7): a two-head collision turns main red loudly and recoverably; the invariant firing late is detection working, not failing, and the remedy is repo settings, not the diff.",
   "dissent_preserved": "Chaos-monkey's P2 rating for CM-2 is recorded as a live minority position: this repo's operating mode — concurrent agent sessions appending ledger entries, as this landing itself demonstrates — makes collisions non-hypothetical. R7 carries an explicit revisit trigger: if .ledger-touching PR frequency grows, re-escalate to P2 and enable a merge queue."
  },
  {
   "parties": "ecological-systems-analyst ECO-2 (P2: 'a pinned ecosystem needs a gardener, and the diff appoints none') vs red-lines gate ('tradeable maintenance debt, not a categorical bound') and the omission of ECO-2 from every other lens's condition set",
   "conflict": "Whether the absence of any pin-refresh owner/trigger (ubuntu-24.04 runner label, action SHAs, Go 1.25.1, gitleaks) is execution-safety (P2) blocking-conditional on this merge, or quality debt (P3).",
   "ruling": "OVERRULED",
   "evidence_weight": "V/I — verified that the diff adds no dependabot/renovate surface and the sole appended ledger entry's revisit_when covers the five-controls inventory, not pins [V evidence/diff.patch:185, I-anchored]; but nothing in the record places any pin failure on a near horizon — runner-label retirement and scanner-rule aging are slow variables with loud, fail-closed failure modes.",
   "justification": "Overruled as a P2 condition on this merge; preserved intact at P3 (R11). The red-lines gate's analysis is correct: this is serviceable, tradeable debt, and blocking a strict security improvement on its future maintenance schedule inverts the cost-benefit. No other lens ranked it merge-conditional.",
   "dissent_preserved": "ECO's closing question — who is the gardener when GitHub retires ubuntu-24.04, when gitleaks ships rules for a new secret class — is the correct question and remains unanswered on the record. R11's acceptance criteria make the answer mandatory in the first follow-up: a named owner with revisit_when in a durable ledger entry plus a dependabot github-actions config. The diff hardens against every environmental change except the ones that arrive slowly; that sentence stands."
  },
  {
   "parties": "disgruntled-maintainer F2 falsifier (requires >=1 non-author human approval to void) vs decision-rights-auditor DRA-2 (operator-owned informed approval is the operative control) vs the record itself (no second maintainer evidenced anywhere)",
   "conflict": "What independent verification leg is required to discharge the single-actor trust chain, given that a second human reviewer may not exist.",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "evidence_weight": "V — every control in the current chain terminates in one identity: authorship and sign-off [V evidence/commits.txt:2], the only CI evidence is operator-produced local output [V evidence/ci-battery.txt:3], GitHub-side CI never ran [V evidence/continuity-digest.md:6]. Nothing in the record evidences an available second human reviewer.",
   "justification": "The substance — at least one verification leg independent of the integrator — is upheld and made concrete: GitHub-side CI on GitHub's runners (machine leg, R2) plus an operator-authored informed approval artifact acknowledging C9/C13 (human leg, R4) plus the durable provenance record (R3). A second-human review cannot be manufactured by ruling; its absence is recorded as accepted structural residual rather than pretending the operator's self-approval is independent review.",
   "dissent_preserved": "The maintainer's core point stands undiluted: detection independent of the integrator does not exist today, and every attestation this branch carries is self-referential — 'everything here shows sabotage would have been undetectable.' The residual is accepted, not refuted. If a second maintainer ever joins the repo, retroactive review of this landing's diff against the original PR heads (a51c77b, da3e013, 4b8502e) is the cheapest debt to retire first."
  }
 ],
 "computed_verdict": "CONDITIONAL",
 "next_action": "Operator opens the PR from branch head 4e49ba5f in person — one artifact discharges four of the five open P2s at once: it triggers the first GitHub-side run of all three workflows on the exact tree (R2; merge only on 3/3 green, run URLs recorded), and its body records the 2026-08-03 ls-remote pin verification (R1's remains-resolved contingency: setup-python v5.6.0 == a26af69b..., setup-go v5.0.2 == 0a12ed9d..., checkout v4.3.1 == 34e11487...), the original-head provenance (a51c77b/SternOne, da3e013) with the human certifying party (R3), and the C9 override plus C13 scope interpretation citing this gauntlet ruling (R4). Before merging, run the one-command R9(a) charter diff (git diff da3e013 HEAD -- docs/coordination/epistemic-calibration.md), and state in the merge-decision record whether R5 and R6 are discharged pre-merge or as tracked first-follow-up conditions (each has a documented cheap path: written scope narrowing for R5, residual-risk acceptance entry for R6). Verdict gate applied: zero P1 open (sole P1 overruled by its own executed falsifier), five P2 open -> CONDITIONAL; red-lines gate PASS-WITH-NOTES imposes no cap. Independence caveat per arbitrator discipline: this arbitration runs on an Anthropic Claude model (Fable 5), likely the same model family as the lens reports."
}
```
