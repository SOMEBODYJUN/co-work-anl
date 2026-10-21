"""Finite floating discovery for min-iid-coverage on safety-optimal face, n=2."""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
rng=np.random.default_rng(211626)
report={'scope':'Floating finite search; no universal inference','trials':0,'largest_observed_PminusW':-1e9,'candidate':None}
for it in range(1800):
 k=int(rng.choice([3,4,5,6]));D=(1<<k)-1;M=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)])
 w=rng.integers(1,15,D)*(rng.random(D)<rng.choice([.1,.3,.6,1.]))
 if not w.any():continue
 util=np.array([[(M[a]/(1+M[b]))@w for b in range(k)] for a in range(k)])
 children=[[b for b in range(k) if util[b,a]>=max(util[:,a])-1e-9] for a in range(k)]
 floor=max(min(util[a,b] for b in children[a]) for a in range(k))
 choices=[(a,b) for a in range(k) for b in children[a] if util[a,b]>=floor-1e-9]
 worst=min(sum(w*((M[a]+M[b])>0)) for a,b in choices)
 sec=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-util.T,np.ones(k)],b_ub=np.zeros(k),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 p=sec.x[:-1];v=sec.x[-1]
 ps=[p]
 for t in range(4):
  obj=rng.normal(size=k)
  out=linprog(obj,A_ub=-util.T,b_ub=np.repeat(-v+1e-9,k),A_eq=[np.ones(k)],b_eq=[1],bounds=[(0,None)]*k,method='highs')
  if out.success:ps.append(out.x)
 vals=[float((2*(pp@M)-(pp@M)**2)@w) for pp in ps];best=min(vals);gap=best-worst
 report['trials']=it+1
 if gap>report['largest_observed_PminusW']:
  report['largest_observed_PminusW']=gap
  print(it,'gap',gap,'W',worst,'v',v,flush=True)
 if gap>1e-6:
  report['candidate']={'k':k,'weights':{str(i+1):int(q) for i,q in enumerate(w) if q},'P':best,'W':float(worst),'safety_value':float(v),'p_vertices':list(map(lambda x:x.tolist(),ps))};break
Path(__file__).with_name('two_player_safe_iid_numerical.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
