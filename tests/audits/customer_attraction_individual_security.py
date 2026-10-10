"""Definition-level exact replay of the individual mixed-security counterexample.

No equilibrium solver, optimizer, or other verifier is imported. Compressed
integer populations are expanded into distinct unit customers. The full policy,
static saddle point, uniqueness, coverage and on-path budgets are all checked.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def determinant(matrix):
    rows = [list(map(F, row)) for row in matrix]
    value = F(1)
    for column in range(len(rows)):
        pivot = next((i for i in range(column, len(rows)) if rows[i][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            rows[pivot], rows[column] = rows[column], rows[pivot]
            value = -value
        coefficient = rows[column][column]
        value *= coefficient
        rows[column] = [x / coefficient for x in rows[column]]
        for i in range(column + 1, len(rows)):
            coefficient = rows[i][column]
            rows[i] = [a - coefficient * b for a, b in zip(rows[i], rows[column])]
    return value


def run():
    input_file = ROOT / 'examples/customer_attraction/individual_security_failure.json'
    certificate_file = ROOT / 'evidence/certificates/customer_attraction/individual_security_failure.json'
    game = json.loads(input_file.read_text())
    certificate = json.loads(certificate_file.read_text())
    n, m = game['players'], len(game['topics'])
    assert (n, m) == (3, 6)
    units = []
    seen = set()
    for row in game['customers']:
        likes = frozenset(row['topics'])
        count = row['multiplicity']
        assert likes and likes not in seen and len(likes) == len(row['topics'])
        assert all(type(a) is int and 0 <= a < m for a in likes)
        assert type(count) is int and count > 0
        seen.add(likes)
        units.extend([likes] * count)
    assert len(units) == 34 and len(seen) == 13
    histories = [h for depth in range(n) for h in product(range(m), repeat=depth)]
    entries = certificate['strategy']['actions']
    policy = {tuple(row['history']): row['action'] for row in entries}
    assert len(policy) == len(entries) and set(policy) == set(histories)
    assert all(type(a) is int and 0 <= a < m for a in policy.values())

    @lru_cache(None)
    def terminal(history):
        return history if len(history) == n else terminal(history + (policy[history],))

    def utilities(profile):
        values = [F(0)] * n
        for likes in units:
            coverers = [i for i, a in enumerate(profile) if a in likes]
            for i in coverers:
                values[i] += F(1, len(coverers))
        return tuple(values)

    def coverage(profile):
        return sum(any(a in likes for a in profile) for likes in units)

    def query(a, rivals):
        return sum((F(1, 1 + sum(b in likes for b in rivals))
                    for likes in units if a in likes), F(0))

    comparisons = []
    for history in histories:
        own = utilities(terminal(history))[len(history)]
        for a in range(m):
            slack = own - utilities(terminal(history + (a,)))[len(history)]
            assert slack >= 0, (history, a, slack)
            comparisons.append((history, a, slack))
    outcome = terminal(())
    assert outcome == (0, 3, 4)
    assert certificate['strategy']['terminal_counts'] == [outcome.count(a) for a in range(m)]
    u, W = utilities(outcome), coverage(outcome)
    profiles = list(product(range(m), repeat=n))
    for profile in profiles:
        assert sum(utilities(profile)) == coverage(profile)
    O = max(map(coverage, profiles))
    assert (u, W, O) == ((F(29, 3), F(67, 6), F(67, 6)), 32, 34)
    signatures = [frozenset(i for i, likes in enumerate(units) if a in likes) for a in range(m)]
    assert len(set(signatures)) == m
    p = tuple(map(F, certificate['security']['primary']))
    Q = [(tuple(row['rivals']), F(row['probability'])) for row in certificate['security']['dual']]
    assert len(p) == m and min(p) >= 0 and sum(p) == 1
    assert all(len(B) == n - 1 and all(0 <= a < m for a in B) and q > 0 for B, q in Q)
    assert sum(q for _, q in Q) == 1
    backgrounds = list(product(range(m), repeat=n - 1))
    primary_values = [sum((p[a] * query(a, B) for a in range(m)), F(0)) for B in backgrounds]
    dual_values = [sum((q * query(a, B) for B, q in Q), F(0)) for a in range(m)]
    v = F(certificate['security']['value'])
    assert min(primary_values) == max(dual_values) == v == F(2411, 246)
    assert len(Q) == m and all(value == v for value in dual_values)
    binding_matrix = [[query(a, B) for a in range(m)] for B, _ in Q]
    det = determinant(binding_matrix)
    assert det == -F(12055, 48)
    # Positive Q-support implies every one of these constraints binds at an
    # optimal primary distribution. The invertible matrix proves uniqueness.
    assert all(sum((p[a] * row[a] for a in range(m)), F(0)) == v for row in binding_matrix)
    budget_rows = []
    for i in range(n):
        rivals = {}
        for b in range(m):
            off = terminal(outcome[:i] + (b,))
            rivals[b] = off[:i] + off[i + 1:]
        D = sum((p[a] * query(a, rivals[a]) for a in range(m)), F(0))
        C = sum((p[a] * p[b] * query(a, rivals[b]) for a in range(m) for b in range(m)), F(0))
        assert u[i] >= D
        budget_rows.append((D, C, D - C, u[i] - D))
    GB = W - sum(row[1] for row in budget_rows)
    assert GB == sum(row[2] + row[3] for row in budget_rows) == F(60, 41)
    assert budget_rows[0][:2] == (F(29, 3), v)
    assert u[0] - v == -F(11, 82) and W - n * v == F(213, 82)
    nontrivial = [s for h, a, s in comparisons if a != policy[h]]
    assert len(nontrivial) == 215 and sum(s == 0 for s in nontrivial) == 71
    result = {
        'status': 'PASS', 'unit_customers': len(units), 'customer_types': len(seen),
        'ordered_histories': len(histories), 'all_action_comparisons': len(comparisons),
        'nontrivial_deviations': len(nontrivial), 'strictly_losing_deviations': sum(s > 0 for s in nontrivial),
        'tied_deviations': sum(s == 0 for s in nontrivial), 'outcome': outcome,
        'utilities': list(map(str, u)), 'W': W, 'OPT': O, 'security_value': str(v),
        'first_player_u_minus_v': str(u[0] - v), 'W_minus_n_v': str(W - n * v),
        'half_coverage_margin': 2 * W - O, 'primary_is_unique': True,
        'binding_query_matrix_determinant': str(det),
        'onpath_D_C_kappa_slack': [list(map(str, row)) for row in budget_rows],
        'optimal_primary_GB': str(GB), 'distinct_topic_coverages': True,
        'sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (input_file, certificate_file, Path(__file__))},
        'scope': 'Exact finite full-history counterexample to individual security; aggregate BR and half coverage hold.'
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = json.dumps(run(), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(report)
    print(report, end='')
