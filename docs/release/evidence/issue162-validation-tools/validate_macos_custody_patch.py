"""External validation only: simulations are not native Linux/NTFS evidence."""
import ast,contextlib,copy,importlib.util,inspect,io,json,pathlib,subprocess,sys,tempfile,textwrap
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve();base='6f31811a173967568513d5deec316199c2df7669';rel='plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py';contract=root/pathlib.Path(rel).parent;sys.path.insert(0,str(contract));import test_custody_mission as t
from custody_mission import _normalize_relpath
fixed=(root/rel).read_text();original=subprocess.check_output(['git','show',f'{base}:{rel}'],cwd=root,text=True)
def checks(source):
 fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='test_distinct_files_never_share_an_obligation')
 return sorted([n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check'],key=lambda n:(n.lineno,n.col_offset))
class NormalizeFixture(ast.NodeTransformer):
 def visit_Name(self,node):
  return ast.copy_location(ast.Constant({'real_name':'straße.txt','decoy_name':'strasse.txt'}[node.id]),node) if node.id in ('real_name','decoy_name') else node
 def visit_JoinedStr(self,node):
  node=self.generic_visit(node);parts=[]
  for v in node.values:
   if isinstance(v,ast.Constant) and isinstance(v.value,str):parts.append(v.value)
   elif isinstance(v,ast.FormattedValue) and isinstance(v.value,ast.Constant) and isinstance(v.value.value,str):parts.append(v.value.value)
   else:return node
  return ast.copy_location(ast.Constant(''.join(parts)),node)
a=checks(original);b=checks(fixed);assert len(a)==len(b)
assert [ast.dump(x,include_attributes=False)for x in a]==[ast.dump(NormalizeFixture().visit(copy.deepcopy(x)),include_attributes=False)for x in b]
results={'source_assertions':{'static_check_calls':len(a),'baseline_and_fixed_conditions_identical_after_fixture_name_normalization':True},'probe_simulation':[],'actual_mac_runs':[]}
probe=textwrap.dedent(fixed[fixed.index('    real_name, decoy_name = "straße.txt"',fixed.index('def test_distinct_files_never_share_an_obligation')):fixed.index('    # end to end: covering a different file',fixed.index('def test_distinct_files_never_share_an_obligation'))])
for aliases,permission in [(False,False),(True,False),(False,True)]:
 fs={};opens=[]
 def key(s):return s.replace('straße.txt','strasse.txt') if aliases else s
 class P:
  def __init__(self,value):self.value=str(value)
  def __truediv__(self,child):return P(self.value+'/'+child)
  def write_text(self,value,**kw):fs[key(self.value)]=value
  def open(self,mode,**kw):
   opens.append(mode)
   if permission:raise PermissionError('simulated access failure')
   assert mode=='x'
   if key(self.value) in fs:raise FileExistsError(self.value)
   fs[key(self.value)]=''
   class H:
    def __enter__(h):return h
    def __exit__(h,*args):pass
    def write(h,value):fs[key(self.value)]=value
   return H()
 class T:
  @staticmethod
  @contextlib.contextmanager
  def TemporaryDirectory(**kw):yield 'probe'
 ns={'workspace':'workspace','tempfile':T,'Path':P};stream=io.StringIO();raised=False
 with contextlib.redirect_stdout(stream):
  try:exec(compile(probe,'<actual-source-probe-simulation>','exec'),ns)
  except PermissionError:raised=True
 if permission:assert raised and 'LIMITED' not in stream.getvalue()
 else:
  assert not raised and opens==['x'];assert fs[key('probe/straße.txt')]=='sentinel'
  assert (ns['real_name'],ns['decoy_name'])==(('custody-real.txt','custody-decoy.txt')if aliases else('straße.txt','strasse.txt'))
  assert ('LIMITED es#162' in stream.getvalue())==aliases
 results['probe_simulation'].append({'aliasing':aliases,'permission_error':permission,'exclusive_create_modes':opens,'outcome':'PermissionError propagated'if permission else 'fallback names and visible LIMIT'if aliases else 'original Unicode names retained','sentinel_unchanged':fs[key('probe/straße.txt')]=='sentinel'})
original_open=t.open_mission
for mutant in ('none','write-decoy-to-real','suppress-tamper-drift','overfold-unicode-comparator'):
 observed=[];stream=io.StringIO()
 def record(label,condition):observed.append((label,bool(condition)))
 def opener(*args,**kw):
  m=original_open(*args,**kw);effect=m.record_effect;resume=m.resume
  def altered_effect(name,content,rid):
   if mutant=='write-decoy-to-real' and rid=='id-decoy':name='custody-real.txt'
   return effect(name,content,rid)
  def altered_resume(*args,**kw):
   if mutant=='suppress-tamper-drift' and any(p.name=='custody-decoy.txt' and p.read_text()=='tampered'for p in args_workspace.iterdir() if p.is_file()):return []
   return resume(*args,**kw)
  m.record_effect=altered_effect;m.resume=altered_resume;return m
 with tempfile.TemporaryDirectory(prefix='custody-assertion-check-') as td:
  args_workspace=pathlib.Path(td)
  with patch.object(t,'check',record),patch.object(t,'open_mission',opener),contextlib.redirect_stdout(stream):
   if mutant=='overfold-unicode-comparator':
    with patch.object(t,'_same_artifact',lambda left,right:_normalize_relpath(left).casefold()==_normalize_relpath(right).casefold()):t.test_distinct_files_never_share_an_obligation(args_workspace)
   else:t.test_distinct_files_never_share_an_obligation(args_workspace)
 failed=[label for label,passed in observed if not passed];assert len(observed)==18
 if mutant=='none':assert not failed and 'LIMITED es#162' in stream.getvalue()
 elif mutant=='write-decoy-to-real':assert 'distinct-decoy-did-not-discharge'in failed and 'distinct-real-file-untouched'in failed
 elif mutant=='suppress-tamper-drift':assert 'distinct-both-files-tracked-separately'in failed
 else:assert 'eszett-not-same-artifact'in failed and 'kelvin-not-same-artifact'in failed
 results['actual_mac_runs'].append({'mutant':mutant,'checks_executed':len(observed),'failures_detected':failed,'limitation_visible':'LIMITED es#162'in stream.getvalue()})
results['limits']='Probe simulation is in-memory branch coverage, not Linux/NTFS execution. Actual runs exercise this Mac only. Production162 remains unresolved.'
print(json.dumps(results,indent=2))
