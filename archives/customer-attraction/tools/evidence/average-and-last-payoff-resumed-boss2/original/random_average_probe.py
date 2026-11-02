"""Floating stress test for all-history averaging against a fixed comparison portfolio."""
import itertools,json,random,sys,importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py');mod=importlib.util.module_from_spec(spec);sys.modules['lp']=mod;spec.loader.exec_module(mod)
rng=random.Random(10324);best=0;winner=None
for p,n,N in [(3,3,200),(4,3,200),(4,4,200),(5,5,80),(6,3,100),(6,5,30)]:
 J=tuple(range(min(p,n)));obj=np.asarray(mod.coverage_row(p,J),float)
 for ci in range(N):
  actions={h:rng.randrange(p) for k in range(n) for h in itertools.product(range(p),repeat=k)}
  C=mod.StrategyCone(p,n,actions);rows=[]
  for h,act in C.actions.items():
   u=np.asarray(mod.payoff_row(p,C.terminals[h],act),float)
   rows.append(u-sum((np.asarray(mod.payoff_row(p,C.terminals[h+(a,)],a),float) for a in J))/len(J))
  res=linprog(-obj,A_ub=-np.asarray(rows),b_ub=np.zeros(len(rows)),A_eq=[np.asarray(C.welfare,float)],b_eq=[1],bounds=(0,None),method='highs')
  val=-res.fun if res.success else float('inf')
  if val>best+1e-8:
   best=val;print(p,n,ci,val,flush=True)
  if val>2.000001:
   winner={'topics':p,'players':n,'index':ci,'J':J,'value':val,'point':res.x.tolist() if res.success else None,'actions':[{'history':h,'action':a}for h,a in actions.items()]}
   break
 if winner:break
Path(__file__).with_name('random_average_probe.json').write_text(json.dumps({'best':best,'counterexample_to_template':winner},indent=2))
