#!/usr/bin/env python3
"""Closed-vocabulary planning-contract validator (standard library only)."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path

PORTABILITY_DIR=Path(__file__).resolve().parents[2]/'packaging/portability'
VOCABULARY_PATH=PORTABILITY_DIR/'claim-vocabulary.json'
STAGE_A_RUNNER_SHA256="7b9db15350b0da4e9ae2eb3e5122abc5be79a7766cf53c86bfb2442d537e32e3"
STAGE_A_VERIFIER_SHA256="d8138fcad2bebedfef0a3068b44030a16b5d4eb9550c38ef063c67b3573fed2d"
STAGE_A_AUTHORITY_SHA256="2a1a18ac98973f9e4d6ead47c7fe81c9238044c190ee7b697d4688f480e2e46d"

class DuplicateJsonMember(ValueError):pass

def duplicate_rejecting_object(pairs):
 result={}
 for key,value in pairs:
  if key in result:raise DuplicateJsonMember(key)
  result[key]=value
 return result

def load_json_path(path):
 return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=duplicate_rejecting_object)

def load_claim_vocabulary(path=VOCABULARY_PATH):return load_json_path(path)

def runtime_vocabulary(vocabulary):
 compatibility=vocabulary.get('capacity_compatibility',{}) if isinstance(vocabulary,dict) else {}
 return {
  'tiers':tuple(vocabulary.get('cumulative_tiers',())),
  'validities':tuple(vocabulary.get('claim_states',())),
  'capacity':tuple(compatibility),
  'terminals':tuple(vocabulary.get('success_terminals',())),
  'consequences':tuple(vocabulary.get('invalidation_consequences',())),
  'classes':tuple(vocabulary.get('inventory_classes',())),
  'edge_kinds':tuple(vocabulary.get('edge_kinds',())),
 }

ARTIFACTS={'capability_claim':'capability-claim.schema.json','requirements':'consumer-requirements.schema.json','baseline':'support-baseline.schema.json','planning_dag':'planning-dag.schema.json','harness_profile':'harness-profile.schema.json','evidence_invalidation_map':'evidence-invalidation-map.schema.json','operation_fault_matrix':'operation-fault-matrix.schema.json','inventory_completeness':'inventory-completeness.schema.json','conformance_result':'conformance-result.schema.json','stage_a_spike':'stage-a-portability-spike.schema.json'}
ROOT_SCHEMAS={'fleet_census':'fleet-surface-census.schema.json','authority_artifact':'authority-artifact.schema.json','authorities':'authority-artifact-set.schema.json','transition_artifact':'transition-artifact.schema.json','transitions':'transition-artifact-set.schema.json','tier_evidence_artifact':'tier-evidence-artifact.schema.json','tier_evidence':'tier-evidence-set.schema.json','stage_c_record':'stage-c-authority-record.schema.json','stage_c_records':'stage-c-authority-set.schema.json','evidence_trust_root':'authoritative-evidence-trust-root.schema.json','evidence_source':'authoritative-evidence-source.schema.json','evidence_sources':'authoritative-evidence-source-set.schema.json','fixture_manifest':'portability-fixture.schema.json'}
SCHEMA_FILES={**ARTIFACTS,**ROOT_SCHEMAS}
SCHEMA_DIR=PORTABILITY_DIR/'schemas'
FIELDS={'capability_claim':{'record','claim_key','product','surface','resolved_release_or_build','profile_revision','achieved_tier','custody_capacity_policy_revision','evidence_epoch','tier_evidence_set_digest','tier_evidence_artifact_ids','validity','capacity_policy','rendered_status'},'requirements':{'record','issuer_identity','decision_digest','scope','revision','required_consumers','publisher_consumers','content_digest','census_content_digest','authority_artifact_id'},'baseline':{'record','revision','requirements_revision','requirements_decision_digest','requirements_content_digest','census_content_digest','authority_artifacts_digest','tier_evidence_set_digest','stage_c_authority_set_digest','evidence_trust_root_digest','evidence_source_set_digest','capability_claims_digest','conformance_results_digest','content_digest','consumers','success_terminal','scope_reduction'},'planning_dag':{'record','nodes','edges','bindings','content_digest'},'harness_profile':{'record','product','surface','resolved_release_or_build','profile_revision','observation_date','native_boundary'},'evidence_invalidation_map':{'record','inventoried_targets','mappings'},'operation_fault_matrix':{'record','material_boundaries','cells'},'inventory_completeness':{'record','authored_inventory','enumeration','checkers','claim_set'},'conformance_result':{'record','claim_key','evidence_epoch','tier_evidence_set_digest','tier_evidence_artifact_ids','claim_digest','validity','outcome','success_terminal'},'stage_a_spike':{'record','decision','evidence_epoch','input_digests','input_kinds','planning_dag_content_digest','affected_dag_edges','edge_dispositions','outcome_criteria','probe_observations','supersession_rule','evidence_class','admissible_for','not_evidence_for','decision_digest','content_digest'}}
REQUIRED={k:set(v) for k,v in FIELDS.items()}; REQUIRED['baseline']-= {'scope_reduction'}; REQUIRED['inventory_completeness']-= {'claim_set'}
def s(x): return isinstance(x,str) and bool(x.strip())
def add(e,c): e.append(c)
def basic(k,d,e):
 if not isinstance(d,dict): add(e,'SCHEMA_DOCUMENT_NOT_OBJECT');return False
 if set(d)-FIELDS[k]:add(e,'SCHEMA_UNKNOWN_FIELD')
 if REQUIRED[k]-set(d):add(e,'SCHEMA_REQUIRED')
 if d.get('record')!=ARTIFACTS[k].replace('.schema.json','@1'):add(e,'SCHEMA_RECORD')
 return True
def claim(d,e,rv):
 if not basic('capability_claim',d,e):return
 if not all(s(d.get(x)) for x in ('claim_key','product','surface','resolved_release_or_build','profile_revision','achieved_tier','custody_capacity_policy_revision','evidence_epoch','tier_evidence_set_digest')) or not isinstance(d.get('tier_evidence_artifact_ids'),list) or not d.get('tier_evidence_artifact_ids') or not all(s(x) for x in d.get('tier_evidence_artifact_ids',[])):add(e,'CLAIM_MISSING_DIMENSION')
 parts=d.get('claim_key','').split('|') if isinstance(d.get('claim_key'),str) else []
 dimensions=(('product','CLAIM_KEY_PRODUCT_MISMATCH'),('surface','CLAIM_KEY_SURFACE_MISMATCH'),('resolved_release_or_build','CLAIM_KEY_RELEASE_MISMATCH'),('profile_revision','CLAIM_KEY_PROFILE_MISMATCH'),('achieved_tier','CLAIM_KEY_TIER_MISMATCH'),('capacity_policy','CLAIM_KEY_CAPACITY_MISMATCH'),('evidence_epoch','CLAIM_KEY_EPOCH_MISMATCH'))
 if len(parts)!=7 or any(not part or '|' in str(d.get(field,'')) for (field,_),part in zip(dimensions,parts)):add(e,'CLAIM_KEY_ENCODING')
 else:
  mismatches=[code for ((field,code),part) in zip(dimensions,parts) if d.get(field)!=part]
  e.extend(mismatches)
  if mismatches:return
 if d.get('achieved_tier') not in rv['tiers'] or d.get('validity') not in rv['validities'] or d.get('capacity_policy') not in rv['capacity'] or d.get('custody_capacity_policy_revision')!=d.get('capacity_policy') or d.get('rendered_status') not in ('current-usable','historical-only','not-usable'):add(e,'CLAIM_VOCABULARY')
 if (d.get('capacity_policy')=='singleton-safe@1' and d.get('achieved_tier')=='U5') or (d.get('capacity_policy')=='n-active-unverified' and (d.get('achieved_tier') in rv['tiers'] or d.get('validity')=='verified')):add(e,'CLAIM_TIER_CAPACITY')
 if d.get('rendered_status')=='current-usable' and d.get('validity')!='verified':add(e,'CLAIM_UNVERIFIED_USABLE')
def req(d,e,rv):
 if not basic('requirements',d,e):return
 if not all(s(d.get(x)) for x in ('issuer_identity','decision_digest','scope','revision')):add(e,'REQUIREMENTS_MISSING_AUTHORITY')
 cs=d.get('required_consumers');
 if not isinstance(cs,list) or not cs:add(e,'REQUIREMENTS_REQUIRED_CONSUMERS');return
 for x in cs:
  if not isinstance(x,dict) or set(x)!={'id','minimum_tier'} or not s(x.get('id')) or x.get('minimum_tier') not in rv['tiers']:add(e,'REQUIREMENTS_CONSUMER')
def baseline(d,r,claim_,conf,e,rv):
 if not basic('baseline',d,e):return
 if not isinstance(r,dict):r=None
 if not isinstance(claim_,dict):claim_=None
 if not isinstance(conf,dict):conf=None
 cs=d.get('consumers');
 if not isinstance(cs,list):add(e,'BASELINE_CONSUMERS');return
 seen={};
 for x in cs:
  if not isinstance(x,dict) or set(x)!={'id','disposition','reason','claim_key'} or not s(x.get('id')) or x.get('disposition') not in ('applicable','not_applicable','unsupported','unverified') or not s(x.get('reason')) or (x['disposition']=='applicable' and not s(x.get('claim_key'))):add(e,'BASELINE_CONSUMER')
  elif x['id'] in seen:add(e,'REGISTRY_DUPLICATE_CONSUMER_KEY')
  else:seen[x['id']]=x
 if r:
  if d.get('requirements_revision')!=r.get('revision') or d.get('requirements_decision_digest')!=r.get('decision_digest'):add(e,'BASELINE_REQUIREMENTS_STALE')
  raw_required=r.get('required_consumers')
  required={x.get('id'):x.get('minimum_tier') for x in raw_required if isinstance(x,dict) and s(x.get('id'))} if isinstance(raw_required,list) else {}
  if not set(required)<=set(seen):add(e,'BASELINE_REQUIRED_CONSUMER_MISSING')
  if d.get('success_terminal')=='bounded-product-usable':
   for ident,tier in required.items():
    x=seen.get(ident,{});key=x.get('claim_key')
    achieved=claim_.get('achieved_tier') if claim_ else None
    if x.get('disposition')!='applicable' or not claim_ or not conf or claim_.get('claim_key')!=key or conf.get('claim_key')!=key or claim_.get('validity')!='verified' or conf.get('validity')!='verified' or conf.get('outcome')!='passed' or conf.get('success_terminal')!='bounded-product-usable' or claim_.get('rendered_status')!='current-usable' or achieved not in rv['tiers'] or tier not in rv['tiers'] or rv['tiers'].index(achieved)<rv['tiers'].index(tier):add(e,'BASELINE_PRODUCT_EVIDENCE_MISSING');break
 if d.get('success_terminal') not in rv['terminals']:add(e,'BASELINE_SUCCESS_TERMINAL')
 red=d.get('scope_reduction')
 if red is not None:
  need={'requirements_revision','requirements_decision_digest','approval_decision','approval_digest','removed_consumers'}
  if not isinstance(red,dict) or set(red)!=need or not s(red.get('approval_digest')) or red.get('approval_decision')!='operator-approved-scope-reduction' or not isinstance(red.get('removed_consumers'),list) or not all(s(item) for item in red.get('removed_consumers',[])):add(e,'BASELINE_SCOPE_REDUCTION_UNSIGNED')
  elif not r or red['requirements_revision']!=r.get('revision') or red['requirements_decision_digest']!=r.get('decision_digest'):add(e,'BASELINE_SCOPE_REDUCTION_UNBOUND')
def dag(d,e,rv):
 if not basic('planning_dag',d,e):return
 ns=d.get('nodes');es=d.get('edges'); nodes={}
 if not isinstance(ns,list) or not isinstance(es,list) or not ns or not es:add(e,'DAG_STRUCTURE');return
 for n in ns:
  if not isinstance(n,dict) or set(n)!={'id','stage','kind','terminal'} or not s(n.get('id')) or n.get('stage') not in ('A','B','C') or n.get('kind') not in ('stage-a-portability-spike','concurrency-prerequisites','frozen-successor-design','gauntlet-go','operator-decision','n-active-candidate','promotion','contract') or not isinstance(n.get('terminal'),bool):add(e,'DAG_NODE')
  else:nodes[n['id']]=n
 graph={k:[] for k in nodes}
 for x in es:
  if not isinstance(x,dict) or set(x) not in ({'from','to','kind','transition_artifact'},{'from','to','kind','mode','transition_artifact'}) or not s(x.get('from')) or not s(x.get('to')) or x.get('from') not in nodes or x.get('to') not in nodes or x.get('kind') not in rv['edge_kinds'] or ('mode'in x and x.get('mode') not in ('live','template')) or not s(x.get('transition_artifact')):add(e,'DAG_EDGE');continue
  graph[x['from']].append(x['to'])
  if nodes[x['from']]['stage']>nodes[x['to']]['stage']:add(e,'DAG_REVERSED_AUTHORITY_EDGE')
 def reach(src):
  out=set();todo=[src]
  while todo:
   a=todo.pop()
   for b in graph.get(a,[]):
    if b not in out:out.add(b);todo.append(b)
  return out
 for start in nodes:
  if start in reach(start):add(e,'DAG_CYCLE');break
 for n in nodes.values():
  if n['kind']=='n-active-candidate':
   ancestors={a for a in nodes if n['id'] in reach(a)}
   if not {'stage-a-portability-spike','concurrency-prerequisites','frozen-successor-design','gauntlet-go','operator-decision'} <= {nodes[a]['kind'] for a in ancestors}:add(e,'DAG_N_ACTIVE_PREREQUISITE_MISSING')
 # A promotion edge may pass through Stage-C evidence and acceptance nodes, but
 # its source must still descend from the N-active candidate.
 candidate_ids=[node_id for node_id,node in nodes.items() if node['kind']=='n-active-candidate']
 for edge in es:
  if isinstance(edge,dict) and s(edge.get('to')) and edge.get('to') in nodes and nodes[edge.get('to')]['kind']=='promotion' and s(edge.get('from')):
   from_n_active=any(edge.get('from')==candidate or edge.get('from') in reach(candidate) for candidate in candidate_ids)
   singleton_route=edge.get('from','').startswith('singleton-') and edge.get('to','').startswith('singleton-')
   if not from_n_active and not singleton_route:add(e,'DAG_GATE_BYPASS')
 # Require each named prerequisite to dominate every N-active candidate: after
 # removing a gate there must be no root-to-candidate path left.
 incoming={node_id:0 for node_id in nodes}
 for source, destinations in graph.items():
  for destination in destinations: incoming[destination]+=1
 roots=[node_id for node_id,count in incoming.items() if count==0]
 if len(roots)!=1:add(e,'DAG_ROOT_AMBIGUOUS')
 def reachable_without(start,target,blocked):
  if start==blocked:return False
  todo=[start];seen=set()
  while todo:
   current=todo.pop()
   if current==blocked or current in seen:continue
   if current==target:return True
   seen.add(current);todo.extend(graph.get(current,[]))
  return False
 for target in (node_id for node_id,node in nodes.items() if node['kind']=='n-active-candidate'):
  for gate_kind in ('stage-a-portability-spike','concurrency-prerequisites','frozen-successor-design','gauntlet-go','operator-decision'):
   gates=[node_id for node_id,node in nodes.items() if node['kind']==gate_kind and target in reach(node_id)]
   if not gates or any(reachable_without(root,target,gate) for gate in gates for root in roots):add(e,'DAG_GATE_BYPASS')
 if not any(n['terminal'] and n['id'] in set().union(*(reach(x) for x in nodes)) for n in nodes.values()):add(e,'DAG_TERMINAL_UNREACHABLE')
def invalid(d,e):
 if not basic('evidence_invalidation_map',d,e):return
 ts=d.get('inventoried_targets');ms=d.get('mappings');mapped=set(); need={'target','affected_claim_keys','probes','degraded_behavior','maximum_detection_bound','independent_record','successor_evidence_epoch','reaward_rule'}
 if not isinstance(ts,list) or not isinstance(ms,list):add(e,'INVALIDATION_STRUCTURE');return
 for x in ms:
  if not isinstance(x,dict) or set(x)!=need or not s(x.get('target')) or not all(isinstance(x.get(y),list) and x[y] for y in ('affected_claim_keys','probes')) or x.get('degraded_behavior') not in ('demote-unverified','fail-closed') or not all(s(x.get(y)) for y in need-{'target','affected_claim_keys','probes','degraded_behavior'}):add(e,'INVALIDATION_MAPPING')
  else:mapped.add(x['target'])
 if any(not s(x) or x not in mapped for x in ts):add(e,'INVALIDATION_TARGET_UNMAPPED')
def fault_vocabulary(schema):
 try: properties=schema['properties']['cells']['items']['properties']
 except (KeyError,TypeError):return {}
 vocabulary={}
 for name in ('operation','fault','cut_class'):
  values=properties.get(name,{}).get('enum')
  if not isinstance(values,list) or not values or not all(s(value) for value in values) or len(values)!=len(set(values)):return {}
  vocabulary[name]=tuple(values)
 return vocabulary
def fault(d,e,schema,rv):
 if not basic('operation_fault_matrix',d,e):return
 vocabulary=fault_vocabulary(schema)
 if set(vocabulary)!={'operation','fault','cut_class'}:add(e,'FAULT_SCHEMA_VOCABULARY_INVALID');return
 bs=d.get('material_boundaries');cs=d.get('cells'); cuts=set();fields={'cut_id','operation','fault','cut_class','expected_protected_outcome','expected_neighbor_outcome','maximum_timeout','permitted_durable_state','forbidden_residue','required_evidence','recovery_procedure','recovery_attempt_budget','recovery_time_budget','terminal','tier_consequence'}
 if not isinstance(bs,list) or not bs or not isinstance(cs,list) or not cs:add(e,'FAULT_MATRIX_STRUCTURE');return
 for x in bs:
  if not isinstance(x,dict) or set(x)!={'cut_id','class'} or not s(x.get('cut_id')) or x.get('class') not in ('durable-mutation','external-effect','evidence-publication','acknowledgement'):add(e,'FAULT_MATERIAL_CUT_ID_MISSING')
  else:cuts.add(x['cut_id'])
 got=set()
 for x in cs:
  if not isinstance(x,dict) or set(x)!=fields or not all(s(x.get(k)) for k in fields-{'recovery_attempt_budget'}) or not isinstance(x.get('recovery_attempt_budget'),int) or x['recovery_attempt_budget']<1 or x.get('tier_consequence') not in rv['consequences']:add(e,'FAULT_CELL')
  elif x.get('operation') not in vocabulary['operation'] or x.get('fault') not in vocabulary['fault'] or x.get('cut_class') not in vocabulary['cut_class']:add(e,'FAULT_VOCABULARY')
  else:
   key=(x['operation'],x['fault'],x['cut_class'])
   if key in got:add(e,'FAULT_DENOMINATOR_DUPLICATE')
   got.add(key)
 if not all(any(cell.get('cut_id')==cut for cell in cs if isinstance(cell,dict)) for cut in cuts):add(e,'FAULT_MATERIAL_CUT_UNCOVERED')
 required={(operation,fault,cut_class) for operation in vocabulary['operation'] for fault in vocabulary['fault'] for cut_class in vocabulary['cut_class']}
 if required-got:add(e,'FAULT_DENOMINATOR_MISSING')
 if got-required:add(e,'FAULT_DENOMINATOR_EXTRA')
def inventory(d,e,rv):
 if not basic('inventory_completeness',d,e):return
 a=d.get('authored_inventory');en=d.get('enumeration');ch=d.get('checkers')
 if not isinstance(a,list) or not isinstance(en,dict) or not isinstance(ch,list):add(e,'INVENTORY_STRUCTURE');return
 authored=set()
 for x in a:
  if not isinstance(x,dict) or set(x)!={'class','items'} or x.get('class') not in rv['classes'] or not isinstance(x.get('items'),list) or not all(s(i) for i in x['items']):add(e,'INVENTORY_CLASS')
  else:authored|={(x['class'],i) for i in x['items']}
 if set(en)!={'independent','status','items'} or en.get('independent') is not True or en.get('status')!='available' or not isinstance(en.get('items'),list):add(e,'INVENTORY_INDEPENDENT_ENUMERATION_REQUIRED')
 else:
  observed=set()
  for x in en['items']:
   if not isinstance(x,dict) or set(x)!={'class','item'} or x.get('class') not in rv['classes'] or not s(x.get('item')):add(e,'INVENTORY_ENUMERATION_ITEM')
   else:observed.add((x['class'],x['item']))
  if observed-authored:add(e,'INVENTORY_UNEXPLAINED_DISCOVERY')
  if authored-observed:add(e,'INVENTORY_AUTHORED_UNOBSERVED')
 for x in ch:
  if not isinstance(x,dict) or set(x)!={'identity','status','consequence','affected_claim_keys'} or not s(x.get('identity')) or x.get('status') not in ('available','unavailable','error') or x.get('consequence') not in rv['consequences'] or not isinstance(x.get('affected_claim_keys'),list):add(e,'CHECKER_STRUCTURE');continue
  if x['status'] in ('unavailable','error') and x['consequence']!='demote-unverified':add(e,'CHECKER_UNAVAILABLE_NO_DEMOTION')
def scope_approval_shape(approval,e):
 if not isinstance(approval,dict):add(e,'SCHEMA_DOCUMENT_NOT_OBJECT');return False
 fields={'record','approval_id','issuer_identity','requirements_revision','requirements_decision_digest','baseline_revision','approved_removed_consumers','approver_identity','authority','decision_digest','evidence_reference','evidence_epoch'}
 if set(approval)!=fields or approval.get('record')!='scope-approval@1' or not all(s(approval.get(k)) for k in fields-{'record','approved_removed_consumers'}) or not isinstance(approval.get('approved_removed_consumers'),list) or not all(s(x) for x in approval['approved_removed_consumers']):add(e,'SCOPE_APPROVAL_SHAPE');return False
 return True
def scope_approval(approval,baseline_doc,requirements_doc,e):
 reduction=baseline_doc.get('scope_reduction') if isinstance(baseline_doc,dict) else None
 if reduction is None:return
 if approval is None:add(e,'SCOPE_APPROVAL_MISSING');return
 if not scope_approval_shape(approval,e):return
 if not isinstance(requirements_doc,dict) or approval['issuer_identity']!=requirements_doc.get('issuer_identity') or approval['requirements_revision']!=requirements_doc.get('revision') or approval['requirements_decision_digest']!=requirements_doc.get('decision_digest') or approval['baseline_revision']!=baseline_doc.get('revision'):add(e,'SCOPE_APPROVAL_BINDING')
 if reduction.get('approval_digest')!=approval.get('decision_digest'):add(e,'SCOPE_APPROVAL_DIGEST_MISMATCH')
 removed_values=reduction.get('removed_consumers')
 if not isinstance(removed_values,list) or not all(s(item) for item in removed_values):add(e,'BASELINE_SCOPE_REDUCTION_UNSIGNED');return
 removed=set(removed_values);approved=set(approval['approved_removed_consumers'])
 if approved-removed:add(e,'SCOPE_APPROVAL_OVERBROAD')
 if removed-approved:add(e,'SCOPE_APPROVAL_MISSING_CELL')
def conf(d,e,rv):
 if not basic('conformance_result',d,e):return
 if not all(s(d.get(field)) for field in ('claim_key','evidence_epoch','tier_evidence_set_digest','claim_digest')) or not isinstance(d.get('tier_evidence_artifact_ids'),list) or not d.get('tier_evidence_artifact_ids') or not all(s(x) for x in d.get('tier_evidence_artifact_ids',[])):add(e,'CONFORMANCE_CLAIM_KEY')
 if d.get('validity') not in rv['validities'] or d.get('outcome') not in ('passed','failed','unverified') or d.get('success_terminal') not in rv['terminals']:add(e,'CONFORMANCE_VOCABULARY')
def load_contract_schemas(schema_dir=SCHEMA_DIR):
 return {kind:load_json_path(Path(schema_dir)/name) for kind,name in SCHEMA_FILES.items()}
def schema_errors(schema,value):
 errors=[]
 def walk(s,v):
  if 'const' in s and v!=s['const']:add(errors,'SCHEMA_CONST')
  if 'enum' in s and v not in s['enum']:add(errors,'SCHEMA_ENUM')
  typ=s.get('type')
  types={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),'string':lambda x:isinstance(x,str),'integer':lambda x:isinstance(x,int) and not isinstance(x,bool),'boolean':lambda x:isinstance(x,bool)}
  if typ and not types[typ](v):add(errors,'SCHEMA_TYPE');return
  if isinstance(v,str) and len(v)<s.get('minLength',0):add(errors,'SCHEMA_STRING_BOUND')
  if isinstance(v,(int,float)) and v<s.get('minimum',float('-inf')):add(errors,'SCHEMA_NUMERIC_BOUND')
  if isinstance(v,list):
   if len(v)<s.get('minItems',0):add(errors,'SCHEMA_ARRAY_BOUND')
   if 'items'in s:
    for item in v:walk(s['items'],item)
  if isinstance(v,dict):
   if any(k not in v for k in s.get('required',[])):add(errors,'SCHEMA_REQUIRED')
   props=s.get('properties',{})
   if s.get('additionalProperties') is False and set(v)-set(props):add(errors,'SCHEMA_UNKNOWN_FIELD')
   for k,sub in props.items():
    if k in v:walk(sub,v[k])
 walk(schema,value);return errors

def validate_vocabulary(vocabulary,schemas):
 e=[]
 required={'record','revision','claim_states','cumulative_tiers','capacity_compatibility','success_terminals','edge_kinds','inventory_classes','invalidation_consequences'}
 if not isinstance(vocabulary,dict) or set(vocabulary)!=required or vocabulary.get('record')!='claim-vocabulary@1' or not s(vocabulary.get('revision')):
  return ['VOCABULARY_SHAPE']
 runtime=runtime_vocabulary(vocabulary)
 for name in ('tiers','validities','capacity','terminals','consequences','classes','edge_kinds'):
  values=runtime[name]
  if not values and name!='capacity':add(e,'VOCABULARY_EMPTY')
  if len(values)!=len(set(values)) or not all(s(value) for value in values):add(e,'VOCABULARY_DUPLICATE_OR_INVALID')
 compatibility=vocabulary.get('capacity_compatibility')
 if not isinstance(compatibility,dict) or set(compatibility)!=set(runtime['capacity']):add(e,'VOCABULARY_CAPACITY_SHAPE')
 else:
  for policy,value in compatibility.items():
   if not isinstance(value,dict) or set(value)!={'awardable_tiers','n_active_service'} or not isinstance(value.get('awardable_tiers'),list) or not isinstance(value.get('n_active_service'),bool) or any(tier not in runtime['tiers'] for tier in value.get('awardable_tiers',[])):add(e,'VOCABULARY_CAPACITY_SHAPE')
 try:
  identities=(
   (schemas['capability_claim']['properties']['achieved_tier']['enum'],runtime['tiers']),
   (schemas['capability_claim']['properties']['validity']['enum'],runtime['validities']),
   (schemas['conformance_result']['properties']['validity']['enum'],runtime['validities']),
   (schemas['baseline']['properties']['success_terminal']['enum'],runtime['terminals']),
   (schemas['conformance_result']['properties']['success_terminal']['enum'],runtime['terminals']),
   (schemas['planning_dag']['properties']['edges']['items']['properties']['kind']['enum'],runtime['edge_kinds']),
   (schemas['inventory_completeness']['properties']['authored_inventory']['items']['properties']['class']['enum'],runtime['classes']),
   (schemas['inventory_completeness']['properties']['checkers']['items']['properties']['consequence']['enum'],runtime['consequences']),
   (schemas['operation_fault_matrix']['properties']['cells']['items']['properties']['tier_consequence']['enum'],runtime['consequences']),
  )
 except (KeyError,TypeError):add(e,'VOCABULARY_SCHEMA_PATH_MISSING')
 else:
  if any(tuple(schema_values)!=runtime_values for schema_values,runtime_values in identities):add(e,'VOCABULARY_SCHEMA_DIVERGENCE')
  if set(schemas['capability_claim']['properties']['capacity_policy']['enum'])!=set(runtime['capacity']) or set(schemas['capability_claim']['properties']['custody_capacity_policy_revision']['enum'])!=set(runtime['capacity']):add(e,'VOCABULARY_SCHEMA_DIVERGENCE')
 return sorted(set(e))

def parse_consumer_key(value):
 parts=value.split('|') if isinstance(value,str) else []
 if len(parts)!=5 or any(not part for part in parts):raise ValueError('invalid consumer key')
 registry_class,product,surface,resolved_release_or_channel,profile_revision=parts
 if registry_class not in ('fleet','external','publisher'):raise ValueError('invalid registry class')
 return {'registry_class':registry_class,'product':product,'surface':surface,'resolved_release_or_channel':resolved_release_or_channel,'profile_revision':profile_revision}

def parse_claim_key(value):
 parts=value.split('|') if isinstance(value,str) else []
 if len(parts)!=7 or any(not part for part in parts):raise ValueError('invalid claim key')
 product,surface,resolved_release_or_build,profile_revision,achieved_tier,capacity_policy,evidence_epoch=parts
 if achieved_tier not in TIERS or capacity_policy not in CAPACITY:raise ValueError('invalid claim vocabulary')
 return {'product':product,'surface':surface,'resolved_release_or_build':resolved_release_or_build,'profile_revision':profile_revision,'achieved_tier':achieved_tier,'capacity_policy':capacity_policy,'evidence_epoch':evidence_epoch}

def validate_documents(ds,vocabulary=None,schemas=None):
 e=[]
 if not isinstance(ds,dict):return ['SCHEMA_DOCUMENT_NOT_OBJECT']
 try:
  if vocabulary is None:vocabulary=load_claim_vocabulary()
  if schemas is None:schemas=load_contract_schemas()
 except DuplicateJsonMember:return ['DUPLICATE_JSON_MEMBER']
 except (OSError,json.JSONDecodeError):return ['SCHEMA_LOAD_ERROR']
 rv=runtime_vocabulary(vocabulary);e.extend(validate_vocabulary(vocabulary,schemas))
 if schemas:
  for k,v in ds.items():
   if k in schemas:e.extend(schema_errors(schemas[k],v))
   elif k=='capability_claims':
    if not isinstance(v,list):add(e,'SCHEMA_TYPE')
    else:
     for item in v:e.extend(schema_errors(schemas['capability_claim'],item))
   elif k=='conformance_results':
    if not isinstance(v,list):add(e,'SCHEMA_TYPE')
    else:
     for item in v:e.extend(schema_errors(schemas['conformance_result'],item))
 for k in ds:
  if k not in ARTIFACTS and k not in ('scope_approval','capability_claims','conformance_results'):add(e,'ARTIFACT_KIND_UNKNOWN')
 if 'capability_claim'in ds:claim(ds['capability_claim'],e,rv)
 if 'capability_claims'in ds:
  if isinstance(ds['capability_claims'],list):
   for item in ds['capability_claims']:claim(item,e,rv)
  else:add(e,'SCHEMA_DOCUMENT_NOT_OBJECT')
 if 'requirements'in ds:req(ds['requirements'],e,rv)
 if 'conformance_result'in ds:conf(ds['conformance_result'],e,rv)
 if 'conformance_results'in ds:
  if isinstance(ds['conformance_results'],list):
   for item in ds['conformance_results']:conf(item,e,rv)
  else:add(e,'SCHEMA_DOCUMENT_NOT_OBJECT')
 if 'scope_approval'in ds and not scope_approval_shape(ds['scope_approval'],e):pass
 elif 'scope_approval'in ds and not isinstance(ds.get('baseline'),dict):add(e,'SCOPE_APPROVAL_ORPHAN')
 if 'baseline'in ds:
  baseline(ds['baseline'],ds.get('requirements'),ds.get('capability_claim'),ds.get('conformance_result'),e,rv)
  scope_approval(ds.get('scope_approval'),ds['baseline'],ds.get('requirements'),e)
 if 'planning_dag'in ds:dag(ds['planning_dag'],e,rv)
 if 'evidence_invalidation_map'in ds:invalid(ds['evidence_invalidation_map'],e)
 if 'operation_fault_matrix'in ds:
  if schemas:fault(ds['operation_fault_matrix'],e,schemas['operation_fault_matrix'],rv)
  else:add(e,'FAULT_SCHEMA_VOCABULARY_INVALID')
 if 'inventory_completeness'in ds:
  inventory(ds['inventory_completeness'],e,rv)
  inv=ds['inventory_completeness']
  full_claims=ds.get('capability_claims');full_results=ds.get('conformance_results')
  for checker in inv.get('checkers',[]) if isinstance(inv,dict) else []:
   if isinstance(checker,dict) and checker.get('status') in ('unavailable','error'):
    full_mode='claim_set' in inv or 'capability_claims' in ds or 'conformance_results' in ds
    if not full_mode:
     singular=ds.get('conformance_result');affected=checker.get('affected_claim_keys')
     if not isinstance(affected,list) or not affected or not isinstance(singular,dict) or not s(singular.get('claim_key')) or singular.get('claim_key') not in affected or singular.get('validity')!='unverified':add(e,'CHECKER_CLAIM_NOT_DEMOTED')
     continue
    declared=inv.get('claim_set')
    if not isinstance(declared,list) or not all(s(key) for key in declared) or not isinstance(full_claims,list) or not isinstance(full_results,list):add(e,'CHECKER_CLAIM_SET_INCOMPLETE');continue
    claim_keys=[x.get('claim_key') for x in full_claims if isinstance(x,dict) and s(x.get('claim_key'))];result_keys=[x.get('claim_key') for x in full_results if isinstance(x,dict) and s(x.get('claim_key'))]
    if len(claim_keys)!=len(set(claim_keys)) or len(result_keys)!=len(set(result_keys)):add(e,'CHECKER_DUPLICATE_CLAIM_KEY')
    claim_map={x['claim_key']:x for x in full_claims if isinstance(x,dict) and s(x.get('claim_key'))};result_map={x['claim_key']:x for x in full_results if isinstance(x,dict) and s(x.get('claim_key'))}
    if set(declared)!=set(claim_map) or set(declared)!=set(result_map):add(e,'CHECKER_CLAIM_SET_INCOMPLETE')
    affected=checker.get('affected_claim_keys')
    if not isinstance(affected,list) or not all(s(key) for key in affected):add(e,'CHECKER_STRUCTURE');continue
    for key in affected:
     if key not in claim_map or key not in result_map or claim_map[key].get('validity')!='unverified' or result_map[key].get('validity')!='unverified':add(e,'CHECKER_CLAIM_NOT_DEMOTED')
 if 'harness_profile'in ds:basic('harness_profile',ds['harness_profile'],e)
 return sorted(set(e))
def validate_paths(ps):
 ds={};e=[]
 for k,p in ps.items():
  try:
   if isinstance(p,list):ds[k]=[load_json_path(item) for item in p]
   else:ds[k]=load_json_path(p)
  except DuplicateJsonMember:add(e,'DUPLICATE_JSON_MEMBER')
  except (OSError,json.JSONDecodeError):add(e,'ARTIFACT_JSON_UNREADABLE')
 return sorted(set(e+validate_documents(ds)))

PLANNING_ROOT_FILES={'vocabulary':'claim-vocabulary.json','fleet_census':'fleet-surface-census.json','authorities':'authority-artifacts.json','transitions':'transition-artifacts.json','tier_evidence':'tier-evidence-set.json','stage_c_records':'stage-c-authority-set.json','evidence_trust_root':'authoritative-evidence-trust-root.json','evidence_sources':'authoritative-evidence-sources.json','requirements':'consumer-requirements.json','baseline':'support-baseline.json','planning_dag':'planning-dag.json','capability_claims':'capability-claims.json','conformance_results':'conformance-results.json'}
ROOT_FILES={**PLANNING_ROOT_FILES,'stage_a_spike':'stage-a-portability-spike.json','stage_a_epoch':'stage-a-evidence-epoch.json','stage_a_bundle':'stage-a-portability-spike.bundle.json','stage_a_code_authority':'stage-a-execution-authority.json'}
AUTHORIZED_ISSUER='operator-authority:ZMS-Labs/epistemic-skills:complete-manifest-mission-custody-usability'
KERNEL_CODES={'issue-173-cross-mission-drift-suppression':'DAG_KERNEL_DRIFT_NOT_DOMINATING','issue-173-bounded-regex-validation':'DAG_KERNEL_REGEX_NOT_DOMINATING','issue-173-fail-open-inversion-duplicate-resolution':'DAG_KERNEL_FAIL_OPEN_DUPLICATE_NOT_DOMINATING','issue-173-charter-conjoin-migration-refusal':'DAG_KERNEL_CHARTER_NOT_DOMINATING'}
TYPE_FOR_EDGE={'authority':'authority-decision@1','evidence':'evidence-plan@1','implementation':'implementation-plan@1','promotion':'promotion-decision@1'}
FLEET_PRODUCTS={'codex':'openai-codex','claude_code':'anthropic-claude-code','cursor_agent':'cursor-agent','gemini':'google-gemini-cli','kimi_code':'moonshot-kimi-code','aider':'aider','litellm':'litellm','hermes':'hermes','ollama':'ollama','openclaw_memory':'openclaw-memory','openclaw_browser':'openclaw-browser','openclaw_voice':'openclaw-voice','openclaw_phone':'openclaw-phone','acp_runtime':'acp-runtime','discord_gateway':'discord-gateway','signal_gateway':'signal-gateway','imessage_gateway':'imessage-gateway','vllm':'vllm','deepseek_harness':'deepseek-harness'}
PROFILE_REVISION='manifest-custody-profile@1'
FROZEN_PUBLISHER_KEYS={'publisher|openai-chatgpt|chatgpt-plugin|publisher-channel-unresolved|manifest-custody-profile@1','publisher|github-copilot|github-copilot|publisher-channel-unresolved|manifest-custody-profile@1'}
STAGE_C_TYPES={'exact-candidate-conformance@1','exact-head-ci@1','independent-acceptance@1','operator-promotion-decision@1','stage-c-principal-control@1','independently-retained-audit@1'}
STAGE_C_DUTIES={'exact-candidate-conformance@1':{'exact-conformance'},'exact-head-ci@1':{'exact-head-ci'},'independent-acceptance@1':{'independent-acceptance'},'operator-promotion-decision@1':{'operator-promotion'},'stage-c-principal-control@1':{'governed-mutation','native-enforcement'},'independently-retained-audit@1':{'audit-retention'}}
STAGE_C_SUCCESS_OUTCOMES={'exact-candidate-conformance@1':'passed','exact-head-ci@1':'passed','independent-acceptance@1':'accepted','operator-promotion-decision@1':'approved','stage-c-principal-control@1':'enforced','independently-retained-audit@1':'retained'}
INCOMPATIBLE_DUTIES={'exact-conformance|independent-acceptance','operator-promotion|independent-acceptance','governed-mutation|audit-retention'}
U3_EVIDENCE_TYPES={'installed-package-launcher-evidence@1','interruption-evidence@1','recovery-evidence@1','actor-authority-separation@1','independent-acceptance-evidence@1'}
U4_EVIDENCE_TYPES=U3_EVIDENCE_TYPES|{'native-boundary-identity@1','matched-deny-evidence@1','neighboring-allow-evidence@1','failure-behavior-evidence@1','hook-configuration-evidence@1'}
SOURCE_KIND_BY_RECORD_TYPE={
 'installed-package-launcher-evidence@1':'installed-package-launcher-observation',
 'interruption-evidence@1':'custody-interruption-observation',
 'recovery-evidence@1':'custody-recovery-observation',
 'actor-authority-separation@1':'actor-authority-separation-observation',
 'independent-acceptance-evidence@1':'tier-independent-acceptance-verdict',
 'native-boundary-identity@1':'native-boundary-attestation',
 'matched-deny-evidence@1':'matched-deny-observation',
 'neighboring-allow-evidence@1':'neighboring-allow-observation',
 'failure-behavior-evidence@1':'failure-behavior-observation',
 'hook-configuration-evidence@1':'hook-configuration-readback',
 'exact-candidate-conformance@1':'exact-candidate-conformance-run',
 'exact-head-ci@1':'exact-head-ci-run',
 'independent-acceptance@1':'independent-acceptance-decision',
 'operator-promotion-decision@1':'operator-promotion-decision',
 'stage-c-principal-control@1':'native-stage-c-control',
 'independently-retained-audit@1':'independent-audit-retention-readback',
}
TIER_SOURCE_KINDS={SOURCE_KIND_BY_RECORD_TYPE[kind] for kind in U4_EVIDENCE_TYPES}
STAGE_C_SOURCE_KINDS={SOURCE_KIND_BY_RECORD_TYPE[kind] for kind in STAGE_C_TYPES}
# This pin authorizes only a disposable, non-production equivalence corpus. A
# production trust root must be separately reviewed and pinned before the
# authoritative context can resolve any U3+ evidence.
PINNED_EVIDENCE_TRUST_ROOT_DIGESTS={'authoritative-equivalence':'811ed4cd23a19d7d7d760aad435ac46d7d58f2f170bf30bed4c9b354af41213d'}

def canonical_bytes(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()+b'\n'
def canonical_digest(value):return hashlib.sha256(canonical_bytes(value)).hexdigest()
def record_digest(value):
 if not isinstance(value,dict):return ''
 return canonical_digest({key:item for key,item in value.items() if key!='content_digest'})

def source_statement_digest(value):
 if not isinstance(value,dict):return ''
 excluded={'content_digest','source_record_digest','source_statement_digest'}
 return canonical_digest({key:item for key,item in value.items() if key not in excluded})

def load_root_bundle(root):
 root=Path(root)
 bundle={kind:load_json_path(root/name) for kind,name in ROOT_FILES.items()}
 bundle['schemas']=load_contract_schemas(root/'schemas')
 return bundle

def load_planning_root_bundle(root):
 root=Path(root);bundle={kind:load_json_path(root/name) for kind,name in PLANNING_ROOT_FILES.items()};bundle['schemas']=load_contract_schemas(root/'schemas');return bundle

def root_bundle_digest(bundle):
 schema_digests={SCHEMA_FILES[kind]:canonical_digest(value) for kind,value in sorted(bundle['schemas'].items()) if kind!='stage_a_spike'}
 return canonical_digest({'documents':{kind:canonical_digest(bundle[kind]) for kind in PLANNING_ROOT_FILES},'schemas':schema_digests})

def load_pinned_stage_a_module(filename,module_name,expected_digest):
 path=Path(__file__).with_name(filename)
 try:data=path.read_bytes()
 except OSError as error:raise ValueError('STAGE_A_ENTRYPOINT_UNAPPROVED') from error
 if hashlib.sha256(data).hexdigest()!=expected_digest:raise ValueError('STAGE_A_ENTRYPOINT_UNAPPROVED')
 spec=importlib.util.spec_from_file_location(module_name,path)
 if spec is None or spec.loader is None:raise ValueError('STAGE_A_ENTRYPOINT_UNAPPROVED')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def load_stage_a_runner():
 return load_pinned_stage_a_module('run_portability_spike.py','root_bound_stage_a_runner',STAGE_A_RUNNER_SHA256)

def load_stage_a_verifier():
 return load_pinned_stage_a_module('verify_portability_spike_bundle.py','root_bound_stage_a_verifier',STAGE_A_VERIFIER_SHA256)

def contains_exact_reference(value,reference):
 if isinstance(value,str):return value==reference
 if isinstance(value,list):return any(contains_exact_reference(item,reference) for item in value)
 if isinstance(value,dict):return any(contains_exact_reference(item,reference) for item in value.values())
 return False

def stage_a_reuse_errors(bundle,content_digest):
 reference='stage-a-portability-spike@sha256:'+str(content_digest);errors=[]
 if contains_exact_reference(bundle.get('conformance_results'),reference) or contains_exact_reference(bundle.get('stage_c_records'),reference):errors.append('STAGE_A_EVIDENCE_FORBIDDEN_EXACT_CONFORMANCE')
 if contains_exact_reference(bundle.get('tier_evidence'),reference):errors.append('STAGE_A_EVIDENCE_FORBIDDEN_TIER_AWARD')
 if contains_exact_reference(bundle.get('transitions'),reference):errors.append('STAGE_A_EVIDENCE_FORBIDDEN_PROMOTION')
 if contains_exact_reference(bundle.get('capability_claims'),reference) or contains_exact_reference(bundle.get('baseline'),reference):errors.append('STAGE_A_EVIDENCE_FORBIDDEN_CURRENT_USABILITY')
 return sorted(set(errors))

def validate_stage_a_bundle(bundle,spike):
 errors=[]
 fields={'record','source_revision','code_revision','authoritative_revision','code_authority_digest','canonical_request','artifact_resolvers','request_digest','result_digest','content_digest'}
 if not isinstance(bundle,dict) or set(bundle)!=fields or bundle.get('record')!='stage-a-portability-evidence-bundle@2':return ['STAGE_A_BUNDLE_INVALID']
 request=bundle.get('canonical_request');resolvers=bundle.get('artifact_resolvers')
 if not isinstance(request,dict) or not isinstance(resolvers,dict):return ['STAGE_A_BUNDLE_INVALID']
 if bundle.get('code_authority_digest')!=STAGE_A_AUTHORITY_SHA256:errors.append('STAGE_A_BUNDLE_CODE_AUTHORITY_UNAPPROVED')
 if canonical_digest(request)!=bundle.get('request_digest'):errors.append('STAGE_A_BUNDLE_REQUEST_DIGEST_MISMATCH')
 if canonical_digest(spike)!=bundle.get('result_digest'):errors.append('STAGE_A_BUNDLE_RESULT_DIGEST_MISMATCH')
 if record_digest(bundle)!=bundle.get('content_digest'):errors.append('STAGE_A_BUNDLE_CONTENT_DIGEST_MISMATCH')
 artifacts=request.get('artifacts')
 if not isinstance(artifacts,dict) or set(artifacts)!=set(resolvers) or set(artifacts)!=set(spike.get('input_digests',{})):errors.append('STAGE_A_BUNDLE_RESOLVER_SET_MISMATCH')
 else:
  for name,descriptor in artifacts.items():
   resolver=resolvers.get(name)
   if not isinstance(descriptor,dict) or not isinstance(resolver,dict) or descriptor.get('sha256')!=resolver.get('sha256') or descriptor.get('kind')!=resolver.get('artifact_kind') or spike['input_digests'].get(name)!=resolver.get('sha256'):
    errors.append('STAGE_A_BUNDLE_RESOLVER_DIGEST_MISMATCH');break
 return sorted(set(errors))

def parse_consumer_key(value):
 parts=value.split('|') if isinstance(value,str) else []
 if len(parts)!=5 or any(not part for part in parts):raise ValueError('invalid consumer key')
 registry_class,product,surface,resolved_release_or_channel,profile_revision=parts
 if registry_class not in ('fleet','external','publisher'):raise ValueError('invalid registry class')
 return {'registry_class':registry_class,'product':product,'surface':surface,'resolved_release_or_channel':resolved_release_or_channel,'profile_revision':profile_revision}

def parse_baseline_address(value,rv):
 parts=value.split('|') if isinstance(value,str) else []
 if len(parts)==7 and parts[0]=='profile':
  _,product,surface,resolved,profile_revision,capacity,evidence_epoch=parts
  if capacity not in rv['capacity'] or not all(parts):raise ValueError('invalid profile address')
  return {'address_type':'profile','product':product,'surface':surface,'resolved_release_or_build':resolved,'profile_revision':profile_revision,'capacity_policy':capacity,'evidence_epoch':evidence_epoch}
 if len(parts)==7:
  product,surface,resolved,profile_revision,tier,capacity,evidence_epoch=parts
  if tier not in rv['tiers'] or capacity not in rv['capacity'] or not all(parts):raise ValueError('invalid claim key')
  return {'address_type':'claim','product':product,'surface':surface,'resolved_release_or_build':resolved,'profile_revision':profile_revision,'achieved_tier':tier,'capacity_policy':capacity,'evidence_epoch':evidence_epoch}
 raise ValueError('invalid baseline address')

def parse_claim_key(value):
 vocabulary=load_claim_vocabulary();return parse_baseline_address(value,runtime_vocabulary(vocabulary))

def reach(graph,start):
 seen=set();todo=[start]
 while todo:
  current=todo.pop()
  for target in graph.get(current,()):
   if target not in seen:seen.add(target);todo.append(target)
 return seen

def reaches_without(graph,start,target,blocked):
 if start==blocked:return False
 seen=set();todo=[start]
 while todo:
  current=todo.pop()
  if current==blocked or current in seen:continue
  if current==target:return True
  seen.add(current);todo.extend(graph.get(current,()))
 return False

def stage_a_affected_edges(dag_doc):
 nodes=dag_doc.get('nodes') if isinstance(dag_doc,dict) else None;edges=dag_doc.get('edges') if isinstance(dag_doc,dict) else None
 if not isinstance(nodes,list) or not isinstance(edges,list):raise ValueError('invalid DAG')
 node_ids={node.get('id') for node in nodes if isinstance(node,dict) and s(node.get('id'))};start='stage-a-portability-spike'
 if len(node_ids)!=len(nodes) or start not in node_ids:raise ValueError('invalid DAG')
 graph={node:[] for node in node_ids};normalized=[];seen=set()
 for edge in edges:
  if not isinstance(edge,dict) or edge.get('from') not in node_ids or edge.get('to') not in node_ids or not s(edge.get('transition_artifact')) or edge['transition_artifact'] in seen:raise ValueError('invalid DAG')
  seen.add(edge['transition_artifact']);graph[edge['from']].append(edge['to']);normalized.append(edge)
 reachable={start};todo=[start]
 while todo:
  for target in graph[todo.pop()]:
   if target not in reachable:reachable.add(target);todo.append(target)
 return sorted(edge['transition_artifact'] for edge in normalized if edge['from'] in reachable)

def validate_root_bundle(bundle,validation_context='authoritative',stage_replay_verified=False):
 errors=[];empty={'live_reachable':set(),'template_reachable':set(),'live_graph':{},'template_graph':{},'n_active_awarded':False,'bundle':bundle}
 if not isinstance(bundle,dict):return {**empty,'errors':['SCHEMA_DOCUMENT_NOT_OBJECT']}
 required=(set(PLANNING_ROOT_FILES) if validation_context=='planning-authority' else set(ROOT_FILES))|{'schemas'}
 if not required<=set(bundle):return {**empty,'errors':['ARTIFACT_MISSING']}
 if validation_context not in ('authoritative','planning-authority','authoritative-equivalence','synthetic-positive-control','negative-control'):errors.append('VALIDATION_CONTEXT_INVALID')
 vocabulary=bundle['vocabulary'];schemas=bundle['schemas'];rv=runtime_vocabulary(vocabulary)
 schema_docs={'requirements':bundle['requirements'],'baseline':bundle['baseline'],'planning_dag':bundle['planning_dag'],'capability_claims':bundle['capability_claims'],'conformance_results':bundle['conformance_results']}
 errors.extend(validate_documents(schema_docs,vocabulary,schemas));errors=[code for code in errors if code!='BASELINE_PRODUCT_EVIDENCE_MISSING']
 census=bundle['fleet_census'];authorities=bundle['authorities'];transitions=bundle['transitions'];tier_evidence=bundle['tier_evidence'];stage_c_records=bundle['stage_c_records'];evidence_trust_root=bundle['evidence_trust_root'];evidence_sources=bundle['evidence_sources'];requirements_doc=bundle['requirements'];baseline_doc=bundle['baseline'];dag_doc=bundle['planning_dag'];stage_a_spike=bundle.get('stage_a_spike');stage_a_epoch=bundle.get('stage_a_epoch');stage_a_bundle=bundle.get('stage_a_bundle');stage_a_code_authority=bundle.get('stage_a_code_authority')
 if not all(isinstance(item,dict) for item in (census,authorities,transitions,tier_evidence,stage_c_records,evidence_trust_root,evidence_sources,requirements_doc,baseline_doc,dag_doc)):
  return {**empty,'errors':sorted(set(errors+['SCHEMA_DOCUMENT_NOT_OBJECT']))}
 errors.extend(schema_errors(schemas['fleet_census'],census));errors.extend(schema_errors(schemas['authorities'],authorities));errors.extend(schema_errors(schemas['transitions'],transitions));errors.extend(schema_errors(schemas['tier_evidence'],tier_evidence));errors.extend(schema_errors(schemas['stage_c_records'],stage_c_records));errors.extend(schema_errors(schemas['evidence_trust_root'],evidence_trust_root));errors.extend(schema_errors(schemas['evidence_sources'],evidence_sources))

 stage_a_blocked=validation_context=='authoritative';stage_a_affected=set();stage_error_start=len(errors)
 if validation_context=='authoritative':
  try:expected_edges=stage_a_affected_edges(dag_doc);stage_a_affected=set(expected_edges)
  except Exception:expected_edges=[];stage_a_affected={edge.get('transition_artifact') for edge in dag_doc.get('edges',[]) if isinstance(edge,dict) and s(edge.get('transition_artifact'))};errors.append('STAGE_A_EDGE_CLOSURE_MISMATCH')
  try:
   stage_runner=load_stage_a_runner()
   if stage_runner.affected_edges(dag_doc)!=expected_edges:errors.append('STAGE_A_EDGE_CLOSURE_MISMATCH')
  except Exception as error:
   stage_runner=None;errors.append('STAGE_A_ENTRYPOINT_UNAPPROVED' if str(error)=='STAGE_A_ENTRYPOINT_UNAPPROVED' else 'STAGE_A_EDGE_CLOSURE_MISMATCH')
  if not isinstance(stage_a_code_authority,dict) or stage_a_code_authority.get('record')!='stage-a-execution-authority@2' or record_digest(stage_a_code_authority)!=stage_a_code_authority.get('content_digest') or canonical_digest(stage_a_code_authority)!=STAGE_A_AUTHORITY_SHA256:errors.append('STAGE_A_CODE_AUTHORITY_INVALID')
  if not isinstance(stage_a_spike,dict) or not isinstance(stage_a_epoch,dict) or not isinstance(stage_a_bundle,dict):errors.append('STAGE_A_RECORD_INVALID');stage_a_blocked=True
  else:
   errors.extend(schema_errors(schemas['stage_a_spike'],stage_a_spike))
   try:
    semantic=stage_runner.validate_spike_record(stage_a_spike) if stage_runner is not None else ['SPIKE_RECORD_VALIDATOR_UNAVAILABLE']
   except Exception:semantic=['SPIKE_RECORD_VALIDATOR_UNAVAILABLE']
   if semantic:errors.append('STAGE_A_RECORD_INVALID');stage_a_blocked=True
   retained_request=stage_a_bundle.get('canonical_request',{}) if isinstance(stage_a_bundle,dict) else {};retained_artifacts=retained_request.get('artifacts',{}) if isinstance(retained_request,dict) else {};retained_dag=retained_artifacts.get('planning_dag',{}) if isinstance(retained_artifacts,dict) else {}
   if stage_a_spike.get('input_digests',{}).get('planning_dag')!=retained_dag.get('sha256') or stage_a_spike.get('planning_dag_content_digest')!=dag_doc.get('content_digest'):errors.append('STAGE_A_DAG_BINDING_STALE');stage_a_blocked=True
   if set(stage_a_epoch)!={'record','current_epoch','authority'} or stage_a_epoch.get('record')!='evidence-epoch@1':errors.append('STAGE_A_EVIDENCE_EPOCH_INVALID');stage_a_blocked=True
   if stage_a_spike.get('evidence_epoch')!=stage_a_epoch.get('current_epoch'):errors.append('STAGE_A_EVIDENCE_EPOCH_STALE');stage_a_blocked=True
   if stage_a_spike.get('input_digests',{}).get('epoch')!=hashlib.sha256(canonical_bytes(stage_a_epoch)).hexdigest():errors.append('STAGE_A_EVIDENCE_EPOCH_BINDING_STALE');stage_a_blocked=True
   expected_disposition='eligible-for-next-gate' if stage_a_spike.get('decision')=='proceed' else 'blocked'
   if stage_a_spike.get('affected_dag_edges')!=expected_edges or stage_a_spike.get('edge_dispositions')!=[{'edge_id':edge,'disposition':expected_disposition} for edge in expected_edges]:errors.append('STAGE_A_EDGE_CLOSURE_MISMATCH');stage_a_blocked=True
   bundle_errors=validate_stage_a_bundle(stage_a_bundle,stage_a_spike);errors.extend(bundle_errors)
   if bundle_errors:stage_a_blocked=True
   errors.extend(stage_a_reuse_errors(bundle,stage_a_spike.get('content_digest')))
   if stage_a_spike.get('decision')=='proceed' and stage_replay_verified and len(errors)==stage_error_start:stage_a_blocked=False

 legacy_tier_assertion=any(isinstance(item,dict) and ({'u3_evidence','u4_evidence'}&set(item)) for item in bundle['capability_claims'] if isinstance(bundle['capability_claims'],list))
 if legacy_tier_assertion:
  errors=[code for code in errors if code not in ('SCHEMA_UNKNOWN_FIELD','ARTIFACT_UNKNOWN_FIELD')];errors.append('TIER_EVIDENCE_SELF_ASSERTED')

 census_subject={key:census.get(key) for key in ('record','repository','tree','source_symbol','surface_kinds','evidence_record')}
 if canonical_digest(census_subject)!=census.get('content_digest'):errors.append('CENSUS_CONTENT_DIGEST_MISMATCH')
 requirement_subject={key:requirements_doc.get(key) for key in ('record','scope','revision','required_consumers','publisher_consumers','census_content_digest')}
 if canonical_digest(requirement_subject)!=requirements_doc.get('content_digest'):errors.append('REQUIREMENTS_CONTENT_DIGEST_MISMATCH')
 if record_digest(baseline_doc)!=baseline_doc.get('content_digest'):errors.append('BASELINE_CONTENT_DIGEST_MISMATCH')
 if record_digest(dag_doc)!=dag_doc.get('content_digest'):errors.append('DAG_CONTENT_DIGEST_MISMATCH')

 authority_items=authorities.get('artifacts');authority_map={}
 if not isinstance(authority_items,list):errors.append('AUTHORITY_ARTIFACT_SET_INVALID');authority_items=[]
 for artifact in authority_items:
  errors.extend(schema_errors(schemas['authority_artifact'],artifact))
  if not isinstance(artifact,dict) or not s(artifact.get('id')):errors.append('AUTHORITY_ARTIFACT_INVALID');continue
  if artifact['id'] in authority_map:errors.append('AUTHORITY_ARTIFACT_DUPLICATE')
  authority_map[artifact['id']]=artifact
  if record_digest(artifact)!=artifact.get('content_digest'):errors.append('AUTHORITY_ARTIFACT_DIGEST_MISMATCH')
  if artifact.get('issuer_identity')!=AUTHORIZED_ISSUER:errors.append('AUTHORITY_ISSUER_UNAUTHORIZED')
  if artifact.get('authority')!='planning-only-no-promotion-no-n-active':errors.append('AUTHORITY_SCOPE_INVALID')
  if not s(artifact.get('rationale')):errors.append('AUTHORITY_RATIONALE_MISSING')
 if record_digest(authorities)!=authorities.get('content_digest'):errors.append('AUTHORITY_SET_DIGEST_MISMATCH')
 def exact_authority(artifact,record_type,subject_kind,subject_id,subject_digest,referenced_record,binding_code):
  if not artifact or artifact.get('record_type')!=record_type or artifact.get('subject_digest')!=subject_digest:return errors.append(binding_code)
  if artifact.get('subject_id')!=subject_id:errors.append('AUTHORITY_SUBJECT_ID_MISMATCH')
  if artifact.get('subject_kind')!=subject_kind:errors.append('AUTHORITY_SUBJECT_KIND_MISMATCH')
  if artifact.get('referenced_record')!=referenced_record:errors.append('AUTHORITY_REFERENCED_RECORD_MISMATCH')
 census_auth=authority_map.get(census.get('authority_artifact_id'))
 exact_authority(census_auth,'operator-decision@1','fleet-surface-census@1',census.get('record'),census.get('content_digest'),census.get('evidence_record'),'CENSUS_AUTHORITY_BINDING_INVALID')
 if not census_auth or census.get('decision_digest')!=census_auth.get('content_digest'):errors.append('CENSUS_AUTHORITY_BINDING_INVALID')
 req_auth=authority_map.get(requirements_doc.get('authority_artifact_id'))
 census_ref='authority-artifact:'+str(census.get('authority_artifact_id'))+'@sha256:'+str(census.get('decision_digest'))
 exact_authority(req_auth,'operator-decision@1','consumer-requirements@1',requirements_doc.get('revision'),requirements_doc.get('content_digest'),census_ref,'REQUIREMENTS_AUTHORITY_BINDING_INVALID')
 if not req_auth or requirements_doc.get('decision_digest')!=req_auth.get('content_digest') or requirements_doc.get('issuer_identity')!=AUTHORIZED_ISSUER:errors.append('REQUIREMENTS_AUTHORITY_BINDING_INVALID')
 if requirements_doc.get('census_content_digest')!=census.get('content_digest'):errors.append('REQUIREMENTS_CENSUS_STALE')
 if baseline_doc.get('requirements_revision')!=requirements_doc.get('revision') or baseline_doc.get('requirements_decision_digest')!=requirements_doc.get('decision_digest'):errors.append('BASELINE_REQUIREMENTS_STALE')
 if baseline_doc.get('requirements_content_digest')!=requirements_doc.get('content_digest') or baseline_doc.get('census_content_digest')!=census.get('content_digest'):errors.append('BASELINE_REQUIREMENTS_STALE')
 if baseline_doc.get('authority_artifacts_digest')!=authorities.get('content_digest'):errors.append('BASELINE_AUTHORITY_BINDING_STALE')
 if baseline_doc.get('tier_evidence_set_digest')!=tier_evidence.get('content_digest'):errors.append('BASELINE_TIER_EVIDENCE_BINDING_STALE')
 if baseline_doc.get('stage_c_authority_set_digest')!=stage_c_records.get('content_digest'):errors.append('BASELINE_STAGE_C_AUTHORITY_BINDING_STALE')
 if baseline_doc.get('evidence_trust_root_digest')!=evidence_trust_root.get('content_digest') or baseline_doc.get('evidence_source_set_digest')!=evidence_sources.get('content_digest'):errors.append('BASELINE_EVIDENCE_TRUST_BINDING_STALE')

 req_items=requirements_doc.get('required_consumers');base_items=baseline_doc.get('consumers')
 publisher_items=requirements_doc.get('publisher_consumers')
 if not isinstance(req_items,list) or not isinstance(publisher_items,list) or not isinstance(base_items,list):req_items=[];publisher_items=[];base_items=[]
 req_ids=[item.get('id') for item in req_items if isinstance(item,dict) and s(item.get('id'))];base_ids=[item.get('id') for item in base_items if isinstance(item,dict) and s(item.get('id'))]
 publisher_ids=[item.get('id') for item in publisher_items if isinstance(item,dict) and s(item.get('id'))]
 if len(req_ids)!=len(set(req_ids)) or len(base_ids)!=len(set(base_ids)):errors.append('REGISTRY_DUPLICATE_CONSUMER_KEY')
 if not set(req_ids)<=set(base_ids):errors.append('BASELINE_REQUIRED_CONSUMER_MISSING')
 parsed_required=[]
 for identifier in set(req_ids):
  try:parsed_required.append(parse_consumer_key(identifier))
  except ValueError:errors.append('REGISTRY_CONSUMER_KEY_INVALID')
 census_surfaces=set(census.get('surface_kinds',[])) if isinstance(census.get('surface_kinds'),list) else set()
 fleet_release='fleet-tree-'+str(census.get('tree'))
 expected_required={f"fleet|{FLEET_PRODUCTS[surface]}|{surface}|{fleet_release}|{PROFILE_REVISION}" for surface in census_surfaces if surface in FLEET_PRODUCTS}|{f'external|google-antigravity|antigravity|external-channel-unresolved|{PROFILE_REVISION}'}
 exact_registry_invalid=set(req_ids)!=expected_required or set(publisher_ids)!=FROZEN_PUBLISHER_KEYS or (not (set(req_ids)-set(base_ids)) and set(base_ids)!=(set(req_ids)|set(publisher_ids)))
 if exact_registry_invalid and 'BASELINE_REQUIRED_CONSUMER_MISSING' not in errors and 'REGISTRY_DUPLICATE_CONSUMER_KEY' not in errors:errors.append('REGISTRY_EXACT_KEY_SET_MISMATCH')
 if {item['surface'] for item in parsed_required if item['registry_class']=='fleet'}!=census_surfaces or {item['surface'] for item in parsed_required if item['registry_class']=='external'}!={'antigravity'}:errors.append('REGISTRY_CENSUS_MISMATCH')

 req_map={item['id']:item for item in req_items if isinstance(item,dict) and s(item.get('id'))};applicable_keys=[]
 requirement_ref='authority-artifact:'+str(requirements_doc.get('authority_artifact_id'))+'@sha256:'+str(requirements_doc.get('decision_digest'))
 for item in base_items:
  if not isinstance(item,dict):continue
  try:consumer=parse_consumer_key(item.get('id'));address=parse_baseline_address(item.get('claim_key'),rv)
  except ValueError:errors.append('REGISTRY_CONSUMER_KEY_INVALID');continue
  if consumer['product']!=address['product'] or consumer['surface']!=address['surface'] or consumer['profile_revision']!=address['profile_revision']:errors.append('REGISTRY_CLAIM_KEY_MISMATCH')
  decision=authority_map.get(item.get('reason'));expected_subject=canonical_digest({'consumer_id':item.get('id'),'disposition':item.get('disposition'),'profile_address':item.get('claim_key')})
  if not decision or decision.get('record_type')!='disposition-decision@1' or decision.get('subject_digest')!=expected_subject:errors.append('BASELINE_EVIDENCE_REFERENCE_UNRESOLVED')
  else:
   if decision.get('subject_id')!=item.get('id'):errors.append('AUTHORITY_SUBJECT_ID_MISMATCH')
   if decision.get('subject_kind')!='support-baseline-consumer@1':errors.append('AUTHORITY_SUBJECT_KIND_MISMATCH')
   if decision.get('referenced_record')!=requirement_ref:errors.append('AUTHORITY_REFERENCED_RECORD_MISMATCH')
  if item.get('disposition')=='applicable':
   if address.get('address_type')!='claim':errors.append('BASELINE_PRODUCT_EVIDENCE_MISSING')
   else:applicable_keys.append(item['claim_key'])
  elif address.get('address_type')!='profile':errors.append('BASELINE_UNVERIFIED_ACHIEVEMENT_ENCODED')

 claim_items=bundle['capability_claims'];result_items=bundle['conformance_results']
 claim_map={item.get('claim_key'):item for item in claim_items if isinstance(item,dict) and s(item.get('claim_key'))} if isinstance(claim_items,list) else {}
 result_map={item.get('claim_key'):item for item in result_items if isinstance(item,dict) and s(item.get('claim_key'))} if isinstance(result_items,list) else {}
 if not isinstance(claim_items,list) or not isinstance(result_items,list):errors.append('SCHEMA_TYPE');claim_items=[];result_items=[]
 if len(claim_map)!=len(claim_items) or len(result_map)!=len(result_items):errors.append('PRODUCT_EVIDENCE_DUPLICATE_CLAIM_KEY')
 claim_set_digest=canonical_digest(claim_items);result_set_digest=canonical_digest(result_items)
 if baseline_doc.get('capability_claims_digest')!=claim_set_digest:errors.append('CAPABILITY_CLAIMS_DIGEST_MISMATCH')
 if baseline_doc.get('conformance_results_digest')!=result_set_digest:errors.append('CONFORMANCE_RESULTS_DIGEST_MISMATCH')

 trust_root_valid=record_digest(evidence_trust_root)==evidence_trust_root.get('content_digest')
 if not trust_root_valid:errors.append('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_DIGEST_MISMATCH')
 source_items=evidence_sources.get('sources');source_map={};source_set_valid=record_digest(evidence_sources)==evidence_sources.get('content_digest')
 if not source_set_valid:errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_SET_DIGEST_MISMATCH')
 if not isinstance(source_items,list):errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_SET_INVALID');source_items=[]
 for source in source_items:
  errors.extend(schema_errors(schemas['evidence_source'],source))
  if not isinstance(source,dict) or not s(source.get('id')):errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_INVALID');continue
  if source['id'] in source_map:errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_DUPLICATE')
  source_map[source['id']]=source
  if record_digest(source)!=source.get('content_digest'):errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_DIGEST_MISMATCH')
  expected_readback=canonical_digest({'source_id':source.get('id'),'accepted_statement_digest':source.get('accepted_statement_digest'),'retention_policy':source.get('retention_policy'),'retention_days':source.get('retention_days'),'readback_method':source.get('readback_method'),'readback_principal_identity':source.get('readback_principal_identity'),'readback_credential_class':source.get('readback_credential_class'),'readback_credential_digest':source.get('readback_credential_digest'),'readback_outcome':source.get('readback_outcome')})
  if source.get('readback_digest')!=expected_readback or source.get('readback_outcome')!='retained' or source.get('principal_identity')==source.get('readback_principal_identity'):errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_READBACK_INVALID')
 accepted_source_ids=evidence_trust_root.get('accepted_source_ids');accepted_issuers=evidence_trust_root.get('accepted_issuer_identities');accepted_credentials=evidence_trust_root.get('accepted_credential_classes');accepted_kinds=evidence_trust_root.get('accepted_source_kinds');decision_roots=evidence_trust_root.get('decision_roots');transparency_roots=evidence_trust_root.get('transparency_roots')
 exact_trust_sets=(
  (accepted_source_ids,set(source_map)),
  (accepted_issuers,{item.get('issuer_identity') for item in source_items if isinstance(item,dict)}),
  (accepted_credentials,{value for item in source_items if isinstance(item,dict) for value in (item.get('credential_class'),item.get('readback_credential_class'))}),
  (accepted_kinds,{item.get('source_kind') for item in source_items if isinstance(item,dict)}),
  (decision_roots,{item.get('decision_root') for item in source_items if isinstance(item,dict)}),
  (transparency_roots,{item.get('transparency_root') for item in source_items if isinstance(item,dict)}),
 )
 if evidence_trust_root.get('source_set_digest')!=evidence_sources.get('content_digest') or any(not isinstance(values,list) or len(values)!=len(set(values)) or set(values)!=expected for values,expected in exact_trust_sets):errors.append('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_CLOSURE_INVALID')
 minimum_retention=evidence_trust_root.get('minimum_retention_days')
 if not isinstance(minimum_retention,int) or any(item.get('environment')!=evidence_trust_root.get('environment') or not isinstance(item.get('retention_days'),int) or item.get('retention_days')<minimum_retention or item.get('readback_method')!=evidence_trust_root.get('required_readback_method') for item in source_items if isinstance(item,dict)):errors.append('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_CLOSURE_INVALID')

 high_tier_claimed=any(isinstance(item,dict) and item.get('achieved_tier') in ('U3','U4','U5') for item in claim_items)
 trusted_context=validation_context in ('authoritative','authoritative-equivalence') and high_tier_claimed
 pinned_trust_root=PINNED_EVIDENCE_TRUST_ROOT_DIGESTS.get(validation_context)
 trust_root_resolved=trust_root_valid and source_set_valid and s(pinned_trust_root) and pinned_trust_root!='PIN_AFTER_GENERATION' and evidence_trust_root.get('content_digest')==pinned_trust_root
 if trusted_context and not trust_root_resolved:errors.append('AUTHORITATIVE_EVIDENCE_TRUST_ROOT_UNRESOLVED')

 def trusted_source_resolves(record):
  if not trusted_context or not trust_root_resolved:return not trusted_context
  source=source_map.get(record.get('source_id'));record_type=record.get('record_type');expected_kind=SOURCE_KIND_BY_RECORD_TYPE.get(record_type)
  if not source or record.get('source_kind')!=expected_kind or source.get('source_kind')!=expected_kind or source.get('accepted_record_type')!=record_type:return False
  if record.get('source_record_digest')!=source.get('content_digest') or record.get('issuer_identity')!=source.get('issuer_identity') or record.get('principal_identity')!=source.get('principal_identity') or record.get('credential_class')!=source.get('credential_class') or record.get('credential_digest')!=source.get('credential_digest'):return False
  statement=source_statement_digest(record)
  if record.get('source_statement_digest')!=statement or source.get('accepted_statement_digest')!=statement:return False
  if source.get('id') not in set(accepted_source_ids or ()) or source.get('issuer_identity') not in set(accepted_issuers or ()) or source.get('credential_class') not in set(accepted_credentials or ()) or source.get('source_kind') not in set(accepted_kinds or ()):return False
  if source.get('decision_root') not in set(decision_roots or ()) or source.get('transparency_root') not in set(transparency_roots or ()):return False
  return True

 tier_items=tier_evidence.get('artifacts');tier_map={};tier_set_valid=record_digest(tier_evidence)==tier_evidence.get('content_digest')
 if not tier_set_valid:errors.append('TIER_EVIDENCE_SET_DIGEST_MISMATCH')
 if not isinstance(tier_items,list):errors.append('TIER_EVIDENCE_SET_INVALID');tier_items=[]
 expected_evidence_scope='authoritative' if validation_context in ('authoritative','authoritative-equivalence') else 'fixture-only'
 tier_source_unresolved=False
 for artifact in tier_items:
  errors.extend(schema_errors(schemas['tier_evidence_artifact'],artifact))
  if not isinstance(artifact,dict) or not s(artifact.get('id')):errors.append('TIER_EVIDENCE_ARTIFACT_INVALID');continue
  if artifact['id'] in tier_map:errors.append('TIER_EVIDENCE_ARTIFACT_DUPLICATE')
  tier_map[artifact['id']]=artifact
  if record_digest(artifact)!=artifact.get('content_digest'):errors.append('TIER_EVIDENCE_ARTIFACT_DIGEST_MISMATCH')
  issuer=artifact.get('issuer_identity','')
  if artifact.get('authority_scope')!=expected_evidence_scope or (expected_evidence_scope=='fixture-only' and not issuer.startswith('fixture-evidence-authority:')) or (expected_evidence_scope=='authoritative' and not issuer.startswith('authoritative-evidence-authority:')):errors.append('TIER_EVIDENCE_AUTHORITY_CONTEXT_MISMATCH')
  if artifact.get('subject_kind')!='capability-claim-evidence@1' or artifact.get('outcome')!='passed' or not s(artifact.get('rationale')):errors.append('TIER_EVIDENCE_SEMANTICS_INVALID')
  if trusted_context and not trusted_source_resolves(artifact):tier_source_unresolved=True
 if tier_source_unresolved and trust_root_resolved:errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_UNRESOLVED')
 for artifact in tier_items:
  if isinstance(artifact,dict) and any(ref not in tier_map for ref in artifact.get('referenced_record_ids',[]) if isinstance(ref,str)):errors.append('TIER_EVIDENCE_REFERENCE_UNRESOLVED')

 referenced_tier_ids={identifier for claim_doc in claim_items if isinstance(claim_doc,dict) for identifier in claim_doc.get('tier_evidence_artifact_ids',[]) if isinstance(identifier,str)}
 if set(tier_map)!=referenced_tier_ids:errors.append('TIER_EVIDENCE_SET_NOT_EXACT')

 def claim_evidence_subject(claim_doc):
  return {key:claim_doc.get(key) for key in ('claim_key','product','surface','resolved_release_or_build','profile_revision','achieved_tier','capacity_policy','evidence_epoch')}
 def validate_tier_for_claim(claim_doc,result_doc):
  if claim_doc.get('tier_evidence_set_digest')!=tier_evidence.get('content_digest') or result_doc.get('tier_evidence_set_digest')!=tier_evidence.get('content_digest'):errors.append('CONFORMANCE_EVIDENCE_MISMATCH');return
  ids=claim_doc.get('tier_evidence_artifact_ids');result_ids=result_doc.get('tier_evidence_artifact_ids')
  if not isinstance(ids,list) or ids!=result_ids or len(ids)!=len(set(ids)):errors.append('CONFORMANCE_EVIDENCE_MISMATCH');return
  if any(identifier not in tier_map for identifier in ids):errors.append('TIER_EVIDENCE_REFERENCE_UNRESOLVED');return
  records=[tier_map[identifier] for identifier in ids];record_types=[item.get('record_type') for item in records];tier=claim_doc.get('achieved_tier');required=U4_EVIDENCE_TYPES if tier in ('U4','U5') else U3_EVIDENCE_TYPES if tier=='U3' else set()
  if required and len(record_types)!=len(set(record_types)):errors.append('TIER_EVIDENCE_TYPE_CARDINALITY_INVALID');return
  by_type={item.get('record_type'):item for item in records}
  if required and set(by_type)!=required:
   errors.append('TIER_EVIDENCE_INCOMPLETE' if required-set(by_type) else 'TIER_EVIDENCE_TYPE_CARDINALITY_INVALID');return
  if required and len(records)!=len(required):errors.append('TIER_EVIDENCE_TYPE_CARDINALITY_INVALID');return
  expected_subject=canonical_digest(claim_evidence_subject(claim_doc))
  if any(item.get('subject_id')!=claim_doc.get('claim_key') or item.get('subject_digest')!=expected_subject or item.get('evidence_epoch')!=claim_doc.get('evidence_epoch') for item in records):errors.append('TIER_EVIDENCE_BINDING_INVALID');return
  if not required:return
  launcher=by_type['installed-package-launcher-evidence@1'];interruption=by_type['interruption-evidence@1'];recovery=by_type['recovery-evidence@1'];separation=by_type['actor-authority-separation@1'];acceptance=by_type['independent-acceptance-evidence@1']
  actors=(separation.get('actor_identity'),separation.get('authority_identity'),separation.get('independent_acceptor_identity'))
  u3_valid=s(launcher.get('installed_package_digest')) and s(launcher.get('launcher_digest')) and s(interruption.get('interruption_record_id')) and s(recovery.get('recovery_record_id')) and interruption['id'] in recovery.get('referenced_record_ids',[]) and len(set(actors))==3 and acceptance.get('independent_acceptor_identity')==separation.get('independent_acceptor_identity') and {launcher['id'],interruption['id'],recovery['id'],separation['id']}<=set(acceptance.get('referenced_record_ids',[]))
  if not u3_valid:errors.append('TIER_EVIDENCE_SEMANTICS_INVALID');return
  if tier in ('U4','U5'):
   boundary=by_type['native-boundary-identity@1'];deny=by_type['matched-deny-evidence@1'];allow=by_type['neighboring-allow-evidence@1'];failure=by_type['failure-behavior-evidence@1'];hook=by_type['hook-configuration-evidence@1'];boundary_id=boundary.get('native_boundary_identity');scope=boundary.get('actuator_scope')
   u4_valid=s(boundary_id) and s(scope) and deny.get('native_boundary_identity')==boundary_id and allow.get('native_boundary_identity')==boundary_id and hook.get('native_boundary_identity')==boundary_id and deny.get('actuator_scope')==scope and allow.get('actuator_scope')==scope and hook.get('actuator_scope')==scope and deny.get('decision')=='deny' and allow.get('decision')=='allow' and set(failure.get('failure_modes',[]))=={'timeout','crash','malformed-output'} and failure.get('failure_behavior') in ('fail-closed','demote-unverified') and s(hook.get('hook_config_digest')) and hook.get('hook_installed') is True and hook.get('hook_trusted') is True and hook.get('hook_active') is True
   if not u4_valid:errors.append('TIER_EVIDENCE_SEMANTICS_INVALID')

 for key,result_doc in result_map.items():
  claim_doc=claim_map.get(key)
  if not claim_doc:continue
  if result_doc.get('evidence_epoch')!=claim_doc.get('evidence_epoch'):errors.append('CONFORMANCE_EPOCH_MISMATCH')
  if result_doc.get('tier_evidence_set_digest')!=claim_doc.get('tier_evidence_set_digest') or result_doc.get('tier_evidence_artifact_ids')!=claim_doc.get('tier_evidence_artifact_ids'):errors.append('CONFORMANCE_EVIDENCE_MISMATCH')
  if result_doc.get('claim_digest')!=canonical_digest(claim_doc):errors.append('CONFORMANCE_CLAIM_DIGEST_MISMATCH')
  if not any(code.startswith('CLAIM_KEY_') for code in errors) and 'CAPABILITY_CLAIMS_DIGEST_MISMATCH' not in errors and 'CONFORMANCE_RESULTS_DIGEST_MISMATCH' not in errors:validate_tier_for_claim(claim_doc,result_doc)

 if any(code in errors for code in ('TIER_EVIDENCE_REFERENCE_UNRESOLVED','TIER_EVIDENCE_TYPE_CARDINALITY_INVALID','TIER_EVIDENCE_INCOMPLETE')):
  errors=[code for code in errors if code!='TIER_EVIDENCE_SET_NOT_EXACT']

 all_unverified=bool(base_items) and all(isinstance(item,dict) and item.get('disposition')=='unverified' for item in base_items)
 success_binding=None;claim_key_error=any(code.startswith('CLAIM_KEY_') for code in errors)
 if baseline_doc.get('success_terminal')=='bounded-product-usable':
  if all_unverified:
   errors.append('BASELINE_ALL_UNVERIFIED_PRODUCT_SUCCESS')
  elif not claim_key_error:
   if set(applicable_keys)!=set(claim_map) or set(applicable_keys)!=set(result_map):errors.append('BASELINE_PRODUCT_EVIDENCE_MISSING')
   unverified=False;baseline_by_claim={item.get('claim_key'):item for item in base_items if isinstance(item,dict)}
   for key in applicable_keys:
    claim_doc=claim_map.get(key,{});result_doc=result_map.get(key,{});consumer_item=baseline_by_claim.get(key,{});minimum=req_map.get(consumer_item.get('id'),{}).get('minimum_tier')
    if claim_doc.get('validity')!='verified' or result_doc.get('validity')!='verified':unverified=True;continue
    tier=claim_doc.get('achieved_tier')
    if result_doc.get('outcome')!='passed' or result_doc.get('success_terminal')!='bounded-product-usable' or claim_doc.get('rendered_status')!='current-usable' or tier not in rv['tiers'] or minimum not in rv['tiers'] or rv['tiers'].index(tier)<rv['tiers'].index(minimum):errors.append('BASELINE_PRODUCT_EVIDENCE_MISSING')
   if unverified or any(item.get('id') in req_map and item.get('disposition')=='unverified' for item in base_items if isinstance(item,dict)):errors.append('BASELINE_APPLICABLE_UNVERIFIED')
   capacities={claim_map[key].get('capacity_policy') for key in applicable_keys if key in claim_map};epochs={claim_map[key].get('evidence_epoch') for key in applicable_keys if key in claim_map}
   if applicable_keys and not unverified and len(capacities)==1 and len(epochs)==1:
    success_binding={'capacity_policy':next(iter(capacities)),'claim_keys':sorted(applicable_keys),'evidence_epoch':next(iter(epochs)),'capability_claims_digest':claim_set_digest,'conformance_results_digest':result_set_digest,'tier_evidence_set_digest':tier_evidence.get('content_digest'),'stage_c_authority_set_digest':stage_c_records.get('content_digest'),'evidence_trust_root_digest':evidence_trust_root.get('content_digest'),'evidence_source_set_digest':evidence_sources.get('content_digest')}
   elif applicable_keys and not unverified and (len(capacities)!=1 or len(epochs)!=1):errors.append('PRODUCT_SUCCESS_ROUTE_MIXED')
 elif claim_map or result_map:errors.append('REGISTRY_TERMINAL_CANNOT_CONSUME_PRODUCT_EVIDENCE')
 if 'CAPABILITY_CLAIMS_DIGEST_MISMATCH' in errors or 'CONFORMANCE_RESULTS_DIGEST_MISMATCH' in errors:success_binding=None

 stage_items=stage_c_records.get('records');stage_map={};stage_set_valid=record_digest(stage_c_records)==stage_c_records.get('content_digest')
 if not stage_set_valid:errors.append('STAGE_C_AUTHORITY_SET_DIGEST_MISMATCH')
 if not isinstance(stage_items,list):errors.append('STAGE_C_AUTHORITY_SET_INVALID');stage_items=[]
 for record in stage_items:
  errors.extend(schema_errors(schemas['stage_c_record'],record))
  if not isinstance(record,dict) or not s(record.get('id')):errors.append('STAGE_C_AUTHORITY_RECORD_INVALID');continue
  if record['id'] in stage_map:errors.append('STAGE_C_AUTHORITY_RECORD_DUPLICATE')
  stage_map[record['id']]=record
  if record_digest(record)!=record.get('content_digest'):errors.append('STAGE_C_AUTHORITY_RECORD_DIGEST_MISMATCH')
  if not s(record.get('rationale')):errors.append('STAGE_C_AUTHORITY_RECORD_INVALID')
 stage_types=[record.get('record_type') for record in stage_items if isinstance(record,dict)]
 stage_cardinality_invalid=bool(stage_items) and (len(stage_items)!=len(STAGE_C_TYPES) or len(stage_types)!=len(set(stage_types)) or set(stage_types)!=STAGE_C_TYPES)
 if stage_cardinality_invalid:errors.append('STAGE_C_AUTHORITY_CARDINALITY_INVALID')
 stage_outcome_invalid=any(STAGE_C_SUCCESS_OUTCOMES.get(record.get('record_type'))!=record.get('outcome') for record in stage_items if isinstance(record,dict) and record.get('record_type') in STAGE_C_TYPES)
 if stage_outcome_invalid:errors.append('STAGE_C_OUTCOME_INVALID')
 stage_source_unresolved=trusted_context and trust_root_resolved and any(not trusted_source_resolves(record) for record in stage_items if isinstance(record,dict))
 if stage_source_unresolved and not stage_cardinality_invalid and not stage_outcome_invalid:errors.append('AUTHORITATIVE_EVIDENCE_SOURCE_UNRESOLVED')

 transition_items=transitions.get('artifacts');transition_map={};invalid_transitions=set();fixture_forbidden=False
 if not isinstance(transition_items,list):errors.append('TRANSITION_ARTIFACT_SET_INVALID');transition_items=[]
 for artifact in transition_items:
  errors.extend(schema_errors(schemas['transition_artifact'],artifact))
  if not isinstance(artifact,dict) or not s(artifact.get('id')):errors.append('TRANSITION_ARTIFACT_INVALID');continue
  if artifact['id'] in transition_map:errors.append('TRANSITION_ARTIFACT_DUPLICATE')
  transition_map[artifact['id']]=artifact
  if record_digest(artifact)!=artifact.get('content_digest'):errors.append('TRANSITION_ARTIFACT_DIGEST_MISMATCH');invalid_transitions.add(artifact['id'])
  if artifact.get('issuer_identity')!=AUTHORIZED_ISSUER:errors.append('TRANSITION_ARTIFACT_ISSUER_UNAUTHORIZED');invalid_transitions.add(artifact['id'])
  authority=artifact.get('authority')
  if authority not in ('planning-order-only','fixture-only','resolved-stage-c-authority'):errors.append('TRANSITION_ARTIFACT_AUTHORITY_INVALID');invalid_transitions.add(artifact['id'])
  if artifact.get('subject_kind')!='planning-dag-edge@1':errors.append('TRANSITION_SUBJECT_KIND_MISMATCH');invalid_transitions.add(artifact['id'])
  if artifact.get('subject_id')!=f"{artifact.get('from')}->{artifact.get('to')}":errors.append('TRANSITION_SUBJECT_ID_MISMATCH');invalid_transitions.add(artifact['id'])
  if not s(artifact.get('rationale')):errors.append('TRANSITION_RATIONALE_MISSING');invalid_transitions.add(artifact['id'])
  expected_reference=census.get('evidence_record') if authority=='planning-order-only' else 'fixture-context:'+validation_context if authority=='fixture-only' else 'stage-c-authority-set@sha256:'+str(stage_c_records.get('content_digest'))
  if artifact.get('referenced_record')!=expected_reference:errors.append('TRANSITION_REFERENCED_RECORD_MISMATCH');invalid_transitions.add(artifact['id'])
  if authority=='fixture-only' and validation_context in ('authoritative','authoritative-equivalence'):fixture_forbidden=True
 if fixture_forbidden:errors.append('FIXTURE_ONLY_AUTHORITY_FORBIDDEN')
 transition_set_valid=record_digest(transitions)==transitions.get('content_digest')
 if not transition_set_valid:errors.append('TRANSITION_SET_DIGEST_MISMATCH')
 expected_bindings={'requirements_content_digest':requirements_doc.get('content_digest'),'baseline_content_digest':baseline_doc.get('content_digest'),'census_content_digest':census.get('content_digest'),'authority_artifacts_digest':authorities.get('content_digest'),'transition_artifacts_digest':transitions.get('content_digest'),'tier_evidence_set_digest':tier_evidence.get('content_digest'),'stage_c_authority_set_digest':stage_c_records.get('content_digest'),'evidence_trust_root_digest':evidence_trust_root.get('content_digest'),'evidence_source_set_digest':evidence_sources.get('content_digest'),'capability_claims_digest':claim_set_digest,'conformance_results_digest':result_set_digest}
 if dag_doc.get('bindings')!=expected_bindings:errors.append('DAG_BINDING_STALE')
 nodes={item.get('id'):item for item in dag_doc.get('nodes',[]) if isinstance(item,dict) and s(item.get('id'))};live_graph={key:[] for key in nodes};template_graph={key:[] for key in nodes};structural_template_graph={key:[] for key in nodes};edge_artifacts={}
 for edge_doc in dag_doc.get('edges',[]):
  if not isinstance(edge_doc,dict):continue
  artifact=transition_map.get(edge_doc.get('transition_artifact'))
  if not artifact:errors.append('DAG_TRANSITION_ARTIFACT_MISSING');continue
  if not transition_set_valid or artifact.get('id') in invalid_transitions:continue
  if artifact.get('from')!=edge_doc.get('from') or artifact.get('to')!=edge_doc.get('to') or artifact.get('edge_kind')!=edge_doc.get('kind') or artifact.get('record_type')!=TYPE_FOR_EDGE.get(edge_doc.get('kind')):errors.append('DAG_TRANSITION_ARTIFACT_BINDING_INVALID');continue
  subject=canonical_digest({'from':artifact.get('from'),'to':artifact.get('to'),'edge_kind':artifact.get('edge_kind'),'objective':artifact.get('rationale')})
  if artifact.get('subject_digest')!=subject:errors.append('DAG_TRANSITION_ARTIFACT_BINDING_INVALID');continue
  pair=(edge_doc.get('from'),edge_doc.get('to'));edge_artifacts[pair]=(edge_doc,artifact);structural_template_graph.setdefault(pair[0],[]).append(pair[1])
  edge_blocked=validation_context=='authoritative' and edge_doc.get('transition_artifact') in stage_a_affected and stage_a_blocked
  if not edge_blocked:template_graph.setdefault(pair[0],[]).append(pair[1])
  if edge_doc.get('mode')=='live':
   if artifact.get('resolution')!='resolved':errors.append('DAG_LIVE_EDGE_UNRESOLVED')
   elif not edge_blocked:live_graph.setdefault(pair[0],[]).append(pair[1])
  elif edge_doc.get('mode')=='template':
   if artifact.get('resolution')!='unresolved':errors.append('DAG_TEMPLATE_EDGE_RESOLVED')
  else:errors.append('DAG_EDGE_MODE_MISSING')
 live_reachable=reach(live_graph,'reviewed-contract');template_reachable=reach(template_graph,'reviewed-contract')
 incoming={identifier:0 for identifier in nodes}
 for targets in structural_template_graph.values():
  for target in targets:
   if target in incoming:incoming[target]+=1
 roots={identifier for identifier,count in incoming.items() if count==0};terminals={identifier for identifier,node_doc in nodes.items() if node_doc.get('terminal') is True}
 expected_terminals={'stage-a-decision-ready-not-usable','n-active-candidate','singleton-bounded-exact-claim','n-active-bounded-exact-claim'}
 if roots!={'reviewed-contract'} or terminals!=expected_terminals:errors.append('DAG_ROOT_TERMINAL_SET')
 if 'stage-a-portability-spike' not in live_reachable:errors.append('DAG_STAGE_A_SPIKE_UNREACHABLE')
 if not stage_a_blocked and 'stage-a-decision-ready-not-usable' not in live_reachable:errors.append('DAG_STAGE_A_UNREACHABLE')
 if {'n-active-candidate','n-active-bounded-exact-claim'}&live_reachable:errors.append('DAG_N_ACTIVE_PREMATURE')
 candidate='n-active-candidate';structural_reachable=reach(structural_template_graph,'reviewed-contract');kernel_fail=[(kernel,code) for kernel,code in KERNEL_CODES.items() if reaches_without(structural_template_graph,'reviewed-contract',candidate,kernel)]
 if candidate not in structural_reachable or 'n-active-bounded-exact-claim' not in structural_reachable:errors.append('DAG_N_ACTIVE_PREREQUISITE_MISSING')
 if 'singleton-bounded-exact-claim' not in reach(structural_template_graph,'stage-a-decision-ready-not-usable') or not reaches_without(structural_template_graph,'stage-a-decision-ready-not-usable','singleton-bounded-exact-claim','n-active-candidate'):errors.append('DAG_SINGLETON_ROUTE_MISSING')
 other_gates=('stage-a-portability-spike','frozen-n-active-successor-design','separate-n-active-gauntlet-go','explicit-n-active-operator-decision')
 general_bypass=any(reaches_without(structural_template_graph,'reviewed-contract',candidate,gate) for gate in other_gates)
 errors=[code for code in errors if code!='DAG_GATE_BYPASS']
 if general_bypass or len(kernel_fail)>1:errors.append('DAG_GATE_BYPASS')
 elif len(kernel_fail)==1:errors.append(kernel_fail[0][1])

 def stage_c_authority_resolves(binding,resolution):
  expected_scope='authoritative' if validation_context in ('authoritative','authoritative-equivalence') else 'fixture-only';expected_prefix='authoritative-stage-c-authority:' if expected_scope=='authoritative' else 'fixture-stage-c-authority:'
  resolution_ids=resolution.get('record_ids',[]) if isinstance(resolution,dict) else []
  if stage_cardinality_invalid or stage_outcome_invalid or not stage_set_valid or not isinstance(resolution,dict) or resolution.get('stage_c_authority_set_digest')!=stage_c_records.get('content_digest') or resolution.get('tier_evidence_set_digest')!=tier_evidence.get('content_digest') or resolution.get('evidence_trust_root_digest')!=evidence_trust_root.get('content_digest') or resolution.get('evidence_source_set_digest')!=evidence_sources.get('content_digest') or len(resolution_ids)!=len(STAGE_C_TYPES) or len(resolution_ids)!=len(set(resolution_ids)) or set(resolution_ids)!=set(stage_map):return False
  by_type={record['record_type']:record for record in stage_items}
  subject={key:binding.get(key) for key in ('capacity_policy','claim_keys','evidence_epoch','capability_claims_digest','conformance_results_digest','tier_evidence_set_digest')};subject_digest=canonical_digest(subject);audit=by_type['independently-retained-audit@1'];audit_id=audit['id']
  unresolved=False
  for kind,record in by_type.items():
   if record.get('authority_scope')!=expected_scope or not record.get('issuer_identity','').startswith(expected_prefix):unresolved=True
   if record.get('subject_kind')!='bounded-product-success@1' or record.get('subject_id')!='sha256:'+subject_digest or record.get('subject_digest')!=subject_digest or record.get('evidence_epoch')!=binding.get('evidence_epoch') or record.get('claim_keys')!=binding.get('claim_keys') or record.get('capability_claims_digest')!=binding.get('capability_claims_digest') or record.get('conformance_results_digest')!=binding.get('conformance_results_digest') or record.get('tier_evidence_set_digest')!=binding.get('tier_evidence_set_digest'):unresolved=True
   expected_decision=canonical_digest({'record_type':kind,'subject_digest':subject_digest,'actor_identity':record.get('actor_identity'),'outcome':record.get('outcome')})
   if record.get('decision_digest')!=expected_decision or record.get('independent_audit_record_id')!=audit_id or not s(record.get('principal_identity')) or not s(record.get('credential_class')) or not s(record.get('credential_digest')) or not s(record.get('enforcement_point')) or not s(record.get('enforcement_policy_digest')):unresolved=True
   if set(record.get('duties',[]))!=STAGE_C_DUTIES[kind] or set(record.get('incompatible_duty_pairs',[]))!=INCOMPATIBLE_DUTIES:errors.append('STAGE_C_DUTY_SEPARATION_INVALID')
  conform=by_type['exact-candidate-conformance@1'];ci=by_type['exact-head-ci@1'];accept=by_type['independent-acceptance@1'];promote=by_type['operator-promotion-decision@1'];principal=by_type['stage-c-principal-control@1']
  expected_audit_readback=canonical_digest({'audit_sink_identity':audit.get('audit_sink_identity'),'audit_record_digest':audit.get('audit_record_digest'),'retention_policy':audit.get('retention_policy'),'retention_days':audit.get('retention_days'),'readback_method':audit.get('readback_method'),'readback_principal_identity':audit.get('readback_principal_identity'),'readback_credential_class':audit.get('readback_credential_class'),'readback_credential_digest':audit.get('readback_credential_digest'),'evidence_epoch':audit.get('evidence_epoch')})
  if not s(conform.get('exact_candidate_digest')) or not s(ci.get('exact_head_commit')) or not s(ci.get('ci_run_digest')) or not s(accept.get('acceptance_verdict_digest')) or not s(promote.get('operator_decision_digest')) or not s(promote.get('promotion_scope')) or not s(principal.get('authority_matrix_digest')) or not s(audit.get('audit_sink_identity')) or not s(audit.get('audit_record_digest')) or not isinstance(audit.get('retention_days'),int) or audit.get('retention_days')<1 or not all(s(audit.get(field)) for field in ('retention_policy','readback_method','readback_principal_identity','readback_credential_class','readback_credential_digest','readback_digest')) or audit.get('readback_digest')!=expected_audit_readback or audit.get('readback_principal_identity') in {audit.get('principal_identity'),audit.get('actor_identity'),principal.get('principal_identity'),promote.get('principal_identity')}:unresolved=True
  expected_refs={
   'exact-candidate-conformance@1':set(identifier for claim_doc in claim_items for identifier in claim_doc.get('tier_evidence_artifact_ids',[])),
   'exact-head-ci@1':{conform['id']},
   'independent-acceptance@1':{conform['id'],ci['id'],principal['id'],audit_id},
   'operator-promotion-decision@1':{conform['id'],ci['id'],accept['id'],principal['id'],audit_id},
   'stage-c-principal-control@1':{audit_id},
   'independently-retained-audit@1':set(),
  }
  if any(set(record.get('referenced_record_ids',[]))!=expected_refs[kind] for kind,record in by_type.items()):unresolved=True
  actors=[record.get('actor_identity') for record in by_type.values()];principals=[record.get('principal_identity') for record in by_type.values()];credentials=[record.get('credential_digest') for record in by_type.values()];sources=[record.get('source_id') for record in by_type.values()] if expected_scope=='authoritative' else [];accept_actor=accept.get('actor_identity');tier_actors={value for record in tier_items if isinstance(record,dict) for value in (record.get('actor_identity'),record.get('authority_identity'))}
  if len(actors)!=len(set(actors)) or len(principals)!=len(set(principals)) or len(credentials)!=len(set(credentials)) or (sources and len(sources)!=len(set(sources))) or any(record.get('actor_identity')==record.get('principal_identity') for record in by_type.values()) or accept_actor in tier_actors or audit.get('principal_identity') in {principal.get('principal_identity'),promote.get('principal_identity')}:errors.append('STAGE_C_DUTY_SEPARATION_INVALID')
  if expected_scope=='authoritative' and (not trust_root_resolved or stage_source_unresolved):unresolved=True
  return not unresolved

 if success_binding:
  capacity=success_binding['capacity_policy']
  routes={
   'singleton-safe@1':(('stage-a-decision-ready-not-usable','singleton-exact-conformance'),('singleton-exact-conformance','singleton-independent-acceptance'),('singleton-independent-acceptance','singleton-promotion-operator-decision'),('singleton-promotion-operator-decision','singleton-bounded-exact-claim')),
   'n-active-unverified':(('n-active-candidate','n-active-exact-conformance'),('n-active-exact-conformance','n-active-independent-acceptance'),('n-active-independent-acceptance','n-active-promotion-operator-decision'),('n-active-promotion-operator-decision','n-active-bounded-exact-claim')),
  }
  route=routes.get(capacity,());terminal=route[-1][1] if route else None
  route_records=[edge_artifacts[pair][1] for pair in route if pair in edge_artifacts];resolution=route_records[0].get('authority_resolution') if len(route_records)==len(route) else None;stage_resolved=stage_c_authority_resolves(success_binding,resolution)
  if not stage_resolved and not stage_cardinality_invalid and not stage_outcome_invalid and 'AUTHORITATIVE_EVIDENCE_SOURCE_UNRESOLVED' not in errors and 'AUTHORITATIVE_EVIDENCE_TRUST_ROOT_UNRESOLVED' not in errors:errors.append('STAGE_C_AUTHORITY_UNRESOLVED')
  if not route or terminal not in live_reachable or any(pair not in edge_artifacts or edge_artifacts[pair][0].get('mode')!='live' for pair in route):errors.append('PRODUCT_SUCCESS_STAGE_C_ROUTE_MISSING')
  else:
   for pair in route:
    artifact=edge_artifacts[pair][1]
    if artifact.get('success_binding')!=success_binding:errors.append('PRODUCT_SUCCESS_STAGE_C_BINDING_MISMATCH');break
    if artifact.get('authority_resolution')!=resolution:errors.append('STAGE_C_AUTHORITY_UNRESOLVED');break
    if stage_resolved:
     if validation_context in ('synthetic-positive-control','negative-control'):
      if artifact.get('authority')!='fixture-only':errors.append('PRODUCT_SUCCESS_STAGE_C_AUTHORITY_INVALID');break
     elif not fixture_forbidden and artifact.get('authority')!='resolved-stage-c-authority':errors.append('PRODUCT_SUCCESS_STAGE_C_AUTHORITY_INVALID');break
 elif 'singleton-bounded-exact-claim' in live_reachable and baseline_doc.get('success_terminal')!='bounded-product-usable':errors.append('DAG_SINGLETON_PROMOTION_UNBOUND')
 n_active_awarded='n-active-candidate' in live_reachable
 return {'errors':sorted(set(errors)),'live_reachable':live_reachable,'template_reachable':template_reachable,'live_graph':live_graph,'template_graph':template_graph,'structural_template_graph':structural_template_graph,'n_active_awarded':n_active_awarded,'bundle':bundle}

def validate_root_report(root):
 try:
  bundle=load_root_bundle(root);report=validate_root_bundle(bundle)
  if not report['errors']:
   try:
    load_stage_a_verifier().replay_portability_root(Path(root).resolve())
    report=validate_root_bundle(bundle,stage_replay_verified=True)
   except Exception as error:report['errors']=['STAGE_A_ENTRYPOINT_UNAPPROVED' if str(error)=='STAGE_A_ENTRYPOINT_UNAPPROVED' else 'STAGE_A_EVIDENCE_OBJECT_MISSING' if str(error)=='BUNDLE_OBJECT_MISSING' else 'STAGE_A_EVIDENCE_REPLAY_FAILED']
  return report
 except DuplicateJsonMember:return {'errors':['DUPLICATE_JSON_MEMBER'],'live_reachable':set(),'template_reachable':set(),'n_active_awarded':False,'bundle':{}}
 except FileNotFoundError:return {'errors':['ARTIFACT_MISSING'],'live_reachable':set(),'template_reachable':set(),'n_active_awarded':False,'bundle':{}}
 except (OSError,json.JSONDecodeError,AttributeError,TypeError,KeyError,ValueError):return {'errors':['ARTIFACT_JSON_UNREADABLE'],'live_reachable':set(),'template_reachable':set(),'n_active_awarded':False,'bundle':{}}

def validate_root(root):return validate_root_report(root)['errors']

def load_fixture_bundle(root,fixture):
 base=load_root_bundle(root);manifest=load_json_path(Path(fixture)/'fixture-manifest.json')
 if schema_errors(base['schemas']['fixture_manifest'],manifest):raise ValueError('invalid fixture manifest schema')
 if manifest.get('record')!='portability-fixture@1' or manifest.get('base')!='authoritative' or manifest.get('base_digest')!=root_bundle_digest(base):raise ValueError('invalid fixture manifest')
 inherit=manifest.get('inherit');overrides=manifest.get('overrides')
 if not isinstance(inherit,list) or not isinstance(overrides,dict) or set(inherit)|set(overrides)!=set(PLANNING_ROOT_FILES) or set(inherit)&set(overrides):raise ValueError('incomplete fixture manifest')
 result={'schemas':base['schemas'],'stage_a_spike':base['stage_a_spike'],'stage_a_epoch':base['stage_a_epoch'],'stage_a_bundle':base['stage_a_bundle'],'stage_a_code_authority':base['stage_a_code_authority']}
 for kind in inherit:result[kind]=base[kind]
 for kind,filename in overrides.items():result[kind]=load_json_path(Path(fixture)/filename)
 return result

def validate_fixture_report(root,fixture):
 try:
  manifest=load_json_path(Path(fixture)/'fixture-manifest.json');return validate_root_bundle(load_fixture_bundle(root,fixture),validation_context=manifest.get('context'))
 except DuplicateJsonMember:return {'errors':['DUPLICATE_JSON_MEMBER'],'live_reachable':set(),'template_reachable':set(),'n_active_awarded':False,'bundle':{}}
 except (OSError,json.JSONDecodeError,AttributeError,TypeError,KeyError,ValueError):return {'errors':['FIXTURE_MANIFEST_INVALID'],'live_reachable':set(),'template_reachable':set(),'n_active_awarded':False,'bundle':{}}

def validate_fixture(root,fixture):return validate_fixture_report(root,fixture)['errors']

def main(a=None):
 parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--artifact',nargs=2,action='append');group.add_argument('--root');group.add_argument('--planning-root');args=parser.parse_args(a)
 if args.planning_root:
  try:report=validate_root_bundle(load_planning_root_bundle(Path(args.planning_root)),validation_context='planning-authority')
  except Exception:return 1
  print(json.dumps({'errors':report['errors'],'valid':not report['errors']},sort_keys=True));return 0 if not report['errors'] else 1
 if args.root:
  root=Path(args.root);report=validate_root_report(root);errors=list(report['errors']);rejected=0;accepted=0
  if not errors:
   invalid_root=root/'tests/invalid'
   for fixture in sorted((path for path in invalid_root.iterdir() if path.is_dir()),key=lambda path:path.name) if invalid_root.is_dir() else ():
    try:expected=(fixture/'expected-error.txt').read_text().strip()
    except OSError:errors.append('INVALID_FIXTURE_EXPECTATION_UNREADABLE');continue
    fixture_errors=validate_fixture(root,fixture)
    if fixture_errors==[expected]:rejected+=1
    else:errors.append('INVALID_FIXTURE_EXPECTATION_MISMATCH')
   valid_root=root/'tests/valid'
   for fixture in sorted((path for path in valid_root.iterdir() if path.is_dir()),key=lambda path:path.name) if valid_root.is_dir() else ():
    if not validate_fixture(root,fixture):accepted+=1
    else:errors.append('VALID_FIXTURE_REJECTED')
  result={'errors':sorted(set(errors)),'invalid_fixtures_rejected':rejected,'valid_fixtures_accepted':accepted,'n_active_awarded':report['n_active_awarded'],'live_reachable':sorted(report['live_reachable']),'valid':not errors}
  print(json.dumps(result,sort_keys=True));return 0 if not errors else 1
 paths={}
 for kind,value in args.artifact:
  if kind not in ARTIFACTS and kind not in ('scope_approval','capability_claims','conformance_results'):parser.error('unknown artifact kind: '+kind)
  if kind in ('capability_claims','conformance_results'):paths.setdefault(kind,[]).append(value)
  elif kind in paths:parser.error('artifact supplied twice: '+kind)
  else:paths[kind]=value
 errors=validate_paths(paths);print(json.dumps({'errors':errors,'valid':not errors},sort_keys=True));return 0 if not errors else 1

if __name__=='__main__':raise SystemExit(main())
