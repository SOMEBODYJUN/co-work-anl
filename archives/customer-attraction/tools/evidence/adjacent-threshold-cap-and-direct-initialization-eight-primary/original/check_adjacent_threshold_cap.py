"""Targeted diagnostic of C: adjacent realized ascent a<b implies mu(b+B)<=b.
Uses only named preexisting instances; no search over new instances.
All ordered paths come from the full set-valued SPE recurrence.
"""
from fractions import Fraction
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
ROOT=Path(__file__).resolve().parents[6]
NAMES=['root_tax_failure','aggregate_theta_failure','portfolio_matching_failure','worst_pne_welfare_failure','coverage_opportunity_failure']
records=[]
for name in NAMES:
 p=ROOT/'examples/customer_attraction'/f'{name}.json'
 if not p.exists():continue
 I=Instance.from_dict(json.loads(p.read_text())); solver=ExactSPESolver(I)
 checked=0;violations=[]
 for q in solver.outcomes():
  u=I.topic_payoffs(q)
  for path in solver.ordered_outcomes(q):
   counts=[0]*I.topic_count
   for i in range(I.players-1):
    A,B=path[i:i+2];alpha,beta=u[A],u[B]
    if alpha<beta:
     mu_counts=counts.copy();mu_counts[B]+=1
     mu=solver.threshold(mu_counts);checked+=1
     if mu>beta:
      violations.append({'path':path,'q':q,'i':i,'alpha':str(alpha),'beta':str(beta),'mu_B':str(mu),'prefix_counts':counts.copy()})
      break
    counts[A]+=1
   if violations:break
  if violations:break
 records.append({'name':name,'ascents_checked':checked,'violations':violations,'scope':'named fixed input only; not a general theorem'})
 print(json.dumps(records[-1]),flush=True)
 if violations:break
Path(__file__).with_name('adjacent_threshold_cap_diagnostic.json').write_text(json.dumps(records,indent=2)+'\n')
