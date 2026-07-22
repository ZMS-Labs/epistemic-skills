// CLAUDE CODE REFERENCE IMPLEMENTATION of the evidence-locked-UAT role separation
// (actor / blinded verifier / deterministic judge as concurrent isolated sub-agents).
// Other harnesses meet the same contract with their own subagent primitive.
//
// CANONICAL JUDGE: the deterministic aggregation in the Judge phase below is an
// embedded copy of scripts/judge.py, which is canonical — any harness runs that
// stdlib script identically. The copy exists only because the Workflow tool
// executes this file standalone; it is verified against scripts/judge.py by that
// script's `--self-test` fixtures (including the INCONCLUSIVE synthesis paths and
// id-drift single-orphan positional matching). Change judge.py FIRST, then port.
export const meta = {
  name: 'evidence-locked-uat',
  description: 'Evidence-locked UAT: compile contracts, human-mode actor executes, blinded verifier judges, deterministic gate',
  phases: [
    { title: 'Compile', detail: 'requirements -> acceptance contracts' },
    { title: 'Execute', detail: 'human-mode actor per case (no verdict)' },
    { title: 'Verify', detail: 'blinded per-criterion verification' },
    { title: 'Judge', detail: 'deterministic aggregation' },
  ],
}

// args: { run_id, tier, target_url, commit_sha, change_summary, requirement_sources: string[],
//         evidence_dir, target_repo_dir }
// The runtime's `args` global is not reliably visible inside function closures
// (verified failure wf_6e9fb422-425: closures saw undefined). Bind it once at
// top level; use RUN everywhere below — never reference `args` in a closure.
const RUN = (typeof args === 'string') ? JSON.parse(args) : args

const VALID_TIERS = ['smoke', 'standard', 'release']
if (!VALID_TIERS.includes(RUN.tier)) { throw new Error('Invalid tier: ' + RUN.tier + ' (must be one of ' + VALID_TIERS.join('|') + ')') }

const VERDICTS = ['PASS', 'FAIL_PRODUCT', 'INCONCLUSIVE', 'FAIL_TEST_HARNESS', 'BLOCKED_ENVIRONMENT', 'FLAKY', 'NOT_RUN']
const ORACLES = ['rendered-ui', 'accessibility-semantic', 'business-state', 'network', 'invariant', 'persistence', 'metamorphic']

const CONTRACTS_SCHEMA = {
  type: 'object', required: ['contracts'], additionalProperties: false,
  properties: {
    contracts: {
      type: 'array', minItems: 1,
      items: {
        type: 'object', required: ['id', 'user_goal', 'criticality', 'task_prompt', 'criteria'],
        additionalProperties: false,
        properties: {
          id: { type: 'string' },
          user_goal: { type: 'string' },
          criticality: { enum: ['critical', 'high', 'medium', 'low'] },
          provisional: { type: 'boolean' },
          preconditions: { type: 'array', items: { type: 'string' } },
          task_prompt: { type: 'string' },
          criteria: {
            type: 'array', minItems: 1,
            items: {
              type: 'object', required: ['id', 'statement', 'required_oracles'], additionalProperties: false,
              properties: {
                id: { type: 'string' },
                statement: { type: 'string' },
                required_oracles: { type: 'array', items: { enum: ORACLES } },
                invariants: { type: 'array', items: { type: 'string' } },
                timeout_ms: { type: 'number' },
              },
            },
          },
          prohibited_side_effects: { type: 'array', items: { type: 'string' } },
          ambiguity_notes: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
}

// NO verdict / success / confidence fields — blinding is schema-enforced.
const ACTOR_SCHEMA = {
  type: 'object', required: ['case_id', 'completed', 'stop_reason', 'steps'], additionalProperties: false,
  properties: {
    case_id: { type: 'string' },
    completed: { type: 'boolean' },
    stop_reason: { type: 'string' },
    knowledge_ledger: { type: 'array', items: { type: 'string' } },
    steps: {
      type: 'array',
      items: {
        type: 'object', required: ['n', 'subgoal', 'precommit', 'action', 'observed_after'], additionalProperties: false,
        properties: {
          n: { type: 'number' },
          subgoal: { type: 'string' },
          precommit: {
            type: 'object', required: ['target_visible_label', 'expected_immediate', 'expected_stable'],
            additionalProperties: false,
            properties: {
              target_visible_label: { type: 'string' },
              target_role: { type: 'string' },
              target_region: { type: 'string' },
              expected_immediate: { type: 'string' },
              expected_stable: { type: 'string' },
              prohibited_effects: { type: 'array', items: { type: 'string' } },
            },
          },
          action: { type: 'string' },
          screenshots: {
            type: 'object', additionalProperties: false,
            properties: {
              before: { type: 'string' }, target_crop: { type: 'string' },
              immediate_after: { type: 'string' }, stable_after: { type: 'string' },
            },
          },
          observed_after: { type: 'string' },
          annotation: {
            type: 'object', additionalProperties: false,
            properties: {
              noticed: { type: 'string' }, expected: { type: 'string' },
              discrepancy: { type: 'string' }, confusion: { type: 'boolean' },
            },
          },
        },
      },
    },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', required: ['criteria'], additionalProperties: false,
  properties: {
    criteria: {
      type: 'array', minItems: 1,
      items: {
        type: 'object', required: ['criterion_id', 'status', 'evidence_for', 'evidence_against'],
        additionalProperties: false,
        properties: {
          criterion_id: { type: 'string' },
          status: { enum: VERDICTS.filter((v) => v !== 'FLAKY') },
          evidence_for: { type: 'array', items: { type: 'string' } },
          evidence_against: { type: 'array', items: { type: 'string' } },
          uncertainty: { type: ['string', 'null'] },
        },
      },
    },
  },
}

const PERSONAS = {
  'returning-desktop': 'Returning desktop user: ordinary product familiarity, 1440x900 viewport, pointer+keyboard, moderate attention, scans headings and primary actions, patience ~4s without feedback, abandons after 2 failed recoveries.',
  'keyboard-only': 'Keyboard-only desktop user: navigates strictly in focus order via Tab/Shift-Tab/Enter/Space/arrows, NEVER uses the pointer, requires visible focus, abandons if focus is trapped or invisible.',
  'novice-mobile': 'Novice mobile user: 390x844 touch viewport, no prior product familiarity, reads carefully, low tolerance for ambiguity, high risk-aversion on destructive actions.',
}

function actorPrompt(cs, runArgs) {
  return [
    'ROLE: HUMAN-MODE UAT ACTOR (evidence-locked UAT). You operate the interface as a bounded simulated user. You are FORBIDDEN from judging success — a separate blinded verifier does that. Your output schema has no verdict field; do not smuggle judgments into observed_after (describe what rendered, never whether it is correct).',
    '',
    'FIRST: Read ' + runArgs.target_repo_dir + '/artifacts/uat/' + runArgs.run_id + '/DIRECTIVE-PATH.txt to find and read the governing directive (Phases 4-6: personas, environment, observe-commit-act-verify loop). Obey its MUST rules for the actor role.',
    '',
    'INFORMATION PERMISSIONS (hard rules):',
    '- You may use ONLY: this task prompt, the persona description, and what is visibly rendered in the browser.',
    '- You MUST NOT read the product source code, use test IDs, call APIs, query databases, or use browser_evaluate to mutate application state. browser_snapshot/read for grounding visible elements is allowed.',
    '- Maintain a knowledge_ledger of facts the persona legitimately learned (visible content only).',
    '',
    'PERSONA: ' + PERSONAS[cs.persona],
    '',
    'TASK (the only goal you know): ' + cs.contract.task_prompt,
    'TARGET: ' + runArgs.target_url,
    '',
    'LOOP for every meaningful step (observe-commit-act-verify):',
    '1. Take a screenshot BEFORE acting; save as ' + runArgs.evidence_dir + '/cases/' + cs.case_id + '/screenshots/<NNN>-before.png (use mcp playwright browser_take_screenshot with filename). Load Playwright tools via ToolSearch "select:mcp__plugin_playwright_playwright__browser_navigate,mcp__plugin_playwright_playwright__browser_snapshot,mcp__plugin_playwright_playwright__browser_click,mcp__plugin_playwright_playwright__browser_type,mcp__plugin_playwright_playwright__browser_press_key,mcp__plugin_playwright_playwright__browser_take_screenshot,mcp__plugin_playwright_playwright__browser_wait_for,mcp__plugin_playwright_playwright__browser_navigate_back" first.',
    '2. PRECOMMIT in your step record BEFORE acting: visible target label/role/region, expected immediate feedback, expected stable state, prohibited effects.',
    '3. Act ONCE with the persona modality (keyboard-only persona: keys only).',
    '4. Screenshot immediately after (<NNN>-immediate-after.png), then wait for the visible stability condition (never a bare sleep) and screenshot again (<NNN>-stable-after.png).',
    '4b. TRANSIENT FEEDBACK: when the precommitted expected_immediate feedback may be ephemeral (toast, flash message), issue the acting call AND a browser_wait_for for the expected visible text in the SAME tool-call block (batched, no reasoning gap between them). Record the wait outcome verbatim in observed_after — a successful visible-text wait is the rendered-evidence instrument for feedback too short-lived for your screenshots. Also capture a browser_snapshot right after as structural evidence.',
    '5. Record observed_after: what rendered, what changed, what did not — description only.',
    '6. If a criterion mentions persistence: reload the page (browser_navigate to the same URL) and capture a post-reload screenshot as a separate step.',
    'STOP (with stop_reason) if: target ambiguous for a consequential action, state unknown, repeated action yields no new information, or any directive stop condition triggers. Stopping is not failure — the verifier decides.',
    '',
    'Also write your full step log as JSON to ' + runArgs.evidence_dir + '/cases/' + cs.case_id + '/actor-output.json (same content as your structured return).',
    'Return the structured output exactly per schema. Paths in screenshots fields are relative to ' + runArgs.evidence_dir + '.',
  ].join('\n')
}

function verifierPrompt(cs, actorOut, runArgs) {
  const contractForVerifier = { id: cs.contract.id, user_goal: cs.contract.user_goal, criticality: cs.contract.criticality, criteria: cs.contract.criteria, prohibited_side_effects: cs.contract.prohibited_side_effects || [], preconditions: cs.contract.preconditions || [] }
  return [
    'You are an INDEPENDENT UAT VERIFIER. You did not operate the application. Do not trust the actor\'s intention or implied success; no actor verdict exists and none may be inferred from completion. Default to INCONCLUSIVE when evidence is missing, stale, ambiguous, or contradictory — never PASS.',
    '',
    'ACCEPTANCE CONTRACT:',
    JSON.stringify(contractForVerifier, null, 2),
    '',
    'ACTOR ACTION LOG (precommits + objective actions + observations; contains no verdict):',
    JSON.stringify(actorOut, null, 2),
    '',
    'EVIDENCE ROOT: ' + runArgs.evidence_dir + ' — Read the referenced screenshots (they are images; inspect them visually). For each criterion:',
    '1. Identify the exact required claims.',
    '2. Inspect rendered evidence: is the required outcome visible, in correct context, unclipped, unobscured, associated with the right entity?',
    '3. Check the precommitted expectation against what the stable-after screenshot actually shows.',
    '4. Check required non-visual oracles where the contract demands them (persistence: does the post-reload screenshot still show the outcome? invariant: does any evidence contradict it?). A required oracle with no evidence present = INCONCLUSIVE for that criterion (or FAIL_TEST_HARNESS if the harness failed to capture it).',
    '4b. TRANSIENT STATES: a successful browser_wait_for on visible feedback text, recorded in the objective action log at act-time, is valid rendered/structural evidence for feedback too short-lived for screenshot latency (e.g. a 2-3s toast) when corroborated by at least one other channel (persistence, snapshot, invariant). A screenshot that misses an ephemeral toast is not by itself evidence of absence if the batched wait succeeded; conversely a FAILED wait for expected feedback is evidence of absence.',
    '5. Cite evidence FOR and AGAINST every verdict (file paths + what they show). Seek contradictory evidence actively.',
    '6. Use only the verdict vocabulary. Missing screenshots for a rendered-ui criterion = INCONCLUSIVE, never PASS. Cross-channel contradiction = FAIL_PRODUCT or INCONCLUSIVE, never PASS.',
    '',
    'Also write your criterion decisions to ' + runArgs.evidence_dir + '/verifier/' + cs.case_id + '.json.',
    'Return structured output per schema.',
  ].join('\n')
}

const TIER_PERSONAS = {
  smoke: ['returning-desktop'],
  standard: ['returning-desktop', 'keyboard-only'],
  release: ['returning-desktop', 'keyboard-only', 'novice-mobile'],
}

phase('Compile')
const compiled = await agent([
  'You are the REQUIREMENTS COMPILER for an evidence-locked UAT run (read ' + RUN.target_repo_dir + '/artifacts/uat/' + RUN.run_id + '/DIRECTIVE-PATH.txt, then read that directive, Phase 1).',
  'Sources to read: ' + JSON.stringify(RUN.requirement_sources),
  'Change under test: ' + RUN.change_summary,
  'Target: ' + RUN.target_url,
  'ORACLE CHANNELS AVAILABLE IN THIS HARNESS (Level 1): rendered-ui, accessibility-semantic (snapshot), persistence (reload/re-entry), invariant. Do NOT set required_oracles to network, business-state, or metamorphic unless the run explicitly provides a probe for them — a required oracle the harness cannot capture forces INCONCLUSIVE and is a contract defect.',
  'Irreversible or high-impact criteria SHOULD require three of the available channels. Note: at Level 1 all available channels are adjudicated by an LLM verifier from captured evidence; there is no deterministic programmatic oracle.',
  'Compile executable acceptance contracts: stable IDs, user goal, criticality, a task_prompt written for a user who knows NOTHING about the implementation, criterion-level statements with required oracles (critical criteria: rendered-ui plus at least one non-visual oracle; persistence criteria must name the persistence oracle), invariants, prohibited side effects. Mark inferred criteria provisional:true and record ambiguity_notes instead of improvising pass conditions.',
  'Write the contracts as YAML to ' + RUN.evidence_dir + '/contracts.yaml AND return them per schema.',
].join('\n'), { schema: CONTRACTS_SCHEMA, label: 'compile', phase: 'Compile' })

const personas = TIER_PERSONAS[RUN.tier]
const cases = []
for (const contract of compiled.contracts) {
  if (RUN.tier === 'smoke' && contract.criticality !== 'critical' && contract.criticality !== 'high') continue
  for (const persona of personas) {
    if (persona === 'novice-mobile' && contract.criticality === 'low') continue
    cases.push({ case_id: contract.id + '--' + persona, contract, persona })
  }
}
log(cases.length + ' cases planned (tier=' + RUN.tier + ', ' + compiled.contracts.length + ' contracts)')

// coverage_omitted: case ids in the full (release-tier) contract x persona matrix
// that this tier does not run. Computed here by the judge, never added
// procedurally by the orchestrator (fail-closed honesty — see schemas.md).
const coverageOmitted = (() => {
  const plannedIds = new Set(cases.map((c) => c.case_id))
  const omitted = []
  for (const contract of compiled.contracts) {
    for (const persona of TIER_PERSONAS.release) {
      if (persona === 'novice-mobile' && contract.criticality === 'low') continue
      const id = contract.id + '--' + persona
      if (!plannedIds.has(id)) omitted.push(id)
    }
  }
  return omitted
})()

const results = await pipeline(
  cases,
  (cs) => agent(actorPrompt(cs, RUN), { schema: ACTOR_SCHEMA, label: 'act:' + cs.case_id, phase: 'Execute' })
    .then((actorOut) => ({ cs, actorOut })),
  (r) => r && r.actorOut
    ? agent(verifierPrompt(r.cs, r.actorOut, RUN), { schema: VERIFY_SCHEMA, label: 'verify:' + r.cs.case_id, phase: 'Verify' })
        .then((verify) => ({ ...r, verify }))
    : r && { ...r, verify: null }
)

phase('Judge')
// Embedded copy of scripts/judge.py (canonical). Keep semantics line-for-line
// identical; equivalence is exercised by judge.py --self-test.
const SEVERITY = ['FAIL_PRODUCT', 'FAIL_TEST_HARNESS', 'BLOCKED_ENVIRONMENT', 'FLAKY', 'INCONCLUSIVE', 'NOT_RUN']
const byCase = new Map(results.filter(Boolean).map((r) => [r.cs.case_id, r]))
const caseVerdicts = cases.map((cs, i) => {
  let r = byCase.get(cs.case_id)
  if (r === undefined) {
    const fallback = results[i]
    r = (fallback && fallback.cs && fallback.cs.case_id === cs.case_id) ? fallback : undefined
  }
  if (!r || !r.verify) {
    return { case_id: cs.case_id, criticality: cs.contract.criticality, status: r && r.actorOut ? 'FAIL_TEST_HARNESS' : 'NOT_RUN', criteria: [] }
  }

  // C1: criterion-completeness. Every contract criterion must receive a verdict.
  const contractCriteria = cs.contract.criteria
  const verifierRows = r.verify.criteria
  const usedVerifierIdx = new Set()
  const matchedContractIds = new Set()
  const completed = []

  // Exact-id pass.
  for (const cc of contractCriteria) {
    const idx = verifierRows.findIndex((row, ri) => row.criterion_id === cc.id && !usedVerifierIdx.has(ri))
    if (idx !== -1) {
      usedVerifierIdx.add(idx)
      matchedContractIds.add(cc.id)
      completed.push(verifierRows[idx])
    }
  }

  // Positional single-orphan pairing pass (tolerates verifier id-drift/shortening).
  const unmatchedContract = contractCriteria.filter((cc) => !matchedContractIds.has(cc.id))
  const unmatchedVerifierIdx = verifierRows.map((_, ri) => ri).filter((ri) => !usedVerifierIdx.has(ri))
  if (unmatchedContract.length === 1 && unmatchedVerifierIdx.length === 1) {
    const cc = unmatchedContract[0]
    const ri = unmatchedVerifierIdx[0]
    const row = verifierRows[ri]
    usedVerifierIdx.add(ri)
    matchedContractIds.add(cc.id)
    completed.push({
      ...row,
      evidence_against: [...(row.evidence_against || []), 'criterion id mismatch (' + row.criterion_id + ' vs contract ' + cc.id + '), matched positionally as the single remaining orphan pair'],
    })
  }

  // Remaining contract criteria with no verdict at all.
  for (const cc of contractCriteria) {
    if (matchedContractIds.has(cc.id)) continue
    completed.push({
      criterion_id: cc.id,
      status: 'INCONCLUSIVE',
      evidence_for: [],
      evidence_against: ['verifier returned no verdict for this contract criterion (completeness check)'],
      uncertainty: 'missing verdict',
    })
  }

  // Verifier rows that matched no contract criterion: keep, flagged.
  for (let ri = 0; ri < verifierRows.length; ri++) {
    if (usedVerifierIdx.has(ri)) continue
    const row = verifierRows[ri]
    completed.push({
      ...row,
      evidence_against: [...(row.evidence_against || []), 'criterion_id does not match the contract (unknown id)'],
    })
  }

  let status = 'PASS'
  for (const sev of SEVERITY) {
    if (completed.some((c) => c.status === sev)) { status = sev; break }
  }
  return { case_id: cs.case_id, criticality: cs.contract.criticality, status, criteria: completed, provisional: !!cs.contract.provisional }
})

const anyCriticalFail = caseVerdicts.some((v) => v.status === 'FAIL_PRODUCT' && (v.criticality === 'critical' || v.criticality === 'high'))
const allPass = caseVerdicts.length > 0 && caseVerdicts.every((v) => v.status === 'PASS')
// Level-1 honesty fields, emitted by the judge (constant/computable), never
// appended procedurally by the orchestrator. Must equal KNOWN_LIMITATIONS in
// scripts/judge.py.
const KNOWN_LIMITATIONS = [
  'Level 1: no pairwise coverage',
  'verifier same-provider (independence is context/prompt-level only)',
  'a11y = keyboard-path procedural only',
  'all oracle channels LLM-adjudicated at Level 1 (no deterministic programmatic oracle)',
  'feedback visible <~3s is below the harness\'s reliable detection threshold — ephemeral confirmations yield INCONCLUSIVE/predicted usability risk, not PASS',
]
const gate = {
  release_decision: anyCriticalFail ? 'FAIL' : allPass ? 'PASS' : 'INCONCLUSIVE',
  run_id: RUN.run_id,
  tier: RUN.tier,
  calibration_status: 'uncalibrated',
  target: RUN.target_url,
  target_commit_sha: RUN.commit_sha,
  cases: caseVerdicts,
  coverage_omitted: coverageOmitted,
  known_limitations: KNOWN_LIMITATIONS,
}
log('Gate: ' + gate.release_decision + ' (' + caseVerdicts.filter((v) => v.status === 'PASS').length + '/' + caseVerdicts.length + ' cases PASS)')
return gate
