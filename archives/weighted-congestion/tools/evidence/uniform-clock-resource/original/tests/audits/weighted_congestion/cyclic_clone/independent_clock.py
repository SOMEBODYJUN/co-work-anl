#!/usr/bin/env python3
"""Independent exact all-state audit of the triple-inversion clock geometry."""
from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import random
import sys


def one_case(weights, alpha, eta):
    n = len(weights)
    pairs = list(itertools.combinations(range(1, n), 2))
    ell = comb(n - 1, 2)
    delta = max(1 - min(weights[0], weights[i], weights[j]) /
                (weights[0] + weights[i] + weights[j]) for i, j in pairs)
    bound = eta / (4 * alpha * alpha * ell)  # B=1
    d = 1
    power = delta
    while power > bound:
        power *= delta
        d += 1
    amplitude = 2 * alpha
    resources = []
    for i, j in pairs:
        group = (0, i, j)
        total = sum(weights[k] for k in group)
        for c in (0, 1):
            literal = (c, 1 - c, c)
            prices = {}
            for mask in range(8):
                load = sum(weights[group[k]] for k in range(3) if mask >> k & 1)
                prices[mask] = amplitude * (load / total) ** d
            resources.append((group, literal, prices))

    def costs(state):
        result = [Q(0)] * n
        full = []
        for group, literal, prices in resources:
            mask = sum((1 << k) for k in range(3) if state[group[k]] == literal[k])
            if mask == 7:
                full.append(group)
            for k in range(3):
                if mask >> k & 1:
                    result[group[k]] += prices[mask]
        return result, full

    cycle = set()
    state = [0] * n
    for _ in range(2):
        for i in range(n):
            cycle.add(tuple(state))
            state[i] = 1 - state[i]
    assert state == [0] * n and len(cycle) == 2 * n
    checked = 0
    off_cycle = 0
    for state in itertools.product((0, 1), repeat=n):
        y = [state[i] ^ state[0] for i in range(1, n)]
        ordered = all(y[i] <= y[i + 1] for i in range(n - 2))
        assert (state in cycle) == ordered
        old, full = costs(state)
        checked += 1
        if ordered:
            assert not full
            assert max(old) <= ell * amplitude * power
            assert alpha * max(old) <= eta / 2
        else:
            off_cycle += 1
            i = 1 + y.index(1)
            target = list(state)
            target[i] = state[0]
            new, new_full = costs(target)
            assert old[i] >= amplitude
            assert all(i not in group for group in new_full)
            assert new[i] <= ell * amplitude * power
            assert old[i] - alpha * (1 + new[i]) >= Q(1, 2)
    return checked, off_cycle, d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    counts = dict(cases=0, states=0, off_cycle_states=0, maximum_degree=0)
    for n in range(3, 8):
        for seed in range(4):
            rng = random.Random(seed)
            weights = [Q(rng.randint(1, 5), rng.randint(1, 3)) for _ in range(n)]
            for alpha in [Q(1), Q(3, 2), Q(2)]:
                states, off_cycle, d = one_case(weights, alpha, Q(1, 4))
                counts['cases'] += 1
                counts['states'] += states
                counts['off_cycle_states'] += off_cycle
                counts['maximum_degree'] = max(counts['maximum_degree'], d)
    report = dict(status='passed', source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  arithmetic='Fraction exact', python_version=sys.version,
                  n_range=[3, 7], seed_range=[0, 3], alpha=['1', '3/2', '2'],
                  assumed_original_B='1', assumed_original_eta='1/4', counts=counts,
                  scope='Clock geometry and worst-case margin bounds only; no original cycle assumed by code.')
    with open(args.output, 'x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
