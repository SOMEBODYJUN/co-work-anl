#!/usr/bin/env python3
"""Exact derivation of three simultaneous true internal SAFE budgets.

No optimization, numerical library, or producer code is used.  The six
parameter facets are justified by literal states; all their vertices are
enumerated by rational 3x3 elimination and checked on all128 states.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from math import lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PINS = {
    'main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json':
        'a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba',
    'main_source2_maximum_nested_safe/proof.md':
        '1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067',
    'main_source2_maximum_nested_safe/manifest.json':
        '3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269',
    'visible_maximum_joint/exact_input.json':
        'b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33',
    'visible_maximum_joint_solve/exact_certificate.json':
        '8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347',
}
for name, digest in PINS.items():
    assert sha256((WS / name).read_bytes()).hexdigest() == digest, name


def read(name):
    return json.loads((WS / name).read_text())


def write(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def share(bit, prefix, following=0):
    return F(1, prefix + 1 + following) if bit else F(0)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def source_terms(p, c, menu, tail):
    r3, r4, r5, r6 = tail
    v2 = share(c, p, sum(tail))
    v6 = share(r6, p + c + r3 + r4 + r5)
    br6 = sum((share(q, p + c + r3 + r4 + r5) for q in menu), F(0)) / 6
    base = 25 * v2 + F(r3 + r4 + r5, 2) + r6 - v6 + br6
    increments = []
    for source in (3, 4, 5):
        k = source - 3
        actual = share(tail[k], p + c + sum(tail[:k]), sum(tail[k + 1:]))
        safe = sum((share(q, p + c + sum(tail[:k]), 6 - source)
                    for q in menu), F(0)) / 6
        increments.append(safe - actual)
    return base, increments


def target_terms(p, c, o):
    m0 = F(5, 2) * c + F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1))
    slopes = [F(o, 6 * (p + (source - 2) * c + 7 - source)) - F(c, 5)
              for source in (3, 4, 5)]
    return m0, slopes


# Each facet is a+b.theta>=0.  The first3 are allowed budget signs.
facets = [
    ('theta3_nonnegative', F(0), [F(1), F(0), F(0)]),
    ('theta4_nonnegative', F(0), [F(0), F(1), F(0)]),
    ('theta5_nonnegative', F(0), [F(0), F(0), F(1)]),
    ('cap5', F(5, 12), [F(0), F(0), F(-1)]),
    ('cap4', F(5, 12), [F(0), F(-1), -F(1, 36)]),
    ('cap3', F(5, 12), [F(-1), -F(1, 72), -F(1, 36)]),
]
states = {}
for p, c, o in product((0, 1), repeat=3):
    m0, target_slopes = target_terms(p, c, o)
    for tail in product((0, 1), repeat=4):
        base, inc = source_terms(p, c, (o, 0, 0, 0, 0, 0), tail)
        a = base - m0
        b = [v - t for v, t in zip(inc, target_slopes)]
        assert a >= 0
        states[p, c, o, tail] = (a, b, base, inc)
for name, tail in [('cap3', (1, 0, 0, 0)), ('cap4', (0, 1, 0, 0)), ('cap5', (0, 0, 1, 0))]:
    a, b, _, _ = states[0, 0, 1, tail]
    _, fa, fb = next(f for f in facets if f[0] == name)
    assert a == fa and b == fb


def solve3(rows):
    mat = [list(b) + [-a] for _, a, b in rows]
    for col in range(3):
        pivot = next((j for j in range(col, 3) if mat[j][col]), None)
        if pivot is None:
            return None
        mat[col], mat[pivot] = mat[pivot], mat[col]
        den = mat[col][col]
        mat[col] = [v / den for v in mat[col]]
        for j in range(3):
            if j != col:
                factor = mat[j][col]
                mat[j] = [v - factor * u for v, u in zip(mat[j], mat[col])]
    return tuple(mat[j][3] for j in range(3))


enumerated = set()
for triplet in combinations(facets, 3):
    theta = solve3(triplet)
    if theta is not None and all(a + dot(b, theta) >= 0 for _, a, b in facets):
        enumerated.add(theta)
vertices = {}
for e3, e4, e5 in product((0, 1), repeat=3):
    t5 = F(5, 12) * e5
    t4 = (F(5, 12) - t5 / 36) * e4
    t3 = (F(5, 12) - t4 / 72 - t5 / 36) * e3
    vertices['V%d%d%d' % (e3, e4, e5)] = (t3, t4, t5)
assert len(enumerated) == 8 and enumerated == set(vertices.values())
joint = vertices['V111']
assert joint == (F(12425, 31104), F(175, 432), F(5, 12))
vertex_checks = 0
for theta in vertices.values():
    for (p, c, o, tail), (a, b, base, inc) in states.items():
        assert a + dot(b, theta) >= 0
        vertex_checks += 1
    for p, c, o in product((0, 1), repeat=3):
        common_tail = (0, 0, 0, 0) if not c else (1, 1, 1, 1 - p)
        a, b, _, _ = states[p, c, o, common_tail]
        assert a + dot(b, theta) == 0
assert vertex_checks == 1024

# Exact nonnegative certificate for maximum total theta in this domain.
sum_weights = [F(2449, 2592), F(71, 72), F(1)]  # cap5,cap4,cap3
upper_facets = facets[3:]
assert [sum((w * b[k] for w, (_, a, b) in zip(sum_weights, upper_facets)), F(0))
        for k in range(3)] == [F(-1)] * 3
sum_upper = sum((w * a for w, (_, a, b) in zip(sum_weights, upper_facets)), F(0))
assert sum_upper == sum(joint) == F(37985, 31104)
assert all(w > 0 for w in sum_weights)

joint_states, minima = [], []
for p, c, o in product((0, 1), repeat=3):
    m0, slopes = target_terms(p, c, o)
    minimum = m0 + dot(joint, slopes)
    actual = {}
    for tail in product((0, 1), repeat=4):
        a, b, base, inc = states[p, c, o, tail]
        value = base + dot(joint, inc)
        residual = value - minimum
        assert residual == a + dot(b, joint) >= 0
        actual[tail] = value
        joint_states.append({'p': p, 'c': c, 'o': o, 'tail': list(tail),
                              'cost': str(value), 'minimum': str(minimum), 'residual': str(residual)})
    assert min(actual.values()) == minimum
    minima.append({'p': p, 'c': c, 'o': o, 'minimum': str(minimum),
                   'zero_states': [list(t) for t, v in actual.items() if v == minimum]})

# Check exact menu weakening as an affine identity in all three theta's.
menu_checks = 0
for p, c in product((0, 1), repeat=2):
    for menu in product((0, 1), repeat=6):
        d, o = sum(menu), int(any(menu))
        for tail in product((0, 1), repeat=4):
            base, inc = source_terms(p, c, menu, tail)
            weak, weak_inc = source_terms(p, c, (o, 0, 0, 0, 0, 0), tail)
            assert base - weak == F(d - o, 6 * (p + c + sum(tail[:3]) + 1)) >= 0
            for k, source in enumerate((3, 4, 5)):
                assert inc[k] - weak_inc[k] == F(d - o, 6 * (p + c + sum(tail[:k]) + 7 - source)) >= 0
            menu_checks += 1
assert menu_checks == 4096

inp = read('visible_maximum_joint/exact_input.json')
cert = read('visible_maximum_joint_solve/exact_certificate.json')
atoms = inp['atom_columns']
assert len(atoms) == 512 and inp['K_column'] == 512
U, B, M, N3, N4, N5, CS = ([F(0)] * 513 for _ in range(7))
NS = [N3, N4, N5]
for j, bits in enumerate(product((0, 1), repeat=9)):
    aa, x, o, c = bits[:6], bits[6], bits[7], bits[8]
    p = aa[0]
    assert atoms[j] == {'index': j, 'old_index': j // 2, 'a': list(aa), 'x': x, 'o': o, 'c': c}
    U[j] = share(aa[1], p, sum(aa[2:]))
    B[j], M[j], CS[j] = F(c, p + 5), F(o, 6 * (p + 4 * c + 1)), F(c)
    for vec, source in zip(NS, (3, 4, 5)):
        vec[j] = F(o, 6 * (p + (source - 2) * c + 7 - source))
K = [F(0)] * 512 + [F(1)]


def row(theta):
    total = sum(theta)
    return [25 * U[j] + total * K[j] / 5 - 24 * B[j] - M[j]
            - sum((t * n[j] for t, n in zip(theta, NS)), F(0)) for j in range(513)]


family = []
for name, theta in vertices.items():
    coeff = row(theta)
    family.append({'name': 'SOURCE2_MAXIMUM_C_INTERNAL_SAFE_' + name,
                   'family': 'TRUE_SAME_BRANCH_THREE_INTERNAL_SAFE',
                   'theta3_theta4_theta5': list(map(str, theta)),
                   'a': {str(j): str(v) for j, v in enumerate(coeff)},
                   'rhs': '0', 'numerical_divisor': '25'})
joint_row = next(r for r in family if r['name'].endswith('V111'))
joint_row = dict(joint_row, name='SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE')
raw_joint = row(joint)
scale = lcm(*(v.denominator for v in (*joint, sum(joint) / 5)))
assert scale == 31104
integer_row = dict(joint_row,
    name='SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE_INTEGER_WALLET',
    a={str(j): str(scale * v) for j, v in enumerate(raw_joint)},
    numerical_divisor=str(25 * scale), positive_scale_from_preferred_row=str(scale))
g = F(5, 2) - sum(joint) / 5
assert g == F(70163, 31104)
hidden_payment_checks = 0
for j, h in enumerate(atoms):
    p, c, o = h['a'][0], h['c'], h['o']
    for tail in product((0, 1), repeat=4):
        a, b, base, inc = states[p, c, o, tail]
        cost = base + dot(joint, inc)
        residual = a + dot(joint, b)
        assert raw_joint[j] == 25 * U[j] - cost + residual + g * c
        hidden_payment_checks += 1
assert raw_joint[512] == F(5, 2) - g == F(7597, 31104)

single = read('main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json')
single_vector = [F(single['a'][str(j)]) for j in range(513)]
assert row(vertices['V001']) == [v / 12 for v in single_vector]
old_p25 = [F(inp['raw_rows'][927]['a'].get(str(j), '0')) for j in range(513)]
assert inp['raw_rows'][927]['name'] == 'PORTFOLIO25_i2_TC_QOmean'
assert row(vertices['V000']) == [old_p25[j] + F(5, 2) * (CS[j] - K[j]) for j in range(513)]
for j in range(513):
    assert raw_joint[j] - row(vertices['V001'])[j] == joint[0] * (K[j] / 5 - N3[j]) + joint[1] * (K[j] / 5 - N4[j])
    assert scale * raw_joint[j] - 2592 * single_vector[j] == 5005 * K[j] - 12425 * N3[j] - 12600 * N4[j]

z = list(map(F, cert['primal']))
reference_values = {name: str(dot(row(theta), z)) for name, theta in vertices.items()}
best = min(F(v) for v in reference_values.values())
best_names = [name for name, value in reference_values.items() if F(value) == best]
assert best_names == ['V111']
comparison = {
    'scope': 'Exact substitution at the already frozen1002 reference point; no new1003 point is bound.',
    'input_sha256': PINS['visible_maximum_joint/exact_input.json'],
    'certificate_sha256': PINS['visible_maximum_joint_solve/exact_certificate.json'],
    'common_scale': 'coefficient of actual u2 equals25',
    'eight_vertex_slacks': reference_values,
    'strongest_vertex_at_this_point': best_names,
    'single_NS5_at_common_scale': reference_values['V001'],
    'joint_at_common_scale': reference_values['V111'],
    'joint_minus_single_at_common_scale': str(F(reference_values['V111']) - F(reference_values['V001'])),
    'joint_integer_wallet_slack': str(scale * F(reference_values['V111'])),
    'no_unconditional_pointwise_domination_claim': True,
    'exact_difference': 'Rjoint-Rsingle=theta3*(K/5-N3)+theta4*(K/5-N4)',
}

write('state_halfspaces.json', [
    {'p': p, 'c': c, 'o': o, 'tail': list(tail), 'constant': str(a),
     'theta3_theta4_theta5_coefficients': list(map(str, b))}
    for (p, c, o, tail), (a, b, base, inc) in states.items()])
write('parameter_polytope.json', {
    'scope': 'Complete nonnegative-theta domain for this specified affine exact minimum, not all possible SPE wallets.',
    'facets': [{'name': name, 'constant': str(a), 'theta_coefficients': list(map(str, b))} for name, a, b in facets],
    'vertices': {name: list(map(str, theta)) for name, theta in vertices.items()},
    'facet_triples_enumerated': 20, 'feasible_distinct_vertices': 8,
    'vertex_hidden_state_checks': vertex_checks,
    'necessity_witnesses': {'cap3': [0, 0, 1, 1, 0, 0, 0], 'cap4': [0, 0, 1, 0, 1, 0, 0], 'cap5': [0, 0, 1, 0, 0, 1, 0]},
    'unique_maximum_total_theta_vertex': 'V111', 'maximum_total_theta': str(sum_upper),
    'sum_bound_facet_weights_cap5_cap4_cap3': list(map(str, sum_weights)),
    'sufficiency': 'Every state residual affine in theta; nonnegative at all vertices of bounded six-facet polytope. A common exact minimizing tail exists for each p,c,o.'})
write('joint_hidden_states.json', joint_states)
write('joint_minimum_table.json', minima)
write('SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE.json', joint_row)
write('SOURCE2_MAXIMUM_C_JOINT_INTERNAL_SAFE_INTEGER_WALLET.json', integer_row)
write('eight_vertex_family.json', family)
write('comparison_frozen1002.json', comparison)
result = {
    'status': 'PASS_COMPLETE_THREE_WEIGHT_DOMAIN_AND_UNIVERSAL_JOINT_WALLET',
    'theta3_theta4_theta5': list(map(str, joint)), 'sum_theta': str(sum(joint)),
    'complete_parameter_domain_proved': True, 'parameter_vertices': 8,
    'hidden_affine_states': 128, 'vertex_hidden_state_checks': vertex_checks,
    'joint_exact_minima': 8, 'real_menu_affine_checks': menu_checks,
    'preferred_row_columns': 513, 'eight_vertex_family_coefficients': 8 * 513,
    'joint_hidden_payment_checks': hidden_payment_checks,
    'preferred_scale': 'actual u2 coefficient25; numerical_divisor25',
    'integer_wallet_scale': str(scale),
    'integer_wallet': {'u2': '777600', 'K': '7597', 'B': '746496', 'M': '31104', 'N3': '12425', 'N4': '12600', 'N5': '12960'},
    'free_C_size_multiplier_preferred': str(g), 'free_C_size_multiplier_integer': str(scale * g),
    'single_NS5_full513_identity_checked': True, 'P25_zero_vertex_full513_identity_checked': True,
    'comparison_to_frozen1002_point': comparison,
    'point_binding_to_unfrozen1003': False,
    'optimizer_calls': 0, 'Main_builder_solver_or_prior_audit_code_executed_or_imported': False,
    'source_sha256': {'research/workspaces/six-boss1-20261111/' + name: digest for name, digest in PINS.items()},
    'not_claimed': ['optimality among arbitrary SPE wallets', 'unconditional domination over single NS5', 'new global LP optimum', 'complete SPE realization', 'half theorem'],
    'outstanding_errors': [],
}
write('checker_output.json', result)
print(json.dumps({k: result[k] for k in ['status', 'theta3_theta4_theta5', 'parameter_vertices',
    'vertex_hidden_state_checks', 'real_menu_affine_checks', 'integer_wallet', 'outstanding_errors']}, indent=2))
