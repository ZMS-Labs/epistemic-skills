#!/usr/bin/env python3
"""Verify retained native-discovery transcripts through a bounded boundary."""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path

EMPTY=hashlib.sha256(b'').hexdigest()
def cb(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def digest(value):return hashlib.sha256(cb(value)).hexdigest()
def file_digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def subject(item):return {key:value for key,value in item.items() if key!='transcript_digest'}
def verify_item(item,root,epoch,authority):
 fields={'record','product','surface','evidence_epoch','authority_id','issuer_identity','readback_identity','platform','tool_sha256','executable_name','executable_path','executable_sha256','version','command','exit_code','stdout_sha256','stderr_sha256','served_bytes_sha256','readback_sha256','positive_discovery','neighboring_negative_rejected','status','reason','transcript_digest'}
 if not isinstance(item,dict) or set(item)!=fields or item.get('record')!='native-probe-transcript@1' or item.get('evidence_epoch')!=epoch or item.get('authority_id')!=authority['authority_id'] or item.get('issuer_identity')!=authority['probe_issuer_identity'] or item.get('readback_identity')!=authority['probe_readback_identity'] or item.get('issuer_identity')==item.get('readback_identity') or item.get('tool_sha256')!=authority['tools']['probe_tool']['sha256'] or item.get('transcript_digest')!=digest(subject(item)):raise RuntimeError('PROBE_TRANSCRIPT_INVALID')
 if item.get('platform')!='linux':return {'product':item['product'],'surface':item['surface'],'status':'unverified','executable_path':item['executable_path'],'version':item['version'],'boundary':'native transcript outside proven Linux scope','reason':'platform boundary unverified'}
 if item.get('status')=='unverified':
  if item.get('executable_path')!='unavailable' or item.get('executable_sha256')!='unavailable' or item.get('version')!='unavailable' or item.get('exit_code') is not None or item.get('stdout_sha256')!=EMPTY or item.get('stderr_sha256')!=EMPTY or item.get('served_bytes_sha256')!='unavailable' or item.get('readback_sha256')!='unavailable' or item.get('positive_discovery')!='unverified' or item.get('neighboring_negative_rejected')!='unverified' or shutil.which(item.get('executable_name','')) is not None:raise RuntimeError('PROBE_UNVERIFIED_NOT_CURRENT')
  return {'product':item['product'],'surface':item['surface'],'status':'unverified','executable_path':'unavailable','version':'unavailable','boundary':'retained authorized native probe transcript in disposable Linux home/workspace','reason':item['reason']}
 if item.get('status')!='observed':raise RuntimeError('PROBE_STATUS_INVALID')
 executable=(root/item.get('executable_path','')).resolve()
 try:executable.relative_to(root.resolve())
 except ValueError:raise RuntimeError('PROBE_EXECUTABLE_ESCAPE')
 if not executable.is_file() or file_digest(executable)!=item.get('executable_sha256'):raise RuntimeError('PROBE_EXECUTABLE_INVALID')
 command=item.get('command');
 if not isinstance(command,list) or not command or command[0]!=item.get('executable_path') or not all(isinstance(x,str) for x in command):raise RuntimeError('PROBE_COMMAND_INVALID')
 with tempfile.TemporaryDirectory(prefix='zms-native-probe-') as temporary:
  base=Path(temporary);home=base/'home';workspace=base/'workspace';home.mkdir();workspace.mkdir();env={'HOME':str(home),'PATH':str(executable.parent), 'LANG':'C','LC_ALL':'C'}
  completed=subprocess.run([str(executable),*command[1:]],cwd=workspace,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
 if completed.returncode!=item.get('exit_code') or hashlib.sha256(completed.stdout).hexdigest()!=item.get('stdout_sha256') or hashlib.sha256(completed.stderr).hexdigest()!=item.get('stderr_sha256'):raise RuntimeError('PROBE_EXECUTION_MISMATCH')
 try:payload=json.loads(completed.stdout)
 except Exception as error:raise RuntimeError('PROBE_OUTPUT_INVALID') from error
 expected={'version':item.get('version'),'served_bytes_sha256':item.get('served_bytes_sha256'),'readback_sha256':item.get('readback_sha256'),'positive_discovery':True,'neighboring_negative_rejected':True}
 if payload!=expected or item.get('positive_discovery') is not True or item.get('neighboring_negative_rejected') is not True or item.get('served_bytes_sha256')!=item.get('readback_sha256'):raise RuntimeError('PROBE_ORACLE_MISMATCH')
 return {'product':item['product'],'surface':item['surface'],'status':'observed','executable_path':item['executable_path'],'version':item['version'],'boundary':'authorized discriminating native discovery and neighboring-negative readback in disposable Linux home/workspace','reason':item['reason']}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--transcripts',type=Path,required=True);p.add_argument('--authority',type=Path,required=True);p.add_argument('--epoch',required=True);a=p.parse_args(argv)
 doc=json.loads(a.transcripts.read_text());authority=json.loads(a.authority.read_text());items=doc.get('transcripts') if isinstance(doc,dict) and set(doc)=={'record','transcripts'} and doc.get('record')=='native-probe-transcript-set@1' else None
 if not isinstance(items,list) or not items:raise RuntimeError('PROBE_TRANSCRIPT_SET_INVALID')
 observations=[verify_item(item,a.root.resolve(),a.epoch,authority) for item in items]
 if len({(x['product'],x['surface']) for x in observations})!=len(observations):raise RuntimeError('PROBE_TRANSCRIPT_DUPLICATE')
 print(json.dumps({'record':'native-probe-verdict@1','observations':observations},sort_keys=True));return 0
if __name__=='__main__':
 try:raise SystemExit(main())
 except BaseException as error:
  if isinstance(error,SystemExit) and isinstance(error.code,int):raise
  print('REFUSED PROBE_TRANSCRIPT_UNRESOLVED: '+type(error).__name__);raise SystemExit(2) from None
