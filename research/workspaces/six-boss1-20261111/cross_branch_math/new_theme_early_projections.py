#!/usr/bin/env python3
"""Apply established exact early projections to explicit new H/M/Y topics.

Every source is an actual ordered-history node, with its correct number of
remaining players. Each forced topic and query belongs to the common menu.
The hidden replies are recomputed jointly within the relevant old theorem.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path


REQUERY = (
    tuple(map(F, ('4/7', '1/7', '1/14', '3/28', '1/28', '2/7'))),
    tuple(map(F, ('3/5', '1/10', '1/20', '3/40', '1/40', '1/4'))),
)
# (middle actual-last price, terminal actual-last price, terminal capacity,
#  single common-terminal query weight); all middle capacities are zero.
PORTFOLIO = tuple(tuple(map(F, row)) for row in (
    ('1/18', '7/120', '19/360', '1/9'),
    ('1/18', '16/225', '1/25', '1/9'),
    ('3/64', '1/64', '3/64', '1/16'),
    ('1/26', '1/26', '1/26', '1/13'),
    ('1/18', '1/12', '1/36', '1/9'),
    ('1/8', '3/16', '1/16', '1/4'),
    ('1/18', '1/18', '1/18', '1/9'),
    ('2/27', '1/27', '2/27', '1/9'),
))


def share(numerator, denominator):
    if not numerator:
        return F(0)
    assert denominator > 0
    return numerator / denominator


@lru_cache(None)
def psi(mechanism, params, source, p, ell, t, q):
    """source is zero-based actual position. All arithmetic is exact."""
    if mechanism == 'requery':
        assert 0 <= source <= 3
        alpha, gamma, delta_j, delta_v, kappa, mu = params
        assert 0 <= alpha <= 1 and min(params[1:]) >= 0
        values = []
        for s, sp in product(range(4 - source), repeat=2):
            for b, c, j, v in product((0, 1), repeat=4):
                z1, z2 = p + t + s + b + c, p + c + sp + j + v
                value = (
                    share(alpha * t - mu * c, z1)
                    + share((1 - alpha) * c - gamma * v, z2)
                    + F(gamma * b, p + c + sp + j + 1)
                    + F(delta_j * j + delta_v * v, ell + 1)
                    + kappa * v
                    + F(mu * q, p + t + s + b + 1)
                )
                values.append(value)
        assert len(values) == 16 * (4 - source) ** 2
        return min(values)

    assert mechanism == 'portfolio' and 0 <= source <= 4
    alpha_m, alpha_l, beta_l, mu = params
    assert min(params) >= 0
    n = 5 - source
    values = []
    for s, g in product(range(n), (0, 1)):
        z = p + t + s + g
        values.append(
            share(F(t) - mu * g, z)
            + F(alpha_m * s + alpha_l * g, ell + 1)
            + beta_l * g
            + F(mu * q, p + t + s + 1)
        )
    assert len(values) == 2 * n
    return min(values)


def budgets(mechanism, params, source):
    if mechanism == 'requery':
        return params[2] + params[3], params[4]
    return (4 - source) * params[0] + params[1], params[2]


def feature(column, actual, name):
    if name.startswith('A') and name[1:] in ('1', '2', '3', '4', '5', '6'):
        return F(actual[int(name[1:]) - 1])
    if name == 'M':
        return F(column['M'])
    if name == 'Y-average':
        return F(column['ell'], 6)
    assert name.startswith('H')
    return F(column['hidden'][int(name[1:])])


def topology(point):
    columns = point['columns']
    hist = {i: c for i, c in enumerate(columns) if c['kind'] == 'hist'}
    weights = [F(c['weight']) for c in columns]
    assert min(weights) >= 0
    actual_profit = [F(0)] * 6
    for i, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        count = sum(a)
        for j in range(6):
            actual_profit[j] += weights[i] * (F(a[j], count) if a[j] else F(0))
    family = defaultdict(list)
    for i, c in enumerate(columns):
        if c['kind'] == 'actual-B-family-state':
            family[f"B{c['source']}"] .append(i)
        elif c['kind'] == 'maximum-root-family-state':
            family['M1'].append(i)
    pairs = []
    for name, indexes in sorted(family.items()):
        n_hidden = 5 if name == 'M1' else 6 - int(name[1:])
        named = (['M'] if name == 'M1' else []) + [f'H{i}' for i in range(n_hidden)]
        totals = defaultdict(F)
        for i in indexes:
            totals[columns[i]['hist_column']] += weights[i]
        assert set(totals) == set(hist)
        for hi in hist:
            assert totals[hi] == weights[hi]
        for forced in named + ['Y-average']:
            for query in ['A6'] + named:
                # The query is a fixed named theme; only the forced theme
                # may be a uniform menu average. No unknown Y-Y product.
                pairs.append((name, forced, query))
    assert len(pairs) == 99
    return columns, hist, weights, actual_profit, family, pairs


def projected_cost(mechanism, params, source, actual, t, q):
    p, ell = sum(actual[:source]), sum(actual[:5])
    assert q in (0, 1)
    z0 = psi(mechanism, params, source, p, ell, 0, int(q))
    z1 = psi(mechanism, params, source, p, ell, 1, int(q))
    return (1 - t) * z0 + t * z1


def row_coefficients(spec, columns, hist, family):
    mechanism = spec['mechanism']
    params = tuple(map(F, spec['parameters']))
    source = spec['actual_source_zero_based']
    last_price, capacity = budgets(mechanism, params, source)
    coefficients = {0: capacity}
    for i in family[spec['family']]:
        c = columns[i]
        actual = tuple(map(int, hist[c['hist_column']]['actual_bits']))
        count = sum(actual)
        source_pay = F(actual[source], count) if actual[source] else F(0)
        last_pay = F(actual[5], count) if actual[5] else F(0)
        t = feature(c, actual, spec['forced'])
        q = feature(c, actual, spec['query'])
        coeff = source_pay + last_price * last_pay - projected_cost(mechanism, params, source, actual, t, q)
        if coeff:
            coefficients[i] = coeff
    return sorted(coefficients.items())


def screen(point, max_selected=40):
    columns, hist, weights, profits, family, pairs = topology(point)
    K = weights[0]
    assert columns[0]['kind'] == 'K'
    # For screening, coalesce the point's nonzero state weights by the
    # visible actual bits and forced/query features; row construction below
    # still uses every column, including all zero-weight columns.
    pair_masses = {}
    for name, forced, query in pairs:
        masses = defaultdict(F)
        for i in family[name]:
            if not weights[i]:
                continue
            c = columns[i]
            actual = tuple(map(int, hist[c['hist_column']]['actual_bits']))
            t, q = feature(c, actual, forced), feature(c, actual, query)
            masses[(actual, t, q)] += weights[i]
        pair_masses[(name, forced, query)] = masses

    records = []
    for mechanism, seed_list, source_range in (
        ('requery', REQUERY, range(4)),
        ('portfolio', PORTFOLIO, range(5)),
    ):
        for seed, params in enumerate(seed_list):
            for source in source_range:
                lp, cap = budgets(mechanism, params, source)
                budget = profits[source] + lp * profits[5] + cap * K
                for name, forced, query in pairs:
                    cost = sum((mass * projected_cost(mechanism, params, source, actual, t, q)
                                for (actual, t, q), mass in pair_masses[(name, forced, query)].items()), F(0))
                    slack = budget - cost
                    records.append({
                        'name': f'new-theme-{mechanism}:{seed}:{source}:{name}:{forced}:{query}',
                        'mechanism': mechanism, 'seed': seed,
                        'parameters': list(map(str, params)),
                        'actual_source_zero_based': source, 'family': name,
                        'forced': forced, 'query': query,
                        'slack': str(slack), 'slack_float': float(slack),
                    })
    assert len(records) == 4752
    negatives = sorted((r for r in records if F(r['slack']) < 0), key=lambda r: F(r['slack']))
    selected = []
    seen = set()
    for r in negatives:
        coeffs = row_coefficients(r, columns, hist, family)
        key = tuple(coeffs)
        if key in seen:
            continue
        seen.add(key)
        exact_backsub = sum((value * weights[i] for i, value in coeffs), F(0))
        assert exact_backsub == F(r['slack'])
        selected.append(dict(r, coefficients=[[i, str(v)] for i, v in coeffs]))
        if len(selected) >= max_selected:
            break
    return records, selected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--max-selected', type=int, default=40)
    args = ap.parse_args()
    raw = args.point.read_bytes()
    point = json.loads(raw)
    records, selected = screen(point, args.max_selected)
    negatives = [r for r in records if F(r['slack']) < 0]
    output = {
        'scope': 'Established early necessary projections applied to new legal themes; fixed support, not full SPE',
        'source': str(args.point.resolve()),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'columns': len(point['columns']), 'candidate_count': len(records),
        'negative_count': len(negatives), 'selected_distinct_count': len(selected),
        'minimum_slack': min((r['slack'] for r in records), key=F),
        'rows': records, 'selected_rows': selected,
        'psi_cache': str(psi.cache_info()),
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k not in {'rows', 'selected_rows'}}, ensure_ascii=False), flush=True)
    for r in selected[:10]:
        print(r['name'], r['slack'], r['slack_float'], flush=True)


if __name__ == '__main__':
    main()
