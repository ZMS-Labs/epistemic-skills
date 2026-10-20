from pathlib import Path
import subprocess,hashlib,json,sys,tempfile,re,platform
root=Path.cwd();out=root.parent/'validation'
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
tracked=['.github/workflows/mission-custody-contract.yml','plugins/epistemic-skills/contracts/mission-custody/README.md','plugins/epistemic-skills/contracts/mission-custody/custody_mission.py','plugins/epistemic-skills/contracts/mission-custody/probe_case_insensitivity.py']
added=['plugins/epistemic-skills/contracts/mission-custody/custody_identity.py','plugins/epistemic-skills/contracts/mission-custody/test_custody_identity.py','docs/release/evidence/2026-10-20-issue162-local-safeguard.md']
patch=subprocess.check_output(['git','diff','--binary','--',*tracked])
for name in added:
 p=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],capture_output=True)
 assert p.returncode==1 and not p.stderr
 patch+=p.stdout
patchfile=out/'issue162-local-safeguard.patch';patchfile.write_bytes(patch)
old=(out/'macos-custody-followup.patch').read_bytes()
oldhash=hashlib.sha256(old).hexdigest();assert oldhash=='d2712bee7e0bd5e4dab1b06992873630be4ee37624c13170cea0f680fd21d821'
priornames=['plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py','plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py']
oldparts=[]
for part in old.split(b'diff --git ')[1:]:
 if any((' b/'+name+'\n').encode() in part.splitlines(keepends=True)[0] for name in priornames):oldparts.append(b'diff --git '+part)
assert b''.join(oldparts)==subprocess.check_output(['git','diff','--binary','--',*priornames])
# Confirm the separate additive patch can apply to its declared release base.
with tempfile.TemporaryDirectory(prefix='identity-patch-check-',dir=out) as td:
 for name in tracked:
  target=Path(td,name);target.parent.mkdir(parents=True,exist_ok=True)
  target.write_bytes(subprocess.check_output(['git','show',base+':'+name]))
 p=subprocess.run(['git','apply','--check',str(patchfile)],cwd=td,capture_output=True,text=True)
 assert p.returncode==0,p.stderr
schemas=[]
for path in sorted((root/'plugins/epistemic-skills/contracts/mission-custody').glob('*.schema.json')):
 rel=str(path.relative_to(root)); data=path.read_bytes()
 assert data==subprocess.check_output(['git','show',base+':'+rel])
 schemas.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'unchanged_from_base':True})
focus=(out/'issue162-native-test_custody_identity.py.log').read_text()
assert 'Ran 25 tests' in focus and '\nOK\n' in focus and 'skipped=' not in focus
native=json.loads((out/'issue162-native-suite-results.json').read_text())
sim=json.loads((out/'issue162-compatible-simulation-suite-results.json').read_text())
receipt={
 'recorded_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
 'repository':'https://github.com/ZMS-Labs/epistemic-skills','worktree':str(root),
 'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
 'base':base,'state':'LOCAL UNCOMMITTED CANDIDATE; NOT INTEGRATION READY; issue162 open',
 'implementation_patch':patchfile.name,'implementation_patch_sha256':hashlib.sha256(patch).hexdigest(),
 'implementation_files':[{'path':name,'sha256':hashlib.sha256((root/name).read_bytes()).hexdigest()} for name in tracked+added],
 'prior_test_patch':{'sha256':oldhash,'original_test_edits_preserved_byte_for_byte':True,'separate_integration_authority_required':True},
 'environment':{'system':platform.system(),'machine':platform.machine(),'python':platform.python_version(),'native_compatible_filesystem_qualified':False},
 'red_evidence':['issue162-red.log','issue162-sibling-red.log','issue162-discovery-red.log','issue162-diagnostic-red.log','issue162-resolution-red.log'],
 'focused':{'command':'python3 plugins/epistemic-skills/contracts/mission-custody/test_custody_identity.py','tests':25,'failures':0,'skips':0,'native_log':'issue162-native-test_custody_identity.py.log','latest_log':'issue162-focused.log','simulations_explicitly_labeled':True},
 'native_probe':{'log':'issue162-native-probe.log','filesystem_folds_case':True,'comparator_folds_case':False,'managed_operation':'SAFEGUARD REFUSED','issue_closed':False},
 'native_full_suite_attempt':native,'compatible_measurement_simulation':sim,
 'parity_blocker':'test_mission_custody_jsonschema.py: ERROR: jsonschema is required for the Draft 2020-12 parity oracle; no install attempted',
 'schemas':schemas,'compile':'PASS: custody_identity.py, custody_mission.py, probe_case_insensitivity.py, test_custody_identity.py',
 'whitespace':'git diff --check PASS','patch_applies_to_declared_base':'git apply --check PASS',
 'independent_review':{'reviewer':'candidate_review','final_tests_independently_rerun':25,'outcome':'No remaining material findings in bounded safeguard','material_finding_fixed':'Sibling pending state previously did not block other missions; fixed workspace union and explicit-stat UNKNOWN discovery with red/green tests'},
 'remaining_integration_gates':['Compatibility-aware legacy fixture/expectation adaptation; full legacy suite is NOT green','JSON Schema parity in approved dependency environment','Python3.12/native compatible-platform and hosted CI validation; simulations do not qualify Linux/NTFS','Separate integration/push/PR authorization; no publication authority','Prior test-only patch remains separately preserved, not integrated'],
 'actions':{'local_source_implementation':True,'dependencies_installed':False,'external_writes':False,'push_pr_merge_release_deploy':False,'gui':False,'automatic_orphan_recovery_deletion_adoption':False},
 'security_scan':'No coverage claimed; earlier external-egress denial respected; no retry',
}
(out/'issue162-local-implementation-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'patch_sha256':receipt['implementation_patch_sha256'],'focused_tests':25,'prior_edits_preserved':True,'schemas_unchanged':len(schemas),'patch_apply_check':'PASS','state':receipt['state']},indent=2))
