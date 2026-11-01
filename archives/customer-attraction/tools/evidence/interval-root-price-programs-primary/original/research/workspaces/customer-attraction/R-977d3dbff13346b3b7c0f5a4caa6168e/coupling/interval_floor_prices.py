"""Terminal-correlated path LP for the HI ancestor-floor price interface.

Finite candidate generator. Accepted primal and dual are checked with Fraction;
ordinary unlabelled edge flows are deliberately not used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import sys

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE.parent/'background'))
from customer_attraction import CustomerType, Instance
from interval_ceiling_dp import IntervalCeilingFloor


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F())


def solve(ins, *, path_limit=100000):
    hi = IntervalCeilingFloor(ins)
    zero = (0,)*ins.topic_count
    hi.bounds(zero)
    paths = []
    def walk(b, actions, edges):
        if sum(b) == ins.players:
            paths.append((tuple(actions), b, tuple(edges)))
            if len(paths) > path_limit:
                raise ValueError('path limit exceeded; use a terminal-labelled flow implementation')
            return
        hi.bounds(b)
        for a in hi.allowed[b]:
            walk(hi.add(b, a), actions+[a], edges+[(b, a)])
    walk(zero, [], [])
    edges = sorted({e for _, _, es in paths for e in es})
    margins = [[F() for _ in paths] for _ in edges]
    edge_index = {e: i for i, e in enumerate(edges)}
    costs = [F(ins.welfare(q)) for _, q, _ in paths]
    for j, (_, q, es) in enumerate(paths):
        utility = ins.topic_payoffs(q)
        for b, a in es:
            margins[edge_index[(b, a)]][j] = utility[a]-hi.level[b]
    result = linprog(np.array(costs, dtype=float),
                     A_ub=-np.array(margins, dtype=float), b_ub=np.zeros(len(edges)),
                     A_eq=np.ones((1, len(paths))), b_eq=[1],
                     bounds=(0, None), method='highs')
    assert result.success, result.message
    values = [F(float(x)).limit_denominator(10**7) for x in result.x]
    lambdas = [F(float(-x)).limit_denominator(10**7) for x in result.ineqlin.marginals]
    value = F(float(result.fun)).limit_denominator(10**7)
    primal_ok = (all(x >= 0 for x in values) and sum(values) == 1
                 and all(dot(row, values) >= 0 for row in margins)
                 and dot(costs, values) == value)
    residual = [costs[j]-sum((lambdas[i]*margins[i][j] for i in range(len(edges))), F())-value
                for j in range(len(paths))]
    dual_ok = all(x >= 0 for x in lambdas) and all(x >= 0 for x in residual)
    # The original HI payment is exactly the lambda=1 path price, not merely
    # bounded by it. This is checked from the terminal payoffs independently.
    all_one = min(costs[j]-sum((row[j] for row in margins), F()) for j in range(len(paths)))
    assert all_one == hi.root()
    out = {'instance': ins.to_dict(), 'path_count': len(paths), 'edge_count': len(edges),
           'G_I': str(hi.root()), 'minimum_HI_terminal_W': str(min(costs)),
           'candidate_value': str(value), 'exact_primal': primal_ok, 'exact_dual': dual_ok}
    if primal_ok and dual_ok:
        out['exact_price_value'] = str(value)
        out['dual_nonzero'] = [{'b': b, 'a': a, 'lambda': str(lam)}
                               for (b, a), lam in zip(edges, lambdas) if lam]
        out['primal_nonzero'] = [{'actions': actions, 'terminal': q, 'weight': str(weight),
                                 'W': str(costs[j])}
                                for j, ((actions, q, _), weight) in enumerate(zip(paths, values)) if weight]
        out['minimum_dual_residual'] = str(min(residual))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--output', default='interval_floor_prices.json')
    args = parser.parse_args()
    source = json.loads((HERE.parent/'background/interval_regression.json').read_text())
    first = Instance.from_dict(source['first_strict_exact_gap']['instance'])
    records = [solve(first)]
    if args.scan:
        for bits in product([0, 1], repeat=7):
            customers = tuple(CustomerType(frozenset(a for a in range(3) if mask >> a & 1))
                              for mask, present in zip(range(1, 8), bits) if present)
            for m in (3, 4):
                ins = Instance(('0', '1', '2'), customers, m)
                if not customers:
                    continue
                out = solve(ins)
                if not (out['exact_primal'] and out['exact_dual']):
                    continue
                baseline = max(F(out['G_I']), F(out['minimum_HI_terminal_W']))
                if F(out['exact_price_value']) > baseline:
                    records.append(out)
                    print(json.dumps({'strict_price_improvement': out['exact_price_value'],
                                      'baseline': str(baseline), 'm': m,
                                      'customers': len(customers)}), flush=True)
    ans = {'identity': 'finite diagnostic of terminal-correlated HI ancestor-floor prices',
           'not_a_general_half_bound': True, 'records': records}
    (HERE/args.output).write_text(json.dumps(ans, indent=2)+'\n')
    print(json.dumps({'saved_records': len(records), 'first_case': records[0]}, indent=2))


if __name__ == '__main__':
    main()
