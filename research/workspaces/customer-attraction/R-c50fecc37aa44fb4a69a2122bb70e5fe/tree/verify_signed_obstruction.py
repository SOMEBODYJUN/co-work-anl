"""Definition-only exact audit. No numpy, scipy or project solver imports.

The input is a common SIGNED-customer payoff game. This is explicitly not a
Q-CAG-HALF counterexample. In particular a negative observable local atom below
proves no nonnegative customer realization can preserve these payoff data.
"""
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent

def comps(n,p):
 if p==1:yield(n,);return
 for i in range(n+1):
  for r in comps(n-i,p-1):yield (i,)+r

def run():
 raw=json.loads((BASE/'signed_policy_n4_p6_b_best.json').read_text())
 n,p=raw['n'],raw['p'];common_denominator=85320
 weights={r['mask']:Q(round(Q(r['weight'])*common_denominator),common_denominator) for r in raw['signed_customer_weights']}
 actions={tuple(r['history']):r['action'] for r in raw['strategy_actions']}
 assert len(actions)==sum(p**d for d in range(n))
 types=range(1,1<<p)
 den={q:{B:sum(q[b] for b in range(p) if B>>b&1) for B in types} for q in comps(n,p)}
 def cov(A):return sum((w for B,w in weights.items() if any(B>>a&1 for a in A)),Q(0))
 util={(q,a):sum((w/den[q][B] for B,w in weights.items() if B>>a&1),Q(0)) for q in den for a in range(p) if q[a]}
 assert min(util.values())>=0
 terminals={}
 for d in reversed(range(n+1)):
  for h in product(range(p),repeat=d):
   terminals[h]=tuple(h.count(a) for a in range(p)) if d==n else terminals[h+(actions[h],)]
 comparisons=0;minimum_gap=None
 for h,a in actions.items():
  for b in range(p):
   gap=util[terminals[h],a]-util[terminals[h+(b,)],b]
   assert gap>=0,('incentive',h,a,b,gap)
   comparisons+=1
   if b!=a:minimum_gap=gap if minimum_gap is None else min(minimum_gap,gap)
 dilution=0;dilution_gap=None
 for (q,a),uq in util.items():
  for (r,b),ur in util.items():
   if a!=b or q==r:continue
   kap=max(Q(den[r][B],den[q][B]) for B in types if B>>a&1)
   gap=kap*ur-uq
   assert gap>=0,('dilution',q,r,a,gap)
   dilution+=1;dilution_gap=gap if dilution_gap is None else min(dilution_gap,gap)
 for q in den:
  assert sum((q[a]*util[q,a] for a in range(p) if q[a]),Q(0))==cov([a for a in range(p) if q[a]])
 actual=tuple(a for a in range(p) if terminals[()][a]);target=tuple(raw['target'])
 W=cov(actual);T=cov(target)
 assert W==1 and T==Q(160,79) and T>2*W
 # Find an observable atom in a <=m-label projection. A nonempty pattern X
 # has mass sum_{D subset X}(-1)^|D| C_{(A\X) union D}, with a sign below.
 local_bad=[]
 for k in range(1,min(n,p)+1):
  for A in combinations(range(p),k):
   maskA=sum(1<<a for a in A)
   for j in range(1,k+1):
    for X in combinations(A,j):
     maskX=sum(1<<a for a in X)
     atom=sum((w for B,w in weights.items() if B&maskA==maskX),Q(0))
     if atom<0:local_bad.append((atom,A,X))
 local_bad.sort()
 report=dict(scope='exact common signed customer obstruction only; not true CAG SPE',n=n,p=p,decision_histories=len(actions),incentive_comparisons=comparisons,dilution_comparisons=dilution,terminal_payoff_vertices=len(util),minimum_terminal_payoff=str(min(util.values())),minimum_incentive_gap=str(minimum_gap),minimum_dilution_gap=str(dilution_gap),actual_counts=terminals[()],actual_W=str(W),target=target,target_coverage=str(T),negative_local_atoms=len(local_bad))
 if local_bad:report['smallest_local_atom']=dict(value=str(local_bad[0][0]),support=local_bad[0][1],pattern=local_bad[0][2])
 # Return the exact signed representation, never silently replace with units.
 payload=dict(scope=report['scope'],n=n,p=p,target=target,actual_counts=terminals[()],target_coverage=str(T),weights=[dict(mask=B,weight=str(w)) for B,w in sorted(weights.items())],strategy_actions=raw['strategy_actions'])
 (BASE/'signed_obstruction_exact.json').write_text(json.dumps(payload,indent=2)+'\n')
 (BASE/'signed_obstruction_report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':run()
