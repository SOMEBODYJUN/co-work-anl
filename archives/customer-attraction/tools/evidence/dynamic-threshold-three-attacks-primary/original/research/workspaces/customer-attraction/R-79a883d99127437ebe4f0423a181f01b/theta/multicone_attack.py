"""Targeted LP attack on TB / TB-ANY using independent local-SPE witnesses.

Status: experimental attack, not a general proof. Floating LP output is only a
proposal; a strict counterexample is reported only after exact rational checks.
Run from repository root with PYTHONPATH=. .
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import lcm
import argparse
import json
import random
import time

import numpy as np
from scipy.optimize import linprog

from customer_attraction import CustomerType, ExactSPESolver, Instance


def increment(c, a):
    return tuple(v + (j == a) for j, v in enumerate(c))


def local_certificate(solver, prefix):
    """A complete local SPE attaining the minimum first-player payoff Theta."""
    inst = solver.instance
    p, m = inst.topic_count, inst.players
    c0 = inst.counts(prefix)
    theta = solver.threshold(c0)
    first, target = next(
        (a, z)
        for a in range(p)
        for z in sorted(solver.outcomes(increment(c0, a)))
        if inst.topic_payoff(a, z) == theta
    )
    actions = {}

    def expand(h, c, z):
        if len(h) == m:
            return
        floor = solver.threshold(c)
        good = [a for a in range(p)
                if z in solver.outcomes(increment(c, a))
                and inst.topic_payoff(a, z) >= floor]
        a = first if h == prefix else good[0]
        assert a in good
        actions[h] = a
        for b in range(p):
            d = increment(c, b)
            if b == a:
                zz = z
            else:
                zz = min(solver.outcomes(d), key=lambda w: (inst.topic_payoff(b, w), w))
            expand(h + (b,), d, zz)

    expand(prefix, c0, target)
    return actions, first, target


def data_from_actions(p, m, actions, prefix):
    """Integer SPE inequality rows, and first-player payoff coefficients."""
    D = lcm(*range(1, m + 1))
    masks = range(1, 1 << p)

    @lru_cache(None)
    def leaf(h):
        if len(h) == m:
            return tuple(h.count(j) for j in range(p))
        return leaf(h + (actions[h],))

    @lru_cache(None)
    def payoff(a, z):
        return tuple(D // sum(z[j] for j in range(p) if B >> j & 1)
                     if B >> a & 1 else 0 for B in masks)

    rows = set()
    for h, a in actions.items():
        base = payoff(a, leaf(h))
        for b in range(p):
            if b != a:
                other = payoff(b, leaf(h + (b,)))
                row = tuple(x - y for x, y in zip(base, other))
                if any(row):
                    rows.add(row)
    a = actions[prefix]
    return rows, payoff(a, leaf(prefix)), leaf(prefix), D


def rational_vertex(x, rows):
    """Recover a rational basic point, then check all homogeneous inequalities."""
    support = [j for j, y in enumerate(x) if y > 1e-7]
    s = len(support)
    basis = {}

    def add_equation(coefficients, rhs):
        row = list(map(Fraction, coefficients)) + [Fraction(rhs)]
        for pivot in sorted(basis):
            factor = row[pivot]
            if factor:
                row = [a - factor * b for a, b in zip(row, basis[pivot])]
        pivot = next((j for j in range(s) if row[j]), None)
        if pivot is None:
            return False
        factor = row[pivot]
        basis[pivot] = [a / factor for a in row]
        return True

    add_equation([1] * s, 1)
    for row in rows:
        if abs(sum(row[j] * x[j] for j in support)) > 1e-6:
            continue
        sub = [row[j] for j in support]
        if not any(sub):
            continue
        add_equation(sub, 0)
        if len(basis) == s:
            break
    if len(basis) != s:
        return None
    vals = [Fraction(0)] * s
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot]
        vals[pivot] = row[-1] - sum(row[j] * vals[j] for j in range(pivot + 1, s))
    out = [Fraction(0)] * len(x)
    for j, v in zip(support, vals):
        out[j] = v
    if any(v < 0 for v in out) or sum(out) != 1:
        return None
    if any(sum(a * y for a, y in zip(row, out)) < 0 for row in rows):
        return None
    return out


def attempt(inst, path=None):
    p, m = inst.topic_count, inst.players
    solver = ExactSPESolver(inst)
    mode = 'TB' if path is None else 'TB-ANY'
    if path is None:
        z = min(solver.worst_outcomes())
        path = next(solver.ordered_outcomes(z))
        actual = solver.certificate(z, on_path=path).actions
        rows, _, _, D = data_from_actions(p, m, actual, ())
    else:
        rows = set()
        D = lcm(*range(1, m + 1))
        z = inst.counts(path)
    sum_payoff = [0] * ((1 << p) - 1)
    witnesses = []
    for i in range(m):
        actions, first, target = local_certificate(solver, path[:i])
        rr, pp, leaf, DD = data_from_actions(p, m, actions, path[:i])
        assert D == DD and leaf == target
        rows.update(rr)
        sum_payoff = [x + y for x, y in zip(sum_payoff, pp)]
        witnesses.append({'prefix':path[:i], 'action':first, 'target':target})
    # A comparator need not remain optimal after varying the masses: a larger
    # comparator than the proposed budget already refutes the bridge.
    opt_support = max((s for k in range(1, min(p, m) + 1)
                       for s in combinations(range(p), k)),
                      key=lambda s: inst.welfare(tuple(int(j in s) for j in range(p))))
    cmp_mask = sum(1 << j for j in opt_support)
    actual_mask = sum(1 << j for j in range(p) if z[j])
    objective = [v + D * bool(B & actual_mask) - D * bool(B & cmp_mask)
                 for B, v in enumerate(sum_payoff, 1)]
    rows = sorted(rows)
    result = linprog(objective, A_ub=-np.array(rows, dtype=float) if rows else None,
                     b_ub=np.zeros(len(rows)) if rows else None,
                     A_eq=np.ones((1, len(objective))), b_eq=[1],
                     bounds=(0, None), method='highs')
    if not result.success:
        return {'status':'LP failure', 'message':result.message}
    report = {'status':'nonnegative cone minimum' if result.fun >= -1e-7 else 'negative float proposal',
              'value':float(result.fun / D), 'path':path, 'p':p, 'm':m,
              'constraints':len(rows), 'comparator':opt_support, 'mode':mode}
    if result.fun >= -1e-7:
        return report
    mass = rational_vertex(result.x, rows)
    if mass is None:
        report['status'] = 'unreconstructed float proposal'
        return report
    exact = sum(a * y for a, y in zip(objective, mass)) / D
    if exact >= 0:
        report['status'] = 'nonnegative rational proposal'
        return report
    scale = lcm(*(v.denominator for v in mass))
    ints = [int(v * scale) for v in mass]
    new_inst = Instance(tuple('T'+str(j) for j in range(p)), tuple(
        CustomerType(frozenset(j for j in range(p) if B >> j & 1), w)
        for B, w in enumerate(ints, 1) if w), m)
    check = ExactSPESolver(new_inst)
    theta_sum = sum(check.threshold(new_inst.counts(path[:i])) for i in range(m))
    W = new_inst.welfare(new_inst.counts(path))
    O = new_inst.optimal_welfare()
    is_spe = path in set(check.ordered_outcomes())
    assert W + theta_sum < O
    if mode == 'TB':
        assert is_spe
    report.update({'status':'exact ' + mode + ' counterexample', 'instance':new_inst.to_dict(),
                   'exact_cone_objective':str(exact), 'W':W, 'OPT':O,
                   'sumTheta':str(theta_sum), 'path_is_SPE':is_spe,
                   'witnesses':witnesses})
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=100)
    ap.add_argument('--seed', type=int, default=2026102402)
    ap.add_argument('--arbitrary-path', action='store_true')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    start = time.time()
    best = 1e9
    for it in range(args.trials):
        p = rng.choice((4, 5))
        m = rng.choice((3, 4, 5))
        types = tuple(CustomerType(frozenset(j for j in range(p) if B >> j & 1), w)
                      for B in range(1, 1 << p)
                      if (w := rng.choice((0, 0, 0, 1, 2, 5, 10, 20))))
        inst = Instance(tuple('T'+str(j) for j in range(p)), types, m)
        path = tuple(rng.randrange(p) for _ in range(m)) if args.arbitrary_path else None
        report = attempt(inst, path)
        best = min(best, report.get('value', best))
        if report['status'].startswith('exact '):
            print(json.dumps({'iteration':it, 'seed':args.seed, **report}, indent=2))
            break
        if it % 10 == 0:
            print(json.dumps({'iteration':it, 'elapsed':time.time()-start,
                              'best_scaled_cone_minimum':best, 'latest':report}), flush=True)
    else:
        print(json.dumps({'status':'finite cone attack only', 'trials':args.trials,
                          'seed':args.seed, 'elapsed':time.time()-start,
                          'best_scaled_cone_minimum':best}))
