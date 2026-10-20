"""Read-only source investigation; effects stay in disposable isolated workspaces.
Exit zero means the stated regression observations reproduced, not custody PASS.
"""
from pathlib import Path
import importlib.util,sys,tempfile,os,inspect,json,contextlib,io
source=Path(sys.argv[1]).resolve();contract=source/'plugins/epistemic-skills/contracts/mission-custody';sys.path.insert(0,str(contract))
import test_custody_mission as tests
from custody_mission import Mission,_same_artifact
out={'platform':sys.platform,'python':sys.version.split()[0],'observations':{}}
with tempfile.TemporaryDirectory(prefix='custody-identity-') as tmp:
 root=Path(tmp)
 for name,pair in [('unicode',('straße.txt','strasse.txt')),('ascii',('Case.txt','case.txt')),('control',('real-artifact.txt','decoy-artifact.txt'))]:
  ws=root/name;ws.mkdir();left,right=(ws/n for n in pair);left.write_text('left-sentinel');seen=right.exists();aliases=seen and os.path.samefile(left,right);right.write_text('right-sentinel');out['observations'][name]={'second_exists_before_write':seen,'samefile_before_write':aliases,'left_after_second_write':left.read_text(),'comparison_equal':_same_artifact(*pair)}
 for name,substitute in [('original_fixture',False),('distinct_filename_control',True)]:
  ws=root/name;ws.mkdir();checks=[];ns=dict(vars(tests));ns['check']=lambda label,condition:checks.append({'label':label,'pass':bool(condition)})
  body=inspect.getsource(tests.test_distinct_files_never_share_an_obligation)
  if substitute:body=body.replace('straße.txt','real-artifact.txt').replace('strasse.txt','decoy-artifact.txt')
  exec(compile(body,'<controlled-distinct-file-fixture>','exec'),ns)
  ns['test_distinct_files_never_share_an_obligation'](ws);out[name]={'failures':[x['label']for x in checks if not x['pass']],'checks':len(checks),'variable_changed':'filename pair only' if substitute else 'none'}
 ws=root/'scope';ws.mkdir();m=Mission.open(ws,mission_id='identity-scope',instruction='Synthetic scope identity probe',operator_ref='operator:example',steward_ref='agent:example',required_tier='declared-role-separation',actor='agent:example',scope_out=['secrets.env']);m.approve();m.record_effect('SECRETS.env','synthetic payload','probe-1');out['scope']={'excluded_alias_exists':(ws/'secrets.env').exists(),'findings':m.scope_consistency()}
if out['observations']['unicode']['samefile_before_write']:
 assert out['original_fixture']['failures']==['distinct-real-file-untouched','distinct-both-files-tracked-separately']
assert out['distinct_filename_control']['failures']==[]
print(json.dumps(out,indent=2,ensure_ascii=True))
