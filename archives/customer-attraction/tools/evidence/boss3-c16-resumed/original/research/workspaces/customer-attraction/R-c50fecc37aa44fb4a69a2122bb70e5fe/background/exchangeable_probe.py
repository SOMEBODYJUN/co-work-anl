"""Explore two within-group-exchangeable opposite-group reply menus.

This is a menu relaxation until every later mover's incentives are added.
Variables are orbit masses, not per-individual customer weights. Rational
orbit masses can be scaled by binomial orbit sizes to compile unit customers.
"""
from fractions import Fraction
from math import comb
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def choose(n,k):
    return comb(n,k) if 0<=k<=n else 0


def miss(L,a,t):
    return Fraction(choose(L-t,a),choose(L,a))


def leader(L,a,b,m):
    # One chosen X label; m-1 distinct Y followers, averaged over orbit.
    ans=Fraction()
    for h in range(min(b,m-1)+1):
        ans+=Fraction(choose(b,h)*choose(L-b,m-1-h),choose(L,m-1)*(h+1))
    return Fraction(a,L)*ans


def solve(L,m):
    types=[(a,b) for a in range(L+1) for b in range(L+1) if a+b]
    rx=np.array([float(leader(L,a,b,m)) for a,b in types])
    ry=np.array([float(leader(L,b,a,m)) for a,b in types])
    res=[]
    for r in range(m+1):
        o=np.array([float(1-miss(L,a,r)*miss(L,b,m-r)) for a,b in types])
        lp=linprog(-o,A_ub=np.array([rx,ry]),b_ub=np.ones(2),bounds=(0,None),method='highs')
        nz=[(types[i],str(Fraction(float(x)).limit_denominator(100000))) for i,x in enumerate(lp.x) if x>1e-7]
        res.append({'r':r,'value':-lp.fun,'support':nz})
    return {'L':L,'m':m,'best':max(res,key=lambda x:x['value']),'all_values':[a['value'] for a in res]}


if __name__=='__main__':
    out=[]
    for m in range(2,16):
        r=solve(m,m)
        out.append(r)
        print(m,r['best'],flush=True)
    Path(__file__).with_name('exchangeable_probe.json').write_text(json.dumps(out,indent=2)+'\n')
