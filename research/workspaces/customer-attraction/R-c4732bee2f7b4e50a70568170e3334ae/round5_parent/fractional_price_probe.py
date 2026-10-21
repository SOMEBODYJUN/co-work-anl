"""Attack the auxiliary B(u_i)<=W using fixed fractional topic menus.

Finite floating discovery only. Original Q-CAG-HALF is not changed.
Complete history policies are generated from set-valued BI, then their whole
one-step inequality matrices are optimized. No Markov completeness is assumed.
"""
from pathlib import Path
import argparse
import importlib.util
from itertools import combinations
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction').is_dir())
sys.path.insert(0, str(ROOT))
source = Path(__file__).resolve().parents[1]/'credible_search/iterative_search.py'
spec = importlib.util.spec_from_file_location('previous_search', source)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=5)
    ap.add_argument('--players', type=int, default=3)
    ap.add_argument('--rounds', type=int, default=20)
    ap.add_argument('--seed', type=int, default=315219)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    s = prior.Search(args.topics, args.players, args.seed)
    # Uniform fractional menus on each support are exact candidate prices.
    menus = []
    for n in range(3, args.topics+1):
        for J in combinations(range(args.topics), n):
            for k in range(2, n):
                cover = np.minimum(1, s.I[:, J].sum(axis=1)/k)
                menus.append((J, k, cover, n/k))
    queue = list(prior.seeds(args.topics, args.players))
    log = []
    best = -1e100
    start = time.monotonic()
    for it in range(args.rounds):
        label, r = queue[it] if it < len(queue) else s.rng.choice(queue)
        if it >= 3 and it % 3 == 2:
            r = r.copy()
            for _ in range(2):
                r[s.rng.randrange(len(r))] += .05*max(r.max(), 1)
        _, target, _ = s.solve(r)
        actions, A = s.policy(target, ['min','max','uniform','highW'][it%4])
        used = [b for b,c in enumerate(s.Q[target]) if c]
        best_local = None
        for b in used:
            for J,k,cover,tau in menus:
                gain = cover-s.w[target]-tau*s.pay[target,b]
                out = linprog(-gain, A_ub=-A, b_ub=np.zeros(len(A)),
                              A_eq=s.w[[target]], b_eq=[1], bounds=(0,None), method='highs')
                if out.success and (best_local is None or out.fun < best_local[0].fun):
                    best_local = out,b,J,k
        if best_local is None:
            continue
        out,b,J,k = best_local
        queue.append((f'LP{it}', out.x))
        value = -out.fun
        row = {'iteration':it, 'source':label, 'violation_float':value,
               'counts':s.Q[target], 'topic':b, 'menu_support':J, 'menu_weight':f'1/{k}',
               'rows':len(A), 'elapsed':time.monotonic()-start}
        log.append(row)
        if value > best:
            best = value
            saved = {'record':row,'weights_float':out.x.tolist(),
                     'strategy': [[list(h),a] for h,a in actions.items()]}
        report = {'claim':'B(u_i)<=W for each actual player',
                  'status':'finite floating discovery only', 'seed':args.seed,
                  'topics':args.topics,'players':args.players,'log':log,'best':saved}
        args.output.write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(row), flush=True)
        if value > 1e-7:
            break


if __name__ == '__main__':
    main()
