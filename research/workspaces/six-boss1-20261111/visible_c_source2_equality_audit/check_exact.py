#!/usr/bin/env python3
"""Independent source2 maximum-C equality audit and entire-face obstruction.

Standard-library exact arithmetic only.  No producer/Main/old audit program is
executed or imported.  No optimization is performed.  The conditional SAFE
rows below are conclusions under P25(C,Omean)=0, not unconditional LP rows.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PINS = {
    'visible_maximum_joint/exact_input.json':
        'b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33',
    'visible_maximum_joint/freeze_manifest.json':
        '31af8bc9ddfa35fd0a62b546cdf095fbd2cc76dfde76fc5ccfc010967f735966',
    'visible_maximum_joint_solve/exact_certificate.json':
        '8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347',
    'visible_maximum_joint_solve/freeze_manifest.json':
        '13a5a0206c1332433fa823d25be67cb6b1244375c0269c8e9dca7e3aef0dc98f',
    'visible_maximum_joint_solve/proof.md':
        '4414e3f0e8cb6e1754377f938fb4374f42aae8437afc2df1865a1a221f836480',
    'visible_maximum_joint/source_review.md':
        'e69440b5e52b528f540605a1fd3ddc833be99a48779b265e6389a9d615067b3a',
    'main_all_source25_family/proof.md':
        'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
}
for name, digest in PINS.items():
    assert sha256((WS / name).read_bytes()).hexdigest() == digest, name


def read(name):
    return json.loads((WS / name).read_text())


def share(bit, prefix, following=0):
    return F(1, prefix + 1 + following) if bit else F(0)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def vector(a):
    return [F(a.get(str(j), '0')) for j in range(513)]


def add_vector(*terms):
    return [sum((scale * v[j] for scale, v in terms), F(0))
            for j in range(513)]


def fstrings(values):
    return [str(x) for x in values]


# Literal source-payment cost: 25 IC2, three half caps, terminal cap,
# and the average of six BRs at the same terminal node.
def cost(p, c, menu, tail):
    s, z = sum(tail[:3]), tail[3]
    return (25 * share(c, p, s + z) + F(s, 2) + z
            - share(z, p + c + s)
            + sum((share(q, p + c + s) for q in menu), F(0)) / 6)


def pure_minimum(p, c, q):
    return F(5, 2) * c + F(24 * c, p + 5) + F(q, p + 1 + 4 * c)


allowed = {
    (0, 0): [(0, 0, 0, 0), (0, 0, 0, 1)],
    (1, 0): [(0, 0, 0, 0)],
    (0, 1): [(1, 1, 1, 1)],
    (1, 1): [(1, 1, 1, 0), (1, 1, 1, 1)],
}
literal_cases = zero_cases = 0
for p, c in product((0, 1), repeat=2):
    for menu in product((0, 1), repeat=6):
        d, o = sum(menu), int(any(menu))
        weak_min = F(5, 2) * c + F(24 * c, p + 5) + F(o, 6 * (p + 1 + 4 * c))
        real_min = sum((pure_minimum(p, c, q) for q in menu), F(0)) / 6
        overlap_slack = F(d - o, 6 * (p + 1 + 4 * c))
        assert real_min - weak_min == overlap_slack >= 0
        for tail in product((0, 1), repeat=4):
            phi = cost(p, c, menu, tail)
            residual = phi - weak_min
            assert phi - real_min >= 0 and residual >= 0
            expected_zero = d <= 1 and tail in allowed[p, c]
            assert (residual == 0) == expected_zero
            zero_cases += residual == 0
            literal_cases += 1
        assert min(cost(p, c, menu, tail) for tail in product((0, 1), repeat=4)) == real_min
assert literal_cases == 4096 and zero_cases == 42

# Per-customer identities on every permitted equality state.  E and F are
# customer sets, not separately selected marginal terminal completions.
payoff_cases = 0
for (p, c), tails in allowed.items():
    for tail in tails:
        s, z = sum(tail[:3]), tail[3]
        assert tail[:3] == (c, c, c)
        remove = p * c * (1 - z)
        insert = (1 - p) * (1 - c) * z
        assert z - c == insert - remove
        base = F(c, p + 5)
        forced = share(c, p, sum(tail))
        terminal = share(z, p + c + s)
        assert forced == base + F(remove, 30)
        assert terminal == base + insert - F(remove, 6)
        seq = (p, c) + tail
        for idx in (2, 3, 4):
            assert share(seq[idx], sum(seq[:idx]), sum(seq[idx + 1:])) == forced
        payoff_cases += 1
assert payoff_cases == 6

inp = read('visible_maximum_joint/exact_input.json')
cert = read('visible_maximum_joint_solve/exact_certificate.json')
assert cert['input_sha256'] == PINS['visible_maximum_joint/exact_input.json']
assert inp['variables'] == 513 and inp['K_column'] == 512
assert inp['nonnegative_columns'] == list(range(513))
assert len(inp['raw_rows']) == 1002 and len(inp['equalities']) == 2
assert inp['inequality_convention'] == 'a dot z >= rhs'
atoms = inp['atom_columns']
for j, bits in enumerate(product((0, 1), repeat=9)):
    assert atoms[j] == {'index': j, 'old_index': j // 2,
                        'a': list(bits[:6]), 'x': bits[6], 'o': bits[7], 'c': bits[8]}
rows = inp['raw_rows']
z = list(map(F, cert['primal']))
assert len(z) == 513 and all(v >= 0 for v in z)
U, B, M, O, CSIZE, A1, X, W = ([F(0)] * 513 for _ in range(8))
for j, h in enumerate(atoms):
    aa, p, c, o = h['a'], h['a'][0], h['c'], h['o']
    U[j] = share(aa[1], sum(aa[:1]), sum(aa[2:]))
    B[j] = F(c, p + 5)
    M[j] = F(o, 6 * (p + 4 * c + 1))
    O[j], CSIZE[j], A1[j], X[j] = map(F, (o, c, p, h['x']))
    W[j] = F(bool(sum(aa)))
K = [F(0)] * 512 + [F(1)]
assert W == vector(inp['objective'])
assert vector(inp['equalities'][0]['a']) == O
assert vector(inp['equalities'][1]['a']) == add_vector((1, CSIZE), (-1, K))
assert [F(e['rhs']) for e in inp['equalities']] == [F(1), F(0)]

roles = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'X', 'C', 'Omean']


def query(h, role):
    if role.startswith('A'):
        return F(h['a'][int(role[1:]) - 1])
    if role == 'X':
        return F(h['x'])
    if role == 'C':
        return F(h['c'])
    assert role == 'Omean'
    return F(h['o'], 6)


# Rebuild all nine C-forcing source2 rows, including the positive mean row.
p25_rows = {}
terminal_vectors = {}
for role in roles:
    name = 'PORTFOLIO25_i2_TC_Q' + role
    idx = next(j for j, r in enumerate(rows) if r['name'] == name)
    terminal = [query(h, role) / (h['a'][0] + 4 * h['c'] + 1) for h in atoms] + [F(0)]
    expected = add_vector((25, U), (-24, B), (-1, terminal),
                          (F(5, 2), K), (-F(5, 2), CSIZE))
    assert expected == vector(rows[idx]['a'])
    assert F(rows[idx]['rhs']) == 0
    assert F(rows[idx]['numerical_divisor']) == 25
    p25_rows[role] = idx
    terminal_vectors[role] = terminal
assert p25_rows['Omean'] == 927 and terminal_vectors['Omean'] == M

# Replay the released numeric certificate with exact arithmetic, as data.
# This is not another source audit of the other 993 original rows.
eq = [vector(e['a']) for e in inp['equalities']]
rhs = [F(e['rhs']) for e in inp['equalities']]
assert [dot(e, z) - h for e, h in zip(eq, rhs)] == [F(0), F(0)]
assert cert['equality_residuals'] == ['0', '0']
slacks = []
for j, row in enumerate(rows):
    slack = sum((F(v) * z[int(col)] for col, v in row['a'].items()), F(0)) - F(row['rhs'])
    assert slack == F(cert['raw_row_slacks'][j]) >= 0
    slacks.append(slack)
weights = list(map(F, cert['dual']['raw_row_weights']))
etas = list(map(F, cert['dual']['equality_multipliers']))
assert len(weights) == 1002 and len(etas) == 2 and all(y >= 0 for y in weights)
positive = [j for j, y in enumerate(weights) if y > 0]
assert positive == cert['dual']['positive_raw_indices']
assert positive == [46, 47, 65, 218, 221, 222, 640, 647, 654, 673, 868, 927]
assert weights[927] > 0 and slacks[927] == 0
positive_matrix = [vector(rows[j]['a']) for j in positive]
residual = [W[col] - sum((weights[idx] * v[col] for idx, v in zip(positive, positive_matrix)), F(0))
            - sum((eta * e[col] for eta, e in zip(etas, eq)), F(0)) for col in range(513)]
assert residual == list(map(F, cert['dual']['nonnegative_column_residual']))
assert all(r >= 0 for r in residual)
dual_value = sum((weights[j] * F(rows[j]['rhs']) for j in positive), F(0)) + dot(etas, rhs)
assert dual_value == dot(W, z) == F(cert['objective']) == F(cert['dual']['objective'])
assert all(y * s == 0 for y, s in zip(weights, slacks))
assert all(v * r == 0 for v, r in zip(z, residual))

conditional_safe = {}
point_safe = []
for source in (3, 4, 5):
    for role in roles:
        costs = [query(h, role) / (h['a'][0] + (source - 2) * h['c'] + 7 - source)
                 for h in atoms] + [F(0)]
        coeff = add_vector((1, U), (-1, costs))
        conditional_safe[source, role] = coeff
        value = dot(coeff, z)
        point_safe.append({'source': source, 'query': role, 'slack': str(value),
                           'negative': value < 0})
terminal_checks = []
for role in roles[:-1]:
    difference = add_vector((1, M), (-1, terminal_vectors[role]))
    assert difference == add_vector((1, vector(rows[p25_rows[role]]['a'])),
                                    (-1, vector(rows[927]['a'])))
    value = dot(difference, z)
    assert value >= 0
    terminal_checks.append({'query': role, 'slack': str(value),
                            'already_paid_by_existing_P25_difference': True})

delta_vec = add_vector((30, U), (-30, B))
delta = dot(delta_vec, z)
intersection = sum((h['a'][0] * h['c'] * z[j] for j, h in enumerate(atoms)), F(0))
outside = sum(((1 - h['a'][0]) * (1 - h['c']) * z[j] for j, h in enumerate(atoms)), F(0))
assert delta == F(6, 5) * (dot(M, z) - dot(B, z))
assert 0 <= delta <= min(intersection, outside)
assert dot(B, z) + F(5, 6) * delta == dot(M, z)

# Any optimizer attaining this exact lower bound has support only on ZR,
# all positive budgets tight, and both independent mass equations.  Work on
# this affine containing space; no face optimizer or all-face enumeration.
ZR = [j for j, r in enumerate(residual) if r == 0]
assert ZR == [0, 2, 3, 10, 11, 14, 15, 18, 19, 22, 23, 50, 51, 74, 75, 267,
              459, 467, 483, 499, 512]
for j in ZR:
    if j == 512:
        continue
    h = atoms[j]
    assert h['a'][0] <= h['c'] <= h['o']
    assert h['a'][0] * h['x'] == 0
E = positive_matrix + eq
H = [F(rows[j]['rhs']) for j in positive] + rhs
labels = [rows[j]['name'] for j in positive] + [e['name'] for e in inp['equalities']]
rr = [[row[j] for j in ZR] for row in E]
ops = [[F(i == j) for j in range(len(E))] for i in range(len(E))]
pivots = []
lead = 0
for col in range(len(ZR)):
    candidates = [r for r in range(lead, len(rr)) if rr[r][col]]
    if not candidates:
        continue
    pick = candidates[0]
    rr[lead], rr[pick] = rr[pick], rr[lead]
    ops[lead], ops[pick] = ops[pick], ops[lead]
    scale = rr[lead][col]
    rr[lead] = [v / scale for v in rr[lead]]
    ops[lead] = [v / scale for v in ops[lead]]
    for r in range(len(rr)):
        if r != lead and rr[r][col]:
            scale = rr[r][col]
            rr[r] = [v - scale * p for v, p in zip(rr[r], rr[lead])]
            ops[r] = [v - scale * p for v, p in zip(ops[r], ops[lead])]
    pivots.append(col)
    lead += 1
    if lead == len(rr):
        break
assert lead == 14
assert all(rr[r][pivots[s]] == F(r == s) for r in range(14) for s in range(14))
free = [ZR[j] for j in range(len(ZR)) if j not in pivots]
assert free == [0, 11, 15, 19, 23, 51, 75]


def certify_fixed(name, coefficients):
    current = [coefficients[j] for j in ZR]
    beta = [F(0)] * len(E)
    for r, col in enumerate(pivots):
        scale = current[col]
        current = [v - scale * p for v, p in zip(current, rr[r])]
        beta = [v + scale * p for v, p in zip(beta, ops[r])]
    assert current == [F(0)] * len(ZR), name
    constant = dot(beta, H)
    remainder = [coefficients[j] - sum((w * row[j] for w, row in zip(beta, E)), F(0))
                 for j in range(513)]
    assert all(remainder[j] == 0 for j in ZR)
    assert all(residual[j] > 0 for j in range(513) if remainder[j] != 0)
    assert dot(coefficients, z) == constant
    assert all(coefficients[j] == sum((w * row[j] for w, row in zip(beta, E)), F(0))
               + remainder[j] for j in range(513))
    return {'name': name, 'constant_on_optimal_face': str(constant),
            'signed_equation_multipliers': {label: str(v) for label, v in zip(labels, beta)},
            'full513_target_coefficients': {str(j): str(v) for j, v in enumerate(coefficients)},
            'full513_off_support_remainder': {str(j): str(v) for j, v in enumerate(remainder)},
            'identity_columns_checked': 513,
            'identity': 'target(z)=constant+sum beta*(E*z-H)+sum remainder_j*z_j; remainder vanishes on every residual-zero column.'}


fixed = []
for name, coeff in [('K', K), ('u2', U), ('size_A1', A1), ('size_X', X),
                     ('B', B), ('M', M), ('delta', delta_vec)]:
    fixed.append(certify_fixed(name, coeff))
mean_safe_fixed = []
for src in (3, 4, 5):
    item = certify_fixed('TRUE_SAFE_source%d_Omean' % src,
                         conditional_safe[src, 'Omean'])
    assert F(item['constant_on_optimal_face']) < 0
    mean_safe_fixed.append(item)

# On A1 subset C subset O the source5 mean cost has this elementary form.
simple_s5 = add_vector((1, U), (-F(1, 12), O), (F(1, 20), K), (F(1, 180), A1))
for j in ZR:
    # K and sum C are equal through the independent C-size equation.
    assert conditional_safe[5, 'Omean'][j] == simple_s5[j] + F(1, 20) * (CSIZE[j] - K[j])
simple_item = certify_fixed('source5_mean_simplified', simple_s5)
assert simple_item['constant_on_optimal_face'] == mean_safe_fixed[2]['constant_on_optimal_face']
fixed.append(simple_item)

# Check constancy of all nonzero old visible marginals without assuming it
# from the producer's face parameterization.  The all-zero mass remains free.
old_marginals = {}
for old in range(1, 256):
    coeff = [F(0)] * 513
    coeff[2 * old] = coeff[2 * old + 1] = F(1)
    cur = [coeff[j] for j in ZR]
    for r, col in enumerate(pivots):
        scale = cur[col]
        cur = [v - scale * p for v, p in zip(cur, rr[r])]
    assert cur == [F(0)] * len(ZR)
    old_marginals[str(old)] = str(dot(coeff, z))

point_values = {'u2': str(dot(U, z)), 'B': str(dot(B, z)), 'M': str(dot(M, z)),
                'K': str(z[512]), 'A1_intersect_C': str(intersection),
                'outside_A1_union_C_capacity': str(outside), 'delta': str(delta),
                'source2_safe_C': str(dot(U, z) - dot(B, z)),
                'terminal_payoff': str(dot(M, z))}
face_certificate = {
    'status': 'PASS_ENTIRE_OPTIMAL_FACE_EXCLUDED_BY_TRUE_INTERMEDIATE_MEAN_SAFE',
    'input_sha256': PINS['visible_maximum_joint/exact_input.json'],
    'certificate_sha256': PINS['visible_maximum_joint_solve/exact_certificate.json'],
    'optimal_objective': str(dual_value), 'positive_raw_indices': positive,
    'equation_names': labels, 'equation_rhs': fstrings(H),
    'zero_residual_columns': ZR, 'forced_zero_column_count': 513 - len(ZR),
    'restricted_equation_rank': lead, 'affine_containing_space_free_coordinates': free,
    'actual_feasible_face_dimension_claimed': False,
    'support_consequences': ['A1 subset C subset O', 'A1 intersect X empty'],
    'fixed_functionals': fixed, 'three_constant_negative_mean_SAFE_identities': mean_safe_fixed,
    'all255_nonzero_old_marginals_fixed': old_marginals,
    'all_zero_old_mass_may_vary': True,
    'signed_identity_scope': 'Only on the optimal face: twelve positive original rows are tight; both mass equalities hold; other 492 columns vanish by complementary slackness.',
    'new_uniformly_larger_universal_bound_claimed': False,
    'optimizer_calls': 0,
}
(HERE / 'face_exclusion_certificate.json').write_text(json.dumps(face_certificate, indent=2) + '\n')

result = {
    'status': 'PASS_SOURCE2_P25_EQUALITY_STRUCTURE_AND_WHOLE_FACE_EXCLUSION',
    'literal_p_c_menu_tail_cases': literal_cases, 'zero_cases': zero_cases,
    'allowed_tail_states': {str(k): [list(t) for t in v] for k, v in allowed.items()},
    'per_customer_equality_payoff_checks': payoff_cases,
    'd_equals_o_proved': True,
    'source2_forced_C_pure_and_mean_rows_rebuilt': 9,
    'source_row_coefficient_comparisons': 9 * 513,
    'released_primal_raw_rows_checked': 1002,
    'released_dual_columns_checked': 513,
    'released_equalities_checked': 2,
    'released_primal_dual_gap': '0',
    'positive_C_mean_row_raw_index': 927,
    'positive_C_mean_row_weight': str(weights[927]),
    'point_values': point_values,
    'conditional_true_intermediate_SAFE_checks': point_safe,
    'terminal_existing_P25_checks': terminal_checks,
    'entire_optimal_face_excluded': True,
    'whole_face_constant_mean_SAFE': {str(src): item['constant_on_optimal_face']
                                    for src, item in zip((3, 4, 5), mean_safe_fixed)},
    'entire_face_source5_mean_violation': mean_safe_fixed[2]['constant_on_optimal_face'],
    'independent_face_rank': lead, 'affine_containing_free_coordinates': free,
    'source_sha256': {'research/workspaces/six-boss1-20261111/' + p: h for p, h in PINS.items()},
    'optimizer_calls': 0,
    'Main_builder_solver_or_prior_audit_code_executed_or_imported': False,
    'not_claimed': ['unconditional validity of conditional SAFE rows',
                    'new quantified universal lower bound beyond the released optimum',
                    'new LP or phase-I solution', 'SPE construction', 'half theorem'],
    'outstanding_errors': [],
}
(HERE / 'audit_result.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'literal_p_c_menu_tail_cases',
    'source_row_coefficient_comparisons', 'whole_face_constant_mean_SAFE',
    'entire_optimal_face_excluded', 'independent_face_rank', 'outstanding_errors']}, indent=2))
