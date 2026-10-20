from pathlib import Path
import ast,json,hashlib
root=Path('plugins/epistemic-skills/contracts/mission-custody');before=Path('../validation/issue162-before-compat')
exceptions={'test_failed_effect_removes_the_directories_it_created','test_failed_mkdir_removes_the_ancestors_it_already_created'}
rows=[]
for file in ('test_custody_mission.py','test_custody_gate.py','test_es173_cases.py','test_custody_cli.py','test_custody_process_proof.py'):
 old=ast.parse((before/file).read_text());new=ast.parse((root/file).read_text());fns={n.name:n for n in new.body if isinstance(n,ast.FunctionDef)}
 count=0
 for fn in old.body:
  if not isinstance(fn,ast.FunctionDef) or not fn.name.startswith('test_') or fn.name in exceptions:continue
  assert fn.name in fns
  checks=lambda node:[ast.dump(n,include_attributes=False) for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check']
  assert checks(fn)==checks(fns[fn.name]), (file,fn.name,'assertion changed')
  count+=1
 rows.append({'file':file,'cases_with_identical_assertion_AST':count})
assert (root/'test_custody_gate.py').read_bytes()==(before/'test_custody_gate.py').read_bytes()
# Retain every nonblank line added by the earlier manual test patch. Only
# later explicit fixture preparation and two superseded tests were changed.
old=Path('../validation/macos-custody-followup.patch').read_text();parts=old.split('diff --git ')[1:]
for name in ('test_custody_gate.py','test_custody_mission.py'):
 part=next(p for p in parts if p.splitlines()[0].endswith('/'+name))
 current=(root/name).read_text().splitlines()
 additions=[line[1:] for line in part.splitlines() if line.startswith('+') and not line.startswith('+++') and line[1:].strip()]
 assert all(line in current for line in additions),(name,'prior manual added line lost')
result={'assertion_AST_preservation':rows,'approved_replacements':sorted(exceptions),'prior_manual_test_added_lines_preserved':True,'gate_file_unchanged_from_before_compat':True}
Path('../validation/issue162-fixture-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
