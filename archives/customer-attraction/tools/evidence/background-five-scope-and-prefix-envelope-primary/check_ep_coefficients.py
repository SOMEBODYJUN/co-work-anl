"""New EP complete coefficient checks and finite algebra controls.

Does not run missing original probes, a SPE solver, or any LP/MILP.
The 1960-row domain is the entire local coefficient domain, not sampled games.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
import sys


def share(n, d):
    return F(n, d) if n else F(0)


def terms(a, b, e1, e2, p, d, ell):
    total = p + a + b
    alpha, beta = share(a, total), share(b, total)
    G = 6 * alpha + beta / 2 - F(d, p + 1) - F(ell, 12 * (p + a + 1)) + F(d * ell, 6 * (p + 1) * (p + 2))
    H1 = share(e1, total) - F(a, 6)
    H2 = share(e2, total) - F(a, 6)
    L = beta - F(a, p + a + 1)
    base = 2 * int(total > 0) - int(d > 0) - G
    Q = base - F(5, 4) * H1 - F(5, 4) * H2 - L
    return G, H1, H2, L, Q


def main():
    out = Path(sys.argv[1]); assert sys.flags.optimize == 0 and out.is_dir() and not list(out.iterdir())
    rows, grouped = [], {}
    for a in [0, 1]:
        for early in product([0, 1], repeat=4):
            if a and not (early[2] and early[3]):
                continue
            p = sum(early)
            for b, d, ell in product([0, 1], range(7), range(7)):
                G, H1, H2, L, Q = terms(a, b, early[0], early[1], p, d, ell)
                assert Q >= 0
                row = {'a': a, 'b': b, 'early_memberships': early, 'p': p, 'd': d, 'ell': ell,
                       'G': str(G), 'H1': str(H1), 'H2': str(H2), 'L': str(L), 'Q': str(Q)}
                rows.append(row)
                key = (a, b, early[0], early[1], p)
                if key not in grouped or Q < grouped[key][0]:grouped[key] = (Q, d, ell)
    assert len(rows) == 1960 and min(F(x['Q']) for x in rows) == 0 and len(grouped) == 32
    corners = [(0, 0), (0, 6), (1, 0), (1, 6), (6, 0), (6, 6)]
    table = []
    for key, (minimum, _, _) in sorted(grouped.items()):
        a, b, e1, e2, p = key
        minimum_corner = min(terms(a, b, e1, e2, p, d, ell)[-1] for d, ell in corners)
        assert minimum == minimum_corner
        table.append({'a': a, 'b': b, 'e1': e1, 'e2': e2, 'p': p, 'minimum_Q': str(minimum)})
    obstruction = []
    for a, b, e1, e2, p, d, ell in [(1, 0, 0, 0, 2, 1, 0), (0, 0, 1, 0, 1, 1, 0), (0, 0, 0, 1, 1, 1, 0)]:
        G = terms(a, b, e1, e2, p, d, ell)[0]
        total = p + a + b
        K1 = share(e1, total) - F(a, 6) + (share(b, total) - F(e1, p + a + 1)) / 5
        K2 = share(e2, total) - F(a, 6) + (share(b, total) - F(e2, p + a + 1)) / 5
        base = 2 * int(total > 0) - int(d > 0) - G
        obstruction.append({'a': a, 'b': b, 'e1': e1, 'e2': e2, 'p': p, 'd': d, 'ell': ell,
                            'G': str(G), 'K1': str(K1), 'K2': str(K2), 'base': str(base)})
    assert [(x['G'], x['K1'], x['K2'], x['base']) for x in obstruction] == [
        ('5/3', '-1/6', '-1/6', '-2/3'), ('-1/2', '9/10', '0', '3/2'), ('-1/2', '0', '9/10', '3/2')]
    assert F(5, 3) * 2 < 4
    kernels=[]
    for b in [1, 2, 3, 4, 5, 6, 10**30]:
        for k in range(7):
            for c in range(b, b+k+1):
                assert F(1,b+k)<=F(1,c)<=F(1,b)
                kernels.append({'b':b,'k':k,'c':c})
    envelope=[]
    for p,m in [(3,4),(4,3)]:
        weights={mask:mask for mask in range(1,8)}
        checks=0;empty_positions=0
        for t in range(1,m+1):
            for h in product(range(p),repeat=t):
                for tail in product(range(p),repeat=m-t):
                    z=h+tail
                    for a in h:
                        lower=upper=actual=F(0)
                        for mask,n in weights.items():
                            if not mask>>a&1:continue
                            prefix=sum(bool(mask>>x&1) for x in h)
                            load=sum(bool(mask>>x&1) for x in z)
                            assert prefix>=1
                            lower+=F(n,prefix+m-t);upper+=F(n,prefix);actual+=F(n,load)
                        assert lower<=actual<=upper
                        checks+=1;empty_positions+=int(a==3)
        envelope.append({'p':p,'m':m,'types_mask_to_unit_multiplicity':weights,'old_position_checks':checks,
                         'empty_topic_positions':empty_positions,'SPE_checks':0})
    beta=F(1499,750); lam=max(F(d*(5-d),(2+d)*4) for d in range(1,6));c=F(9,35)+2/(5+4*lam)
    assert lam==F(3,8) and c==F(257,455) and 1/c<2
    legal=[(u,v,u+v) for u,v in product(range(4),repeat=2) if u+v<=3]
    assert len(legal)==10 and comb(11,5)==462
    report={'scope':'new EP complete local coefficient proof and finite algebra, not historical probes or SPE replay',
            'containment_complete_domain':rows,'containment_minimum_Q':'0','compressed_minimum_table':table,
            'six_corner_reduction_validated_for_each_class':True,'uniform_K_three_rows':obstruction,
            'prefix_scalar_kernels':kernels,'prefix_all_completion_checks':envelope,
            'background_scope':{'if_three_coordinates_are_A_B_AB_loads':'b_AB=b_A+b_B',
                                'legal_vectors_inside_0_to_3_cube':legal,'cube_size':64,
                                'old_probe_background_interpretation_certified':False,
                                'five_multisets_of_seven_indices':462,'high_background_lambda_5_2':str(lam),
                                'high_background_c_5_2':str(c),'high_background_beta_5_2':str(1/c),
                                'beta4':str(beta),'old_probe_runs':0},
            'all_big_analytic_controls':[{'m':m,'p':p,'W':m,'OPT':2*m-1,'each_u':1,'gap_over_min_u':m-1,
                                         'historical_saved_candidate_identity_claimed':False}
                                        for m,p in [(3,6),(4,5),(5,7)]],
            'original_entries':0,'LP_MILP_calls':0,'SPE_games_sampled':0,'general_half_proved':False}
    (out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'pass','complete_containment_coefficients':len(rows),'compressed_classes':len(table),
                      'minimum_Q':'0','K_obstruction_rows':len(obstruction),'prefix_scalar_kernels':len(kernels),
                      'old_position_checks':sum(x['old_position_checks'] for x in envelope),'original_entries':0,
                      'LP_MILP_calls':0,'SPE_games_sampled':0}))


if __name__=='__main__':main()
