"""Replay nine selected fixed cones and two small theta helper cases, not random main."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys,itertools,hashlib,time
import numpy as np
BASE=Path(__file__).resolve().parent
ROOT=BASE/'runtime'
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
workspace=ROOT/'research/workspaces/customer-attraction/R-6e3a5707f1f94c1d86bcbc61b4db4345'
union=load('r6e_union_probe',workspace/'independent_attack/union_extension_attack.py')
theta=load('r6e_theta_probe',workspace/'equilibrium_tree/theta_attack.py')
meta=json.loads((BASE/'source-manifest.json').read_text())
old=json.loads((BASE/'original'/next(x['path'] for x in meta if x['id']=='cc4d55390abc43e18b65')).read_text())
new=[]
for record in old:
 t=time.monotonic();r=union.attack(ROOT/record['source']);assert r is not None
 assert r['source']==record['source'] and r['players']==record['players'] and r['topics']==record['topics']
 assert list(r['comparison'])==record['comparison'] and r['exact_ratio']==record['exact_ratio']
 assert abs(r['proposal']-record['proposal'])<1e-10
 new.append({'saved':record,'replayed':r,'seconds':time.monotonic()-t,'float_proposal_bitwise_equal':r['proposal']==record['proposal']})
 print(record['source'].split('/')[-1],r['exact_ratio'],flush=True)
# Check every joining coefficient in explicit small domains using direct fractions.
checked=0
for p in range(1,5):
 for m in range(1,5):
  arr=theta.joining(p,m)
  backgrounds=list(theta.counts(p,m-1))
  assert arr.shape==(len(backgrounds),p,(1<<p)-1)
  for j,b in enumerate(backgrounds):
   for a in range(p):
    for mask in range(1,1<<p):
     q=F(bool(mask&(1<<a)),1+sum(b[t] for t in range(p) if mask&(1<<t)))
     assert abs(arr[j,a,mask-1]-float(q))<1e-15
     checked+=1
from customer_attraction import Instance,CustomerType,ExactSPESolver
from customer_attraction_strategy_lp import StrategyCone
cases=[]
for p,m,x in [(1,2,[1]),(2,3,[1,2,1])]:
 i=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),n) for mask,n in enumerate(x,1) if n),m)
 s=ExactSPESolver(i);target=sorted(s.worst_outcomes())[0]
 cert=s.certificate(target)
 c=StrategyCone(p,m,cert.actions)
 r=theta.optimize(c,np.array(x,dtype=float),theta.joining(p,m))
 assert r is not None
 v,y=r;gaps=c.matrix@y
 assert min(gaps,default=0)>-1e-8 and abs(np.asarray(c.welfare,dtype=float)@y-1)<1e-8
 actual=float(np.min(np.max(theta.joining(p,m)@y,axis=1)))
 assert abs(v-actual)<1e-12
 cases.append({'p':p,'m':m,'input_multiplicities':x,'theta_per_W':v,'W_per_theta':1/v,'float_weights':list(y),'min_float_cone_slack':float(min(gaps,default=0)),'scope':'floating helper check, no exact LP optimum certificate'})
report={'execution_scope':'nine explicit attack(path) calls, two optimize() calls; neither random main executed','union_comparisons':new,'joining_coefficients_checked':checked,'theta_small_cases':cases}
(BASE/'probe-replay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASSED',len(new),'fixed cones,',checked,'joining coefficients,',len(cases),'theta helper cases',flush=True)
