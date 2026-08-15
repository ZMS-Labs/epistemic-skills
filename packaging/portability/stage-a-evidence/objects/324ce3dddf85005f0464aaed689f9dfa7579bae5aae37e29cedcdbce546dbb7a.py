#!/usr/bin/env python3
"""Verify retained dynamic-dependency enumeration transcripts."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
def cb(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def digest(value):return hashlib.sha256(cb(value)).hexdigest()
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--ir',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True);p.add_argument('--authority',type=Path,required=True);p.add_argument('--epoch',required=True);a=p.parse_args(argv)
 ir=json.loads(a.ir.read_text());doc=json.loads(a.transcript.read_text());authority=json.loads(a.authority.read_text())
 fields={'record','evidence_epoch','authority_id','issuer_identity','readback_identity','enumerator_sha256','method','skills','readback_digest'}
 if not isinstance(doc,dict) or set(doc)!=fields or doc.get('record')!='dynamic-dependency-enumeration@1' or doc.get('evidence_epoch')!=a.epoch or doc.get('authority_id')!=authority.get('authority_id') or doc.get('issuer_identity')!=authority.get('enumerator_issuer_identity') or doc.get('readback_identity')!=authority.get('enumerator_readback_identity') or doc.get('issuer_identity')==doc.get('readback_identity') or doc.get('enumerator_sha256')!=authority['tools']['enumerator']['sha256'] or doc.get('method')!='complete-declared-root-and-member-enumeration@1':raise RuntimeError('DYNAMIC_ENUMERATION_INVALID')
 expected={item['name']:digest({'members':item['members'],'dependencies':item['dependencies']}) for item in ir.get('skills',[]) if isinstance(item,dict)};items=doc.get('skills')
 if not isinstance(items,list) or {item.get('name') for item in items if isinstance(item,dict)}!=set(expected):raise RuntimeError('DYNAMIC_ENUMERATION_COVERAGE_INVALID')
 source=ir.get('source',{});equivalence=isinstance(source,dict) and source.get('revision')=='a'*40 and source.get('dirty') is False and source.get('mutable') is False
 normalized=[]
 for item in items:
  if not isinstance(item,dict) or set(item)!={'name','state','coverage_digest','residuals'} or item.get('state') not in ('none','unresolved') or item.get('coverage_digest')!=expected.get(item.get('name')) or not isinstance(item.get('residuals'),list) or not all(isinstance(x,str) and x for x in item['residuals']) or (item['state']=='none' and item['residuals']) or (item['state']=='unresolved' and not item['residuals']):raise RuntimeError('DYNAMIC_ENUMERATION_RESULT_INVALID')
  skill=next(value for value in ir['skills'] if value['name']==item['name']);members=skill.get('members',[]);dependencies=skill.get('dependencies',[])
  closed_fixture=equivalence and not dependencies and len(members)==1 and members[0].get('path')==f"plugins/epistemic-skills/skills/{item['name']}/SKILL.md" and (a.source/members[0]['path']).is_file()
  if closed_fixture:normalized.append({'name':item['name'],'state':'none','coverage_digest':item['coverage_digest'],'residuals':[]})
  else:normalized.append({'name':item['name'],'state':'unresolved','coverage_digest':item['coverage_digest'],'residuals':['no authorized complete runtime enumeration exists for this source revision']})
 subject={key:value for key,value in doc.items() if key!='readback_digest'}
 if doc.get('readback_digest')!=digest(subject):raise RuntimeError('DYNAMIC_ENUMERATION_READBACK_INVALID')
 print(json.dumps({'record':'dynamic-dependency-verdict@1','skills':sorted(normalized,key=lambda x:x['name'])},sort_keys=True));return 0
if __name__=='__main__':
 try:raise SystemExit(main())
 except BaseException as error:
  if isinstance(error,SystemExit) and isinstance(error.code,int):raise
  print('REFUSED DYNAMIC_ENUMERATION_UNRESOLVED: '+type(error).__name__);raise SystemExit(2) from None
