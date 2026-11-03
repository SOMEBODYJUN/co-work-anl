"""Necessary security LP for opt-private X_i plus outside-opt pair insurance.
Bank clients may have arbitrary actual-theme membership and one optimal T_i.
All original actual, optimal and insurance query lower bounds are retained.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import numpy as np,json
from scipy.optimize import linprog

def solve(path):
 n=max(path)+1;m=5;edges=list(combinations(range(5),2));p=n+5+10
 types=[tuple(a for a in range(n) if S>>a&1)+(n+j,) for S in range(1,1<<n) for j in range(5)]
 types += [(n+j,)+tuple(n+5+k for k,e in enumerate(edges) if j in e) for j in range(5)]
 q=[path.count(a) for a in range(p)]
 def row(q,a):return [F(1,sum(q[b] for b in typ)) if a in typ else F(0) for typ in types]
 rows=[];labels=[]
 for i,a in enumerate(path):
  old=[path[:i].count(b) for b in range(p)];actual=row(q,a);r=m-i
  for t in range(p):
   dev=old[:];dev[t]+=r
   rows.append([x-y for x,y in zip(actual,row(dev,t))]);labels.append((i+1,t))
 W=[F(any(a<n for a in typ)) for typ in types];L=[1-v for v in W]
 res=linprog(-np.array(L,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=[np.array(W,float)],b_eq=[1],bounds=(0,None),method='highs');assert res.success
 x=[F(float(t)).limit_denominator(10**7) for t in res.x];beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7);mu=[F(float(-t)).limit_denominator(10**7) for t in res.ineqlin.marginals]
 dot=lambda a,b:sum((v*w for v,w in zip(a,b)),F(0))
 residual=[beta*W[j]-sum(mu[k]*rows[k][j] for k in range(len(rows)))-L[j] for j in range(len(types))]
 return {'path':path,'beta':str(beta),'primal_exact':all(v>=0 for v in x) and dot(W,x)==1 and all(dot(r,x)>=0 for r in rows),'dual_exact':all(v>=0 for v in mu) and all(v>=0 for v in residual),'point':[(types[j],str(v)) for j,v in enumerate(x) if v], 'dual':[(labels[k],str(v)) for k,v in enumerate(mu) if v], 'minimum_residual':str(min(residual))}
if __name__=='__main__':
 reports=[solve(p) for p in [(0,0,1,1,2),(0,1,2,3,4)]]
 Path(__file__).with_suffix('.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
