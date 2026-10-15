#!/usr/bin/env python3
"""Literal exact verification of WC-R1-INTEGER-TRIAD v1; standard library only."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import platform

WEIGHTS = (16, 2, 5)
# membership[i]: 0 absent, 1 action zero, 2 action one, 3 both actions
PAIRS = (((0, 1, 1), 2, 13), ((1, 1, 2), 1, 59), ((1, 2, 1), 2, 2))

def resources():
    out = []
    for mask, degree, coefficient in PAIRS:
        opposite = tuple(3 - x if x in (1, 2) else x for x in mask)
        for pattern in (mask, opposite):
            out.append((pattern, degree, coefficient))
    return out

def costs(profile, weights=WEIGHTS, data=None):
    """Evaluate from resource loads, never from a precomputed ratio formula."""
    total = [Fraction(0) for _ in weights]
    for mask, degree, coefficient in (resources() if data is None else data):
        users = [i for i in range(len(weights)) if mask[i] & (1 << profile[i])]
        load = sum(Fraction(weights[i]) for i in users)
        value = Fraction(coefficient) * load ** degree
        for i in users:
            total[i] += value
    return total

def ratio(old, new):
    if new:
        return old / new
    return None if old else Fraction(1)  # None denotes positive / zero = infinity

def verify():
    report = []
    for profile in product((0, 1), repeat=3):
        current = costs(profile)
        deviations, factors = [], []
        for i in range(3):
            changed = list(profile)
            changed[i] ^= 1
            new = costs(changed)[i]
            q = ratio(current[i], new)
            assert q is not None  # all six resources have positive coefficients
            factors.append(q)
            deviations.append({'player': i, 'current': str(current[i]),
                               'after': str(new), 'ratio': str(q)})
        factor = max([Fraction(1), *factors])
        report.append({'profile': list(profile), 'deviations': deviations,
                       'factor': str(factor), 'attacker': factors.index(max(factors))})
    threshold = min(Fraction(row['factor']) for row in report)
    assert threshold == Fraction(286, 267)
    assert threshold > Fraction(16, 15)
    # Check that the endpoint is attained, including every player's inequality.
    endpoints = []
    for row in report:
        s = row['profile']
        if all(Fraction(dev['current']) <= threshold * Fraction(dev['after'])
               for dev in row['deviations']):
            endpoints.append(s)
    assert endpoints == [[0, 1, 0], [1, 0, 1]]
    # Symmetry and scaling are independently checked at every state.
    for row in report:
        s = row['profile']
        assert costs(s) == costs([1 - x for x in s])
        assert costs(s, data=[(u, k, 7 * a) for u, k, a in resources()]) == [7 * x for x in costs(s)]
    # Cost-zero conventions, constant cost, empty action, invariant membership.
    assert costs((0,), (1,), [((0,), 0, 4)]) == [0]
    assert costs((0,), (1,), [((1,), 0, 4)]) == [4]
    assert costs((1,), (1,), [((1,), 0, 4)]) == [0]
    assert costs((0,), (1,), [((3,), 0, 4)]) == costs((1,), (1,), [((3,), 0, 4)])
    assert ratio(Fraction(0), Fraction(0)) == 1
    assert ratio(Fraction(1), Fraction(0)) is None
    return {'claim': 'WC-R1-INTEGER-TRIAD v1', 'python': platform.python_version(),
            'arithmetic': 'fractions.Fraction, exact integers/rationals',
            'seed': None, 'precision': 'exact', 'weights': list(WEIGHTS),
            'resources': [{'mask': list(u), 'degree': k, 'coefficient': a} for u, k, a in resources()],
            'states': report, 'threshold': str(threshold), 'endpoint_PNE': endpoints,
            'comparisons': {'threshold_minus_16_over_15': str(threshold - Fraction(16, 15))},
            'limitations': ['one degree-two finite game; no infinite growing lower family',
                            'this verifier does not prove a global upper bound or novelty']}

if __name__ == '__main__':
    result = verify()
    path = Path(__file__).with_name('verification.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'threshold': result['threshold'],
                      'states': len(result['states']), 'deviations': sum(len(r['deviations']) for r in result['states']),
                      'endpoint_PNE': result['endpoint_PNE']}, ensure_ascii=False))
