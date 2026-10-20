from pathlib import Path
import subprocess,hashlib,json,sys,tempfile,shutil,re,platform,datetime
root=Path.cwd();out=root.parent/'validation';base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
sha=lambda data:hashlib.sha256(data).hexdigest()
prior=out/'macos-custody-followup.patch';assert sha(prior.read_bytes())=='d2712bee7e0bd5e4dab1b06992873630be4ee37624c13170cea0f680fd21d821'
# Keep the previous bounded candidate/receipt unchanged as historical evidence.
assert sha((out/'issue162-local-safeguard.patch').read_bytes())=='d536dc6a8294b16c3c77388fcb9891b3d0fda8634ad6d7fe34f52cd4b8762d0d'
tracked=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines();added=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines();files=tracked+added
with tempfile.TemporaryDirectory(prefix='identity-continuation-replay-',dir=out) as td:
 temp=Path(td);a=temp/'a';b=temp/'b';c=temp/'c';a.mkdir();c.mkdir()
 for name in tracked:
  data=subprocess.check_output(['git','show',base+':'+name])
  for directory in (a,c):
   target=directory/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 p=subprocess.run(['git','apply',str(prior)],cwd=a,capture_output=True,text=True);assert p.returncode==0,p.stderr
 shutil.copytree(a,b)
 for name in files:
  target=b/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((root/name).read_bytes())
 diff=subprocess.run(['git','diff','--no-index','--binary','--','a','b'],cwd=temp,capture_output=True);assert diff.returncode==1 and not diff.stderr
 patch=diff.stdout
 patch=re.sub(rb'(?m)^diff --git a/[ab]/(.*?) b/[ab]/(.*?)$',rb'diff --git a/\1 b/\2',patch)
 patch=re.sub(rb'(?m)^--- a/[ab]/',b'--- a/',patch);patch=re.sub(rb'(?m)^\+\+\+ b/[ab]/',b'+++ b/',patch)
 delta=out/'issue162-validated-local-safeguard.patch';delta.write_bytes(patch)
 p=subprocess.run(['git','apply','--check',str(delta)],cwd=a,capture_output=True,text=True);assert p.returncode==0,p.stderr
 p=subprocess.run(['git','apply',str(delta)],cwd=a,capture_output=True,text=True);assert p.returncode==0,p.stderr
 for name in files:assert (a/name).read_bytes()==(root/name).read_bytes(),name
 # Separate combined replay is provided for inspection; it grants no authority
 # to integrate earlier manual changes or this implementation.
 combined=subprocess.check_output(['git','diff','--binary'])
 for name in added:
  p=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],capture_output=True);assert p.returncode==1 and not p.stderr;combined+=p.stdout
 combinedfile=out/'issue162-combined-local-candidate.patch';combinedfile.write_bytes(combined)
 p=subprocess.run(['git','apply',str(combinedfile)],cwd=c,capture_output=True,text=True);assert p.returncode==0,p.stderr
 for name in files:assert (c/name).read_bytes()==(root/name).read_bytes(),name
schemas=[]
for path in sorted((root/'plugins/epistemic-skills/contracts/mission-custody').glob('*.schema.json')):
 name=str(path.relative_to(root));assert path.read_bytes()==subprocess.check_output(['git','show',base+':'+name]);schemas.append({'path':name,'sha256':sha(path.read_bytes())})
lock='plugins/epistemic-skills/contracts/mission-custody/requirements-jsonschema-parity-ubuntu-py312.txt';assert (root/lock).read_bytes()==subprocess.check_output(['git','show',base+':'+lock])
expected=dict(re.findall(r'^([a-zA-Z0-9-]+)==([^\s\\]+)',(root/lock).read_text(),re.M))
envs={}
for label,directory in [('py312','issue162-py312-env'),('py314','issue162-parity-env')]:
 executable=out/directory/'bin/python';code='import importlib.metadata as m,json; print(json.dumps({p:m.version(p) for p in '+repr(list(expected))+'}))'
 versions=json.loads(subprocess.check_output([str(executable),'-c',code],text=True));assert versions==expected
 envs[label]={'executable':str(executable),'versions':versions,'isolated':True,'source':'official PyPI; binary-only required hashes; platform-specific digest verified from official metadata'}
matrix=json.loads((out/'issue162-continuation-matrix.json').read_text());sim=[row for row in matrix if row['mode']=='compatible-measurement-simulation'];assert len(sim)==6 and all(row['exit']==0 for row in sim)
assert sum(row['printed_ok_checks'] for row in sim)==2299
native=json.loads((out/'issue162-native-case-diagnosis.json').read_text());failures=[row for row in native if row['error'] or row['failed_checks']];direct=[row for row in failures if row['error'] and 'KNOWN_MISMATCH' in row['error']['message']]
cascades=json.loads((out/'issue162-native-cascade-diagnosis.json').read_text());assert len(native)==275 and len(failures)==208 and len(direct)==188 and len(cascades)==20 and all(row['managed_refusal_evidence'] for row in cascades)
remaining=[{'module':row['module'],'case':row['case'],'classification':'direct KNOWN_MISMATCH refusal' if row in direct else 'assertion cascade after captured CLI KNOWN_MISMATCH refusal','failed_checks':row['failed_checks'],'exception':row['error']['type'] if row['error'] else None} for row in failures]
(out/'issue162-remaining-native-failures.json').write_text(json.dumps(remaining,indent=2)+'\n')
receipt={
 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'repository':'https://github.com/ZMS-Labs/epistemic-skills','worktree':str(root),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'base':base,
 'state':'LOCAL VALIDATION COMPLETE WITH EXPLICIT PLATFORM LIMITS; UNCOMMITTED; INTEGRATION HELD; ISSUE162 OPEN',
 'implementation_delta':{'file':delta.name,'sha256':sha(delta.read_bytes()),'baseline':base+' plus separately preserved prior test patch '+sha(prior.read_bytes()),'replay_to_exact_working_files':'PASS'},
 'combined_inspection_patch':{'file':combinedfile.name,'sha256':sha(combinedfile.read_bytes()),'baseline':base,'replay_to_exact_working_files':'PASS','does_not_grant_integration_authority':True},
 'prior_candidate_preserved':{'patch':'issue162-local-safeguard.patch','sha256':sha((out/'issue162-local-safeguard.patch').read_bytes()),'receipt':'issue162-local-implementation-receipt.json'},
 'changed_files':[{'path':name,'sha256':sha((root/name).read_bytes())} for name in files],
 'fixture_preservation':json.loads((out/'issue162-fixture-preservation.json').read_text()),
 'schema_files_unchanged':schemas,'original_dependency_lock_unchanged':{'path':lock,'sha256':sha((root/lock).read_bytes())},
 'test_environments':envs,'system_python_defaults_unchanged':'python3 remains 3.14.7; existing bundled 3.12.14 used only via explicit path/local venv',
 'pypi_wheel_provenance':['issue162-rpds-pypi-py312-metadata.json','issue162-rpds-pypi-metadata.json'],
 'matrix':matrix,'compatible_simulation_total_printed_checks':2299,'compatible_simulation_unexplained_failures':0,
 'focused':{'py312':{'tests':26,'exit':0,'log':'issue162-continuation-native-test_custody_identity.py.log'},'py314':{'tests':26,'exit':0,'log':'issue162-continuation-focused-py314.log'},'mode':'mixed actual filesystem witnesses and explicitly injected error/compatible measurement cases; not native compatible-platform qualification'},
 'parity':{'py312':'8 fields x 33 cases + compound control PASS','py314':'8 fields x 33 cases + compound control PASS'},
 'remaining_native_failures':{'total_legacy_cases':275,'failed':208,'direct_refusals':188,'captured_cli_refusal_cascades':20,'exact_case_list':'issue162-remaining-native-failures.json','full_traces':'issue162-native-case-diagnosis.json','cascade_evidence':'issue162-native-cascade-diagnosis.json','classification':'accepted conservative refusal on this aliasing Mac, NOT green native legacy suites'},
 'production_defect_corrected':{'case':'PASS receipt-parent collection leaked real symlink-loop RuntimeError on Python3.12','red_log':'issue162-pass-resolution-red.log','result':'typed AcceptanceRefused UNKNOWN; no success fallback, checkpoint/verdict mutation, or weakened safety'},
 'independent_review':{'reviewer':'candidate_review','outcome':'No material defect or expectation weakening in continuation; independently ran26 focused defaultMac tests; assertion AST inspection','scope_limit':'did not independently certify Python3.12/dependency env or final full legacy matrix; those executed by sole writer'},
 'local_checks':{'compile':'PASS Python3.12','git_diff_check':'PASS','source_assertion_preservation':'273 existing case check ASTs unchanged; two approved mkdir tests replaced; prior manual added test lines preserved'},
 'remaining_gates':['Native compatible-filesystem / Linux / NTFS / per-directory-mode qualification absent','Hosted CI not run; local workflow focused test step covers Ubuntu only','Integration, commit, push, PR, merge, release and deployment remain held; prior edits retain separate authority boundary'],
 'actions':{'one_writer':True,'source_safety_weakened':False,'system_defaults_changed':False,'remote_environment_acquired':False,'external_source_writes':False,'commit_push_pr_merge_release_deploy':False,'gui':False,'only_external_downloads':'official PyPI pinned test dependencies/metadata in approved isolated env'},
 'security_scan':'No coverage claimed; previous external-egress denial respected without retry'
}
(out/'issue162-continuation-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'delta_sha256':receipt['implementation_delta']['sha256'],'combined_sha256':receipt['combined_inspection_patch']['sha256'],'simulated_compatible_checks':2299,'focused_tests':26,'native_failures_classified':208,'replay':'PASS','state':receipt['state']},indent=2))
