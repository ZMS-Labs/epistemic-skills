#!/usr/bin/env python3
"""Behavioral fixtures for the generated portability planning contract."""
from __future__ import annotations
import importlib.util, json, subprocess, sys, tempfile, unittest
from unittest import mock
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
VALIDATOR_PATH=ROOT/'.github/scripts/validate_portability_contract.py'
CLAIM_A='p|s|b|r|U2|singleton-safe@1|e'
CLAIM_B='p2|s2|b2|r2|U2|singleton-safe@1|e2'
def load_validator():
 spec=importlib.util.spec_from_file_location('validate_portability_contract',VALIDATOR_PATH); module=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module); return module
def claim(**c):
 v={'record':'capability-claim@1','claim_key':CLAIM_A,'product':'p','surface':'s','resolved_release_or_build':'b','profile_revision':'r','achieved_tier':'U2','custody_capacity_policy_revision':'singleton-safe@1','evidence_epoch':'e','tier_evidence_set_digest':'evidence-set-a','tier_evidence_artifact_ids':['evidence-a'],'validity':'verified','capacity_policy':'singleton-safe@1','rendered_status':'current-usable'};v.update(c);return v
def requirements(**c):
 v={'record':'consumer-requirements@1','issuer_identity':'operator-1','decision_digest':'requirements-digest','content_digest':'requirements-content','census_content_digest':'census-content','authority_artifact_id':'authority-a','scope':'scope','revision':'1','required_consumers':[{'id':'consumer-a','minimum_tier':'U2'}],'publisher_consumers':[{'id':'publisher-a'},{'id':'publisher-b'}]};v.update(c);return v
def baseline(**c):
 v={'record':'support-baseline@1','revision':'1','requirements_revision':'1','requirements_decision_digest':'requirements-digest','requirements_content_digest':'requirements-content','census_content_digest':'census-content','authority_artifacts_digest':'authorities-content','tier_evidence_set_digest':'tier-evidence-content','stage_c_authority_set_digest':'stage-c-content','evidence_trust_root_digest':'trust-root-content','evidence_source_set_digest':'source-set-content','capability_claims_digest':'claims-content','conformance_results_digest':'results-content','content_digest':'baseline-content','consumers':[{'id':'consumer-a','disposition':'applicable','reason':'required','claim_key':CLAIM_A}],'success_terminal':'registry-disposition-complete'};v.update(c);return v
def conformance(**c):
 v={'record':'conformance-result@1','claim_key':CLAIM_A,'evidence_epoch':'e','tier_evidence_set_digest':'evidence-set-a','tier_evidence_artifact_ids':['evidence-a'],'claim_digest':'claim-digest-a','validity':'verified','outcome':'passed','success_terminal':'bounded-product-usable'};v.update(c);return v
def dag(**c):
 v={'record':'planning-dag@1','content_digest':'dag-content','bindings':{'requirements_content_digest':'r','baseline_content_digest':'b','census_content_digest':'c','authority_artifacts_digest':'a','transition_artifacts_digest':'t','tier_evidence_set_digest':'te','stage_c_authority_set_digest':'sc','evidence_trust_root_digest':'etr','evidence_source_set_digest':'ess','capability_claims_digest':'cc','conformance_results_digest':'cr'},'nodes':[{'id':'spike','stage':'A','kind':'stage-a-portability-spike','terminal':False},{'id':'prereq','stage':'A','kind':'concurrency-prerequisites','terminal':False},{'id':'design','stage':'A','kind':'frozen-successor-design','terminal':False},{'id':'go','stage':'A','kind':'gauntlet-go','terminal':False},{'id':'decision','stage':'A','kind':'operator-decision','terminal':False},{'id':'candidate','stage':'B','kind':'n-active-candidate','terminal':False},{'id':'promotion','stage':'C','kind':'promotion','terminal':True}],'edges':[{'from':'spike','to':'candidate','kind':'authority','mode':'template','transition_artifact':'spike-result'},{'from':'prereq','to':'candidate','kind':'authority','mode':'template','transition_artifact':'kernel-evidence'},{'from':'design','to':'candidate','kind':'authority','mode':'template','transition_artifact':'design'},{'from':'go','to':'candidate','kind':'authority','mode':'template','transition_artifact':'gauntlet'},{'from':'decision','to':'candidate','kind':'authority','mode':'template','transition_artifact':'decision'},{'from':'candidate','to':'promotion','kind':'authority','mode':'template','transition_artifact':'conformance'}]};v.update(c);return v
def invalidation(**c):
 v={'record':'evidence-invalidation-map@1','inventoried_targets':['canonical-source'],'mappings':[{'target':'canonical-source','affected_claim_keys':['consumer-a'],'probes':['probe'],'degraded_behavior':'demote-unverified','maximum_detection_bound':'PT1H','independent_record':'audit','successor_evidence_epoch':'next','reaward_rule':'all-probes-pass'}]};v.update(c);return v
def matrix(**c):
 cells=[]
 for operation in ('effect','verification-start','close-accept','install','upgrade','rollback','uninstall','duplicate-resolution','guarded-action'):
  for fault in ('timeout','crash','malformed-output','interruption','denied-evidence-retention'):
   for cut_class in ('before-mutation','partial-mutation','after-mutation-before-durable-evidence','after-durable-evidence-before-ack'):
    cells.append({'cut_id':'effect','operation':operation,'fault':fault,'cut_class':cut_class,'expected_protected_outcome':'blocked','expected_neighbor_outcome':'unaffected','maximum_timeout':'PT1M','permitted_durable_state':'none','forbidden_residue':'orphan','required_evidence':'receipt','recovery_procedure':'reconcile','recovery_attempt_budget':1,'recovery_time_budget':'PT1M','terminal':'fail-closed','tier_consequence':'demote-unverified'})
 v={'record':'operation-fault-matrix@1','material_boundaries':[{'cut_id':'effect','class':'durable-mutation'}],'cells':cells};v.update(c);return v
def inventory(**c):
 v={'record':'inventory-completeness@1','authored_inventory':[{'class':'runtime-bindings','items':['hook']}],'enumeration':{'independent':True,'status':'available','items':[{'class':'runtime-bindings','item':'hook'}]},'checkers':[{'identity':'checker','status':'available','consequence':'none','affected_claim_keys':[]}]};v.update(c);return v
class T(unittest.TestCase):
 def setUp(self): self.v=load_validator();self.d=tempfile.TemporaryDirectory()
 def tearDown(self): self.d.cleanup()
 def errors(self,**docs):
  paths={}
  for k,v in docs.items(): p=Path(self.d.name)/(k+'.json');p.write_text(json.dumps(v));paths[k]=p
  return self.v.validate_paths(paths)
 def reject(self,code,**docs): self.assertIn(code,self.errors(**docs))
 def cli(self,**docs):
  args=[sys.executable,str(VALIDATOR_PATH)]
  for kind,value in docs.items():
   values=value if kind in ('capability_claims','conformance_results') and isinstance(value,list) else [value]
   for index,item in enumerate(values):
    path=Path(self.d.name)/f'{kind}-{index}.json';path.write_text(json.dumps(item));args.extend(('--artifact',kind,str(path)))
  return subprocess.run(args,capture_output=True,text=True)
 def assert_cli_rejects(self,code,**docs):
  run=self.cli(**docs)
  self.assertNotEqual(0,run.returncode)
  self.assertNotIn('Traceback',run.stderr)
  self.assertIn(code,json.loads(run.stdout)['errors'])
 def test_missing_claim_dimension_is_rejected(self): x=claim();del x['evidence_epoch'];self.reject('CLAIM_MISSING_DIMENSION',capability_claim=x)
 def test_invalid_tier_capacity_pair_is_rejected(self): self.reject('CLAIM_TIER_CAPACITY',capability_claim=claim(claim_key='p|s|b|r|U5|singleton-safe@1|e',achieved_tier='U5'))
 def test_unverified_claim_cannot_render_currently_usable(self): self.reject('CLAIM_UNVERIFIED_USABLE',capability_claim=claim(validity='unverified'))
 def test_all_unverified_required_consumers_can_only_complete_registry(self):
  all_unverified=baseline(consumers=[{'id':'consumer-a','disposition':'unverified','reason':'not observed','claim_key':'consumer-a'}])
  self.assertEqual([],self.errors(requirements=requirements(),baseline=all_unverified))
  all_unverified['success_terminal']='bounded-product-usable'
  self.reject('BASELINE_PRODUCT_EVIDENCE_MISSING',requirements=requirements(),baseline=all_unverified)
 def test_missing_required_consumer_is_rejected(self): self.reject('BASELINE_REQUIRED_CONSUMER_MISSING',requirements=requirements(),baseline=baseline(consumers=[]))
 def test_unsigned_scope_reduction_is_rejected(self): self.reject('BASELINE_SCOPE_REDUCTION_UNSIGNED',requirements=requirements(),baseline=baseline(scope_reduction={'from_revision':'0'}))
 def test_reversed_planning_dag_authority_edge_is_rejected(self): self.reject('DAG_REVERSED_AUTHORITY_EDGE',planning_dag=dag(edges=[{'from':'promotion','to':'candidate','kind':'authority','transition_artifact':'x'}]))
 def test_inventoried_mutable_target_requires_invalidation_mapping(self): self.reject('INVALIDATION_TARGET_UNMAPPED',evidence_invalidation_map=invalidation(inventoried_targets=['canonical-source','served-bytes']))
 def test_material_effect_boundary_requires_stable_cut_id(self): self.reject('FAULT_MATERIAL_CUT_ID_MISSING',operation_fault_matrix=matrix(material_boundaries=[{'cut_id':'','class':'durable-mutation'}]))
 def test_authored_empty_inventory_requires_independent_enumeration(self): self.reject('INVENTORY_INDEPENDENT_ENUMERATION_REQUIRED',inventory_completeness=inventory(authored_inventory=[],enumeration={'independent':False,'status':'available','items':[]}))
 def test_unavailable_checker_must_demote_the_claim(self): self.reject('CHECKER_UNAVAILABLE_NO_DEMOTION',inventory_completeness=inventory(checkers=[{'identity':'checker','status':'unavailable','consequence':'none','affected_claim_keys':[]}]))
 def test_bare_harness_profile_is_rejected(self): self.reject('SCHEMA_REQUIRED',harness_profile={'record':'harness-profile@1'})
 def test_claim_requires_closed_rendered_status(self): x=claim();del x['rendered_status'];self.reject('SCHEMA_REQUIRED',capability_claim=x)
 def test_bounded_success_requires_current_claim_and_conformance(self): self.reject('BASELINE_PRODUCT_EVIDENCE_MISSING',requirements=requirements(),baseline=baseline(success_terminal='bounded-product-usable'),capability_claim=claim(),conformance_result=conformance(claim_key='wrong'))
 def test_nested_records_fail_closed(self): self.reject('DAG_NODE',planning_dag=dag(nodes=[{'id':'x','stage':'A','kind':'stage-a-portability-spike','terminal':False,'extra':True}]))
 def test_scope_reduction_binds_requirements_authority(self): self.reject('BASELINE_SCOPE_REDUCTION_UNBOUND',requirements=requirements(),baseline=baseline(scope_reduction={'requirements_revision':'wrong','requirements_decision_digest':'wrong','approval_decision':'operator-approved-scope-reduction','approval_digest':'approval','removed_consumers':['z']}))
 def test_checker_failure_demotes_affected_claim(self): self.reject('CHECKER_CLAIM_NOT_DEMOTED',inventory_completeness=inventory(checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}]),conformance_result=conformance())
 def test_inventory_reconciles_unexplained_discovery(self): self.reject('INVENTORY_UNEXPLAINED_DISCOVERY',inventory_completeness=inventory(enumeration={'independent':True,'status':'available','items':[{'class':'runtime-bindings','item':'surprise'}]}))
 def test_fault_cell_requires_full_recovery_oracle(self): x=matrix();del x['cells'][0]['maximum_timeout'];self.reject('FAULT_CELL',operation_fault_matrix=x)
 def test_non_object_inputs_return_stable_errors(self):
  self.reject('SCHEMA_DOCUMENT_NOT_OBJECT',requirements=[],baseline=[])
 def test_schema_rejects_full_key_wrong_types_and_enums(self):
  self.reject('SCHEMA_TYPE',harness_profile={'record':'harness-profile@1','product':7,'surface':'s','resolved_release_or_build':'b','profile_revision':'r','observation_date':'d','native_boundary':'imaginary'})
 def test_product_success_rejects_stale_requirements_binding(self):
  self.reject('BASELINE_REQUIREMENTS_STALE',requirements=requirements(),baseline=baseline(requirements_revision='0',success_terminal='bounded-product-usable'),capability_claim=claim(),conformance_result=conformance())
 def test_product_success_rejects_non_product_conformance_terminal(self):
  self.reject('BASELINE_PRODUCT_EVIDENCE_MISSING',requirements=requirements(),baseline=baseline(success_terminal='bounded-product-usable'),capability_claim=claim(),conformance_result=conformance(success_terminal='registry-disposition-complete'))
 def test_inventory_rejects_authored_but_unobserved_item(self):
  self.reject('INVENTORY_AUTHORED_UNOBSERVED',inventory_completeness=inventory(authored_inventory=[{'class':'runtime-bindings','items':['hook','missing']}]))
 def test_fault_denominator_rejects_arbitrary_fault_and_missing_cells(self):
  self.reject('FAULT_VOCABULARY',operation_fault_matrix=matrix(cells=[dict(matrix()['cells'][0],fault='anything')]))
 def test_fault_denominator_rejects_missing_and_duplicate_tuple(self):
  item=matrix();item['cells'].pop();self.reject('FAULT_DENOMINATOR_MISSING',operation_fault_matrix=item)
  item=matrix();item['cells'].append(dict(item['cells'][0]));self.reject('FAULT_DENOMINATOR_DUPLICATE',operation_fault_matrix=item)
 def test_cli_accepts_cross_record_arguments_and_reports_malformed_without_traceback(self):
  def put(name,value):
   path=Path(self.d.name)/name;path.write_text(json.dumps(value));return path
  malformed=put('bad.json',claim(claim_key='p|s|b|r|NOT-A-TIER|singleton-safe@1|e',achieved_tier='NOT-A-TIER'))
  run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--artifact','capability_claim',str(malformed)],capture_output=True,text=True)
  self.assertEqual(1,run.returncode);self.assertIn('CLAIM_VOCABULARY',json.loads(run.stdout)['errors']);self.assertNotIn('Traceback',run.stderr)
 def test_cli_malformed_cross_record_values_fail_closed_without_traceback(self):
  cases=(
   ('required-consumers-scalar','SCHEMA_TYPE',{'requirements':requirements(required_consumers=7),'baseline':baseline()}),
   ('required-consumers-map','SCHEMA_TYPE',{'requirements':requirements(required_consumers={'consumer-a':'U2'}),'baseline':baseline()}),
   ('claim-set-scalar','SCHEMA_TYPE',{'inventory_completeness':inventory(claim_set=7,checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}])}),
   ('claim-set-map','SCHEMA_TYPE',{'inventory_completeness':inventory(claim_set={'consumer-a':True},checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}])}),
   ('claim-key-list','SCHEMA_TYPE',{'capability_claims':[claim(claim_key=['consumer-a'])]}),
   ('claim-key-map','SCHEMA_TYPE',{'capability_claims':[claim(claim_key={'id':'consumer-a'})]}),
   ('result-key-list','SCHEMA_TYPE',{'conformance_results':[conformance(claim_key=['consumer-a'])]}),
   ('result-key-map','SCHEMA_TYPE',{'conformance_results':[conformance(claim_key={'id':'consumer-a'})]}),
   ('affected-keys-scalar','SCHEMA_TYPE',{'inventory_completeness':inventory(claim_set=['consumer-a'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':7}])}),
   ('affected-keys-map','SCHEMA_TYPE',{'inventory_completeness':inventory(claim_set=['consumer-a'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':{'consumer-a':True}}])}),
   ('fault-operation-list','SCHEMA_TYPE',{'operation_fault_matrix':matrix(cells=[dict(matrix()['cells'][0],operation=['effect'])])}),
   ('dag-node-id-list','SCHEMA_TYPE',{'planning_dag':dag(nodes=[{'id':['spike'],'stage':'A','kind':'stage-a-portability-spike','terminal':False}])}),
  )
  for name,code,docs in cases:
   with self.subTest(name=name): self.assert_cli_rejects(code,**docs)
 def test_cli_rejects_scalar_documents_for_every_accepted_artifact_kind(self):
  kinds=('capability_claim','requirements','baseline','planning_dag','harness_profile','evidence_invalidation_map','operation_fault_matrix','inventory_completeness','conformance_result','scope_approval','capability_claims','conformance_results')
  for kind in kinds:
   with self.subTest(kind=kind): self.assert_cli_rejects('SCHEMA_DOCUMENT_NOT_OBJECT',**{kind:17})
 def test_acyclic_missing_n_active_prerequisite_is_rejected(self):
  x=dag();x['edges']=[edge for edge in x['edges'] if edge['from']!='decision'];self.reject('DAG_N_ACTIVE_PREREQUISITE_MISSING',planning_dag=x)
 def test_scope_reduction_requires_separate_exact_approval(self):
  reduced=baseline(scope_reduction={'requirements_revision':'1','requirements_decision_digest':'requirements-digest','approval_decision':'operator-approved-scope-reduction','approval_digest':'x','removed_consumers':['consumer-a']})
  self.reject('SCOPE_APPROVAL_MISSING',requirements=requirements(),baseline=reduced)
 def test_scope_reduction_rejects_overbroad_approval(self):
  reduced=baseline(scope_reduction={'requirements_revision':'1','requirements_decision_digest':'requirements-digest','approval_decision':'operator-approved-scope-reduction','approval_digest':'x','removed_consumers':['consumer-a']})
  approval={'record':'scope-approval@1','approval_id':'a','issuer_identity':'operator-1','requirements_revision':'1','requirements_decision_digest':'requirements-digest','baseline_revision':'1','approved_removed_consumers':['consumer-a','consumer-z'],'approver_identity':'operator-2','authority':'operator','decision_digest':'d','evidence_reference':'e','evidence_epoch':'epoch'}
  self.reject('SCOPE_APPROVAL_OVERBROAD',requirements=requirements(),baseline=reduced,scope_approval=approval)
 def test_checker_demotes_every_affected_claim_and_result(self):
  affected=inventory(claim_set=['consumer-a','consumer-b'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a','consumer-b']}])
  self.reject('CHECKER_CLAIM_NOT_DEMOTED',inventory_completeness=affected,capability_claims=[claim(validity='unverified',rendered_status='not-usable'),claim(claim_key='consumer-b')],conformance_results=[conformance(validity='unverified',outcome='unverified'),conformance(claim_key='consumer-b')])
 def test_cli_accepts_complete_checker_demotion_without_singular_result(self):
  affected=inventory(claim_set=[CLAIM_A,CLAIM_B],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':[CLAIM_A,CLAIM_B]}])
  claims=[claim(validity='unverified',rendered_status='not-usable'),claim(claim_key=CLAIM_B,product='p2',surface='s2',resolved_release_or_build='b2',profile_revision='r2',evidence_epoch='e2',tier_evidence_artifact_ids=['evidence-b'],validity='unverified',rendered_status='not-usable')]
  results=[conformance(validity='unverified',outcome='unverified'),conformance(claim_key=CLAIM_B,evidence_epoch='e2',tier_evidence_artifact_ids=['evidence-b'],claim_digest='claim-digest-b',validity='unverified',outcome='unverified')]
  run=self.cli(inventory_completeness=affected,capability_claims=claims,conformance_results=results)
  self.assertEqual(0,run.returncode,run.stdout+run.stderr)
  self.assertEqual({'errors':[],'valid':True},json.loads(run.stdout))
 def test_cli_rejects_incomplete_checker_demotion_set(self):
  affected=inventory(claim_set=['consumer-a','consumer-b'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a','consumer-b']}])
  self.assert_cli_rejects('CHECKER_CLAIM_SET_INCOMPLETE',inventory_completeness=affected,capability_claims=[claim(validity='unverified',rendered_status='not-usable')],conformance_results=[conformance(validity='unverified',outcome='unverified')])
 def test_cli_rejects_duplicate_checker_demotion_keys(self):
  affected=inventory(claim_set=['consumer-a'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}])
  self.assert_cli_rejects('CHECKER_DUPLICATE_CLAIM_KEY',inventory_completeness=affected,capability_claims=[claim(validity='unverified',rendered_status='not-usable'),claim(validity='unverified',rendered_status='not-usable')],conformance_results=[conformance(validity='unverified',outcome='unverified')])
 def test_cli_rejects_wrong_state_checker_demotion(self):
  affected=inventory(claim_set=['consumer-a'],checkers=[{'identity':'checker','status':'error','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}])
  self.assert_cli_rejects('CHECKER_CLAIM_NOT_DEMOTED',inventory_completeness=affected,capability_claims=[claim()],conformance_results=[conformance()])
 def test_checker_requires_complete_claim_set(self):
  affected=inventory(checkers=[{'identity':'checker','status':'unavailable','consequence':'demote-unverified','affected_claim_keys':['consumer-a']}])
  self.reject('CHECKER_CLAIM_SET_INCOMPLETE',inventory_completeness=affected,capability_claims=[claim(validity='unverified',rendered_status='not-usable')],conformance_results=[conformance(validity='unverified',outcome='unverified')])
 def test_dag_rejects_gate_bypass_path(self):
  x=dag();x['nodes'].append({'id':'root','stage':'A','kind':'contract','terminal':False});x['edges'].append({'from':'root','to':'promotion','kind':'authority','transition_artifact':'bypass'});self.reject('DAG_GATE_BYPASS',planning_dag=x)
 def test_dag_rejects_candidate_reachable_without_each_gate(self):
  x=dag();x['nodes'].append({'id':'root','stage':'A','kind':'contract','terminal':False});x['edges'].append({'from':'root','to':'candidate','kind':'authority','transition_artifact':'bypass'});self.reject('DAG_GATE_BYPASS',planning_dag=x)
 def test_dag_accepts_dominating_multi_branch_gate(self):
  x={'record':'planning-dag@1','nodes':[{'id':'root','stage':'A','kind':'contract','terminal':False},{'id':'spike','stage':'A','kind':'stage-a-portability-spike','terminal':False},{'id':'prereq','stage':'A','kind':'concurrency-prerequisites','terminal':False},{'id':'design','stage':'A','kind':'frozen-successor-design','terminal':False},{'id':'go','stage':'A','kind':'gauntlet-go','terminal':False},{'id':'decision','stage':'A','kind':'operator-decision','terminal':False},{'id':'candidate','stage':'B','kind':'n-active-candidate','terminal':False},{'id':'promotion','stage':'C','kind':'promotion','terminal':True}], 'edges':[{'from':'root','to':'spike','kind':'authority','transition_artifact':'a'},{'from':'spike','to':'prereq','kind':'authority','transition_artifact':'a'},{'from':'prereq','to':'design','kind':'authority','transition_artifact':'a'},{'from':'design','to':'go','kind':'authority','transition_artifact':'a'},{'from':'go','to':'decision','kind':'authority','transition_artifact':'a'},{'from':'decision','to':'candidate','kind':'authority','transition_artifact':'a'},{'from':'candidate','to':'promotion','kind':'authority','transition_artifact':'a'}]}
  x.update(content_digest='dag-content',bindings={'requirements_content_digest':'r','baseline_content_digest':'b','census_content_digest':'c','authority_artifacts_digest':'a','transition_artifacts_digest':'t','tier_evidence_set_digest':'te','stage_c_authority_set_digest':'sc','evidence_trust_root_digest':'etr','evidence_source_set_digest':'ess','capability_claims_digest':'cc','conformance_results_digest':'cr'})
  for edge in x['edges']:edge['mode']='template'
  self.assertEqual([],self.errors(planning_dag=x))
 def test_dag_cycle_and_missing_n_active_prerequisite_are_rejected(self):
  x=dag();x['edges'].append({'from':'promotion','to':'spike','kind':'authority','transition_artifact':'cycle'});self.reject('DAG_CYCLE',planning_dag=x)
 def test_fault_schema_is_the_runtime_vocabulary_source(self):
  schemas=self.v.load_contract_schemas()
  vocabulary=self.v.fault_vocabulary(schemas['operation_fault_matrix'])
  cell_properties=schemas['operation_fault_matrix']['properties']['cells']['items']['properties']
  self.assertEqual(tuple(cell_properties['operation']['enum']),vocabulary['operation'])
  self.assertEqual(tuple(cell_properties['fault']['enum']),vocabulary['fault'])
  self.assertEqual(tuple(cell_properties['cut_class']['enum']),vocabulary['cut_class'])
  bad=matrix();bad['cells'][0]['fault']='arbitrary-fault'
  self.assertIn('SCHEMA_ENUM',self.v.schema_errors(schemas['operation_fault_matrix'],bad))

class Task2AuthoritativeSet(unittest.TestCase):
 def setUp(self):
  self.v=load_validator()
  self.root=ROOT/'packaging/portability'

 def test_executable_graph_reaches_only_current_stage_a_terminal(self):
  report=self.v.validate_root_report(self.root)
  self.assertEqual([],report['errors'])
  self.assertIn('stage-a-portability-spike',report['live_reachable'])
  self.assertNotIn('stage-a-decision-ready-not-usable',report['live_reachable'])
  self.assertNotIn('n-active-candidate',report['live_reachable'])
  self.assertNotIn('singleton-bounded-exact-claim',report['live_reachable'])
  self.assertNotIn('n-active-bounded-exact-claim',report['live_reachable'])
  self.assertFalse(report['n_active_awarded'])

 def test_stage_a_evidence_is_rejected_by_each_later_consumer(self):
  digest='a'*64;reference='stage-a-portability-spike@sha256:'+digest
  cases=(
   ('conformance_results',[{'evidence_reference':reference}],'STAGE_A_EVIDENCE_FORBIDDEN_EXACT_CONFORMANCE'),
   ('tier_evidence',{'artifacts':[{'evidence_reference':reference}]},'STAGE_A_EVIDENCE_FORBIDDEN_TIER_AWARD'),
   ('transitions',{'artifacts':[{'authority_resolution':{'evidence_reference':reference}}]},'STAGE_A_EVIDENCE_FORBIDDEN_PROMOTION'),
   ('capability_claims',[{'evidence_reference':reference}],'STAGE_A_EVIDENCE_FORBIDDEN_CURRENT_USABILITY'),
  )
  for key,value,code in cases:
   with self.subTest(key=key):
    bundle={'conformance_results':[],'tier_evidence':{'artifacts':[]},'transitions':{'artifacts':[]},'capability_claims':[],'baseline':{}}
    bundle[key]=value
    self.assertEqual([code],self.v.stage_a_reuse_errors(bundle,digest))

 def test_stage_a_current_bindings_are_recomputed(self):
  import copy
  original=self.v.load_root_bundle(self.root)
  probes=[]
  changed=copy.deepcopy(original);changed['stage_a_epoch']['current_epoch']='stale';probes.append(('STAGE_A_EVIDENCE_EPOCH_STALE',changed))
  changed=copy.deepcopy(original);changed['stage_a_spike']['planning_dag_content_digest']='0'*64;probes.append(('STAGE_A_DAG_BINDING_STALE',changed))
  changed=copy.deepcopy(original);changed['stage_a_spike']['affected_dag_edges']=changed['stage_a_spike']['affected_dag_edges'][:-1];probes.append(('STAGE_A_EDGE_CLOSURE_MISMATCH',changed))
  changed=copy.deepcopy(original);changed['stage_a_bundle']['request_digest']='0'*64;probes.append(('STAGE_A_BUNDLE_REQUEST_DIGEST_MISMATCH',changed))
  for code,bundle in probes:
   with self.subTest(code=code):self.assertIn(code,self.v.validate_root_bundle(bundle)['errors'])

 def test_missing_scalar_and_malformed_stage_a_default_block_every_downstream_edge(self):
  import copy
  original=self.v.load_root_bundle(self.root);downstream='stage-a-decision-ready-not-usable'
  cases=[]
  changed=copy.deepcopy(original);changed.pop('stage_a_spike');cases.append(changed)
  changed=copy.deepcopy(original);changed['stage_a_spike']=17;cases.append(changed)
  changed=copy.deepcopy(original);changed['stage_a_spike']={'record':'stage-a-portability-spike@1'};cases.append(changed)
  for bundle in cases:
   report=self.v.validate_root_bundle(bundle)
   self.assertTrue(report['errors']);self.assertNotIn(downstream,report['live_reachable']);self.assertNotIn(downstream,report['template_reachable'])

 def test_authoritative_registry_is_exact_and_unresolved_profiles_have_no_u0(self):
  bundle=self.v.load_root_bundle(self.root)
  requirements_doc=bundle['requirements'];baseline_doc=bundle['baseline']
  fleet_surfaces={'codex','claude_code','cursor_agent','gemini','kimi_code','aider','litellm','hermes','ollama','openclaw_memory','openclaw_browser','openclaw_voice','openclaw_phone','acp_runtime','discord_gateway','signal_gateway','imessage_gateway','vllm','deepseek_harness'}
  required=[self.v.parse_consumer_key(item['id']) for item in requirements_doc['required_consumers']]
  self.assertEqual(fleet_surfaces,{item['surface'] for item in required if item['registry_class']=='fleet'})
  self.assertEqual({'antigravity'},{item['surface'] for item in required if item['registry_class']=='external'})
  self.assertEqual('registry-disposition-complete',baseline_doc['success_terminal'])
  for item in baseline_doc['consumers']:
   address=self.v.parse_baseline_address(item['claim_key'],self.v.runtime_vocabulary(bundle['vocabulary']))
   if item['disposition']!='applicable':
    self.assertEqual('profile',address['address_type']);self.assertNotIn('achieved_tier',address)

 def test_every_invalid_fixture_is_complete_and_isolated(self):
  expected={'reverse-order':'DAG_REVERSED_AUTHORITY_EDGE','omitted-consumer':'BASELINE_REQUIRED_CONSUMER_MISSING','hidden-failure':'BASELINE_EVIDENCE_REFERENCE_UNRESOLVED','scope-reduction-without-exact-approval':'SCOPE_APPROVAL_MISSING','all-unverified-success':'BASELINE_ALL_UNVERIFIED_PRODUCT_SUCCESS','applicable-unverified-evidence':'BASELINE_APPLICABLE_UNVERIFIED','premature-n-active':'DAG_N_ACTIVE_PREMATURE','bypass':'DAG_GATE_BYPASS','duplicate-consumer-id':'REGISTRY_DUPLICATE_CONSUMER_KEY','duplicate-json-member':'DUPLICATE_JSON_MEMBER','stale-authority':'BASELINE_REQUIREMENTS_STALE','kernel-bypass-drift':'DAG_KERNEL_DRIFT_NOT_DOMINATING','kernel-bypass-regex':'DAG_KERNEL_REGEX_NOT_DOMINATING','kernel-bypass-fail-open-duplicate':'DAG_KERNEL_FAIL_OPEN_DUPLICATE_NOT_DOMINATING','kernel-bypass-charter':'DAG_KERNEL_CHARTER_NOT_DOMINATING','live-unresolved-edge':'DAG_LIVE_EDGE_UNRESOLVED','template-resolved-edge':'DAG_TEMPLATE_EDGE_RESOLVED','claim-key-product-mismatch':'CLAIM_KEY_PRODUCT_MISMATCH','claim-key-surface-mismatch':'CLAIM_KEY_SURFACE_MISMATCH','claim-key-release-mismatch':'CLAIM_KEY_RELEASE_MISMATCH','claim-key-profile-mismatch':'CLAIM_KEY_PROFILE_MISMATCH','claim-key-tier-mismatch':'CLAIM_KEY_TIER_MISMATCH','claim-key-capacity-mismatch':'CLAIM_KEY_CAPACITY_MISMATCH','claim-key-epoch-mismatch':'CLAIM_KEY_EPOCH_MISMATCH','u3-evidence-missing':'TIER_EVIDENCE_INCOMPLETE','u4-evidence-missing':'TIER_EVIDENCE_INCOMPLETE','conformance-epoch-mismatch':'CONFORMANCE_EPOCH_MISMATCH','conformance-evidence-mismatch':'CONFORMANCE_EVIDENCE_MISMATCH','capability-claim-set-tamper':'CAPABILITY_CLAIMS_DIGEST_MISMATCH','conformance-result-set-tamper':'CONFORMANCE_RESULTS_DIGEST_MISMATCH'}
  expected.update({'stage-c-self-promotion-relabel':'STAGE_C_AUTHORITY_UNRESOLVED','stage-c-duty-collision':'STAGE_C_DUTY_SEPARATION_INVALID','tier-evidence-self-asserted-boolean':'TIER_EVIDENCE_SELF_ASSERTED','tier-evidence-self-asserted-string':'TIER_EVIDENCE_REFERENCE_UNRESOLVED','tier-evidence-relabel-redigest':'TIER_EVIDENCE_AUTHORITY_CONTEXT_MISMATCH','registry-class-mutation':'REGISTRY_EXACT_KEY_SET_MISMATCH','registry-product-mutation':'REGISTRY_EXACT_KEY_SET_MISMATCH','registry-surface-mutation':'REGISTRY_EXACT_KEY_SET_MISMATCH','registry-channel-mutation':'REGISTRY_EXACT_KEY_SET_MISMATCH','registry-profile-mutation':'REGISTRY_EXACT_KEY_SET_MISMATCH','registry-extra-key':'REGISTRY_EXACT_KEY_SET_MISMATCH'})
  expected.update({'authoritative-prefix-self-authored':'AUTHORITATIVE_EVIDENCE_SOURCE_UNRESOLVED','stage-c-duplicate-type':'STAGE_C_AUTHORITY_CARDINALITY_INVALID','tier-evidence-duplicate-type':'TIER_EVIDENCE_TYPE_CARDINALITY_INVALID','tier-evidence-unreferenced-replay':'TIER_EVIDENCE_SET_NOT_EXACT','stage-c-outcome-conformance-failed':'STAGE_C_OUTCOME_INVALID','stage-c-outcome-ci-failed':'STAGE_C_OUTCOME_INVALID','stage-c-outcome-acceptance-rejected':'STAGE_C_OUTCOME_INVALID','stage-c-outcome-promotion-rejected':'STAGE_C_OUTCOME_INVALID','stage-c-outcome-control-disabled':'STAGE_C_OUTCOME_INVALID','stage-c-outcome-audit-missing':'STAGE_C_OUTCOME_INVALID'})
  invalid_root=self.root/'tests/invalid'
  self.assertEqual(set(expected),{path.name for path in invalid_root.iterdir() if path.is_dir()})
  for name,code in expected.items():
   with self.subTest(fixture=name):
    self.assertTrue((invalid_root/name/'fixture-manifest.json').is_file())
    self.assertEqual([code],self.v.validate_fixture(self.root,invalid_root/name))
    self.assertEqual(code,(invalid_root/name/'expected-error.txt').read_text().strip())

 def test_valid_fixtures_are_nontrivial_and_do_not_award_n_active(self):
  valid_root=self.root/'tests/valid';fixtures={path.name:path for path in valid_root.iterdir() if path.is_dir()}
  self.assertEqual({'authoritative-registry','bounded-multi-consumer','authoritative-equivalence-u3-u4'},set(fixtures))
  reports={name:self.v.validate_fixture_report(self.root,path) for name,path in fixtures.items()}
  self.assertEqual([],reports['authoritative-registry']['errors']);self.assertEqual([],reports['bounded-multi-consumer']['errors'])
  self.assertEqual([],reports['authoritative-equivalence-u3-u4']['errors'])
  self.assertEqual('registry-disposition-complete',reports['authoritative-registry']['bundle']['baseline']['success_terminal'])
  bounded=reports['bounded-multi-consumer']['bundle'];self.assertEqual('bounded-product-usable',bounded['baseline']['success_terminal'])
  self.assertEqual(2,len(bounded['capability_claims']));self.assertEqual(2,len(bounded['conformance_results']))
  self.assertTrue({'not_applicable','unsupported'}<={item['disposition'] for item in bounded['baseline']['consumers']})
  self.assertIn('singleton-bounded-exact-claim',reports['bounded-multi-consumer']['live_reachable'])
  for report in reports.values():
   self.assertNotIn('n-active-candidate',report['live_reachable']);self.assertNotIn('n-active-bounded-exact-claim',report['live_reachable']);self.assertFalse(report['n_active_awarded'])

 def test_claim_vocabulary_is_identical_to_root_local_schemas(self):
  bundle=self.v.load_root_bundle(self.root);self.assertEqual([],self.v.validate_vocabulary(bundle['vocabulary'],bundle['schemas']))

 def test_root_cli_is_cwd_relative_and_isolated_copy_self_contained(self):
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   tmp=Path(tmp);isolated=tmp/'isolated-portability';shutil.copytree(self.root,isolated);outside=tmp/'unrelated';outside.mkdir()
   run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--root',str(isolated)],cwd=outside,capture_output=True,text=True)
   self.assertEqual(0,run.returncode,run.stdout+run.stderr);result=json.loads(run.stdout);self.assertTrue(result['valid']);self.assertFalse(result['n_active_awarded'])

 def test_root_cli_fails_closed_without_traceback_for_bad_root_inputs(self):
  import shutil
  cases=(('missing','claim-vocabulary.json',None,'ARTIFACT_MISSING'),('malformed','support-baseline.json','{','ARTIFACT_JSON_UNREADABLE'),('wrong-type','consumer-requirements.json','17\n','SCHEMA_DOCUMENT_NOT_OBJECT'),('wrong-vocabulary-type','claim-vocabulary.json','[]\n','ARTIFACT_JSON_UNREADABLE'),('duplicate','consumer-requirements.json','{"record":"consumer-requirements@1","decision_digest":"a","decision_digest":"b"}\n','DUPLICATE_JSON_MEMBER'))
  for name,relative,content,code in cases:
   with self.subTest(name=name),tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp)/'root';shutil.copytree(self.root,target);path=target/relative
    if content is None:path.unlink()
    else:path.write_text(content)
    run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--root',str(target)],cwd=tmp,capture_output=True,text=True)
    self.assertNotEqual(0,run.returncode);self.assertNotIn('Traceback',run.stderr);self.assertIn(code,json.loads(run.stdout)['errors'])

 def test_authority_and_content_tampering_is_detected(self):
  import copy
  original=self.v.load_root_bundle(self.root);probes=[]
  changed=copy.deepcopy(original);changed['requirements']['required_consumers'][0]['minimum_tier']='U0';probes.append(('REQUIREMENTS_CONTENT_DIGEST_MISMATCH',changed))
  changed=copy.deepcopy(original);changed['requirements']['scope']='tampered scope';probes.append(('REQUIREMENTS_CONTENT_DIGEST_MISMATCH',changed))
  changed=copy.deepcopy(original);changed['baseline']['consumers'][0]['disposition']='unsupported';probes.append(('BASELINE_CONTENT_DIGEST_MISMATCH',changed))
  changed=copy.deepcopy(original);changed['planning_dag']['edges'][0]['transition_artifact']='missing-ref';probes.append(('DAG_TRANSITION_ARTIFACT_MISSING',changed))
  changed=copy.deepcopy(original);changed['transitions']['artifacts'][0]['content_digest']='0'*64;probes.append(('TRANSITION_ARTIFACT_DIGEST_MISMATCH',changed))
  changed=copy.deepcopy(original);artifact=changed['authorities']['artifacts'][0];artifact['issuer_identity']='unauthorized:attacker';artifact['content_digest']=self.v.record_digest(artifact);changed['authorities']['content_digest']=self.v.record_digest(changed['authorities']);probes.append(('AUTHORITY_ISSUER_UNAUTHORIZED',changed))
  changed=copy.deepcopy(original);artifact=changed['authorities']['artifacts'][2];artifact['rationale']='tampered but internally re-digested authority';artifact['content_digest']=self.v.record_digest(artifact);changed['authorities']['content_digest']=self.v.record_digest(changed['authorities']);probes.append(('BASELINE_AUTHORITY_BINDING_STALE',changed))
  for code,bundle in probes:
   with self.subTest(code=code):self.assertIn(code,self.v.validate_root_bundle(bundle)['errors'])

 def test_claim_key_is_derived_from_every_claim_dimension_and_tier_evidence(self):
  base=claim(claim_key='p|s|b|r|U2|singleton-safe@1|e')
  cases=(
   ('product','other','CLAIM_KEY_PRODUCT_MISMATCH'),
   ('surface','other','CLAIM_KEY_SURFACE_MISMATCH'),
   ('resolved_release_or_build','other','CLAIM_KEY_RELEASE_MISMATCH'),
   ('profile_revision','other','CLAIM_KEY_PROFILE_MISMATCH'),
   ('achieved_tier','U3','CLAIM_KEY_TIER_MISMATCH'),
   ('capacity_policy','n-active-unverified','CLAIM_KEY_CAPACITY_MISMATCH'),
   ('evidence_epoch','other','CLAIM_KEY_EPOCH_MISMATCH'),
  )
  for field,value,code in cases:
   changed=dict(base);changed[field]=value
   with self.subTest(field=field):self.assertIn(code,self.v.validate_documents({'capability_claim':changed}))
  self.assertIn('CLAIM_MISSING_DIMENSION',self.v.validate_documents({'capability_claim':claim(claim_key='p|s|b|r|U3|singleton-safe@1|e',achieved_tier='U3',tier_evidence_artifact_ids=[])}))
  self.assertIn('SCHEMA_UNKNOWN_FIELD',self.v.validate_documents({'capability_claim':claim(u3_evidence=True)}))

 def test_singleton_and_n_active_stage_c_routes_are_separate(self):
  report=self.v.validate_root_bundle(self.v.load_root_bundle(self.root));graph=report.get('structural_template_graph',{});filtered=report.get('template_graph',{})
  singleton_terminal='singleton-bounded-exact-claim';n_active_terminal='n-active-bounded-exact-claim'
  self.assertIn(singleton_terminal,self.v.reach(graph,'stage-a-decision-ready-not-usable'))
  self.assertTrue(self.v.reaches_without(graph,'stage-a-decision-ready-not-usable',singleton_terminal,'n-active-candidate'))
  self.assertIn(n_active_terminal,self.v.reach(graph,'n-active-candidate'))
  self.assertNotIn(singleton_terminal,self.v.reach(graph,'n-active-candidate'))
  self.assertNotIn(singleton_terminal,self.v.reach(filtered,'stage-a-portability-spike'));self.assertNotIn(n_active_terminal,self.v.reach(filtered,'stage-a-portability-spike'))

 def test_fixture_success_has_live_singleton_route_but_is_not_authoritative(self):
  fixture=self.root/'tests/valid/bounded-multi-consumer';report=self.v.validate_fixture_report(self.root,fixture)
  self.assertEqual([],report['errors']);self.assertIn('singleton-bounded-exact-claim',report['live_reachable']);self.assertNotIn('n-active-candidate',report['live_reachable'])
  authoritative_errors=self.v.validate_root_bundle(report['bundle'])['errors'];self.assertIn('FIXTURE_ONLY_AUTHORITY_FORBIDDEN',authoritative_errors);self.assertIn('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_UNRESOLVED',authoritative_errors)

 def test_authoritative_equivalence_u3_u4_uses_pinned_nonproduction_trust_root(self):
  fixture=self.root/'tests/valid/authoritative-equivalence-u3-u4';report=self.v.validate_fixture_report(self.root,fixture)
  self.assertEqual([],report['errors'])
  bundle=report['bundle'];self.assertEqual('non-production-authoritative-equivalence',bundle['evidence_trust_root']['environment'])
  self.assertEqual({'U3','U4'},{item['achieved_tier'] for item in bundle['capability_claims']})
  self.assertIn('singleton-bounded-exact-claim',report['live_reachable']);self.assertFalse(report['n_active_awarded'])
  self.assertIn('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_UNRESOLVED',self.v.validate_root_bundle(bundle,validation_context='authoritative')['errors'])

 def test_stage_c_and_tier_evidence_require_exact_type_and_global_id_closure(self):
  invalid=self.root/'tests/invalid'
  self.assertEqual(['STAGE_C_AUTHORITY_CARDINALITY_INVALID'],self.v.validate_fixture(self.root,invalid/'stage-c-duplicate-type'))
  self.assertEqual(['TIER_EVIDENCE_TYPE_CARDINALITY_INVALID'],self.v.validate_fixture(self.root,invalid/'tier-evidence-duplicate-type'))
  self.assertEqual(['TIER_EVIDENCE_SET_NOT_EXACT'],self.v.validate_fixture(self.root,invalid/'tier-evidence-unreferenced-replay'))

 def test_stage_c_outcomes_are_closed_per_record_type(self):
  invalid=self.root/'tests/invalid';names={
   'stage-c-outcome-conformance-failed','stage-c-outcome-ci-failed','stage-c-outcome-acceptance-rejected',
   'stage-c-outcome-promotion-rejected','stage-c-outcome-control-disabled','stage-c-outcome-audit-missing',
  }
  for name in names:
   with self.subTest(fixture=name):self.assertEqual(['STAGE_C_OUTCOME_INVALID'],self.v.validate_fixture(self.root,invalid/name))

 def test_authoritative_prefix_self_authorship_cannot_mint_trust(self):
  fixture=self.root/'tests/invalid/authoritative-prefix-self-authored';report=self.v.validate_fixture_report(self.root,fixture)
  self.assertEqual(['AUTHORITATIVE_EVIDENCE_SOURCE_UNRESOLVED'],report['errors'])

 def test_round4_trust_records_and_sources_are_closed(self):
  bundle=self.v.load_root_bundle(self.root);schemas=bundle['schemas']
  self.assertTrue({'evidence_trust_root','evidence_source','evidence_sources'}<=set(schemas))
  self.assertTrue({'evidence_trust_root','evidence_sources'}<=set(self.v.ROOT_FILES))
  trust=bundle['evidence_trust_root'];sources=bundle['evidence_sources']['sources']
  self.assertEqual(trust['source_set_digest'],bundle['evidence_sources']['content_digest'])
  self.assertEqual(set(trust['accepted_source_ids']),{item['id'] for item in sources})
  for source in sources:
   self.assertTrue(source['decision_root']);self.assertTrue(source['transparency_root'])
   self.assertGreaterEqual(source['retention_days'],1);self.assertEqual('retained',source['readback_outcome'])
   self.assertNotEqual(source['principal_identity'],source['readback_principal_identity'])

 def test_relabel_and_redigest_cannot_self_authorize_stage_c(self):
  import copy
  fixture=self.root/'tests/valid/bounded-multi-consumer';bundle=copy.deepcopy(self.v.validate_fixture_report(self.root,fixture)['bundle'])
  for artifact in bundle['transitions']['artifacts']:
   if artifact.get('success_binding') is not None:
    artifact['authority']='promotion-authority';artifact['referenced_record']='promotion-authority:'+artifact['subject_digest'];artifact['content_digest']=self.v.record_digest(artifact)
  bundle['transitions']['content_digest']=self.v.record_digest(bundle['transitions']);bundle['planning_dag']['bindings']['transition_artifacts_digest']=bundle['transitions']['content_digest'];bundle['planning_dag']['content_digest']=self.v.record_digest(bundle['planning_dag'])
  self.assertIn('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_UNRESOLVED',self.v.validate_root_bundle(bundle,validation_context='authoritative')['errors'])

 def test_round3_root_records_are_closed_and_fixture_evidence_is_typed(self):
  self.assertTrue({'stage_c_records','tier_evidence'}<=set(self.v.ROOT_FILES))
  bundle=self.v.validate_fixture_report(self.root,self.root/'tests/valid/bounded-multi-consumer').get('bundle',{})
  stage_c_types={item.get('record_type') for item in bundle.get('stage_c_records',{}).get('records',[])}
  self.assertEqual({'exact-candidate-conformance@1','exact-head-ci@1','independent-acceptance@1','operator-promotion-decision@1','stage-c-principal-control@1','independently-retained-audit@1'},stage_c_types)
  self.assertTrue(bundle.get('tier_evidence',{}).get('artifacts'))
  for claim_doc in bundle.get('capability_claims',[]):
   self.assertNotIn('u3_evidence',claim_doc);self.assertNotIn('u4_evidence',claim_doc)
   self.assertEqual(bundle['tier_evidence']['content_digest'],claim_doc.get('tier_evidence_set_digest'));self.assertTrue(claim_doc.get('tier_evidence_artifact_ids'))

 def test_registry_rejects_authorized_extra_key_with_allowed_surface(self):
  import copy
  changed=copy.deepcopy(self.v.load_root_bundle(self.root));source=next(item for item in changed['baseline']['consumers'] if 'chatgpt-plugin' in item['id']);decision=next(item for item in changed['authorities']['artifacts'] if item['id']==source['reason'])
  item=copy.deepcopy(source);item.update(id='fleet|invented-product|chatgpt-plugin|invented-channel|invented-profile@1',reason='invented-disposition',claim_key='profile|invented-product|chatgpt-plugin|unresolved-build|invented-profile@1|singleton-safe@1|unverified-initial-epoch@1')
  authority=copy.deepcopy(decision);authority.update(id=item['reason'],subject_id=item['id'],subject_digest=self.v.canonical_digest({'consumer_id':item['id'],'disposition':item['disposition'],'profile_address':item['claim_key']}),rationale='Adversarial extra consumer with an otherwise allowed publisher surface.');authority['content_digest']=self.v.record_digest(authority)
  changed['baseline']['consumers'].append(item);changed['authorities']['artifacts'].append(authority);changed['authorities']['content_digest']=self.v.record_digest(changed['authorities']);changed['baseline']['authority_artifacts_digest']=changed['authorities']['content_digest'];changed['baseline']['content_digest']=self.v.record_digest(changed['baseline']);changed['planning_dag']['bindings']['authority_artifacts_digest']=changed['authorities']['content_digest'];changed['planning_dag']['bindings']['baseline_content_digest']=changed['baseline']['content_digest'];changed['planning_dag']['content_digest']=self.v.record_digest(changed['planning_dag'])
  self.assertIn('REGISTRY_EXACT_KEY_SET_MISMATCH',self.v.validate_root_bundle(changed)['errors'])

 def test_conformance_and_complete_evidence_sets_are_bound(self):
  import copy
  fixture=self.root/'tests/valid/bounded-multi-consumer';base=self.v.validate_fixture_report(self.root,fixture)['bundle']
  probes=[]
  changed=copy.deepcopy(base);changed['conformance_results'][0]['evidence_epoch']='other';probes.append(('CONFORMANCE_EPOCH_MISMATCH',changed))
  changed=copy.deepcopy(base);changed['conformance_results'][0]['tier_evidence_set_digest']='0'*64;probes.append(('CONFORMANCE_EVIDENCE_MISMATCH',changed))
  changed=copy.deepcopy(base);changed['capability_claims'][0]['tier_evidence_set_digest']='0'*64;probes.append(('CAPABILITY_CLAIMS_DIGEST_MISMATCH',changed))
  changed=copy.deepcopy(base);changed['conformance_results'][0]['outcome']='failed';probes.append(('CONFORMANCE_RESULTS_DIGEST_MISMATCH',changed))
  for code,bundle in probes:
   try:errors=self.v.validate_root_bundle(bundle,validation_context='synthetic-positive-control')['errors']
   except TypeError:errors=[]
   with self.subTest(code=code):self.assertIn(code,errors)

 def test_root_only_record_schemas_are_closed_and_authoritative_bindings_required(self):
  bundle=self.v.load_root_bundle(self.root);schemas=bundle['schemas']
  self.assertTrue({'fleet_census','authority_artifact','authorities','transition_artifact','transitions','tier_evidence_artifact','tier_evidence','stage_c_record','stage_c_records','fixture_manifest','evidence_trust_root','evidence_source','evidence_sources'}<=set(schemas))
  self.assertTrue({'content_digest','census_content_digest','authority_artifact_id','publisher_consumers'}<=set(schemas['requirements']['required']))
  self.assertTrue({'content_digest','requirements_content_digest','census_content_digest','authority_artifacts_digest','tier_evidence_set_digest','stage_c_authority_set_digest','capability_claims_digest','conformance_results_digest'}<=set(schemas['baseline']['required']))
  self.assertTrue({'content_digest','bindings'}<=set(schemas['planning_dag']['required']))
  self.assertIn('mode',schemas['planning_dag']['properties']['edges']['items']['required'])
  bindings=schemas['planning_dag']['properties']['bindings'];self.assertFalse(bindings['additionalProperties']);self.assertEqual(set(bindings['required']),set(bindings['properties']))

 def test_redigested_semantic_authority_tamper_is_rejected(self):
  import copy
  original=self.v.load_root_bundle(self.root)
  cases=(('subject_id','wrong','AUTHORITY_SUBJECT_ID_MISMATCH'),('subject_kind','wrong','AUTHORITY_SUBJECT_KIND_MISMATCH'),('rationale','','AUTHORITY_RATIONALE_MISSING'),('referenced_record','wrong','AUTHORITY_REFERENCED_RECORD_MISMATCH'))
  for field,value,code in cases:
   changed=copy.deepcopy(original);artifact=changed['authorities']['artifacts'][2];artifact[field]=value;artifact['content_digest']=self.v.record_digest(artifact);changed['authorities']['content_digest']=self.v.record_digest(changed['authorities']);changed['baseline']['authority_artifacts_digest']=changed['authorities']['content_digest'];changed['baseline']['content_digest']=self.v.record_digest(changed['baseline']);changed['planning_dag']['bindings']['authority_artifacts_digest']=changed['authorities']['content_digest'];changed['planning_dag']['bindings']['baseline_content_digest']=changed['baseline']['content_digest'];changed['planning_dag']['content_digest']=self.v.record_digest(changed['planning_dag'])
   with self.subTest(field=field):self.assertIn(code,self.v.validate_root_bundle(changed)['errors'])

 def test_transition_subject_semantics_are_exact(self):
  import copy
  original=self.v.load_root_bundle(self.root)
  for artifact in original['transitions']['artifacts']:
   self.assertEqual('planning-dag-edge@1',artifact.get('subject_kind'))
   self.assertEqual(f"{artifact.get('from')}->{artifact.get('to')}",artifact.get('subject_id'))
  cases=(('subject_id','wrong','TRANSITION_SUBJECT_ID_MISMATCH'),('subject_kind','wrong','TRANSITION_SUBJECT_KIND_MISMATCH'),('referenced_record','wrong','TRANSITION_REFERENCED_RECORD_MISMATCH'),('rationale','','TRANSITION_RATIONALE_MISSING'))
  for field,value,code in cases:
   changed=copy.deepcopy(original);artifact=changed['transitions']['artifacts'][0];artifact[field]=value;artifact['content_digest']=self.v.record_digest(artifact);changed['transitions']['content_digest']=self.v.record_digest(changed['transitions']);changed['planning_dag']['bindings']['transition_artifacts_digest']=changed['transitions']['content_digest'];changed['planning_dag']['content_digest']=self.v.record_digest(changed['planning_dag'])
   with self.subTest(field=field):self.assertIn(code,self.v.validate_root_bundle(changed)['errors'])

 def test_minimal_authoritative_root_without_fixture_directories_is_total(self):
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   tmp=Path(tmp);target=tmp/'root';target.mkdir();shutil.copytree(self.root/'schemas',target/'schemas')
   shutil.copytree(self.root/'stage-a-evidence',target/'stage-a-evidence')
   for name in self.v.ROOT_FILES.values():shutil.copy2(self.root/name,target/name)
   outside=tmp/'outside';outside.mkdir();run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--root',str(target)],cwd=outside,capture_output=True,text=True)
   self.assertEqual(0,run.returncode,run.stdout+run.stderr);self.assertNotIn('Traceback',run.stderr);result=json.loads(run.stdout);self.assertTrue(result['valid']);self.assertEqual(0,result['invalid_fixtures_rejected']);self.assertEqual(0,result['valid_fixtures_accepted'])

 def test_root_cli_requires_replayable_stage_a_inputs(self):
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   target=Path(tmp)/'root';shutil.copytree(self.root,target)
   bundle=json.loads((target/'stage-a-portability-spike.bundle.json').read_text());object_path=bundle['artifact_resolvers']['source']['path']
   (target/Path(object_path).relative_to('packaging/portability')).unlink()
   run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--root',str(target)],capture_output=True,text=True)
   self.assertEqual(1,run.returncode,run.stdout+run.stderr);result=json.loads(run.stdout);self.assertIn('STAGE_A_EVIDENCE_OBJECT_MISSING',result['errors']);self.assertNotIn('stage-a-decision-ready-not-usable',result['live_reachable'])

 def test_stage_a_runner_load_failure_still_blocks_every_downstream_edge(self):
  bundle=self.v.load_root_bundle(self.root)
  with mock.patch.object(self.v,'load_stage_a_runner',side_effect=RuntimeError('unavailable')):
   report=self.v.validate_root_bundle(bundle)
  self.assertIn('STAGE_A_EDGE_CLOSURE_MISMATCH',report['errors']);self.assertNotIn('stage-a-decision-ready-not-usable',report['live_reachable']);self.assertNotIn('stage-a-decision-ready-not-usable',report['template_reachable']);self.assertNotIn('n-active-candidate',report['template_reachable'])

 def test_trusted_root_refuses_replaced_runner_verifier_and_combined_library_before_top_level_execution(self):
  import shutil
  for names in (('run_portability_spike.py',),('verify_portability_spike_bundle.py',),('run_portability_spike.py','verify_portability_spike_bundle.py'),('skill_artifact_lib.py','run_portability_spike.py'),('skill_artifact_lib.py','verify_portability_spike_bundle.py'),('skill_artifact_lib.py','run_portability_spike.py','verify_portability_spike_bundle.py')):
   with self.subTest(names=names),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);shutil.copytree(self.root,root/'packaging/portability');scripts=root/'.github/scripts';scripts.mkdir(parents=True)
    for filename in ('validate_portability_contract.py','run_portability_spike.py','verify_portability_spike_bundle.py','skill_artifact_lib.py'):
     shutil.copy2(ROOT/'.github/scripts'/filename,scripts/filename)
    marker=root/'executed'
    for filename in names:
     target=scripts/filename;sentinel=f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n".encode()
     target.write_bytes(target.read_bytes()+b'\n'+sentinel if filename=='skill_artifact_lib.py' else sentinel+target.read_bytes())
    run=subprocess.run([sys.executable,str(scripts/'validate_portability_contract.py'),'--root',str(root/'packaging/portability')],capture_output=True,text=True)
    self.assertEqual(1,run.returncode,run.stdout+run.stderr);self.assertFalse(marker.exists());self.assertIn('STAGE_A_ENTRYPOINT_UNAPPROVED',run.stdout)

 def test_trusted_root_runner_does_not_execute_replaced_ambient_artifact_library(self):
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);shutil.copytree(self.root,root/'packaging/portability');scripts=root/'.github/scripts';scripts.mkdir(parents=True)
   for filename in ('validate_portability_contract.py','run_portability_spike.py','verify_portability_spike_bundle.py','skill_artifact_lib.py'):
    shutil.copy2(ROOT/'.github/scripts'/filename,scripts/filename)
   marker=root/'executed';library=scripts/'skill_artifact_lib.py'
   library.write_bytes(library.read_bytes()+f"\nfrom pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n".encode())
   run=subprocess.run([sys.executable,str(scripts/'validate_portability_contract.py'),'--root',str(root/'packaging/portability')],capture_output=True,text=True)
   self.assertEqual(0,run.returncode,run.stdout+run.stderr);self.assertFalse(marker.exists())

 def test_trusted_root_rejects_preloaded_artifact_library_alias_before_use(self):
  import hashlib as _hashlib
  import types
  marker=Path(tempfile.mkdtemp())/'executed'
  self.addCleanup(lambda: __import__('shutil').rmtree(marker.parent,ignore_errors=True))
  class Poison(types.ModuleType):
   def __getattribute__(self,name):
    if name in {'ArtifactError','DuplicateJsonMember','canonical_json_bytes','load_json_strict','portable_tree_sha256','regular_files','sha256_bytes'}:marker.write_text('executed')
    return super().__getattribute__(name)
  poison=Poison('skill_artifact_lib');poison.ArtifactError=ValueError;poison.DuplicateJsonMember=ValueError
  poison.canonical_json_bytes=lambda value:(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();poison.load_json_strict=lambda path:json.loads(Path(path).read_text());poison.portable_tree_sha256=lambda path:'';poison.regular_files=lambda path:[];poison.sha256_bytes=lambda data:_hashlib.sha256(data).hexdigest()
  sentinel=object();prior=sys.modules.pop('skill_artifact_lib',sentinel);sys.modules['skill_artifact_lib']=poison
  try:report=self.v.validate_root_bundle(self.v.load_root_bundle(self.root))
  finally:
   sys.modules.pop('skill_artifact_lib',None)
   if prior is not sentinel:sys.modules['skill_artifact_lib']=prior
  self.assertFalse(marker.exists());self.assertIn('STAGE_A_ENTRYPOINT_UNAPPROVED',report['errors'])

 def test_pinned_loader_executes_the_approved_snapshot_after_path_replacement_and_normalizes_import_errors(self):
  import hashlib as _hashlib
  import shutil
  with tempfile.TemporaryDirectory() as tmp:
   scripts=Path(tmp)/'.github/scripts';scripts.mkdir(parents=True);shutil.copy2(VALIDATOR_PATH,scripts/'validate_portability_contract.py')
   spec=importlib.util.spec_from_file_location('isolated_validator',scripts/'validate_portability_contract.py');validator=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(validator)
   target=scripts/'loader_fixture.py';approved=b"snapshot = 'approved'\n";marker=Path(tmp)/'changed-executed';changed=f"from pathlib import Path\nPath({str(marker)!r}).write_text('changed')\nsnapshot = 'changed'\n".encode();target.write_bytes(approved)
   def replace_path(path):path.write_bytes(changed)
   loaded=validator.load_pinned_stage_a_module('loader_fixture.py','snapshot_fixture',_hashlib.sha256(approved).hexdigest(),allowed_imports=(),after_snapshot=replace_path)
   self.assertEqual('approved',loaded.snapshot);self.assertFalse(marker.exists());self.assertEqual(changed,target.read_bytes())
   broken=b"raise RuntimeError('unstable import detail')\n";target.write_bytes(broken)
   with self.assertRaisesRegex(ValueError,'^STAGE_A_ENTRYPOINT_UNAPPROVED$'):
    validator.load_pinned_stage_a_module('loader_fixture.py','broken_fixture',_hashlib.sha256(broken).hexdigest(),allowed_imports=())

 def test_literal_all_unverified_registry_fixture_is_isolated(self):
  fixture=self.root/'tests/invalid/all-unverified-success';bundle=self.v.load_fixture_bundle(self.root,fixture)
  self.assertEqual([],bundle['capability_claims']);self.assertEqual([],bundle['conformance_results']);self.assertTrue(all(item['disposition']=='unverified' and item['claim_key'].startswith('profile|') for item in bundle['baseline']['consumers']))
  self.assertEqual(['BASELINE_ALL_UNVERIFIED_PRODUCT_SUCCESS'],self.v.validate_fixture(self.root,fixture))
  applicable=self.root/'tests/invalid/applicable-unverified-evidence';self.assertEqual(['BASELINE_APPLICABLE_UNVERIFIED'],self.v.validate_fixture(self.root,applicable))

 def test_root_cli_reports_all_fixture_results(self):
  run=subprocess.run([sys.executable,str(VALIDATOR_PATH),'--root',str(self.root)],capture_output=True,text=True)
  self.assertEqual(0,run.returncode,run.stdout+run.stderr);result=json.loads(run.stdout)
  self.assertTrue(result['valid']);self.assertEqual(51,result['invalid_fixtures_rejected']);self.assertEqual(3,result['valid_fixtures_accepted']);self.assertFalse(result['n_active_awarded'])

if __name__=='__main__': unittest.main(verbosity=2)
