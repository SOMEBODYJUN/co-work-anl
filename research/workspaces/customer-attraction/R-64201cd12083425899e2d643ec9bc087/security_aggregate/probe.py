"""Exploratory exact-outcome / floating-security probe for residual subgames.

Integer payoffs are scaled by lcm(1,...,background_size+remaining).  This
recovers ALL pure SPE terminal count vectors, retaining arbitrary historical
tie breaking via the set-valued recursion.  LP numbers are screening only.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations_with_replacement
from math import lcm
import json
from pathlib import Path
import random

import numpy as np
from scipy.optimize import linprog


def multisets(k, n):
    for h in combinations_with_replacement(range(k), n):
        q = [0] * k
        for a in h:
            q[a] += 1
        yield tuple(q)


def probe(k, r, weights, prefix=()):
    masks = np.arange(1, 1 << k, dtype=np.int64)
    inc = ((masks[:, None] >> np.arange(k)) & 1)
    w = np.array(weights, dtype=np.int64)
    bgq = np.bincount(prefix, minlength=k)
    bg = inc @ bgq
    scale = lcm(*range(1, r + len(prefix) + 1))
    terminals = list(multisets(k, r))
    terminal_index = {q: j for j, q in enumerate(terminals)}
    payoffs = []
    totals = []
    for q in terminals:
        load = inc @ np.array(q)
        den = bg + load
        share = np.array([scale // int(d) if d else 0 for d in den]) * w
        u = share @ inc
        payoffs.append(u)
        totals.append(int(u @ np.array(q)))
    payoffs = np.array(payoffs)

    @lru_cache(None)
    def outcomes(q):
        if sum(q) == r:
            return frozenset((terminal_index[q],))
        children = [outcomes(q[:a] + (q[a] + 1,) + q[a+1:]) for a in range(k)]
        floor = max(min(int(payoffs[z, a]) for z in child) for a, child in enumerate(children))
        return frozenset(z for a, child in enumerate(children) for z in child if payoffs[z, a] >= floor)

    root = outcomes((0,) * k)
    worst = min(root, key=totals.__getitem__)
    # Recover one admissible ordered realization, while allowing different
    # off-path selections in the set-valued recursion.
    q = (0,) * k
    path = []
    while len(path) < r:
        children = [outcomes(q[:a] + (q[a]+1,) + q[a+1:]) for a in range(k)]
        floor = max(min(int(payoffs[z,a]) for z in child) for a,child in enumerate(children))
        a = next(a for a,child in enumerate(children) if worst in child and payoffs[worst,a] >= floor)
        path.append(a)
        q = q[:a] + (q[a]+1,) + q[a+1:]
    # The security opponent cannot observe the query's sampled label.
    f = []
    for q in multisets(k, r - 1):
        den = bg + inc @ np.array(q) + 1
        f.append((w / den) @ inc)
    f = np.array(f)
    result = linprog(np.r_[np.zeros(k), -1.], A_ub=np.c_[-f, np.ones(len(f))], b_ub=np.zeros(len(f)), A_eq=[np.r_[np.ones(k), 0]], b_eq=[1], bounds=[(0, None)]*k+[(None, None)], method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    value = result.x[-1]
    total = totals[worst] / scale
    return {'k': k, 'r': r, 'prefix': list(prefix), 'weights': list(map(int, weights)), 'terminal': terminals[worst], 'ordered_path':path, 'path_payoffs':[int(payoffs[worst,a])/scale for a in path], 'tail_total': total, 'security': value, 'ratio': total / (r*value) if value else 1., 'root_outcomes': len(root)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples', type=int, default=300)
    ap.add_argument('--k', type=int, default=6)
    ap.add_argument('--r', type=int, default=3)
    ap.add_argument('--background', type=int, default=3)
    ap.add_argument('--seed', type=int, default=20261021)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    best = None
    for i in range(args.samples):
        density = rng.choice((.1, .3, 1.))
        w = [rng.randint(1, 10) if rng.random() < density else 0 for _ in range((1 << args.k)-1)]
        prefix = tuple(rng.randrange(args.k) for _ in range(args.background))
        result = probe(args.k, args.r, w, prefix)
        if best is None or result['ratio'] < best['ratio'] - 1e-10:
            best = result
            print(json.dumps({'sample': i, 'ratio': result['ratio'], 'tail_total': result['tail_total'], 'security': result['security'], 'terminal': result['terminal'], 'prefix': prefix}), flush=True)
        if result['ratio'] < 1 - 1e-8:
            print('CANDIDATE FAILURE', json.dumps(result), flush=True)
            break
    if args.output:
        with args.output.open('x') as stream:
            json.dump({'status': 'floating LP exploratory; not proof', 'samples_requested': args.samples, 'seed': args.seed, 'best': best}, stream, indent=2)


if __name__ == '__main__':
    main()
