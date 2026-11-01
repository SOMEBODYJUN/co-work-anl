"""Discover whether on-path decorrelated budget can fail at a true optimal p.
Fixed-policy, fixed-p, fixed-dual-Q cone LP; no aggregate conclusion is assumed.
"""
from pathlib import Path
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
basepath=Path(__file__).with_name('first_pair_iid_attack.py')
spec=importlib.util.spec_from_file_location('base',basepath);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
z=b.z;M=b.M;k=b.k;d=b.d;G=b.G;U=b.U
C=np.zeros(d)
for i in range(b.n):
 for a in range(k):
  end=b.terminal(z[:i]+(a,));B=end[:i]+end[i+1:]
  C+=b.p[a]*(b.p@M)/(1+sum(M[t] for t in B))
c=(sum(M[a] for a in z)>0).astype(float)
A=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-b.beta,np.ones(len(b.beta))],np.c_[b.cap,-np.ones(k)]])
res=linprog(np.r_[c-C,0.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[c,0.]],b_eq=[1],bounds=[(0,None)]*d+[(None,None)],method='highs')
rec={'scope':'Floating discovery; original34 policy,p,Q constrained saddle','status':res.status,'message':res.message}
if res.success:rec.update(violation_CminusW=float(-res.fun),weights={str(j+1):float(w) for j,w in enumerate(res.x[:-1]) if w>1e-8},security=float(res.x[-1]))
Path(__file__).with_name('optimal_p_budget_numerical.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
