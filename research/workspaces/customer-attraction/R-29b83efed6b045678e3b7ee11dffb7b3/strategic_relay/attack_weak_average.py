"""One targeted attack on optimal-portfolio weak-average relay; finite diagnostics only."""
import itertools,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
CASES=[
 ('root_tax',4,6,'evidence/certificates/customer_attraction/root_tax_failure.json',lambda d:d['strategy']['actions']),
 ('actual_B',4,6,'research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json',lambda d:d['certificate']['actions']),
 ('individual_security',3,6,'evidence/certificates/customer_attraction/individual_security_failure.json',lambda d:d['strategy']['actions']),
 ('portfolio_matching',2,5,'evidence/certificates/customer_attraction/portfolio_matching_failure.json',lambda d:d['actions']),
]
def rollout(actions,n,h):
 h=tuple(h)
 while len(h)<n:h+=(actions[h],)
 return h
def payoff(n,k,z,a):
 return [F(int(s>>a&1),sum(bool(s>>j&1) for j in z)) if s>>a&1 else F(0) for s in range(1,1<<k)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def run():
 report={'candidate':'For each complete SPE and every optimal m-portfolio T: sum_i,j V_i(T_j) >= m(OPT-W)', 'scope':'fixed complete-policy cones, all customer types, fixed chosen portfolio constrained optimal; finite targeted attack, no general conclusion','cases':[]}
 for name,n,k,path,get in CASES:
  d=json.loads((ROOT/path).read_text()); raw=get(d)
  actions={tuple(e['history']):e['action'] for e in raw}
  z=rollout(actions,n,()); W=[int(any(s>>a&1 for a in z)) for s in range(1,1<<k)]
  rows=[]
  for ell in range(n):
   for h in itertools.product(range(k),repeat=ell):
    base=payoff(n,k,rollout(actions,n,h),actions[h])
    for a in range(k):
     if a!=actions[h]:rows.append([x-y for x,y in zip(base,payoff(n,k,rollout(actions,n,h+(a,)),a))])
  portfolios=list(itertools.combinations_with_replacement(range(k),n))
  cover={T:[int(any(s>>a&1 for a in T)) for s in range(1,1<<k)] for T in portfolios}
  out={'case':name,'path':z,'histories':len(actions),'true_rows':len(rows),'portfolios':len(portfolios),'best_gap':None}
  for T in portfolios:
   O=cover[T]; val=[F(0)]*((1<<k)-1)
   for i in range(n):
    for t in T:
     v=payoff(n,k,rollout(actions,n,z[:i]+(t,)),t)
     val=[x+y for x,y in zip(val,v)]
   objective=[v+n*w-n*o for v,w,o in zip(val,W,O)]
   optrows=[[o-b for o,b in zip(O,cover[B])] for B in portfolios if B!=T]
   A=np.array(rows+optrows,dtype=float)
   lp=linprog(np.array(objective,dtype=float),A_ub=-A,b_ub=np.zeros(len(A)),A_eq=[W],b_eq=[1.],bounds=(0,None),method='highs')
   if not lp.success:continue
   if out['best_gap'] is None or lp.fun<out['best_gap']:
    out.update(best_gap=float(lp.fun),portfolio=T,weights=lp.x.tolist())
   if lp.fun < -1e-7:
    rat=[F(float(x)).limit_denominator(10**7) for x in lp.x]
    slacks=[dot(row,rat) for row in rows+optrows]
    out.update(exact_gap=str(dot(objective,rat)),exact_min_slack=str(min(slacks)),rational_weights=[str(x) for x in rat])
    if min(slacks)>=0 and dot(objective,rat)<0:
     report['cases'].append(out); (HERE/'weak_average_attack.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(out)); return
  report['cases'].append(out); print(name,out['best_gap'],out.get('portfolio'),flush=True)
  (HERE/'weak_average_attack.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':run()
