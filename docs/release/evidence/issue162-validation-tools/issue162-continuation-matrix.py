from pathlib import Path
import subprocess,sys,json,re,platform
root=Path('plugins/epistemic-skills/contracts/mission-custody');out=Path('../validation');rows=[]
names=('test_mission_custody_jsonschema.py','test_mission_custody.py','test_custody_store.py','test_custody_mission.py','test_custody_cli.py','test_custody_gate.py','test_es173_cases.py','test_custody_hook.py','test_custody_process_proof.py','test_custody_identity.py')
for mode in ('native','compatible-measurement-simulation'):
 for name in names:
  if mode!='native' and name not in ('test_custody_mission.py','test_custody_cli.py','test_custody_gate.py','test_es173_cases.py','test_custody_hook.py','test_custody_process_proof.py'):continue
  command=[sys.executable,str(root/name)] if mode=='native' else [sys.executable,str(out/'issue162-run-compatible-simulation.py'),str(root),name]
  p=subprocess.run(command,capture_output=True,text=True);log=p.stdout+p.stderr;filename=f'issue162-continuation-{mode}-{name}.log';(out/filename).write_text(log)
  failures=[line for line in log.splitlines() if line.startswith(('FAIL ','FAILED ','custody_mission.CustodyError','FileNotFoundError','AssertionError','ERROR:'))]
  tests=re.search(r'Ran (\d+) tests',log)
  row={'suite':name,'mode':mode,'python':platform.python_version(),'exit':p.returncode,'printed_ok_checks':len(re.findall(r'^ok\s',log,re.M)),'unittest_tests':int(tests.group(1)) if tests else None,'log':filename,'failure_evidence':failures,'last_line':log.strip().splitlines()[-1] if log.strip() else ''}
  rows.append(row);print(mode,name,p.returncode,flush=True)
(out/'issue162-continuation-matrix.json').write_text(json.dumps(rows,indent=2)+'\n')
