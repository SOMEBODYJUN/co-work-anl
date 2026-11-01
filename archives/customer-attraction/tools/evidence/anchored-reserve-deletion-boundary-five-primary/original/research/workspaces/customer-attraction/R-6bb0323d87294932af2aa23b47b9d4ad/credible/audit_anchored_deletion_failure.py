"""Independent unit-customer full positive-depth audit; standard library only.

The general candidate being falsified is J_actual-deletions <= 2W for every
sunk-root continuation SPE. This is NOT a Q-CAG-HALF counterexample.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
LABELS=('A','B','T','D','E','empty')
TYPES=((('B',),3),(('T',),3),(('A','D'),2),(('A','E'),2),(('B','D','E'),2),(('T','D','E'),2))
UNITS=[frozenset(LABELS.index(a) for a in likes) for likes,n in TYPES for _ in range(n)]
M=3; E=5

def utility(leaf,i):
    a=leaf[i]
    return sum((F(1,sum(t in B for t in leaf)) for B in UNITS if a in B),F(0))
def welfare(leaf):return sum(any(a in B for a in leaf) for B in UNITS)
def query(a,background):
    return sum((F(1,1+sum(t in B for t in background)) for B in UNITS if a in B),F(0))
def last_br(h):
    return max(range(6),key=lambda a:(utility(h+(a,),2),-a))
policy={}
# The actual sunk-empty child reproduces the known residual-counterexample
# response map. Empty deviations are completed with a genuine last BR.
known=(1,3,3,4,3,3)
for a,b in product(range(6),repeat=2):
    policy[(a,b)]=known[b] if a==E else last_br((a,b))
for a in range(6):
    policy[(a,)]=0 if a==E else max(range(6),key=lambda b:(utility((a,b,policy[(a,b)]),1),-b))
policy[()]=E

def rollout(h):
    while len(h)<M:h=h+(policy[h],)
    return h

def main():
    comparisons=[]
    for d in (1,2):
        for h in product(range(6),repeat=d):
            prescribed=rollout(h);u=utility(prescribed,d)
            for a in range(6):
                deviation=rollout(h+(a,))
                gap=u-utility(deviation,d)
                assert gap>=0,(h,a,gap)
                comparisons.append(gap)
    leaf=rollout(());W=welfare(leaf);opt=max(map(welfare,product(range(6),repeat=3)))
    assert leaf==(E,0,1) and W==9 and opt==14
    backgrounds=((E,1),(E,0))
    matrices=[[query(a,q) for a in range(6)] for q in backgrounds]
    assert all(row[2]==5 and max(row)==5 for row in matrices)
    # For ANY mixing lambda, pure T is a dual lower bound t>=5, and all
    # entries are <=5, hence the free-mixture restricted value is exactly5.
    r=2;k=3;C=k+r-1
    J=C*F(5);assert J==20>2*W
    nonactual=(E,3)
    nonactual_prices=[query(a,nonactual) for a in range(6)]
    assert max(nonactual_prices)==4
    root_u=utility(leaf,0)
    root_deviations=[utility(rollout((a,)),0) for a in range(6)]
    assert root_u==0 and max(root_deviations)>root_u
    report={'status':'PASS','scope':'All positive-depth original-game SPE inequalities; root is deliberately arbitrary and fails optimality. Refutes only actual-deletion anchored budget, not root-only half or Q-CAG-HALF.','unit_customers':len(UNITS),'players':M,'topics':LABELS,'positive_depth_nodes':6+36,'comparisons_including_self':len(comparisons),'min_slack':str(min(comparisons)),'actual_leaf':[LABELS[a] for a in leaf],'actual_payoffs':[str(utility(leaf,i)) for i in range(3)],'W':W,'OPT_3':opt,'half_margin':2*W-opt,'deletion_backgrounds':[[LABELS[a] for a in q] for q in backgrounds],'deletion_query_vectors':[[str(x) for x in row] for row in matrices],'ancestor_reserve':'0','restricted_query_value':'5','coefficient':C,'J':str(J),'violation':str(J-2*W),'nonactual_background':[LABELS[a] for a in nonactual],'nonactual_query_vector':list(map(str,nonactual_prices)),'nonactual_budget':str(C*max(nonactual_prices)),'root_deviation_payoffs':list(map(str,root_deviations)),'policy':[{'history':[LABELS[a] for a in h],'action':LABELS[a]} for h,a in sorted(policy.items(),key=lambda z:(len(z[0]),z[0]))],'types':[{'likes':list(likes),'count':n} for likes,n in TYPES]}
    dest=Path(__file__).with_name('anchored_deletion_failure_exact.json');dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','positive_depth_nodes','comparisons_including_self','actual_leaf','W','OPT_3','J','violation','nonactual_budget')}))
if __name__=='__main__':main()
