"""Exact saved-menu arithmetic only, not a new full-DAG/SPE or LP audit."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
B=Path(__file__).resolve().parent
P=B/'related/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_m6_dag.json'
C=B/'original/research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/dual/padded_full_menu_exact.json'
d=json.loads(P.read_text());cert=json.loads(C.read_text());nodes=d['nodes'];N=d['instance']['players'];K=len(d['instance']['topics']);customers=d['instance']['customers']
assert(N,K)==(6,9)
def follow(idx):
 path=[];visited=[]
 while 'action'in nodes[idx]:
  visited.append(idx);node=nodes[idx];a=node['action'];path.append(a);idx=node['children'][a]
 return path,tuple(nodes[idx]['counts']),visited
actual,root_target,root_nodes=follow(d['root']);assert actual==d['expected']['path']
columns=[]
for pos,idx in enumerate(root_nodes):
 for forced in range(K):
  child=nodes[idx]['children'][forced];tail,terminal,used=follow(child)
  assert terminal==tuple(nodes[child]['target'])and sum(terminal)==6
  columns.append({'position':pos+1,'actual_prefix':actual[:pos],'forced_action':forced,'child_index':child,'terminal':terminal,'continuation_indices':used})
menu=sorted({tuple(x['terminal'])for x in columns});assert len(menu)==16
p=list(map(F,cert['p']));assert len(p)==9 and min(p)>=0 and sum(p)==1
Q=[(tuple(x['background']),F(x['probability']))for x in cert['Q']];assert all(z in menu and q>=0 for z,q in Q)and sum(q for z,q in Q)==1
cap=F(cert['cap'])
def value(a,z):
 return sum((F(x['multiplicity'],1+sum(z[b]for b in x['topics']))for x in customers if a in x['topics']),F(0))
primal=[sum((p[a]*value(a,z)for a in range(K)),F(0))for z in menu]
queries=[sum((q*value(a,z)for z,q in Q),F(0))for a in range(K)]
assert primal==list(map(F,cert['all_menu_primal_values']))and queries==list(map(F,cert['query_values']))
assert min(primal)==cap==max(queries)
W=sum(x['multiplicity']for x in customers if any(root_target[a]for a in x['topics']))
result={'scope':'one fixed saved six-player input; all54 first-deviation full-terminal columns read; exact16menu minimax primal/dual arithmetic; no SPE/threshold/LP recomputation','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'menu_certificate_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'actual_path':actual,'root_coverage':W,'column_count':len(columns),'columns':columns,'unique_menu_size':len(menu),'unique_menu_lexicographic':menu,'p':[str(v)for v in p],'Q':[{'background':z,'probability':str(q)}for z,q in Q],'all_menu_primal_values':[str(v)for v in primal],'query_values':[str(v)for v in queries],'min_primal_and_max_dual':str(cap),'W_minus_m_cap':str(F(W)-N*cap),'status':'all source p/Q/menu arithmetic matched; exact fixed-menu saddle cap established','new_arithmetic_checker_runs':1,'original_group_verifier_runs':0,'original_padded_generator_or_DAG_solver_runs':0,'SPE_IC_checks':0}
with(B/'padded-menu-arithmetic.json').open('x')as out:json.dump(result,out,ensure_ascii=False,indent=2);out.write('\n')
print(json.dumps({k:v for k,v in result.items()if k not in ['columns','unique_menu_lexicographic','p','Q','all_menu_primal_values','query_values']},ensure_ascii=False))
