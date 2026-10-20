from pathlib import Path
import ast,json
path=Path('plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py');source=path.read_text();tree=ast.parse(source)
# These three tests consist of successful writes followed by scope comparison,
# and have independently observed missing-parent failures at multiple sites.
known={'test_windows_scope_entries_with_spaces_bind_end_to_end','test_scope_consistency_and_acceptance_boundary','test_trailing_slash_scope_entry_binds_the_subtree'}
lines=source.splitlines(keepends=True);edits={}
for fn in tree.body:
 if not isinstance(fn,ast.FunctionDef) or fn.name not in known:continue
 for call in ast.walk(fn):
  if not isinstance(call,ast.Call) or not isinstance(call.func,ast.Attribute) or call.func.attr!='record_effect':continue
  stmt=min((n for n in ast.walk(fn) if isinstance(n,ast.stmt) and n.lineno<=call.lineno and n.end_lineno>=call.end_lineno),key=lambda n:n.end_lineno-n.lineno)
  if '# Explicit #162 fixture parent.' in lines[stmt.lineno-2]:continue
  mission=ast.get_source_segment(source,call.func.value);arg=ast.get_source_segment(source,call.args[0])
  text=f'{mission}._resolve_artifact_path({arg}).parent.mkdir(parents=True, exist_ok=True)  # Explicit #162 fixture parent.\n'
  indent=lines[stmt.lineno-1][:len(lines[stmt.lineno-1])-len(lines[stmt.lineno-1].lstrip())];edits[stmt.lineno]=indent+text
for line,text in sorted(edits.items(),reverse=True):lines.insert(line-1,text)
path.write_text(''.join(lines));print('Additional success-intended parent fixtures:',len(edits))
