"""Add explicit existing-parent fixtures ONLY at observed escaping failures.
No production gates are patched, and no assertion is removed.
"""
from pathlib import Path
import ast,json,re
root=Path('plugins/epistemic-skills/contracts/mission-custody')
rows=json.load(open('../validation/issue162-legacy-case-diagnosis.json'))
skip={'test_failed_effect_removes_the_directories_it_created','test_failed_mkdir_removes_the_ancestors_it_already_created'}
edits={};notes=[]
for row in rows:
 if not row['error'] or row['case'] in skip:continue
 if 'identity probe failed (FileNotFoundError)' not in row['error']['message']:continue
 frames=re.findall(r'File "[^"]*/(test_\w+\.py)", line (\d+), in (\w+)\n\s+([^\n]+)',row['error']['traceback'])
 name,line,_,_=frames[-1];line=int(line);path=root/name;source=path.read_text();tree=ast.parse(source)
 calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and n.lineno<=line<=n.end_lineno and isinstance(n.func,ast.Attribute) and n.func.attr=='record_effect']
 if not calls:continue
 call=min(calls,key=lambda n:n.end_lineno-n.lineno)
 stmt=min((n for n in ast.walk(tree) if isinstance(n,ast.stmt) and n.lineno<=call.lineno and n.end_lineno>=call.end_lineno),key=lambda n:n.end_lineno-n.lineno)
 mission=ast.get_source_segment(source,call.func.value);argument=ast.get_source_segment(source,call.args[0])
 text=f'{mission}._resolve_artifact_path({argument}).parent.mkdir(parents=True, exist_ok=True)  # Explicit #162 fixture parent.\n'
 edits.setdefault(path,{})[stmt.lineno]=text
 notes.append({'case':row['case'],'file':str(path),'before_line':stmt.lineno,'fixture':text.strip(),'evidence':'observed escaping missing-parent UNKNOWN'})
for path,changes in edits.items():
 lines=path.read_text().splitlines(keepends=True)
 for line,text in sorted(changes.items(),reverse=True):
  original=lines[line-1];indent=original[:len(original)-len(original.lstrip())];lines.insert(line-1,indent+text)
 path.write_text(''.join(lines))
Path('../validation/issue162-fixture-parent-adaptations.json').write_text(json.dumps(notes,indent=2)+'\n')
print('Explicit parent fixtures added at',len(notes),'observed call sites')
