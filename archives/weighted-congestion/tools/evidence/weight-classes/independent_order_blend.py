#!/usr/bin/env python3
"""Independent exact oracle for two-weight-class path-mixture potentials.

No project implementation is imported. Fractions are exact; finite experiments
are regression evidence, not a proof. Output paths are opened exclusively.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys


def polynomial(coefficients, load):
    return sum(c * load ** k for k, c in enumerate(coefficients))


def paths(cost, a, b, p, q):
    high_last = a * sum(cost(a * j + b * q) for j in range(1, p + 1))
    high_last += b * sum(cost(b * j) for j in range(1, q + 1))
    low_last = b * sum(cost(a * p + b * j) for j in range(1, q + 1))
    low_last += a * sum(cost(a * j) for j in range(1, p + 1))
    return high_last, low_last


def grid_checks():
    checks = 0
    for k in range(0, 14):
        degree_bound = max(1, k)
        for a, b in [(Q(1), Q(1)), (Q(3, 2), Q(1)),
                     (Q(2), Q(1)), (Q(7), Q(1)), (Q(101, 3), Q(1))]:
            cost = lambda x: x ** k
            for p, q in itertools.product(range(7), repeat=2):
                h, l = paths(cost, a, b, p, q)
                x = a * p + b * q
                if p:
                    hp, lp = paths(cost, a, b, p - 1, q)
                    assert h - hp == a * cost(x)
                    assert 0 <= l - lp <= a * cost(x)
                    checks += 2
                if q:
                    hp, lp = paths(cost, a, b, p, q - 1)
                    assert l - lp == b * cost(x)
                    assert b * cost(x) <= h - hp <= degree_bound * b * cost(x)
                    checks += 2
    return checks


def game_oracle(weights, cohorts, a, b, strategies, costs, alpha):
    """Enumerate actual strategy profiles and recompute every deviation load."""
    n, m = len(weights), len(costs)
    theta = Q(1, alpha)
    states = list(itertools.product(*(range(len(s)) for s in strategies)))
    potential = {}
    player_costs = {}
    for s in states:
        selected = [strategies[i][s[i]] for i in range(n)]
        loads = [sum(weights[i] for i in range(n) if e in selected[i])
                 for e in range(m)]
        resource_costs = [polynomial(costs[e], loads[e]) for e in range(m)]
        player_costs[s] = [sum(resource_costs[e] for e in selected[i])
                           for i in range(n)]
        phi = Q(0)
        for e in range(m):
            p = sum(cohorts[i] == 0 and e in selected[i] for i in range(n))
            q = sum(cohorts[i] == 1 and e in selected[i] for i in range(n))
            h, l = paths(lambda x: polynomial(costs[e], x), a, b, p, q)
            phi += theta * h + (1 - theta) * l
        potential[s] = phi
    minimum = min(potential.values())
    counts = dict(states=len(states), deviations=0, strict_improvements=0,
                  local_minima=0, global_minima=0)
    for s in states:
        local_minimum = True
        approximate_equilibrium = True
        for i in range(n):
            for j in range(len(strategies[i])):
                if j == s[i]:
                    continue
                t = s[:i] + (j,) + s[i + 1:]
                counts['deviations'] += 1
                if potential[t] < potential[s]:
                    local_minimum = False
                if player_costs[s][i] > alpha * player_costs[t][i]:
                    counts['strict_improvements'] += 1
                    approximate_equilibrium = False
                    assert potential[t] < potential[s], (s, i, j)
        if local_minimum:
            counts['local_minima'] += 1
            assert approximate_equilibrium
        if potential[s] == minimum:
            counts['global_minima'] += 1
            assert approximate_equilibrium
    return counts


def fixtures(d):
    z = [Q(0)] * (d + 1)
    constant = z.copy(); constant[0] = Q(2, 3)
    mono = z.copy(); mono[d] = Q(1, 2)
    mixed = z.copy(); mixed[0] = Q(1); mixed[1] += Q(2, 5); mixed[d] += Q(1, 7)
    costs = [z, constant, mono, mixed]
    strategies = [
        [frozenset(), frozenset({0, 2}), frozenset({1, 2})],
        [frozenset({2}), frozenset({1, 2}), frozenset({2, 3})],
        [frozenset(), frozenset({0, 3}), frozenset({1, 3})],
        [frozenset({0, 1}), frozenset({0, 2, 3})],
    ]
    for a, b in [(Q(3), Q(1)), (Q(1), Q(1)), (Q(5, 2), Q(1, 2))]:
        for cohorts in [(0, 0, 1, 1), (0, 0, 0, 0), (1, 1, 1, 1)]:
            weights = [a if c == 0 else b for c in cohorts]
            yield weights, cohorts, a, b, strategies, costs


def random_game(seed, d):
    rng = random.Random(seed)
    a, b = rng.choice([(Q(3), Q(1)), (Q(1), Q(1)),
                       (Q(5, 2), Q(1, 2)), (Q(101, 3), Q(1))])
    cohorts = tuple(rng.randrange(2) for _ in range(4))
    weights = [a if c == 0 else b for c in cohorts]
    subsets = [frozenset(e for e in range(4) if mask >> e & 1) for mask in range(16)]
    strategies = [rng.sample(subsets, rng.randint(1, 3)) for _ in range(4)]
    costs = []
    for e in range(4):
        coefficients = [Q(0)] * (d + 1)
        for k in set([0, 1, d]):
            coefficients[k] = Q(rng.randrange(4), rng.randrange(1, 5))
        costs.append(coefficients)
    return weights, cohorts, a, b, strategies, costs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--seed-start', type=int, default=0)
    parser.add_argument('--seed-count', type=int, default=24)
    args = parser.parse_args()
    totals = dict(games=0, states=0, deviations=0, strict_improvements=0,
                  local_minima=0, global_minima=0)
    for d, alpha in [(1, 1), (3, 2), (7, 3), (13, 4)]:
        assert alpha * (alpha - 1) == d - 1
        cases = list(fixtures(d))
        cases += [random_game(seed, d) for seed in range(args.seed_start,
                  args.seed_start + args.seed_count)]
        for game in cases:
            result = game_oracle(*game, alpha)
            totals['games'] += 1
            for key, value in result.items():
                totals[key] += value
    report = dict(status='passed', arithmetic='fractions.Fraction (exact)',
                  python_version=sys.version,
                  random_generator='random.Random (Mersenne Twister), one instance per seed',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seed_start=args.seed_start, seed_count=args.seed_count,
                  degree_alpha_pairs=[[1, 1], [3, 2], [7, 3], [13, 4]],
                  grid_checks=grid_checks(), counts=totals,
                  fixtures=['empty strategies', 'retained resources', 'zero costs',
                            'constant terms', 'equal weights', 'absent high class',
                            'absent low class', 'mixed-degree nonnegative polynomials'],
                  scope='Finite exact regression evidence; not a general proof.')
    with open(args.output, 'x', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
