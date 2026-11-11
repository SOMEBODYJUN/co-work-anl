"""Main's source2/maximum-size line: all128 literal states, no optimization."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent


def load(p):
    return json.loads(p.read_text())


def main():
    states = []
    bases = []
    positive = zero = 0
    for a, t, q in product((0, 1), repeat=3):
        values = []
        m = 4*t+F(30*t, a+5)+F(q, a+1+4*t)
        for d3, d4, d5, z in product((0, 1), repeat=4):
            s = d3+d4+d5
            total = a+t+s+z
            source2_share = F(t, total) if total else F(0)
            terminal_share = F(z, total) if total else F(0)
            terminal_query = F(q, a+t+s+1)
            phi = 31*source2_share+(s+z)-terminal_share+terminal_query
            compact = (F(31*t-z, total) if total else F(0))+(s+z)+terminal_query
            assert phi == compact
            residual = phi-m
            assert residual >= 0
            values.append((phi, [d3, d4, d5, z]))
            positive += residual > 0
            zero += residual == 0
            states.append({'bits': [a,t,q,d3,d4,d5,z], 'Phi': str(phi), 'm': str(m), 'residual': str(residual)})
        assert min(v for v, _ in values) == m
        bases.append({'a': a, 't': t, 'q': q, 'm': str(m), 'minimizers': [b for v,b in values if v == m]})
    # Verify the monotone analytic proof separately from the minimum enumeration.
    decrease_checks = 0
    for a, q, z in product((0,1), repeat=3):
        for s in range(3):
            diff = 1-F(31-z, (a+1+s+z)*(a+2+s+z))-F(q, (a+2+s)*(a+3+s))
            assert diff <= 0
            decrease_checks += 1
    for a,q in product((0,1), repeat=2):
        final_diff = 1+F(30,a+5)-F(31,a+4)
        assert final_diff < 0
        decrease_checks += 1
    old = load(WS/'universal_union_wallet_v3/exact_input.json')
    rows = {r['name']:r for r in old['raw_rows']}
    face = load(HERE/'face_certificate.json')
    gap = load(HERE/'signed_identities.json')['identities']['FORCED_MAX_C_TAIL_X_GAP']
    cut = {}
    for v in range(256):
        bits = tuple(map(int, format(v,'08b')))
        a,t,q = bits[0],bits[5],bits[6]
        load_actual = sum(bits[:6])
        u2 = F(bits[1],load_actual) if load_actual else F(0)
        cut[str(v)] = str(31*u2-4*t-F(30*t,a+5)-F(q,a+1+4*t))
    cut['256'] = '4'
    for j in range(257):
        value = 30*F(rows['SAFE_2_6']['a'].get(str(j),'0'))+4*F(rows['K_ge_size_6']['a'].get(str(j),'0'))-F(gap['target'][str(j)])
        assert value == F(cut[str(j)])
    dot = lambda field: sum(F(cut[str(j)])*F(face[field][str(j)]) for j in range(257))
    kappa = dot('constant')
    assert kappa == -F(gap['normalization']) < 0
    assert dot('t_direction') == dot('sigma_direction') == 0
    report = {
        'status': 'PASS_LITERAL128_STATES_EIGHT_MINIMA_AND_ALL257_VISIBLE_COLUMNS',
        'optimizer_calls': 0,
        'scope': 'For every actual source2 history(A1), every legal T,Q, and the same prescribed four-tail continuation after forcing T. K is true global maximum bare size; T need not attain K.',
        'budget_weights': {'SOURCE2_IC':31,'CAP_D3':1,'CAP_D4':1,'CAP_D5':1,'CAP_D6':1,'TERMINAL_BR_Q':1},
        'wallet': {'actual_u2':31,'K':4},
        'all128_states': states,'all8_minima':bases,
        'positive_residual_count':positive,'zero_residual_count':zero,
        'analytic_monotonicity_checks':decrease_checks,
        'all257_actual_T_A6_Q_X_coefficients':cut,
        'whole_v3_face_value':str(kappa),'whole_v3_face_value_decimal':float(kappa),
        'all257_identity':'SOURCE2_MAX_SIZE_CUT = 30 SAFE_2_6 + 4 K_ge_size_6 - FORCED_MAX_C_TAIL_X_GAP',
        'universal_line':'31u2+4K-4|T|-30 sum_T 1/(a1+5)-sum_Q 1/(a1+1+4t) >= 0',
        'not_used_in_existing_strict_dual':True,
        'not_claimed':['new LP optimum','half coverage','independent branch continuations'],
    }
    (HERE/'source2_max_size_cut.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['all128_states','all8_minima','all257_actual_T_A6_Q_X_coefficients']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
