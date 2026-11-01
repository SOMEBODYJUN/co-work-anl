"""Exact, independent finite coefficient checks; no optimizer or source import.

The six identities are transcribed from the separately preserved 4870-byte
opposite_group_pair_payment.md.  Analytic positivity is proved in the formal
pages.  Decimal JSON tokens are checked literally, not silently rounded.
"""
from pathlib import Path
from itertools import product, combinations, combinations_with_replacement
from functools import lru_cache
from fractions import Fraction as Q
from math import factorial
from datetime import datetime, timezone
import hashlib
import json
import sys
import time

BASE = Path(__file__).resolve().parent
RAW = BASE / 'original/81320cad6b217355eb30/submodular_probe.json'
OUT = BASE / 'contract-replay'
N = 63
ZERO = (Q(0),) * N


def add(a, b, scale=1):
    return tuple(x + scale * y for x, y in zip(a, b))


def total(vectors):
    ans = ZERO
    for vector in vectors:
        ans = add(ans, vector)
    return ans


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def unit(mask):
    return tuple(Q(mask == i + 1) for i in range(N))


@lru_cache(None)
def phi(h):
    d = len(h)
    result = [Q(0)] * N
    for subset in range(1, 1 << d):
        selected = [h[i] for i in range(d) if subset >> i & 1]
        mask = 0
        for label in selected:
            mask |= 1 << label
        j = len(selected)
        result[mask - 1] += Q(factorial(j - 1) * factorial(d - j), factorial(d))
    return tuple(result)


def ph(h):
    return phi(tuple(sorted(h)))


def u(h, a):
    return add(ph(tuple(h) + (a,)), ph(tuple(h)), -1)


def act(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def terminal(h):
    h = tuple(h)
    while len(h) < 3:
        h += (act(h),)
    return h


def payoff(z, i):
    return u(z[:i] + z[i + 1:], z[i])


def gamma(h, alternative):
    z = terminal(h)
    other = terminal(tuple(h) + (alternative,))
    return add(payoff(z, len(h)), payoff(other, len(h)), -1)


def tax(c, a, b, d):
    # -D_(a,b) D_(a,d) Phi(c).
    return total([ph((c, a, b)), ph((c, a, d)),
                  tuple(-x for x in ph((c, b, d))),
                  tuple(-x for x in ph((c, a, a)))])


def main():
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    OUT.mkdir(exist_ok=False)
    literal = json.loads(RAW.read_text(), parse_float=Q)
    assert literal['k'] == 6 and literal['star_tax'] is False
    assert len(literal['F']) == 63 and len(literal['query']) == 6
    old_f = tuple(map(Q, literal['F']))
    p = tuple(map(Q, literal['query']))
    s = sum(p, Q(0))
    assert min(p) >= 0
    actual = terminal(())
    assert actual == (0, 3, 4) == tuple(literal['actual'])
    profits = [payoff(actual, i) for i in range(3)]
    welfare = total(profits)
    assert welfare == unit((1 << 0) | (1 << 3) | (1 << 4))
    first_two = add(profits[0], profits[1])
    table = [
        ([ ((), 3), ((0,), 1), ((0, 2), 0), ((1, 5), 0) ], (1, 0, 3, 5)),
        ([ ((), 3), ((0,), 1), ((0, 4), 1) ], (0, 1, 3, 4)),
        ([ ((), 3), ((0,), 1), ((0, 5), 2), ((3, 0), 2) ], (0, 2, 3, 5)),
        ([ ((), 3), ((0,), 1), ((0, 2), 3) ], None),
        ([ ((), 4), ((0,), 1), ((0, 2), 4) ], None),
        ([ ((), 5), ((0,), 1), ((0, 2), 5) ], None),
    ]
    identities = []
    for a, (terms, remainder) in enumerate(table):
        lhs = add(add(first_two, u((0, 1), a), -1), u((0, 2), a), -1)
        rhs = total(gamma(h, b) for h, b in terms)
        if remainder:
            rhs = add(rhs, tax(*remainder))
        assert lhs == rhs
        identities.append({
            'query': a,
            'incentive_terms': [{'history': list(h), 'alternative': b} for h, b in terms],
            'tax_c_a_b_d': remainder,
            'lhs_coefficients': list(map(str, lhs)),
            'rhs_coefficients': list(map(str, rhs)),
            'coefficient_count': N,
            'all_equal': True,
        })
    rows = []
    for mask in range(64):
        absent = [a for a in range(6) if not mask >> a & 1]
        for a in absent:
            rows.append(('monotone', [mask, a], add(unit(mask | 1 << a), unit(mask), -1), Q(0)))
        for a, b in combinations(absent, 2):
            vector = add(add(add(unit(mask | 1 << a), unit(mask | 1 << b)), unit(mask), -1), unit(mask | 1 << a | 1 << b), -1)
            rows.append(('submodular', [mask, a, b], vector, Q(0)))
    policy = []
    for depth in range(3):
        for h in product(range(6), repeat=depth):
            policy.append({'history': list(h), 'action': act(h), 'terminal': list(terminal(h))})
            for b in range(6):
                if b != act(h):
                    rows.append(('SPE', [list(h), b], gamma(h, b), Q(0)))
    for h in combinations_with_replacement(range(6), 2):
        vector = total(tuple(p[a] * x for x in u(h, a)) for a in range(6))
        rows.append(('static_background', list(h), vector, Q(-1)))
    counts = {family: sum(row[0] == family for row in rows)
              for family in ['monotone', 'submodular', 'SPE', 'static_background']}
    assert counts == {'monotone': 192, 'submodular': 240, 'SPE': 215, 'static_background': 21}
    all_rows = []
    exact_f = (Q(1),) * 63
    exact_t = s / 3
    for family, key, coefficients, t_coefficient in rows:
        frozen_slack = dot(coefficients, old_f) + t_coefficient * literal['t']
        exact_slack = dot(coefficients, exact_f) + t_coefficient * exact_t
        assert exact_slack >= 0
        all_rows.append({'family': family, 'key': key,
                         'frozen_decimal_slack': str(frozen_slack),
                         'rank_one_exact_slack': str(exact_slack)})
    assert dot(welfare, exact_f) == 1
    statistics = {}
    for family in counts:
        selected = [row for row in all_rows if row['family'] == family]
        values = [Q(row['frozen_decimal_slack']) for row in selected]
        statistics[family] = {'rows': len(values),
                              'negative_literal_rows': sum(v < 0 for v in values),
                              'minimum_literal_slack': str(min(values)),
                              'minimum_literal_slack_float': float(min(values))}
    rng_result = {'checked': False}
    try:
        import numpy as np
        rng = np.random.default_rng(22107)
        samples = [np.ones(6) / 6] + [rng.dirichlet(np.ones(6)) for _ in range(9)]
        report_float = json.loads(RAW.read_text())['query']
        matches = [j for j, query in enumerate(samples) if query.tolist() == report_float]
        rng_result = {'checked': True, 'numpy_version': np.__version__, 'seed': 22107,
                      'current_default_grid_indices_zero_based': matches,
                      'actual_historical_trials_not_known': True,
                      'optimization_calls': 0}
    except ImportError:
        pass
    report = {
        'source_sha256': hashlib.sha256(RAW.read_bytes()).hexdigest(),
        'literal_query_sum': str(s), 'literal_query_sum_minus_one': str(s - 1),
        'analytic_exact_LP_optimum_for_nonnegative_query_weights': str(exact_t),
        'unit_probability_query_optimum': '1/3',
        'literal_report_t_minus_analytic_optimum': str(literal['t'] - exact_t),
        'literal_report_F_max_distance_from_one': str(max(abs(x - 1) for x in old_f)),
        'literal_normalization_residual': str(dot(welfare, old_f) - 1),
        'exact_rank_one_normalization': str(dot(welfare, exact_f)),
        'exact_rank_one_first_two_payoff': str(dot(first_two, exact_f)),
        'exact_rank_one_all_668_rows_pass': True,
        'policy_nodes': len(policy), 'nonself_incentives': counts['SPE'],
        'matrix_rows_without_optional_star': len(rows),
        'matrix_rows_with_optional_star_from_source_count': 2180,
        'six_query_identity_coefficients_checked': 6 * N,
        'frozen_decimal_row_statistics': statistics,
        'rng_data_only_comparison': rng_result,
        'original_submodular_CLI_or_solve_calls': 0,
        'new_LP_or_MIP_calls': 0,
        'not_a_proof_of_historical_HiGHS_dual_or_binary_matrix_optimality': True,
    }
    for name, data in [('six-query-identities.json', identities), ('complete-policy.json', policy),
                       ('all-668-row-slacks.json', all_rows), ('report.json', report)]:
        (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    event = {'argv': [sys.executable, '-B', str(Path(__file__).resolve())],
             'started_utc': started, 'elapsed_seconds': time.perf_counter() - t0,
             'python': sys.version, 'optimize': sys.flags.optimize,
             'source_imports': 0, 'new_optimization_calls': 0,
             'scope': 'one independent exact coefficient and saved-decimal-data audit',
             'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / 'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
