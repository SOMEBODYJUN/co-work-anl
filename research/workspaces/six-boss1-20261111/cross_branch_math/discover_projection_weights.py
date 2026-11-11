#!/usr/bin/env python3
"""Targeted nonnegative-weight LP discovery with exact acceptance.

The LP is only a parameter finder. A result is a certified separating cut
only after all weights are rationalized inside the nonnegative domain,
the complete hidden domain is minimized exactly, and the original point
has strictly negative exact slack in the full column layout.
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

import numpy as np
from scipy.optimize import linprog

import new_theme_early_projections as base


def ratio(n, d):
    return F(n, d) if n else F(0)


@lru_cache(None)
def affine_candidates(mechanism, source, case):
    """Every candidate is (constant, tuple(global-parameter coefficients))."""
    if mechanism == 'portfolio':
        p, ell, t, q = case
        n = 5 - source
        assert 0 <= source <= 4
        candidates = []
        for s, g in product(range(n), (0, 1)):
            z = p + t + s + g
            candidates.append((ratio(t, z), (
                F(s, ell + 1), F(g, ell + 1), F(s), F(g),
                -ratio(g, z) + ratio(q, p + t + s + 1),
            )))
        assert len(candidates) == 2 * n
        return tuple(dict.fromkeys(candidates))

    assert mechanism in ('requery', 'observed-first') and 0 <= source <= 3
    if mechanism == 'observed-first':
        p, ell, t, s, b, c, q = case
        first_states = ((s, b, c),)
    else:
        p, ell, t, q = case
        first_states = tuple((s, b, c) for s in range(4 - source)
                             for b, c in product((0, 1), repeat=2))
    candidates = []
    for s, b, c in first_states:
        z1 = p + t + s + b + c
        for sp in range(4 - source):
            for j, v in product((0, 1), repeat=2):
                z2 = p + c + sp + j + v
                candidates.append((ratio(c, z2), (
                    ratio(t, z1) - ratio(c, z2),
                    -ratio(v, z2) + F(b, p + c + sp + j + 1),
                    F(j, ell + 1), F(v, ell + 1), F(v),
                    -ratio(c, z1) + ratio(q, p + t + s + b + 1),
                )))
    raw_expected = (4 * (4 - source) if mechanism == 'observed-first'
                    else 16 * (4 - source) ** 2)
    assert len(candidates) == raw_expected
    return tuple(dict.fromkeys(candidates))


@lru_cache(None)
def exact_min(mechanism, source, case, parameters):
    return min(constant + sum((a * p for a, p in zip(coeff, parameters)), F(0))
               for constant, coeff in affine_candidates(mechanism, source, case))


def budget_coefficients(mechanism, source, parameters):
    if mechanism == 'portfolio':
        am, al, bm, bl, _ = parameters
        return (4 - source) * am + al, (4 - source) * bm + bl
    return parameters[2] + parameters[3], parameters[4]


def cases_for_state(spec, column, actual):
    source, mechanism = spec['actual_source_zero_based'], spec['mechanism']
    p, ell = sum(actual[:source]), sum(actual[:5])
    q = base.feature(column, actual, spec['query'])
    if mechanism == 'observed-first':
        expected_source = 0 if spec['family'] == 'M1' else int(spec['family'][1:]) - 1
        assert source == expected_source
        hidden = column['hidden']
        assert len(hidden) == 5 - source
        t = column['M'] if spec['family'] == 'M1' else actual[5]
        s, b, c = sum(hidden[:-2]), hidden[-2], hidden[-1]
        return (((p, ell, t, s, b, c, q), F(1)),)
    t = base.feature(column, actual, spec['forced'])
    assert q in (0, 1)
    return tuple((case, probability) for case, probability in (
        ((p, ell, 0, int(q)), 1 - t), ((p, ell, 1, int(q)), t),
    ) if probability)


def build_exact_row(spec, parameters, columns, hist, family):
    source, mechanism = spec['actual_source_zero_based'], spec['mechanism']
    last_price, capacity = budget_coefficients(mechanism, source, parameters)
    row = {0: capacity} if capacity else {}
    for index in family[spec['family']]:
        column = columns[index]
        actual = tuple(map(int, hist[column['hist_column']]['actual_bits']))
        count = sum(actual)
        up = F(actual[source], count) if actual[source] else F(0)
        u6 = F(actual[5], count) if actual[5] else F(0)
        cost = sum((probability * exact_min(mechanism, source, case, parameters)
                    for case, probability in cases_for_state(spec, column, actual)), F(0))
        coefficient = up + last_price * u6 - cost
        if coefficient:
            row[index] = coefficient
    return row


def discover(spec, columns, hist, weights, profits, family, weight_budget):
    source, mechanism = spec['actual_source_zero_based'], spec['mechanism']
    seed_parameters = tuple(map(F, spec['seed_parameters']))
    if mechanism == 'portfolio':
        am, al, bl, mu = seed_parameters
        seed_parameters = (am, al, F(0), bl, mu)
    seed_row = build_exact_row(spec, seed_parameters, columns, hist, family)
    seed_value = sum((v * weights[i] for i, v in seed_row.items()), F(0))
    assert seed_value == F(spec['seed_slack']), ('affine/seed implementation mismatch', spec, seed_value)
    masses = defaultdict(F)
    for index in family[spec['family']]:
        if not weights[index]:
            continue
        column = columns[index]
        actual = tuple(map(int, hist[column['hist_column']]['actual_bits']))
        for case, probability in cases_for_state(spec, column, actual):
            masses[case] += weights[index] * probability
    cases = sorted(masses)
    parameters_count = 5 if mechanism == 'portfolio' else 6
    objective = [0.0] * (parameters_count + len(cases))
    K, u6 = weights[0], profits[5]
    if mechanism == 'portfolio':
        parameter_names = ['alpha_middle', 'alpha_last', 'beta_middle', 'beta_last', 'mu']
        objective[:5] = list(map(float, ((4-source)*u6, u6, (4-source)*K, K, F(0))))
        parameter_bounds = [(0, None)] * 5
        budget_start = 0
    else:
        parameter_names = ['alpha', 'gamma', 'delta_J', 'delta_V', 'kappa', 'mu']
        objective[:6] = list(map(float, (F(0), F(0), u6, u6, K, F(0))))
        parameter_bounds = [(0, 1)] + [(0, None)] * 5
        budget_start = 1
    inequalities, upper = [], []
    for ci, case in enumerate(cases):
        objective[parameters_count + ci] = -float(masses[case])
        for constant, coefficients in affine_candidates(mechanism, source, case):
            row = [-float(c) for c in coefficients] + [0.0] * len(cases)
            row[parameters_count + ci] = 1.0
            inequalities.append(row)
            upper.append(float(constant))
    # Compact discovery section, not a mathematical upper bound on valid
    # weights. Failure to separate in this section is not projection closure.
    normalization = [0.0] * (parameters_count + len(cases))
    for j in range(budget_start, parameters_count):
        normalization[j] = 1.0
    inequalities.append(normalization)
    upper.append(float(weight_budget))
    result = linprog(
        objective, A_ub=np.asarray(inequalities), b_ub=np.asarray(upper),
        bounds=parameter_bounds + [(None, None)] * len(cases),
        method='highs',
        options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9},
    )
    report = dict(spec, parameter_names=parameter_names, weight_budget=weight_budget,
                  positive_visible_states=len(cases), inequalities=len(inequalities),
                  success=bool(result.success), status=str(result.message))
    if not result.success:
        return report
    parameters = [F(float(v)).limit_denominator(1_000_000) for v in result.x[:parameters_count]]
    parameters = [max(F(0), v) for v in parameters]
    if mechanism != 'portfolio':
        parameters[0] = min(F(1), parameters[0])
    parameters = tuple(parameters)
    assert min(parameters) >= 0
    if mechanism != 'portfolio':
        assert parameters[0] <= 1
    row = build_exact_row(spec, parameters, columns, hist, family)
    exact_slack = sum((coefficient * weights[i] for i, coefficient in row.items()), F(0))
    report.update({
        'float_slack': float(result.fun) + float(profits[source]),
        'parameters_float': [float(v) for v in result.x[:parameters_count]],
        'parameters': list(map(str, parameters)),
        'exact_slack': str(exact_slack), 'exact_slack_float': float(exact_slack),
        'accepted_negative': exact_slack < 0,
        'coefficients': [[i, str(v)] for i, v in sorted(row.items())],
    })
    return report


def select_specs(audit_paths, per_mechanism):
    by_key = {}
    for path in audit_paths:
        audit = json.loads(path.read_text())
        for record in audit['rows']:
            mechanism = record.get('mechanism', 'observed-first')
            key = (mechanism, record['actual_source_zero_based'], record['family'],
                   record.get('forced'), record['query'])
            if key not in by_key or F(record['slack']) < F(by_key[key]['seed_slack']):
                by_key[key] = {
                    'mechanism': mechanism,
                    'actual_source_zero_based': record['actual_source_zero_based'],
                    'family': record['family'], 'forced': record.get('forced'),
                    'query': record['query'], 'seed_slack': record['slack'],
                    'seed_name': record['name'],
                    'seed_parameters': record['parameters'],
                }
    selected = []
    for mechanism in ('portfolio', 'requery', 'observed-first'):
        candidates = sorted((s for s in by_key.values() if s['mechanism'] == mechanism),
                            key=lambda s: F(s['seed_slack']))
        selected.extend(candidates[:per_mechanism])
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--point', type=Path, required=True)
    parser.add_argument('--seed-audits', type=Path, nargs='+', required=True)
    parser.add_argument('--per-mechanism', type=int, default=3)
    parser.add_argument('--weight-budget', type=int, default=32)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.point.read_bytes()
    point = json.loads(raw)
    columns, hist, weights, profits, family, _ = base.topology(point)
    specs = select_specs(args.seed_audits, args.per_mechanism)
    reports = []
    for spec in specs:
        report = discover(spec, columns, hist, weights, profits, family, args.weight_budget)
        reports.append(report)
        print(json.dumps({k: v for k, v in report.items() if k != 'coefficients'}, ensure_ascii=False), flush=True)
    output = {
        'scope': 'Targeted compact-section weight discovery plus exact rational cut acceptance; no full closure claim',
        'source': str(args.point.resolve()), 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'columns': len(columns), 'LP_count': len(reports),
        'accepted_negative_count': sum(r.get('accepted_negative', False) for r in reports),
        'rows': reports,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'rows'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
