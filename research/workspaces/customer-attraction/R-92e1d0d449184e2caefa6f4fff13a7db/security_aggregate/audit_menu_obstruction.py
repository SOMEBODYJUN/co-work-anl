"""Definition-level rational audit. No project solver or discovery imports."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
import json

WEIGHTS={3:2,4:3,8:2,9:3}
MENU=((0,3),(0,3),(2,0),(3,0))
P=(F(3,10),F(0),F(2,5),F(3,10))
ROOT_Q={(0,3):F(3,5),(0,2):F(1,5),(2,3):F(1,5)}
LOCAL_Q=((F(0),F(0),F(1,3),F(2,3)),
         (F(0),F(0),F(1,8),F(7,8)),
         (F(1,2),F(0),F(0),F(1,2)),
         (F(2,3),F(0),F(1,3),F(0)))

# Expand different unit customers before computing any payoff.
CUSTOMERS=tuple(t for t,r in WEIGHTS.items() for _ in range(r))
def payoff(a,z):
    return sum((F(1,sum(bool(t&(1<<b)) for b in z))
                for t in CUSTOMERS if t&(1<<a)),F())
def welfare(z):return sum(any(t&(1<<b) for b in z) for t in CUSTOMERS)
def fixed_query(a,background):return payoff(a,(a,)+tuple(background))

roots=[];branches=[]
for a,tail in enumerate(MENU):
    z=(a,)+tail
    roots.append(payoff(a,z))
    tail_sum=sum((payoff(b,z) for b in tail),F())
    local_values=[sum((LOCAL_Q[a][b]*fixed_query(c,(a,b)) for b in range(4)),F())
                  for c in range(4)]
    assert tail_sum>=2*max(local_values)
    last_values=[payoff(c,z[:-1]+(c,)) for c in range(4)]
    assert payoff(z[-1],z)==max(last_values)
    branches.append(dict(root=a,terminal=z,root_payoff=payoff(a,z),tail_sum=tail_sum,
                         local_static_dual_values=local_values,local_static_cap=max(local_values),
                         last_query_values=last_values))
assert roots[0]==max(roots)==2
assert welfare((0,)+MENU[0])==7
root_values={b:sum((P[a]*fixed_query(a,b) for a in range(4)),F())
             for b in combinations_with_replacement(range(4),2)}
assert min(root_values.values())==F(12,5)
root_dual_values=[sum((q*fixed_query(a,b) for b,q in ROOT_Q.items()),F()) for a in range(4)]
assert max(root_dual_values)==F(12,5)
assert 3*min(root_values.values())-7==F(1,5)
deviation_last_values=[payoff(c,(0,2,c)) for c in range(4)]
assert deviation_last_values[3]==max(deviation_last_values)
assert sum(x==max(deviation_last_values) for x in deviation_last_values)==1
assert payoff(2,(0,2,3))==3>payoff(0,(0,0,3))==2

# Existing H_I interval recurrence, reproduced only to compare identities.
# This screen rejects the fake menu, so this is not a G_I counterexample.
@lru_cache(None)
def interval_terminals(prefix):
    if len(prefix)==3:return frozenset([prefix])
    children={a:interval_terminals(tuple(sorted(prefix+(a,)))) for a in range(4)}
    floor=max(min(payoff(a,z) for z in outcomes) for a,outcomes in children.items())
    actions=[a for a,outcomes in children.items() if max(payoff(a,z) for z in outcomes)>=floor]
    return frozenset.union(*(children[a] for a in actions))
assert interval_terminals(())==frozenset([(0,2,3)])
assert (0,0,3) not in interval_terminals((0,))

def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list,set,frozenset)):return [clean(v) for v in x]
    return x
result=dict(status='PASS: compressed root-menu interface only; not a SPE',unit_customers=len(CUSTOMERS),
            types=WEIGHTS,branches=branches,root_payoffs=roots,W=7,OPT=10,
            static_root_primal_values=root_values,static_root_dual_values=root_dual_values,
            v3=F(12,5),three_v_minus_W=F(1,5),
            mandatory_penultimate_violation=dict(history=(0,),actual_action=0,actual_payoff=2,
                deviation_action=2,last_query_values=deviation_last_values,unique_last_best_reply=3,
                deviation_payoff=3),
            interval_root_terminals=interval_terminals(()),
            not_refuted=['Q-CAG-HALF','true SPE W >= m v_m','weak security bridge','G_I half'])
print(json.dumps(clean(result),indent=2))
