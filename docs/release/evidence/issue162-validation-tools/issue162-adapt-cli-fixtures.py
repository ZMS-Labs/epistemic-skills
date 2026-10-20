from pathlib import Path
import ast,json
root=Path('plugins/epistemic-skills/contracts/mission-custody')
rows=json.load(open('../validation/issue162-legacy-case-diagnosis.json'))
for name in ('test_custody_cli','test_custody_process_proof'):
 path=root/(name+'.py');source=path.read_text();tree=ast.parse(source);edits={}
 failing={r['case'] for r in rows if r['module']==name and (r['error'] or r['failed_checks'])}
 for fn in tree.body:
  if not isinstance(fn,ast.FunctionDef) or fn.name not in failing:continue
  for call in ast.walk(fn):
   if not isinstance(call,ast.Call) or not isinstance(call.func,ast.Name) or call.func.id!='run' or not call.args:continue
   if not isinstance(call.args[0],ast.Constant) or call.args[0].value!='effect':continue
   flags={v.value:i for i,v in enumerate(call.args) if isinstance(v,ast.Constant) and isinstance(v.value,str)}
   assert '--workspace' in flags and '--path' in flags
   workspace=call.args[flags['--workspace']+1];assert isinstance(workspace,ast.Call) and len(workspace.args)==1
   ws=ast.get_source_segment(source,workspace.args[0]);rel=ast.get_source_segment(source,call.args[flags['--path']+1])
   stmt=min((n for n in ast.walk(fn) if isinstance(n,ast.stmt) and n.lineno<=call.lineno and n.end_lineno>=call.end_lineno),key=lambda n:n.end_lineno-n.lineno)
   edits[stmt.lineno]=f'({ws} / ({rel}).replace("\\\\", "/")).parent.mkdir(parents=True, exist_ok=True)  # Explicit #162 fixture parent.\n'
 lines=source.splitlines(keepends=True)
 for line,text in sorted(edits.items(),reverse=True):
  indent=lines[line-1][:len(lines[line-1])-len(lines[line-1].lstrip())];lines.insert(line-1,indent+text)
 path.write_text(''.join(lines));print(name,len(edits),'observed-success fixture sites')
