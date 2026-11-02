"""Finite attack on total on-path decorrelation at a safety-optimal query.
Fix an existing complete formal strategy and exact matching static saddle p,Q.
Vary all nonnegative incidence weights within their simultaneous linear cone.
"""
import json,pathlib,itertools,math,functools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=pathlib.Path(__file__).resolve().parents[5]; OUT=pathlib.Path(__file__).resolve().parent
SOURCES=['individual_security_failure','local_security_increment','global_decorrelation_failure']

def run():
 reports=[]
 for name in SOURCES:
  obj=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()); cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
  n=obj['players'];k=len(obj['topics']); masks=list(range(1,1<<k)); L=len(masks)
  acts={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
  sec=cert.get('security',cert.get('security_global'));p=list(map(F,sec['primary'])); Q=[(tuple(q['rivals']),F(q['probability'])) for q in sec['dual']]
  @functools.lru_cache(None)
  def end(h):
   return h if len(h)==n else end(h+(acts[h],))
  @functools.lru_cache(None)
  def payoff(a,z):
   return tuple(F(1,sum(bool(m&(1<<t)) for t in z)) if m&(1<<a) else F() for m in masks)
  z0=end(());wc=tuple(F(any(m&(1<<t) for t in z0)) for m in masks)
  Gamma=set()
  for h,ch in acts.items():
   actual=payoff(ch,end(h))
   for a in range(k):
    g=tuple(x-y for x,y in zip(actual,payoff(a,end(h+(a,)))))
    if any(g):Gamma.add(g)
  def beta(B):return tuple(sum(p[a] for a in range(k) if m&(1<<a))/F(1+sum(bool(m&(1<<t)) for t in B)) for m in masks)
  alpha=[tuple(sum((q*F(1,1+sum(bool(m&(1<<t)) for t in B)) for B,q in Q),F()) if m&(1<<a) else F() for m in masks) for a in range(k)]
  backgrounds=list(itertools.combinations_with_replacement(range(k),n-1))
  A=[list(map(float,g))+[0.] for g in Gamma]
  A.extend([list(map(float,beta(B)))+[-1.] for B in backgrounds])
  A.extend([[-float(x) for x in row]+[1.] for row in alpha])
  # C total (independent p action and p query at each actual prefix).
  c=[F() for _ in masks]
  for i in range(n):
   h=z0[:i]
   for a in range(k):
    z=end(h+(a,)); B=z[:i]+z[i+1:]
    for j,b in enumerate(beta(B)):c[j]+=p[a]*b
  objective=[x-y for x,y in zip(c,wc)]
  result=linprog([-float(x) for x in objective]+[0.],A_ub=-np.array(A),b_ub=np.zeros(len(A)),A_eq=[[1.]*L+[0.]],b_eq=[1.],bounds=[(0,None)]*L+[(None,None)],method='highs')
  row={'source':name,'gamma_rows':len(Gamma),'variables':L+1,'status':result.message,'max_total_C_minus_W':None if not result.success else -result.fun}
  reports.append(row); print(json.dumps(row),flush=True)
  (OUT/'optimal_query_budget_diagnostic.json').write_text(json.dumps(reports,indent=2)+'\n')
  if result.success and -result.fun>1e-8:
   rat=[F(float(v)).limit_denominator(10000000) for v in result.x]
   w=rat[:-1];v=rat[-1]
   exact_rows=[sum((x*y for x,y in zip(g,w)),F()) for g in Gamma]
   primal=[sum((x*y for x,y in zip(beta(B),w)),F())-v for B in backgrounds]
   dual=[v-sum((x*y for x,y in zip(a,w)),F()) for a in alpha]
   row['rational_min_constraints']=str(min(exact_rows+primal+dual))
   if min(exact_rows+primal+dual)>=0:
    row['exact_gap']=str(sum((x*y for x,y in zip(objective,w)),F()))
    row['weights']={str(m):str(z) for m,z in zip(masks,w) if z}
    row['v']=str(v)
    (OUT/'optimal_query_budget_witness.json').write_text(json.dumps(row,indent=2)+'\n')
    print('EXACT POSITIVE',json.dumps(row),flush=True)
 (OUT/'optimal_query_budget_diagnostic.json').write_text(json.dumps(reports,indent=2)+'\n')
if __name__=='__main__':run()
