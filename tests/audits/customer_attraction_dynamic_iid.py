#!/usr/bin/env python3
"""Exact audit of the dynamic iid debt interface and actual-prefix failure.

The full strategy is read from its certificate; no construction or canonical
solver/verifier is imported. The general proof is in the current mathematical
page. Scalar polynomial checks here are finite implementation audits.
"""
import argparse
from fractions import Fraction as F
from itertools import product
from math import comb, lcm
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def bernstein_polynomial(values):
    degree = len(values) - 1
    coefficients = [F(0)] * (degree + 1)
    for j, value in enumerate(values):
        for k in range(degree - j + 1):
            coefficients[j + k] += value * comb(degree, j) * comb(degree - j, k) * (-1) ** k
    return coefficients


def derivative(coefficients):
    return [i * coefficients[i] for i in range(1, len(coefficients))]


def formula_audit():
    checks = 0
    for r in range(1, 8):
        for p in range(8):
            harmonic = [sum((F(1, p + j) for j in range(1, k + 1)), F(0)) for k in range(r + 1)]
            f = bernstein_polynomial(harmonic)
            g = bernstein_polynomial([F(1, p + 1 + k) for k in range(r)])
            assert derivative(f) == [r * x for x in g]
            if r >= 2:
                curvature = bernstein_polynomial([
                    F(-r * (r - 1), (p + 1 + k) * (p + 2 + k))
                    for k in range(r - 1)
                ])
                assert derivative(derivative(f)) == curvature
            for t in (F(0), F(1, 7), F(1, 2), F(1)):
                expected = sum((F(comb(r, k)) * t ** k * (1 - t) ** (r - k) * F(k, p + k)
                                for k in range(1, r + 1)), F(0))
                scaled = r * t * sum((F(comb(r - 1, k)) * t ** k * (1 - t) ** (r - 1 - k)
                                      / (p + 1 + k) for k in range(r)), F(0))
                assert expected == scaled
            checks += 1
    return checks


def audit(input_path, certificate_path):
    game_raw = input_path.read_bytes()
    certificate_raw = certificate_path.read_bytes()
    game = json.loads(game_raw)
    data = json.loads(certificate_raw)
    n = game['players']
    m = len(game['topics'])
    assert type(n) is int and n == 5 and m == 7
    assert len(set(game['topics'])) == m
    weights = {}
    for row in game['customers']:
        labels = row['topics']
        weight = row['multiplicity']
        assert labels and len(set(labels)) == len(labels)
        assert all(type(a) is int and 0 <= a < m for a in labels)
        assert type(weight) is int and weight > 0
        mask = sum(1 << a for a in labels)
        assert mask not in weights
        weights[mask] = weight
    assert len(weights) == 19 and sum(weights.values()) == 60
    policy = {}
    for row in data['certificate']['actions']:
        h = tuple(row['history'])
        a = row['action']
        assert len(h) < n and all(type(b) is int and 0 <= b < m for b in h)
        assert type(a) is int and 0 <= a < m and h not in policy
        policy[h] = a
    histories = {h for k in range(n) for h in product(range(m), repeat=k)}
    assert set(policy) == histories and len(policy) == 2801
    scale = lcm(*range(1, n + 1))

    def terminal(h):
        while len(h) < n:
            h += (policy[h],)
        return h

    def payoff(z, i):
        return sum(weight * (scale // sum(T >> a & 1 for a in z))
                   for T, weight in weights.items() if T >> z[i] & 1)

    checks = ties = strict = 0
    for h in histories:
        z = terminal(h)
        i = len(h)
        for a in range(m):
            slack = payoff(z, i) - payoff(terminal(h + (a,)), i)
            assert slack >= 0, (h, a, slack)
            checks += 1
            ties += slack == 0
            strict += slack > 0
    z = terminal(())
    u = [F(payoff(z, i), scale) for i in range(n)]
    assert z == (6, 6, 0, 3, 4) and list(z) == data['root']
    assert u == [F(12), F(12), F(10), F(12), F(12)]
    assert list(map(str, u)) == data['root_payoffs']
    counts = [z.count(a) for a in range(m)]
    assert counts == data['certificate']['terminal_counts']
    welfare = sum(weight for T, weight in weights.items() if any(T >> a & 1 for a in z))
    assert welfare == sum(u) == 58
    optimal_profile = (6, 0, 1, 2, 6)
    assert all(any(T >> a & 1 for a in optimal_profile) for T in weights)

    def residual_ne(prefix, q):
        r = n - len(prefix)
        assert len(q) == m and all(x >= 0 for x in q) and sum(q) == 1
        alpha = []
        for a in range(m):
            value = F(0)
            for T, weight in weights.items():
                if not T >> a & 1:
                    continue
                p = sum(T >> b & 1 for b in prefix)
                t = sum(q[b] for b in range(m) if T >> b & 1)
                g = sum((F(comb(r - 1, k)) * t ** k * (1 - t) ** (r - 1 - k)
                         / (p + 1 + k) for k in range(r)), F(0))
                value += weight * g
            alpha.append(value)
        v = sum(q[a] * alpha[a] for a in range(m))
        assert all(x <= v for x in alpha)
        assert all(not q[a] or alpha[a] == v for a in range(m))
        Z = r * v
        rent = coverage = F(0)
        for T, weight in weights.items():
            p = sum(T >> a & 1 for a in prefix)
            t = sum(q[a] for a in range(m) if T >> a & 1)
            if p:
                rent += weight * sum((F(comb(r, k)) * t ** k * (1 - t) ** (r - k)
                                      * F(p, p + k) for k in range(r + 1)), F(0))
                coverage += weight
            else:
                coverage += weight * (1 - (1 - t) ** r)
        assert coverage == rent + Z
        return Z, rent, coverage, alpha

    states = []
    for row in data['dynamic_iid_states']:
        h = tuple(row['history'])
        values = residual_ne(h, list(map(F, row['q'])))
        assert values[:3] == tuple(F(row[key]) for key in ('Z', 'prefix_rent', 'complete_expected_coverage'))
        states.append({'history': list(h), 'Z': str(values[0]), 'prefix_rent': str(values[1]),
                       'complete_expected_coverage': str(values[2]), 'alpha': list(map(str, values[3]))})
    assert [row['Z'] for row in states] == ['97/3', '21', '12']
    debt = [F(97, 3) - 21 - u[2], F(21) - 12 - u[3], F(12) - u[4]]
    assert debt == [F(4, 3), F(-3), F(0)] and sum(debt) == F(97, 3) - sum(u[2:])
    local_deficit = F(9, 10) * (F(97, 3) - 21) - u[2]
    assert local_deficit == F(data['weak_local_deficit']) == F(1, 5) > 0
    # The whole root benchmark is not computed. The optimal-cover upper bound suffices.
    assert data['root_Z_exactly_computed'] is False and F(data['root_Z_upper_bound']) == 60
    global_slack_lower_bound = F(welfare) - F(9, 10) * 60
    assert global_slack_lower_bound == 4
    return {
        'claims': ['CA-DYNAMIC-IID-DEBT-INTERFACE', 'CA-WEAK-LOCAL-IID-DRIFT-NO'],
        'input_sha256': hashlib.sha256(game_raw).hexdigest(),
        'certificate_sha256': hashlib.sha256(certificate_raw).hexdigest(),
        'full_ordered_history_pure_SPE': True,
        'checked_histories': len(histories), 'checked_action_comparisons': checks,
        'ties_including_selected_actions': ties, 'strict_comparisons': strict,
        'root': list(z), 'root_payoffs': list(map(str, u)), 'W': welfare, 'OPT_5': 60,
        'residual_states': states, 'old_tail_debts': list(map(str, debt)),
        'old_tail_total_debt': str(sum(debt)), 'weak_actual_node_deficit': str(local_deficit),
        'root_Z_exactly_computed': False, 'root_Z_upper_bound': '60',
        'global_weak_bridge_slack_lower_bound': str(global_slack_lower_bound),
        'scalar_polynomial_audit_cases': formula_audit(),
        'unrestricted_global_iid_bridge_proved': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'examples/customer_attraction/dynamic_iid_local.json')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'evidence/certificates/customer_attraction/dynamic_iid_local.json')
    parser.add_argument('--output', type=Path, help='create a new JSON report; existing files are never overwritten')
    args = parser.parse_args()
    rendered = json.dumps(audit(args.input, args.certificate), indent=2) + '\n'
    if args.output:
        try:
            with args.output.open('x', encoding='utf-8') as handle:
                handle.write(rendered)
        except FileExistsError:
            parser.error(f'Refusing to overwrite existing output: {args.output}')
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
