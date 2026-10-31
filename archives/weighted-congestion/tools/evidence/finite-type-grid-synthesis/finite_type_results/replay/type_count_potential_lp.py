"""Deterministic finite-type approximate-potential synthesis.
No random seed is used. scipy HiGHS solves the explicit marginal-envelope LP.
For each resource with c(x)=x**degree, weights in {1, q}, populations
n1,nq, solve min alpha subject to:
 w*c(load+w) <= F(k+1,l)-F(k,l) <= alpha*w*c(load+w),
and the analogous heavy-player edge. This is a sufficient alpha-potential
certificate for every strategy system with those populations. It is NOT a
lower bound on the equilibrium existence threshold of the games themselves.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def solve(n1,nq,q,degree):
 states=list(product(range(n1+1),range(nq+1)))
 ix={s:i for i,s in enumerate(states)}; alpha=len(states); n=alpha+1
 A=[]; b=[]; edges=[]
 for k,l in states:
  for dk,dl,w in [(1,0,1),(0,1,q)]:
   if k+dk>n1 or l+dl>nq: continue
   u=ix[(k,l)];v=ix[(k+dk,l+dl)]; cost=w*(k+q*l+w)**degree
   row=np.zeros(n); row[u]=1;row[v]=-1;A.append(row);b.append(-cost)
   row=np.zeros(n);row[v]=1;row[u]=-1;row[alpha]=-cost;A.append(row);b.append(0)
   edges.append((u,v,cost))
 objective=np.zeros(n);objective[alpha]=1
 bounds=[(None,None)]*n;bounds[0]=(0,0);bounds[alpha]=(1,None)
 r=linprog(objective,A_ub=np.array(A),b_ub=np.array(b),bounds=bounds,method='highs')
 if not r.success: return {'error':r.message}
 ratios=[(r.x[v]-r.x[u])/c for u,v,c in edges]
 return dict(n1=n1,nq=nq,q=q,degree=degree,alpha=r.x[-1],rational=str(Fraction(r.x[-1]).limit_denominator(1000000)),min_marginal_ratio=min(ratios),max_marginal_ratio=max(ratios),max_constraint_violation=float(max(np.array(A)@r.x-np.array(b))),variables=n,constraints=len(b))

if __name__=='__main__':
 cases=[(n,n,q,d) for q in [1.01,1.1,1.5,2,3,10] for d in [2,3] for n in [1,2,5,10,20]]
 out=[solve(*x) for x in cases]
 Path(__file__).with_name('type_count_results.json').write_text(json.dumps(out,indent=2))
 for z in out:
  if z['q']==2 or z['n1']==20:print(z)
