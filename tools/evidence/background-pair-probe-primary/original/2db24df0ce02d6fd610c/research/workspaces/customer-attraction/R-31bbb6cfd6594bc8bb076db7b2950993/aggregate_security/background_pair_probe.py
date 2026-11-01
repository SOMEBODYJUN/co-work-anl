"""Numerical attack on first-two security payment with legal sunk backgrounds.

This retains every ordered-history incentive of a generated full SPE policy.
Fixed-query cone LP plus zero-sum LP alternation is discovery only.
"""
import argparse
import itertools
import json
import math
import random
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def representation(n, k, background):
    member = np.array([[(mask >> a) & 1 for mask in range(1, 1 << k)]
                       for a in range(k)], dtype=np.int64)
    sunk = np.array(background) @ member
    backgrounds = np.array([tuple(b.count(a) for a in range(k))
                           for b in itertools.combinations_with_replacement(range(k), n-1)])
    reciprocal = 1 / (1 + sunk + backgrounds @ member)
    scale = math.lcm(*range(1, int(max(sunk)) + n + 1))
    return member, sunk, reciprocal, scale


def policy_cone(n, k, member, sunk, scale, weights, rng):
    actions = {}
    rows = []
    def util(a, q):
        return member[a] * (scale // np.maximum(sunk + np.array(q) @ member, 1))
    def walk(h):
        if len(h) == n:
            return tuple(h.count(a) for a in range(k))
        children = [walk(h+(a,)) for a in range(k)]
        vals = [int(util(a, children[a]) @ weights) for a in range(k)]
        best = max(vals)
        a = rng.choice([a for a in range(k) if vals[a] == best])
        actions[h] = a
        q = children[a]
        for b in range(k):
            if b != a:
                rows.append(util(a, q)-util(b, children[b]))
        return q
    q = walk(())
    actual = []
    h = ()
    for i in range(n):
        a = actions[h]
        actual.append(a)
        h += (a,)
    G = np.unique(np.array(rows), axis=0).astype(float) / scale
    pair = (member[actual[0]]+member[actual[1]]) / np.maximum(sunk+np.array(q)@member, 1)
    return actions, G, pair, actual


def security(weights, member, R):
    pay = (R*weights) @ member.T
    out = linprog(np.r_[np.zeros(len(member)), -1.],
                  A_ub=np.column_stack([-pay, np.ones(len(pay))]),
                  b_ub=np.zeros(len(pay)),
                  A_eq=[np.r_[np.ones(len(member)), 0.]], b_eq=[1.],
                  bounds=[(0, None)]*len(member)+[(None, None)], method='highs')
    if not out.success:
        raise ValueError(out.message)
    return out.x[:-1], out.x[-1]


def cone_step(G, pair, member, R, p):
    beta = R*(p@member)
    A = np.vstack([np.column_stack([-G, np.zeros(len(G))]),
                   np.column_stack([-beta, np.ones(len(beta))])])
    out = linprog(np.r_[np.zeros(len(pair)), -1.], A_ub=A, b_ub=np.zeros(len(A)),
                  A_eq=[np.r_[pair, 0.]], b_eq=[1.],
                  bounds=[(0, None)]*len(pair)+[(None, None)], method='highs')
    if not out.success:
        raise ValueError(out.message)
    return out.x[:-1], out.x[-1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--trials', type=int, default=160)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--large', action='store_true')
    args=parser.parse_args()
    rng=random.Random(310102181)
    result={'status':'numerical_only','trials':0,'max_ratio':0.,'candidate':None}
    for trial in range(args.trials):
        n,k=rng.choice([(5,7),(6,6),(6,7)]) if args.large else rng.choice([(3,5),(3,6),(4,5),(4,6),(5,6)])
        background=[0]*k
        for _ in range(rng.choice([1,2,3,5,8])):
            background[rng.randrange(k)]+=1
        member,sunk,R,scale=representation(n,k,background)
        density=rng.choice([.15,.4,.7,1.])
        weights=np.array([rng.randrange(1,16) if rng.random()<density else 0
                          for _ in range((1<<k)-1)],dtype=np.int64)
        actions,G,pair,actual=policy_cone(n,k,member,sunk,scale,weights,rng)
        starts=[security(weights,member,R)[0], np.ones(k)/k]
        for si,p in enumerate(starts):
            old=-1.
            for iteration in range(7):
                w,_=cone_step(G,pair,member,R,p)
                p,v=security(w,member,R)
                ratio=2*v
                if ratio>result['max_ratio']+1e-8:
                    result['max_ratio']=float(ratio)
                    result['incumbent']={'trial':trial,'n':n,'k':k,'background':background,
                                         'start':si,'iteration':iteration,'pair_payment':1.,
                                         'static_security':float(v)}
                    print(json.dumps(result['incumbent']|{'ratio':ratio}),flush=True)
                if ratio>1+1e-7:
                    result['candidate']={'n':n,'k':k,'background':background,'weights':w.tolist(),
                                         'p':p.tolist(),'actual':actual,
                                         'actions':{','.join(map(str,h)):a for h,a in actions.items()}}
                    result['trials']=trial+1
                    args.output.write_text(json.dumps(result,indent=2)+'\n')
                    return
                if ratio<old+1e-9:
                    break
                old=ratio
        result['trials']=trial+1
        if trial%10==0:
            args.output.write_text(json.dumps(result,indent=2)+'\n')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('FINISHED',json.dumps(result),flush=True)


if __name__=='__main__':
    main()
