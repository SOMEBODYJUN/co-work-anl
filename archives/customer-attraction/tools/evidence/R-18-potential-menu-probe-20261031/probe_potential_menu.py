"""Finite attack on the aggregate menu conjecture in symmetric potential games.

Arbitrary integer Phi on sizes m-1 and m; no claim that these are CAGs.
All SPE inequalities are checked exactly after complete-history reconstruction.
LP is only a candidate finder; a rational query is checked against every menu.
"""
from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def compositions(n, p):
    if p == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for rest in compositions(n - a, p - 1):
                yield (a,) + rest


def inc(q, a, delta=1):
    q = list(q)
    q[a] += delta
    return tuple(q)


def probe(m, p, rng, tries, report_every):
    root = (0,) * p
    states_m1 = list(compositions(m - 1, p))
    states_m = list(compositions(m, p))
    for trial in range(tries):
        pm1 = {q: rng.randrange(-10, 11) for q in states_m1}
        pm = {q: rng.randrange(-10, 11) for q in states_m}

        def utility(q, a):
            assert q[a] > 0 and sum(q) == m
            return pm[q] - pm1[inc(q, a, -1)]

        @lru_cache(None)
        def solve(k):
            if sum(k) == m:
                return frozenset([k])
            children = [solve(inc(k, a)) for a in range(p)]
            floor = max(min(utility(q, a) for q in child)
                        for a, child in enumerate(children))
            return frozenset(q for a, child in enumerate(children)
                             for q in child if utility(q, a) >= floor)

        outcomes = sorted(solve(root))
        target = rng.choice(outcomes)
        actions = {}

        def expand(h, k, q):
            if len(h) == m:
                assert k == q
                return
            admissible = [a for a in range(p)
                          if q in solve(inc(k, a))
                          and all(utility(q, a) >= min(utility(d, b)
                                   for d in solve(inc(k, b))) for b in range(p))]
            a = rng.choice(admissible)
            actions[h] = a
            for b in range(p):
                menu = [d for d in sorted(solve(inc(k, b)))
                        if utility(d, b) <= utility(q, a)]
                child_q = q if b == a else rng.choice(menu)
                expand(h + (b,), inc(k, b), child_q)

        expand((), root, target)

        @lru_cache(None)
        def terminal(h):
            if len(h) == m:
                q = [0] * p
                for a in h:
                    q[a] += 1
                return tuple(q)
            return terminal(h + (actions[h],))

        path = ()
        while len(path) < m:
            path += (actions[path],)
        q = terminal(())
        assert q == target
        payoffs = [utility(q, a) for a in path]
        for h, a in actions.items():
            ua = utility(terminal(h + (a,)), a)
            assert all(ua >= utility(terminal(h + (b,)), b) for b in range(p))
        backgrounds = set()
        for i in range(m):
            h = path[:i]
            for a in range(p):
                backgrounds.add(inc(terminal(h + (a,)), a, -1))
        backgrounds = sorted(backgrounds)
        matrix = [[pm[inc(b, a)] - pm1[b] for b in backgrounds]
                  for a in range(p)]
        A = np.array(matrix, dtype=float)
        result = linprog([0] * p + [-1],
                         A_ub=np.column_stack([-A.T, np.ones(len(backgrounds))]),
                         b_ub=np.zeros(len(backgrounds)),
                         A_eq=[[1] * p + [0]], b_eq=[1],
                         bounds=[(0, None)] * p + [(None, None)], method='highs')
        assert result.success
        avg = Fraction(sum(payoffs), m)
        if result.x[-1] > float(avg) + 1e-7:
            dist = [Fraction(float(z)).limit_denominator(1000000) for z in result.x[:p]]
            norm = sum(dist)
            dist = [z / norm for z in dist]
            vals = [sum(dist[a] * matrix[a][j] for a in range(p))
                    for j in range(len(backgrounds))]
            if min(vals) <= avg:
                continue
            return {'model': 'arbitrary symmetric exact potential, not necessarily CAG',
                    'm': m, 'p': p, 'trial': trial,
                    'phi_m1': [[list(k), v] for k, v in sorted(pm1.items())],
                    'phi_m': [[list(k), v] for k, v in sorted(pm.items())],
                    'actions': [[list(h), a] for h, a in sorted(actions.items())],
                    'path': list(path), 'payoffs': payoffs,
                    'average': str(avg), 'menu': [list(b) for b in backgrounds],
                    'query': [str(z) for z in dist],
                    'all_menu_expectations': [str(z) for z in vals],
                    'strict_gap': str(min(vals) - avg)}
        if report_every and (trial + 1) % report_every == 0:
            print(json.dumps({'m': m, 'p': p, 'trials': trial + 1,
                              'last_menu': len(backgrounds)}), flush=True)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=3)
    ap.add_argument('--topics', type=int, default=3)
    ap.add_argument('--trials', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=18311)
    ap.add_argument('--report-every', type=int, default=100)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    r = probe(args.players, args.topics, random.Random(args.seed),
              args.trials, args.report_every)
    print(json.dumps(r if r is not None else {'found': False, 'trials': args.trials},
                     ensure_ascii=False, indent=2), flush=True)
    if r is not None and args.output is not None:
        args.output.write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
