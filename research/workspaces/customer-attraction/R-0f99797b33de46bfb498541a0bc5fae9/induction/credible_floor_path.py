"""Diagnostic for a new credible-floor path recursion; not a half proof.

v(k) is the exact maximin current-player payoff against SPE children.
L(k)=v(k)+min_a L(k+e_a) discards incentive feasibility only in the
total-profit minimization, while retaining credible child threats in v.
Every complete pure SPE has remaining profit >= L(k), by induction.
The candidate under attack is F(k) <= 2L(k), at all legal backgrounds.
"""

from __future__ import annotations

import json
import random
import sys
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def increments(k):
    for a in range(len(k)):
        yield a, k[:a] + (k[a] + 1,) + k[a+1:]


def diagnostic(instance):
    solver = ExactSPESolver(instance)
    solver.outcomes()
    m, p = instance.players, instance.topic_count

    @lru_cache(None)
    def L(k):
        if sum(k) == m:
            return Fraction(0), ()
        child, path = min((L(d)[0], (a,) + L(d)[1]) for a, d in increments(k))
        return solver.threshold(k) + child, path

    def profit(k, terminal):
        return sum((Fraction(c.multiplicity * sum(terminal[a] - k[a] for a in c.topics),
                             sum(terminal[a] for a in c.topics))
                    for c in instance.customers
                    if any(terminal[a] - k[a] for a in c.topics)), Fraction(0))

    @lru_cache(None)
    def all_terminals(k):
        if sum(k) == m:
            return frozenset((k,))
        return frozenset(t for _, d in increments(k) for t in all_terminals(d))

    worst = None
    for k in solver._outcomes:
        if sum(k) == m:
            continue
        f, optimum = max((profit(k, t), t) for t in all_terminals(k))
        l, path = L(k)
        gap = f - 2*l
        row = {'prefix': k, 'F': str(f), 'L': str(l), 'gap': str(gap),
               'path': path, 'optimum': optimum,
               'min_spe_profit': str(min(profit(k,t) for t in solver.outcomes(k)))}
        if worst is None or gap > worst[0]:
            worst = gap, row
    root = (0,)*p
    return {'worst': worst[1], 'root_L': str(L(root)[0]),
            'root_OPT': instance.optimal_welfare(),
            'minimum_SPE_W': solver.minimum_welfare()}


def main():
    reports = []
    for f in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        try:
            instance = Instance.from_dict(json.loads(f.read_text()))
        except (ValueError, KeyError, TypeError):
            continue
        if instance.topic_count > 7 or instance.players > 6:
            continue
        row = diagnostic(instance)
        row['name'] = f.name
        reports.append(row)
        print(json.dumps(row), flush=True)
    rng = random.Random(70411)
    for case in range(100):
        p, m = 4, rng.choice((3,4,5))
        customers = tuple(CustomerType(frozenset(a for a in range(p) if mask>>a & 1), mass)
                          for mask in range(1,1<<p)
                          if (mass := rng.randrange(5)))
        instance = Instance(tuple(map(str,range(p))),customers,m)
        row = diagnostic(instance)
        if Fraction(row['worst']['gap']) > 0:
            row['name'] = f'random-{case}'
            row['instance'] = instance.to_dict()
            reports.append(row)
            print(json.dumps(row), flush=True)
            break
    (Path(__file__).parent/'credible_floor_path_results.json').write_text(json.dumps(reports,indent=2)+'\n')


if __name__ == '__main__':
    main()
