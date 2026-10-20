from pathlib import Path
import subprocess,sys,json,re
root=Path('plugins/epistemic-skills/contracts/mission-custody')
out=Path('../validation')
results=[]
for name in ('test_mission_custody_jsonschema.py','test_mission_custody.py','test_custody_store.py','test_custody_mission.py','test_custody_cli.py','test_custody_gate.py','test_es173_cases.py','test_custody_hook.py','test_custody_process_proof.py','test_custody_identity.py'):
 p=subprocess.run([sys.executable,str(root/name)],capture_output=True,text=True)
 log=p.stdout+p.stderr
 (out/('issue162-native-'+name+'.log')).write_text(log)
 failures=[line for line in log.splitlines() if line.startswith('FAIL ') or line.startswith('FAILED ') or line.startswith('ModuleNotFoundError') or line.startswith('custody_mission.CustodyError') or line.startswith('AssertionError') or line.startswith('FileNotFoundError')]
 results.append({'suite':name,'mode':'actual Mac Python '+sys.version.split()[0], 'exit':p.returncode,'printed_ok_checks':len(re.findall(r'^ok\s',log,re.M)),'failure_evidence':failures[-12:]})
print(json.dumps(results,indent=2))
(out/'issue162-native-suite-results.json').write_text(json.dumps(results,indent=2)+'\n')
