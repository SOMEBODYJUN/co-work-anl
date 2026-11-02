#!/usr/bin/env python3
"""Attack a candidate static optimal-portfolio matching bridge in full SPE cones.

The bridge asks for SOME optimal support J and some permutation for which the
sum of frozen-other-player deviation payoffs is <= actual W. This code is a
candidate generator only. Accepted counterexamples are exact and check every
full-history incentive, every optimum support, and every matching permutation.
"""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import json
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone, payoff_row, coverage_row, dot, integer_clones


def root_path(actions, m):
    h = ()
    while len(h) < m:
        h += (actions[h],)
    return h


def static_cost_row(p, root, assignment):
    rows = []
    for i, a in enumerate(assignment):
        q = list(root.count(t) for t in range(p))
        q[root[i]] -= 1
        q[a] += 1
        rows.append(payoff_row(p, tuple(q), a))
    return tuple(sum((row[j] for row in rows), Fraction(0)) for j in range(2**p - 1))


def exact_recover(res, a_ub, b_ub, w_eq):
    approximate = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
    def valid(x):
        return min(x[:-1]) >= 0 and dot(w_eq, x) == 1 and all(dot(a, x) <= b for a, b in zip(a_ub, b_ub))
    if valid(approximate):
        return approximate
    support = [j for j, x in enumerate(res.x[:-1]) if x > 1e-8] + [len(res.x) - 1]
    rows = [(w_eq, Fraction(1))] + [(a, b) for a, b in zip(a_ub, b_ub)
        if abs(sum(float(a[j]) * res.x[j] for j in range(len(a))) - float(b)) < 1e-7]
    basis = {}
    for a, b in rows:
        reduced = [a[j] for j in support] + [b]
        for pivot in sorted(basis):
            coefficient = reduced[pivot]
            if coefficient:
                reduced = [x - coefficient * y for x, y in zip(reduced, basis[pivot])]
        pivot = next((j for j, x in enumerate(reduced[:-1]) if x), None)
        if pivot is not None:
            coefficient = reduced[pivot]
            basis[pivot] = [x / coefficient for x in reduced]
        elif reduced[-1]:
            return None
        if len(basis) == len(support):
            break
    if len(basis) != len(support):
        return None
    solution = [Fraction(0)] * len(support)
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        solution[pivot] = row[-1] - sum(row[j] * solution[j] for j in range(pivot + 1, len(support)))
    result = [Fraction(0)] * len(res.x)
    for j, x in zip(support, solution):
        result[j] = x
    result = tuple(result)
    return result if valid(result) else None


def try_cone(cone):
    p, m = cone.topics, cone.players
    z = root_path(cone.actions, m)
    supports = list(combinations(range(p), m))
    coverage = {J: coverage_row(p, J) for J in supports}
    base = [tuple(-x for x in g) + (Fraction(0),) for g in cone.rows]
    match_rows = {J: [(pi, static_cost_row(p, z, pi)) for pi in permutations(J)] for J in supports}
    for J in supports:
        rows = base + [tuple(x - y for x, y in zip(coverage[K], coverage[J])) + (Fraction(0),)
                       for K in supports if K != J]
        rows += [tuple(c - a for c, a in zip(cone.welfare, cost)) + (Fraction(1),)
                 for _, cost in match_rows[J]]
        rhs = [Fraction(0)] * len(rows)
        eq = cone.welfare + (Fraction(0),)
        res = linprog([0.0] * (2**p - 1) + [-1.0],
                      A_ub=np.array(rows, dtype=float), b_ub=np.zeros(len(rows)),
                      A_eq=np.array([eq], dtype=float), b_eq=[1.0],
                      bounds=[(0, None)] * (2**p - 1) + [(None, None)], method='highs')
        if not res.success or res.x[-1] < 1e-7:
            continue
        solution = exact_recover(res, rows, rhs, eq)
        if solution is None or solution[-1] <= 0:
            continue
        w = solution[:-1]
        assert cone.verify(w) and dot(cone.welfare, w) == 1
        optimum = max(dot(c, w) for c in coverage.values())
        best = None
        opt_table = []
        for K in supports:
            if dot(coverage[K], w) == optimum:
                table = [(pi, dot(cost, w)) for pi, cost in match_rows[K]]
                minimum = min(v for _, v in table)
                opt_table.append((K, minimum))
                best = minimum if best is None else min(best, minimum)
        if best > 1:
            return {'weights': [str(x) for x in w], 'integer_clones': integer_clones(w),
                    'actual_terminal': z, 'normalized_welfare': '1',
                    'normalized_optimum': str(optimum), 'best_static_matching': str(best),
                    'all_optimal_support_minima': [(K, str(v)) for K, v in opt_table],
                    'actions': [{'history': h, 'action': a} for h, a in cone.actions.items()]}
    return None


def main():
    for ip in sorted((ROOT / 'examples/customer_attraction').glob('*.json')):
        cp = ROOT / 'evidence/certificates/customer_attraction' / ip.name
        if not cp.exists():
            continue
        try:
            ins = json.loads(ip.read_text())
            p, m = len(ins['topics']), ins['players']
            if m < 2 or m > 4 or p < m or p > 6:
                continue
            cert = json.loads(cp.read_text())
            cert = cert.get('strategy', cert)
            actions = {tuple(a['history']): a['action'] for a in cert['actions']}
            cone = StrategyCone(p, m, actions)
        except (KeyError, TypeError, ValueError):
            continue
        print(json.dumps({'trying': ip.name, 'players': m, 'topics': p}), flush=True)
        result = try_cone(cone)
        if result:
            result['source_cone'] = ip.name
            target = Path(__file__).with_name('static_opt_matching_counterexample.json')
            target.write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({'counterexample': str(target), 'best_matching': result['best_static_matching'],
                              'optimum': result['normalized_optimum']}), flush=True)
            return
    print('No exact counterexample found in processed cones.')


if __name__ == '__main__':
    main()
