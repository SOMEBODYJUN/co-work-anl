"""Max-cardinality root-deviation branch with one genuine four-tail deviation.
A is largest, ABCDE is its true forced-root outcome, A E Q R S is genuine
second-player deviation to E. No on-path root optimality at A is assumed.
"""
from itertools import product
from scipy.optimize import linprog
import numpy as np,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
vs=[v+(o,) for v in product(range(2),repeat=8) for o in range(2) if any(v) or o]
N=len(vs)
def row(fn):return np.array([fn(v) for v in vs],float)
def payoff(a,path):return row(lambda v:v[a]/sum(v[t] for t in path) if v[a] else 0)
def floor(a,prefix,remain):return row(lambda v:v[a]/(sum(v[t] for t in prefix)+remain))
actual=(0,1,2,3,4);branch=(0,4,5,6,7)
us=[payoff(i,actual) for i in actual];zs=[payoff(i,branch) for i in branch]
rows=[];rhs=[];names=[]
def add(r,b,n):rows.append(r);rhs.append(b);names.append(n)
for a in range(1,8):add(row(lambda v:v[a]),1,'size_'+str(a))
add(row(lambda v:v[8]),5,'opt_total_size')
add(zs[1]-us[1],0,'genuine_B_to_E')
for path,U,start in [(actual,us,1),(branch,zs,2)]:
 for i in range(start,5):
  for a in range(8):add(floor(a,path[:i],5-i)-U[i],0,'floor_'+str(path)+'_'+str(i)+'_'+str(a))
  add(row(lambda v:v[8]/(sum(v[t] for t in path[:i])+5-i))-5*U[i],0,'opt_floor_'+str(path)+'_'+str(i))
# Four-tail certificate for the five four-subtuples of optimum, weakened by
# projecting every customer's optimal multiplicity to its union bit.
from importlib.util import spec_from_file_location,module_from_spec
s=spec_from_file_location('rho',HERE.parent/'induction/audit_root_share_interface.py');m=module_from_spec(s);s.loader.exec_module(m)
def four(v):
 a=v[0];n=sum(v[1:5]);r=m.rho(a,v[1:5],v[5:8])
 f=(4/(a+1) if v[8] else 0)
 return f+5*float(r)-5*float(m.F(1499,750))*(n/(a+n) if n else 0)
add(row(four),0,'paid_four_tail')
opt=row(lambda v:v[8]);eq=row(lambda v:v[0]);out=[]
for t in [.2,.202,.205,.21,.215,.22,.225,.23,.24,.25,.26,.28,.3,.35,.4,.5,.6,.75]:
 r=linprog(-opt,A_ub=np.array(rows+[us[0]]),b_ub=np.array(rhs+[t]),A_eq=[eq],b_eq=[1],bounds=(0,None),method='highs')
 if r.success:
  e={'t':t,'O':-r.fun,'dual':[(names+['root_threshold'])[i]+':'+str(x) for i,x in enumerate(r.ineqlin.marginals) if abs(x)>1e-8],'eq':r.eqlin.marginals.tolist(),'support':[(vs[i],r.x[i]) for i in range(N) if r.x[i]>1e-8]};out.append(e)
  print({k:v for k,v in e.items() if k not in ('support','dual','eq')},flush=True)
 else: print(t,r.message)
(HERE/'max_topic_credible_lp.json').write_text(json.dumps(out,indent=2)+'\n')
