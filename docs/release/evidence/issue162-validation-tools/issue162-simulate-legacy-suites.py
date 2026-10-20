from pathlib import Path
import json,re,subprocess,sys
root=Path('plugins/epistemic-skills/contracts/mission-custody')
out=Path('../validation')
results=[]
for name in ('test_custody_mission.py','test_custody_cli.py','test_custody_gate.py','test_es173_cases.py','test_custody_hook.py','test_custody_process_proof.py'):
 p=subprocess.run([sys.executable,str(out/'issue162-run-compatible-simulation.py'),str(root),name],capture_output=True,text=True)
 log=p.stdout+p.stderr
 (out/('issue162-compatible-simulation-'+name+'.log')).write_text(log)
 failures=[line for line in log.splitlines() if line.startswith(('FAIL ','FAILED ','custody_mission.CustodyError','FileNotFoundError','AssertionError'))]
 results.append({'suite':name,'mode':'SIMULATION of compatible measurement only; real managed gates and parent restriction', 'exit':p.returncode,'printed_ok_checks':len(re.findall(r'^ok\s',log,re.M)),'failure_evidence':failures[-15:]})
(out/'issue162-compatible-simulation-suite-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
