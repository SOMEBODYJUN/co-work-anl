"""Independent exact arithmetic for the explicit uncompletable lure family.
No SPE oracle is assumed: the all-history contradiction is the proof in private_guard.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from two_support_obstruction import coeffs
HERE=Path(__file__).resolve().parent

def case(m):
    a=3*m*m-8*m+7;b=2*(m-1)*(m-2);c=6*(m-1)
    W=m*(b+c);O=m*(a+b+c);uB=F(m*b,m-2);uC=F(m*c,2)
    assert F(O,W)==F(5*m*m-8*m+5,2*(m*m-1))
    assert O>2*W and 2*a>a+b+c and a>uB
    assert a+F(b,m-1)+F(c,2)==uC
    assert F(m*c,3)==uB
    atoms,w,o,names,G=coeffs(m,(0,)*(m-2)+(1,1))
    # Every customer lies in exactly one optimal T_i (j=1).
    masses=[m*b if (B,C,j)==(1,0,1) else m*c if (B,C,j)==(0,1,1) else m*a if (B,C,j)==(0,0,1) else 0 for B,C,j in atoms]
    vals=[sum(x*n for x,n in zip(row,masses)) for row in G]
    assert all(v>=0 for v in vals)
    assert sum(x*n for x,n in zip(w,masses))==W
    assert sum(x*n for x,n in zip(o,masses))==O
    return {'m':m,'a':a,'b':b,'c':c,'W':W,'OPT':O,'ratio_of_impossible_path':str(F(O,W)),'B_player_payoff':str(uB),'C_player_payoff':str(uC),'private_guard_size_gap':2*a-(a+b+c),'strict_private_deviation_gap':str(a-uB),'all_actual_floor_and_last_two_tax_rows_nonnegative':True,'minimum_row_slack':str(min(vals)),'zero_rows':[name for name,v in zip(names,vals) if v==0]}

if __name__=='__main__':
    cases=[case(m) for m in range(7,51)]
    report={'status':'No SPE counterexample: every proposed path is ruled out for all full-history pure SPE by the private-guard backward induction.','audited_m_range':[7,50],'cases':cases,'m7_reduced':{'per_T_private':49,'per_T_B_shared':30,'per_T_C_shared':18,'T_size':97,'W':336,'OPT':679,'B_payoff':42,'C_payoff':63,'guard_gap':1,'deviation_private_gap':7}}
    (HERE/'private_guard_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'m7_impossible_path_ratio':cases[0]['ratio_of_impossible_path'],'minimum_guard_gap':min(x['private_guard_size_gap'] for x in cases),'all_necessary_rows_nonnegative':True}))
