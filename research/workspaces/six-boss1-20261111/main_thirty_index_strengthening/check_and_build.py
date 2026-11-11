"""Main exact 30-index strengthening, root fixed-dual payment, and four rows.

No optimizer. All old files are read-only; every output stays in this directory.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from math import lcm, gcd
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent


def load(path, expected=None):
    p = WS / path
    if expected is not None:
        assert sha256(p.read_bytes()).hexdigest() == expected, path
    return json.loads(p.read_text())


def save(name, data):
    p = HERE / name
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return sha256(p.read_bytes()).hexdigest()


def dot(a, b):
    return sum((F(v) * F(b.get(str(k), 0)) for k, v in a.items()), F(0))


def coeff(row, j):
    return F(row['a'].get(str(j), 0))


def contribution(n, d):
    return F(n, d) if d else F(0)


def main():
    g = load('universal_union_wallet_v3/exact_input.json',
             'd5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55')
    old_cut = load('main_opt_requery_cut_check.json')
    root = load('maximal_root_tail_wallet_v2/exact_input.json',
                '86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d')
    rc = load('maximal_root_tail_wallet_v2/exact_certificate.json',
              '8b38a322e3b6ddffefee25d3db157e3fbbddb284a4b636143360bd00d4db5b46')
    strict = load('v3_optimum_joint_face/strict_dual_certificate.json',
                  '5a327d8c549897f465537ea3bac8f3e6cab8ae4c7ce947f7411ad3ce94a55224')
    source2 = load('v3_optimum_joint_face/source2_max_size_cut.json',
                   '6bdda3643213a9712c74d3a1f2f87be1f559aec40e2879966c6fda7e564a9c53')

    # Literal 30 ordered distinct-index average, not a disjointness hypothesis.
    pair_checks = []
    for menu in product((0, 1), repeat=6):
        d, o = sum(menu), int(any(menu))
        for D in range(1, 6):
            literal = sum((F(menu[i]+menu[j], D)-F(menu[i]*menu[j], D*(D+1))
                           for i in range(6) for j in range(6) if i != j), F(0))/30
            formula = F(d, 3*D)-F(d*(d-1), 30*D*(D+1))
            full36 = F(d, 3*D)-F(d*d, 36*D*(D+1))
            assert literal == formula >= F(o, 3*D)
            assert formula-full36 == F(d*(6-d), 180*D*(D+1)) >= 0
            pair_checks.append({'menu': list(menu), 'D': D, 'cost30': str(formula),
                                'union_residual': str(formula-F(o, 3*D))})

    envelopes, costs_out, m30, m36, c30 = [], [], {}, {}, {}
    pos = zero = 0
    for h, bits in enumerate(product((0, 1), repeat=7)):
        p, y2, y3, y4, y5, z, o = bits
        b, load_old = p+y2, sum(bits[:6])
        costs, oldcosts = {}, {}
        for q, r, y, t in product((0, 1), repeat=4):
            D = 1+b+q+r
            val = F(126000*q, b+1+r+y+t)
            val += F(43*r+31218*y+34458*t, b+y3+3)
            val += F(1654*(r+y+t), b+y3+y4+y5+1)
            val += 5400*F(F(o, 6)-t, D+y)
            val += 7740*(F(o, 3*D)-F(y, D+t)-F(t, D+y)-F(y, D*(D+1)))
            state = (q, r, y, t)
            costs[state] = val
            oldcosts[state] = val-F(215*o, D*(D+1))
        aq = [min(v for state, v in costs.items() if state[0] == q) for q in (0, 1)]
        oldaq = [min(v for state, v in oldcosts.items() if state[0] == q) for q in (0, 1)]
        delta, gamma = max(aq[1]-aq[0], F(0)), max(aq[0]-aq[1], F(0))
        mm = aq[0] if not o else min((5*aq[0]+aq[1])/6, aq[1])
        oldmm = oldaq[0] if not o else min((5*oldaq[0]+oldaq[1])/6, oldaq[1])
        assert mm == aq[0]+F(o, 6)*delta-o*gamma
        assert oldmm == F(old_cut['local_envelopes'][h]['m'])
        assert mm-oldmm >= F(43*o, 6)
        wallet = contribution(126000*y3+65719*y4+4962*z, load_old)
        assert wallet-oldmm == F(old_cut['cut_all128'][str(h)])
        m30[h], m36[h], c30[h] = mm, oldmm, wallet-mm
        for state, val in costs.items():
            residue = val+(gamma-delta)*state[0]-aq[0]
            assert residue >= 0
            pos += residue > 0
            zero += residue == 0
            costs_out.append({'h': h, 'state': list(state), 'cost': str(val),
                              'old36_cost': str(oldcosts[state]), 'residual': str(residue)})
        envelopes.append({'h': h, 'bits': list(bits), 'a0': str(aq[0]), 'a1': str(aq[1]),
                          'delta': str(delta), 'gamma': str(gamma), 'm30': str(mm),
                          'm36': str(oldmm), 'improvement': str(mm-oldmm), 'cut': str(wallet-mm)})

    # Independent original root72 primal and 131-column homogeneous identity.
    lam = {k: F(v) for k, v in rc['dual']['original_unscaled_row_weights'].items()}
    assert all(v >= 0 for v in lam.values())
    rows = {r['name']: r for r in root['raw_rows']}
    primal = {str(i): F(rc['primal'].get(str(i), 0)) for i in range(129)}
    assert all(v >= 0 for v in primal.values())
    K, O = F(root['fixed_K']), F(root['fixed_O'])
    for row in root['raw_rows']:
        slack = dot(row['a'], primal)-F(row['bK'])*K-F(row['bO'])*O
        assert slack == F(rc['raw_unscaled_row_slacks'][row['name']]) >= 0
        assert lam.get(row['name'], 0)*slack == 0
    for eq in root['equalities']:
        assert dot(eq['a'], primal) == F(eq['rhs'])
    pip, pio = F(rc['dual']['equality_C_size']), F(rc['dual']['equality_OPT_union'])
    a = pip+sum((v*F(rows[name]['bK']) for name, v in lam.items()), F(0))
    oldb = pio+sum((v*F(rows[name]['bO']) for name, v in lam.items()), F(0))
    assert a == F(rc['universal_root_line']['a']) and oldb == F(rc['universal_root_line']['b'])
    assert primal['128'] == F(rc['objective']) == a*K+oldb*O
    oldres = {}
    for j in range(129):
        residue = F(j == 128)-sum((v*coeff(rows[name], j) for name, v in lam.items()), F(0))
        residue -= pip*F(root['equalities'][0]['a'].get(str(j), 0))
        residue -= pio*F(root['equalities'][1]['a'].get(str(j), 0))
        assert residue == F(rc['dual']['column_residuals'][str(j)]) >= 0
        assert residue*primal[str(j)] == 0
        oldres[j] = residue

    # Replace the two positively paid rows and retain all original weights.
    shifted = {}
    newrows = {name: dict(row, a=dict(row['a'])) for name, row in rows.items()}
    for h, bits in enumerate(product((0, 1), repeat=7)):
        p, y2, y3, y4, y5, z, o = bits
        D = 1+p+y2+y3+y4
        dp = F(o, 36*D*(D+1))
        dm = m30[h]-m36[h]
        assert coeff(rows['OPT_SOURCE3_REQUERY_CUT'], h) == F(old_cut['cut_all128'][str(h)])
        newrows['PAIR|Omean|Omean']['a'][str(h)] = str(coeff(rows['PAIR|Omean|Omean'], h)-dp)
        newrows['OPT_SOURCE3_REQUERY_CUT']['a'][str(h)] = str(c30[h])
        shifted[h] = oldres[h]+lam['PAIR|Omean|Omean']*dp+lam['OPT_SOURCE3_REQUERY_CUT']*dm
    eta = min(shifted[h] for h in range(128) if h % 2)
    assert eta > 0
    newb, newpio = oldb+eta, pio+eta
    residuals = {}
    for j in range(129):
        residue = F(j == 128)-sum((v*coeff(newrows[name], j) for name, v in lam.items()), F(0))
        residue -= pip*F(root['equalities'][0]['a'].get(str(j), 0))
        residue -= newpio*F(root['equalities'][1]['a'].get(str(j), 0))
        expected = shifted[j]-eta*(j % 2) if j < 128 else oldres[j]
        assert residue == expected >= 0
        residuals[str(j)] = str(residue)
    assert a == pip+sum((v*F(newrows[name]['bK']) for name, v in lam.items()), F(0))
    assert newb == newpio+sum((v*F(newrows[name]['bO']) for name, v in lam.items()), F(0))
    scale = lcm(a.denominator, newb.denominator)
    ints = [scale, int(a*scale), int(newb*scale)]
    common = gcd(gcd(ints[0], ints[1]), ints[2])
    ints = [n//common for n in ints]

    # Replay the frozen strict global certificate over every column.
    grows = {r['name']: r for r in g['raw_rows']}
    strictw = {k: F(v) for k, v in strict['old_row_weights'].items()}
    assert all(v >= 0 for v in strictw.values())
    sweight = F(strict['ACTUAL_OPT_REQUERY_CUT_weight'])
    assert sweight > 0
    for j in range(257):
        cutj = F(old_cut['actual_all256_coefficients'].get(str(j), 0))
        assert cutj == F(strict['new_cut_all257_coefficients'].get(str(j), 0))
        residue = F(g['objective'].get(str(j), 0))-F(strict['new_bound'])*F(g['equality']['a'].get(str(j), 0))
        residue -= sum((v*coeff(grows[name], j) for name, v in strictw.items()), F(0))+sweight*cutj
        assert residue == F(strict['all257_nonnegative_column_residuals'][str(j)]) >= 0

    # Literal source2 minimum for arbitrary legal T,Q, independent of X maximality.
    source2_states = []
    for a1, t, q in product((0, 1), repeat=3):
        expected = 4*t+F(30*t, a1+5)+F(q, a1+1+4*t)
        values = []
        for r3, r4, r5, z in product((0, 1), repeat=4):
            s = r3+r4+r5
            val = contribution(31*t-z, a1+t+s+z)+s+z+F(q, a1+t+s+1)
            assert val >= expected
            values.append(val)
            source2_states.append({'bits': [a1,t,q,r3,r4,r5,z], 'cost': str(val),
                                   'residual': str(val-expected)})
        assert min(values) == expected

    actual_c, actual_rc, actual31, actual_root = {}, {}, {}, {}
    for atom in g['atom_columns']:
        j, aa, x, o = atom['index'], atom['a'], atom['x'], atom['o']
        h = 0
        for bit in aa+[o]: h = 2*h+bit
        P, total = sum(aa[:4]), sum(aa)
        actual_c[str(j)] = str(c30[h])
        actual_rc[str(j)] = str(contribution(aa[4], total)+F(x, P+1)-F(o, 3*(P+1)))
        assert F(actual_rc[str(j)]) == coeff(grows['RC_8_8'], j)-F(o, 36*(P+1)*(P+2))
        actual31[str(j)] = str(contribution(31*aa[1], total)-4*aa[5]-F(30*aa[5], aa[0]+5)-F(x, aa[0]+1+4*aa[5]))
        assert F(actual31[str(j)]) == F(source2['all257_actual_T_A6_Q_X_coefficients'][str(j)])
        actual_root[str(j)] = str(contribution(aa[0], total)-newb*o)
    actual_c['256'] = actual_rc['256'] = '0'
    actual31['256'] = '4'
    actual_root['256'] = str(-a)
    assert F(source2['all257_actual_T_A6_Q_X_coefficients']['256']) == 4
    released = [
        {'name': 'ACTUAL_OPT_REQUERY_30_CUT', 'family': 'ACTUAL_OPT_REQUERY_30', 'a': actual_c, 'rhs': '0', 'numerical_divisor': '126000'},
        {'name': 'RC_OPT_30', 'family': 'RC_30', 'a': actual_rc, 'rhs': '0', 'numerical_divisor': '1'},
        {'name': 'SOURCE2_MAXSIZE_31', 'family': 'TRUE_SOURCE2_PORTFOLIO', 'a': actual31, 'rhs': '0', 'numerical_divisor': '31'},
        {'name': 'ROOT_REQUERY_30_FIXED_DUAL', 'family': 'ROOT_REQUERY_30', 'a': actual_root, 'rhs': '0', 'numerical_divisor': '1'},
    ]
    hashes = {}
    for row in released:
        assert len(row['a']) == 257 and F(row['numerical_divisor']) > 0
        hashes[row['name']] = save(row['name']+'.json', row)
    oldpoint = load('universal_union_wallet_v3/exact_certificate.json')['primal']
    evaluations = {row['name']: str(dot(row['a'], oldpoint)) for row in released}
    outputs = {
        'status': 'PASS_MAIN_LITERAL_FULL_DOMAIN_AND_131_COLUMN_ROOT_IDENTITY',
        'optimizer_calls': 0,
        'scope': 'All finite unit clients, finite nonempty common label catalog, complete ordered-history pure SPE; repeated labels, empty labels, arbitrary weak ties retained.',
        'pair_literal_states': 320, 'requery_full_states': 2048, 'requery_old_types': 128,
        'requery_positive_residuals': pos, 'requery_zero_residuals': zero,
        'min_delta': str(min(F(e['delta']) for e in envelopes)),
        'gamma_all_zero': all(F(e['gamma']) == 0 for e in envelopes),
        'root72_original_primal_and_dual_check': 'PASS_ALL72_ROWS_2_EQUALITIES_131_HOMOGENEOUS_COLUMNS',
        'root_fixed_weights': {k: str(v) for k,v in lam.items()},
        'root_old_a': str(a), 'root_old_b': str(oldb), 'root_eta': str(eta), 'root_new_b': str(newb),
        'root_eta_decimal': float(eta), 'root_eta_attaining_types': [h for h in range(128) if h%2 and shifted[h]==eta],
        'root_primitive_integer_line': dict(zip(['u','K','O'], map(str, ints))),
        'root_equality_multipliers': {'K': str(pip), 'O': str(newpio)},
        'root_all129_residuals': residuals,
        'root_fixed_K_v3_value': str(a*K+newb*O),
        'strict_v3face_certificate_check': 'PASS_ALL257_COLUMNS',
        'strict_global_bound': strict['new_bound'],
        'source2_literal_states': 128,
        'rows': released, 'row_file_sha256': hashes, 'v3_point_evaluations': evaluations,
        'not_claimed': ['new root-cone optimum', 'four-row extended cone optimum', 'half coverage', 'SPE counterexample'],
    }
    save('pair30_literal.json', pair_checks)
    save('requery30_envelopes.json', envelopes)
    save('requery30_states.json', costs_out)
    save('source2_literal.json', source2_states)
    save('exact_certificate.json', outputs)
    print(json.dumps({k: outputs[k] for k in ['status','optimizer_calls','root_eta','root_new_b','root_primitive_integer_line','root_fixed_K_v3_value','strict_global_bound','v3_point_evaluations','row_file_sha256']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
