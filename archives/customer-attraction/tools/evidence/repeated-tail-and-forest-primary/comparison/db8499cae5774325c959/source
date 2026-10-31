"""Exact-certificate attack on forest last-slot floor inside sampled full SPE cones.

The LP chooses all forest-resource weights and a lower bound t on every
last-slot menu. A positive t-u_i gives a genuine full-history counterexample
to the forest individual-floor candidate. No finite negative result is a proof.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from math import lcm
from pathlib import Path
import random
import sys
import time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import ExactSPESolver, verify_certificate, Instance, CustomerType
from probe_forest_floor import counts, generator, floor


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction())


def attack(instance):
    solver = ExactSPESolver(instance)
    q = min(solver.worst_outcomes())
    cert = solver.certificate(q)
    p, m = instance.topic_count, instance.players
    support = tuple(sorted({tuple(sorted(c.topics)) for c in instance.customers}))

    @lru_cache(None)
    def payoff(q, a):
        return tuple(Fraction(int(a in t), sum(q[b] for b in t)) if a in t else Fraction()
                     for t in support)

    terminals = {}
    for h in product(range(p), repeat=m):
        terminals[h] = tuple(h.count(a) for a in range(p))
    for depth in range(m - 1, -1, -1):
        for h in product(range(p), repeat=depth):
            terminals[h] = terminals[h + (cert.actions[h],)]
    rows = set()
    for h, a in cert.actions.items():
        actual = payoff(terminals[h], a)
        for b in range(p):
            deviation = payoff(terminals[h + (b,)], b)
            row = tuple(x - y for x, y in zip(actual, deviation))
            if any(row):
                rows.add(row)
    weights = tuple(sum(c.multiplicity for c in instance.customers if tuple(sorted(c.topics)) == t)
                    for t in support)
    menu_rows = []
    for prefix in counts(p, m - 1):
        options = []
        for a in range(p):
            final = prefix[:a] + (prefix[a] + 1,) + prefix[a + 1:]
            row = payoff(final, a)
            options.append((dot(row, weights), row))
        menu_rows.append(max(options, key=lambda item: item[0])[1])
    welfare = tuple(Fraction(any(q[a] for a in t)) for t in support)
    A = [[-float(x) for x in row] + [0.] for row in rows]
    A += [[-float(x) for x in row] + [1.] for row in menu_rows]
    best = None
    for a in range(p):
        if not q[a]:
            continue
        actual = payoff(q, a)
        objective = [float(x) for x in actual] + [-1.]
        res = linprog(objective, A_ub=A, b_ub=np.zeros(len(A)),
                      A_eq=[[float(x) for x in welfare] + [0.]], b_eq=[1.],
                      bounds=(0, None), method='highs')
        if not res.success:
            raise AssertionError(res.message)
        if best is None or -res.fun > best['floating_gap']:
            best = {'floating_gap': float(-res.fun), 'action': a}
        if res.fun >= -1e-8:
            continue
        exact = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
        x, t = exact[:-1], exact[-1]
        if (dot(welfare, x) != 1 or any(value < 0 for value in x)
                or any(dot(row, x) < 0 for row in rows)
                or any(dot(row, x) < t for row in menu_rows)
                or t <= dot(actual, x)):
            raise AssertionError('positive floating point not exactly recovered')
        scale = lcm(*(v.denominator for v in x))
        cloned = Instance(instance.topics,
                          tuple(CustomerType(frozenset(s), int(v * scale))
                                for s, v in zip(support, x) if v), m)
        verify_certificate(cloned, cert).assert_valid()
        theta = floor(cloned)
        actual_u = cloned.topic_payoffs(q)[a]
        assert theta > actual_u
        return {'counterexample': True, 'instance': cloned.to_dict(), 'theta': str(theta),
                'actual_u': str(actual_u), 'root_counts': q, 'action': a,
                'full_strategy': cert.to_dict(), 'floor_lower_bound': str(t * scale),
                'menu_witness_actions': None, 'rows': len(rows)}
    return {'counterexample': False, 'p': p, 'm': m, 'support': support,
            'rows': len(rows), 'root': q, **best}


def main():
    started = time.monotonic()
    rng = random.Random(202610232)
    records = []
    for i in range(80):
        p, m = (5, 6, 7, 8)[i % 4], (3, 4, 5, 6)[i // 4 % 4]
        result = attack(generator(rng, p, m))
        records.append(result)
        print(json.dumps({k: v for k, v in result.items() if k not in ('full_strategy', 'instance', 'support')}
                         | {'i': i, 'seconds': time.monotonic() - started}), flush=True)
        if result['counterexample']:
            HERE.joinpath('forest_floor_cone_counterexample.json').write_text(json.dumps(result, indent=2) + '\n')
            return
    HERE.joinpath('forest_floor_cone_probe.json').write_text(json.dumps(
        {'counterexample': False, 'universal_claim_proved': False, 'records': records,
         'seconds': time.monotonic() - started}, indent=2) + '\n')


if __name__ == '__main__':
    main()
