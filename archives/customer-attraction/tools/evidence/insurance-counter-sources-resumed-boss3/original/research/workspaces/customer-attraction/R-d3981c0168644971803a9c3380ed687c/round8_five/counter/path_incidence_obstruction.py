"""Symmetrized optimal-query security relaxation for fixed actual 5-move paths.
Column (actual membership S, optimal membership degree d); all five optimal
queries are summed. Missing columns only have d>=k. Exact primal/dual recovery
is checked, so nonnegative conclusions certify the stated relaxation.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def solve(path,k):
    n=max(path)+1; m=len(path); q=[path.count(a) for a in range(n)]
    types=[(S,d) for S in range(1<<n) for d in range(6) if (S or d>=k) and (S or d)]
    rows=[]
    for i,a in enumerate(path):
        old=[path[:i].count(b) for b in range(n)]; r=m-i
        row=[]
        for S,d in types:
            oldload=sum(old[b] for b in range(n) if S>>b&1)
            load=sum(q[b] for b in range(n) if S>>b&1)
            actual=F(5,load) if S>>a&1 else F(0)
            deviation=F(d,oldload+r)
            row.append(actual-deviation)
        rows.append(row)
    W=[F(bool(S)) for S,d in types]
    V=[F(not S)-F(S!=0 and d==0) for S,d in types]
    res=linprog(-np.array(V,float),A_ub=-np.array(rows,float),b_ub=np.zeros(m),A_eq=[np.array(W,float)],b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return {'path':path,'k':k,'error':res.message}
    x=[F(float(v)).limit_denominator(10**7) for v in res.x]
    beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    mu=[F(float(-v)).limit_denominator(10**7) for v in res.ineqlin.marginals]
    residual=[beta*W[j]-sum(mu[i]*rows[i][j] for i in range(m))-V[j] for j in range(len(types))]
    return {'path':path,'minimum_omitted_degree':k,'status':'path summed security relaxation, not SPE attainability','beta':str(beta),'value':str(dot(V,x)), 'primal_exact':all(v>=0 for v in x) and dot(W,x)==1 and all(dot(r,x)>=0 for r in rows),'dual_exact':all(v>=0 for v in mu) and all(v>=0 for v in residual),'mu':[str(v) for v in mu],'point':[(str(types[j]),str(v)) for j,v in enumerate(x) if v], 'minimum_residual':str(min(residual)), 'types':types, 'residual':[str(v) for v in residual]}
if __name__=='__main__':
    paths=[(0,0,1,1,2),(0,1,0,1,2),(0,0,1,2,1),(0,1,2,0,1),(0,1,2,3,4),(0,0,0,0,0)]
    reports=[solve(p,k) for p in paths for k in (1,2,3)]
    Path(__file__).with_suffix('.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('types','residual')} for r in reports],indent=2))
