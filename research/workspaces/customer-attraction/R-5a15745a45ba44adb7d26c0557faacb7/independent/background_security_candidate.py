"""Falsification only: every r-player subgame has suffix profit >= r v_r(b).

Float LPs propose query distributions. A reported violation is certified by
exact Fraction evaluation of every nonobserving static (r-1)-tuple.
No negative run is evidence for the universal assertion.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json
import random
import sys

from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver


def compositions(total, slots):
    for seq in combinations_with_replacement(range(slots), total):
        q = [0] * slots
        for a in seq:
            q[a] += 1
        yield tuple(q)


def matrix(inst, prefix, r):
    rows = []
    k = inst.topic_count
    for q in compositions(r - 1, k):
        vals = []
        for a in range(k):
            vals.append(sum((Fraction(c.multiplicity,
                sum(prefix[t] + q[t] for t in c.topics) + 1)
                for c in inst.customers if a in c.topics), Fraction()))
        rows.append(vals)
    return rows


def lower_bound(rows):
    k = len(rows[0])
    opt = linprog([0.] * k + [-1.],
        A_ub=[[-float(x) for x in row] + [1.] for row in rows],
        b_ub=[0.] * len(rows), A_eq=[[1.] * k + [0.]], b_eq=[1.],
        bounds=[(0., None)] * k + [(None, None)], method='highs')
    if not opt.success:
        raise RuntimeError(opt.message)
    p = [Fraction(float(x)).limit_denominator(10**7) for x in opt.x[:k]]
    scale = sum(p)
    p = [x / scale for x in p]
    return min(sum((x * y for x, y in zip(row, p)), Fraction())
               for row in rows), p


def main():
    rng = random.Random(7723645)
    smallest_ratio = None
    for rep in range(1500):
        k = rng.choice([3, 4, 5, 6])
        r = rng.choice([3, 4, 5])
        old = rng.choice([1, 1, 2, 3, 5])
        prefix = [0] * k
        for _ in range(old):
            prefix[rng.randrange(k)] += 1
        customers = []
        for mask in range(1, 1 << k):
            multiplicity = rng.randrange(0, 9) if rng.random() < .65 else 0
            if multiplicity:
                customers.append(CustomerType(frozenset(a for a in range(k)
                    if mask & (1 << a)), multiplicity))
        inst = Instance(tuple(map(str, range(k))), tuple(customers), old + r)
        solver = ExactSPESolver(inst)
        outcomes = solver.outcomes(prefix)
        vals = []
        for q in outcomes:
            pay = inst.topic_payoffs(q)
            profit = sum(((q[a] - prefix[a]) * pay[a] for a in range(k)), Fraction())
            vals.append((profit, q))
        profit, target = min(vals)
        vlow, p = lower_bound(matrix(inst, prefix, r))
        ratio = profit / (r * vlow) if vlow else Fraction(1)
        if smallest_ratio is None or ratio < smallest_ratio:
            smallest_ratio = ratio
            print(rep, 'smallest', str(ratio), 'prefix', prefix, 'r', r, flush=True)
        if ratio < 1:
            obj = {'candidate': 'Every background b and r-player pure SPE has suffix profit >= r v_r(b)',
                   'instance': inst.to_dict(), 'prefix': prefix, 'remaining': r,
                   'target_counts': target, 'suffix_profit': str(profit),
                   'safe_query': list(map(str, p)), 'safe_lower_bound': str(vlow),
                   'ratio': str(ratio)}
            dest = Path(__file__).with_name('background_security_violation.json')
            dest.write_text(json.dumps(obj, indent=2) + '\n')
            print('EXACT VIOLATION', dest, flush=True)
            return
    print('No violation in finite random test; no universal conclusion.', flush=True)


if __name__ == '__main__':
    main()
