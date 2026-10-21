"""Floating discovery only: vary saddle p,Q over the fixed two-group policy cone."""
from pathlib import Path
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
f=Path(__file__).with_name('first_pair_iid_attack.py');sp=importlib.util.spec_from_file_location('b',f);b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
M=b.M;U=b.U;G=b.G;d=b.d;k=b.k;z=b.z;n=b.n;c=(sum(M[a] for a in z)>0).astype(float)
rng=np.random.default_rng(211627);best=-100;report={'scope':'Floating discovery; full fixed policy cone and fixed-saddle steps','trials':0,'max_GB_violation':None,'candidate':None}
for it in range(120):
 obj=rng.normal(size=d)
 out=linprog(obj,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(d)],b_eq=[1],bounds=[(0,None)]*d,method='highs')
 if not out.success:continue
 w=out.x
 mat=U@w
 sec=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 p=sec.x[:-1];Q=-sec.ineqlin.marginals;cap=np.tensordot(Q,U,axes=1);beta=U.transpose(0,2,1)@p
 C=np.zeros(d)
 for i in range(n):
  for a in range(k):
   end=b.terminal(z[:i]+(a,));B=end[:i]+end[i+1:]
   C+=p[a]*(p@M)/(1+sum(M[t] for t in B))
 A=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(len(beta))],np.c_[cap,-np.ones(k)]])
 res=linprog(np.r_[c-C,0],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[c,0]],b_eq=[1],bounds=[(0,None)]*d+[(None,None)],method='highs')
 report['trials']=it+1
 if res.success and -res.fun>best+1e-8:
  best=-res.fun;report.update(max_GB_violation=float(best),incumbent={'iteration':it,'p':p.tolist(),'Q':Q.tolist()})
  print(it,best,flush=True)
 if res.success and -res.fun>1e-7:
  ww=res.x[:-1];act=U@ww;active=np.abs(act@p-res.x[-1])<1e-7
  rank=int(np.linalg.matrix_rank(np.vstack([np.c_[act[active],-np.ones(sum(active))],np.r_[np.ones(k),0]])))
  report['candidate']={'weights':{str(j+1):float(q) for j,q in enumerate(ww) if q>1e-8},'p':p.tolist(),'Q':Q.tolist(),'value':float(res.x[-1]),'rank_active':rank};break
Path(__file__).with_name('optimal_p_budget_walk_numerical.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
