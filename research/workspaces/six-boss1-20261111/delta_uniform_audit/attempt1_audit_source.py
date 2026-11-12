#!/usr/bin/env python3
"""Independent Fraction replay; no producer imports and no optimization.

This program writes only its own delta_uniform_audit directory.  The proofs
and frozen JSON inputs supply mathematical data, never executable code.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json

OUT = Path(__file__).resolve().parent
WS = OUT.parent
REPO = WS.parents[2]
AGENT = '/root/delta_uniform_audit'
RUN = 'six-boss1-20261111'
AUDIT_ID = 'B1-DELTA-UNIFORM-AUDIT-20261112'
PINS = {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(rel):
    p = WS / rel
    PINS[rel] = digest(p)
    return p


def read(rel):
    return json.loads(pin(rel).read_text())


def enc(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, Path):
        return str(x)
    raise TypeError(type(x).__name__)


def write(name, obj):
    assert '/' not in name and name.endswith('.json')
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2,
                                     default=enc) + '\n')


def decimal(q):
    with localcontext() as ctx:
        ctx.prec = 70
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def dense(sparse, n):
    return [F(sparse.get(str(j), '0')) for j in range(n)]


def sparse(v):
    return {str(j): x for j, x in enumerate(v) if x}


def frac_share(member, load):
    assert member == 0 or load > 0
    return F(member, load) if load else F(0)


def check_vector(actual, expected, label):
    assert len(actual) == len(expected), label
    bad = [(i, a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
    assert not bad, (label, bad[:3])


# Every frozen Main byte, including its failed first attempt, is protected.
main_freeze = read('main_delta_uniform_improvement/freeze_manifest.json')
for rel, expected in main_freeze['artifacts'].items():
    assert digest(pin(rel)) == expected, ('Main freeze mismatch', rel)
for p in (WS / 'main_delta_uniform_improvement').rglob('*'):
    if p.is_file():
        pin(str(p.relative_to(WS)))
for rel in [
    'visible_maximum_joint_v5_solve/proof.md',
    'source2_minimal_cap_safe/proof.md',
    'registration/stage19-root270-addition.md',
    'maximal_root_tail_wallet_v3/proof.md',
    'maximal_root_tail_wallet_v3/source_review.md',
    'visible_c_source2_equality_audit/root270_formula_erratum.md',
]:
    pin(rel)
model_path = REPO / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
assert model_path.is_file(), model_path
PINS['../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'] = digest(model_path)

inp = read('visible_maximum_joint_v5/exact_input.json')
old = read('visible_maximum_joint_v5_solve/exact_certificate.json')
root_inp = read('maximal_root_tail_wallet_v3/exact_input.json')
root_cert = read('maximal_root_tail_wallet_v3/exact_certificate.json')
main = read('main_delta_uniform_improvement/exact_certificate.json')
main_states = read('main_delta_uniform_improvement/all256_true_delta_state_checks.json')
main_cuts = read('main_delta_uniform_improvement/two_true_delta_cuts.json')
main_root = read('main_delta_uniform_improvement/root131_replay.json')
main_columns = read('main_delta_uniform_improvement/all513_global_identity_checks.json')

assert old['input_sha256'] == PINS['visible_maximum_joint_v5/exact_input.json']
assert root_cert['input_sha256'] == PINS['maximal_root_tail_wallet_v3/exact_input.json']
assert inp['variables'] == 513 and inp['K_column'] == 512
assert inp['bit_order'] == ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'x', 'o', 'c']
assert inp['nonnegative_columns'] == list(range(513))
assert len(inp['raw_rows']) == 3056 and len(inp['equalities']) == 2
atoms = inp['atom_columns']
assert len(atoms) == 512
for j, t in enumerate(atoms):
    bits = [int(c) for c in f'{j:09b}']
    assert t['index'] == j and t['a'] + [t['x'], t['o'], t['c']] == bits

W = [F(int(any(t['a']))) for t in atoms] + [F(0)]
O = [F(t['o']) for t in atoms] + [F(0)]
EC = [F(t['c']) for t in atoms] + [F(-1)]
K = [F(0)] * 512 + [F(1)]
check_vector(dense(inp['objective'], 513), W, 'actual welfare all columns')
check_vector(dense(inp['equalities'][0]['a'], 513), O, 'O normalization')
check_vector(dense(inp['equalities'][1]['a'], 513), EC, 'C size equality')
assert [F(e['rhs']) for e in inp['equalities']] == [F(1), F(0)]

# Recompute the original dual and primal directly from coefficient strings.
rows = inp['raw_rows']
y = list(map(F, old['dual']['raw_row_weights']))
eta_o, eta_c = map(F, old['dual']['equality_multipliers'])
alpha = F(old['objective'])
assert len(y) == 3056 and min(y) >= 0
rhs = [F(r['rhs']) for r in rows]
assert sum(b == -1 for b in rhs) == 30
assert set(rhs) == {F(-1), F(0)}
affine_payment = sum((yy * bb for yy, bb in zip(y, rhs)), F(0))
assert affine_payment == 0 and alpha == eta_o + affine_payment
all_original_slacks = []
primal = list(map(F, old['primal']))
assert len(primal) == 513 and min(primal) >= 0
positive_primal = {str(i): x for i, x in enumerate(primal) if x}
original_sum = [F(0)] * 513
matrix_entries_read = 0
affine_records = []
all_row_records = []
for i, row in enumerate(rows):
    assert F(row['numerical_divisor']) > 0
    parsed = {k: F(v) for k, v in row['a'].items()}
    assert all(0 <= int(k) <= 512 for k in parsed)
    matrix_entries_read += len(parsed)
    if y[i]:
        for k, value in parsed.items():
            original_sum[int(k)] += y[i] * value
    slack = sum((parsed.get(k, F(0)) * x for k, x in positive_primal.items()), F(0)) - rhs[i]
    assert slack >= 0 and slack == F(old['raw_row_slacks'][i])
    assert y[i] * slack == 0
    all_original_slacks.append(slack)
    record = {'raw_index': i, 'name': row['name'], 'rhs': rhs[i],
              'old_payment': y[i], 'primal_slack': slack,
              'homogenization': 'A_i dot z - rhs_i * |O|'}
    all_row_records.append(record)
    if rhs[i]:
        av = [parsed.get(str(j), F(0)) - rhs[i] * O[j] for j in range(513)]
        assert y[i] == 0
        affine_records.append({**record, 'homogeneous_coefficients': sparse(av)})

old_residual = [W[j] - original_sum[j] - eta_o * O[j] - eta_c * EC[j]
                for j in range(513)]
check_vector(old_residual, list(map(F, old['dual']['nonnegative_column_residual'])),
             'original residual full513')
assert min(old_residual) >= 0
assert all(old_residual[j] * primal[j] == 0 for j in range(513))
assert sum((W[j] * primal[j] for j in range(513)), F(0)) == alpha
assert sum((O[j] * primal[j] for j in range(513)), F(0)) == 1
assert sum((EC[j] * primal[j] for j in range(513)), F(0)) == 0
write('original3056_replay.json', {
    'status': 'PASS', 'optimizer_calls': 0, 'rows_retained': 3056,
    'columns_retained': 513, 'stored_coefficient_strings_parsed': matrix_entries_read,
    'equality_multipliers_are_free': True, 'eta_O': eta_o, 'eta_C': eta_c,
    'alpha': alpha, 'affine_rhs_payment': affine_payment,
    'rhs_minus_one_count': len(affine_records), 'all_raw_rows': all_row_records,
    'nonnegative_column_residual': old_residual,
    'primal_and_dual_objectives_match': True,
})
write('all30_affine_homogenizations.json', affine_records)

# Rebuild the second-source budgets directly, independently of Main's code.
tau0 = [F(0), F(5977, 6912), F(43, 48)]
epsilon = F(1, 144)
tau = [tau0[0], tau0[1] - epsilon, tau0[2] + epsilon]
sstar = F(61273, 6912)


def caps(weights):
    return [F(1, 12) + weights[k] +
            sum((weights[l] / (6 * (4 - l) * (5 - l)) for l in range(k + 1, 3)), F(0))
            for k in range(3)]


beta0, beta = caps(tau0), caps(tau)
S0, S = F(1) + sum(beta0), F(1) + sum(beta)
assert S0 == F(1528993, 497664) and S - S0 == epsilon / 24
assert tau == [F(0), F(5929, 6912), F(65, 72)]
assert min(tau) >= 0 and min(beta) > 0


def cost_parts(p, c, o_or_d, tail, s, weights, hats):
    """o_or_d is a true six-label membership count, or its union bound."""
    a = F(25) + sum(weights) - s
    load = p + c + sum(tail)
    parts = {
        'source_IC_cost': a * frac_share(c, load),
        'middle_CAP_cost': sum((hats[k] * tail[k] for k in range(3)), F(0)),
        'last_CAP_cost': F(tail[3]),
        'last_BR_income_credit': -frac_share(tail[3], load),
        'internal_SAFE_income_credit': -sum((weights[k] * frac_share(tail[k], load)
                                            for k in range(3)), F(0)),
        'last_six_query_cost': F(o_or_d, 6 * (p + c + sum(tail[:3]) + 1)),
        'internal_six_query_cost': sum((weights[k] * F(o_or_d,
             6 * (p + c + sum(tail[:k]) + 4 - k)) for k in range(3)), F(0)),
    }
    return parts


def anchor(p, c, o, s, weights, total_cap):
    return c * (total_cap + F(24, p + 5) - s / 5) + F(o, 6 * (p + 4 * c + 1)) + sum(
        (weights[k] * F(o, 6 * (p + (k + 1) * c + 4 - k)) for k in range(3)), F(0))


state_checks, all_cut_vectors, cut_records = [], [], []
menu_count = 0
menu_min = None
for sid, s in enumerate([F(0), sstar]):
    a = F(25) + sum(tau) - s
    assert a > 0
    tables = []
    min_lookup = {}
    for p, c, o in product([0, 1], repeat=3):
        table = []
        old_costs = []
        for tail in product([0, 1], repeat=4):
            parts = cost_parts(p, c, o, tail, s, tau, beta)
            val = sum(parts.values(), F(0))
            load = p + c + sum(tail)
            num = a * c - tail[3] - sum((tau[k] * tail[k] for k in range(3)), F(0))
            assert load > 0 or num == 0
            formula = ((num / load) if load else F(0)) + sum(
                (beta[k] * tail[k] for k in range(3)), F(0)) + tail[3] + F(
                o, 6 * (p + c + sum(tail[:3]) + 1)) + sum(
                (tau[k] * F(o, 6 * (p + c + sum(tail[:k]) + 4 - k))
                 for k in range(3)), F(0))
            assert val == formula
            table.append({'tail': list(tail), 'cost': val, 'budget_parts': parts})
            old_costs.append(sum(cost_parts(p, c, o, tail, s, tau0, beta0).values(), F(0)))
        minimum = min(t['cost'] for t in table)
        old_minimum = min(old_costs)
        assert old_minimum == anchor(p, c, o, s, tau0, S0)
        loss = F(p * c * (1 - o), 180)
        if s:
            loss += F(101 * (1 - p) * c * (1 - o), 27648)
        assert minimum == anchor(p, c, o, s, tau, S) - loss
        tails = [t['tail'] for t in table if t['cost'] == minimum]
        for t in table:
            t['residual_to_minimum'] = t['cost'] - minimum
            assert t['residual_to_minimum'] >= 0
        main_table = main_states[sid]['states'][len(tables)]
        assert main_table['pco'] == [p, c, o]
        assert F(main_table['minimum']) == minimum
        assert main_table['all_weak_tails'] == tails
        assert F(main_table['loss_from_shifted_anchor']) == loss
        for mine, theirs in zip(table, main_table['all_costs']):
            assert mine['tail'] == theirs['tail']
            assert mine['cost'] == F(theirs['cost'])
            assert mine['residual_to_minimum'] == F(theirs['residual_to_minimum'])
        tables.append({'pco': [p, c, o], 'minimum': minimum,
                       'old_minimum': old_minimum, 'loss_from_shifted_anchor': loss,
                       'all_weak_tails': tails, 'all_costs': table})
        min_lookup[p, c, o] = minimum
    # All actual six-query patterns, including empty and repeated-index membership.
    for p, c in product([0, 1], repeat=2):
        for tail in product([0, 1], repeat=4):
            for menu in product([0, 1], repeat=6):
                d, o = sum(menu), int(any(menu))
                actual_cost = sum(cost_parts(p, c, d, tail, s, tau, beta).values(), F(0))
                union_cost = sum(cost_parts(p, c, o, tail, s, tau, beta).values(), F(0))
                kernel = F(1, p + c + sum(tail[:3]) + 1) + sum(
                    (tau[k] / (p + c + sum(tail[:k]) + 4 - k) for k in range(3)), F(0))
                gap = F(d - o, 6) * kernel
                assert actual_cost - union_cost == gap and gap >= 0 and kernel > 0
                menu_min = gap if menu_min is None else min(menu_min, gap)
                menu_count += 1
    mu = S - s / 5  # unrestricted sign; this is not a paid inequality.
    cv = []
    before_cv = []
    identities = []
    for j, t in enumerate(atoms):
        p, c, o = t['a'][0], t['c'], t['o']
        u2 = frac_share(t['a'][1], sum(t['a']))
        from_budget = a * u2 - min_lookup[p, c, o] + mu * c
        loss = F(p * c * (1 - o), 180)
        if s:
            loss += F(101 * (1 - p) * c * (1 - o), 27648)
        explicit = a * u2 - F(24 * c, p + 5) - F(o, 6 * (p + 4 * c + 1)) - sum(
            (tau[k] * F(o, 6 * (p + (k + 1) * c + 4 - k)) for k in range(3)), F(0)) + loss
        old_row = a * u2 - F(24 * c, p + 5) - F(o, 6 * (p + 4 * c + 1)) - sum(
            (tau0[k] * F(o, 6 * (p + (k + 1) * c + 4 - k)) for k in range(3)), F(0))
        assert from_budget == explicit
        cv.append(explicit)
        before_cv.append(old_row)
        identities.append({'column': j, 'from_true_budget': from_budget,
                           'conditional_row': explicit, 'difference': from_budget - explicit})
    cv.append(S - mu)
    before_cv.append(s / 5)
    assert cv[-1] == s / 5
    identities.append({'column': 512, 'from_true_budget': S - mu,
                       'conditional_row': s / 5, 'difference': F(0)})
    assert cv == dense(main_cuts[sid]['a_coefficients'], 513)
    assert F(main_cuts[sid]['free_C_equality_multiplier']) == mu
    check_vector(before_cv,
                 [F(rows[2606]['a'].get(str(j), '0')) + S0 * EC[j] for j in range(513)]
                 if not s else dense(rows[1803]['a'], 513),
                 'original C-only identity')
    all_cut_vectors.append(cv)
    cut_records.append({'name': 'C_DELTA_EPS_S0' if not s else 'C_DELTA_EPS_SSTAR',
                        's': s, 'tau': tau, 'a': a, 'beta': beta, 'S': S,
                        'free_C_equality_multiplier': mu,
                        'coefficients': sparse(cv), 'all513_budget_identity_checks': identities})
    state_checks.append({'s': s, 'states': tables})
assert menu_count == 8192
write('all256_true_delta_state_checks.json', state_checks)
write('two_true_delta_cuts.json', cut_records)
write('true_delta_budget_summary.json', {
    'status': 'PASS', 'hidden_states': 256, 'all_weak_minimum_tables': 16,
    'all_actual_six_query_patterns_checked': menu_count, 'minimum_menu_gap': menu_min,
    'all513_budget_identity_columns': 1026, 'old_tau': tau0, 'new_tau': tau,
    'epsilon': epsilon, 'S0': S0, 'S': S, 'S_difference': S - S0,
    'all_paid_budget_weights_nonnegative': True,
    'equality_multiplier_has_no_sign_constraint': True,
    'Main_state_and_cut_data_match': True,
})

# Root rows are rebuilt from their true-wallet formulas before their weights
# or residuals are used.  In particular C30 is recomputed from 2048 states.
root_names = ['ROOT_IC'] + [f'CAP_B{i}' for i in range(2, 7)] + [
    'SAFE_j6|Omean', 'PAIR30|Omean|Omean',
    'OPT_SOURCE3_REQUERY_30_CUT', 'PORTFOLIO25_i4|T=B6|Q=Omean']
root_ints = [67510295447690880, 622403086173831, 3736778489617071,
             3696167188982850, 3608286607200810, 3553563630176244,
             1712829042623520, 2292281651099340, 24602518440, 61096128288912]
DB = F(67510295447690880)
root_y = {n: F(w) / DB for n, w in zip(root_names, root_ints)}
root_pi_c = F(22380459227386502) / DB
root_pi_o = F(1349360725088052) / DB
assert root_y == {n: F(v) for n, v in root_cert['dual']['original_unscaled_row_weights'].items()}
assert root_pi_c == F(root_cert['dual']['equality_C_size'])
assert root_pi_o == F(root_cert['dual']['equality_OPT_union'])
assert min(root_y.values()) > 0
root_rows = {n: [F(0)] * 129 for n in root_names}
root_rows['ROOT_IC'][128] = F(1)
c30_tables, c30_states = [], []
c30_menu_count = 0
for h, bits in enumerate(product([0, 1], repeat=7)):
    c, b2, b3, b4, b5, b6, o = bits
    ell, load = bits[:6], sum(bits[:6])
    v = [frac_share(x, load) for x in ell]
    root_rows['ROOT_IC'][h] = -v[0]
    for i in range(2, 7):
        root_rows[f'CAP_B{i}'][h] = -F(ell[i - 1])
    root_rows['SAFE_j6|Omean'][h] = v[5] - F(o, 6 * (sum(ell[:5]) + 1))
    D = 1 + sum(ell[:4])
    root_rows['PAIR30|Omean|Omean'][h] = v[4] + v[5] + F(b5, D * (D + 1)) - F(o, 3 * D)
    b = c + b2
    qtables = []
    for q in [0, 1]:
        values = []
        for r, yy, tt in product([0, 1], repeat=3):
            DD = 1 + b + q + r
            parts = [F(126000 * q, b + 1 + r + yy + tt),
                     F(43 * r + 31218 * yy + 34458 * tt, b + b3 + 3),
                     F(1654 * (r + yy + tt), b + b3 + b4 + b5 + 1),
                     F(5400) * (F(o, 6) - tt) / (DD + yy),
                     F(7740) * (F(o, 3 * DD) - F(yy, DD + tt) - F(tt, DD + yy)
                                 - F(yy, DD * (DD + 1)))]
            val = sum(parts, F(0))
            values.append({'q': q, 'tail': [r, yy, tt], 'cost': val, 'five_cost_parts': parts})
        amin = min(z['cost'] for z in values)
        for z in values:
            z['residual_to_q_minimum'] = z['cost'] - amin
            assert z['residual_to_q_minimum'] >= 0
        qtables.append({'q': q, 'minimum': amin,
                        'all_weak_tails': [z['tail'] for z in values if z['cost'] == amin]})
        c30_states.extend({'root_type': h, 'bits': list(bits), **z} for z in values)
    a0, a1 = [z['minimum'] for z in qtables]
    envelope = a0 if not o else min((5 * a0 + a1) / 6, a1)
    for menu in product([0, 1], repeat=6):
        if int(any(menu)) != o:
            continue
        avg = a0 + F(sum(menu), 6) * (a1 - a0)
        assert avg >= envelope
        c30_menu_count += 1
    c30_tables.append({'root_type': h, 'bits': list(bits), 'q_minima': qtables,
                       'complete_menu_envelope': envelope,
                       'free_constant_a0_may_have_either_sign': a0})
    root_rows['OPT_SOURCE3_REQUERY_30_CUT'][h] = 126000 * v[2] + 65719 * v[3] + 4962 * v[5] - envelope
    p = c + b2 + b3
    p25_cost = (F(3, 2) + F(24, p + 3)) * b6 + F(o, 6 * (p + 1 + 2 * b6))
    root_rows['PORTFOLIO25_i4|T=B6|Q=Omean'][h] = 25 * v[3] - p25_cost
assert len(c30_states) == 2048 and c30_menu_count == 4096
pair_menu_checks = []
for D in range(1, 6):
    for menu in product([0, 1], repeat=6):
        d, o = sum(menu), int(any(menu))
        actual = F(d, 3 * D) - F(d * (d - 1), 30 * D * (D + 1))
        weakened = F(o, 3 * D)
        assert actual >= weakened
        pair_menu_checks.append({'D': D, 'menu': list(menu), 'actual_cost': actual,
                                 'union_cost': weakened, 'gap': actual - weakened})
p25_checks = []
for p in range(4):
    for t, q in product([0, 1], repeat=2):
        vals = []
        for r, z in product([0, 1], repeat=2):
            L = p + t + r + z
            numerator = 25 * t - z
            assert L > 0 or numerator == 0
            cost = (F(numerator, L) if L else F(0)) + F(r, 2) + z + F(q, p + t + r + 1)
            vals.append({'tail': [r, z], 'cost': cost})
        minimum = F(3 * t, 2) + F(24 * t, p + 3) + F(q, p + 1 + 2 * t)
        assert min(z['cost'] for z in vals) == minimum
        p25_checks.append({'p': p, 't': t, 'q': q, 'minimum': minimum,
                           'all_weak_tails': [z['tail'] for z in vals if z['cost'] == minimum],
                           'all_four_hidden_states': vals})

root_input_rows = {r['name']: r for r in root_inp['raw_rows']}
root_input_matches = []
for name in root_names:
    check_vector(root_rows[name], dense(root_input_rows[name]['a'], 129), 'root row ' + name)
    expected_bk = F(-1) if name.startswith('CAP_') else F(-3, 2) if name.startswith('PORTFOLIO') else F(0)
    assert F(root_input_rows[name]['bK']) == expected_bk
    assert F(root_input_rows[name]['bO']) == 0
    root_input_matches.append({'name': name, 'columns': 129, 'all_differences_zero': True,
                               'K_rhs': expected_bk, 'O_rhs': F(0), 'payment': root_y[name]})
root_a = root_pi_c + sum((root_y[n] * F(root_input_rows[n]['bK']) for n in root_names), F(0))
root_b = root_pi_o
assert root_a == F(883952004100291, 8438786930961360)
assert root_b == F(37482242363557, 1875285984658080)
root_residual = []
for h in range(129):
    c, o = (root_inp['atoms'][h]['bits'][0], root_inp['atoms'][h]['bits'][6]) if h < 128 else (0, 0)
    val = F(h == 128) - sum((root_y[n] * root_rows[n][h] for n in root_names), F(0)) - root_pi_c * c - root_pi_o * o
    assert val >= 0
    root_residual.append(val)
check_vector(root_residual, dense(root_cert['dual']['column_residuals'], 129), 'original root residual')
check_vector(root_residual, list(map(F, main_root['all129_remainders'])), 'Main root residual')
outside_root = [h for h, t in enumerate(root_inp['atoms']) if t['bits'][0] and not t['bits'][6]]
root_eta = min(root_residual[h] for h in outside_root)
assert root_eta == F(1087978231314917, 84387869309613600)
assert root_eta == F(main_root['root_eta'])
root_strong_residual = [r - (root_eta if h in outside_root else 0) for h, r in enumerate(root_residual)]
assert min(root_strong_residual) >= 0
root131 = []
for h in range(131):
    if h < 129:
        c, o = (root_inp['atoms'][h]['bits'][0], root_inp['atoms'][h]['bits'][6]) if h < 128 else (0, 0)
        lhs = F(h == 128) - root_eta * c * (1 - o)
        rv = sum((root_y[n] * root_rows[n][h] for n in root_names), F(0)) + root_strong_residual[h] + root_pi_c * c + root_pi_o * o
    elif h == 129:
        lhs = -root_a
        rv = -sum((root_y[n] * F(root_input_rows[n]['bK']) for n in root_names), F(0)) - root_pi_c
    else:
        lhs = -root_b
        rv = -root_pi_o
    assert lhs == rv
    root131.append({'column': h if h < 128 else ['u', 'K', 'O'][h - 128],
                    'left': lhs, 'right': rv, 'identity_difference': lhs - rv})
root_global = []
for t in atoms:
    root_global.append(frac_share(t['a'][0], sum(t['a'])) - root_b * t['o'])
root_global.append(-root_a)
check_vector(root_global, dense(rows[868]['a'], 513), 'raw868 ROOT270 mapping')
write('root_true_budget_reconstruction.json', {
    'status': 'PASS', 'positive_row_count': 10, 'original_row_input_comparisons': root_input_matches,
    'C30_all2048_states': c30_states, 'C30_all128_envelopes': c30_tables,
    'C30_all_actual_six_query_patterns_checked': c30_menu_count,
    'PAIR30_all320_menu_states': pair_menu_checks,
    'P25_source4_all64_hidden_states_in_16_tables': p25_checks,
    'arbitrary_six_legal_queries': True, 'OPT_union_upper_cap_payment': F(0),
    'new_source1_IC_payment': F(0),
})
write('root131_replay.json', {
    'status': 'PASS', 'a': root_a, 'b': root_b, 'eta': root_eta,
    'integer_budget_denominator': DB, 'positive_budget_weights': root_y,
    'free_C_multiplier': root_pi_c, 'free_O_multiplier': root_pi_o,
    'all129_original_residuals': root_residual,
    'all129_strengthened_residuals': root_strong_residual,
    'outside_minimum_types': [h for h in outside_root if root_residual[h] == root_eta],
    'all131_strong_identity_checks': root131,
    'all513_raw868_mapping_checked': True,
})

# Six actual SAFE(C) are independently identified by their formulas, source
# indices and literal names.  No meaning is inferred from an old suffix 8.
T = []
safe_checks = []
safe_vectors = []
for source in range(1, 7):
    raw_i = 868 + source
    row = rows[raw_i]
    assert row['name'] == f'SAFE_{source}_C' and row['source'] == source and row['Q'] == 'C'
    sv = [frac_share(t['a'][source - 1], sum(t['a'])) - F(t['c'], sum(t['a'][:source - 1]) + 7 - source)
          for t in atoms] + [F(0)]
    check_vector(sv, dense(row['a'], 513), f'actual SAFE C {source}')
    safe_vectors.append(sv)
for j, t in enumerate(atoms):
    val = t['c'] * (sum((F(1, sum(t['a'][:i]) + 6 - i) for i in range(6)), F(0)) - 1)
    assert val >= 0
    T.append(val)
T.append(F(0))
for j in range(513):
    left = W[j] - K[j]
    right = sum((sv[j] for sv in safe_vectors), F(0)) + T[j] + EC[j]
    assert left == right
    safe_checks.append({'column': j, 'W_minus_K': left, 'sum_six_SAFE_C': sum((sv[j] for sv in safe_vectors), F(0)),
                        'T_C': T[j], 'E_C': EC[j], 'identity_difference': left - right})
write('all513_actual_SAFE_C_identity.json', safe_checks)

# Structural Delta identities, with the independent K coordinate retained.
Mout = [F(t['c'] * (1 - t['o'])) for t in atoms] + [F(0)]
M10 = [F(t['a'][0] * t['c'] * (1 - t['o'])) for t in atoms] + [F(0)]
M1 = [F(t['a'][0] * t['o'] * (1 - t['c'])) for t in atoms] + [F(0)]
M0 = [F((1 - t['a'][0]) * t['o'] * (1 - t['c'])) for t in atoms] + [F(0)]
delta = [F(t['o'], 6 * (t['a'][0] + 3 * t['c'] + 2)) - F(t['o'], 6 * (t['a'][0] + 2 * t['c'] + 3))
         for t in atoms] + [F(0)]
delta_checks = []
for j in range(513):
    D0 = M0[j] / 72
    rhs72 = D0 + (O[j] - K[j] + Mout[j] - EC[j]) / 72
    rhs36 = (O[j] - K[j] + Mout[j] - EC[j]) / 36 - M1[j] / 72
    assert delta[j] == rhs72 == rhs36
    if j < 512:
        t = atoms[j]
        assert delta[j] == F(t['o'] * (1 - t['c']), 6 * (t['a'][0] + 2) * (t['a'][0] + 3))
    delta_checks.append({'column': j, 'N5_minus_N4': delta[j], 'form72': rhs72,
                         'form36': rhs36, 'difference72': delta[j] - rhs72,
                         'difference36': delta[j] - rhs36})
write('all513_delta_identities.json', delta_checks)

lambda0, lambdar = y[2606], y[868]
debit = lambda0 * epsilon / 72
free_ec = eta_c - lambda0 * S0
strong_root = [root_global[j] - root_eta * Mout[j] for j in range(513)]
new_delta = all_cut_vectors[0]
assert all(new_delta[j] == F(rows[2606]['a'].get(str(j), '0')) + S0 * EC[j]
           - epsilon * delta[j] + M10[j] / 180 for j in range(513))


def certificate(denominator):
    gamma = lambda0 * epsilon / denominator
    new_alpha = (alpha + gamma) / (1 + gamma)
    assert new_alpha > alpha
    new_y = y.copy()
    for i in range(869, 875):
        new_y[i] += gamma
    res = []
    details = []
    checks = []
    for j in range(513):
        delta_adjustment = debit * M0[j] if denominator == 72 else -debit * M1[j]
        outside_credit = (lambdar * root_eta + gamma) * Mout[j]
        loss_payment = -lambda0 * M10[j] / 180
        tc_payment = gamma * T[j]
        r = old_residual[j] + delta_adjustment + outside_credit + loss_payment + tc_payment
        res.append(r)
        details.append({'column': j, 'old_residual': old_residual[j],
                         'Delta_adjustment': delta_adjustment, 'C_outside_credit': outside_credit,
                         'conditional_loss_debit': loss_payment, 'T_C_credit': tc_payment,
                         'final_residual': r})
        left = (1 + gamma) * W[j] - (alpha + gamma) * O[j]
        # Every original raw row is retained; rhs_i O is present even though
        # all thirty nonzero rhs rows happen to have zero weight here.
        right = r + free_ec * EC[j]
        for i, weight in enumerate(new_y):
            if not weight:
                continue
            av = (strong_root[j] if i == 868 else new_delta[j] if i == 2606
                  else F(rows[i]['a'].get(str(j), '0')))
            right += weight * (av - rhs[i] * O[j])
        assert left == right, (denominator, j, left, right)
        checks.append({'column': j, 'left': left, 'right': right,
                       'identity_difference': left - right, 'nonnegative_residual': r})
    negatives = [x for x in details if x['final_residual'] < 0]
    assert not negatives, negatives
    assert min(new_y) >= 0
    override = {
        '868': {'name': 'ROOT270_MINUS_ETA_C_OUTSIDE_O', 'coefficients': sparse(strong_root), 'rhs': F(0)},
        '2606': {'name': 'C_DELTA_EPS_S0', 'coefficients': sparse(new_delta), 'rhs': F(0)},
    }
    obj = {
        'schema': 'independent_delta_uniform_certificate_v1',
        'status': 'PASS_FULL_3056_RETAINED_513_HOMOGENEOUS_IDENTITY',
        'audit_id': AUDIT_ID, 'agent_id': AGENT, 'RUN': RUN, 'optimizer_calls': 0,
        'base_input_path': 'visible_maximum_joint_v5/exact_input.json',
        'base_input_sha256': PINS['visible_maximum_joint_v5/exact_input.json'],
        'base_certificate_sha256': PINS['visible_maximum_joint_v5_solve/exact_certificate.json'],
        'all_original_raw_rows_retained': 3056, 'all_columns_retained': 513,
        'homogeneous_row_convention': 'R_i^h = A_i dot z - rhs_i * |O|',
        'all30_rhs_minus_one_rows_retained': [x['raw_index'] for x in affine_records],
        'row_coefficient_overrides': override,
        'epsilon': epsilon, 'lambda0': lambda0, 'lambdar': lambdar, 'root_eta': root_eta,
        'boost_denominator': denominator, 'gamma': gamma,
        'alpha_old': alpha, 'alpha_new': new_alpha, 'alpha_new_decimal': decimal(new_alpha),
        'strict_improvement': new_alpha - alpha,
        'strict_improvement_decimal': decimal(new_alpha - alpha),
        'normalization_divisor': 1 + gamma,
        'all3056_payments_before_normalization': new_y,
        'all3056_payments_normalized': [yy / (1 + gamma) for yy in new_y],
        'positive_raw_indices': [i for i, yy in enumerate(new_y) if yy],
        'free_EC_weight_before_normalization': free_ec,
        'free_EC_weight_normalized': free_ec / (1 + gamma),
        'free_EC_has_no_sign_restriction': True,
        'all513_residuals_before_normalization': res,
        'all513_residuals_normalized': [rr / (1 + gamma) for rr in res],
        'negative_columns': negatives,
        'zero_residual_columns': [j for j, rr in enumerate(res) if not rr],
        'C_outside_credit_before_M10_debit': lambdar * root_eta + gamma,
        'C_outside_credit_after_M10_debit': lambdar * root_eta + gamma - lambda0 / 180,
        'arbitrary_six_legal_query_union': True,
        'scope': 'Original complete ordered-history common-catalog six-player pure SPE; all weak ties retained. No exact worst-case or half claim.',
    }
    write(f'certificate_gamma{denominator}.json', obj)
    write(f'all513_identity_gamma{denominator}.json', checks)
    write(f'all513_residual_decomposition_gamma{denominator}.json', details)
    return obj, checks, res


cert72, checks72, res72 = certificate(72)
assert F(main['boost']) == cert72['gamma']
assert F(main['alpha_new']) == cert72['alpha_new']
assert F(main['free_C_equality_weight_before_normalization']) == free_ec
check_vector(res72, list(map(F, main['nonnegative_column_residual_before_normalization'])), 'Main final residual')
for j, check in enumerate(checks72):
    assert F(main_columns[j]['left']) == check['left']
    assert F(main_columns[j]['right']) == check['right']
    assert F(main_columns[j]['residual']) == res72[j]
assert {str(i): yy for i, yy in enumerate(cert72['all3056_payments_before_normalization']) if yy} == {
    i: F(v) for i, v in main['new_positive_raw_weights_before_normalization'].items()}
cert36, checks36, res36 = certificate(36)
assert cert36['alpha_new'] > cert72['alpha_new'] > alpha
debit_ids = [j for j, mass in enumerate(M1) if mass]
assert len(debit_ids) == 64
minimum_debit_old = min(old_residual[j] for j in debit_ids)
minimum_debit_new = min(old_residual[j] - debit for j in debit_ids)
assert minimum_debit_new > 0
debit_checks = [{'column': j, 'bits': f'{j:09b}', 'old_residual': old_residual[j],
                 'extra_debit': debit, 'remaining_residual': old_residual[j] - debit,
                 'all_other_adjustments_zero': res36[j] == old_residual[j] - debit}
                for j in debit_ids]
write('all64_p1_Oonly_debits.json', debit_checks)

# Re-read every pinned byte after all calculations, including Main's complete
# freeze.  No producer, Main program, optimizer, Git or registry was invoked.
assert all(digest(WS / rel) == h for rel, h in PINS.items())
write('source_pins_and_immutability.json', {
    'status': 'PASS_ALL_PINNED_BYTES_UNCHANGED', 'source_pins': PINS,
    'Main_frozen_artifacts_all_match_manifest': True,
    'producer_python_imports': 0, 'optimizer_calls': 0,
    'writes_outside_authorized_audit_scope': 0,
})
summary = {
    'status': 'PASS_MAIN72_AND_STRICTER_GAMMA36_UNIVERSAL_CERTIFICATE',
    'audit_id': AUDIT_ID, 'agent_id': AGENT, 'RUN': RUN,
    'optimizer_calls': 0, 'producer_imports': 0,
    'Main_claim_independently_reconstructed': True,
    'true_delta_states': 256, 'true_delta_menu_states': menu_count,
    'true_delta_full_column_identities': 1026,
    'root_C30_hidden_states': len(c30_states), 'root_columns': 131,
    'original_raw_rows': 3056, 'affine_rhs_minus_one_rows': 30,
    'final_columns_per_certificate': 513,
    'alpha_old': alpha, 'alpha_main72': cert72['alpha_new'],
    'alpha_independent36': cert36['alpha_new'],
    'alpha_independent36_decimal': cert36['alpha_new_decimal'],
    'improvement_over_old': cert36['alpha_new'] - alpha,
    'improvement_over_Main72': cert36['alpha_new'] - cert72['alpha_new'],
    'gamma36': cert36['gamma'], 'free_EC_weight_before_normalization': free_ec,
    'p1_Oonly_columns': len(debit_ids),
    'minimum_old_p1_Oonly_residual': minimum_debit_old,
    'minimum_p1_Oonly_residual_after_debit': minimum_debit_new,
    'minimum_debit_columns': [j for j in debit_ids if old_residual[j] == minimum_debit_old],
    'zero_final_residual_columns_gamma36': cert36['zero_residual_columns'],
    'negative_final_residual_columns_gamma36': [],
    'half_status': 'OPEN',
}
write('audit_result.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2, default=enc))
