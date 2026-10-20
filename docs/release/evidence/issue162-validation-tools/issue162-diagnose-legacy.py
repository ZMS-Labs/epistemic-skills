"""Independent per-case continuation: compatible witness SIMULATION only."""
from pathlib import Path
import sys, tempfile, contextlib, io, inspect, importlib, json, traceback
from unittest.mock import patch
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root))
import custody_identity as identity
results=[]
for name in ('test_custody_mission','test_custody_gate','test_es173_cases','test_custody_cli','test_custody_process_proof'):
 module=importlib.import_module(name)
 tests=getattr(module,'TESTS',None) or [v for k,v in vars(module).items() if k.startswith('test_') and callable(v)]
 for fn in tests:
  output=io.StringIO();before=len(module.FAILURES);err=None
  try:
   with tempfile.TemporaryDirectory(prefix='identity-legacy-diagnosis-') as td, contextlib.redirect_stdout(output),contextlib.redirect_stderr(output),(contextlib.nullcontext() if '--native' in sys.argv else patch.object(identity,'_measure_pairs',return_value='NO_MISMATCH_OBSERVED')):
    fn(Path(td)) if len(inspect.signature(fn).parameters) else fn()
  except Exception as exc:
   err={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
  checks=module.FAILURES[before:]
  results.append({'module':name,'case':fn.__name__,'error':err,'failed_checks':checks,'log':output.getvalue() if err or checks else None})
out=Path('../validation/issue162-native-case-diagnosis.json' if '--native' in sys.argv else '../validation/issue162-legacy-case-diagnosis.json');out.write_text(json.dumps(results,indent=2)+'\n')
failed=[r for r in results if r['error'] or r['failed_checks']]
print(json.dumps({'cases':len(results),'failed_cases':len(failed),'failures':[{'module':r['module'],'case':r['case'],'error':r['error']['message'] if r['error'] else None,'checks':r['failed_checks']} for r in failed]},indent=2))
