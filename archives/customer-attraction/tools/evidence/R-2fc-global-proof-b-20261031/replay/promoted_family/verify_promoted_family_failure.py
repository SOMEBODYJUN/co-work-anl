from fractions import Fraction as F
from itertools import product
import json

def verify(t,k):
    assert t>=2 and k>=1
    m=k+t-1
    # symbolic target path consists of k C_i and t-1 D_r in any order.
    # Each target action has payoff t due to disjoint blocks.
    # Last C_i deviation to A_i gets 2t-1; last D_r deviation to A_i gets t/2+(t-1).
    c_gain=F(2*t-1)-t
    d_gain=F(t,2)+t-1-t
    return {'t':t,'k':k,'m':m,'target_payoff':t,'last_C_deviation':'%s'%F(2*t-1),'last_C_gain':'%s'%c_gain,'last_D_deviation':'%s'%F(t,2)+str(F(t-1)) if False else '%s'%F(t,2)+f'+{t-1}', 'last_D_deviation_exact':'%s'% (F(t,2)+t-1),'last_D_gain':'%s'%d_gain,'C_failure':c_gain>0,'D_failure':d_gain>0,'all_target_permutations_fail_for_t_gt_2':(t>2 and c_gain>0 and d_gain>0)}
rows=[verify(t,k) for t in range(2,7) for k in range(1,4)]
assert all(r['C_failure'] for r in rows)
assert all((r['D_failure']==(r['t']>2)) for r in rows)
assert rows[0]['last_D_gain']=='0'
print(json.dumps({'identity':'exact terminal-node obstruction for promoted punishment family','cases':rows,'scope':'symbolic last-player deviation; no solver/oracle inference'},indent=2))
