"""Research experiment: joint reoptimization of early normalization multipliers.

This is a template test, not a search for a genuine bad SPE.  Its primal has two
nonnegative client populations whose early SPE slacks can compensate each other.
All accepted output is checked with Fraction.  No external state is mutated.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import random

import numpy as np
from scipy.optimize import linprog


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def data(actions, p, n):
    terminal = {}
    for d in range(n, -1, -1):
        for h in product(range(p), repeat=d):
            terminal[h] = h if d == n else terminal[h + (actions[h],)]

    def payoff(h, a):
        end = terminal[h]
        return tuple(F(1, sum(bool(mask & (1 << z)) for z in end))
                     if mask & (1 << a) else F(0)
                     for mask in range(1, 1 << p))

    early, late, early_keys, late_keys = [], [], [], []
    for h in sorted(actions, key=lambda x: (len(x), x)):
        chosen = actions[h]
        for a in range(p):
            if a == chosen:
                continue
            row = tuple(x - y for x, y in zip(payoff(h, chosen), payoff(h + (a,), a)))
            (late if len(h) == n - 1 else early).append(row)
            (late_keys if len(h) == n - 1 else early_keys).append((h, a))
    c = tuple(F(any(mask & (1 << a) for a in terminal[()])) for mask in range(1, 1 << p))
    return early, late, c, early_keys, late_keys, terminal[()]


def normalize(actions, p, n, root):
    reps = {}
    actual = root[:-1]
    reps[tuple(actual.count(a) for a in range(p))] = actual
    for h in product(range(p), repeat=n-1):
        reps.setdefault(tuple(h.count(a) for a in range(p)), h)
    result = actions.copy()
    for h in product(range(p), repeat=n-1):
        result[h] = actions[reps[tuple(h.count(a) for a in range(p))]]
    return result


def recover_vertex(rows, normalization, floating):
    """Recover the optimizer on its positive support with active rational rows."""
    support = [i for i, x in enumerate(floating) if x > 1e-8]
    candidates = [(normalization, F(1))] + [(row, F(0)) for row in rows
        if abs(sum(float(a) * b for a, b in zip(row, floating))) < 1e-7]
    basis = {}
    for row, rhs in candidates:
        line = [row[j] for j in support] + [rhs]
        for pivot in sorted(basis):
            coefficient = line[pivot]
            if coefficient:
                line = [x - coefficient*y for x, y in zip(line, basis[pivot])]
        pivot = next((j for j, x in enumerate(line[:-1]) if x), None)
        if pivot is None:
            if line[-1]:
                return None
            continue
        basis[pivot] = [x / line[pivot] for x in line]
        if len(basis) == len(support):
            break
    if len(basis) != len(support):
        return None
    x = [F(0)]*len(support)
    for pivot in sorted(basis, reverse=True):
        line = basis[pivot]
        x[pivot] = line[-1] - sum(line[j]*x[j] for j in range(pivot+1, len(support)))
    result = [F(0)]*len(floating)
    for j, v in zip(support, x):
        result[j] = v
    return result


def optimize(actions, p, n):
    e, l, c, ek, lk, root = data(actions, p, n)
    normalized = normalize(actions, p, n, root)
    be, bl, bc, _, _, _ = data(normalized, p, n)
    assert bc == c
    z = (F(0),)*len(c)
    rows = [tuple(a)+tuple(b) for a, b in zip(e, be)]
    rows += [tuple(a)+z for a in l] + [z+tuple(b) for b in bl]
    normalization = c+c
    best = None
    for support in combinations(range(p), min(n, p)):
        mask = sum(1 << a for a in support)
        o = tuple(F(bool(mask & b)) for b in range(1, 1 << p))
        objective = o+o
        result = linprog(-np.array(objective, float), A_ub=-np.array(rows, float),
            b_ub=np.zeros(len(rows)), A_eq=np.array([normalization], float),
            b_eq=[1.], bounds=(0, None), method="highs")
        if not result.success:
            continue
        x = [F(float(t)).limit_denominator(10**7) for t in result.x]
        if min(x) < 0 or dot(normalization, x) != 1 or any(dot(row, x) < 0 for row in rows):
            x = recover_vertex(rows, normalization, result.x)
        if x is None or min(x) < 0 or dot(normalization, x) != 1 or any(dot(row, x) < 0 for row in rows):
            continue
        value = dot(objective, x)
        if best is None or value > best[0]:
            best = value, x, support
    return best, normalized, root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topics", type=int, default=3)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=387511)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    histories = [h for d in range(args.players) for h in product(range(args.topics), repeat=d)]
    best, record = F(0), None
    for t in range(args.trials):
        actions = {h: rng.randrange(args.topics) for h in histories}
        result, normalized, root = optimize(actions, args.topics, args.players)
        if result and result[0] > best:
            best = result[0]
            record = dict(seed=args.seed, trial=t, topics=args.topics, players=args.players,
                value=str(best), actual_root=root, support=result[2],
                x=[str(z) for z in result[1]],
                actions=[[list(h), a] for h, a in actions.items()],
                normalized_actions=[[list(h), a] for h, a in normalized.items()])
            print(json.dumps({"trial": t, "best": str(best)}), flush=True)
        if best > 2:
            break
    if args.output:
        args.output.write_text(json.dumps(record, indent=2)+"\n")


if __name__ == "__main__":
    main()
