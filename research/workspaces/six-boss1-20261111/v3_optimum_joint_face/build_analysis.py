"""Exact linear algebra and Boolean enumeration only. No optimizer imports/calls."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
R = sp.Rational


def read(folder, name):
    return json.loads((WS / folder / name).read_text())


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def hashfile(p):
    return sha256(p.read_bytes()).hexdigest()


def vector(row):
    return sp.Matrix([R(row['a'].get(str(j), '0')) for j in range(257)])


def allstrings(v):
    return {str(j): str(q) for j, q in enumerate(v)}


def root_literal(h):
    l = tuple(int(c) for c in format(h, '07b'))
    p, y2, y3, y4, y5, z, o = l
    load = sum(l[:6])
    pay = [R(a, load) if load else R(0) for a in l[:6]]
    rows = {'ROOT_IC': -pay[0]}
    for j in range(2, 7):
        rows[f'CAP_B{j}'] = -l[j-1]
    for j in (3, 4, 6):
        rows[f'SAFE_j{j}|Omean'] = pay[j-1] - R(o, 6 * (sum(l[:j-1]) + 7-j))
    D = 1 + p + y2 + y3 + y4
    rows['PAIR|Omean|Omean'] = pay[4] + pay[5] + R(y5, D*(D+1)) - R(o, 3*D) + R(o, 36*D*(D+1))
    return l, rows


def main():
    pinned = {
        'universal_union_wallet_v3/exact_input.json': 'd5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55',
        'universal_union_wallet_v3/exact_certificate.json': '1d9a898e3ca429b6af3611f01ada831ad50cf7f0708f14d7c518478573f0a9e3',
        'maximal_root_tail_wallet/exact_input.json': '3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65',
        'maximal_root_tail_wallet/exact_certificate.json': '80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771',
        'maximal_root_opt_requery/exact_certificate.json': '209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e',
        'main_opt_requery_cut_check.json': 'e2241d3513bb4d824212d127ccdfec845e242186c23a6c935a75e2d47e2a066f',
    }
    for name, h in pinned.items():
        assert hashfile(WS / name) == h, name
    source_files = list(pinned) + [
        'maximal_root_tail_wallet/proof.md',
        'maximal_root_tail_wallet/derivation.md',
        'maximal_root_opt_requery/proof.md',
        'maximal_root_opt_requery/derivation.md',
        'universal_union_wallet_v3/proof.md',
        'universal_union_wallet_v3/manifest.json',
    ]
    sources = {str((WS / name).relative_to(REPO)): hashfile(WS / name) for name in source_files}
    for name in [
        'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
        'archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md',
    ]:
        sources[name] = hashfile(REPO / name)
    dump('source_pins.json', sources)
    old = read('universal_union_wallet_v3', 'prior_frozen_hashes.json')
    for p in (WS / 'universal_union_wallet_v3').rglob('*'):
        if p.is_file():
            old[str(p.relative_to(WS))] = hashfile(p)
    old['universal_union_wallet_v3.md'] = hashfile(WS / 'universal_union_wallet_v3.md')
    dump('prior_frozen_hashes.json', old)

    data = read('universal_union_wallet_v3', 'exact_input.json')
    cert = read('universal_union_wallet_v3', 'exact_certificate.json')
    by = {row['name']: row for row in data['raw_rows']}
    names = list(cert['dual']['row_weights'])
    assert len(names) == 10
    assert all(R(by[n]['rhs']) == 0 for n in names)
    old_h = sp.Matrix([R(cert['dual']['nonnegative_column_residual'].get(str(j), '0')) for j in range(257)])
    support = [j for j in range(257) if old_h[j] == 0]
    rows = [data['equality']] + [by[n] for n in names]
    M = sp.Matrix([[R(row['a'].get(str(j), '0')) for j in support] for row in rows])
    rhs = sp.Matrix([R(row['rhs']) for row in rows])
    sol, pars = M.gauss_jordan_solve(rhs)
    assert len(pars) == 2 and M.rank() == 11
    sigma, t = sp.symbols('sigma t')
    sol = sol.subs({pars[0]: sigma, pars[1]: t})
    point = sp.zeros(257, 1)
    for j, v in zip(support, sol):
        point[j] = v
    assert point[0] == sigma and point[11] == t
    origin = point.subs({sigma: 0, t: 0})
    dt = point.diff(t)
    ds = point.diff(sigma)
    _, pivots = M.rref()
    determinant = M[:, list(pivots)].det()
    assert determinant != 0
    fullA = sp.Matrix([[R(row['a'].get(str(j), '0')) for j in range(257)] for row in rows])

    inequalities = []
    for index, row in enumerate(data['raw_rows']):
        v = vector(row)
        a = (v.dot(origin) - R(row['rhs']))
        b = v.dot(dt)
        d = v.dot(ds)
        assert d == 0
        inequalities.append({'index': index, 'name': row['name'], 'constant': str(a), 't': str(b), 'sigma': str(d)})
    conditions = [(r['name'], R(r['constant']), R(r['t'])) for r in inequalities]
    for j in support:
        if j != 0:
            conditions.append(('nonneg_' + str(j), origin[j], dt[j]))
    low = max(-a/b for _, a, b in conditions if b > 0)
    high = min(-a/b for _, a, b in conditions if b < 0)
    assert low < high
    assert all(a >= 0 for _, a, b in conditions if b == 0)
    assert all(a+b*low >= 0 and a+b*high >= 0 for _, a, b in conditions)
    alpha = R(cert['objective'])
    objective = sp.Matrix([R(data['objective'].get(str(j), '0')) for j in range(257)])
    assert objective.dot(origin) == alpha and objective.dot(dt) == objective.dot(ds) == 0
    face = {
        'scope': 'Exact entire normalized optimum face of the frozen221 necessary rows; no SPE realization claim.',
        'optimizer_calls': 0, 'zero_residual_columns': support,
        'positive_rows': names, 'equality_order': ['OPT_union_normalization'] + names,
        'rank': 11, 'columns_after_complementarity': 13, 'affine_dimension': 2,
        'minor_column_positions': list(pivots), 'minor_determinant': str(determinant),
        'parameters': {'sigma': 'z_0, arbitrary nonnegative invisible mass', 't': 'z_11'},
        'constant': allstrings(origin), 't_direction': allstrings(dt), 'sigma_direction': allstrings(ds),
        't_lower': str(low), 't_upper': str(high),
        't_lower_decimal': float(low), 't_upper_decimal': float(high),
        'lower_bound_sources': [n for n, a, b in conditions if b > 0 and -a/b == low],
        'upper_bound_sources': [n for n, a, b in conditions if b < 0 and -a/b == high],
        'all221_row_affine_slacks': inequalities,
        'always_tight_rows': [r['name'] for r in inequalities if R(r['constant']) == R(r['t']) == 0],
        'objective': str(alpha), 'all_rows_checked_at_both_endpoints': 221,
        'K': str(origin[256]),
    }
    dump('face_certificate.json', face)
    dump('face_endpoints.json', {'lower': allstrings(origin + low*dt), 'upper': allstrings(origin + high*dt)})

    def signed_identity(target):
        b = target.dot(dt)
        d = target.dot(ds)
        shifted = target.copy()
        shifted[11] -= b
        shifted[0] -= d
        mult, free = M.T.gauss_jordan_solve(shifted[support, 0])
        assert not free
        rem = shifted - fullA.T * mult
        assert all(rem[j] == 0 for j in support)
        return {'target': allstrings(target), 'normalization': str(mult[0]),
                't_coefficient': str(b), 'sigma_coefficient': str(d),
                'signed_row_weights': {n: str(q) for n, q in zip(names, mult[1:])},
                'signed_column_coefficients': allstrings(rem)}

    u1 = sp.zeros(257, 1)
    forced_C_gap = sp.zeros(257, 1)
    for j in range(256):
        bits = tuple(map(int, format(j, '08b')))
        if bits[0]:
            u1[j] = R(1, sum(bits[:6]))
        actual_u2 = R(bits[1], sum(bits[:6])) if sum(bits[:6]) else R(0)
        forced_C_gap[j] = R(bits[6], bits[0]+4*bits[5]+1)-actual_u2
    Kvec = sp.zeros(257, 1)
    Kvec[256] = 1
    main_cut = json.loads((WS / 'main_opt_requery_cut_check.json').read_text())
    g = sp.Matrix([R(main_cut['actual_all256_coefficients'].get(str(j), '0')) for j in range(257)])
    assert main_cut['actual_K_coefficient'] == '0'
    identities = {n: signed_identity(v) for n, v in {
        'K': Kvec, 'u1': u1, 'SAFE6_X': vector(by['SAFE_6_7']),
        'RC_X_Omean': vector(by['RC_7_8']), 'ACTUAL_OPT_REQUERY_CUT': g,
        'FORCED_MAX_C_TAIL_X_GAP': forced_C_gap,
    }.items()}
    assert identities['RC_X_Omean']['normalization'] == '0'
    assert identities['SAFE6_X']['t_coefficient'] == '1/2'
    assert R(identities['SAFE6_X']['normalization']) == -low/2
    assert identities['ACTUAL_OPT_REQUERY_CUT']['t_coefficient'] == '0'
    dump('signed_identities.json', {'convention': 'target = kappa*O + t_coefficient*z11 + sigma_coefficient*z0 + sum beta_r*row_r + sum gamma_j*z_j. beta and gamma may have either sign; each equality checked on all257 columns.', 'identities': identities})
    forced_gap_value = R(identities['FORCED_MAX_C_TAIL_X_GAP']['normalization'])
    assert forced_gap_value > 0
    assert identities['FORCED_MAX_C_TAIL_X_GAP']['t_coefficient'] == '0'
    dump('conditional_identity_obstruction.json', {
        'scope': 'Conditional exact obstruction on the old v3 optimum face; the gap is NOT asserted to be an unconditional valid inequality and is NOT used in the strict universal dual.',
        'conditions': ['SAFE_2_6=0', 'K=|A6|', 'C=A6 is a real legal maximum-size label'],
        'genuine_branch': '(A1,C,D3,D4,D5,D6) after actual source2 forces C',
        'forced_coverage_equalities': 'cov(D3)=cov(D4)=cov(D5)=cov(D6)=cov(C); labels may differ',
        'terminal_current_payoff': 'sum a6/(a1+5)=actual u2',
        'terminal_X_query_payoff': 'sum x/(a1+4*a6+1)',
        'whole_face_strict_gain': str(forced_gap_value),
        'whole_face_strict_gain_decimal': float(forced_gap_value),
        'conclusion': 'No complete pure SPE can realize any old v3 optimum-face point.',
        'optimizer_calls': 0,
    })

    cutid = identities['ACTUAL_OPT_REQUERY_CUT']
    kappa = R(cutid['normalization'])
    assert kappa < 0 and kappa == R('-1458110288660943054148007972513/1471748948895441544929768608')
    beta = {n: R(cutid['signed_row_weights'][n]) for n in names}
    gamma = sp.Matrix([R(cutid['signed_column_coefficients'][str(j)]) for j in range(257)])
    caps = []
    for n in names:
        if beta[n] > 0:
            caps.append((R(cert['dual']['row_weights'][n])/beta[n], 'row:' + n))
    for j in range(257):
        if gamma[j] > 0:
            caps.append((old_h[j]/gamma[j], 'column:' + str(j)))
    epsilon = min(a for a, _ in caps)
    assert epsilon > 0
    newalpha = alpha - epsilon*kappa
    newweights = {n: R(cert['dual']['row_weights'][n]) - epsilon*beta[n] for n in names}
    new_h = old_h - epsilon*gamma
    assert all(x >= 0 for x in list(newweights.values()) + list(new_h))
    for j in range(257):
        assert objective[j]-newalpha*fullA[0, j] == epsilon*g[j] + sum(newweights[n]*fullA[k+1, j] for k, n in enumerate(names)) + new_h[j]
    strict = {
        'scope': 'Constructed universal lower bound, not an optimized222-row value. Sign-preserving exact line step; zero optimizer calls.',
        'optimizer_calls': 0, 'old_bound': str(alpha), 'whole_face_cut_value': str(kappa),
        'epsilon': str(epsilon), 'epsilon_decimal': float(epsilon),
        'ratio_constraints': [{'source': n, 'upper_bound': str(v)} for v, n in caps],
        'limiting_constraints': [n for v, n in caps if v == epsilon],
        'new_bound': str(newalpha), 'new_bound_decimal': float(newalpha),
        'strict_improvement': str(newalpha-alpha),
        'normalization_multiplier': str(newalpha),
        'old_row_weights': {n: str(v) for n, v in newweights.items()},
        'ACTUAL_OPT_REQUERY_CUT_weight': str(epsilon),
        'new_cut_all257_coefficients': allstrings(g),
        'all257_nonnegative_column_residuals': allstrings(new_h),
        'positive_budget_count': sum(1 for v in newweights.values() if v > 0) + 1,
        'zero_column_residuals': [j for j in range(257) if new_h[j] == 0],
        'positive_column_residuals': [j for j in range(257) if new_h[j] > 0],
    }
    dump('strict_dual_certificate.json', strict)

    rootin = read('maximal_root_tail_wallet', 'exact_input.json')
    rootcert = read('maximal_root_tail_wallet', 'exact_certificate.json')
    L = {n: R(q) for n, q in rootcert['dual']['integer_row_weights'].items()}
    pp, po = map(R, rootcert['dual']['integer_equality_multipliers'])
    N = R(112944305160)
    root_r = {}
    rho = {}
    for h in range(128):
        bits, row = root_literal(h)
        root_r[h] = row
        rho[h] = -sum(L[n]*row[n] for n in L) - pp*bits[0] - po*bits[6]
        assert rho[h] == N*R(rootcert['dual']['column_residuals'][str(h)]) >= 0
    Z = [h for h in range(128) if rho[h] == 0]
    rootK = origin[256]
    rootu = u1.dot(origin)
    RM = sp.Matrix([[root_r[h][n] for h in Z] for n in L])
    rb = sp.Matrix([-rootu if n == 'ROOT_IC' else -rootK if n.startswith('CAP_') else 0 for n in L])
    for bit, val in [(0, rootK), (6, R(1))]:
        RM = RM.col_join(sp.Matrix([[int(format(h, '07b')[bit]) for h in Z]]))
        rb = rb.col_join(sp.Matrix([val]))
    rsol, rpars = RM.gauss_jordan_solve(rb)
    assert RM.rank() == 11 and len(rpars) == 2
    w3free = rsol[Z.index(3)]
    T6 = sp.simplify(rsol[Z.index(2)] + w3free)
    assert not T6.free_symbols
    e = sp.symbols('e')
    rootpoint = sp.zeros(128, 1)
    repl = {rpars[0]: sigma-e, rpars[1]: T6-e}
    for h, value in zip(Z, rsol):
        rootpoint[h] = sp.expand(value.subs(repl))
    assert rootpoint[0] == sigma-e and rootpoint[2] == e and rootpoint[33] == 0
    rorigin = rootpoint.subs({sigma: 0, e: 0})
    rde, rds = rootpoint.diff(e), rootpoint.diff(sigma)
    assert all(v >= 0 for v in rorigin)
    root_slacks = []
    for idx, row in enumerate(rootin['raw_rows']):
        rv = sp.Matrix([R(row['a'].get(str(h), '0')) for h in range(128)])
        a = rv.dot(rorigin) + R(row['a'].get('128', '0'))*rootu - R(row['bK'])*rootK - R(row['bO'])
        b = rv.dot(rde)
        d = rv.dot(rds)
        assert d == 0 and a >= 0
        root_slacks.append({'index': idx, 'name': row['name'], 'constant': str(a), 'e': str(b)})
    root_upper = min([T6] + [-R(r['constant'])/R(r['e']) for r in root_slacks if R(r['e']) < 0])
    assert root_upper >= 0
    root_lower = max([R(0)] + [-R(r['constant'])/R(r['e']) for r in root_slacks if R(r['e']) > 0])
    assert root_lower <= root_upper
    joint = []
    removed = []
    for j in support:
        if j == 256:
            continue
        vbits = tuple(map(int, format(j, '08b')))
        for h in Z:
            hbits = tuple(map(int, format(h, '07b')))
            if vbits[5] == hbits[0] and vbits[7] == hbits[6]:
                (removed if h == 33 else joint).append({'v': j, 'h': h})
    assert len(joint) == 57 and len(removed) == 6
    onC = [h for h in Z if int(format(h, '07b')[0])]
    visible = {
        'C_size': str(rootK),
        'u1': str(rootu),
        'C_intersection_X': str(origin[7]),
        'X_minus_C': str(origin[3] + origin[11]),
        'C_intersection_A5': '0',
        'X_clients_have_actual_P_zero': True,
        'root_B2_same_coverage_as_C_and_actual_A6': True,
        'root_B2_label_identity_not_asserted': True,
    }
    structure = {
        'scope': 'Necessary equalities of one real root-C branch, conditional on a hypothetical SPE realizing the old v3 optimal face. The new actual requery cut already excludes every such realization.',
        'integer_positive_budgets': {n: str(v) for n, v in L.items()},
        'all128_root_residuals': {str(h): str(q) for h, q in rho.items()},
        'zero_root_types': [{'h': h, 'bits': format(h, '07b')} for h in Z],
        'root_rank': 11, 'root_equality_count': 12,
        'root_constant': allstrings(rorigin), 'root_e_direction': allstrings(rde), 'root_sigma_direction': allstrings(rds),
        'e_interpretation': '|B6 outside O|, subset of the invisible actual type0',
        'e_lower_from_root71': str(root_lower), 'e_upper_from_root71': str(root_upper),
        'additional_shared_client_constraint': '0 <= e <= sigma',
        'all71_root_row_affine_slacks': root_slacks,
        'root_B6_outside_C_total': str(T6),
        'on_C_allowed_tail_patterns_B3_to_B6': [format(h, '07b')[2:6] for h in onC],
        'root_union_size': str(2*rootK + rorigin[121]),
        'visible_identities': visible,
        'compatible_joint_atom_pairs_after_forced_B2_identity': joint,
        'forced_zero_joint_pairs_with_h33': removed,
        'joint_optimizer_calls': 0,
        'not_claimed': ['joint SPE feasibility', 'independent branch continuations', 'label equality from equal coverage', 'new joint LP optimum'],
    }
    dump('root_equality_structure.json', structure)
    with (HERE / 'face_row_slacks.tsv').open('w') as f:
        f.write('index\tname\tconstant\tt_coefficient\tat_lower\tat_upper\n')
        for r in inequalities:
            a, b = R(r['constant']), R(r['t'])
            f.write(f"{r['index']}\t{r['name']}\t{a}\t{b}\t{a+b*low}\t{a+b*high}\n")
    with (HERE / 'strict_dual_columns.tsv').open('w') as f:
        f.write('column\tcut_coefficient\tcut_signed_residual\tnew_nonnegative_residual\n')
        for j in range(257):
            f.write(f'{j}\t{g[j]}\t{gamma[j]}\t{new_h[j]}\n')
    for name, h in old.items():
        assert hashfile(WS / name) == h, name
    print(json.dumps({'status': 'EXACT_ANALYSIS_BUILT', 'optimizer_calls': 0,
        'face_interval': [str(low), str(high)], 'K': str(rootK), 'u1': str(rootu),
        'whole_face_cut': str(kappa), 'strict_bound': str(newalpha), 'strict_bound_decimal': float(newalpha),
        'epsilon': str(epsilon), 'limiter': strict['limiting_constraints'],
        'root_e_bounds': [str(root_lower), str(root_upper)], 'joint_types': len(joint)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
