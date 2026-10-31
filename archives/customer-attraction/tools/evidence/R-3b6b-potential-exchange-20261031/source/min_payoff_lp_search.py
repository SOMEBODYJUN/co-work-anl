"""Explore the stronger OPT <= W+(m-1) min_i u_i bridge.

Generate complete SPE policies with the repository oracle, then optimize customer
weights subject to every actual ordered-history incentive row of that fixed
policy. This is discovery code, never a proof of the general bridge.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from random import Random
import argparse
import json
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, ExactSPESolver


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--seed', type=int, default=81891)
    ap.add_argument('--trials', type=int, default=1000)
    ap.add_argument('--topics', type=int, default=4)
    ap.add_argument('--players', type=int, default=3)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    R = Random(args.seed)
    k, n = args.topics, args.players
    masks = list(range(1, 2**k))

    def coeff(a, i):
        return np.array([int(mask >> a[i] & 1) / max(1, sum(mask >> t & 1 for t in a))
                         for mask in masks])

    best = 0.0
    policies = set()
    result = None
    for it in range(args.trials):
        w = [R.randrange(10) for _ in masks]
        I = Instance(tuple(map(str, range(k))), tuple(
            CustomerType(frozenset(j for j in range(k) if mask >> j & 1), v)
            for mask, v in zip(masks, w) if v), n)
        sol = ExactSPESolver(I)
        cert = sol.worst_certificate()
        pol = dict(cert.actions)
        key = tuple(sorted(pol.items()))
        if key in policies:
            continue
        policies.add(key)

        def terminal(h):
            while len(h) < n:
                h = h + (pol[h],)
            return h

        rows = []
        for d in range(n):
            for h in product(range(k), repeat=d):
                base = coeff(terminal(h), d)
                for a in range(k):
                    rows.append(base - coeff(terminal(h+(a,)), d))
        rows = np.array(rows)
        path = terminal(())
        actual_cover = np.array([int(any(mask >> t & 1 for t in path)) for mask in masks])
        for support in combinations(range(k), min(n, k)):
            opt_cover = np.array([int(any(mask >> t & 1 for t in support)) for mask in masks])
            for i in range(n):
                objective = opt_cover - actual_cover - (n-1)*coeff(path, i)
                lp = linprog(-objective, A_ub=-rows, b_ub=np.zeros(len(rows)),
                             A_eq=[np.ones(len(masks))], b_eq=[1], bounds=(0, None), method='highs')
                if lp.success and -lp.fun > best:
                    best = float(-lp.fun)
                if lp.success and -lp.fun > 1e-8:
                    fractions = [Fraction(float(x)).limit_denominator(10**6) for x in lp.x]
                    result = {'seed': args.seed, 'trial': it, 'topics': k, 'players': n,
                              'path': path, 'comparison_support': support,
                              'queried_player': i, 'gap_normalized_float': -lp.fun,
                              'weights_fraction_candidate': [str(x) for x in fractions],
                              'certificate': cert.to_dict(),
                              'warning': 'LP output is discovery only; exact certificate audit required.'}
                    break
            if result:
                break
        if result:
            break
        if (it+1) % 100 == 0:
            print(json.dumps({'trial': it+1, 'policies': len(policies), 'best': best}), flush=True)
    report = result or {'seed': args.seed, 'trials': args.trials, 'policies': len(policies),
                        'best_gap_normalized': best, 'result': 'no counterexample found',
                        'scope': 'Finite fixed-policy search; does not establish the bridge.'}
    print(json.dumps(report, indent=2))
    if args.output:
        with args.output.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    main()
