#!/usr/bin/env python3
"""Execute the approved portability generator in an isolated child process."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path

def cb(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def tree_hash(root):
 module=sys.modules['skill_artifact_lib'];return module.portable_tree_sha256(root)
def main(argv=None):
 parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--request',type=Path);group.add_argument('--materialize-request',type=Path);args=parser.parse_args(argv);request=load(args.request or args.materialize_request)
 common={'source','source_record','profile','generator','artifact_library'};fields=common|({'expected_ir','expected_projection','expected_installed'} if args.request else {'out_dir'})
 if not isinstance(request,dict) or set(request)!=fields:raise RuntimeError('GENERATOR_EXECUTOR_REQUEST_INVALID')
 generator=Path(request['generator']).resolve();library=Path(request['artifact_library']).resolve()
 if generator.parent!=library.parent or generator.name!='build_portable_skill_projection.py' or library.name!='skill_artifact_lib.py':raise RuntimeError('GENERATOR_EXECUTOR_CODE_LAYOUT_INVALID')
 if 'skill_artifact_lib' in sys.modules:raise RuntimeError('GENERATOR_EXECUTOR_PRELOADED_ALIAS')
 sys.path.insert(0,str(generator.parent))
 try:
  spec=importlib.util.spec_from_file_location('approved_portability_generator',generator)
  if spec is None or spec.loader is None:raise RuntimeError('GENERATOR_EXECUTOR_IMPORT_INVALID')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  imported=sys.modules.get('skill_artifact_lib')
  if imported is None or Path(imported.__file__).resolve()!=library:raise RuntimeError('GENERATOR_EXECUTOR_LIBRARY_ALIAS')
  if getattr(module,'GENERATOR_REVISION',None)!='phase1-v1':raise RuntimeError('GENERATOR_EXECUTOR_REVISION_INVALID')
  if args.materialize_request:
   result=module.build_projection(Path(request['source']),Path(request['out_dir']),request['source_record'],request['profile'])
   print(json.dumps({'record':'generator-materialization-verdict@1','status':'passed','ir_path':str(result.ir_path),'projection_path':str(result.result_path),'installed_path':str(result.projection_root)},sort_keys=True));return 0
  with tempfile.TemporaryDirectory(prefix='zms-generator-child-') as temporary:
   root=Path(temporary);source=root/'source';shutil.copytree(Path(request['source']),source)
   result=module.build_projection(source,root/'projection',request['source_record'],request['profile'])
   if result.ir_path.read_bytes()!=Path(request['expected_ir']).read_bytes():raise RuntimeError('GENERATOR_EXECUTOR_IR_MISMATCH')
   if result.result_path.read_bytes()!=Path(request['expected_projection']).read_bytes():raise RuntimeError('GENERATOR_EXECUTOR_PROJECTION_MISMATCH')
   digest=tree_hash(result.projection_root)
   if digest!=tree_hash(Path(request['expected_installed'])):raise RuntimeError('GENERATOR_EXECUTOR_INSTALLED_MISMATCH')
   shutil.rmtree(source)
   if tree_hash(result.projection_root)!=digest:raise RuntimeError('GENERATOR_EXECUTOR_MUTATION_INDEPENDENCE_FAILED')
  print(json.dumps({'record':'generator-execution-verdict@1','status':'passed','generator_path':str(generator),'artifact_library_path':str(library)},sort_keys=True));return 0
 finally:
  sys.path.pop(0)
if __name__=='__main__':
 try:raise SystemExit(main())
 except BaseException as error:
  if isinstance(error,SystemExit) and isinstance(error.code,int):raise
  print('REFUSED GENERATOR_EXECUTOR_FAILED: '+type(error).__name__);raise SystemExit(2) from None
