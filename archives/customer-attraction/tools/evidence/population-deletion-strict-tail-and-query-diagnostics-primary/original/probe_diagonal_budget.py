"""One bounded diagnostic of existing complete certificates against DB.
Discovery LP only; every proposed positive witness is rechecked as Fraction.
No model or SPE solver imports.
"""
import json,pathlib,itertools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=pathlib.Path(__file__).resolve().parents[5]
OUT=pathlib.Path(__file__).resolve().parent

def scan():
 report=[]
 for ip in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
  cp=ROOT/'evidence/certificates/customer_attraction'/ip.name
  if not cp.exists(): continue
  obj=json.loads(ip.read_text()); cert=json.loads(cp.read_text())
  if not isinstance(cert,dict):continue
  strategy=cert.get('strategy',{})
  if not isinstance(strategy,dict) or not strategy.get('actions'):continue
  acts={tuple(r['history']):r['action'] for r in strategy['actions']}
  n=obj['players'];k=len(obj['topics'])
  customers=[frozenset(c['topics']) for c in obj['customers'] for _ in range(c.get('multiplicity',1))]
  def end(h):
   while len(h)<n:h=h+(acts[h],)
   return h
  def payoff(a,z,extra=0):
   return sum((F(1,extra+sum(t in C for t in z)) for C in customers if a in C),F())
  complete=sum(k**i for i in range(n))==len(acts)
  if not complete:continue
  checks=0
  for h in acts:
   if payoff(acts[h],end(h))<max(payoff(a,end(h+(a,))) for a in range(k)):
    raise AssertionError((ip.name,h))
   checks+=k
  # Test root, and actual-path proper prefixes (all depths, no new finite-depth relaxation).
  z0=end(())
  for depth in range(n):
   h=z0[:depth]
   Z=[end(h+(a,)) for a in range(k)]
   d=[payoff(a,Z[a]) for a in range(k)]
   K=[[payoff(t,Z[a],1) for a in range(k)] for t in range(k)]
   matrix=np.array([[float(K[t][a]-d[t]) for t in range(k)]+[-1.] for a in range(k)])
   result=linprog([0.]*k+[-1.],A_ub=-matrix,b_ub=np.zeros(k),A_eq=[[1.]*k+[0.]],b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method='highs')
   p=[F(float(v)).limit_denominator(10000000) for v in result.x[:k]]
   p=[v/sum(p) for v in p]
   D=sum((p[t]*d[t] for t in range(k)),F())
   columns=[sum((p[t]*K[t][a] for t in range(k)),F()) for a in range(k)]
   row={'instance':ip.name,'prefix':list(h),'root_utility':str(payoff(acts[h],Z[acts[h]])),'gap_lp':-result.fun,'p':[str(v) for v in p],'D':str(D),'min_column':str(min(columns)),'exact_gap':str(min(columns)-D),'full_spe_comparisons':checks}
   report.append(row)
   if min(columns)>D:
    print('POSITIVE',json.dumps(row))
 print(json.dumps({'nodes_checked':len(report),'max_gap':max(r['gap_lp'] for r in report),'positive':sum(F(r['exact_gap'])>0 for r in report)},indent=2))
 (OUT/'diagonal_budget_existing_diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':scan()
