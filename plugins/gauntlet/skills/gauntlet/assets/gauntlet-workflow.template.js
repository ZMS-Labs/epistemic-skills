// Gauntlet panel orchestration — CLAUDE CODE REFERENCE IMPLEMENTATION of the
// harness-agnostic Step-5 contract (concurrent isolated role-agents + barrier).
// Other harnesses meet the same contract with their own subagent primitive.
// Gauntlet panel orchestration — the STANDARD execution model (Phase 0.6).
// generate_options (open axis) -> deterministic fan-out -> barrier -> mechanical
// criticism -> arbitrate -> verdict. Pass the frozen dossier + the selection made by
// scripts/select_lenses.py via `args`. The Workflow journal IS the append-only
// replayable record and budget.spent() IS the meter==log accounting.
//
// args = {
//   dossierPath, evidenceRoot, subjectOneLine, axis: "open"|"fixed",
//   docketMode, independence: "independent",
//   selectionPath,               // replay record from select_lenses.py (recorded, not re-derived)
//   generators: [ {persona, cardText} ... ],      // open axis only; [] on fixed
//   panel: [ {role:"adversary|constructive|metatextual", persona, cardText} ... ],
//   gates:  [ {persona, cardText} ... ],          // governance-lawyer / red-lines-arbitrator
//   judgePersona, judgeCardText,                  // pragmatic-judge default
//   hypotheses: [ "H1 ...", ... ]
// }

export const meta = {
  name: 'gauntlet-panel',
  description: 'Sovereign-Gauntlet: options (open axis) -> independent lenses -> verified -> gated -> arbitrated GO/CONDITIONAL/NO-GO',
  phases: [
    { title: 'Options',   detail: 'pre-panel option generators (open questions only; null option mandatory)' },
    { title: 'Lenses',    detail: 'independent role-agents, one per persona (barrier)' },
    { title: 'Verify',    detail: 'mechanical criticism: evidence tiers + structural falsifier well-formedness' },
    { title: 'Gate',      detail: 'categorical + process gates (can block regardless of weighing)' },
    { title: 'Arbitrate', detail: 'Conflict Ledger + computed verdict (ruling-set@1)' },
  ],
}

// Defensive: `args` may arrive as a JSON string (harness serialization).
const A = (typeof args === 'string') ? JSON.parse(args) : (args || {})

// finding-set@1 — evidence is tiered; falsifier is STRUCTURED (observable by
// construction: method + threshold + timeframe), not a free string.
const FALSIFIER_SCHEMA = {
  type: 'object',
  properties: {
    statement: { type: 'string' },   // what observation would prove this WRONG
    method:    { type: 'string' },   // how to obtain it (grep/probe/test/measurement)
    threshold: { type: 'string' },   // the pass/fail line
    timeframe: { type: 'string' },   // when/for how long it must be observed
  },
  required: ['statement', 'method', 'threshold', 'timeframe'],
}
const LENS_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },                                   // stable finding id (lens:slug)
          severity: { type: 'string', enum: ['P1', 'P2', 'P3', 'P4'] },
          claim: { type: 'string' },
          evidence: { type: 'array', items: { type: 'object', properties: {
            tier: { type: 'string', enum: ['V', 'I', 'H'] },
            ref:  { type: 'string' },                               // [V] path:line | [I] anchor list | [H] rationale
          }, required: ['tier', 'ref'] } },
          reasoning: { type: 'string' },
          hypothesis_impact: { type: 'string' },
          falsifier: FALSIFIER_SCHEMA,                              // REQUIRED + structured
          impact: { type: 'string' },
          proposed_action: { type: 'string' },
        },
        required: ['id', 'severity', 'claim', 'evidence', 'falsifier', 'proposed_action'],
      },
    },
    hypothesis_supported: { type: 'string' },
    hypothesis_killed: { type: 'string' },
    fix_or_move: { type: 'string' },
  },
  required: ['verdict', 'findings', 'hypothesis_supported'],
}

// option-set@1
const OPTION_SCHEMA = {
  type: 'object',
  properties: {
    options: {
      type: 'array', minItems: 3, maxItems: 5,
      items: { type: 'object', properties: {
        option: { type: 'string' },
        is_null_option: { type: 'boolean' },
        assumptions: { type: 'array', items: { type: 'string' } },
        evidence_status: { type: 'string' },
        differentiators: { type: 'string' },
        upside: { type: 'string' },
        risks: { type: 'string' },
        cheapest_discriminator_test: { type: 'string' },
        kill_criterion: { type: 'string' },
      }, required: ['option', 'is_null_option', 'assumptions', 'differentiators', 'upside', 'risks',
                    'cheapest_discriminator_test', 'kill_criterion'] },
    },
  },
  required: ['options'],
}

// ruling-set@1
const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    conflict_ledger: { type: 'array', items: { type: 'object', properties: {
      parties: { type: 'string' }, conflict: { type: 'string' },
      evidence_weight: { type: 'string' },                          // which side's [V]/[I] outweighs
      ruling: { type: 'string', enum: ['UPHELD', 'OVERRULED', 'UPHELD-WITH-QUALIFICATIONS', 'SPLIT'] },
      dissent_preserved: { type: 'string' },                        // the losing view, verbatim spirit
      justification: { type: 'string' } }, required: ['conflict', 'ruling', 'evidence_weight', 'dissent_preserved'] } },
    decisions: { type: 'array', items: { type: 'object', properties: {
      tier: { type: 'string', enum: ['P1', 'P2', 'P3', 'P4'] },
      decision: { type: 'string' }, acceptance: { type: 'string' } }, required: ['tier', 'decision', 'acceptance'] } },
    verdict: { type: 'string', enum: ['GO', 'CONDITIONAL', 'NO-GO'] },  // computed from the P1/P2 gate
    next_action: { type: 'string' },
    external_gate_owed: { type: 'boolean' },
  },
  required: ['conflict_ledger', 'decisions', 'verdict', 'next_action'],
}
const GATE_SCHEMA = {
  type: 'object',
  properties: {
    gate: { type: 'string' },
    result: { type: 'string', enum: ['PASS', 'BLOCK', 'PASS-WITH-NOTES'] },
    findings: { type: 'array', items: { type: 'string' } },
  },
  required: ['gate', 'result'],
}

function lensPrompt(a, optionsBlock) {
  return `Frozen dossier: read ${A.dossierPath} (evidence root ${A.evidenceRoot}). ` +
    `Subject: ${A.subjectOneLine} (axis: ${A.axis}). ` +
    `Rival hypotheses to weigh: ${A.hypotheses.join(' | ')}. ` +
    (optionsBlock ? `Generated alternatives to inspect (from the pre-panel generators):\n${optionsBlock}\n` : '') +
    `Your persona card ({{PERSONA_SPEC}}):\n${a.cardText}\n` +
    `Tiered evidence ([V]/[I]/[H]) and a structured falsifier (statement/method/threshold/timeframe) on every finding. Return structured output.`
}

// ---- Phase: Options (open axis only; generators run BEFORE and apart from the panel) ----
let optionSets = []
if (A.axis === 'open' && (A.generators || []).length) {
  phase('Options')
  optionSets = (await parallel(A.generators.map(g => () =>
    agent(`Frozen dossier: read ${A.dossierPath}. Subject (open question): ${A.subjectOneLine}. ` +
          `Your persona card ({{PERSONA_SPEC}}):\n${g.cardText}\n` +
          `Produce 3-5 materially distinct options, option 0 = steelmanned null/status-quo. Return structured output.`,
      { label: `gen:${g.persona}`, phase: 'Options', agentType: 'gauntlet-generator', schema: OPTION_SCHEMA })
      .then(r => ({ persona: g.persona, options: r.options }))
  ))).filter(Boolean)
  const nullPresent = optionSets.some(s => s.options.some(o => o.is_null_option))
  log(`option sets: ${optionSets.length}; null option present: ${nullPresent}`)
}
const optionsBlock = optionSets.length ? JSON.stringify(optionSets, null, 1) : ''

// ---- Phase: Lenses (barrier — independence is the whole point; lenses never see each other) ----
phase('Lenses')
const reports = await parallel(A.panel.map(a => () =>
  agent(lensPrompt(a, optionsBlock), {
    label: `lens:${a.role}:${a.persona}`,
    phase: 'Lenses',
    agentType: `gauntlet-${a.role}`,   // predefined role-agent, not general-purpose
    schema: LENS_SCHEMA,
  }).then(r => ({ persona: a.persona, role: a.role, report: r }))
)).then(rs => rs.filter(Boolean))

// ---- Phase: Verify (mechanical criticism; deterministic) ----
phase('Verify')
function falsifierOk(f) {
  return f && ['statement', 'method', 'threshold', 'timeframe'].every(k => f[k] && String(f[k]).trim())
}
function evidenceWeight(ev) {
  // accepted factual support requires at least one V or I ref; H-only = zero weight
  return (ev || []).some(e => e.tier === 'V' || e.tier === 'I')
}
const verified = reports.map(r => {
  const kept = (r.report.findings || []).filter(f => falsifierOk(f.falsifier))
  const zeroWeight = kept.filter(f => !evidenceWeight(f.evidence)).map(f => f.id)
  return { ...r, report: { ...r.report, findings: kept }, zero_weight_findings: zeroWeight }
})
log(`verified ${verified.length} lens reports; malformed-falsifier findings struck; ` +
    `${verified.reduce((n, v) => n + v.zero_weight_findings.length, 0)} H-only findings flagged zero-weight ` +
    `(run scripts/verify_evidence.py on saved reports for the [V] truth-check + Fingerprint)`)

// ---- Phase: Gate (categorical + process gates; a BLOCK is a verdict input the judge cannot trade away) ----
phase('Gate')
let gateResults = []
if ((A.gates || []).length) {
  gateResults = (await parallel(A.gates.map(g => () =>
    agent(`Subject: ${A.subjectOneLine}. Selection replay record: ${A.selectionPath}. ` +
          `Verified lens reports:\n${JSON.stringify(verified, null, 1)}\n` +
          `Your gate card ({{PERSONA_SPEC}}):\n${g.cardText}\nApply your gate. Return structured output.`,
      { label: `gate:${g.persona}`, phase: 'Gate', agentType: 'gauntlet-arbitrator', schema: GATE_SCHEMA })
  ))).filter(Boolean)
  log(`gates: ${gateResults.map(g => `${g.gate}=${g.result}`).join(', ')}`)
}

// ---- Phase: Arbitrate (the record is closed; no new evidence) ----
phase('Arbitrate')
const verdict = await agent(
  `You are the gauntlet final judge (${A.judgePersona || 'pragmatic-judge'}). Decide ON THE RECORD — no new evidence. ` +
  `Subject: ${A.subjectOneLine}. Rival hypotheses: ${A.hypotheses.join(' | ')}. ` +
  (optionsBlock ? `Generated option sets (open question):\n${optionsBlock}\n` : '') +
  `Gate results (a BLOCK is categorical — it caps the verdict at NO-GO for that path regardless of weighing):\n` +
  JSON.stringify(gateResults, null, 1) +
  `\nVerified independent lens reports (dissent to preserve, never average; H-only findings carry zero weight):\n` +
  JSON.stringify(verified, null, 1) +
  (A.judgeCardText ? `\nYour judge card ({{PERSONA_SPEC}}):\n${A.judgeCardText}` : '') +
  `\nBuild the Conflict Ledger with evidence weights + preserved dissent, assign P1-P4 with acceptance criteria, ` +
  `and COMPUTE the verdict from the gate: unresolved P1 -> NO-GO; P1 done + P2 open -> CONDITIONAL; P1+P2 accepted -> GO. ` +
  `Docket mode was ${A.docketMode}; independence ${A.independence}. Return structured output.`,
  { label: 'arbitrate', phase: 'Arbitrate', agentType: 'gauntlet-arbitrator', schema: VERDICT_SCHEMA, effort: 'high' }
)

return { subject: A.subjectOneLine, docketMode: A.docketMode, selectionPath: A.selectionPath,
         optionSets, gates: gateResults,
         lenses: verified.map(v => `${v.role}:${v.persona}`), verdict,
         spent_tokens: budget.spent() }
