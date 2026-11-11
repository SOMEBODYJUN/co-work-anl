#!/usr/bin/env python3
"""Independent ROOT30 sign audit; no imported builder/Main/old-audit program.

Reconstruct the nine source3 costs from literal shares, recompute both all128
moment envelopes, then verify only the explicitly authorized fixed-dual ROOT30
identity. This does not optimize a cone or bind the source2 layer to a point.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
MAIN = WS / 'main_thirty_index_strengthening'
OLD = WS / 'maximal_root_tail_wallet_v2'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(bit, prefix, followers=0):
    return F(1, prefix + 1 + followers) if bit else F(0)


def payoff(bits, i):
    return share(bits[i], sum(bits[:i]), sum(bits[i+1:]))


def cost_two(t, s, prefix):
    return share(t, prefix, s) + share(s, prefix)


def wallet(sequence):
    prefix = sum(sequence[:4]); y, z = sequence[4:]
    return (payoff(sequence, 4) + payoff(sequence, 5)
            + share(y, prefix) - share(y, prefix, 1))


# Explicitly averaged query costs at the weak one-covered-index endpoint.
MENU_PAIR = {}
for D in range(1, 6):
    for o in (0, 1):
        menu = (o, 0, 0, 0, 0, 0)
        for distinct in (False, True):
            pairs = [(i, j) for i in range(6) for j in range(6)
                     if not distinct or i != j]
            MENU_PAIR[D, o, distinct] = sum(
                (cost_two(menu[i], menu[j], D-1) for i, j in pairs), F(0)) / len(pairs)


def source3_cost(bits, state, distinct):
    old, o = bits[:6], bits[6]
    q, r4, r5, r6 = state
    new = old[:2] + (q, r4, r5, r6)
    result = 126000 * payoff(new, 2)
    for tail, weight in zip((r4, r5, r6), (43, 31218, 34458)):
        result += weight * share(tail, sum(old[:3]), 2)
    for tail in (r4, r5, r6):
        result += 1654 * share(tail, sum(old[:5]))
    result += 5400 * (share(o, sum(new[:5])) / 6 - payoff(new, 5))
    result += 7740 * (MENU_PAIR[1+sum(new[:4]), o, distinct] - wallet(new))
    return result


def root_positive_row(name, bits, m, distinct):
    sequence, o = bits[:6], bits[6]
    if name == 'ROOT_IC': return -payoff(sequence, 0)
    if name.startswith('CAP_B'): return -F(sequence[int(name[-1])-1])
    if name.startswith('SAFE_j'):
        j = int(name.split('|')[0][-1])
        return payoff(sequence, j-1) - share(o, sum(sequence[:j-1]), 6-j)/6
    if name == 'PAIR|Omean|Omean':
        return wallet(sequence) - MENU_PAIR[1+sum(sequence[:4]), o, distinct]
    if name == 'OPT_SOURCE3_REQUERY_CUT':
        return 126000*payoff(sequence, 2) + 65719*payoff(sequence, 3) + 4962*payoff(sequence, 5) - m
    raise AssertionError(name)


def main():
    old_cert_path = OLD / 'exact_certificate.json'
    assert digest(old_cert_path) == '8b38a322e3b6ddffefee25d3db157e3fbbddb284a4b636143360bd00d4db5b46'
    old = json.loads(old_cert_path.read_text())
    current = json.loads((MAIN / 'exact_certificate.json').read_text())
    declared_env = json.loads((MAIN / 'requery30_envelopes.json').read_text())
    declared_states = json.loads((MAIN / 'requery30_states.json').read_text())
    states_by_key = {(r['h'], tuple(r['state'])): r for r in declared_states}
    assert len(declared_env) == 128 and len(states_by_key) == 2048
    bits_all = list(product((0, 1), repeat=7))
    m30, m36 = [], []
    costs = {}
    positive = zeros = 0
    deltas = []
    for h, bits in enumerate(bits_all):
        new_min, old_min = [], []
        for q in (0, 1):
            vals30, vals36 = [], []
            for tails in product((0, 1), repeat=3):
                state = (q,) + tails
                phi30 = source3_cost(bits, state, True)
                phi36 = source3_cost(bits, state, False)
                D = 1 + sum(bits[:2]) + q + tails[0]
                assert phi30 - phi36 == F(215*bits[6], D*(D+1))
                stored = states_by_key[h, state]
                assert F(stored['cost']) == phi30 and F(stored['old36_cost']) == phi36
                costs[h, state] = phi30
                vals30.append(phi30); vals36.append(phi36)
            new_min.append(min(vals30)); old_min.append(min(vals36))
        a0, a1 = new_min; b0, b1 = old_min; o = bits[6]
        new_m = a0 if not o else min((5*a0+a1)/6, a1)
        old_m = b0 if not o else min((5*b0+b1)/6, b1)
        delta = max(a1-a0, F(0)); gamma = max(a0-a1, F(0))
        assert new_m == a0 + delta*o/6 - gamma*o
        assert new_m-old_m >= F(43*o, 6)
        declaration = declared_env[h]
        assert declaration['h'] == h and tuple(declaration['bits']) == bits
        for key, value in [('a0', a0), ('a1', a1), ('delta', delta), ('gamma', gamma),
                           ('m30', new_m), ('m36', old_m), ('improvement', new_m-old_m)]:
            assert F(declaration[key]) == value, (h, key)
        for state in product((0, 1), repeat=4):
            residual = costs[h, state] + (gamma-delta)*state[0] - a0
            assert residual >= 0 and residual == F(states_by_key[h, state]['residual'])
            positive += residual > 0; zeros += residual == 0
        m30.append(new_m); m36.append(old_m); deltas.append(delta)

    lam = {name: F(value) for name, value in old['dual']['original_unscaled_row_weights'].items()}
    assert len(lam) == 10 and all(value > 0 for value in lam.values())
    assert {k: F(v) for k, v in current['root_fixed_weights'].items()} == lam
    pi_K = F(old['dual']['equality_C_size'])
    pi_O = F(old['dual']['equality_OPT_union'])
    a = F(old['universal_root_line']['a'])
    b = F(old['universal_root_line']['b'])
    assert a == F(current['root_old_a']) and b == F(current['root_old_b'])
    old_res = old['dual']['column_residuals']
    available, new_budget_coeffs = [], []
    for h, bits in enumerate(bits_all):
        old_coefficient = sum((weight*root_positive_row(name, bits, m36[h], False)
                               for name, weight in lam.items()), F(0))
        rho = -old_coefficient-pi_K*bits[0]-pi_O*bits[6]
        assert rho >= 0 and rho == F(old_res[str(h)])
        new_coefficient = sum((weight*root_positive_row(name, bits, m30[h], True)
                               for name, weight in lam.items()), F(0))
        D = 1+sum(bits[:4]); o = bits[6]
        extra = lam['PAIR|Omean|Omean']*F(o, 36*D*(D+1))
        extra += lam['OPT_SOURCE3_REQUERY_CUT']*(m30[h]-m36[h])
        assert old_coefficient-new_coefficient == extra
        available.append(rho+extra); new_budget_coeffs.append(new_coefficient)
    eta = min(available[h] for h, bits in enumerate(bits_all) if bits[6])
    assert eta == F('10132956584/286481466938835') == F(current['root_eta'])
    attain = [h for h, bits in enumerate(bits_all) if bits[6] and available[h] == eta]
    assert attain == current['root_eta_attaining_types']
    new_pi_O = pi_O+eta
    new_b = b+eta
    assert new_b == new_pi_O == F(current['root_new_b'])
    assert F(current['root_equality_multipliers']['K']) == pi_K
    assert F(current['root_equality_multipliers']['O']) == new_pi_O
    residuals = []
    for h, bits in enumerate(bits_all):
        rho = available[h]-eta*bits[6]
        assert rho >= 0 and rho == F(current['root_all129_residuals'][str(h)])
        assert new_budget_coeffs[h]+pi_K*bits[0]+new_pi_O*bits[6]+rho == 0
        residuals.append(rho)
    # The u coefficient is independent of all128 customer atoms.
    assert lam['ROOT_IC'] == 1 and F(current['root_all129_residuals']['128']) == 0
    # Keep K,O independent; these are the final two homogeneous columns.
    cap_weight = sum((weight for name, weight in lam.items() if name.startswith('CAP_B')), F(0))
    assert cap_weight-pi_K == -a
    assert -new_pi_O == -new_b
    integer_line = {key: int(value) for key, value in current['root_primitive_integer_line'].items()}
    assert integer_line == {'u': 1145925867755340, 'K': 117315110077815, 'O': 22894569998026}
    assert F(integer_line['K'], integer_line['u']) == a
    assert F(integer_line['O'], integer_line['u']) == new_b

    # The exported actual-type row is only a substitution of actual root u1.
    exported = json.loads((MAIN / 'ROOT_REQUERY_30_FIXED_DUAL.json').read_text())
    for h, bits in enumerate(product((0, 1), repeat=8)):
        expect = payoff(bits[:6], 0)-new_b*bits[7]
        assert F(exported['a'].get(str(h), '0')) == expect
    assert F(exported['a']['256']) == -a and F(exported['rhs']) == 0
    files = [old_cert_path, MAIN/'proof.md', MAIN/'exact_certificate.json',
             MAIN/'requery30_envelopes.json', MAIN/'requery30_states.json',
             MAIN/'ROOT_REQUERY_30_FIXED_DUAL.json']
    result = {
        'status': 'PASS_INDEPENDENT_ROOT30_PAYMENT_DIRECTION_AND_131_COLUMNS',
        'source3_literal_states': 2048, 'source3_old_types': 128,
        'source3_new_residuals_positive': positive, 'source3_new_residuals_zero': zeros,
        'minimum_lower_moment_weight': str(min(deltas)),
        'root_positive_budget_weights_unchanged': 10,
        'root_homogeneous_identity_columns': 131,
        'root_atom_residuals_positive': sum(r > 0 for r in residuals),
        'root_atom_residuals_zero': sum(r == 0 for r in residuals),
        'root_u_residual': '0', 'root_eta': str(eta), 'root_eta_attaining_types': attain,
        'old_slope': str(a), 'old_intercept': str(b), 'new_intercept': str(new_b),
        'equality_K': str(pi_K), 'equality_O': str(new_pi_O),
        'integer_line': integer_line, 'exported_actual_row_columns': 257,
        'scope': 'Actual root payoff, true maximum naked label size K, and union O of any six legal labels; union-cap and root-floor weights stay zero.',
        'source_sha256': {str(p.relative_to(REPO)): digest(p) for p in files},
        'optimizer_calls': 0, 'builder_or_Main_code_imported_or_executed': False,
        'old_point_recomputed': False,
        'not_claimed': ['new root-cone optimum', 'matching new primal',
                        'new global LP result', 'best-known welfare bound'],
        'outstanding_errors': [],
    }
    (HERE/'root30_context_result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'source3_literal_states',
                       'root_homogeneous_identity_columns', 'root_eta',
                       'integer_line', 'outstanding_errors')}, indent=2))


if __name__ == '__main__':
    main()
