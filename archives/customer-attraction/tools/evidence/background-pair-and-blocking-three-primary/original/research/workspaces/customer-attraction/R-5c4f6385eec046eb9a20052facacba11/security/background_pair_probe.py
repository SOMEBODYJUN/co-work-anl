"""Discovery only: fixed legal background, full ordered suffix policy cone.

The LP preserves every decision in the suffix.  Background providers are
fixed exogenous history, so a separation is not a root-security violation.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import random
import numpy as np
from scipy.optimize import linprog

OUT = Path(__file__).resolve().parent


def make_policy(w, member, r, background, rng):
    k = len(member)
    actions = {}
    base = np.array(background) @ member
    terminal = {}
    for depth in reversed(range(r)):
        for h in itertools.product(range(k), repeat=depth):
            scores = []
            for a in range(k):
                child = h + (a,)
                q = child if len(child) == r else terminal[child]
                load = base + np.sum(member[list(q)], axis=0)
                scores.append(np.dot(w, member[a] / np.maximum(load, 1)))
            vmax = max(scores)
            chosen = rng.choice([a for a in range(k) if scores[a] >= vmax - 1e-9])
            actions[h] = chosen
            child = h + (chosen,)
            terminal[h] = child if len(child) == r else terminal[child]
    return actions


def matrices(actions, member, r, background):
    k = len(member)
    base = np.array(background) @ member
    rows = []
    def util(a, q):
        return member[a] / np.maximum(base + np.sum(member[list(q)], axis=0), 1)
    def walk(h):
        if len(h) == r:
            return h
        children = [walk(h+(a,)) for a in range(k)]
        a = actions[h]
        for b in range(k):
            if b != a:
                rows.append(util(a, children[a])-util(b, children[b]))
        return children[a]
    z = walk(())
    pair = util(z[0], z) + util(z[1], z)
    welfare = sum((util(a, z) for a in z), np.zeros(member.shape[1]))
    backgrounds = list(itertools.combinations_with_replacement(range(k), r-1))
    beta = np.array([1/(1+base+np.sum(member[list(h)], axis=0)) for h in backgrounds])
    return np.unique(np.array(rows), axis=0), pair, welfare, beta, z


def security(w, member, beta):
    pay = (beta*w) @ member.T
    k = len(member)
    result = linprog(np.r_[np.zeros(k), -1.], A_ub=np.column_stack([-pay, np.ones(len(pay))]),
        b_ub=np.zeros(len(pay)), A_eq=np.array([np.r_[np.ones(k), 0.]]), b_eq=[1.],
        bounds=[(0,None)]*k+[(None,None)], method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    return result.x[:-1], result.x[-1]


def optimize(G, c, member, beta, p):
    query = beta*(p@member)
    A = np.vstack([np.column_stack([-G,np.zeros(len(G))]),
                   np.column_stack([-query,np.ones(len(query))])])
    result = linprog(np.r_[np.zeros(len(c)),-1.],A_ub=A,b_ub=np.zeros(len(A)),
        A_eq=np.array([np.r_[c,0.]]),b_eq=[1.],
        bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
    if not result.success:
        return None
    return result.x[:-1], result.x[-1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--runs',type=int,default=500)
    ap.add_argument('--seed',type=int,default=7801288)
    ap.add_argument('--mode',choices=['pair','aggregate'],default='pair')
    args=ap.parse_args()
    rng=random.Random(args.seed)
    nrng=np.random.default_rng(args.seed)
    best=0
    for trial in range(args.runs):
        r=rng.choice([3,4,5])
        k=rng.choice([4,5,6])
        member=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)])
        background=[0]*k
        for j in range(rng.randrange(1,9)):
            background[rng.randrange(k)]+=1
        w=np.array([rng.randrange(1,20) if rng.random()<.4 else 0 for mask in range(1,1<<k)],dtype=float)
        actions=make_policy(w,member,r,background,rng)
        G,pair,wel,beta,z=matrices(actions,member,r,background)
        target=pair if args.mode=='pair' else wel
        factor=2 if args.mode=='pair' else r
        starts=[security(w,member,beta)[0],np.ones(k)/k,nrng.dirichlet(np.ones(k))]
        for s,p in enumerate(starts):
            previous=-1
            for iteration in range(5):
                result=optimize(G,target,member,beta,p)
                if result is None: break
                w,v=result
                p,v=security(w,member,beta)
                ratio=factor*v
                if ratio>best+1e-7:
                    best=ratio
                    print(json.dumps(dict(trial=trial,r=r,k=k,background=background,ratio=ratio)),flush=True)
                if ratio>1+1e-7:
                    packet=dict(trial=trial,r=r,k=k,background=background,ratio=ratio,
                        weights=w.tolist(),p=p.tolist(),path=z,mode=args.mode,
                        actions=[dict(h=h,a=a) for h,a in sorted(actions.items())],status='numerical_only')
                    (OUT/f'background_{args.mode}_failure.json').write_text(json.dumps(packet,indent=2)+'\n')
                    return
                if ratio<=previous+1e-8: break
                previous=ratio
        if trial%20==0:
            print(json.dumps(dict(done=trial,best=best)),flush=True)
    print(json.dumps(dict(status='finite_no_separation',runs=args.runs,mode=args.mode,best=best)),flush=True)


if __name__=='__main__': main()
