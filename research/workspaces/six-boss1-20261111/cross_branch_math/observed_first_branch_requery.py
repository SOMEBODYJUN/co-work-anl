#!/usr/bin/env python3
"""Same-source requery with the already recorded first branch kept visible.

Only the second branch is projected. The shared first terminal C remains
the forced topic of that second branch. This is a stronger projection of
the established seven true inequalities, not a new equilibrium theorem.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path

import new_theme_early_projections as base


@lru_cache(None)
def second_min(params, source, p, ell, b, c):
    alpha, gamma, delta_j, delta_v, kappa, _ = params
    values = []
    for sp in range(4 - source):
        for j, v in product((0, 1), repeat=2):
            z2 = p + c + sp + j + v
            values.append(
                base.share((1 - alpha) * c - gamma * v, z2)
                + F(gamma * b, p + c + sp + j + 1)
                + F(delta_j * j + delta_v * v, ell + 1)
                + kappa * v
            )
    assert len(values) == 4 * (4 - source)
    return min(values)


def state_coefficient(params, source, column, actual, query):
    hidden = column['hidden']
    assert len(hidden) == 5 - source
    p, ell = sum(actual[:source]), sum(actual[:5])
    first_t = column['M'] if column['kind'] == 'maximum-root-family-state' else actual[5]
    first_middle = sum(hidden[:-2])
    b, c = hidden[-2:]
    assert len(hidden[:-2]) == 3 - source
    alpha, _, delta_j, delta_v, kappa, mu = params
    q = base.feature(column, actual, query)
    # Query averaging is legal here because q occurs only in this visible
    # first-branch term, outside the second-branch minimum.
    z1 = p + first_t + first_middle + b + c
    rhs = (
        base.share(alpha * first_t - mu * c, z1)
        + F(mu * q, p + first_t + first_middle + b + 1)
        + second_min(params, source, p, ell, b, c)
    )
    count = sum(actual)
    up = F(actual[source], count) if actual[source] else F(0)
    u6 = F(actual[5], count) if actual[5] else F(0)
    return up + (delta_j + delta_v) * u6 - rhs


def build(point):
    columns, hist, weights, _, family, _ = base.topology(point)
    rows = []
    for seed, params in enumerate(base.REQUERY):
        for family_name, indexes in sorted(family.items()):
            source = 0 if family_name == 'M1' else int(family_name[1:]) - 1
            n_hidden = 5 - source
            queries = [f'A{i}' for i in range(1, 7)]
            queries += (['M'] if family_name == 'M1' else []) + [f'H{i}' for i in range(n_hidden)] + ['Y-average']
            for query in queries:
                coeffs = {0: params[4]}
                for i in indexes:
                    c = columns[i]
                    actual = tuple(map(int, hist[c['hist_column']]['actual_bits']))
                    value = state_coefficient(params, source, c, actual, query)
                    if value:
                        coeffs[i] = value
                slack = sum((v * weights[i] for i, v in coeffs.items()), F(0))
                rows.append({
                    'name': f'observed-first-requery:{seed}:{family_name}:{query}',
                    'parameters': list(map(str, params)),
                    'seed': seed, 'actual_source_zero_based': source,
                    'family': family_name, 'query': query,
                    'slack': str(slack), 'slack_float': float(slack),
                    'coefficients': [[i, str(v)] for i, v in sorted(coeffs.items())],
                })
    assert len(rows) == 86
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = args.point.read_bytes()
    point = json.loads(raw)
    rows = build(point)
    negatives = sorted((r for r in rows if F(r['slack']) < 0), key=lambda r: F(r['slack']))
    distinct = {tuple(tuple(c) for c in r['coefficients']) for r in rows}
    output = {
        'scope': 'Seven-IC requery with observed first branch fixed; necessary projection only',
        'source': str(args.point.resolve()),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'columns': len(point['columns']), 'row_count': len(rows),
        'distinct_coefficient_vectors': len(distinct),
        'negative_count': len(negatives),
        'minimum_slack': min((r['slack'] for r in rows), key=F),
        'rows': rows,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'rows'}, ensure_ascii=False), flush=True)
    for r in negatives[:10]:
        print(r['name'], r['slack'], r['slack_float'], flush=True)


if __name__ == '__main__':
    main()
