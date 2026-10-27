"""LP optimization of one *complete* ordered-history strategy's customer weights.

For a fixed strategy, every SPE inequality is linear in type multiplicities.
The continuous LP is exploratory; strict rational feasible solutions can later
be scaled to integer unit customers and checked independently on all histories.
"""
import argparse
import json
from collections import Counter
from functools import lru_cache
from itertools import combinations

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

from spe_dp import solve


def strategy_constraints(strategy, n, players=6):
    @lru_cache(None)
    def terminal(h):
        if len(h) == players:
            return tuple(h.count(a) for a in range(n))
        return terminal(h + (strategy[h],))

    # An inequality is determined by the chosen topic, its final load vector,
    # the deviating topic, and that branch's final load vector.
    keys = set()
    for h, a in strategy.items():
        q = terminal(h)
        for b in range(n):
            if b != a:
                keys.add((a, q, b, terminal(h + (b,))))
    keys = sorted(keys)
    return terminal(()), keys


def matrix(n, constraints):
    masks = list(range(1, 1 << n))
    def coeff(a, q, mask):
        if not mask & (1 << a):
            return 0.0
        return 1.0 / sum(q[b] for b in range(n) if mask & (1 << b))
    rows = []
    cols = []
    data = []
    for i, (a, q, b, r) in enumerate(constraints):
        for j, mask in enumerate(masks):
            x = coeff(a, q, mask) - coeff(b, r, mask)
            if x:
                rows.append(i)
                cols.append(j)
                data.append(-x)  # scipy convention A_ub x <= 0
    return csr_matrix((data, (rows, cols)), shape=(len(constraints), len(masks)))


def optimize(strategy, n=7, players=6):
    q, constraints = strategy_constraints(strategy, n, players)
    A = matrix(n, constraints)
    masks = np.arange(1, 1 << n)
    actual_set = sum((1 << a) for a, c in enumerate(q) if c)
    obj = ((masks & actual_set) > 0).astype(float)
    # Given seven topics and six players, a maximizing set omits one topic.
    best = None
    for omit in range(n):
        opt_mask = (1 << n) - 1 - (1 << omit)
        opt_row = ((masks & opt_mask) > 0).astype(float)
        others = [((masks & ((1 << n)-1-(1 << j))) > 0).astype(float) for j in range(n)]
        fit = linprog(obj, A_ub=csr_matrix(np.vstack([A.toarray(), *others])),
                      b_ub=np.array([0.0] * A.shape[0] + [1.0] * n),
                      A_eq=opt_row[None, :], b_eq=[1.0], bounds=(0, None),
                      method='highs')
        if fit.success and (best is None or fit.fun < best['ratio']):
            best = dict(ratio=fit.fun, omit=omit, weights=[0.0] + fit.x.tolist(),
                        actual_count=q, rows=len(constraints),
                        minimum_slack=float(np.min(-A @ fit.x)))
    return best


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    source = json.load(open(args.input))
    n = (len(source['weights']) - 1).bit_length()
    r = solve(source['weights'], witness=True)
    print('current', r['ratio'], r['min_welfare'], r['optimum'], flush=True)
    strategy = r.pop('strategy')
    lp = optimize(strategy, n)
    print('LP', {k: v for k,v in lp.items() if k!='weights'}, flush=True)
    with open(args.output, 'w') as f:
        json.dump(lp, f, indent=2)


if __name__ == '__main__':
    main()
