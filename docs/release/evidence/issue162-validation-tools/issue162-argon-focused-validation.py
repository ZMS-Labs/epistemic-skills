"""Focused baseline evidence, not an implementation of the proposed safeguard."""
from pathlib import Path
import sys,tempfile,os,json,io,contextlib
from unittest.mock import patch
root=Path('qualified-candidate/plugins/epistemic-skills/contracts/mission-custody').resolve();sys.path.insert(0,str(root));import test_custody_mission as t
from custody_mission import CustodyError
result={'subject':'6f31811a173967568513d5deec316199c2df7669','python':sys.version.split()[0],'platform':sys.platform,'native_pairs':[],'existing_source_tests':[]}
with tempfile.TemporaryDirectory(prefix='identity-pair-')as td:
 ws=Path(td)
 for index,(left,right) in enumerate([('Case.txt','case.txt'),('straße.txt','strasse.txt'),('é.txt','e\u0301.txt'),('ordinary-a.txt','ordinary-b.txt')]):
  folder=ws/str(index);folder.mkdir();a=folder/left;b=folder/right;a.write_text('sentinel');exists=b.exists();same=exists and os.path.samefile(a,b)
  result['native_pairs'].append({'left':left,'right':right,'aliases_on_this_host':same,'lexical_comparator_equal':t._same_artifact(left,right)})
for fn in (t.test_containment_is_validated_before_acknowledgements_commit,t.test_failed_effect_removes_the_directories_it_created):
 checks=[]
 with tempfile.TemporaryDirectory(prefix='identity-source-regression-')as td,patch.object(t,'check',lambda n,v:checks.append((n,bool(v)))),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):fn(Path(td))
 assert all(v for n,v in checks)
 result['existing_source_tests'].append({'test':fn.__name__,'checks':len(checks),'failures':[]})
with tempfile.TemporaryDirectory(prefix='identity-late-refusal-')as td:
 ws=Path(td);m=t.open_mission(ws,'m-late','Synthetic late refusal');m.approve();junk=ws/'missions/.junk/checkpoints';junk.mkdir(parents=True);(junk/'r00000001.json').write_text('{invalid');cps=ws/'missions/m-late/checkpoints';before=len(list(cps.glob('*.json')))
 def refuse(*args,**kwargs):raise CustodyError('injected final-write-seam refusal')
 with patch.object(m,'_write_effect',refuse),contextlib.redirect_stderr(io.StringIO()):
  try:m.record_effect('artifact.txt','payload','req-late',acknowledge_unreadable=['.junk']);raise AssertionError('not refused')
  except CustodyError as e:assert 'injected final-write-seam' in str(e)
 after=len(list(cps.glob('*.json')));latest=m.status();result['late_refusal']={'checkpoint_count_before':before,'checkpoint_count_after':after,'artifact_exists':(ws/'artifact.txt').exists(),'receipt_count':len(list((ws/'missions/m-late/receipts').glob('*.json'))),'acknowledgement_retained':any('unreadable-acknowledged: .junk'in n for n in latest['state']['notes'])};assert after==before+1 and not result['late_refusal']['artifact_exists'] and result['late_refusal']['receipt_count']==0 and result['late_refusal']['acknowledgement_retained']
result['limits']='Native observations are this Mac only. Existing tests/fault injection verify current ordering/cleanup behavior, not future identity-probe cleanup, read-only allow semantics, or a production fix.'
print(json.dumps(result,indent=2,ensure_ascii=True))
