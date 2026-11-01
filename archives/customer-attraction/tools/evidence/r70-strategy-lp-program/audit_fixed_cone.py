#!/usr/bin/env python3
"""Independent key completeness and rational dual checks; no original imports/LP."""
import hashlib
import json
import time
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / 'replay'


def read(name):
    return json.loads((R / name).read_text())


def digest(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    started = time.perf_counter()
    stored = read('complete-strategy.json')
    strategy = {tuple(x['history']): x['action'] for x in stored['entries']}
    domain = {h for depth in range(6) for h in product(range(7), repeat=depth)}
    assert len(strategy) == len(stored['entries']) == 19608 and set(strategy) == domain
    assert all(isinstance(a, int) and 0 <= a < 7 for a in strategy.values())

    @lru_cache(None)
    def final_counts(h):
        if len(h) == 6:
            return tuple(h.count(a) for a in range(7))
        return final_counts(h + (strategy[h],))

    keys = sorted({(chosen, final_counts(h), other, final_counts(h + (other,)))
                   for h, chosen in strategy.items() for other in range(7) if other != chosen})
    frozen = read('constraint-keys.json')
    serialized = [(a, tuple(q), b, tuple(r)) for a, q, b, r in frozen['keys']]
    assert keys == serialized and len(keys) == 3048
    actual = final_counts(())
    assert list(actual) == frozen['actual_count'] == [1, 0, 5, 0, 0, 0, 0]
    ic = read('ic-matrix.json')
    assert ic['shape'] == [3048, 127]
    exact_rows = []
    coefficient_checks = 0
    nonzero_checks = 0
    for i, (a, q, b, r) in enumerate(keys):
        nonzero = {ic['indices'][j]: ic['data'][j] for j in range(ic['indptr'][i], ic['indptr'][i + 1])}
        row = {}
        for mask in range(1, 128):
            left = F(1, sum(q[t] for t in range(7) if mask & (1 << t))) if mask & (1 << a) else F(0)
            right = F(1, sum(r[t] for t in range(7) if mask & (1 << t))) if mask & (1 << b) else F(0)
            value = right - left  # A_ub = -G
            expected_float = -(float(left) - float(right))
            assert nonzero.get(mask - 1, 0) == expected_float
            assert (mask - 1 in nonzero) == bool(value)
            if value:
                row[mask - 1] = value
                nonzero_checks += 1
            coefficient_checks += 1
        exact_rows.append(row)
    assert nonzero_checks == len(ic['data'])

    objective = [F(any(actual[a] and mask & (1 << a) for a in range(7))) for mask in range(1, 128)]
    covers = [[F(bool(mask & (127 - (1 << omit)))) for mask in range(1, 128)] for omit in range(7)]
    fits = read('seven-lp-results.json')['calls']
    assert [x['omit'] for x in fits] == list(range(7))
    reports = []
    all_success = True
    for call in fits:
        fit = call['result']
        omit = call['omit']
        assert fit['success'] and fit['status'] == 0
        y = [F(float(x)).limit_denominator(1000000) for x in fit['ineqlin']['marginals']]
        lam = F(float(fit['eqlin']['marginals'][0])).limit_denominator(1000000)
        assert len(y) == 3055
        residual = objective[:]
        for i, yi in enumerate(y[:3048]):
            if yi:
                for j, aij in exact_rows[i].items():
                    residual[j] -= yi * aij
        for j in range(127):
            residual[j] -= sum(y[3048 + k] * covers[k][j] for k in range(7))
            residual[j] -= lam * covers[omit][j]
        beta = sum(y[3048:]) + lam
        passed = all(yi <= 0 for yi in y) and min(residual) >= 0
        all_success = all_success and passed
        reports.append({'omit': omit, 'status': 'PASS' if passed else 'UNRECOVERED',
                        'numerical_fun': fit['fun'], 'exact_dual_bound': str(beta),
                        'equality_multiplier': str(lam),
                        'nonzero_inequality_multipliers': [{'row': i, 'value': str(v)} for i, v in enumerate(y) if v],
                        'column_residuals': list(map(str, residual)), 'minimum_residual': str(min(residual)),
                        'negative_residual_columns': [i + 1 for i, v in enumerate(residual) if v < 0],
                        'positive_inequality_multiplier_rows': [i for i, v in enumerate(y) if v > 0]})
    report = {'status': 'PASS' if all_success else 'KEYS_PASS_DUAL_RECOVERY_INCOMPLETE',
              'inputs': {name: digest(R / name) for name in ['complete-strategy.json', 'constraint-keys.json', 'ic-matrix.json', 'seven-lp-results.json']},
              'ordered_nodes': len(strategy), 'nonself_history_comparisons_reconstructed_as_keys': 19608 * 6,
              'distinct_keys': len(keys), 'matrix_coefficients_checked': coefficient_checks,
              'matrix_nonzero_entries_checked': nonzero_checks,
              'matrix_check': 'every original float coefficient equals separately evaluated reciprocal difference; dual uses exact Fraction coefficients',
              'dual_column_checks': 7 * 127, 'denominator_recovery_cap': 1000000,
              'duals': reports,
              'scope': {'independent_script_executions': 1, 'original_imports': 0, 'original_helpers': 0, 'DP': 0, 'LP': 0,
                        'point_payoff_audits': 0, 'new_rational_primal_recoveries': 0,
                        'description': 'Rebuild full history-to-key map, bind all coefficient entries, certify seven dual lower bounds only. Feasible rational witness is independently supplied by the paired data audit.'},
              'elapsed_seconds': time.perf_counter() - started}
    (HERE / 'exact-cone-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'ordered_nodes', 'distinct_keys', 'matrix_coefficients_checked', 'matrix_nonzero_entries_checked', 'dual_column_checks', 'elapsed_seconds']}))
    print([(x['omit'], x['status'], x['exact_dual_bound'], x['minimum_residual']) for x in reports])


if __name__ == '__main__':
    main()
