"""Exact certificate audit of every m=3,p=3 same-root suffix-policy pair.

LP only discovers certificates; Fraction checks every final coefficient.
This is a finite catalog/population result, not a general insurer theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json, hashlib
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
P=3
TYPES=tuple(range(1,1<<P))

@lru_cache(None)
def row(h,a):
    return tuple(F(int(bool(t>>a&1)),sum(bool(t>>b&1) for b in h))
                 if t>>a&1 else F(0) for t in TYPES)

def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def policy(e,f):
    rows=[]
    for b in range(P):
        v=row((0,b,f[b]),f[b])
        rows.extend(sub(v,row((0,b,c),c)) for c in range(P) if c!=f[b])
    v=row((0,e,f[e]),e)
    rows.extend(sub(v,row((0,b,f[b]),b)) for b in range(P) if b!=e)
    rows=tuple(sorted(set(r for r in rows if any(r))))
    return dict(e=e,f=f,rows=rows,root=row((0,e,f[e]),0))

def main():
    policies=[policy(e,f) for e in range(P) for f in product(range(P),repeat=P)]
    best=F(-1);worst_dual=F(0);checked=0;dig=hashlib.sha256();witness=None
    for i,A in enumerate(policies):
        for j,B in enumerate(policies):
            c=sub(A['root'],B['root']);rows=tuple(sorted(set(A['rows']+B['rows'])))
            RR=np.array(rows,dtype=float)
            sol=linprog(-np.array(c,dtype=float),A_ub=-RR,b_ub=np.zeros(len(rows)),
                        A_eq=np.ones((1,7)),b_eq=[1],bounds=(0,None),method='highs')
            assert sol.success,sol.message
            x=tuple(F(float(v)).limit_denominator(1000000) for v in sol.x)
            assert sum(x)==1 and min(x)>=0
            assert all(sum(a*b for a,b in zip(r,x))>=0 for r in rows)
            v=sum(a*b for a,b in zip(c,x))
            mu=tuple(F(float(-v)).limit_denominator(1000000) for v in sol.ineqlin.marginals)
            assert min(mu,default=0)>=0
            cap=max(c[k]+sum(mu[z]*rows[z][k] for z in range(len(rows))) for k in range(7))
            assert cap==v,(i,j,v,cap)
            assert cap<=F(1,4),(i,j,v,cap)
            worst_dual=max(worst_dual,cap);checked+=1
            dig.update(str((i,j,v,mu)).encode())
            if v>best:
                best=v;witness=dict(i=i,j=j,high=[A['e'],list(A['f'])],low=[B['e'],list(B['f'])],
                                   x=list(map(str,x)),value=str(v),dual=list(map(str,mu)))
        if i%15==0:print('policies completed',i+1,'of',len(policies),'best',best,flush=True)
    report=dict(scope='All 81 complete two-player suffix policies, all 6561 ordered pairs; m=3,p=3, fixed root topic 0. Arbitrary nonnegative incidence multiplicities.',
                policy_count=len(policies),pairs=checked,exact_max_range=str(best),C='1',
                exact_primal_and_dual_checked=True,certificate_stream_sha256=dig.hexdigest(),witness=witness)
    (HERE/'three_theme_insurer.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
