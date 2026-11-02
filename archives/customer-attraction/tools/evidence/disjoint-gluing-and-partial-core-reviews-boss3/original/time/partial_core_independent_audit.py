"""Independent unit-customer audit of two explicit partial-core tails.
No constructor, canonical model, SPE solver or verifier is imported.
The policy follows its prescribed three-action tail, and chooses D forever
immediately after any first deviation from that tail.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
S={}
X=[{f'x{j}_{a}' for a in range(2)} for j in range(2)]
P=[{f'p{j}_{a}' for a in range(3)} for j in range(2)]
Y={f'y{a}' for a in range(4)};Z={f'z{a}' for a in range(4)}
E=[{f'e{j}_{a}' for a in range(n)} for j,n in enumerate([18,12,12])]
for j in range(2):
 S[f'C{j}']=X[j];S[f'A{j}']=X[j]|P[j]
 S[f'T1_{j}']=E[0]|E[1]|X[j]|P[j]
 S[f'T2_{j}']=E[0]|E[2]|X[j]|P[j]
S['CB']=Y;S['AB']=Y|Z;S['T3']=E[1]|E[2]|Y|Z;S['D']=set.union(*E)
names=tuple(S);k=len(names);topics=list(S.values());idx={a:i for i,a in enumerate(names)}
units=sorted(set.union(*topics));r=3

def pay_path(z,i):
 return sum((F(1,sum(x in topics[b] for b in z)) for x in topics[z[i]]),F())
def audit(prefix_names,tail_names):
 prefix=tuple(idx[a] for a in prefix_names);tail=tuple(idx[a] for a in tail_names)
 policy={h:(tail[t] if h==tail[:t] else idx['D']) for t in range(r) for h in product(range(k),repeat=t)}
 def execute(h):
  while len(h)<r:h=h+(policy[h],)
  return prefix+h
 slacks=[]
 for t in range(r):
  for h in product(range(k),repeat=t):
   own=pay_path(execute(h),len(prefix)+t)
   for b in range(k):slacks.append(own-pay_path(execute(h+(b,)),len(prefix)+t))
 assert min(slacks)>=0
 dominance=[]
 for a,b,c in product(range(k),repeat=3):
  dominance.append(pay_path(prefix+(a,b,idx['D']),len(prefix)+2)-pay_path(prefix+(a,b,c),len(prefix)+2))
 assert min(dominance)>=0
 actual=execute(())
 return dict(prefix=prefix_names,tail=tail_names,root_payoffs=[str(pay_path(actual,i)) for i in range(len(actual))],ordered_tail_nodes=len(policy),all_legal_action_comparisons=len(slacks),minimum_slack=str(min(slacks)),static_D_dominance_comparisons=len(dominance),minimum_D_dominance_slack=str(min(dominance)),policy={','.join(map(str,h)):a for h,a in policy.items()})
small=audit(['A0','C1','CB'],['T1_0','T2_0','T3'])
big=audit(['C0','C1','AB'],['T3','T1_0','T2_1'])
assert small['root_payoffs']==['5/3','2','2','50/3','50/3','18']
assert big['root_payoffs']==['1','1','4','16','19','19']
# The final C in C0,C1,CB,D,D,D is CB. Its bank deviation guarantees R/4
# under every possible continuation, not merely the prescribed punishment.
reserve=42;last_c_payoff=4;guarantee=F(reserve,r+1)
assert guarantee>last_c_payoff
report=dict(status='EXACT_CHECK_PASSED',scope='Two fixed-prefix three-player continuation SPEs only; not a full root SPE or half counterexample.',unit_customers=len(units),topics=list(names),players=6,small=small,big=big,candidate_root_test=dict(candidate_prefix=['C0','C1','CB'],candidate_tail=['D']*r,last_C_payoff=last_c_payoff,D_deviation_guarantee=str(guarantee),strict_gain=str(guarantee-last_c_payoff)))
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(report,small={a:b for a,b in small.items() if a!='policy'},big={a:b for a,b in big.items() if a!='policy'}),indent=2))
