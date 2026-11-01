"""Independent Fraction reconstruction from query-payoff definitions, no source import or optimizer."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import time

BASE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def recover(equations, rhs, width):
    a = [[F(z) for z in row] + [F(b)] for row, b in zip(equations, rhs)]
    pivot, rank = [], 0
    for j in range(width):
        k = next((k for k in range(rank, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[rank], a[k] = a[k], a[rank]
        div = a[rank][j]
        a[rank] = [z / div for z in a[rank]]
        for k in range(len(a)):
            if k != rank and a[k][j]:
                mul = a[k][j]
                a[k] = [z - mul * t for z, t in zip(a[k], a[rank])]
        pivot.append(j)
        rank += 1
    assert all(any(row[:-1]) or not row[-1] for row in a), 'inconsistent exact support'
    assert rank == width, (rank, width)
    result = [F(0)] * width
    for k, j in enumerate(pivot):
        result[j] = a[k][-1]
    assert all(sum(v * z for v, z in zip(row, result)) == F(b) for row, b in zip(equations, rhs))
    return result

def defined_row(m, e, d, ell, tag):
    c = sum(e)
    u = [F(v, c) if c else F(0) for v in e]
    p, a, b = sum(e[:-2]), e[-2], e[-1]
    # Arbitrary matching realizes the recorded d and ell; its intersection cancels.
    t, r = [int(i < d) for i in range(m)], [int(i < ell) for i in range(m)]
    S = sum((u[-2] - F(t[i], p + 1 + r[i]) for i in range(m)), F(0))
    Z = sum((u[-1] - F(r[i], p + a + 1) for i in range(m)), F(0))
    V = sum((F(r[i] - r[j], p + 1 + t[i]) for i in range(m) for j in range(m) if i != j), F(0))
    G = S + Z / (2 * m) + V / m
    if tag == 'prefix':
        den = [sum(e[:i]) + m - i for i in range(m)]
        actual = [u[i] - F(e[j], den[i]) for i in range(m) for j in range(m)]
        cmp = [sum((u[i] - F(tj, den[i]) for tj in t), F(0)) / m for i in range(m)]
        reply = [sum((u[i] - F(rj, den[i]) for rj in r), F(0)) / m for i in range(m)]
        return [G] + actual + cmp + reply
    early = list(range(m - 2))
    P = sum(u[:-2], F(0))
    return [G,
            sum((u[i] - F(a, m) for i in early), F(0)),
            sum((u[-1] - F(e[i], p + a + 1) for i in early), F(0)),
            sum((u[-1] - F(tj, p + a + 1) for tj in t), F(0)),
            sum((u[-1] - F(rj, p + a + 1) for rj in r), F(0)),
            sum((u[i] - F(b, m) for i in early), F(0)),
            sum((u[i] - F(tj, m) for i in early for tj in t), F(0)) / m,
            sum((u[i] - F(rj, m) for i in early for rj in r), F(0)) / m,
            sum((u[-2] - F(e[i], p + 2) for i in early), F(0)),
            u[-2] - F(b, p + 2),
            sum((u[-2] - F(tj, p + 2) for tj in t), F(0)),
            sum((u[-2] - F(rj, p + 2) for rj in r), F(0))]

def check(cap):
    tag, m = cap['tag'], cap['m']
    assert m == 4
    expected = list(product(range(m - 1), range(2), range(2), range(m + 1), range(m + 1))) if tag == 'aggregate' else list(product(range(1 << m), range(m + 1), range(m + 1)))
    assert [list(x) for x in expected] == cap['cols']
    X, w, o = [], [], []
    for co in expected:
        if tag == 'aggregate':
            p, a, b, d, ell = co
            e = [1] * p + [0] * (m - 2 - p) + [a, b]
        else:
            mask, d, ell = co
            e = [(mask >> i) & 1 for i in range(m)]
        X.append(defined_row(m, e, d, ell, tag))
        w.append(int(any(e))); o.append(int(d > 0))
    assert w == cap['w'] and o == cap['o']
    errors = [abs(float(v) - old) for row, oldrow in zip(X, cap['X']) for v, old in zip(row, oldrow)]
    assert max(errors) < 2e-15
    A = [row + [F(-wi)] for row, wi in zip(X, w)]
    assert max(abs(float(v) - old) for row, oldrow in zip(A, cap['A']) for v, old in zip(row, oldrow)) < 2e-15
    assert cap['c'] == [0] * len(X[0]) + [1]
    res = cap['res']
    assert res['success'] and res['status'] == 0
    positive = [i for i, v in enumerate(res['x']) if v > 1e-8]
    active = [j for j, v in enumerate(res['ineqlin']['residual']) if abs(v) < 1e-7]
    recovered = recover([[A[j][i] for i in positive] for j in active], [-o[j] for j in active], len(positive))
    dual = [F(0)] * len(A[0])
    for i, v in zip(positive, recovered):
        dual[i] = v
    assert all(v >= 0 for v in dual)
    residual = [-oi - sum(v * z for v, z in zip(row, dual)) for oi, row in zip(o, A)]
    assert min(residual) >= 0
    support = [j for j, v in enumerate(res['ineqlin']['marginals']) if -v > 1e-8]
    active_primal_rows = [i for i in range(len(X[0])) if abs(res['lower']['marginals'][i]) < 1e-7]
    equations = [[X[j][i] for j in support] for i in active_primal_rows] + [[F(w[j]) for j in support]]
    weights = recover(equations, [F(0)] * len(active_primal_rows) + [F(1)], len(support))
    assert all(v >= 0 for v in weights)
    slack = [sum((mass * X[j][i] for j, mass in zip(support, weights)), F(0)) for i in range(len(X[0]))]
    W = sum((mass * w[j] for j, mass in zip(support, weights)), F(0))
    O = sum((mass * o[j] for j, mass in zip(support, weights)), F(0))
    assert min(slack) >= 0 and W == 1 and O == dual[-1]
    assert all(mass * residual[j] == 0 for j, mass in zip(support, weights))
    assert all(lam * value == 0 for lam, value in zip(dual[:-1], slack))
    names = cap.get('names', ['G', 'early_to_A', 'B_to_early', 'B_to_cmp', 'B_to_reply', 'early_to_B', 'early_to_cmp', 'early_to_reply', 'A_to_early', 'A_to_B', 'A_to_cmp', 'A_to_reply'])
    return {'tag': tag, 'm': m, 'columns': len(X), 'row_families': len(X[0]), 'checked_X_coefficients': len(errors), 'maximum_float_coefficient_error': max(errors), 'beta': str(dual[-1]), 'welfare_factor': str(1 / dual[-1]), 'dual_multipliers': dict(zip(names, map(str, dual[:-1]))), 'dual_slacks_all_columns': list(map(str, residual)), 'dual_slack_min': str(min(residual)), 'dual_zero_slacks': sum(v == 0 for v in residual), 'primal_support': [{'column_index': j, 'column': list(expected[j]), 'mass': str(v)} for j, v in zip(support, weights)], 'primal_row_slacks': dict(zip(names, map(str, slack))), 'W': str(W), 'O': str(O), 'matching_objectives': True, 'all_constraints_exact': True, 'exact_optimum_scope': 'this finite necessary-row cone only; no complete SPE strategy', 'recovery': {'dual_positive_coordinates': positive, 'dual_active_column_equations': active, 'primal_support_indices': support, 'support_tolerance': 1e-8, 'active_tolerance': 1e-7, 'method': 'exact Gaussian elimination on selected support, followed by all-column and all-row Fraction checks'}}

def main():
    start = time.time()
    capture = BASE / 'replay/capture.json'
    output = BASE / 'exact-audit.json'
    assert not output.exists()
    result = {'identity': 'one independent exact reconstruction and certificate recovery; no original imports, LP, or SPE enumeration', 'capture_sha256': sha(capture), 'audit_script_sha256': sha(Path(__file__)), 'results': [check(cap) for cap in json.loads(capture.read_text())], 'original_function_calls': 0, 'LP_calls': 0, 'five_player_witness_recomputations': 0}
    result['seconds'] = time.time() - start
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{k: r[k] for k in ('tag', 'columns', 'checked_X_coefficients', 'beta', 'welfare_factor', 'dual_zero_slacks', 'all_constraints_exact')} for r in result['results']]))

if __name__ == '__main__':
    main()
