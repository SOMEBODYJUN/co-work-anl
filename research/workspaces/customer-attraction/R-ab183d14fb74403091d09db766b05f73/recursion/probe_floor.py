"""Discovery-only search for individual OPT/(2m) failures in full SPE cones."""
from __future__ import annotations
import argparse
import itertools
import json
import random
from pathlib import Path
from functools import lru_cache
from math import lcm
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate


def cone(cert, m, k):
    masks = np.arange(1, 2**k, dtype=np.int64)
    hits = ((masks[:, None] >> np.arange(k)) & 1).astype(float)

    @lru_cache(None)
    def terminal(h):
        if len(h) == m:
            return h
        return terminal(h + (cert.actions[h],))

    @lru_cache(None)
    def coeff(h, a):
        path = terminal(h)
        load = hits[:, path].sum(axis=1)
        return np.divide(hits[:, a], load, out=np.zeros(len(masks)), where=load > 0)

    rows = []
    for h, a in cert.actions.items():
        curr = coeff(h, a)
        for b in range(k):
            if b != a:
                rows.append(coeff(h + (b,), b) - curr)
    return np.array(rows), coeff((), cert.actions[()]), terminal(())


def exactify(x, cert, m, k):
    fs = [Fraction(float(v)).limit_denominator(100000) if v > 1e-8 else Fraction(0) for v in x]
    scale = lcm(*(v.denominator for v in fs))
    nums = [int(v * scale) for v in fs]
    inst = Instance(tuple(map(str, range(k))), tuple(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), n)
        for mask, n in enumerate(nums, 1) if n), m)
    report = verify_certificate(inst, cert)
    return inst, report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--m', type=int, default=3)
    p.add_argument('--k', type=int, default=6)
    p.add_argument('--trials', type=int, default=100)
    p.add_argument('--seed', type=int, default=7112)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    rng = random.Random(args.seed)
    m,k = args.m,args.k
    best = float('inf')
    bestdoc = None
    for trial in range(args.trials):
        weights = [rng.randrange(8) if rng.random() < .6 else 0 for _ in range(1,2**k)]
        if not any(weights): continue
        inst = Instance(tuple(map(str,range(k))), tuple(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), w)
            for mask,w in enumerate(weights,1) if w),m)
        solver = ExactSPESolver(inst)
        # Root action payoffs can vary with prescribed path, so sample several.
        allpaths = list(itertools.islice(solver.ordered_outcomes(), 16))
        for path in allpaths:
            cert = solver.certificate(on_path=path)
            A,c,path = cone(cert,m,k)
            for Q in rng.sample(list(itertools.combinations(range(k), min(m,k))), min(5, len(list(itertools.combinations(range(k), min(m,k)))))):
                qmask = sum(1<<a for a in Q)
                obj = np.array([bool(mask&qmask) for mask in range(1,2**k)], dtype=float)
                ans = linprog(c, A_ub=A,b_ub=np.zeros(len(A)), A_eq=obj[None,:],b_eq=[1.],bounds=(0,None),method='highs')
                if ans.success and ans.fun < best-1e-8:
                    candidate, report = exactify(ans.x,cert,m,k)
                    if not report.valid: continue
                    opt = candidate.optimal_welfare()
                    payoffs = candidate.player_payoffs(path)
                    ratio = payoffs[0]/opt
                    best = float(ratio)
                    bestdoc = {'m':m,'k':k,'trial':trial,'path':path,'instance':candidate.to_dict(),'certificate':cert.to_dict(),
                               'payoffs':list(map(str,payoffs)),'opt':opt,'ratio':str(ratio),'comparison':Q}
                    print(json.dumps({key:bestdoc[key] for key in ('trial','path','payoffs','opt','ratio')}),flush=True)
                    if args.output: args.output.write_text(json.dumps(bestdoc,indent=2))
        if best < 1/(2*m)-1e-8: break
    print('best',best,'threshold',1/(2*m), flush=True)

if __name__=='__main__': main()
