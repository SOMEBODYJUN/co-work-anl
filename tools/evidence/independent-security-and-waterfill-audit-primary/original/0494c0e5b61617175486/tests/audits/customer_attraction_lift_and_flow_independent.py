#!/usr/bin/env python3
"""Exact auxiliary audit of tail lifting and flow-template witnesses.

No repository module, strategy file, solver, or verifier is imported.
The numeric 15-type witness is transcribed as data; all vectors and operations
are rebuilt from player-index allocations and enumerated iid terminal profiles.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def lift_pointwise_checks():
    count = 0
    for n in range(4, 11):
        for d in range(n + 1):
            for b in range(n - 3):
                enumerate_sum = F(0)
                for I in combinations(range(n), 4):
                    j = sum(i < d for i in I)
                    enumerate_sum += F(j, b + j) if j else 0
                hypergeometric_sum = sum(
                    (choose(d, j) * choose(n - d, 4 - j) * F(j, b + j)
                     for j in range(1, 5)), F(0))
                assert enumerate_sum == hypergeometric_sum
                if d:
                    assert hypergeometric_sum >= F(choose(n - 1, 3), b + 1)
                count += 1
    beta = F(1499, 750)
    for n in range(4, 101):
        w_coeff = beta * n / 4
        k_coeff = (n - 4) * (F(1, 2) - beta / 4)
        assert k_coeff >= 0
        assert w_coeff + k_coeff == F(n, 2) - F(1, 750)
    return count


def formal_policy(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    candidates = [0, 1, 2] if h[1] < 3 else [3, 4, 5]
    return min(a for a in candidates if a not in h)


def finish(h, policy, n):
    z = tuple(h)
    while len(z) < n:
        z += (policy(z),)
    return z


def allocated(weights, z):
    payments = [F(0) for _ in z]
    W = 0
    Phi = F(0)
    for mask, weight in weights.items():
        serving = [i for i, a in enumerate(z) if mask & (1 << a)]
        load = len(serving)
        if load:
            W += weight
            for i in serving:
                payments[i] += F(weight, load)
            Phi += weight * sum((F(1, j) for j in range(1, load + 1)), F(0))
    assert sum(payments) == W
    return payments, F(W), Phi


def profile_probability(z, q):
    probability = F(1)
    for a in z:
        probability *= q[a]
    return probability


def independent_flow_audit(weights, policy, q, n):
    m = len(q)
    assert all(v >= 0 for v in q) and sum(q) == 1
    actual = finish((), policy, n)
    actual_u, W, _ = allocated(weights, actual)
    psi = sum((profile_probability(z, q) * allocated(weights, z)[1]
               for z in product(range(m), repeat=n)), F(0))
    alpha = []
    for a in range(m):
        alpha.append(sum((profile_probability(B, q) * allocated(weights, (a,) + B)[0][0]
                          for B in product(range(m), repeat=n - 1)), F(0)))
    E = [psi - n * v for v in alpha]
    assert sum(q[a] * E[a] for a in range(m)) == 0
    nodes, all_gammas, levels, deltas = [], [], [], []
    for depth in range(n):
        level = F(0)
        delta_row = [F(0) for _ in range(n)]
        for h in product(range(m), repeat=depth):
            before = finish(h, policy, n)
            before_u, _, before_phi = allocated(weights, before)
            node_average = F(0)
            gamma_row = []
            for a in range(m):
                after = finish(h + (a,), policy, n)
                after_u, _, after_phi = allocated(weights, after)
                gamma = before_u[depth] - after_u[depth]
                before_deleted = before[:depth] + before[depth + 1:]
                after_deleted = after[:depth] + after[depth + 1:]
                removal_before = before_phi - allocated(weights, before_deleted)[2]
                removal_after = after_phi - allocated(weights, after_deleted)[2]
                assert gamma == removal_before - removal_after
                gamma_row.append(gamma)
                all_gammas.append((h, a, gamma))
                node_average += q[a] * gamma
                coupling_prob = profile_probability(h, q) * q[a]
                for i in range(n):
                    delta_row[i] += coupling_prob * (
                        allocated(weights, before[:i] + before[i + 1:])[2]
                        - allocated(weights, after[:i] + after[i + 1:])[2])
            nodes.append({'history': h, 'Gamma_values': gamma_row, 'M_q': node_average})
            level += profile_probability(h, q) * node_average
        levels.append(level)
        deltas.append(delta_row)
    remainder = sum((n * deltas[k][k] - sum(deltas[k]) for k in range(n)), F(0))
    assert W - psi == n * sum(levels) + remainder
    for z in product(range(m), repeat=n):
        _, wz, phiz = allocated(weights, z)
        deleted_sum = sum((allocated(weights, z[:i] + z[i + 1:])[2] for i in range(n)), F(0))
        assert wz == n * phiz - deleted_sum
    negative = [(h, a, v) for h, a, v in all_gammas if v < 0]
    return {'actual_profile': actual, 'actual_payoffs': actual_u, 'W': W,
            'Psi': psi, 'W_minus_Psi': W - psi, 'E': E, 'G_levels': levels,
            'unit_flow_remainder': W - psi - sum(levels),
            'harmonic_flow_remainder': remainder, 'Delta_rows': deltas,
            'node_count': len(nodes), 'node_average_min': min(row['M_q'] for row in nodes),
            'node_average_zero_count': sum(row['M_q'] == 0 for row in nodes),
            'negative_full_Gamma_count': len(negative), 'negative_full_Gamma_rows': negative,
            'all_nodes': nodes, 'total_mass': sum(weights.values())}


def plain(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def main():
    lift_checks = lift_pointwise_checks()
    original = {(1 << a) | (1 << b): 1 for a in range(3) for b in range(3, 6)}
    for aa in combinations(range(3), 2):
        for bb in combinations(range(3, 6), 2):
            original[sum(1 << a for a in aa + bb)] = 3
    depth_separator = {4: 11988, 25: 17316, 26: 12481, 29: 7312, 34: 19357, 37: 12481}
    node_separator = {
        2: 4452686231690, 4: 6839265002855, 6: 12413611540204,
        18: 2005873636422, 21: 55545726786729, 26: 11682751932414,
        30: 144170590014021, 31: 453930615027141, 32: 252949420150890,
        33: 5430105756036, 41: 4622970055818, 43: 77652459511935,
        45: 70066680831603, 49: 29955175098349, 51: 46800753774087,
    }
    q = [F(1, 6)] * 6
    original_audit = independent_flow_audit(original, formal_policy, q, 3)
    depth_audit = independent_flow_audit(depth_separator, formal_policy, q, 3)
    node_audit = independent_flow_audit(node_separator, formal_policy, q, 3)
    assert original_audit['negative_full_Gamma_count'] == 0
    assert original_audit['W'] == 34 and original_audit['Psi'] == F(97, 3)
    assert original_audit['E'] == [0] * 6
    assert original_audit['G_levels'] == [F(0), F(1, 2), F(31, 18)]
    assert original_audit['unit_flow_remainder'] == -F(5, 9)
    assert original_audit['harmonic_flow_remainder'] == -5
    assert depth_audit['E'] == [0] * 6
    assert depth_audit['G_levels'] == [F(0), F(0), F(607489, 216)]
    assert depth_audit['W_minus_Psi'] == -F(472195, 36)
    assert depth_audit['negative_full_Gamma_count'] == 57
    assert next(v for h, a, v in depth_audit['negative_full_Gamma_rows'] if h == () and a == 1) == -2827
    assert next(v for h, a, v in depth_audit['negative_full_Gamma_rows'] if h == () and a == 2) == -6216
    assert len(node_separator) == 15
    assert node_audit['node_count'] == 43 and node_audit['node_average_min'] == 0
    assert node_audit['E'] == [0] * 6
    assert node_audit['W_minus_Psi'] == -F(1085816540911589, 12)
    assert node_audit['negative_full_Gamma_count'] > 0
    # A nonuniform q and n=4: identities hold for arbitrary complete policies,
    # even when the strategy is not SPE and G has no required sign.
    def extra_policy(h):
        return (sum((i + 1) * a for i, a in enumerate(h)) + len(h)) % 2
    nonuniform_audit = independent_flow_audit({1: 2, 2: 3, 3: 5}, extra_policy, [F(1, 3), F(2, 3)], 4)
    output = {'lift_pointwise_enumeration_checks': lift_checks,
              'original_36': original_audit, 'depth_separator': depth_audit,
              'node_separator_weights': node_separator, 'node_separator': node_audit,
              'nonuniform_n4_identity_check': nonuniform_audit}
    print(json.dumps(plain({
        'lift_pointwise_enumeration_checks': lift_checks,
        'original_36': {k: original_audit[k] for k in ['W', 'Psi', 'G_levels', 'unit_flow_remainder', 'harmonic_flow_remainder']},
        'depth_separator': {k: depth_audit[k] for k in ['total_mass', 'G_levels', 'W_minus_Psi', 'negative_full_Gamma_count']},
        'node_separator': {k: node_audit[k] for k in ['total_mass', 'node_count', 'node_average_min', 'node_average_zero_count', 'W', 'Psi', 'W_minus_Psi', 'negative_full_Gamma_count']},
        'generic_nonuniform_n4_identity': True,
    }), indent=2))


if __name__ == '__main__':
    main()
