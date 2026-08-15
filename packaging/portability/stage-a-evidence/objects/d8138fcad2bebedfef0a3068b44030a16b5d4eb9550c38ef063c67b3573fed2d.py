#!/usr/bin/env python3
"""Replay retained Stage-A evidence without repository-history dependencies."""
from __future__ import annotations
import argparse,hashlib,json,os,re,shutil,subprocess,sys,tarfile,tempfile
from pathlib import Path,PurePosixPath

ROOT=Path(__file__).resolve().parents[2]
APPROVED_EXECUTION_AUTHORITY_DIGEST="2a1a18ac98973f9e4d6ead47c7fe81c9238044c190ee7b697d4688f480e2e46d"
APPROVED_RUNNER_DIGEST="7b9db15350b0da4e9ae2eb3e5122abc5be79a7766cf53c86bfb2442d537e32e3"
APPROVED_VALIDATOR_LOGIC_DIGEST="309acdd1b77ec0eaec861cdd097f3f24cf34a0c75999d025ab35dce9b2a16cd4"
APPROVED_CODE_DIGESTS={
 "artifact_library":"f0ce3ebf462129513abb4dfa034be3959d9ead326bc6f0cfc0fd8938fc1f5c44",
 "enumerator":"3a0f48fa1da818f95c066e406cc79885f1f7a32c467754a3b90a67d059dc2e21",
 "generator":"f34321a8065a224e0114d5e8bdba4d486229d96f726f37b654973435ad8d6597",
 "generator_executor":"5ebd7d24742f28a747058284742799f42b9b3a77a76578420330e5963e2eac1d",
 "probe_tool":"55536d2dfed00d42cd9093aa270d3f07e4a07cc4b2354dc81fa75e3720406de4",
}
VALIDATOR_PIN_PATTERN=re.compile(rb'(?m)^(STAGE_A_(?:RUNNER|VERIFIER)_SHA256=)"[0-9a-f]{64}"$')
EXPECTED_RESOLVERS={
 "source":"object-tree","ir":"derived","generator":"object-file","transform":"object-file","projection":"derived","profile":"object-file","host":"object-file","installer":"object-file","installed":"derived","consumer":"object-file","planning_dag":"root-member","dependency_contract":"root-member","epoch":"root-member","contract_validator":"object-file","authoritative_root":"object-tree","dynamic_dependencies":"object-file","artifact_library":"object-file","runner":"object-file","verifier":"object-file","generator_executor":"object-file","probe_tool":"object-file","enumerator":"object-file","code_authority":"root-member",
}
EXPECTED_ROOT_MEMBERS={
 "planning_dag":"planning-dag.json",
 "dependency_contract":"packaging/portability/dependencies.json",
 "epoch":"stage-a-evidence-epoch.json",
 "code_authority":"stage-a-execution-authority.json",
}
class ReplayError(RuntimeError):pass
def cb(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def sha(data):return hashlib.sha256(data).hexdigest()
def validator_logic_digest(data):
 normalized,replacements=VALIDATOR_PIN_PATTERN.subn(lambda match:match.group(1)+b'"'+b'0'*64+b'"',data)
 if replacements!=2:raise ReplayError('BUNDLE_CODE_UNAPPROVED')
 return sha(normalized)
def strict_json(path):
 def reject(pairs):
  out={}
  for key,value in pairs:
   if key in out:raise ReplayError('BUNDLE_DUPLICATE_JSON_MEMBER')
   out[key]=value
  return out
 try:return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=reject)
 except ReplayError:raise
 except BaseException as error:raise ReplayError('BUNDLE_JSON_UNREADABLE') from error
def object_path(portability,raw):
 try:relative=PurePosixPath(raw);parts=relative.parts;prefix=('packaging','portability')
 except BaseException as error:raise ReplayError('BUNDLE_OBJECT_PATH_INVALID') from error
 if parts[:2]!=prefix or '..' in parts or '\\' in raw:raise ReplayError('BUNDLE_OBJECT_PATH_INVALID')
 path=portability.joinpath(*parts[2:])
 if not path.is_file():raise ReplayError('BUNDLE_OBJECT_MISSING')
 return path
def extract_tree(archive,destination):
 try:
  with tarfile.open(archive,'r:') as tar:
   for member in tar.getmembers():
    pure=PurePosixPath(member.name)
    if pure.is_absolute() or '..' in pure.parts or '\\' in member.name or not (member.isdir() or member.isfile()):raise ReplayError('BUNDLE_TREE_OBJECT_INVALID')
    target=destination.joinpath(*pure.parts)
    if member.isdir():target.mkdir(parents=True,exist_ok=True);continue
    stream=tar.extractfile(member)
    if stream is None:raise ReplayError('BUNDLE_TREE_OBJECT_INVALID')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(stream.read());target.chmod(member.mode & 0o777)
 except ReplayError:raise
 except BaseException as error:raise ReplayError('BUNDLE_TREE_OBJECT_UNREADABLE') from error
def verify_manifest(bundle,request,result):
 fields={'record','source_revision','code_revision','authoritative_revision','code_authority_digest','canonical_request','artifact_resolvers','request_digest','result_digest','content_digest'}
 if not isinstance(bundle,dict) or set(bundle)!=fields or bundle.get('record')!='stage-a-portability-evidence-bundle@2':raise ReplayError('BUNDLE_SHAPE_INVALID')
 if bundle.get('code_authority_digest')!=APPROVED_EXECUTION_AUTHORITY_DIGEST:raise ReplayError('BUNDLE_CODE_AUTHORITY_UNAPPROVED')
 if bundle.get('source_revision')!='content-addressed-tree-sha256:'+request.get('artifacts',{}).get('source',{}).get('sha256','') or bundle.get('authoritative_revision')!='content-addressed-tree-sha256:'+request.get('artifacts',{}).get('authoritative_root',{}).get('sha256',''):raise ReplayError('BUNDLE_REVISION_IDENTITY_INVALID')
 if bundle.get('code_revision')!='execution-authority-sha256:'+APPROVED_EXECUTION_AUTHORITY_DIGEST:raise ReplayError('BUNDLE_CODE_REVISION_UNAPPROVED')
 if sha(cb({key:value for key,value in bundle.items() if key!='content_digest'}))!=bundle.get('content_digest'):raise ReplayError('BUNDLE_CONTENT_DIGEST_MISMATCH')
 if request!=bundle.get('canonical_request') or sha(cb(request))!=bundle.get('request_digest'):raise ReplayError('BUNDLE_REQUEST_DIGEST_MISMATCH')
 if sha(cb(result))!=bundle.get('result_digest'):raise ReplayError('BUNDLE_RESULT_DIGEST_MISMATCH')
 resolvers=bundle.get('artifact_resolvers');artifacts=request.get('artifacts') if isinstance(request,dict) else None
 if not isinstance(resolvers,dict) or not isinstance(artifacts,dict) or set(resolvers)!=set(EXPECTED_RESOLVERS) or set(artifacts)!=set(EXPECTED_RESOLVERS):raise ReplayError('BUNDLE_RESOLVER_SET_MISMATCH')
 for name,kind in EXPECTED_RESOLVERS.items():
  resolver=resolvers[name];descriptor=artifacts[name];fields={'resolver','artifact_kind','sha256'}
  if kind in ('object-tree','object-file'):fields|={'path','object_sha256'}
  elif kind=='root-member':fields|={'member'}
  if not isinstance(resolver,dict) or set(resolver)!=fields or resolver.get('resolver')!=kind or resolver.get('artifact_kind')!=descriptor.get('kind') or resolver.get('sha256')!=descriptor.get('sha256'):raise ReplayError('BUNDLE_RESOLVER_INVALID')
  if kind=='object-file' and resolver.get('object_sha256')!=resolver.get('sha256'):raise ReplayError('BUNDLE_OBJECT_DESCRIPTOR_SPLIT')
  if kind=='root-member' and resolver.get('member')!=EXPECTED_ROOT_MEMBERS.get(name):raise ReplayError('BUNDLE_RESOLVER_INVALID')
 for name,digest in {**APPROVED_CODE_DIGESTS,'runner':APPROVED_RUNNER_DIGEST}.items():
  if artifacts[name].get('sha256')!=digest or resolvers[name].get('sha256')!=digest:raise ReplayError('BUNDLE_CODE_UNAPPROVED')
 verifier_digest=sha(Path(__file__).read_bytes())
 if artifacts['verifier'].get('sha256')!=verifier_digest or resolvers['verifier'].get('sha256')!=verifier_digest:raise ReplayError('BUNDLE_CODE_UNAPPROVED')
 return bundle
def verify_object_files(portability,resolvers):
 for name,kind in EXPECTED_RESOLVERS.items():
  if kind!='object-file':continue
  resolver=resolvers[name];path=object_path(portability,resolver['path'])
  try:data=path.read_bytes()
  except BaseException as error:raise ReplayError('BUNDLE_OBJECT_UNREADABLE') from error
  actual=sha(data)
  if actual!=resolver.get('sha256') or actual!=resolver.get('object_sha256'):raise ReplayError('BUNDLE_OBJECT_DIGEST_MISMATCH')
  if name=='contract_validator' and validator_logic_digest(data)!=APPROVED_VALIDATOR_LOGIC_DIGEST:raise ReplayError('BUNDLE_CODE_UNAPPROVED')
def copy_object(portability,resolver,target):
 source=object_path(portability,resolver['path'])
 try:data=source.read_bytes()
 except BaseException as error:raise ReplayError('BUNDLE_OBJECT_UNREADABLE') from error
 if sha(data)!=resolver.get('object_sha256'):raise ReplayError('BUNDLE_OBJECT_DIGEST_MISMATCH')
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
def run_child(command,code,timeout=20,parse_json=True):
 try:result=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout,env={'PATH':'','LANG':'C','LC_ALL':'C'})
 except BaseException as error:raise ReplayError(code) from error
 if result.returncode:raise ReplayError(code)
 if not parse_json:return result.stdout
 try:return json.loads(result.stdout)
 except BaseException as error:raise ReplayError(code) from error
def replay_portability_root(portability):
 portability=Path(portability).resolve();bundle=verify_manifest(strict_json(portability/'stage-a-portability-spike.bundle.json'),strict_json(portability/'stage-a-evidence/request.json'),strict_json(portability/'stage-a-portability-spike.json'));request=bundle['canonical_request'];resolvers=bundle['artifact_resolvers'];verify_object_files(portability,resolvers)
 with tempfile.TemporaryDirectory(prefix='zms-stage-a-replay-') as temporary:
  work=Path(temporary)
  for name in ('source','authoritative_root'):
   resolver=resolvers[name];archive=object_path(portability,resolver['path'])
   try:data=archive.read_bytes()
   except BaseException as error:raise ReplayError('BUNDLE_OBJECT_UNREADABLE') from error
   if sha(data)!=resolver['object_sha256']:raise ReplayError('BUNDLE_OBJECT_DIGEST_MISMATCH')
   extract_tree(archive,work/('source' if name=='source' else 'authoritative-root'))
  for name,kind in EXPECTED_RESOLVERS.items():
   if kind!='object-file':continue
   copy_object(portability,resolvers[name],work/request['artifacts'][name]['path'])
  root_members={'planning_dag':'planning-dag.json','epoch':'stage-a-evidence-epoch.json','code_authority':'stage-a-execution-authority.json','dependency_contract':'../source/packaging/portability/dependencies.json'}
  for name,member in root_members.items():
   source=(work/'source/packaging/portability/dependencies.json') if name=='dependency_contract' else (work/'authoritative-root'/member)
   target=work/request['artifacts'][name]['path'];target.parent.mkdir(parents=True,exist_ok=True)
   if source.resolve()!=target.resolve():shutil.copy2(source,target)
  authority=strict_json(work/'authoritative-root/stage-a-execution-authority.json')
  if sha(cb(authority))!=APPROVED_EXECUTION_AUTHORITY_DIGEST:raise ReplayError('BUNDLE_CODE_AUTHORITY_UNAPPROVED')
  materialize=work/'materialize.json';materialize.write_bytes(cb({'source':str(work/'source'),'source_record':{'kind':'content-addressed-tree','revision':request['artifacts']['source']['sha256'],'dirty':False,'mutable':False},'profile':strict_json(work/'profile.json'),'generator':str(work/'.github/scripts/build_portable_skill_projection.py'),'artifact_library':str(work/'.github/scripts/skill_artifact_lib.py'),'out_dir':str(work/'projection-output')}))
  verdict=run_child([sys.executable,'-I',str(work/'.github/scripts/execute_portability_generator.py'),'--materialize-request',str(materialize)],'BUNDLE_DERIVATION_FAILED')
  if verdict.get('record')!='generator-materialization-verdict@1' or verdict.get('status')!='passed':raise ReplayError('BUNDLE_DERIVATION_FAILED')
  shutil.copy2(work/'projection-output/PORTABILITY-IR.json',work/'ir.json');shutil.copy2(work/'projection-output/PROJECTION-RESULT.json',work/'projection.json')
  request_path=work/'request.json';request_path.write_bytes(cb(request));output=work/'result.json'
  run_child([sys.executable,'-s','-E',str(work/'.github/scripts/run_portability_spike.py'),'--root',str(work),'--request',str(request_path),'--out',str(output)],'BUNDLE_REPLAY_FAILED',30,False)
  replayed=output.read_bytes()
  if replayed!=(portability/'stage-a-portability-spike.json').read_bytes():raise ReplayError('BUNDLE_RESULT_NOT_BYTE_IDENTICAL')
  return replayed
def replay(repo_root=ROOT):return replay_portability_root(Path(repo_root)/'packaging/portability')
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args(argv);replay(args.root);print('verified-byte-identical');return 0
if __name__=='__main__':
 try:raise SystemExit(main())
 except BaseException as error:
  if isinstance(error,SystemExit) and isinstance(error.code,int):raise
  code=str(error) if isinstance(error,ReplayError) else 'BUNDLE_VERIFIER_FAILED'
  print('REFUSED '+code);raise SystemExit(2) from None
