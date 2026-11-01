"""Exploratory first-two security in a fixed legal background. Numerical LP only."""
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
OLD = ROOT / 'research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py'
spec = importlib.util.spec_from_file_location('old_background', OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def security(q, r, prefix, weights):
    masks = list(weights)
    member = np.array([[(mask >> a) & 1 for mask in masks] for a in range(q)], dtype=float)
    bgs = np.array(list(old.compositions(r-1, q)))
    loads = (bgs + np.array(prefix)) @ member
    pay = ((np.array(list(weights.values())) / (1+loads)) @ member.T)
    res = linprog(np.r_[np.zeros(q), -1.],
                  A_ub=np.column_stack([-pay, np.ones(len(pay))]),
                  b_ub=np.zeros(len(pay)),
                  A_eq=np.array([np.r_[np.ones(q),0.]]), b_eq=[1.],
                  bounds=[(0,None)]*q+[(None,None)], method='highs')
    assert res.success, res.message
    return res.x[-1], res.x[:-1]


def minimum_pair(sol):
    q = sol.q
    z = (0,)*q
    floor = sol.thresholds[z]
    best = None
    witness = None
    for a in range(q):
        ca = tuple(int(i == a) for i in range(q))
        eligible = sol.out & sol.solve(ca)
        while eligible:
            bit = eligible & -eligible
            eligible -= bit
            ti = bit.bit_length()-1
            if sol.pays[ti][a] < floor:
                continue
            for b in range(q):
                cab = tuple(ca[i]+int(i==b) for i in range(q))
                if not (sol.solve(cab) & bit):
                    continue
                if sol.pays[ti][b] < sol.thresholds[ca]:
                    continue
                val = Fraction(sol.pays[ti][a]+sol.pays[ti][b], sol.scale)
                if best is None or val < best:
                    best = val
                    witness = (a,b,sol.terminals[ti])
    return best, witness


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=731931)
    ap.add_argument('--q',type=int,default=6)
    ap.add_argument('--r',type=int,default=4)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    best = 2.
    started = time.time()
    for trial in range(args.trials):
        q,r = args.q,args.r
        prefix = [0]*q
        for _ in range(rng.randrange(0,10)):
            prefix[rng.randrange(q)] += 1
        density = rng.choice([.08,.2,.5,1.])
        weights = {mask:rng.randrange(1,26) for mask in range(1,1<<q) if rng.random()<density}
        if not weights:
            continue
        sol = old.BackgroundSolver(q,r,prefix,weights)
        pair,witness = minimum_pair(sol)
        v,p = security(q,r,prefix,weights)
        ratio = float(pair)/(2*v) if v else 1.
        if ratio < best-1e-9:
            best = ratio
            rec = dict(trial=trial,q=q,r=r,seed=args.seed,prefix=prefix,weights=weights,
                       pair=str(pair),witness=witness,v=v,p=p.tolist(),ratio=ratio,
                       status='numerical LP search; SPE ordered-prefix admissibility exact')
            (HERE/f'background_pair_best_{q}_{r}.json').write_text(json.dumps(rec,indent=2)+'\n')
            print(json.dumps(dict(trial=trial,r=r,ratio=ratio,pair=str(pair),v=v,seconds=time.time()-started)),flush=True)
        if ratio < 1-1e-7:
            print('PAIR_FAILURE_FOUND',flush=True)
            return
    print(json.dumps(dict(completed=args.trials,best=best,seconds=time.time()-started)),flush=True)


if __name__ == '__main__':
    main()
