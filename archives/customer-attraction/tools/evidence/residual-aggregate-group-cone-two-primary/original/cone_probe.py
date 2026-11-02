"""Search fixed residual full-history strategy cones for aggregate failure."""
from itertools import product
import argparse
import json
import random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

from probe import multisets


def group_policy(h, k):
    group = k // 2
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return group if h[0] < group else 0
    return next(a for a in range(0 if h[1] < group else group,
                                 group if h[1] < group else k) if a not in h)


def gamma(k, r, prefix, policy):
    masks = np.arange(1, 1 << k, dtype=np.int64)
    inc = ((masks[:, None] >> np.arange(k)) & 1)
    bg = inc @ np.bincount(prefix, minlength=k)

    def finish(h):
        while len(h) < r:
            h = h + (policy(h, k),)
        return h

    def row(a, z):
        den = bg + inc @ np.bincount(z, minlength=k)
        return np.divide(inc[:, a], den, out=np.zeros(len(masks)), where=den!=0)

    G = []
    for d in range(r):
        for h in product(range(k), repeat=d):
            z = finish(h)
            u = row(z[d], z)
            G.extend(u - row(a, finish(h+(a,))) for a in range(k) if a != z[d])
    z = finish(())
    c = sum(row(a, z) for a in z)
    beta = np.array([inc / (bg + inc @ np.array(q) + 1)[:,None] for q in multisets(k,r-1)])
    return np.array(G), c, beta


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--samples',type=int,default=200)
    ap.add_argument('--seed',type=int,default=172912)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    rng=random.Random(args.seed)
    k=6; r=3
    best=None
    for i in range(args.samples):
        prefix=tuple(rng.randrange(k) for _ in range(rng.randrange(1,7)))
        G,c,beta=gamma(k,r,prefix,group_policy)
        p=np.array([rng.random()**rng.choice((1,3,10)) for _ in range(k)])
        p/=p.sum()
        b=beta@p
        result=linprog(np.r_[c,-r],A_ub=np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-b,np.ones(len(b))]],b_ub=np.zeros(len(G)+len(b)),A_eq=[np.r_[np.ones(len(c)),0]],b_eq=[1],bounds=[(0,None)]*(len(c)+1),method='highs')
        if not result.success:
            raise RuntimeError(result.message)
        gap=-result.fun
        if best is None or gap>best['gap']+1e-9:
            best={'gap':gap,'prefix':prefix,'p':p.tolist(),'weights':result.x[:-1].tolist()}
            print(json.dumps({'sample':i,'gap':gap,'prefix':prefix,'p':p.tolist()}),flush=True)
        if gap>1e-7:
            print('CANDIDATE FAILURE',json.dumps(best),flush=True)
            break
    if args.output:
        with args.output.open('x') as f:
            json.dump({'status':'float screening, no proof','best':best,'samples_requested':args.samples,'seed':args.seed},f,indent=2)


if __name__=='__main__':
    main()
