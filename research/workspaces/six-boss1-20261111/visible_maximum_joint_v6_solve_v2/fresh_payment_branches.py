#!/usr/bin/env python3
"""Post-solve exact diagnostics from this certificate only. No optimization.

Enumerate every weak tail of every positive projected row, retain literal
source metadata, and identify histories by their ordered label sequence.
This program never imports a builder, solver, or previous solution/face.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WS = HERE.parent
PINS = {}
INPUT_SHA = '8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769'
CERT_SHA = 'bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028'
FACE_SHA = '7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77'
SOURCE_HASHES = {
    'later_sources_lambda_cells/proof.md': '5dfb6e1ed29cd2955461bc15f8184246230de302ef43b6755c907c1b4173195a',
    'source2_conditional_redistribution/proof.md': '9b9128519aa12d2d9c11d197948751a21ed5f1039eb51640a26f1922e818ea1d',
    'all_source_minimal_cap_safe/proof.md': '30e2f3add32ec4d49192325dbe706e9d1c7e958722df0402d4699991fd9f69b6',
    'universal_true_x_tail/proof.md': '7208f00bd969c37ca156335a15659b71d4ddc301b017d20d77f96c0bac66732c',
    'main_thirty_index_strengthening/proof.md': 'd1b3fcec20b3694d76499bcc1566a6a89b80d5b9e738b6bc71d82a5f2bfb42ac',
    'registration/stage19-root270-addition.md': 'a15682dfbec23397ddb765b433a8dd6271d1b5108202dffb2f935383aec3e4b7',
    'main_root270_strict_outside/proof.md': '3671dd202a476f0cbd48fb5e74fd9912c0f12a0dd4edd7be007c32b880b22fdd',
    'main_delta_uniform_improvement/root131_replay.json': '112accfb4ca6886195e9d6983da21055a03868cc6c0c41bc74114b9f6b73aa6b',
    'visible_maximum_joint_v6_model_erratum.md': 'a2b83e67ce90597faa005cb893da647555bbb58b0d502fd3f03c12db924172b7',
    'main_v6_semantic_release.json': '36cdf31f302aefc738a300b9b25a5b29ef9a97e85bdf0499c2beba50bc153c85',
}


def read(path, expected=None, as_json=True):
    b = path.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    if expected is not None:
        assert h == expected, (str(path), h, expected)
    PINS[str(path.relative_to(REPO))] = {'sha256': h, 'bytes': len(b)}
    return json.loads(b) if as_json else b.decode()


def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def bits(n):
    return list(product((0, 1), repeat=n))


def share(atom, player):
    n = sum(atom[:6])
    return F(atom[player - 1], n) if n else F(0)


def actual_history(source, target):
    return [f'A{i}' for i in range(1, source)] + [target]


def full_identity(row, coeff):
    assert len(coeff) == 513 and F(row['rhs']) == 0
    dif = [coeff[j] - F(row['a'].get(str(j), '0')) for j in range(513)]
    assert not any(dif), (row['name'], [(j, str(x)) for j, x in enumerate(dif) if x][:8])
    return [str(v) for v in dif]


def wallet_parameters(row):
    m = row.get('source_row_metadata', row)
    w = m.get('weights', {})
    i = int(m['source'])
    tau = {int(k): F(v) for k, v in m.get('tau_by_true_source', w.get('tau', {})).items()}
    beta = {int(k): F(v) for k, v in m.get('middle_CAP_weights', w.get('beta', {})).items()}
    a = F(m.get('source_IC_weight', w.get('source_IC')))
    S = F(m.get('K_weight', m.get('total_K_weight', w.get('K_before_C_equality'))))
    mu = F(m.get('free_C_equality_multiplier', m.get('C_equality_multiplier')) or 0)
    target = m.get('forced_target', m.get('target'))
    target = 'C' if target == 'C-only' else target
    assert sorted(tau) == sorted(beta) == list(range(i + 1, 6))
    assert a > 0 and all(v >= 0 for v in tau.values()) and all(v > 0 for v in beta.values())
    assert S == 1 + sum(beta.values())
    for j in beta:
        assert beta[j] == F(1, 12) + tau[j] + sum(tau[k] / (6 * (7-k) * (8-k)) for k in tau if k > j)
    assert F(m.get('q0', '1/6')) == F(1, 6)
    lam = a - sum(tau.values())
    if 'lambda_value' in m:
        assert lam == F(m['lambda_value'])
    if 's' in m:
        assert 25 - lam == F(m['s'])
    return i, target, tau, beta, a, S, mu, lam


def wallet_cost(p, t, o, tail, i, tau, beta, a):
    r = {j: tail[j-i-1] for j in range(i+1, 7)}
    L = p + t + sum(tail)
    v = F(a*t-r[6]-sum(tau[j]*r[j] for j in tau), L) if L else F(0)
    v += sum(beta[j]*r[j] for j in beta) + r[6]
    slope = F(1, p+t+sum(tail[:-1])+1)
    slope += sum(tau[j] / (p+t+sum(r[h] for h in range(i+1, j))+7-j) for j in tau)
    assert slope > 0
    return v + F(o, 6)*slope, slope


def wallet_record(idx, row, atoms, weight):
    i, target, tau, beta, a, S, mu, lam = wallet_parameters(row)
    tables, minima = [], {}
    for p, t, o in product(range(i), (0, 1), (0, 1)):
        vals = [(tail, *wallet_cost(p, t, o, tail, i, tau, beta, a)) for tail in bits(6-i)]
        mn = min(v for _, v, _ in vals)
        minima[p, t, o] = mn
        tables.append({'p': p, 't': t, 'o': o, 'minimum': str(mn),
                       'weak_tails': [''.join(map(str, z)) for z, v, _ in vals if v == mn],
                       'all_tail_costs': [{'tail': ''.join(map(str, z)), 'cost': str(v),
                                           'residual': str(v-mn), 'query_slope': str(sl)} for z, v, sl in vals]})
    coeff = []
    for b in atoms:
        t = b[8] if target == 'C' else b[int(target[1:])-1]
        coeff.append(a*share(b, i)-minima[sum(b[:i-1]), t, b[7]]+mu*b[8])
    coeff.append(S-mu)
    return {
        'raw_index': idx, 'name': row['name'], 'raw_payment': str(weight),
        'source_metadata_verbatim': {k: v for k, v in row.items() if k != 'a'},
        'source': i, 'target': target, 'ordered_history': actual_history(i, target),
        'successor_order': [f'R{j}' for j in range(i+1, 7)],
        'source_IC_weight': str(a), 'lambda': str(lam), 's_25_minus_lambda': str(25-lam),
        'tau': {str(k): str(v) for k, v in tau.items()},
        'middle_CAP_weights': {str(k): str(v) for k, v in beta.items()},
        'terminal_CAP_weight': '1', 'terminal_BR_six_query_mean_weight': '1',
        'K_before_C_equality': str(S), 'signed_C_equality_multiplier': str(mu),
        'numerical_divisor_is_not_source_IC_weight': True,
        'all513_column_identity_residuals': full_identity(row, coeff),
        'state_tables': tables,
        'tightness': {
            'source_IC': True, 'all_successor_CAPs': True,
            'terminal_each_legal_query_BR': True,
            'internal_each_legal_query_SAFE_sources': [j for j, v in tau.items() if v > 0],
            'query_multiplicity_equals_union_membership': True,
            'all_weak_tails_retained_before_global_CAP_consequences': True,
        },
    }


def requery_cost(h, q, tail):
    a1, a2, a3, a4, a5, a6, o = h
    r, y, t = tail
    b = a1+a2
    D = 1+b+q+r
    return (F(126000*q, b+1+r+y+t) + F(43*r+31218*y+34458*t, b+a3+3)
            + F(1654*(r+y+t), b+a3+a4+a5+1) + 5400*(F(o, 6)-t)/(D+y)
            + 7740*(F(o, 3*D)-F(y, D+t)-F(t, D+y)-F(y, D*(D+1))))


def requery_tables():
    tables, m = [], {}
    for h in bits(7):
        qm = []
        qs = []
        for q in (0, 1):
            vals = [(z, requery_cost(h, q, z)) for z in bits(3)]
            lo = min(v for _, v in vals)
            qm.append(lo)
            qs.append({'q': q, 'minimum': str(lo),
                       'weak_tails': [''.join(map(str, z)) for z, v in vals if v == lo],
                       'all_tail_costs': [{'tail': ''.join(map(str, z)), 'cost': str(v), 'residual': str(v-lo)} for z, v in vals]})
        lo = qm[0] if not h[6] else min((5*qm[0]+qm[1])/6, qm[1])
        m[h] = lo
        tables.append({'actual_six_and_o': list(h), 'query_tables': qs,
                       'a1_minus_a0': str(qm[1]-qm[0]), 'union_envelope': str(lo),
                       'moment_interval': ['0', '0'] if not h[6] else ['1/6', '1'],
                       'minimizing_moments': ['0'] if not h[6] else (['1/6'] if qm[1] > qm[0] else ['1'] if qm[1] < qm[0] else ['all_[1/6,1]'])})
    return tables, m


def x_cost(b, y, t):
    B = sum(b[:3]); P = sum(b[:4]); D = P+1; d = B+b[6]+1; th = F(b[7], 6)
    return (F(4096*b[6], B+1+y+t)+F(800*y, D)+71*t +384*(th-t)/(d+y)
            +512*(F(b[5], d)+th/d-b[5]*th/(d*(d+1))-F(y, d+t)-F(t, d+y)-F(y, d*(d+1)))
            +900*((t+th)/D-t*th/(D*(D+1))))


def restrict(vector, face):
    assert len(vector) == 513
    constant = sum(vector[c['column']]*F(c['constant']) for c in face['coordinates'])
    pars = [sum(vector[c['column']]*F(c['parameter_coefficients'][k]) for c in face['coordinates'])
            for k in range(len(face['parameters']))]
    return {'constant': str(constant), 'parameter_coefficients': list(map(str, pars)),
            'fixed': not any(pars), 'full513_coefficients': list(map(str, vector))}


def main():
    data = read(WS/'visible_maximum_joint_v6/exact_input.json', INPUT_SHA)
    cert = read(HERE/'exact_certificate.json', CERT_SHA)
    face = read(HERE/'optimal_face.json', FACE_SHA)
    chk = read(HERE/'independent_check_result.json', 'daed49eecbec08d58884cff6c2b290e080e0bfcab81fd9ebb99921a2482dc18d')
    fchk = read(HERE/'optimal_face_check_result.json', '5e6e8d460f3ab98f09ec25f45f2f174a4302c21c9a591a2c2743a6943541b33b')
    assert chk['certificate_sha256'] == fchk['certificate_sha256'] == CERT_SHA
    assert fchk['face_sha256'] == FACE_SHA
    read(HERE/'main_release.json', '9aed677521b19c1c4c4a41a0ef644cf1f540c037c6509210107297479dc4d741')
    marker = read(HERE/'single_lp_consumed.json', '115a3c3ebbec578d682dd0355e8dbe21e78cddee700c2a2f24fb7dd6aa72a209')
    for path, sha in SOURCE_HASHES.items():
        read(WS/path, sha, as_json=False)
    atoms = [tuple(r['a'])+(r['x'], r['o'], r['c']) for r in data['atom_columns']]
    assert atoms == bits(9)
    rows = data['raw_rows']; weights = list(map(F, cert['dual']['raw_row_weights']))
    positive = [i for i, w in enumerate(weights) if w > 0]
    assert positive == [47, 134, 218, 221, 2564, 3459, 3468, 3739, 4012, 4067, 4107, 4176]
    wallet_ids = [i for i in positive if ('source_row_metadata' in rows[i] or rows[i].get('family') == 'ALL_SOURCE_MINIMAL_CAP_TRUE_INTERNAL_SAFE')]
    wallets = [wallet_record(i, rows[i], atoms, weights[i]) for i in wallet_ids]
    groups = []
    for history in sorted({tuple(r['ordered_history']) for r in wallets}):
        same = [r for r in wallets if tuple(r['ordered_history']) == history]
        intersections = []
        for k, first in enumerate(same[0]['state_tables']):
            common = set(first['weak_tails'])
            for r in same[1:]:
                s = r['state_tables'][k]
                assert [s[x] for x in ('p', 't', 'o')] == [first[x] for x in ('p', 't', 'o')]
                common &= set(s['weak_tails'])
            intersections.append({**{x: first[x] for x in ('p', 't', 'o')}, 'common_weak_tails': sorted(common),
                                  'empty_intersection_forces_projected_mass_zero': not common})
        groups.append({'ordered_history': list(history), 'raw_indices': [r['raw_index'] for r in same],
                       'successor_order': same[0]['successor_order'], 'all_state_intersections': intersections})

    # The two direct legacy wallet rows are reconstructed on every original column.
    coeff47 = [share(b, 6)-F(b[7], 6*(sum(b[:5])+1)) for b in atoms]+[F(0)]
    coeff134 = [share(b, 5)-F(b[7], 6*(sum(b[:4])+1))+F(b[6]*b[7], 6*(sum(b[:4])+1)*(sum(b[:4])+2)) for b in atoms]+[F(0)]
    direct = [
        {'raw_index': 47, 'name': rows[47]['name'], 'query': 'six_legal_query_union_mean',
         'history': ['A1','A2','A3','A4','A5'], 'budget': 'u6 - average_k final_BR_payoff(Qk)',
         'all513_column_identity_residuals': full_identity(rows[47], coeff47),
         'tightness': 'Every one of the six legal final-query BR budgets is zero; d=o on every customer.'},
        {'raw_index': 134, 'name': rows[134]['name'], 'queries': ['X', 'six_legal_query_union_mean'],
         'actual_potential_prefix': ['A1','A2','A3','A4'],
         'budget': 'u5+f_P(X) - average_k [f_P(X)+f_P(Qk)-g_P(X,Qk)]',
         'all513_column_identity_residuals': full_identity(rows[134], coeff134),
         'tightness': 'Every RC(X,Qk) wallet is tight; its own true reply histories are retained. The common X is globally maximal only at the actual first-four potential.'},
    ]

    xtables, xmins = [], {}
    for b in bits(8):
        vals = [(z, x_cost(b, *z)) for z in bits(2)]
        lo = min(v for _, v in vals); xmins[b] = lo
        xtables.append({'actual_six_x_o': list(b), 'minimum': str(lo),
                        'weak_tails': [''.join(map(str, z)) for z, v in vals if v == lo],
                        'all_tail_costs': [{'tail': ''.join(map(str, z)), 'cost': str(v), 'residual': str(v-lo)} for z, v in vals]})
    xcoeff = [4096*share(b, 4)+900*share(b, 5)+F(1700*b[6], sum(b[:4])+1)-xmins[b[:8]] for b in atoms]+[F(71)]
    xrecord = {'raw_index': 218, 'history': ['A1','A2','A3','X'], 'successor_order': ['Y','T'],
               'true_budget_weights': {'source4_IC': '4096','MAX_at_actual_P_of_Y': '800','CAP_T': '71',
                                       'branch_final_query_mean': '384','branch_PAIR_A6_query_mean': '512','actual_RC_T_query_mean': '900'},
               'all513_column_identity_residuals': full_identity(rows[218], xcoeff),
               'state_tables': xtables,
               'tightness': 'All six nonnegative wallets are zero; the same Y and T occur in every wallet. MAX uses actual P, not this forced-X prefix.'}

    qtables, qmins = requery_tables()
    qcoeff = [126000*share(b, 3)+65719*share(b, 4)+4962*share(b, 6)-qmins[b[:6]+(b[7],)] for b in atoms]+[F(0)]
    qrecord = {'raw_index': 221, 'history': ['A1','A2'],
               'nested_histories': '(A1,A2,Qk), separately for each legal query index k; continuation follows that actual ordered label history',
               'true_budget_weights': {'source3_IC': '126000','actual_source4_SAFE_R4': '43','actual_source4_SAFE_R5': '31218',
                                       'actual_source4_SAFE_R6': '34458','actual_source6_SAFE_each_R': '1654',
                                       'new_terminal_query_mean': '5400','new_PAIR30': '7740'},
               'all513_column_identity_residuals': full_identity(rows[221], qcoeff),
               'state_tables': qtables,
               'all_a1_minus_a0_strictly_positive': all(F(t['a1_minus_a0']) > 0 for t in qtables),
               'tightness': 'Every positive averaged wallet is tight, every true q-specific tail is a weak minimizer, and d=o because all moment slopes are positive.'}
    assert qrecord['all_a1_minus_a0_strictly_positive']

    # Reconstruct the root source certificate on all 128 customer columns plus u,K,O.
    den = F(67510295447690880)
    rootweights = [67510295447690880,622403086173831,3736778489617071,3696167188982850,
                   3608286607200810,3553563630176244,1712829042623520,2292281651099340,
                   24602518440,61096128288912]
    betaC = F(22380459227386502); betaO = F(1349360725088052)
    B = F(883952004100291,8438786930961360)
    O = F(37482242363557,1875285984658080)
    eta = F(1087978231314917,84387869309613600)
    rootstates = []
    replay = json.loads((WS/'main_delta_uniform_improvement/root131_replay.json').read_text())
    for idx, h in enumerate(bits(7)):
        aa = h[:6]; c,b2,b3,b4,b5,b6 = aa; o = h[6]
        L = sum(aa); vv = [F(x, L) if L else F(0) for x in aa]
        D = sum(aa[:4])+1; p = c+b2+b3
        budgets = [-vv[0],-b2,-b3,-b4,-b5,-b6,
                   vv[5]-F(o,6*(sum(aa[:5])+1)),
                   vv[4]+vv[5]+F(b5,D*(D+1))-F(o,3*D),
                   126000*vv[2]+65719*vv[3]+4962*vv[5]-qmins[h],
                   25*vv[3]-(F(3,2)+F(24,p+3))*b6-F(o,6*(p+1+2*b6))]
        rho = -(sum(w*v for w,v in zip(rootweights,budgets))+betaC*c+betaO*o)/den
        assert rho == F(replay['all129_remainders'][idx])
        adjusted = rho-eta*c*(1-o)
        assert adjusted >= 0
        rootstates.append({'index':idx,'c_b2_b3_b4_b5_b6_o':list(h),
                           'original_remainder':str(rho),'strict_outside_remainder':str(adjusted),
                           'ten_unscaled_budget_column_coefficients':list(map(str,budgets))})
    rk = sum(rootweights[1:6])+F(3,2)*rootweights[9]-betaC
    assert rk/den == -B and -betaO/den == -O and rootweights[0]/den == 1
    assert F(replay['all129_remainders'][128]) == 0
    rcoeff = [share(b,1)-O*b[7]-eta*b[8]*(1-b[7]) for b in atoms]+[-B]
    root = {'raw_index':4176,'history':['C'],'successor_order':['B2','B3','B4','B5','B6'],
            'K_coefficient_b':str(B),'O_coefficient_c':str(O),'outside_coefficient_eta':str(eta),
            'original_ten_budget_integer_weights':rootweights,'common_denominator':str(den),
            'budget_order':['root_IC','CAP_B2','CAP_B3','CAP_B4','CAP_B5','CAP_B6','terminal_six_SAFE_mean','PAIR30','C30_raw126000','source4_P25_raw25'],
            'signed_size_equality_integer_multiplier':str(betaC),'signed_O_equality_integer_multiplier':str(betaO),
            'all131_source_identity_residuals':['0']*131,
            'all513_column_identity_residuals':full_identity(rows[4176],rcoeff),'all128_states':rootstates,
            'weak_state_ids_before_face_C_outside_zero':[r['index'] for r in rootstates if F(r['strict_outside_remainder'])==0],
            'weak_state_ids_after_face_C_outside_zero':[r['index'] for r in rootstates if F(r['strict_outside_remainder'])==0 and not(r['c_b2_b3_b4_b5_b6_o'][0] and not r['c_b2_b3_b4_b5_b6_o'][-1])],
            'tightness':'All ten positive true wallets are zero. All CAPs give |Bj|=K. Query histories in C30/P25 retain their own successors.'}

    # New whole-face functionals, never inferred from just the returned support.
    functions = {}
    for name in ['u2_minus_K_over_5','C_outside_O','N4_C_minus_K_over_5','size_A5','size_A6','C_intersect_A1','C_outside_A1']:
        v = []
        for b in atoms:
            v.append({'u2_minus_K_over_5':share(b,2),'C_outside_O':F(b[8]*(1-b[7])),
                      'N4_C_minus_K_over_5':F(b[7],6*(b[0]+2*b[8]+3)),
                      'size_A5':F(b[4]),'size_A6':F(b[5]),'C_intersect_A1':F(b[8]*b[0]),'C_outside_A1':F(b[8]*(1-b[0]))}[name])
        v.append(F(-1,5) if name in ['u2_minus_K_over_5','N4_C_minus_K_over_5'] else F(0))
        functions[name] = restrict(v,face)
        assert functions[name]['fixed']
    assert F(functions['u2_minus_K_over_5']['constant']) == F(functions['C_outside_O']['constant']) == 0
    gap = F(functions['N4_C_minus_K_over_5']['constant'])
    assert gap > 0
    cg = next(g for g in groups if g['ordered_history']==['A1','C'])
    ct = {(s['p'],s['t'],s['o']):s['common_weak_tails'] for s in cg['all_state_intersections']}
    assert ct[0,1,1] == ['1111'] and ct[1,1,1] == ['1101','1110'] and ct[0,1,0] == []
    assert all(tail[:2]=='11' and p+1+sum(map(int,tail))==5 for p in (0,1) for tail in ct[p,1,1])
    obstruction = {
        'status':'EXACT_WHOLE_OPTIMAL_FACE_SPE_NONREALIZATION_OBSTRUCTION',
        'raw_indices':[4012,4067],'same_ordered_history':['A1','C'],
        'deduction_sequence':[
            'Any SPE attaining alpha maps into this exact complete face, so both positive-payment rows are tight.',
            'C-only is the general C budget plus mu*(|C|-K); this equality is zero in the original model.',
            'All weak tails at the same history must lie in the full intersection displayed above.',
            'The current complete face gives C outside O mass zero. On C, R3=R4=1 and total branch load=5.',
            'Both CAP weights are strictly positive; C is maximum and has mass K. Thus R3 and R4 cover exactly C (coverage, not label identity).',
            'The true source4 payoff on this forced-C branch is v4=K/5.',
            'At the actual internal history (A1,C,R3), true source4 SAFE against the six legal optimal queries gives v4>=sum o/[6(a1+c+r3+3)]=N4.',
            'Whole-face exact substitution gives N4-K/5=gap>0, contradicting that necessary SAFE inequality.'
        ],
        'positive_gap':str(gap),'positive_gap_decimal':float(gap),
        'strict_claim_boundary':'No SPE realizes any point on the alpha optimal face. This neither proves a uniform epsilon improvement nor half, and claims no SPE existence.',
        'coverage_equality_is_not_label_identification':True,
        'other_ordered_histories_were_not_merged':True,
    }
    result = {
        'schema':'v6_solve_v2_fresh_true_payment_diagnostics_v1',
        'status':'EXACT_FRESH_TRUE_BRANCH_DIAGNOSTICS_READY_FOR_INDEPENDENT_CHECK',
        'agent':'/root/visible_joint_v6_solve','optimizer_calls_total_v1_and_v2':1,'optimizer_calls_here':0,
        'input_sha256':INPUT_SHA,'certificate_sha256':CERT_SHA,'face_sha256':FACE_SHA,
        'corrected_X_model':{
            'P':'P_y=sum_{j=1}^4 1[y in actual A_j]',
            'selection':'One legal label X in argmax over the entire common catalog of sum_{y in Q} 1/(P_y+1)',
            'same_X_everywhere':True,'maximality_at_other_histories_assumed':False,
            'C':'a legal label maximizing bare coverage; K=|C|',
            'O':'union of six legal labels attaining OPT6; normalize only when OPT6>0',
            'histories':'complete ordered-label-history pure SPE; aliases, repeats, empty sets, and all weak ties allowed',
        },
        'fresh_positive_raw_indices':positive,
        'source_reading_scope':'Source formulas and universal certificate/replay only. Earlier point or face supports and their weak-state lists are not inputs to this diagnostic. Historical point numbers incidental to source prose are unused.',
        'all_positive_row_metadata':[{'raw_index':i,'raw_weight':str(weights[i]),'raw_row_metadata':{k:v for k,v in rows[i].items() if k!='a'}} for i in positive],
        'seven_minimal_CAP_rows':wallets,'same_history_weak_intersections':groups,
        'direct_legacy_wallets':direct,'true_X_tail_row':xrecord,'actual_requery30_row':qrecord,
        'root270_row':root,'fresh_full_face_functionals':functions,
        'whole_face_SPE_obstruction':obstruction,
        'checks':{'all_positive_rows_reconstructed':12,'all_original_columns_per_row':513,
                  'positive_row_column_identities':12*513,'minimal_CAP_local_tail_states':sum(len(t['all_tail_costs']) for r in wallets for t in r['state_tables']),
                  'X_local_tail_states':256*4,'requery30_local_tail_states':128*2*8,
                  'root_source_columns':131,'no_new_LP_input_or_row_written':True},
    }
    dump('fresh_diagnostic_source_pins.json',{'schema':'v6_fresh_diagnostic_pins_v1','files':PINS})
    result['diagnostic_source_pins_sha256']=hashlib.sha256((HERE/'fresh_diagnostic_source_pins.json').read_bytes()).hexdigest()
    dump('fresh_payment_branches.json',result)
    print(json.dumps({'status':result['status'],'all_positive_rows':12,'column_identities':12*513,
                      'complete_face_SPE_obstruction_gap':str(gap),'optimizer_calls_here':0},indent=2))


if __name__ == '__main__':
    main()
