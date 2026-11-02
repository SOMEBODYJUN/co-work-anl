"""Exploratory screening of safety-optimal mixed static aggregate regret.

All SPE count outcomes are recovered by exact scaled-integer set-valued
backward induction. Security and regret optimization use floating LPs only.
A negative result must be independently rationally reconstructed.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import argparse
import json
import random
import time

import numpy as np
from scipy.optimize import linprog


def multisets(k, n):
    for h in combinations_with_replacement(range(k), n):
        yield tuple(h.count(a) for a in range(k))


def screen(k, n, weights):
    masks=np.arange(1,1<<k,dtype=np.int64)
    inc=(masks[:,None]>>np.arange(k))&1
    w=np.asarray(weights,dtype=np.int64)
    scale=lcm(*range(1,n+1))
    terminals=list(multisets(k,n)); tid={q:j for j,q in enumerate(terminals)}
    loads=np.asarray(terminals)@inc.T
    shares=np.asarray([[scale//int(d) if d else 0 for d in row] for row in loads])*w
    payoffs=shares@inc
    totals=np.sum(payoffs*np.asarray(terminals),axis=1)

    @lru_cache(None)
    def outcomes(q):
        if sum(q)==n:return frozenset((tid[q],))
        children=[outcomes(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(k)]
        floor=max(min(int(payoffs[z,a]) for z in child) for a,child in enumerate(children))
        return frozenset(z for a,child in enumerate(children) for z in child if payoffs[z,a]>=floor)

    f=np.asarray([(w/(1+inc@np.asarray(B)))@inc for B in multisets(k,n-1)])
    sec=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-f,np.ones(len(f))],
                b_ub=np.zeros(len(f)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],
                bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert sec.success
    v=sec.x[-1]
    result=None
    for z in outcomes((0,)*k):
        W=totals[z]/scale
        # Sum_i u_i(a,z_-i), computed directly per customer load.
        c=loads[z]
        coeff=np.where(c>0,(n+1)/(c+1),n)*w
        R=coeff@inc
        opt=linprog(R,A_ub=-f,b_ub=np.full(len(f),-v+1e-9),
                    A_eq=[np.ones(k)],b_eq=[1],bounds=[(0,None)]*k,method='highs')
        assert opt.success
        gap=opt.fun-W
        if result is None or gap>result['gap']:
            result=dict(k=k,n=n,weights=list(map(int,weights)),terminal=terminals[z],
                        welfare=W,security=v,regret_values=R.tolist(),query=opt.x.tolist(),
                        minimum_static_aggregate=opt.fun,gap=gap,root_outcomes=len(outcomes((0,)*k)))
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6)
    ap.add_argument('--n',type=int,default=3);ap.add_argument('--samples',type=int,default=1000)
    ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--seed',type=int,default=101021)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    rng=random.Random(args.seed);best=None;start=time.monotonic();count=0
    for sample in range(args.samples):
        density=rng.choice((.1,.3,1.))
        w=[rng.randrange(1,16) if rng.random()<density else 0 for _ in range((1<<args.k)-1)]
        if not sum(w):continue
        z=screen(args.k,args.n,w);count+=1
        if best is None or z['gap']>best['gap']+1e-7:
            best=z;print(json.dumps(dict(sample=sample,gap=z['gap'],W=z['welfare'],v=z['security'])),flush=True)
        if z['gap']>1e-6 or time.monotonic()-start>args.seconds:break
    packet=dict(status='exploratory exact SPE outcome sets; floating LP screening; not proof',
                seed=args.seed,samples=count,elapsed=time.monotonic()-start,best=best)
    with args.output.open('x') as out:json.dump(packet,out,indent=2)
    print(json.dumps(dict(done=True,samples=count,gap=best['gap'] if best else None)),flush=True)


if __name__=='__main__':main()
