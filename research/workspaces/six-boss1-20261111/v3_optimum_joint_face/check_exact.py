"""Independent stdlib Fraction checker; does not import builder or an optimizer."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import product
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]


def load(p):
    return json.loads(p.read_text())


def vec(d, n=257):
    return [F(d.get(str(j), '0')) for j in range(n)]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def determinant(matrix):
    a = [list(row) for row in matrix]
    answer = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            answer = -answer
        pivot = a[j][j]
        answer *= pivot
        for i in range(j+1, len(a)):
            q = a[i][j]/pivot
            for k in range(j+1, len(a)):
                a[i][k] -= q*a[j][k]
    return answer


def literal_requery(source_cert):
    cut = []
    minima = []
    positives = zeros = 0
    minimum_delta = None
    mean_checks = 0
    for D in range(1, 6):
        for d in range(7):
            menu = [1]*d + [0]*(6-d)
            exact = sum((F(q+r, D)-F(q*r, D*(D+1)) for q in menu for r in menu), F(0))/36
            target = F(bool(d), 3*D)-F(bool(d), 36*D*(D+1))
            assert exact == F(d, 3*D)-F(d*d, 36*D*(D+1))
            assert exact >= target
            mean_checks += 1
    expected = {'SOURCE3_AVERAGE_IC': 126000, 'OLD_SAFE_j4|R4': 43,
        'OLD_SAFE_j4|R5': 31218, 'OLD_SAFE_j4|R6': 34458,
        'OLD_SAFE_j6|R4': 1654, 'OLD_SAFE_j6|R5': 1654, 'OLD_SAFE_j6|R6': 1654,
        'NEW_SAFE_j6|Omean': 5400, 'PAIR|Omean|Omean': 7740}
    assert source_cert['genuine_row_weights'] == expected
    for h, bits in enumerate(product((0, 1), repeat=7)):
        p, a2, a3, a4, a5, a6, o = bits
        b = p+a2
        states = {}
        for q, r, y, t in product((0, 1), repeat=4):
            D = 1+b+q+r
            menu = [o, 0, 0, 0, 0, 0]
            query_pair = sum((F(l+rr, D)-F(l*rr, D*(D+1)) for l in menu for rr in menu), F(0))/36
            phi = 126000*F(q, b+1+r+y+t)
            phi += F(43*r+31218*y+34458*t, b+a3+3)
            phi += F(1654*(r+y+t), b+a3+a4+a5+1)
            phi += 5400*(F(o, 6*(D+y))-F(t, D+y))
            phi += 7740*(query_pair-F(y, D+t)-F(t, D+y)-F(y, D*(D+1)))
            states[(q, r, y, t)] = phi
        low = [min(v for state, v in states.items() if state[0] == q) for q in (0, 1)]
        delta = low[1]-low[0]
        assert delta > 0
        minimum_delta = delta if minimum_delta is None else min(minimum_delta, delta)
        m = low[0] if not o else min((5*low[0]+low[1])/6, low[1])
        assert m == low[0]+F(o, 6)*delta
        for state, value in states.items():
            residual = value-low[state[0]]
            assert residual >= 0
            positives += residual > 0
            zeros += residual == 0
        c = sum(bits[:6])
        wallet = F(126000*a3+65719*a4+4962*a6, c) if c else F(0)
        value = wallet-m
        assert value == F(source_cert['universal_cut']['cut_z'][str(h)])
        cut.append(value)
        minima.append({'h': h, 'a0': str(low[0]), 'a1': str(low[1]), 'm': str(m), 'cut': str(value)})
    return cut, {'states': 2048, 'positive_residuals': positives, 'zero_residuals': zeros,
        'minimum_delta': str(minimum_delta), 'full36_mean_checks': mean_checks, 'envelopes': minima}


def root_rows(h):
    l = tuple(map(int, format(h, '07b')))
    p, b2, b3, b4, b5, b6, o = l
    c = sum(l[:6])
    pay = [F(x, c) if c else F(0) for x in l[:6]]
    r = {'ROOT_IC': -pay[0]}
    for j in range(2, 7):
        r[f'CAP_B{j}'] = -F(l[j-1])
    for j in (3, 4, 6):
        r[f'SAFE_j{j}|Omean'] = pay[j-1]-F(o, 6*(sum(l[:j-1])+7-j))
    D = 1+p+b2+b3+b4
    r['PAIR|Omean|Omean'] = pay[4]+pay[5]+F(b5, D*(D+1))-F(o, 3*D)+F(o, 36*D*(D+1))
    return l, r


def main():
    pins = load(HERE/'source_pins.json')
    for p, h in pins.items():
        assert sha256((REPO/p).read_bytes()).hexdigest() == h, p
    previous = load(HERE/'prior_frozen_hashes.json')
    for p, h in previous.items():
        assert sha256((WS/p).read_bytes()).hexdigest() == h, p
    data = load(WS/'universal_union_wallet_v3/exact_input.json')
    old = load(WS/'universal_union_wallet_v3/exact_certificate.json')
    face = load(HERE/'face_certificate.json')
    signed = load(HERE/'signed_identities.json')['identities']
    strict = load(HERE/'strict_dual_certificate.json')
    root = load(HERE/'root_equality_structure.json')
    by = {r['name']: r for r in data['raw_rows']}
    A = {n: vec(row['a']) for n, row in by.items()}
    norm = vec(data['equality']['a'])
    obj = vec(data['objective'])
    oldalpha = F(old['objective'])
    oldh = vec(old['dual']['nonnegative_column_residual'])
    weights = {n: F(v) for n, v in old['dual']['row_weights'].items()}
    assert len(weights) == 10 and all(q > 0 for q in weights.values())
    assert all(F(by[n]['rhs']) == 0 for n in weights)
    for j in range(257):
        assert obj[j]-oldalpha*norm[j] == sum(w*A[n][j] for n, w in weights.items())+oldh[j]
        assert oldh[j] >= 0
    S = [j for j in range(257) if oldh[j] == 0]
    assert S == face['zero_residual_columns']
    assert face['positive_rows'] == list(weights)
    c, d, e = (vec(face[k]) for k in ['constant', 't_direction', 'sigma_direction'])
    lo, hi = F(face['t_lower']), F(face['t_upper'])
    assert 0 < lo < hi and e[0] == 1 and sum(abs(v) for v in e) == 1
    assert d[11] == 1 and d[0] == 0 and c[11] == c[0] == 0
    for j in range(257):
        assert c[j]+lo*d[j] >= 0 and c[j]+hi*d[j] >= 0
        if oldh[j] > 0:
            assert c[j] == d[j] == e[j] == 0
    for row, rhs in [(norm, F(1))]+[(A[n], F(0)) for n in weights]:
        assert dot(row, c) == rhs and dot(row, d) == dot(row, e) == 0
    restricted = [[r[j] for j in S] for r in [norm]+[A[n] for n in weights]]
    piv = face['minor_column_positions']
    det = determinant([[r[j] for j in piv] for r in restricted])
    assert det == F(face['minor_determinant']) != 0 and len(piv) == 11
    assert dot(obj, c) == oldalpha and dot(obj, d) == dot(obj, e) == 0
    for index, (r, entry) in enumerate(zip(data['raw_rows'], face['all221_row_affine_slacks'])):
        a = dot(A[r['name']], c)-F(r['rhs'])
        b = dot(A[r['name']], d)
        assert entry['index'] == index and entry['name'] == r['name']
        assert F(entry['constant']) == a and F(entry['t']) == b
        assert dot(A[r['name']], e) == F(entry['sigma']) == 0
        assert a+b*lo >= 0 and a+b*hi >= 0
    assert dot(A['SAFE_6_7'], c) == -lo/2 and dot(A['SAFE_6_7'], d) == F(1, 2)
    assert c[3] == hi and d[3] == -1
    assert A['RC_7_8'] == A['MX_8']

    source = load(WS/'maximal_root_opt_requery/exact_certificate.json')
    cut128, literal_report = literal_requery(source)
    assert literal_report['positive_residuals'] == 1758 and literal_report['zero_residuals'] == 290
    cut = []
    u1 = []
    forced_C_gap = []
    for j in range(256):
        bits = tuple(map(int, format(j, '08b')))
        h = int(''.join(map(str, bits[:6]+(bits[7],))), 2)
        cut.append(cut128[h])
        u1.append(F(bits[0], sum(bits[:6])) if sum(bits[:6]) else F(0))
        actual_u2 = F(bits[1], sum(bits[:6])) if sum(bits[:6]) else F(0)
        forced_C_gap.append(F(bits[6], bits[0]+4*bits[5]+1)-actual_u2)
        P = sum(bits[:4]); D = P+1; a5, x, o = bits[4], bits[6], bits[7]
        actual_u5 = F(a5, sum(bits[:6])) if sum(bits[:6]) else F(0)
        rc = actual_u5+F(x, D)-F(x, D)-F(o, 6*D)+F(x*o, 6*D*(D+1))
        assert rc == actual_u5-F(o, 6*(D+x)) == A['RC_7_8'][j]
    cut.append(F(0)); u1.append(F(0)); forced_C_gap.append(F(0))
    expected_targets = {'ACTUAL_OPT_REQUERY_CUT': cut, 'u1': u1,
        'K': [F(j == 256) for j in range(257)], 'SAFE6_X': A['SAFE_6_7'], 'RC_X_Omean': A['RC_7_8'],
        'FORCED_MAX_C_TAIL_X_GAP': forced_C_gap}
    for name, ident in signed.items():
        target = vec(ident['target'])
        assert target == expected_targets[name]
        k, tcoef, scoef = map(F, [ident['normalization'], ident['t_coefficient'], ident['sigma_coefficient']])
        beta = {n: F(v) for n, v in ident['signed_row_weights'].items()}
        rem = vec(ident['signed_column_coefficients'])
        for j in range(257):
            assert target[j] == k*norm[j]+tcoef*(j == 11)+scoef*(j == 0)+sum(q*A[n][j] for n, q in beta.items())+rem[j]
        assert all(rem[j] == 0 for j in S)
    kappa = F(signed['ACTUAL_OPT_REQUERY_CUT']['normalization'])
    assert kappa < 0 and dot(cut, c) == kappa and dot(cut, d) == dot(cut, e) == 0
    assert dot(u1, d) == dot(u1, e) == 0 and d[256] == e[256] == 0
    obstruction = load(HERE/'conditional_identity_obstruction.json')
    forced_gain = F(obstruction['whole_face_strict_gain'])
    assert dot(forced_C_gap, c) == forced_gain > 0
    assert dot(forced_C_gap, d) == dot(forced_C_gap, e) == 0
    equality_load_checks = 0
    for a1 in (0, 1):
        for tails in product((0, 1), repeat=4):
            gap = F(1, a1+1+sum(tails))-F(1, a1+5)
            assert gap >= 0 and (gap == 0) == (sum(tails) == 4)
            equality_load_checks += 1
    eps = F(strict['epsilon'])
    newalpha = F(strict['new_bound'])
    assert newalpha == oldalpha-eps*kappa > oldalpha
    beta = {n: F(q) for n, q in signed['ACTUAL_OPT_REQUERY_CUT']['signed_row_weights'].items()}
    gamma = vec(signed['ACTUAL_OPT_REQUERY_CUT']['signed_column_coefficients'])
    caps = [(weights[n]/v, 'row:'+n) for n, v in beta.items() if v > 0]
    caps += [(oldh[j]/v, 'column:'+str(j)) for j, v in enumerate(gamma) if v > 0]
    assert eps == min(v for v, _ in caps) > 0
    assert strict['limiting_constraints'] == [n for v, n in caps if v == eps] == ['row:UP_3']
    newweights = {n: F(v) for n, v in strict['old_row_weights'].items()}
    newh = vec(strict['all257_nonnegative_column_residuals'])
    assert vec(strict['new_cut_all257_coefficients']) == cut
    for n in weights:
        assert newweights[n] == weights[n]-eps*beta[n] >= 0
    for j in range(257):
        assert newh[j] == oldh[j]-eps*gamma[j] >= 0
        assert obj[j]-newalpha*norm[j] == eps*cut[j]+sum(v*A[n][j] for n, v in newweights.items())+newh[j]
    integer_path = HERE/'strict_integer_identity.json'
    if integer_path.exists():
        ii = load(integer_path)
        scale = F(ii['scale'])
        assert scale > 0 and scale.denominator == 1
        assert F(ii['objective_numerator']) == scale*newalpha
        for n, w in ii['integer_budget_weights'].items():
            assert F(w).denominator == 1
            assert F(w) == scale*(eps if n == 'ACTUAL_OPT_REQUERY_CUT' else newweights[n])
        assert vec(ii['all257_scaled_residuals']) == [scale*v for v in newh]

    ri = load(WS/'maximal_root_tail_wallet/exact_input.json')
    rc = load(WS/'maximal_root_tail_wallet/exact_certificate.json')
    paid = {n: F(v) for n, v in root['integer_positive_budgets'].items()}
    assert paid == {n: F(v) for n, v in rc['dual']['integer_row_weights'].items()}
    rby = {r['name']: r for r in ri['raw_rows']}
    rp, ro = map(F, rc['dual']['integer_equality_multipliers'])
    qroots = []
    for h in range(128):
        bits, rs = root_rows(h)
        for n in paid:
            assert rs[n] == F(rby[n]['a'].get(str(h), '0'))
        rho = -sum(paid[n]*rs[n] for n in paid)-rp*bits[0]-ro*bits[6]
        assert rho == F(root['all128_root_residuals'][str(h)]) == 112944305160*F(rc['dual']['column_residuals'][str(h)]) >= 0
        if rho == 0:
            qroots.append(h)
    assert qroots == [r['h'] for r in root['zero_root_types']]
    assert len(qroots) == 13
    assert rp-sum(paid[n] for n in paid if n.startswith('CAP_')) == 11595684007
    rw = vec(root['root_constant'], 128); re = vec(root['root_e_direction'], 128); rsig = vec(root['root_sigma_direction'], 128)
    K, u = c[256], dot(u1, c)
    for n in paid:
        rv = vec(rby[n]['a'], 128)
        val = dot(rv, rw)+F(rby[n]['a'].get('128', '0'))*u-F(rby[n]['bK'])*K-F(rby[n]['bO'])
        assert val == dot(rv, re) == dot(rv, rsig) == 0
    for pbit, obit in product((0, 1), repeat=2):
        vis = [int(format(j, '08b')[5]) == pbit and int(format(j, '08b')[7]) == obit for j in range(256)]
        hid = [int(format(h, '07b')[0]) == pbit and int(format(h, '07b')[6]) == obit for h in range(128)]
        assert sum(rw[h] for h in range(128) if hid[h]) == sum(c[j] for j in range(256) if vis[j])
        assert sum(re[h] for h in range(128) if hid[h]) == 0
        assert sum(rsig[h] for h in range(128) if hid[h]) == sum(e[j] for j in range(256) if vis[j])
        assert sum(d[j] for j in range(256) if vis[j]) == 0
    erootlo, eroothi = F(root['e_lower_from_root71']), F(root['e_upper_from_root71'])
    assert erootlo == 0 < eroothi
    for r, desc in zip(ri['raw_rows'], root['all71_root_row_affine_slacks']):
        rv = vec(r['a'], 128)
        a = dot(rv, rw)+F(r['a'].get('128', '0'))*u-F(r['bK'])*K-F(r['bO'])
        b = dot(rv, re)
        assert a == F(desc['constant']) and b == F(desc['e'])
        assert dot(rv, rsig) == 0 and a+b*erootlo >= 0 and a+b*eroothi >= 0
    for h in range(128):
        for ev in [erootlo, eroothi]:
            assert rw[h]+ev*re[h]+ev*rsig[h] >= 0
    assert rw[33] == re[33] == rsig[33] == 0
    for h in qroots:
        bits = tuple(map(int, format(h, '07b')))
        assert bits[1] >= bits[0]
        if not bits[0]:
            assert sum(bits[1:6]) <= 1
    for j in S:
        if j == 256:
            continue
        bits = tuple(map(int, format(j, '08b')))
        assert not (bits[4] and bits[5])
        assert not bits[6] or sum(bits[:4]) == 0
    candidates = []
    for j in S:
        if j == 256:
            continue
        v = tuple(map(int, format(j, '08b')))
        for h in qroots:
            w = tuple(map(int, format(h, '07b')))
            if h != 33 and v[5] == w[0] and v[7] == w[6]:
                candidates.append({'v': j, 'h': h})
    assert candidates == root['compatible_joint_atom_pairs_after_forced_B2_identity'] and len(candidates) == 57
    report = {
        'status': 'PASS_EXACT_WHOLE_FACE_SOURCE_EQUALITIES_AND_STRICT_UNIVERSAL_DUAL',
        'optimizer_calls': 0, 'old_rows': 221, 'columns': 257,
        'complementarity_rank': 11, 'complementarity_columns': 13,
        'face_t_interval': [str(lo), str(hi)], 'free_sigma_nonnegative': True,
        'K_fixed': str(K), 'u1_fixed': str(u),
        'SAFE6_X': '(t-t_lower)/2; zero only at the lower endpoint',
        'RC_X_Omean': 'zero on the whole face; exactly the MX8 row',
        'signed_identities': len(signed), 'signed_identity_columns_checked': 257*len(signed),
        'requery_state_checks': literal_report['states'], 'requery_envelopes': 128,
        'whole_face_cut_value': str(kappa), 'whole_face_excluded': True,
        'independent_conditional_forced_C_terminal_gain': str(forced_gain),
        'forced_C_equality_load_checks': equality_load_checks,
        'strict_dual_bound': str(newalpha), 'strict_dual_decimal': float(newalpha),
        'strict_dual_positive_budgets': sum(v > 0 for v in newweights.values())+1,
        'strict_dual_zero_columns': [j for j, v in enumerate(newh) if not v],
        'strict_dual_positive_columns': sum(v > 0 for v in newh),
        'root_source128_checked': True, 'root_zero_types': qroots,
        'root_equal_B2_and_C_is_coverage_only': True,
        'compatible_joint_types': 57, 'joint_feasibility_claimed': False,
        'previous_frozen_files_unchanged': len(previous),
        'not_claimed': ['222-row optimized value', 'half coverage', 'complete SPE construction', 'branch-independent gluing'],
    }
    (HERE/'literal_requery_check.json').write_text(json.dumps(literal_report, ensure_ascii=False, indent=2)+'\n')
    (HERE/'exact_check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
