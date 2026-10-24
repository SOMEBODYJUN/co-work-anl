"""Target only the general candidate u_1+u_2 >= 2 v_r(b).

No finite successful run proves the candidate or Q-CAG-HALF.  A violating
complete SPE and one fixed security-query distribution suffice to disprove it.
The search uses a fixed full strategy cone; no history is omitted.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random

import numpy as np
from scipy.optimize import linprog


def compositions(total, size):
    if size == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, size - 1):
            yield (first,) + tail


def run(players=4, topics=6, tries=100, seed=41023):
    rng = random.Random(seed)
    masks = tuple(range(1, 1 << topics))
    member = np.array([[(mask >> a) & 1 for a in range(topics)]
                       for mask in masks], dtype=int)
    # All terminal and near-terminal states, with exact rational coefficients.
    counts = list(compositions(players, topics))
    coef = {}
    for q in counts:
        load = member @ q
        for a in range(topics):
            if q[a]:
                coef[q, a] = tuple(Fraction(int(t[a]), int(c)) if c else Fraction(0)
                                   for t, c in zip(member, load))
    static = list(compositions(players - 1, topics))
    # Query distribution is fixed during each linear strategy-cone attack.
    # Random positive integer masses avoid relying only on the uniform query.
    security_tensor = np.array([[[Fraction(int(t[a]), 1 + int(t @ q))
                                 for t in member] for a in range(topics)]
                               for q in static], dtype=float)
    best = 2.0
    for trial in range(tries):
        # Independent random priorities are attached to count states.  This is
        # merely a way to generate legal full policies, never a model reduction.
        weights = np.array([rng.randrange(0, 11) if rng.random() < .5 else 0
                            for _ in masks])
        if not weights.any():
            weights[0] = 1
        utility = {(q, a): float(np.dot(weights, coeff))
                   for (q, a), coeff in coef.items()}
        action = {}
        children = {}

        @lru_cache(None)
        def solve(q):
            if sum(q) == players:
                return q
            outcomes = []
            for a in range(topics):
                child = list(q)
                child[a] += 1
                z = solve(tuple(child))
                children[q, a] = z
                outcomes.append((utility[z, a], rng.random(), a, z))
            _, _, a, z = max(outcomes)
            action[q] = a
            return z

        origin = (0,) * topics
        z = solve(origin)
        a = action[origin]
        q1 = list(origin)
        q1[a] += 1
        b = action[tuple(q1)]
        objective = np.array(coef[z, a], dtype=float) + np.array(coef[z, b], dtype=float)
        rows = []
        exact_rows = []
        for q, prescribed in action.items():
            actual = children[q, prescribed]
            for deviation in range(topics):
                row = tuple(x-y for x,y in zip(coef[actual, prescribed],
                                               coef[children[q, deviation], deviation]))
                exact_rows.append(row)
                rows.append(row)
        p_raw = ([1] * topics if trial % 3 == 0 else
                 [rng.randrange(0, 13) for _ in range(topics)])
        if not sum(p_raw):
            p_raw[0] = 1
        p = tuple(Fraction(v, sum(p_raw)) for v in p_raw)
        secure = np.einsum('qam,a->qm', security_tensor, np.array(p, dtype=float))
        matrix = np.vstack((-np.array(rows, dtype=float), -secure))
        rhs = np.concatenate((np.zeros(len(rows)), -np.ones(len(secure))))
        lp = linprog(objective, A_ub=matrix, b_ub=rhs, bounds=(0,None), method='highs')
        if not lp.success:
            continue
        if lp.fun < best - 1e-8:
            best = lp.fun
            print(json.dumps({'trial':trial,'candidate_bound':best}), flush=True)
        if lp.fun < 2 - 1e-7:
            rational = tuple(Fraction(float(x)).limit_denominator(10**7) for x in lp.x)
            if any(sum(x*y for x,y in zip(row,rational)) < 0 for row in exact_rows):
                continue
            sec = min(sum(sum(p[a] * int(t[a]) for a in range(topics)) /
                          (1+int(t @ q)) * w
                          for t,w in zip(member,rational)) for q in static)
            pair = sum((coef[z,a][j]+coef[z,b][j])*w for j,w in enumerate(rational))
            if pair < 2*sec:
                payload = {'players':players,'topics':topics,'seed':seed,'trial':trial,
                           'weights':{str(mask):str(w) for mask,w in zip(masks,rational) if w},
                           'strategy_by_counts':{','.join(map(str,q)):a for q,a in action.items()},
                           'outcome':list(z),'first_two':[a,b],
                           'pair_payoff':str(pair),'security_lower_bound':str(sec),
                           'security_query':[str(v) for v in p],
                           'scope':'Disproves only two-block security candidate; not half coverage.'}
                return payload
    return {'status':'no exact counterexample found','tries':tries,'best_float_bound':best,
            'scope':'Finite attack on two-block security candidate; no positive theorem.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tries', type=int, default=100)
    parser.add_argument('--players', type=int, default=4)
    parser.add_argument('--topics', type=int, default=6)
    parser.add_argument('--seed', type=int, default=41023)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = run(args.players,args.topics,args.tries,args.seed)
    if args.output:
        args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
