"""Independent exact audits for full-tree flow obstructions.

No repository solver, verifier, numerical optimizer, or saved policy is imported.
All strategy continuation, payoff and incentive rows are rebuilt here.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json


def policy36(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[-1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def leaf(h, policy, n):
    h = tuple(h)
    while len(h) < n:
        h += (policy(h),)
    return h


def utility(weights, a, z):
    return sum((F(v, sum(t >> b & 1 for b in z))
                for t, v in weights.items() if t >> a & 1), F(0))


def welfare(weights, z):
    return sum(v for t, v in weights.items() if any(t >> a & 1 for a in z))


def potential(weights, z):
    return sum((v * sum((F(1, j) for j in
                        range(1, sum(t >> a & 1 for a in z) + 1)), F(0))
                for t, v in weights.items()), F(0))


def static_uniform_ne_rows(weights, m, n):
    psi = sum((v * (1 - (1 - F(t.bit_count(), m)) ** n)
               for t, v in weights.items()), F(0))
    alpha = [sum((v * sum(((1 - F(t.bit_count(), m)) ** j
                           for j in range(n)), F(0)) / n
                  for t, v in weights.items() if t >> a & 1), F(0))
             for a in range(m)]
    return psi, [psi - n * x for x in alpha]


def full_rows(weights, policy, m, n):
    rows = []
    for k in range(n):
        for h in product(range(m), repeat=k):
            z = leaf(h, policy, n)
            a0 = policy(h)
            for a in range(m):
                value = utility(weights, a0, z) - utility(
                    weights, a, leaf(h + (a,), policy, n))
                rows.append((h, a0, a, value))
    return rows


def iid_prefix_rows(weights, policy, m, n):
    levels = []
    for k in range(1, n + 1):
        level = F(0)
        for h in product(range(m), repeat=k - 1):
            z = leaf(h, policy, n)
            for a in range(m):
                level += (utility(weights, policy(h), z) - utility(
                    weights, a, leaf(h + (a,), policy, n))) / m ** k
        levels.append(level)
    return levels


def audit_hybrid_identity(weights, policy, m, n):
    """Check W-Psi = n sum(G_k) + sum((n-1)Delta_k-sum_i!=k Delta_i)."""
    z0 = leaf((), policy, n)
    remainder = F(0)
    for k in range(1, n + 1):
        deltas = [F(0)] * n
        for h in product(range(m), repeat=k - 1):
            before = leaf(h, policy, n)
            for a in range(m):
                after = leaf(h + (a,), policy, n)
                for i in range(n):
                    deltas[i] += (potential(weights, before[:i] + before[i+1:])
                                  - potential(weights, after[:i] + after[i+1:])) / m ** k
        remainder += n * deltas[k-1] - sum(deltas)
    psi, _ = static_uniform_ne_rows(weights, m, n)
    levels = iid_prefix_rows(weights, policy, m, n)
    assert welfare(weights, z0) - psi == n * sum(levels) + remainder
    return remainder


def main():
    original = {}
    for a in range(3):
        for b in range(3, 6):
            original[(1 << a) | (1 << b)] = 1
    for aa in combinations(range(3), 2):
        for bb in combinations(range(3, 6), 2):
            original[sum(1 << a for a in aa + bb)] = 3
    z = leaf((), policy36, 3)
    rows = full_rows(original, policy36, 6, 3)
    assert len(rows) == 258 and min(v for *_, v in rows) == 0
    psi, ne = static_uniform_ne_rows(original, 6, 3)
    levels = iid_prefix_rows(original, policy36, 6, 3)
    assert z == (0, 3, 4)
    assert welfare(original, z) == 34 and psi == F(97, 3)
    assert ne == [0] * 6
    assert levels == [F(0), F(1, 2), F(31, 18)]
    remainder = audit_hybrid_identity(original, policy36, 6, 3)
    assert remainder == -5
    assert welfare(original, z) - psi - sum(levels) == -F(5, 9)

    separator = {4: 11988, 25: 17316, 26: 12481,
                 29: 7312, 34: 19357, 37: 12481}
    psi2, ne2 = static_uniform_ne_rows(separator, 6, 3)
    levels2 = iid_prefix_rows(separator, policy36, 6, 3)
    assert sum(separator.values()) == 80935
    assert ne2 == [0] * 6
    assert levels2 == [F(0), F(0), F(607489, 216)]
    assert welfare(separator, z) - psi2 == -F(472195, 36)
    rows2 = full_rows(separator, policy36, 6, 3)
    bad = [(h, a0, a, v) for h, a0, a, v in rows2 if v < 0]
    assert len(bad) == 57
    assert next(v for h, _, a, v in rows2 if h == () and a == 1) == -2827
    assert next(v for h, _, a, v in rows2 if h == () and a == 2) == -6216
    audit_hybrid_identity(separator, policy36, 6, 3)

    # Node weights cannot replace deviation-specific multipliers.
    node_separator = {
        2: 4452686231690, 4: 6839265002855, 6: 12413611540204,
        18: 2005873636422, 21: 55545726786729, 26: 11682751932414,
        30: 144170590014021, 31: 453930615027141, 32: 252949420150890,
        33: 5430105756036, 41: 4622970055818, 43: 77652459511935,
        45: 70066680831603, 49: 29955175098349, 51: 46800753774087,
    }
    psi4, ne4 = static_uniform_ne_rows(node_separator, 6, 3)
    rows4 = full_rows(node_separator, policy36, 6, 3)
    node_values = {}
    for h, _, _, value in rows4:
        node_values[h] = node_values.get(h, F(0)) + value / 6
    assert len(node_values) == 43 and min(node_values.values()) == 0
    assert ne4 == [0] * 6
    assert welfare(node_separator, z) - psi4 == -F(1085816540911589, 12)
    assert any(value < 0 for *_, value in rows4)

    # Actual-terminal uniform deletion cannot universally certify aggregate BR.
    small = {2: 1, 5: 2, 6: 2}
    def policy2(h):
        return 0 if not h else (1 if h[0] == 0 else 2)
    zz = leaf((), policy2, 2)
    rows3 = full_rows(small, policy2, 3, 2)
    assert min(v for *_, v in rows3) == 0
    assert zz == (0, 1) and welfare(small, zz) == 5
    assert [utility(small, a, zz) for a in zz] == [2, 3]
    deleted_query = (utility(small, 2, (2, zz[0]))
                     + utility(small, 2, (2, zz[1]))) / 2
    assert deleted_query == 3 > F(5, 2)
    # Static security has matching pure row and pure column certificates v2=2.
    assert min(utility(small, 2, (2, b)) for b in range(3)) == 2
    assert max(utility(small, a, (a, 2)) for a in range(3)) == 2
    frozen_phi = (potential(small, (2, zz[1]))
                  + potential(small, (zz[0], 2))) / 2
    assert 5 - 2 * deleted_query == 2 * (potential(small, zz) - frozen_phi) == -1
    print(json.dumps({
        "exact": True,
        "original36": {"full_comparisons": len(rows), "W": "34",
                       "Psi": str(psi), "G_levels": list(map(str, levels)),
                       "unit_flow_remainder": "-5/9",
                       "harmonic_flow_remainder": str(remainder)},
        "depth_only_separator": {"weights": separator,
                       "static_ne_rows": list(map(str, ne2)),
                       "G_levels": list(map(str, levels2)),
                       "W_minus_Psi": str(welfare(separator, z) - psi2),
                       "full_strategy_is_SPE": False, "negative_full_rows": len(bad)},
        "node_averaged_separator": {"weights": node_separator,
                       "node_count": len(node_values),
                       "minimum_averaged_node_row": str(min(node_values.values())),
                       "static_ne_rows": list(map(str, ne4)),
                       "W_minus_Psi": str(welfare(node_separator, z) - psi4),
                       "full_strategy_is_SPE": False},
        "terminal_deletion_obstruction": {"weights": small, "W": "5",
                       "v2": "2", "deleted_query_C": str(deleted_query)}
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
