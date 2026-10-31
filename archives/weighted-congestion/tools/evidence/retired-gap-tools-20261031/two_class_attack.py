"""Fixed-x adversarial weight LP for one-large-or-two-small knapsack.

The finite weight LP is exact as a formulation; numerical solutions are evidence,
not universal lower-bound proofs. Requires scipy, numpy. Seed 20261020.
"""
import itertools, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def solve(x, na):
    n=len(x); masks=range(1<<n)
    feas=[]
    for mask in masks:
        aa=(mask & ((1<<na)-1)).bit_count()
        bb=(mask >> na).bit_count()
        if (aa<=1 and bb==0) or (aa==0 and bb<=2):
            feas.append(mask)
    # Variables: n weights followed by one t_R per activation set.
    c=np.zeros(n+(1<<n)); rows=[]
    for r in masks:
        pr=math.prod(x[j] if r>>j&1 else 1-x[j] for j in range(n))
        c[n+r]=pr
        for s in feas:
            if s & ~r: continue
            row=np.zeros(len(c)); row[n+r]=-1
            for j in range(n):
                if s>>j&1: row[j]=1
            rows.append(row)
    eq=np.zeros((1,len(c))); eq[0,:n]=x
    lp=linprog(c,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),
               A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
    assert lp.success, lp.message
    return float(lp.fun), lp.x[:n].tolist()


def uniform_subsupport(x, na):
    """Allow arbitrary supports but one positive weight per size class.

    Piecewise linear breakpoints in u/v are 0,1,2,infinity.
    """
    n=len(x); best=(float('inf'),None)
    for sa in range(1<<na):
        for sb in range(1<<(n-na)):
            for u,v in [(1,0),(0,1),(1,1),(2,1)]:
                w=[u*int(sa>>j&1) if j<na else v*int(sb>>(j-na)&1) for j in range(n)]
                den=sum(p*q for p,q in zip(x,w))
                if den<=0: continue
                num=0
                for r in range(1<<n):
                    pr=math.prod(x[j] if r>>j&1 else 1-x[j] for j in range(n))
                    aw=max([w[j] for j in range(na) if r>>j&1]+[0])
                    bw=sum(sorted([w[j] for j in range(na,n) if r>>j&1],reverse=True)[:2])
                    num+=pr*max(aw,bw)
                val=num/den
                if val<best[0]: best=(val,w)
    return best


def poisson(x,y,u,v):
    # Uniform within classes. Only ratios 0,1,2,infinity need inspection.
    if v==0: return -math.expm1(-x)/x if x else 1.0
    if u==0: return (2-(2+y)*math.exp(-y))/y if y else 1.0
    if u==v: return (2-math.exp(-x-y)-(1+y)*math.exp(-y))/(x+y) if x+y else 1.0
    assert u==2*v
    return (2-(2+y)*math.exp(-x-y))/(2*x+y) if 2*x+y else 1.0


if __name__=='__main__':
    rng=np.random.default_rng(20261020)
    cases=[]; violations=[]
    for na,nb in [(1,2),(2,3),(2,4)]:
        for rep in range(20):
            # a+b>1 and natural LP feasible.
            a,b=0.7,0.4
            x=rng.uniform(.01,.95,na+nb)
            cost=a*sum(x[:na])+b*sum(x[na:])
            if cost>1: x/=cost
            val,w=solve(x,na); uni,uw=uniform_subsupport(x,na)
            case={'a':a,'b':b,'na':na,'x':x.tolist(),'lp':val,'w':w,'class_uniform_subsupport':uni,'uniform_w':uw}
            cases.append(case)
            if val<uni-1e-8: violations.append(case)
    # For NO MIXING, a+b>1. The infimum feasible cost over allowed a,b
    # is (X+Y)/2 if X>=Y, and (2X+Y)/3 if X<=Y.
    # Search the exact closure boundary, not the inadmissible a=.5,b=1/3.
    best=(1,None)
    for j in range(1201):
        y=3*j/1200
        x=2-y if y<=1 else (3-y)/2
        for u,v in [(1,0),(0,1),(1,1),(2,1)]:
            z=poisson(x,y,u,v)
            if z<best[0]: best=(z,[x,y,u,v])
    out={'seed':20261020,'solver':'scipy.optimize.linprog HiGHS','cases':cases,
         'uniformization_violations':violations,'poisson_boundary_grid_min':best,
         'warning':'Finite numeric experiments; not a theorem.'}
    p=Path(__file__).with_suffix('.json'); p.write_text(json.dumps(out,indent=2))
    print(json.dumps({'cases':len(cases),'uniformization_violations':len(violations),'poisson_min':best,'path':str(p)},indent=2))
