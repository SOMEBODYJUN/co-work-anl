#!/usr/bin/env python3
"""Exact finite audit of chores EFX, using types and a labelled control.

Source instance: He--Tao arXiv:2606.08872v2, Section 3, Table 1.
This reproduces a published counterexample; it is not a new theorem.
Only integer inputs and Fraction arithmetic are used. No numerical tolerance.
Run with --output PATH; refuse to overwrite existing frozen output.
"""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import platform
import random


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def validate(costs, multiplicities):
    if not costs or any(len(row) != len(multiplicities) for row in costs):
        raise ValueError('nonempty agent set and rectangular costs required')
    if any(type(v) is not int or v < 0 for row in costs for v in row):
        raise ValueError('costs must be nonnegative integers')
    if any(type(v) is not int or v < 0 for v in multiplicities):
        raise ValueError('multiplicities must be nonnegative integers')


def type_factor(costs, bundles):
    """min alpha>=1 satisfying every chore-removal inequality, or None."""
    n = len(costs)
    factor = Fraction(1)
    for i in range(n):
        owned_costs = [costs[i][t] for t, v in enumerate(bundles[i]) if v]
        if not owned_costs:
            continue
        own = sum(v * costs[i][t] for t, v in enumerate(bundles[i]))
        residual = own - min(owned_costs)
        for j in range(n):
            other = sum(v * costs[i][t] for t, v in enumerate(bundles[j]))
            if other == 0:
                if residual:
                    return None
            else:
                factor = max(factor, Fraction(residual, other))
    return factor


def solve_types(costs, multiplicities):
    validate(costs, multiplicities)
    n, t = len(costs), len(multiplicities)
    choices = [list(compositions(v, n)) for v in multiplicities]
    seen, efx, best, witness, optimal_types = 0, 0, None, None, 0
    for columns in product(*choices):
        bundles = tuple(tuple(columns[k][i] for k in range(t)) for i in range(n))
        seen += 1
        factor = type_factor(costs, bundles)
        if factor == 1:
            efx += 1
        if factor is not None and (best is None or factor < best):
            best, witness, optimal_types = factor, bundles, 1
        elif factor is not None and factor == best:
            optimal_types += 1
    predicted = 1
    for v in multiplicities:
        predicted *= comb(v + n - 1, n - 1)
    assert seen == predicted
    if witness is not None:
        assert all(sum(row[k] for row in witness) == multiplicities[k] for k in range(t))
        assert type_factor(costs, witness) == best
    return {'type_allocations': seen, 'efx_type_allocations': efx,
            'optimal_alpha': str(best) if best is not None else None,
            'optimal_type_allocations': optimal_types, 'witness': witness}


def solve_labelled(costs, multiplicities):
    """Independent direct oracle: remove each labelled chore, no min shortcut."""
    validate(costs, multiplicities)
    types = [t for t, count in enumerate(multiplicities) for _ in range(count)]
    n, best = len(costs), None
    for owners in product(range(n), repeat=len(types)):
        bundles = [[k for k, owner in enumerate(owners) if owner == i] for i in range(n)]
        factor, finite = Fraction(1), True
        for i in range(n):
            for removed in bundles[i]:
                lhs = sum(costs[i][types[k]] for k in bundles[i] if k != removed)
                for j in range(n):
                    rhs = sum(costs[i][types[k]] for k in bundles[j])
                    if rhs == 0 and lhs:
                        finite = False
                    elif rhs:
                        factor = max(factor, Fraction(lhs, rhs))
        if finite and (best is None or factor < best):
            best = factor
    return str(best) if best is not None else None


def run():
    rng = random.Random(20261020)
    controls = [([[3]], [0]), ([[0], [0]], [3]), ([[2]], [5]),
                ([[1, 2], [2, 1]], [1, 1]), ([[4], [4], [4]], [2])]
    for _ in range(18):
        n, t = rng.choice([2, 3]), rng.choice([1, 2, 3])
        counts = [rng.randrange(3) for _ in range(t)]
        costs = [[rng.randrange(8) for _ in range(t)] for _ in range(n)]
        controls.append((costs, counts))
    checked = []
    for costs, counts in controls:
        result = solve_types(costs, counts)
        independent = solve_labelled(costs, counts)
        assert result['optimal_alpha'] == independent, (costs, counts, result, independent)
        checked.append({'costs': costs, 'multiplicities': counts,
                        'optimal_alpha': independent})
    rejected = 0
    for costs, counts in [([], [1]), ([[1]], [1, 1]), ([[-1]], [1]), ([[1]], [-1])]:
        try:
            solve_types(costs, counts)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('invalid input accepted')
    cases = []
    for large, medium in [(20, 7), (7, 7), (20, 1), (19, 7), (21, 7)]:
        costs = [[large, 1, medium]] * 2 + [[large, medium, 1]] * 2
        result = solve_types(costs, [3, 5, 5])
        cases.append({'large': large, 'medium': medium, 'costs': costs,
                      'multiplicities': [3, 5, 5], **result})
    assert cases[0]['efx_type_allocations'] == 0
    assert Fraction(cases[0]['optimal_alpha']) > 1
    return {'source': 'https://arxiv.org/html/2606.08872v2#S3',
            'identity': 'SEL-CHORES-TRIVALUED-AUDIT-v1',
            'status': 'published-instance reproduction; finite exact observations',
            'python': platform.python_version(), 'seed': 20261020,
            'arithmetic': 'integer and fractions.Fraction; no tolerance',
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'independent_labelled_controls': checked,
            'invalid_inputs_rejected': rejected, 'cases': cases,
            'limits': 'No new general EFX theorem or novelty claim; only these finite inputs.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            f.write(output)
    print(json.dumps({'cases': [{k: case[k] for k in ('large', 'medium',
           'type_allocations', 'efx_type_allocations', 'optimal_alpha')}
           for case in result['cases']], 'controls': len(result['independent_labelled_controls']),
           'invalid_rejected': result['invalid_inputs_rejected']}, ensure_ascii=False, indent=2))
