"""Read all frozen result fields; compare one replay; audit the four-state case.

This does not certify the larger-grid float LP outputs.  Exact arithmetic below
uses the intended decimal q (Fraction(str(q))), not the solver's binary float.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import platform
import numpy
import scipy

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'sources/55c5313fb9336914e54f--type_count_results.json'
REPLAY = HERE / 'replay/type_count_results.json'
data = json.loads(SOURCE.read_text())
replay = json.loads(REPLAY.read_text())
keys = {'n1', 'nq', 'q', 'degree', 'alpha', 'rational',
        'min_marginal_ratio', 'max_marginal_ratio',
        'max_constraint_violation', 'variables', 'constraints'}
expected_cases = [(n, n, q, d) for q in [1.01, 1.1, 1.5, 2, 3, 10]
                  for d in [2, 3] for n in [1, 2, 5, 10, 20]]
actual_cases = []
for row in data:
    assert set(row) == keys
    n1, nq = row['n1'], row['nq']
    actual_cases.append((n1, nq, row['q'], row['degree']))
    assert row['variables'] == (n1 + 1) * (nq + 1) + 1
    assert row['constraints'] == 2 * (n1 * (nq + 1) + nq * (n1 + 1))
assert actual_cases == expected_cases

def digest(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(HERE.parent)), 'size': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}

exact_n1 = []
for row in data:
    if row['n1'] != 1:
        continue
    q, d = Q(str(row['q'])), row['degree']
    A = 1 + q * (1 + q)**d  # light then heavy
    B = q**(d + 1) + (1 + q)**d  # heavy then light
    alpha = A / B
    assert A >= B > 0
    values = {(0, 0): Q(0), (1, 0): Q(1),
              (0, 1): alpha * q**(d + 1), (1, 1): A}
    ratios = []
    for k, l in values:
        for dk, dl, w in [(1, 0, Q(1)), (0, 1, q)]:
            target = (k + dk, l + dl)
            if target not in values:
                continue
            cost = w * (k + q * l + w)**d
            marginal = values[target] - values[k, l]
            assert cost <= marginal <= alpha * cost
            ratios.append({'from': [k, l], 'to': list(target),
                           'cost': str(cost), 'marginal': str(marginal),
                           'ratio': str(marginal / cost)})
    assert len(ratios) == 4
    exact_n1.append({'q_decimal': str(row['q']), 'q_exact': str(q),
                     'degree': d, 'two_path_lower_sum': str(A),
                     'two_path_upper_sum_without_alpha': str(B),
                     'exact_alpha': str(alpha),
                     'saved_rational_guess': row['rational'],
                     'guess_minus_exact': str(Q(row['rational']) - alpha),
                     'F': {f'{k},{l}': str(v) for (k, l), v in values.items()},
                     'exact_edges': ratios})

grouped = []
for q in [1.01, 1.1, 1.5, 2, 3, 10]:
    for d in [2, 3]:
        rows = [r for r in data if r['q'] == q and r['degree'] == d]
        grouped.append({'q': q, 'degree': d,
                        'rational_guesses_by_N': {str(r['n1']): r['rational'] for r in rows},
                        'alpha_by_N': {str(r['n1']): r['alpha'] for r in rows},
                        'min_recorded_marginal_ratio': min(r['min_marginal_ratio'] for r in rows),
                        'max_recorded_marginal_ratio': max(r['max_marginal_ratio'] for r in rows),
                        'max_recorded_constraint_violation': max(r['max_constraint_violation'] for r in rows)})

# A different, later count-polynomial ansatz is compared only on its documented
# out-of-grid witnesses.  It is not this source's rectangular, free-state LP.
ROOT = HERE.parents[4]
LATER = ROOT / 'archives/weighted-congestion/tools/evidence/atomic-games/toy_output.json'
later = json.loads(LATER.read_text())
candidate = later['count_polynomial_grid'][-1]
assert candidate['latency_monomial_degree'] == 3
assert candidate['existing_user_limit'] == 50
coefficients = list(map(Q, candidate['rational_coefficients']))
monomials = candidate['coefficient_monomials']
later_exact_checks = []
for witness in later['out_of_grid_falsification_of_cubic_50_user_candidate']:
    a, b, w = witness['a'], witness['b'], witness['adding_weight']
    aa, bb = (a + 1, b) if w == 1 else (a, b + 1)
    marginal = sum(c * (aa**u * bb**v - a**u * b**v)
                   for c, (u, v) in zip(coefficients, monomials))
    ratio = marginal / (w * (a + 2 * b + w)**3)
    assert str(ratio) == witness['exact_ratio']
    assert ratio < 1
    later_exact_checks.append({'a': a, 'b': b, 'w': w, 'ratio': str(ratio),
                               'violates_lower_bound': True})

out = {'scope': 'all 60 frozen rows and all 11 fields read; exact certification only for N=1',
       'environment': {'python': platform.python_version(), 'numpy': numpy.__version__,
                       'scipy': scipy.__version__, 'OMP_NUM_THREADS': '1',
                       'OPENBLAS_NUM_THREADS': '1'},
       'original': digest(SOURCE), 'replay': digest(REPLAY),
       'json_equal': data == replay,
       'bytes_equal': SOURCE.read_bytes() == REPLAY.read_bytes(),
       'number_of_rows': len(data), 'number_of_fields_per_row': len(keys),
       'number_of_distinct_parameter_cases': len(set(actual_cases)),
       'sum_variables': sum(r['variables'] for r in data),
       'sum_constraints': sum(r['constraints'] for r in data),
       'smallest_saved_min_marginal_ratio': min(r['min_marginal_ratio'] for r in data),
       'largest_saved_max_marginal_ratio': max(r['max_marginal_ratio'] for r in data),
       'largest_saved_constraint_violation': max(r['max_constraint_violation'] for r in data),
       'largest_saved_max_ratio_minus_alpha': max(r['max_marginal_ratio'] - r['alpha'] for r in data),
       'all_groups': grouped, 'exact_four_state_checks': exact_n1,
       'later_cubic_candidate_exact_out_of_grid_checks': later_exact_checks,
       'limitations': ['No larger-grid F values or dual certificates were stored in the source JSON.',
                       'Replaying floats does not prove exact feasibility or optimality.',
                       'The N=1 exact formula uses rational decimal q, not the binary float input.',
                       'No full-population or PNE-threshold statement follows from the table.']}
(HERE / 'analysis.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items()
                  if k not in {'all_groups', 'exact_four_state_checks'}}, indent=2))
