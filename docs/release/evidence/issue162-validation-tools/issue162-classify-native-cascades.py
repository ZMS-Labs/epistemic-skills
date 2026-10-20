from pathlib import Path
import sys,json,importlib,inspect,tempfile,contextlib,io,subprocess
from unittest.mock import patch
root=Path('plugins/epistemic-skills/contracts/mission-custody').resolve();sys.path.insert(0,str(root))
old=json.load(open('../validation/issue162-native-case-diagnosis.json'))
rows=[];original=subprocess.run
for case in old:
 if not case['failed_checks'] or (case['error'] and 'KNOWN_MISMATCH' in case['error']['message']):continue
 m=importlib.import_module(case['module']);fn=getattr(m,case['case']);events=[]
 def spy(*a,**kw):
  p=original(*a,**kw)
  if 'identity safeguard: KNOWN_MISMATCH' in (p.stderr or ''):
   events.append({'command':[str(v) for v in a[0]],'exit':p.returncode,'reason':'identity safeguard: KNOWN_MISMATCH'})
  return p
 error=None
 with tempfile.TemporaryDirectory() as td,contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()),patch.object(subprocess,'run',side_effect=spy):
  try:fn(Path(td)) if len(inspect.signature(fn).parameters) else fn()
  except Exception as exc:error=type(exc).__name__+': '+str(exc)
 rows.append({'module':case['module'],'case':case['case'],'managed_refusal_evidence':events,'later_error':error})
Path('../validation/issue162-native-cascade-diagnosis.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Native assertion-cascade cases:',len(rows),'with direct captured known-mismatch refusal:',sum(bool(r['managed_refusal_evidence']) for r in rows))
for row in rows:
 if not row['managed_refusal_evidence']:print('UNCLASSIFIED:',row['case'])
