"""Two exact diagnostics of old prose; definition-only source import, main not run."""
from pathlib import Path
import importlib.util,sys,json,hashlib
from fractions import Fraction

base=Path(__file__).resolve().parent
source=base/'original/e8b6428338f9c956317c.py'
spec=importlib.util.spec_from_file_location('bj_home_definitions_only',source)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=[]
for name,k,edges in [
 ('prune-excess-root-children',(1,0,0),((0,1),(0,2))),
 ('include-nonroot-incoming-unit',(1,2,0),((0,1),(1,2))),
]:
 token=module.build_token(3,edges,k,0)
 sigma=module.schedule_tree(token,edges)
 loads=token.instance.loads(sigma)
 assert len(token.instance.unit_options)==1 if hasattr(token.instance,'unit_options') else len(sigma)-token.instance.nj==1
 rows={'name':name,'demand':k,'given_tree':edges,'tree_score':str(module.tree_score(token,edges)),'actual_schedule':sigma,'actual_loads':list(map(str,loads)),'root_unit_jobs_total':len(sigma)-token.instance.nj,'child_jobs':[list(x) for x in token.child_jobs]}
 if name.startswith('prune'):
  assert loads[0]==1 and sum(sigma[j]!=token.instance.home[j] for j in range(token.instance.nj))==1
  rows['old_unpruned_root_formula']='2-2/1=0';rows['correct_kept_root_formula']='2-1/1=1'
 else:
  assert loads[1]==Fraction(3,2)
  rows['nonroot_home_mass']='1/2';rows['nonroot_incoming_unit']='1';rows['full_nonroot_load']='3/2'
 cases.append(rows)
result={'status':'passed','arithmetic':'exact Fraction','original_entry_runs':0,'definition_only_imports':1,'diagnostic_runs':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':cases}
print(json.dumps(result,ensure_ascii=False,indent=2))
