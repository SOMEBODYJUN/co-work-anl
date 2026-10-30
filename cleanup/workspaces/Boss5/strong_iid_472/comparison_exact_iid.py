"""Recover an exact integer strong-iid counterexample from a saved cone."""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from probe_cones import Model

ROOT=Path(__file__).parent


def integer_row(row):
    den=math.lcm(*(x.denominator for x in row))
    vals=[int(x*den) for x in row]
    gcd=math.gcd(*vals)
    if gcd:
        vals=[x//gcd for x in vals]
    return vals


def exact_rows(policy,m,n):
    masks=range(1,2**m)
    def leaf(h):
        while len(h)<n:
            h=h+(policy[h],)
        return h
    def payoff(a,z):
        return [F(1,sum((t>>b)&1 for b in z)) if t>>a&1 else F(0) for t in masks]
    gamma=[]
    for k in range(n):
        for h in product(range(m),repeat=k):
            base=payoff(policy[h],leaf(h))
            for a in range(m):
                alternative=payoff(a,leaf(h+(a,)))
                gamma.append([x-y for x,y in zip(base,alternative)])
    z=leaf(())
    c=[F(any(t>>a&1 for a in z)) for t in masks]
    return gamma,c,z


def reconstruct(vertex,rows):
    support=[i for i,x in enumerate(vertex) if x>1e-8]
    basis={}
    equations=[([F(1) for _ in support],F(1))]
    for row in rows:
        if abs(sum(float(x)*y for x,y in zip(row,vertex)))<1e-7:
            equations.append(([F(row[i]) for i in support],F(0)))
    for a,b in equations:
        for pivot,(v,rhs) in sorted(basis.items()):
            mult=a[pivot]
            if mult:
                a=[x-mult*y for x,y in zip(a,v)];b-=mult*rhs
        if not any(a):
            assert not b
            continue
        pivot=next(i for i,x in enumerate(a) if x)
        div=a[pivot];a=[x/div for x in a];b/=div
        basis[pivot]=(a,b)
    assert len(basis)==len(support),(len(basis),len(support))
    sol=[F(0)]*len(support)
    for pivot,(a,b) in sorted(basis.items(),reverse=True):
        sol[pivot]=b-sum(a[j]*sol[j] for j in range(pivot+1,len(support)))
    den=math.lcm(*(x.denominator for x in sol))
    whole=[0]*len(vertex)
    for i,x in zip(support,sol):
        whole[i]=int(x*den)
    gcd=math.gcd(*whole)
    return [x//gcd for x in whole]


def main():
    d=json.loads((ROOT/'cones_n3m6.json').read_text())
    m,n=6,3
    policy={tuple(h):a for h,a in d['actions']}
    gamma,c,z=exact_rows(policy,m,n)
    for q in ([F(0),F(1,8),F(0),F(1,4),F(1,4),F(3,8)],
              [F(0),F(11,100),F(0),F(26,100),F(24,100),F(39,100)]):
        ts=[sum(q[a] for a in range(m) if t>>a&1) for t in range(1,2**m)]
        psi=[1-(1-t)**n for t in ts]
        alpha=[[F(bool(t>>a&1))*sum((1-ts[t-1])**j for j in range(n))/n
                for t in range(1,2**m)] for a in range(m)]
        ref=next(a for a in range(m) if q[a])
        kkt=[[x-y for x,y in zip(alpha[ref],alpha[a])] for a in range(m) if a!=ref]
        allrows=[integer_row(row) for row in gamma+kkt]
        lbs=[0]*len(allrows)
        ubs=[np.inf]*len(gamma)+[0 if q[a] else np.inf for a in range(m) if a!=ref]
        obj=[x-y for x,y in zip(c,psi)]
        eq=[np.ones(len(c))]+[allrows[len(gamma)+j] for j,a in enumerate(a for a in range(m) if a!=ref) if q[a]]
        attack=linprog(np.array([float(x) for x in obj]),A_ub=-np.array(allrows,float),
                       b_ub=np.zeros(len(allrows)),A_eq=np.array(eq,float),b_eq=[1]+[0]*(len(eq)-1),
                       bounds=[(0,None)]*len(c),method='highs')
        print('q',q,'exact KKT gap',attack.fun,flush=True)
        if attack.fun >= -1e-8:
            continue
        weights=reconstruct(attack.x,gamma+kkt)
        values=[sum(x*w for x,w in zip(row,weights)) for row in gamma]
        avals=[sum(x*w for x,w in zip(row,weights)) for row in alpha]
        W=sum(x*w for x,w in zip(c,weights));Z=sum(x*w for x,w in zip(psi,weights))
        assert min(values)>=0
        assert all(avals[a]<=avals[ref] for a in range(m))
        assert all(not q[a] or avals[a]==avals[ref] for a in range(m))
        assert W<Z
        witness={'players':n,'topics':list(range(m)),
                 'weights':{str(t):w for t,w in enumerate(weights,1) if w},
                 'q':[str(x) for x in q],'actions':d['actions'],
                 'path':z,'W':str(W),'Z':str(Z),'alpha':[str(x) for x in avals],
                 'minimum_incentive':str(min(values))}
        (ROOT/'strong_iid_integer.json').write_text(json.dumps(witness,indent=2))
        print(json.dumps({k:v for k,v in witness.items() if k!='actions'},indent=2),flush=True)
        return
        allrows.append(integer_row(obj));lbs.append(-np.inf);ubs.append(-1)
        solve=milp(np.ones(len(c)),integrality=np.ones(len(c)),
                   bounds=Bounds(np.zeros(len(c)),np.full(len(c),np.inf)),
                   constraints=LinearConstraint(np.array(allrows,float),lbs,ubs),
                   options={'time_limit':45,'mip_rel_gap':.001})
        print(solve.message,solve.fun,flush=True)
        if solve.x is None:
            continue
        weights=[int(round(x)) for x in solve.x]
        values=[sum(x*w for x,w in zip(row,weights)) for row in gamma]
        avals=[sum(x*w for x,w in zip(row,weights)) for row in alpha]
        W=sum(x*w for x,w in zip(c,weights));Z=sum(x*w for x,w in zip(psi,weights))
        assert min(values)>=0
        assert all(avals[a]<=avals[ref] for a in range(m))
        assert all(not q[a] or avals[a]==avals[ref] for a in range(m))
        assert W<Z
        witness={'players':n,'topics':list(range(m)),
                 'weights':{str(t):w for t,w in enumerate(weights,1) if w},
                 'q':[str(x) for x in q],'actions':d['actions'],
                 'path':z,'W':str(W),'Z':str(Z),'alpha':[str(x) for x in avals],
                 'minimum_incentive':str(min(values))}
        (ROOT/'strong_iid_integer.json').write_text(json.dumps(witness,indent=2))
        print(json.dumps({k:v for k,v in witness.items() if k!='actions'},indent=2),flush=True)
        return

if __name__=='__main__':
    main()
