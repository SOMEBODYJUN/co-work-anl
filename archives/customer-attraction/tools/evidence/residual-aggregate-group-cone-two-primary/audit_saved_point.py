"""Independent exact reconstruction of the archived residual-cone saved point.

No original main, no solver, no randomized scan.  The source module is loaded
once only to compare its floating coefficient arrays with exact definitions.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / 'related'))
spec = importlib.util.spec_from_file_location('archived_cone', BASE / 'original/cone_probe.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def policy(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] in (0, 1, 2) else 0
    group = (0, 1, 2) if h[1] in (0, 1, 2) else (3, 4, 5)
    return min(set(group).difference(h))


def finish(h):
    while len(h) < 3:
        h += (policy(h),)
    return h


def share(mask, action, terminal, prefix):
    if not ((mask >> action) & 1):
        return F(0)
    load = sum((mask >> a) & 1 for a in prefix + terminal)
    assert load > 0
    return F(1, load)


raw = (BASE / 'original/cone_probe_output.json').read_text()
decimal = json.loads(raw, parse_float=F)
binary = json.loads(raw)
point = decimal['best']
prefix = tuple(point['prefix'])
weights = point['weights']
assert prefix == (5, 2, 0, 3, 5)
assert len(weights) == 63 and weights == [F(0)] * 62 + [F(1)]
histories = [h for depth in range(3) for h in product(range(6), repeat=depth)]
assert len(histories) == 43
actions = [{'history': list(h), 'action': policy(h)} for h in histories]
assert all(source.group_policy(h, 6) == policy(h) for h in histories)
terminal = finish(())
assert terminal == (0, 3, 4)
G = []
weighted_slacks = []
for h in histories:
    z = finish(h)
    chosen = z[len(h)]
    for a in range(6):
        if a == chosen:
            continue
        deviation = finish(h + (a,))
        row = [share(mask, chosen, z, prefix) - share(mask, a, deviation, prefix)
               for mask in range(1, 64)]
        G.append(row)
        weighted_slacks.append(sum(c * w for c, w in zip(row, weights)))
assert len(G) == 215 and set(weighted_slacks) == {F(0)}
c = [sum(share(mask, a, terminal, prefix) for a in terminal) for mask in range(1, 64)]
P = sum(v * w for v, w in zip(c, weights))
assert P == F(3, 8)
opponents = list(combinations_with_replacement(range(6), 2))
beta = [[[F((mask >> a) & 1, 1 + sum((mask >> x) & 1 for x in prefix + q))
          for a in range(6)] for mask in range(1, 64)] for q in opponents]
assert len(opponents) == 21

# Compare every source coefficient, not merely its saved weighted evaluation.
float_G, float_c, float_beta = source.gamma(6, 3, prefix, source.group_policy)
exact_flat = [x for row in G for x in row] + c + [x for q in beta for row in q for x in row]
float_flat = list(float_G.flat) + list(float_c.flat) + list(float_beta.flat)
assert len(exact_flat) == len(float_flat) == 21546
max_float_error = max(abs(F(float(v)) - x) for x, v in zip(exact_flat, float_flat))
assert max_float_error <= F(1, 10**15)

interpretations = {}
for name, p in [('decimal_literals', point['p']),
                ('exact_binary_floats', [F(v) for v in binary['best']['p']])]:
    assert len(p) == 6 and all(x > 0 for x in p)
    mass = sum(p)
    raw_values = [sum(beta[i][j][a] * weights[j] * p[a]
                      for j in range(63) for a in range(6)) for i in range(21)]
    normalized = [x / mass for x in p]
    norm_values = [sum(beta[i][j][a] * weights[j] * normalized[a]
                       for j in range(63) for a in range(6)) for i in range(21)]
    assert set(raw_values) == {mass / 8}
    assert sum(normalized) == 1 and set(norm_values) == {F(1, 8)}
    interpretations[name] = {
        'sum_p': str(mass), 'sum_p_minus_one': str(mass - 1),
        'not_a_probability_distribution_exactly': mass != 1,
        'unnormalized_all_opponent_value': str(mass / 8),
        'unnormalized_three_t_minus_P': str(3 * min(raw_values) - P),
        'separately_named_normalized_query': [str(x) for x in normalized],
        'normalized_all_21_opponent_values': [str(x) for x in norm_values],
        'normalized_three_t_minus_P': str(3 * min(norm_values) - P),
    }

# All-interest and zero-customer boundary checks, not additional random samples.
boundaries = []
for m in range(7):
    old = (0,) * m
    slacks = []
    for h in histories:
        z = finish(h)
        for a in range(6):
            slacks.append(share(63, z[len(h)], z, old) - share(63, a, finish(h + (a,)), old))
    assert set(slacks) == {F(0)} and len(slacks) == 258
    v = F(1, m + 3)
    residual = sum(share(63, a, terminal, old) for a in terminal)
    assert residual == 3 * v
    boundaries.append({'old_players': m, 'prefix': list(old), 'comparisons_including_self': len(slacks),
                       'minimum_IC': '0', 'residual_profit': str(residual), 'security': str(v), 'gap': '0',
                       'main_samples_this_old_length': 1 <= m <= 6})

new = json.loads((BASE / 'replay/one-sample-new.json').read_text())
assert new['samples_requested'] == 1
assert new['seed'] == binary['seed']
assert new['best'] == binary['best']
manifest = {}
for name in ['original/cone_probe.py', 'original/cone_probe_output.json', 'related/probe.py',
             'replay/one-sample-new.json']:
    data = (BASE / name).read_bytes()
    manifest[name] = {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

report = {
    'status': 'PASS: exact saved-point reconstruction; unnormalized p is not certified',
    'python': platform.python_version(),
    'source_coefficient_comparison': {'IC_rows_nonself': 215, 'histories': 43,
                                    'customer_types': 63, 'static_opponents': 21,
                                    'coefficients_compared': 21546,
                                    'max_absolute_float_error_exact': str(max_float_error)},
    'complete_policy': actions, 'actual_residual_path': list(terminal),
    'saved_prefix': list(prefix), 'saved_total_players': len(prefix) + 3,
    'positive_type': {'mask': 63, 'unit_customer_multiplicity': 1},
    'exact_min_IC': str(min(weighted_slacks)), 'exact_residual_profit': str(P),
    'exact_security': '1/8', 'full_terminal_coverage': '1', 'old_players_total_rent': '5/8',
    'query_interpretations': interpretations, 'boundary_fixtures': boundaries,
    'zero_customer_boundary': {'all_258_IC': '0', 'P': '0', 'v': '0',
                              'excluded_from_unit_mass_LP_slice': True,
                              'strict_failure_possible_at_zero': False},
    'one_sample_replay_best_exactly_equals_archived_json_after_float_parse': True,
    'new_run_samples_requested': 1, 'historical_samples_requested': 1500,
    'did_not_replay_historical_1500_scan': True,
    'file_manifest': manifest,
}
with (BASE / 'exact-saved-point-audit.json').open('x') as out:
    json.dump(report, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'status': report['status'], 'histories': 43, 'nonself_IC': 215,
                  'coefficients_compared': 21546, 'static_opponents': 21,
                  'P': str(P), 'v': '1/8', 'normalized_gap': '0'}, ensure_ascii=False))
