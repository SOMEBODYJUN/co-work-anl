"""Targeted all-cone check of half dilution vs same-root payoff spread.

m=3,p=3, so OPT_3 equals the total nonempty-type mass C. The objective is
3(u_H-u_L)-2W_H+C. All 81 suffix policies and 6561 ordered pairs are included.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
import numpy as np
from scipy.optimize import linprog
from three_theme_insurer import policy,sub

HERE=Path(__file__).resolve().parent

def main():
    pol=[policy(e,f) for e in range(3) for f in product(range(3),repeat=3)]
    best=F(-100);witness=None;dig=hashlib.sha256();checked=0
    for i,A in enumerate(pol):
        z=(0,A['e'],A['f'][A['e']])
        coverage=tuple(F(any(t>>a&1 for a in z)) for t in range(1,8))
        for j,B in enumerate(pol):
            gap=sub(A['root'],B['root'])
            c=tuple(3*g-2*w+1 for g,w in zip(gap,coverage))
            rows=tuple(sorted(set(A['rows']+B['rows'])))
            sol=linprog(-np.array(c,dtype=float),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),
                        A_eq=np.ones((1,7)),b_eq=[1],bounds=(0,None),method='highs')
            assert sol.success
            x=tuple(F(float(v)).limit_denominator(1000000) for v in sol.x)
            mu=tuple(F(float(-v)).limit_denominator(1000000) for v in sol.ineqlin.marginals)
            assert sum(x)==1 and min(x)>=0 and min(mu,default=0)>=0
            assert all(sum(a*b for a,b in zip(r,x))>=0 for r in rows)
            v=sum(a*b for a,b in zip(c,x))
            cap=max(c[k]+sum(mu[z]*rows[z][k] for z in range(len(rows))) for k in range(7))
            assert cap==v,(i,j,v,cap)
            checked+=1;dig.update(str((i,j,v,mu)).encode())
            if v>best:
                best=v;witness=dict(i=i,j=j,high=[A['e'],list(A['f'])],low=[B['e'],list(B['f'])],
                                   masses=list(map(str,x)),value=str(v),
                                   spread=str(sum(a*b for a,b in zip(gap,x))),
                                   W_H=str(sum(a*b for a,b in zip(coverage,x))),C='1',
                                   dual=list(map(str,mu)))
        if i%15==0:print('policies completed',i+1,'best',best,flush=True)
    report=dict(scope='Exact finite m3p3 all ordered suffix-policy pairs, unrestricted nonnegative incidence types.',
                policies=len(pol),pairs=checked,objective='3spread-2W_H+C',
                exact_maximum=str(best),exact_primals_and_duals_checked=True,
                certificate_stream_sha256=dig.hexdigest(),witness=witness)
    (HERE/'three_theme_dilution.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
