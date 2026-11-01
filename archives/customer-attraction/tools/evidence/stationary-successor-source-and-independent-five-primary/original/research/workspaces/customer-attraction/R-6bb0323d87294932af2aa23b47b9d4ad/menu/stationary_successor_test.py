"""Test named stationary-successor-source restriction, not Mfull or half."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate

def solve(name,ins,cert):
 ck=verify_certificate(ins,cert);ck.assert_valid();m,k=ins.players,ins.topic_count
 def terminal(h):
  while len(h)<m:h=h+(cert.actions[h],)
  return h
 z=terminal(());u=ins.topic_payoffs(ins.counts(z))[z[0]];w=ins.welfare(ins.counts(z))
 cols=[terminal((a,)) for a in range(k)]
 K=[[sum((F(c.multiplicity,1+sum(a in c.topics for a in col)) for c in ins.customers if t in c.topics),F()) for col in cols] for t in range(k)]
 P=[[F(col[1:].count(t),m-1) for col in cols] for t in range(k)]
 eq=[[float(P[t][a]-F(t==a)) for a in range(k)]+[0.] for t in range(k)]+[[1.]*k+[0.]]
 row=[[float(x) for x in r]+[-1.] for r in K]
 out=linprog([0.]*k+[1.],A_ub=row,b_ub=[0.]*k,A_eq=eq,b_eq=[0.]*k+[1.],bounds=[(0,None)]*(k+1),method='highs')
 if not out.success:return dict(name=name,error=out.message)
 q=[F(float(v)).limit_denominator(10**7) for v in out.x[:k]];q=[v/sum(q) for v in q]
 assert all(sum(P[t][a]*q[a] for a in range(k))==q[t] for t in range(k))
 query=[sum(K[t][a]*q[a] for a in range(k)) for t in range(k)]
 # Store rational primal only; a positive result needs exact dual before conclusion.
 return dict(name=name,m=m,k=k,W=w,u=str(u),cap=str(max(query)),gap=str(max(query)-u),Q=list(map(str,q)),queries=list(map(str,query)),terminal=z,full_histories=ck.checked_histories,K=[[str(v) for v in row] for row in K],P=[[str(v) for v in row] for row in P])
res=[]
for fn in ['individual_security_failure.json','aggregate_theta_failure.json','worst_pne_welfare_failure.json','prefix_balance_failure.json','dynamic_iid_local.json']:
 ins=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/fn).read_text()))
 raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/fn).read_text());raw=raw.get('strategy',raw.get('certificate',raw))
 res.append(solve(fn,ins,StrategyCertificate.from_dict(raw)))
f=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json'
d=json.loads(f.read_text());res.append(solve(f.name,Instance.from_dict(d['instance']),StrategyCertificate.from_dict(d['certificate'])))
out=ROOT/'research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/menu/stationary_successor_test.json'
out.write_text(json.dumps(res,indent=2))
for r in res:print({k:r[k] for k in ('name','u','cap','gap','Q') if k in r})
