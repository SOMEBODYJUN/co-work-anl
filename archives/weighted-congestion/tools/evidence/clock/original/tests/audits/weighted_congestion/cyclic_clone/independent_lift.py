#!/usr/bin/env python3
"""Raw-strategy independent exact audit of cyclic-window lifting."""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys


def audit(weights, population, degree, tests):
    m = len(weights)
    players = [(a, j) for j in range(population) for a in range(m)]
    rank = {p: index for index, p in enumerate(players)}
    actions = {p: [set(), set()] for p in players}
    coefficients = {}
    expected = [[Q(0), Q(0)] for _ in range(m)]
    for test_id, (a, b, k, direction, z) in enumerate(tests):
        assert a != b and 1 <= k <= population and direction in (1, -1)
        wa, wb = weights[a], weights[b]
        old = [wa ** degree, sum((wa + r * wb) ** degree for r in range(1, k + 1))]
        new = [(wa + k * wb) ** degree, sum((r * wb) ** degree for r in range(1, k + 1))]
        if direction == -1:
            old, new = new, old
        for index, cls in enumerate((a, b)):
            expected[cls][0] += z * old[index]
            expected[cls][1] += z * new[index]
        delta = int(a > b)
        for j in range(population):
            h = (a, j)
            resources = [(test_id, j, side) for side in (0, 1)]
            for resource in resources:
                coefficients[resource] = z
            actions[h][0].add(resources[0])
            actions[h][1].add(resources[1])
            for offset in range(k):
                u = (b, (j + delta + offset) % population)
                side = 0 if rank[u] < rank[h] else 1
                if direction == -1:
                    side = 1 - side
                actions[u][0].add(resources[side])
                actions[u][1].add(resources[1 - side])
    assert all(not choices[0] & choices[1] for choices in actions.values())

    def actual_cost(p, state):
        value = Q(0)
        for resource in actions[p][state[p]]:
            load = sum(weights[u[0]] for u in players if resource in actions[u][state[u]])
            value += coefficients[resource] * load ** degree
        return value

    state = {p: 0 for p in players}
    first_round = {}
    for round_index in range(2):
        for p in players:
            before = actual_cost(p, state)
            state[p] = 1 - state[p]
            after = actual_cost(p, state)
            assert [before, after] == expected[p[0]], (weights, population, degree, tests, p)
            if round_index == 0:
                first_round[p] = (before, after)
            else:
                assert first_round[p] == (before, after)
    assert all(action == 0 for action in state.values())
    return dict(steps=2 * len(players), players=len(players), resources=len(coefficients))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--seed-start', type=int, default=0)
    parser.add_argument('--seed-count', type=int, default=32)
    args = parser.parse_args()
    totals = dict(cases=0, steps=0, players=0, resources=0)
    weights = [Q(7, 3), Q(1, 2), Q(11, 4)]  # deliberately not sorted by weight
    for n in range(1, 8):
        for k in range(1, n + 1):
            for a, b in itertools.permutations(range(3), 2):
                for degree in (0, 1, 2, 5, 13):
                    for direction in (1, -1):
                        result = audit(weights, n, degree, [(a, b, k, direction, Q(2, 3))])
                        totals['cases'] += 1
                        for key, value in result.items():
                            totals[key] += value
    for seed in range(args.seed_start, args.seed_start + args.seed_count):
        rng = random.Random(seed)
        n = rng.randint(1, 7)
        degree = rng.choice([0, 1, 2, 5, 13])
        tests = []
        for _ in range(rng.randint(2, 10)):
            a, b = rng.sample(range(3), 2)
            tests.append((a, b, rng.randint(1, n), rng.choice([1, -1]),
                          Q(rng.randrange(5), rng.randint(1, 5))))
        result = audit(weights, n, degree, tests)
        totals['cases'] += 1
        for key, value in result.items():
            totals[key] += value
    report = dict(status='passed', arithmetic='Fraction exact', python_version=sys.version,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seed_start=args.seed_start, seed_count=args.seed_count,
                  deterministic_population_range=[1, 7], degrees=[0, 1, 2, 5, 13],
                  weights=[str(w) for w in weights], counts=totals,
                  scope='Single-test and multi-test raw-strategy lifting identity only; not a general proof.')
    with open(args.output, 'x', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
