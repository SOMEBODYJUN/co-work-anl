#!/usr/bin/env python3
"""Independent true-share audit of the maximum-C nested fifth-source SAFE.

Standard-library Fraction arithmetic only.  No Main/builder/solver/old audit
program is imported or executed.  Existing frozen face identities are data
and are rechecked in every one of their 513 columns before composition.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
SRC = WS / 'main_source2_maximum_nested_safe'
THETA = F(5, 12)
PINS = {
    'main_source2_maximum_nested_safe/manifest.json':
        '3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269',
    'main_source2_maximum_nested_safe/proof.md':
        '1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067',
    'main_source2_maximum_nested_safe/exact_certificate.json':
        '97694ec0496d52b428fe6a9cfee7030944312709a11de8a67b201bd724e751ac',
    'main_source2_maximum_nested_safe/hidden_state_checks.json':
        'f376eeb57404bdcd07fc42b6e72e23ecc30c2ed830cba42f1b6e43b77bfdc782',
    'main_source2_maximum_nested_safe/minimum_table.json':
        '140badf8d40d7e7c6a1c544bac7f55f8087a13c3f581a0244af9e6e4ce3a066a',
    'main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json':
        'a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba',
    'visible_maximum_joint/exact_input.json':
        'b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33',
    'visible_maximum_joint_solve/exact_certificate.json':
        '8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347',
    'visible_c_source2_equality_audit/face_exclusion_certificate.json':
        '053325a1ae95209726c268064ad6867e478ae0a2c9545aa7099134a4f9565815',
    'visible_c_source2_equality_audit/freeze_manifest.json':
        'e6ce949e33023d1c5291cde1470a48bd3fec495f034689a4ee9ef638d8f56dec',
}
for name, digest in PINS.items():
    assert sha256((WS / name).read_bytes()).hexdigest() == digest, name


def read(name):
    return json.loads((WS / name).read_text())


def share(bit, prefix, following=0):
    return F(1, prefix + 1 + following) if bit else F(0)


def pure_query(bit, background):
    return F(bit, background + 1)


def components(p, c, menu, tail):
    r3, r4, r5, r6 = tail
    v2 = share(c, p, sum(tail))
    v5 = share(r5, p + c + r3 + r4, r6)
    v6 = share(r6, p + c + r3 + r4 + r5)
    terminal_average = sum((pure_query(q, p + c + r3 + r4 + r5)
                            for q in menu), F(0)) / 6
    # A true source5 deviation has exactly one true successor; its worst
    # possible payoff is the query share with that successor covering it.
    safe5_average = sum((share(q, p + c + r3 + r4, 1)
                        for q in menu), F(0)) / 6
    base = 25 * v2 + F(r3 + r4 + r5, 2) + r6 - v6 + terminal_average
    increment = safe5_average - v5
    return base, increment


def formula(p, c, o):
    m0 = F(5, 2) * c + F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1))
    slope = F(o, 6 * (p + 3 * c + 2)) - F(c, 5)
    return m0, slope


stored_states = read('main_source2_maximum_nested_safe/hidden_state_checks.json')
stored_minima = read('main_source2_maximum_nested_safe/minimum_table.json')
lookup = {(r['p'], r['c'], r['o'], tuple(r['r'])): r for r in stored_states}
assert len(lookup) == len(stored_states) == 128
assert len(stored_minima) == 8
limits, cases, minima, residuals = [], [], {}, {}
for p, c, o in product((0, 1), repeat=3):
    m0, slope = formula(p, c, o)
    target = m0 + THETA * slope
    evaluated, zeros0, zerosT = {}, [], []
    for tail in product((0, 1), repeat=4):
        # One covered menu slot is merely a literal representation of the
        # weakened o/6 cost; all real64 menu strings are checked below.
        base, increment = components(p, c, (o, 0, 0, 0, 0, 0), tail)
        r0, r1 = base - m0, increment - slope
        endpoint = r0 + THETA * r1
        assert r0 >= 0 and endpoint >= 0
        if r1 < 0:
            assert r0 > 0
            limits.append((r0 / (-r1), p, c, o, tail))
        if r0 == 0:
            zeros0.append(tail)
        if endpoint == 0:
            zerosT.append(tail)
        value = base + THETA * increment
        evaluated[tail] = value
        residuals[p, c, o, tail] = endpoint
        st = lookup[p, c, o, tail]
        for key, val in [('base', base), ('increment', increment), ('cost', value),
                         ('minimum', target), ('residual', endpoint)]:
            assert F(st[key]) == val, (p, c, o, tail, key)
        # Fully explicit shares equal the compact signed-numerator form.
        L = p + c + sum(tail)
        numerator = 25 * c - tail[3] - THETA * tail[2]
        compact = (numerator / L if L else F(0)) + F(sum(tail[:3]), 2) + tail[3]
        compact += F(o, 6 * (p + c + sum(tail[:3]) + 1))
        compact += THETA * F(o, 6 * (p + c + sum(tail[:2]) + 2))
        assert value == compact
        cases.append({'p': p, 'c': c, 'o': o, 'tail': list(tail),
                      'residual_at_zero': str(r0), 'residual_slope': str(r1),
                      'residual_at_5_over_12': str(endpoint)})
    assert min(evaluated.values()) == target
    assert set(zeros0).intersection(zerosT)  # exact affine min on full interval
    minima[p, c, o] = target
    record = next(v for v in stored_minima if (v['p'], v['c'], v['o']) == (p, c, o))
    assert F(record['m0']) == m0 and F(record['slope']) == slope
    assert F(record['minimum']) == target
    assert record['zero_states'] == [list(tail) for tail in zerosT]
endpoint = min(v[0] for v in limits)
critical = [(p, c, o, tail) for value, p, c, o, tail in limits if value == endpoint]
assert endpoint == THETA
assert critical == [(0, 0, 1, (0, 0, 1, 0))]

menu_checks = 0
for p, c in product((0, 1), repeat=2):
    for menu in product((0, 1), repeat=6):
        d, o = sum(menu), int(any(menu))
        for tail in product((0, 1), repeat=4):
            actual0, actual1 = components(p, c, menu, tail)
            weak0, weak1 = components(p, c, (o, 0, 0, 0, 0, 0), tail)
            actual, weak = actual0 + THETA * actual1, weak0 + THETA * weak1
            overlap = F(d - o, 6) * (F(1, p + c + sum(tail[:3]) + 1)
                                     + THETA * F(1, p + c + sum(tail[:2]) + 2))
            assert actual - weak == overlap >= 0
            assert actual >= weak >= minima[p, c, o]
            menu_checks += 1
assert menu_checks == 4096

producer_cert = read('main_source2_maximum_nested_safe/exact_certificate.json')
assert F(producer_cert['theta']) == THETA
assert producer_cert['critical_affine_endpoint'] == [{'p': 0, 'c': 0, 'o': 1, 'r': [0, 0, 1, 0]}]
assert sorted(map(F, producer_cert['direct_budget_weights'].values())) == sorted([F(25), F(1, 2), F(1, 2), F(1, 2), F(1), F(1), THETA])

inp = read('visible_maximum_joint/exact_input.json')
primal = read('visible_maximum_joint_solve/exact_certificate.json')
line = read('main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json')
assert line['name'] == 'SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE'
assert line['family'] == 'TRUE_SAME_BRANCH_NESTED_SAFE'
assert F(line['rhs']) == 0 and F(line['numerical_divisor']) == 300
assert set(line['a']) == set(map(str, range(513)))


def vec(a):
    return [F(a.get(str(j), '0')) for j in range(513)]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


U, B, M, N, Csize = ([F(0)] * 513 for _ in range(5))
expected = [F(0)] * 513
for j, bits in enumerate(product((0, 1), repeat=9)):
    aa, x, o, c = bits[:6], bits[6], bits[7], bits[8]
    p = aa[0]
    assert inp['atom_columns'][j] == {'index': j, 'old_index': j // 2,
                                      'a': list(aa), 'x': x, 'o': o, 'c': c}
    U[j] = share(aa[1], aa[0], sum(aa[2:]))
    B[j], M[j], N[j], Csize[j] = F(c, p + 5), F(o, 6 * (p + 4 * c + 1)), F(o, 6 * (p + 3 * c + 2)), F(c)
    expected[j] = 300 * U[j] - 288 * B[j] - 12 * M[j] - 5 * N[j]
    # Eliminate |C|=K with free multiplier +29, preserving K separately.
    assert expected[j] == 300 * U[j] - 12 * minima[p, c, o] + 29 * c
    for tail in product((0, 1), repeat=4):
        base, inc = components(p, c, (o, 0, 0, 0, 0, 0), tail)
        psi = base + THETA * inc
        assert expected[j] == 300 * U[j] - 12 * psi + 12 * residuals[p, c, o, tail] + 29 * c
expected[512] = F(1)
assert F(30) - F(29) == expected[512]
assert vec(line['a']) == expected

# Compose previously frozen exact face identities as data, independently
# verifying their full513 columns.  No earlier code is imported/executed.
face = read('visible_c_source2_equality_audit/face_exclusion_certificate.json')
assert face['status'] == 'PASS_ENTIRE_OPTIMAL_FACE_EXCLUDED_BY_TRUE_INTERMEDIATE_MEAN_SAFE'
pos = face['positive_raw_indices']
E = [vec(inp['raw_rows'][j]['a']) for j in pos] + [vec(e['a']) for e in inp['equalities']]
H = [F(inp['raw_rows'][j]['rhs']) for j in pos] + [F(e['rhs']) for e in inp['equalities']]
labels = [inp['raw_rows'][j]['name'] for j in pos] + [e['name'] for e in inp['equalities']]
assert labels == face['equation_names']
ZR = face['zero_residual_columns']
old_residual = list(map(F, primal['dual']['nonnegative_column_residual']))
assert ZR == [j for j, value in enumerate(old_residual) if value == 0]
Kvec = [F(0)] * 512 + [F(1)]
safe5 = [U[j] - N[j] for j in range(513)]
selected = [next(f for f in face['fixed_functionals'] if f['name'] == name) for name in ('K', 'u2')]
selected.append(next(f for f in face['three_constant_negative_mean_SAFE_identities'] if f['name'] == 'TRUE_SAFE_source5_Omean'))
data = []
for f, target in zip(selected, (Kvec, U, safe5)):
    beta = [F(f['signed_equation_multipliers'][name]) for name in labels]
    rem = vec(f['full513_off_support_remainder'])
    assert vec(f['full513_target_coefficients']) == target
    for j in range(513):
        assert target[j] == sum((b * e[j] for b, e in zip(beta, E)), F(0)) + rem[j]
        if j in ZR:
            assert rem[j] == 0
    assert dot(beta, H) == F(f['constant_on_optimal_face'])
    data.append((beta, rem, F(f['constant_on_optimal_face'])))

beta = [data[0][0][r] - 5 * data[1][0][r] + 5 * data[2][0][r] for r in range(14)]
beta[labels.index('PORTFOLIO25_i2_TC_QOmean')] += 12
beta[labels.index('C_maximum_size')] += 30
rem = [data[0][1][j] - 5 * data[1][1][j] + 5 * data[2][1][j] for j in range(513)]
constant = data[0][2] - 5 * data[1][2] + 5 * data[2][2]
assert constant == dot(beta, H) < 0
for j in range(513):
    assert expected[j] == sum((b * e[j] for b, e in zip(beta, E)), F(0)) + rem[j]
    if rem[j] != 0:
        assert old_residual[j] > 0
    if j in ZR:
        assert rem[j] == 0
z = list(map(F, primal['primal']))
assert dot(expected, z) == constant

face_result = {
    'status': 'PASS_NEW_UNCONDITIONAL_ROW_STRICTLY_NEGATIVE_ON_ENTIRE_OLD_OPTIMAL_FACE',
    'constant': str(constant), 'constant_decimal_display_only': float(constant),
    'equation_names': labels, 'equation_rhs': list(map(str, H)),
    'signed_equation_multipliers': {name: str(v) for name, v in zip(labels, beta)},
    'full513_row_coefficients': {str(j): str(v) for j, v in enumerate(expected)},
    'full513_off_support_remainder': {str(j): str(v) for j, v in enumerate(rem)},
    'zero_residual_columns': ZR,
    'identity': 'NS5(z)=constant+sum beta*(E*z-H)+sum remainder*z; remainder supported only where old optimum forces z=0.',
    'identity_columns_checked': 513,
    'new_optimization_performed': False,
}
(HERE / 'face_violation_certificate.json').write_text(json.dumps(face_result, indent=2) + '\n')
result = {
    'status': 'PASS_UNIVERSAL_TRUE_SOURCE2_NESTED_SOURCE5_SAFE_AND_ALL_FACE_VIOLATION',
    'theta': str(THETA), 'literal_hidden_states': 128, 'exact_minima': 8,
    'zero_residual_states_at_endpoint': sum(v == 0 for v in residuals.values()),
    'literal_six_query_menu_states': menu_checks,
    'affine_interval_exact_minimum': ['0', str(THETA)],
    'unique_finite_upper_endpoint_state': {'p': 0, 'c': 0, 'o': 1, 'tail': [0, 0, 1, 0]},
    'all513_unscaled_coefficients_rebuilt': 513,
    'full_hidden_payment_atom_checks': 512 * 16,
    'independent_K_column_checked': True,
    'C_size_free_multiplier_in_12_times_true_budget_identity': '29',
    'same_true_source5_payoff_used': True,
    'same_query_menu_for_both_means': True,
    'universal_scope': 'Any six legal query labels and their union; true actual source2 history; legal C attaining genuine global maximum naked size K.',
    'new_row': '300*u2+K-288*B-12*M-5*N>=0',
    'raw_row_numerical_divisor': '300',
    'whole_old_face_value': str(constant),
    'whole_old_face_identity_columns': 513,
    'whole_old_face_strictly_excluded': True,
    'new_global_optimum_or_quantified_improvement_claimed': False,
    'optimizer_calls': 0,
    'Main_builder_solver_or_prior_audit_code_executed_or_imported': False,
    'source_sha256': {'research/workspaces/six-boss1-20261111/' + name: digest for name, digest in PINS.items()},
    'outstanding_errors': [],
}
(HERE / 'audit_result.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
(HERE / 'independent_residuals.json').write_text(json.dumps(cases, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'literal_hidden_states', 'exact_minima',
    'literal_six_query_menu_states', 'all513_unscaled_coefficients_rebuilt',
    'whole_old_face_value', 'whole_old_face_strictly_excluded', 'outstanding_errors']}, indent=2))
