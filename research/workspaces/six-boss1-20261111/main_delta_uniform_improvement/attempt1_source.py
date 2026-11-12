"""Main: directly paid delta cuts and a uniform exact improvement, no LP.

The root remainder and all 513 homogeneous columns are independently replayed.
The two new C cuts are reconstructed from all true hidden states, not the face.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

W = Path(__file__).resolve().parent
P = W / 'main_delta_uniform_improvement'
ATOMS = list(product((0, 1), repeat=9))


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def sparse(v):
    return {str(h): str(x) for h, x in enumerate(v) if x}


def true_cost(p, c, o, tail, tau, beta, a):
    L = p+c+sum(tail)
    num = a*c-tail[3]-sum(tau[j]*tail[j] for j in range(3))
    assert L or num == 0
    value = num/L if L else F(0)
    value += sum(beta[j]*tail[j] for j in range(3))+tail[3]
    value += F(o, 6*(p+c+sum(tail[:3])+1))
    value += sum((tau[j]*F(o, 6*(p+c+sum(tail[:j])+4-j)) for j in range(3)), F(0))
    return value


def main():
    P.mkdir(exist_ok=True)
    assert not (P/'exact_certificate.json').exists()
    inp_path = W/'visible_maximum_joint_v5/exact_input.json'
    cert_path = W/'visible_maximum_joint_v5_solve/exact_certificate.json'
    root_input_path = W/'maximal_root_tail_wallet_v3/exact_input.json'
    root_cert_path = W/'maximal_root_tail_wallet_v3/exact_certificate.json'
    assert sha(inp_path) == '12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
    assert sha(cert_path) == 'c29c711bdbfeac80265c8806b1a76e8e5810277c2a11801335d35cc4f3bdb265'
    assert sha(root_input_path) == '01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0'
    assert sha(root_cert_path) == 'b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925'
    assert read(W/'main_visible_c_v5_certificate_check.json')['status'] == 'PASS_MAIN_FULL3056_RAW513_DUAL_FULL_FACE_AND_FRESH_TRUE_C_BRANCH'
    inp, cert = read(inp_path), read(cert_path)
    rows, eqs = inp['raw_rows'], inp['equalities']
    y = list(map(F, cert['dual']['raw_row_weights']))
    old_residual = list(map(F, cert['dual']['nonnegative_column_residual']))
    old_eta = list(map(F, cert['dual']['equality_multipliers']))
    alpha = F(cert['objective'])
    eps, L1, L0 = F(1, 144), F(1, 180), F(101, 27648)
    tau0 = (F(0), F(5977, 6912), F(43, 48))
    tau = (F(0), tau0[1]-eps, tau0[2]+eps)
    beta = tuple(F(1, 12)+tau[j]+sum((tau[l]/(6*(4-l)*(5-l)) for l in range(j+1, 3)), F(0)) for j in range(3))
    assert min(tau) >= 0 and min(beta) > 0 and sum(tau) == sum(tau0)
    S0, S1 = F(1528993, 497664), 1+sum(beta)
    assert S1 == S0+eps/24
    EC = [F(eqs[1]['a'].get(str(h), '0')) for h in range(513)]
    O = [F(eqs[0]['a'].get(str(h), '0')) for h in range(513)]
    targetW = [F(inp['objective'].get(str(h), '0')) for h in range(513)]
    K = [F(0)]*512+[F(1)]
    M0 = [F((1-b[0])*b[8]*(1-b[7])) for b in ATOMS]+[F(0)]
    M1 = [F(b[0]*b[8]*(1-b[7])) for b in ATOMS]+[F(0)]
    Cout = [a+b for a, b in zip(M0, M1)]
    Oout = [F(b[7]*(1-b[8])) for b in ATOMS]+[F(0)]
    Delta = [F(b[7]*(1-b[8]), 6*(b[0]+2)*(b[0]+3)) for b in ATOMS]+[F(0)]
    direct_delta = [F(b[7], 6*(b[0]+3*b[8]+2))-F(b[7], 6*(b[0]+2*b[8]+3)) for b in ATOMS]+[F(0)]
    assert Delta == direct_delta
    LD = [v-o/72 for v, o in zip(Delta, Oout)]
    assert min(LD) >= 0
    assert all(Oout[h] == O[h]-K[h]+Cout[h]-EC[h] for h in range(513))
    cut_records, all_states = [], []
    for s, old_raw in [(F(0), 2606), (F(61273, 6912), 1803)]:
        a = 25+sum(tau)-s
        assert a > 0
        minima = {}; state_records = []
        for p, c, o in product((0, 1), repeat=3):
            vals = {tail: true_cost(p, c, o, tail, tau, beta, a) for tail in product((0, 1), repeat=4)}
            minimum = min(vals.values()); minima[p, c, o] = minimum
            costs = [{'tail': list(t), 'cost': str(v), 'residual_to_minimum': str(v-minimum)} for t, v in vals.items()]
            old_anchor = c*(S0+F(24, p+5)-s/5)+F(o, 6*(p+4*c+1))
            old_anchor += sum((tau0[j]*F(o, 6*(p+(j+1)*c+4-j)) for j in range(3)), F(0))
            deltaN = F(o, 6*(p+3*c+2))-F(o, 6*(p+2*c+3))
            loss = L1*p*c*(1-o)+(L0*(1-p)*c*(1-o) if s else F(0))
            assert minimum == old_anchor+(S1-S0)*c+eps*deltaN-loss
            state_records.append({'pco': [p,c,o], 'minimum': str(minimum), 'all_costs': costs,
                                  'all_weak_tails': [list(t) for t,v in vals.items() if v == minimum],
                                  'loss_from_shifted_anchor': str(loss)})
        cs = []
        for h in range(513):
            if h == 512:
                val = S1
            else:
                b = ATOMS[h]; load_ = sum(b[:6]); u2 = F(b[1], load_) if load_ else F(0)
                val = a*u2-minima[b[0], b[8], b[7]]
            val += (S1-s/5)*EC[h]
            old = F(rows[old_raw]['a'].get(str(h), '0'))+(S0*EC[h] if s == 0 else 0)
            assert val == old-eps*Delta[h]+L1*M1[h]+(L0*M0[h] if s else 0)
            cs.append(val)
        cut_records.append({'name': 'C_DELTA_EPS_S0' if s == 0 else 'C_DELTA_EPS_SSTAR',
                            's': str(s), 'a': str(a), 'tau': list(map(str,tau)),
                            'beta': list(map(str,beta)), 'S': str(S1),
                            'free_C_equality_multiplier': str(S1-s/5),
                            'a_coefficients': sparse(cs), 'rhs': '0', 'numerical_divisor': '25'})
        all_states.append({'s': str(s), 'states': state_records})

    # Replay the already proved ROOT270 certificate and its C\O remainder.
    ri, rc = read(root_input_path), read(root_cert_path)
    rys = {n:F(v) for n,v in rc['dual']['original_unscaled_row_weights'].items()}
    assert all(v > 0 for v in rys.values()) and len(rys) == 10
    root_rows = {r['name']:r for r in ri['raw_rows']}
    rEC, rEO = F(rc['dual']['equality_C_size']), F(rc['dual']['equality_OPT_union'])
    root_a, root_b = F(rc['universal_root_line']['a']), F(rc['universal_root_line']['b'])
    root_atoms = list(product((0,1), repeat=7))
    rho = []
    for h in range(129):
        want = F(h == 128)-sum((v*F(root_rows[n]['a'].get(str(h),'0')) for n,v in rys.items()),F(0))
        if h < 128:
            want -= rEC*root_atoms[h][0]+rEO*root_atoms[h][6]
        assert want == F(rc['dual']['column_residuals'][str(h)]) >= 0
        rho.append(want)
    assert -root_a+sum((v*F(root_rows[n]['bK']) for n,v in rys.items()), F(0))+rEC == 0
    assert -root_b+sum((v*F(root_rows[n]['bO']) for n,v in rys.items()), F(0))+rEO == 0
    root_eta = F(1087978231314917, 84387869309613600)
    assert min(rho[h] for h,b in enumerate(root_atoms) if b[0] and not b[6]) == root_eta
    assert all(rho[h]-root_eta*b[0]*(1-b[6]) >= 0 for h,b in enumerate(root_atoms))
    root_strong = [F(rows[868]['a'].get(str(h),'0'))-root_eta*Cout[h] for h in range(513)]
    for h in range(513):
        u1 = F(ATOMS[h][0],sum(ATOMS[h][:6])) if h<512 and sum(ATOMS[h][:6]) else F(0)
        assert F(rows[868]['a'].get(str(h),'0')) == u1-root_a*K[h]-root_b*O[h]

    lambda0, lambdar = y[2606], y[868]
    boost = lambda0*eps/72
    assert boost > 0
    outside_pay0 = lambdar*root_eta+boost
    outside_pay1 = outside_pay0-lambda0*L1
    assert outside_pay0 > 0 and outside_pay1 > 0
    alpha_new = (alpha+boost)/(1+boost)
    assert alpha_new > alpha and alpha_new < F(1,2)
    # Expand W-K as six actually valid SAFE_i(C) rows, residual, and EC.
    safe_raw = [8*i+7 for i in range(6)]
    safe_remainder = []
    for h in range(513):
        if h < 512:
            b=ATOMS[h]
            coeff=sum((F(b[8],sum(b[:i])+6-i) for i in range(6)),F(0))-b[8]
        else:
            coeff=F(0)
        assert coeff >= 0
        for i,k in enumerate(safe_raw):
            assert rows[k]['name'] == f'SAFE_{i+1}_8'
            want=(F(ATOMS[h][i],sum(ATOMS[h][:6])) if h<512 and sum(ATOMS[h][:6]) else F(0))
            if h<512:
                want -= F(ATOMS[h][8],sum(ATOMS[h][:i])+6-i)
            assert want == F(rows[k]['a'].get(str(h),'0'))
        assert targetW[h]-K[h] == sum((F(rows[k]['a'].get(str(h),'0')) for k in safe_raw),F(0))+coeff+EC[h]
        safe_remainder.append(coeff)
    # Keep all original rows; replace only the two explicitly strengthened rows.
    homogeneous = [[F(r['a'].get(str(h),'0'))-F(r['rhs'])*O[h] for h in range(513)] for r in rows]
    ynew = list(y)
    for k in safe_raw:
        ynew[k] += boost
    new_delta = [F(cut_records[0]['a_coefficients'].get(str(h),'0')) for h in range(513)]
    homogeneous[2606] = new_delta
    homogeneous[868] = root_strong
    newEC = old_eta[1]-lambda0*S0
    new_residual = [old_residual[h]+lambda0*eps*LD[h]+outside_pay0*M0[h]+outside_pay1*M1[h]+boost*safe_remainder[h] for h in range(513)]
    assert min(new_residual) >= 0
    positive = [k for k,v in enumerate(ynew) if v]
    column_checks = []
    for h in range(513):
        left=(1+boost)*targetW[h]-(alpha+boost)*O[h]
        right=sum((ynew[k]*homogeneous[k][h] for k in positive),F(0))+new_residual[h]+newEC*EC[h]
        assert left == right, (h,left-right)
        column_checks.append({'column':h,'left':str(left),'right':str(right),'residual':str(new_residual[h])})
    # The directly paid cut separates all affine directions of the old face.
    face=read(W/'visible_maximum_joint_v5_solve/optimal_face.json')
    coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
    face_values=[sum((new_delta[h]*cs[q] for h,cs in coords.items()),F(0)) for q in range(7)]
    assert all(v == 0 for v in face_values[1:]) and face_values[0] < 0
    Kface=sum((K[h]*cs[0] for h,cs in coords.items()),F(0))
    assert face_values[0] == -eps*(1-Kface)/36
    result={'status':'PASS_MAIN_UNIFORM_DELTA_ROOT_REMAINDER_FULL513_CERTIFICATE',
            'optimizer_calls':0,'alpha_old':str(alpha),'alpha_old_decimal':float(alpha),
            'boost':str(boost),'alpha_new':str(alpha_new),'alpha_new_decimal':float(alpha_new),
            'strict_improvement':str(alpha_new-alpha),'strict_improvement_decimal':float(alpha_new-alpha),
            'eps':str(eps),'root_C_outside_remainder':str(root_eta),
            'remaining_C_outside_A1_credit':str(outside_pay0),
            'remaining_C_inside_A1_credit':str(outside_pay1),
            'root_certificate_columns':131,'real_delta_hidden_states':256,'delta_full_columns':1026,
            'global_full_columns':513,'old_raw_rows_retained':3056,
            'new_positive_raw_weights_before_normalization':{str(k):str(ynew[k]) for k in positive},
            'replacements':{'868':'ROOT270_MINUS_ETA_C_OUTSIDE_O','2606':'C_DELTA_EPS_S0'},
            'free_C_equality_weight_before_normalization':str(newEC),
            'normalization_divisor':str(1+boost),'nonnegative_column_residual_before_normalization':list(map(str,new_residual)),
            'entire_old_face_delta_cut_value':str(face_values[0]),
            'scope':'Uniform universal bound for the original complete-history common-catalog six-player pure SPE model. O is any six legal query union. No LP rerun, no exact worst case, no half conclusion.',
            'source_pins':{str(p.relative_to(W)):sha(p) for p in [inp_path,cert_path,root_input_path,root_cert_path,W/'main_visible_c_v5_certificate_check.json']}}
    outputs={'exact_certificate.json':result,'two_true_delta_cuts.json':cut_records,
             'all256_true_delta_state_checks.json':all_states,'all513_global_identity_checks.json':column_checks,
             'root131_replay.json':{'root_eta':str(root_eta),'all129_remainders':list(map(str,rho)),
                                   'root_K_identity_residual':'0','root_O_identity_residual':'0'}}
    for name,value in outputs.items():
        (P/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['source_pins','new_positive_raw_weights_before_normalization','nonnegative_column_residual_before_normalization','scope']},ensure_ascii=False))


if __name__=='__main__':
    main()
