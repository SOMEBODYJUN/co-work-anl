from pathlib import Path
from fractions import Fraction
from itertools import product
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'source'
audit=json.loads((source/'two_layer_occupancy_audit.json').read_text())
cand=json.loads((source/'two_layer_occupancy_candidate.json').read_text())
# Exact integer client multiset from the audit; candidate's six floating weights are 1/9 multiples.
weights={int(k):int(v) for k,v in audit['weights'].items()}
assert sum(weights.values())==audit['clients']==9
clients=[tuple(a for a in range(6) if mask>>a & 1) for mask,n in weights.items() for _ in range(n)]
policy={tuple(c):int(a) for c,a in cand['policy']}
assert len(policy)==28 and tuple([0]*6) in policy

def state(h):
 c=[0]*6
 for a in h:c[a]+=1
 return tuple(c)
def finish(h):
 h=tuple(h)
 while len(h)<3:h=h+(policy[state(h)],)
 return h
def utility(h,i):
 out=Fraction(0)
 for B in clients:
  if h[i] in B:
   load=sum(a in B for a in h)
   out += Fraction(1,load)
 return out
def covered(h):
 return sum(any(a in B for a in h) for B in clients)
def two_layer(h):
 return sum(min(2,sum(a in B for a in h)) for B in clients)
slacks=[]; strict=0
for d in range(3):
 for h in product(range(6),repeat=d):
  actual=finish(h); on=utility(actual,d)
  for a in range(6):
   off=utility(finish(h+(a,)),d); s=on-off
   assert s>=0,(h,a,s)
   slacks.append(s); strict+=int(s>0)
actual=finish(())
opt=max(covered(h) for h in product(range(6),repeat=3))
opt_paths=[h for h in product(range(6),repeat=3) if covered(h)==opt]
loads=[sum(a in B for a in actual) for B in clients]
comp=tuple(cand['comparison'])
obj=Fraction(two_layer(actual),len(clients))-Fraction(sum(any(a in B for a in comp) for B in clients),len(clients))
# Candidate objective is the normalized LP objective; its exact integer realization is -1/9.
result={
 'clients':len(clients),'actual_path':actual,'actual_vector':[actual.count(a) for a in range(6)],
 'payoffs':[str(utility(actual,i)) for i in range(3)],'loads':loads,
 'W':covered(actual),'two_layer':two_layer(actual),'OPT':opt,'optimal_paths':opt_paths[:20],
 'history_count':sum(6**d for d in range(3)),'comparisons':len(slacks),'strict_comparisons':strict,'minimum_slack':str(min(slacks)),
 'candidate_comparison':comp,'candidate_objective_exact':str(obj),'candidate_objective_float':cand['objective'],
 'candidate_objective_components':{'actual_two_layer':str(Fraction(two_layer(actual),len(clients))),'comparison_fresh':str(Fraction(sum(any(a in B for a in comp) for B in clients),len(clients)))},
 'ratio_OPT_over_W':str(Fraction(opt,covered(actual))),
 'scope':'fixed 9-client candidate; exact all-history audit, no general theorem'
}
assert result['actual_path']==(5,2,3)
assert result['W']==7 and result['two_layer']==7 and result['OPT']==8
assert result['candidate_objective_exact']=='-1/9'
assert result['history_count']==43 and result['comparisons']==258 and result['strict_comparisons']==188 and result['minimum_slack']=='0'
assert audit['actual']==list(actual) and audit['W']==result['W'] and audit['OPT']==result['OPT']
assert audit['Phi']=='7' and audit['truncated_Phi']=='7' and audit['two_layer_occupancy']==7
(ROOT/'two_layer_exact_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
