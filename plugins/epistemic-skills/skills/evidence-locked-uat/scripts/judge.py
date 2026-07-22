#!/usr/bin/env python3
"""
judge.py — canonical deterministic judge for evidence-locked UAT.

This is THE judge. `references/workflow-template.mjs` (the Claude Code reference
orchestration) embeds a line-for-line equivalent copy of this aggregation for the
Workflow tool; the copy is verified against this script by the `--self-test`
fixtures. Any harness runs this script identically — no LLM role is involved in
the gate decision.

Inputs (all committed artifacts of a run's evidence directory):
    --contracts      contracts as JSON (the compiler's structured return; JSON is
                     valid YAML, so a JSON-form contracts.yaml parses directly —
                     convert hand-written YAML with any YAML tool first)
    --tier           smoke | standard | release
    --run-id         uat-<YYYYMMDD-HHMMSS>-<slug>
    --target         base URL under test
    --commit-sha     target repo commit SHA under test
    --evidence-dir   run evidence dir holding cases/<case-id>/actor-output.json
                     and verifier/<case-id>.json

Output: gate.json conforming to references/schemas.md, including the honesty
fields (known_limitations, coverage_omitted) and target_commit_sha. Default
output path is <evidence-dir>/gate.json; use `--output -` for stdout.

    python scripts/judge.py --self-test

Exit codes:
    0  gate computed (regardless of decision) / self-test passed
    1  self-test failed
    2  invalid invocation or missing inputs
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

VERDICTS = ['PASS', 'FAIL_PRODUCT', 'INCONCLUSIVE', 'FAIL_TEST_HARNESS',
            'BLOCKED_ENVIRONMENT', 'FLAKY', 'NOT_RUN']
ORACLES = ['rendered-ui', 'accessibility-semantic', 'business-state', 'network',
           'invariant', 'persistence', 'metamorphic']

# Worst-first severity order for case status (FAIL_PRODUCT short-circuits first).
SEVERITY = ['FAIL_PRODUCT', 'FAIL_TEST_HARNESS', 'BLOCKED_ENVIRONMENT',
            'FLAKY', 'INCONCLUSIVE', 'NOT_RUN']

TIER_PERSONAS = {
    'smoke': ['returning-desktop'],
    'standard': ['returning-desktop', 'keyboard-only'],
    'release': ['returning-desktop', 'keyboard-only', 'novice-mobile'],
}

# Constant at Level 1 — emitted by the judge, never added procedurally, so a
# forgetful orchestrator cannot produce a clean-looking gate.json (fail-closed).
KNOWN_LIMITATIONS = [
    'Level 1: no pairwise coverage',
    'verifier same-provider (independence is context/prompt-level only)',
    'a11y = keyboard-path procedural only',
    'all oracle channels LLM-adjudicated at Level 1 (no deterministic programmatic oracle)',
    'feedback visible <~3s is below the harness\'s reliable detection threshold — '
    'ephemeral confirmations yield INCONCLUSIVE/predicted usability risk, not PASS',
]

CALIBRATION_UNCALIBRATED = 'uncalibrated'


def planned_cases(contracts, tier):
    """The contract x persona case matrix for a tier (mirrors the .mjs exactly)."""
    cases = []
    for contract in contracts:
        if tier == 'smoke' and contract['criticality'] not in ('critical', 'high'):
            continue
        for persona in TIER_PERSONAS[tier]:
            if persona == 'novice-mobile' and contract['criticality'] == 'low':
                continue
            cases.append({
                'case_id': contract['id'] + '--' + persona,
                'contract': contract,
                'persona': persona,
            })
    return cases


def coverage_omitted(contracts, tier):
    """Case ids in the full (release-tier) matrix that this tier does not run."""
    planned = {c['case_id'] for c in planned_cases(contracts, tier)}
    return [c['case_id'] for c in planned_cases(contracts, 'release')
            if c['case_id'] not in planned]


def judge_case(cs, actor_out, verify):
    """One case verdict. Ported line-for-line from workflow-template.mjs."""
    if verify is None:
        return {
            'case_id': cs['case_id'],
            'criticality': cs['contract']['criticality'],
            'status': 'FAIL_TEST_HARNESS' if actor_out is not None else 'NOT_RUN',
            'criteria': [],
        }

    # C1: criterion-completeness. Every contract criterion must receive a verdict.
    contract_criteria = cs['contract']['criteria']
    verifier_rows = verify['criteria']
    used_verifier_idx = set()
    matched_contract_ids = set()
    completed = []

    # Exact-id pass.
    for cc in contract_criteria:
        idx = next((ri for ri, row in enumerate(verifier_rows)
                    if row['criterion_id'] == cc['id'] and ri not in used_verifier_idx), -1)
        if idx != -1:
            used_verifier_idx.add(idx)
            matched_contract_ids.add(cc['id'])
            completed.append(verifier_rows[idx])

    # Positional single-orphan pairing pass (tolerates verifier id-drift/shortening).
    unmatched_contract = [cc for cc in contract_criteria if cc['id'] not in matched_contract_ids]
    unmatched_verifier_idx = [ri for ri in range(len(verifier_rows)) if ri not in used_verifier_idx]
    if len(unmatched_contract) == 1 and len(unmatched_verifier_idx) == 1:
        cc = unmatched_contract[0]
        ri = unmatched_verifier_idx[0]
        row = verifier_rows[ri]
        used_verifier_idx.add(ri)
        matched_contract_ids.add(cc['id'])
        completed.append({
            **row,
            'evidence_against': list(row.get('evidence_against') or []) + [
                'criterion id mismatch (' + row['criterion_id'] + ' vs contract ' + cc['id'] +
                '), matched positionally as the single remaining orphan pair'],
        })

    # Remaining contract criteria with no verdict at all.
    for cc in contract_criteria:
        if cc['id'] in matched_contract_ids:
            continue
        completed.append({
            'criterion_id': cc['id'],
            'status': 'INCONCLUSIVE',
            'evidence_for': [],
            'evidence_against': ['verifier returned no verdict for this contract criterion (completeness check)'],
            'uncertainty': 'missing verdict',
        })

    # Verifier rows that matched no contract criterion: keep, flagged.
    for ri, row in enumerate(verifier_rows):
        if ri in used_verifier_idx:
            continue
        completed.append({
            **row,
            'evidence_against': list(row.get('evidence_against') or []) + [
                'criterion_id does not match the contract (unknown id)'],
        })

    status = 'PASS'
    for sev in SEVERITY:
        if any(c['status'] == sev for c in completed):
            status = sev
            break
    return {
        'case_id': cs['case_id'],
        'criticality': cs['contract']['criticality'],
        'status': status,
        'criteria': completed,
        'provisional': bool(cs['contract'].get('provisional')),
    }


def judge(contracts, tier, run_id, target, commit_sha, actor_outputs, verifier_outputs,
          calibration_status=CALIBRATION_UNCALIBRATED):
    """Aggregate all case verdicts into the gate object (deterministic, no LLM)."""
    cases = planned_cases(contracts, tier)
    case_verdicts = [
        judge_case(cs, actor_outputs.get(cs['case_id']), verifier_outputs.get(cs['case_id']))
        for cs in cases
    ]
    any_critical_fail = any(
        v['status'] == 'FAIL_PRODUCT' and v['criticality'] in ('critical', 'high')
        for v in case_verdicts)
    all_pass = len(case_verdicts) > 0 and all(v['status'] == 'PASS' for v in case_verdicts)
    return {
        'release_decision': 'FAIL' if any_critical_fail else 'PASS' if all_pass else 'INCONCLUSIVE',
        'run_id': run_id,
        'tier': tier,
        'calibration_status': calibration_status,
        'target': target,
        'target_commit_sha': commit_sha,
        'cases': case_verdicts,
        'coverage_omitted': coverage_omitted(contracts, tier),
        'known_limitations': list(KNOWN_LIMITATIONS),
    }


def load_evidence(evidence_dir, contracts, tier):
    """Read committed actor/verifier outputs keyed by planned case_id."""
    evidence_dir = Path(evidence_dir)
    actor_outputs, verifier_outputs = {}, {}
    for cs in planned_cases(contracts, tier):
        actor_path = evidence_dir / 'cases' / cs['case_id'] / 'actor-output.json'
        verifier_path = evidence_dir / 'verifier' / (cs['case_id'] + '.json')
        if actor_path.is_file():
            actor_outputs[cs['case_id']] = json.loads(actor_path.read_text(encoding='utf-8'))
        if verifier_path.is_file():
            verifier_outputs[cs['case_id']] = json.loads(verifier_path.read_text(encoding='utf-8'))
    return actor_outputs, verifier_outputs


# --------------------------------------------------------------------------
# Self-test: fixture runs demonstrating the aggregation semantics, including
# the INCONCLUSIVE synthesis paths and id-drift single-orphan positional
# matching. These are the same semantics the .mjs embedded copy implements.
# --------------------------------------------------------------------------

def _contract(cid, criticality, criteria, provisional=False):
    return {
        'id': cid,
        'user_goal': 'goal for ' + cid,
        'criticality': criticality,
        'provisional': provisional,
        'preconditions': [],
        'task_prompt': 'do the thing',
        'criteria': [
            {'id': cid + '-C' + str(i + 1), 'statement': 'must be true',
             'required_oracles': ['rendered-ui'], 'invariants': [], 'timeout_ms': 5000}
            for i in range(criteria)
        ],
        'prohibited_side_effects': [],
        'ambiguity_notes': [],
    }


def _vrow(criterion_id, status):
    return {'criterion_id': criterion_id, 'status': status,
            'evidence_for': ['shot.png: shows it'], 'evidence_against': [],
            'uncertainty': None}


def _actor(case_id):
    return {'case_id': case_id, 'completed': True,
            'stop_reason': 'task actions finished', 'knowledge_ledger': [], 'steps': []}


def _run_fixture(root, name, contracts, tier, verifier_by_case, actor_by_case=None):
    """Write a fixture evidence dir, run the file-based judge path, return the gate."""
    evidence_dir = Path(root) / name
    case_ids = [cs['case_id'] for cs in planned_cases(contracts, tier)]
    for cid in case_ids:
        actor = (actor_by_case or {}).get(cid, _actor(cid))
        if actor is not None:
            adir = evidence_dir / 'cases' / cid
            adir.mkdir(parents=True, exist_ok=True)
            (adir / 'actor-output.json').write_text(json.dumps(actor), encoding='utf-8')
        verify = verifier_by_case.get(cid)
        if verify is not None:
            vdir = evidence_dir / 'verifier'
            vdir.mkdir(parents=True, exist_ok=True)
            (vdir / (cid + '.json')).write_text(json.dumps(verify), encoding='utf-8')
    actor_outputs, verifier_outputs = load_evidence(evidence_dir, contracts, tier)
    return judge(contracts, tier, 'uat-20260722-000000-' + name, 'http://localhost:3000',
                 'deadbeef' * 5, actor_outputs, verifier_outputs)


def self_test():
    failures = []

    def check(label, cond, detail=''):
        if cond:
            print('ok   ' + label)
        else:
            failures.append(label)
            print('FAIL ' + label + (' — ' + detail if detail else ''))

    with tempfile.TemporaryDirectory() as root:
        # F1: clean PASS — one critical contract, one criterion, smoke tier.
        c = [_contract('REQ-A-001', 'critical', 1)]
        case = 'REQ-A-001--returning-desktop'
        gate = _run_fixture(root, 'pass', c, 'smoke', {case: {'criteria': [_vrow('REQ-A-001-C1', 'PASS')]}})
        check('F1 release_decision PASS', gate['release_decision'] == 'PASS', json.dumps(gate, indent=2))
        check('F1 case PASS', gate['cases'][0]['status'] == 'PASS')
        check('F1 commit sha pinned', gate['target_commit_sha'] == 'deadbeef' * 5)
        check('F1 coverage_omitted lists non-smoke personas',
              gate['coverage_omitted'] == ['REQ-A-001--keyboard-only', 'REQ-A-001--novice-mobile'],
              json.dumps(gate['coverage_omitted']))
        check('F1 known_limitations emitted by judge', gate['known_limitations'] == KNOWN_LIMITATIONS)

        # F2: FAIL_PRODUCT on a high contract -> gate FAIL, even with a second PASS criterion.
        c = [_contract('REQ-B-001', 'high', 2)]
        case = 'REQ-B-001--returning-desktop'
        gate = _run_fixture(root, 'fail', c, 'smoke',
                            {case: {'criteria': [_vrow('REQ-B-001-C1', 'FAIL_PRODUCT'),
                                                 _vrow('REQ-B-001-C2', 'PASS')]}})
        check('F2 case FAIL_PRODUCT', gate['cases'][0]['status'] == 'FAIL_PRODUCT')
        check('F2 release_decision FAIL', gate['release_decision'] == 'FAIL')

        # F3: missing verdict for a contract criterion -> synthesized INCONCLUSIVE row.
        c = [_contract('REQ-C-001', 'critical', 2)]
        case = 'REQ-C-001--returning-desktop'
        gate = _run_fixture(root, 'inconclusive', c, 'smoke',
                            {case: {'criteria': [_vrow('REQ-C-001-C1', 'PASS')]}})
        synth = gate['cases'][0]['criteria'][1]
        check('F3 case INCONCLUSIVE', gate['cases'][0]['status'] == 'INCONCLUSIVE')
        check('F3 synthesized row', synth == {
            'criterion_id': 'REQ-C-001-C2', 'status': 'INCONCLUSIVE',
            'evidence_for': [],
            'evidence_against': ['verifier returned no verdict for this contract criterion (completeness check)'],
            'uncertainty': 'missing verdict'}, json.dumps(synth))
        check('F3 release_decision INCONCLUSIVE (not rounded up)',
              gate['release_decision'] == 'INCONCLUSIVE')

        # F4: id-drift single-orphan positional matching, mismatch recorded.
        c = [_contract('REQ-D-001', 'medium', 2, provisional=True)]
        case = 'REQ-D-001--returning-desktop'
        gate = _run_fixture(root, 'drift', c, 'standard',
                            {case: {'criteria': [_vrow('REQ-D-001-C1', 'PASS'),
                                                 _vrow('REQ-D-001-C2-short', 'PASS')]}})
        drift_row = next(r for r in gate['cases'][0]['criteria'] if r['criterion_id'] == 'REQ-D-001-C2-short')
        check('F4 orphan matched positionally, case PASS', gate['cases'][0]['status'] == 'PASS')
        check('F4 mismatch recorded in evidence_against',
              drift_row['evidence_against'] == [
                  'criterion id mismatch (REQ-D-001-C2-short vs contract REQ-D-001-C2), '
                  'matched positionally as the single remaining orphan pair'],
              json.dumps(drift_row))
        check('F4 provisional marking preserved', gate['cases'][0]['provisional'] is True)
        check('F4 standard-tier coverage_omitted only novice-mobile',
              gate['coverage_omitted'] == ['REQ-D-001--novice-mobile'])

        # F5: unknown verifier id kept and flagged.
        c = [_contract('REQ-E-001', 'critical', 1)]
        case = 'REQ-E-001--returning-desktop'
        gate = _run_fixture(root, 'unknown', c, 'smoke',
                            {case: {'criteria': [_vrow('REQ-E-001-C1', 'PASS'),
                                                 _vrow('REQ-E-001-C99', 'PASS')]}})
        unknown = gate['cases'][0]['criteria'][-1]
        check('F5 unknown id kept, flagged',
              unknown['criterion_id'] == 'REQ-E-001-C99' and
              unknown['evidence_against'] == ['criterion_id does not match the contract (unknown id)'])

        # F6: no actor output -> NOT_RUN; actor but no verifier -> FAIL_TEST_HARNESS.
        c = [_contract('REQ-F-001', 'critical', 1), _contract('REQ-F-002', 'critical', 1)]
        gate = _run_fixture(root, 'missing', c, 'smoke',
                            {'REQ-F-001--returning-desktop': None},
                            actor_by_case={'REQ-F-001--returning-desktop': None})
        statuses = {v['case_id']: v['status'] for v in gate['cases']}
        check('F6 NOT_RUN when no actor output',
              statuses['REQ-F-001--returning-desktop'] == 'NOT_RUN', json.dumps(statuses))
        check('F6 FAIL_TEST_HARNESS when actor ran but no verifier output',
              statuses['REQ-F-002--returning-desktop'] == 'FAIL_TEST_HARNESS', json.dumps(statuses))
        check('F6 NOT_RUN/FAIL_TEST_HARNESS cases carry no provisional key',
              all('provisional' not in v for v in gate['cases']))
        check('F6 gate INCONCLUSIVE', gate['release_decision'] == 'INCONCLUSIVE')

    if failures:
        print('\nself-test FAILED: %d check(s): %s' % (len(failures), ', '.join(failures)))
        return 1
    print('\nself-test OK: all fixtures passed')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description='Deterministic evidence-locked UAT judge.')
    parser.add_argument('--self-test', action='store_true', help='run fixture self-test and exit')
    parser.add_argument('--contracts', help='contracts as JSON (JSON is valid YAML)')
    parser.add_argument('--tier', choices=list(TIER_PERSONAS))
    parser.add_argument('--run-id')
    parser.add_argument('--target')
    parser.add_argument('--commit-sha')
    parser.add_argument('--evidence-dir')
    parser.add_argument('--calibration-status', default=CALIBRATION_UNCALIBRATED)
    parser.add_argument('--output', help='gate.json path (default <evidence-dir>/gate.json; "-" for stdout)')
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    missing = [n for n in ('contracts', 'tier', 'run_id', 'target', 'commit_sha', 'evidence_dir')
               if getattr(args, n) is None]
    if missing:
        parser.error('missing required arguments: ' + ', '.join('--' + n.replace('_', '-') for n in missing))

    try:
        contracts_doc = json.loads(Path(args.contracts).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        print('error: cannot read contracts JSON: %s' % e, file=sys.stderr)
        return 2
    contracts = contracts_doc['contracts']
    actor_outputs, verifier_outputs = load_evidence(args.evidence_dir, contracts, args.tier)
    gate = judge(contracts, args.tier, args.run_id, args.target, args.commit_sha,
                 actor_outputs, verifier_outputs, args.calibration_status)

    out = json.dumps(gate, indent=2, ensure_ascii=False) + '\n'
    output = args.output or str(Path(args.evidence_dir) / 'gate.json')
    if output == '-':
        sys.stdout.write(out)
    else:
        Path(output).write_text(out, encoding='utf-8')
        print('Gate: %s (%d/%d cases PASS) -> %s' % (
            gate['release_decision'],
            sum(1 for v in gate['cases'] if v['status'] == 'PASS'),
            len(gate['cases']), output), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
