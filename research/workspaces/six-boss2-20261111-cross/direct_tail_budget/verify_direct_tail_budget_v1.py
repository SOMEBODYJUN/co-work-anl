#!/usr/bin/env python3
"""Small rational identity audit only; no game search, LP, MILP, or grids.

Contract is frozen in ../direct_tail_budget.md.  The 84 canonical six-index
four-state count vectors cover every (n,m,k) incidence statistic.  Polynomial
coefficient comparisons, rather than parameter sampling, verify the complete
eta/gamma identities.  A single fixed candidate checks the endpoint formula.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


def phi(p, a, n, eta):
    return min(F(n, p + 1), F(n, p + 2) + eta / (p + a + 1))


def psi(p, a, n, eta, gamma):
    c, d = p + 1, p + a + 1
    delta = F(1, c * (c + 1))
    base = (1 + gamma) * n / c - gamma * delta * n * n / 6
    return base - max(F(0), (1 - gamma) * delta * n + 6 * gamma / c - eta / d)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


counts = []
for c00 in range(7):
    for c01 in range(7 - c00):
        for c10 in range(7 - c00 - c01):
            c11 = 6 - c00 - c01 - c10
            counts.append((c00, c01, c10, c11))
assert len(counts) == 84

identity_cases = 0
cycle_cases = 0
for hist in counts:
    pairs = sum(([pair] * number for pair, number in zip(product((0, 1), repeat=2), hist)), [])
    ts, ss = zip(*pairs)
    n, m, k = sum(ts), sum(ss), sum(t * s for t, s in pairs)
    for p, a, b in product(range(5), (0, 1), (0, 1)):
        c, d = p + 1, p + a + 1
        delta = F(1, c * (c + 1))
        alpha = F(a, p + a + b) if a else F(0)
        beta = F(b, p + a + b) if b else F(0)
        direct = 6 * alpha - sum(F(t, c + s) for t, s in pairs)
        actual_price = 6 * beta - sum(F(s, d) for s in ss)
        lij = [[F(ss[i] - ss[j], c + ts[i]) for j in range(6)] for i in range(6)]
        cross = sum(sum(row) for row in lij)
        known = sum(F(6 * ss[i] - n, c + ts[i]) for i in range(6))
        assert direct == 6 * alpha - F(n, c) + delta * k
        assert actual_price == 6 * beta - F(m, d)
        assert cross == delta * (n * m - 6 * k)
        assert known == F(6 * (m - n), c) + delta * (n * n - 6 * k)
        assert cross == sum(lij[i][j] + lij[j][i] for i in range(6) for j in range(i + 1, 6))

        # Every offset is a fixed permutation; offsets together form a
        # one-factorization, so their average also equals all-permutation average.
        cycles = []
        for offset in range(6):
            literal = sum(lij[i][(i + offset) % 6] for i in range(6))
            formula = delta * sum(ts[i] * (ss[(i + offset) % 6] - ss[i]) for i in range(6))
            assert literal == formula
            cycles.append(literal)
            cycle_cases += 1
        assert sum(cycles) / 6 == cross / 6

        # Coefficients of (1, eta, gamma) in the entire true-row combination.
        primitive_poly = (direct + cross / 6, actual_price / 6, (known - cross) / 6)
        formula_poly = (
            6 * alpha - F(n, c) + F(m, 6) * delta * n,
            beta - F(m, 6 * d),
            -F(n, c) + delta * n * n / 6 + F(m, 6) * (F(6, c) - delta * n),
        )
        assert primitive_poly == formula_poly
        identity_cases += 1

eta0, gamma = F(1), F(1, 7)
eta = (1 - gamma) * eta0 + 6 * gamma
min_cases = 0
credit_cases = 0
positive_credit = []
for p, a, n in product(range(5), (0, 1), range(7)):
    c, d = p + 1, p + a + 1
    delta = F(1, c * (c + 1))
    old_costs = [F(n, c) + F(m, 6) * (eta0 / d - n * delta) for m in range(7)]
    joint_costs = [(1 + gamma) * n / c - gamma * delta * n * n / 6
                   + F(m, 6) * (eta / d - (1 - gamma) * delta * n - 6 * gamma / c)
                   for m in range(7)]
    assert min(old_costs) == phi(p, a, n, eta0)
    assert min(joint_costs) == psi(p, a, n, eta, gamma)
    assert min(old_costs) == min(old_costs[0], old_costs[-1])
    assert min(joint_costs) == min(joint_costs[0], joint_costs[-1])
    assert psi(p, a, n, F(6), F(1)) == F(2 * n, c) - delta * n * n / 6 - 6 * a * delta
    credit = min((1 - gamma) * max(F(0), eta0 / d - n * delta), 6 * gamma * a * delta)
    separate = (1 - gamma) * phi(p, a, n, eta0) + gamma * psi(p, a, n, F(6), F(1))
    assert psi(p, a, n, eta, gamma) == separate + credit
    if credit:
        positive_credit.append({'P': p, 'a': a, 'n': n, 'credit': credit})
    min_cases += 2
    credit_cases += 1

breaks = sorted({F(0)} | {F(n * (p + a + 1), (p + 1) * (p + 2))
                            for p, a, n in product(range(5), (0, 1), range(1, 7))})
assert breaks == sorted({F(0)} | {F(r, q) for r, q in product(range(1, 7), repeat=2)})
assert len(breaks) == 24
breaks_one = sorted({F(0)} | {F(p + a + 1, (p + 1) * (p + 2))
                                for p, a in product(range(5), (0, 1))})
assert breaks_one == [F(0), F(1, 6), F(1, 5), F(1, 4), F(1, 3), F(1, 2), F(1)]

example = {
    'P': 1, 'a': 1, 'n': 1, 'eta0': eta0, 'gamma': gamma, 'eta': eta,
    'old': phi(1, 1, 1, eta0), 'pair': psi(1, 1, 1, F(6), F(1)),
    'joint': psi(1, 1, 1, eta, gamma),
}
example['separate'] = (1 - gamma) * example['old'] + gamma * example['pair']
example['credit'] = example['joint'] - example['separate']
assert example['joint'] == F(143, 252)
assert example['separate'] == F(107, 252)
assert example['credit'] == F(1, 7)

sources = [
    'archives/customer-attraction/state/引理/真实末两人菜单交集消去--引理.md',
    'archives/customer-attraction/state/定理/真实末两人加权分数价格包络--定理.md',
    'archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md',
    'archives/customer-attraction/subarchives/six-providers/state/引理/共同四态的双向精确运输与三节点循环障碍--引理.md',
]
report = {
    'status': 'PASS',
    'scope': 'Pointwise rational identities and a fixed candidate; no finite-cone irredundancy or SPE existence claim.',
    'solvers_run': 0,
    'parameter_grids_run': 0,
    'master_points_read': 0,
    'canonical_six_index_counts': len(counts),
    'identity_cases': identity_cases,
    'literal_cycle_cases': cycle_cases,
    'fixed_endpoint_min_cases': min_cases,
    'fixed_credit_identity_cases': credit_cases,
    'breakpoints_full_n': breaks,
    'breakpoints_n_0_or_1': breaks_one,
    'strict_pointwise_example': example,
    'fixed_positive_credit_types': positive_credit,
    'source_sha256': {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest() for name in sources},
}
output = ROOT / 'verify_direct_tail_budget_v1.json'
output.write_text(json.dumps(encode(report), ensure_ascii=False, indent=2) + '\n')
print(json.dumps(encode({key: report[key] for key in (
    'status', 'identity_cases', 'literal_cycle_cases', 'fixed_endpoint_min_cases',
    'fixed_credit_identity_cases', 'strict_pointwise_example')}), ensure_ascii=False, indent=2))
