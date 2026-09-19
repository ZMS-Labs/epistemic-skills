"""Synthetic completion controls against the actual Workflow template; no agent trial."""
import json
import subprocess
import unittest
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / 'assets/gauntlet-workflow.template.js'
NODE = r"""
const fs = require('fs');
const src = fs.readFileSync(process.argv[1], 'utf8').replace('export const meta', 'const meta');
const scenario = process.argv[2];
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const A = {dossierPath:'dossier',evidenceRoot:'evidence',subjectOneLine:'bounded synthetic review',
 axis:'fixed',docketMode:'manual-docket',independence:'synthetic',selectionPath:'selection.json',
 hypotheses:['one'],panel:[{role:'adversary',persona:'one',cardText:'one'},
 {role:'constructive',persona:'two',cardText:'two'},{role:'metatextual',persona:'three',cardText:'three'}],
 gates:scenario==='missing-gate'?[{persona:'required',cardText:'gate'}]:[]};
let calls=0;
const agent=async (prompt,o)=>{
 if(o.phase==='Lenses') {calls++;return {findings:scenario==='incomplete-finding' && calls===1
 ?[{id:'one:material',severity:'P1',claim:'not settled',evidence:[{tier:'V',ref:'a:1'}],falsifier:{}}]:[]};}
 if(o.phase==='Gate') return null;
 return {verdict:'GO',conflict_ledger:[],decisions:[],next_action:'continue'};
};
const parallel=async (jobs)=>{if(scenario==='partial-panel' && calls===0) return [];
 return Promise.all(jobs.map(j=>j()));};
(async()=>{try{const result=await new AsyncFunction('args','phase','agent','parallel','log','budget',src)
 (A,()=>{},agent,parallel,()=>{},{spent:()=>32});console.log(JSON.stringify({result}));}
 catch(e){console.log(JSON.stringify({error:e.message}));}})();
"""

class CompletionTests(unittest.TestCase):
    def run_case(self, case):
        result = subprocess.run(['node', '-e', NODE, str(TEMPLATE), case], capture_output=True,
                                encoding='utf-8', check=True)
        return json.loads(result.stdout)

    def test_complete_clean_control(self):
        self.assertEqual(self.run_case('complete')['result']['verdict']['verdict'], 'GO')

    def test_partial_panel_cannot_be_go(self):
        self.assertIn('INCOMPLETE', self.run_case('partial-panel').get('error', ''))

    def test_missing_gate_cannot_be_go(self):
        self.assertIn('INCOMPLETE', self.run_case('missing-gate').get('error', ''))

    def test_incomplete_material_finding_cannot_disappear(self):
        self.assertIn('INCOMPLETE', self.run_case('incomplete-finding').get('error', ''))

if __name__ == '__main__':
    unittest.main()
