"""Discover and certify background analogues of the arbitrary-topic root row.

Only the stated finite (n,k) coefficient certificates are certified here.
"""
from fractions import Fraction as F
from itertools import product
from scipy.optimize import linprog
import json
from pathlib import Path
records=[]
for n in range(2,11):
 for k in range(2,n+1):
  types=list(product(range(2),range(2),range(2),range(k-1),range(n-k+1)))
  def div(x,d):return F(x,d) if x else F(0)
  rows=[]
  for a,b,d,h,p in types:
   mu=F(1,p+k);uA=div(a,p+h+a+b);uB=div(b,p+h+a+b);uD=div(d,p+h+a+d)
   rows.append((uA-mu*a,mu*(b-a),mu*(h-(k-2)*a),uD-uB,mu*(a-d),mu*d*(1-a)))
  aub=[[float(row[i]) for row in rows]+[-1 if i<2 else -(k-2) if i==2 else 0] for i in range(4)]
  eq=[[row[i] for row in rows]+[0] for i in (4,5)]
  res=linprog([0]*len(types)+[1],A_ub=aub,b_ub=[0]*4,A_eq=eq,b_eq=[0,1],bounds=(0,None),method='highs')
  mu=[F(-x).limit_denominator(10**8) for x in res.ineqlin.marginals]
  nu=[F(x).limit_denominator(10**8) for x in res.eqlin.marginals]
  # Weighted constraint sum is bounded above by delta; every cell must
  # dominate nu[0]*(muA-muD)+nu[1]*mu(D\A).
  residuals=[sum(x*v for x,v in zip(mu,row[:4]))-nu[0]*row[4]-nu[1]*row[5] for row in rows]
  certified=all(x>=0 for x in mu) and mu[0]+mu[1]+(k-2)*mu[2]==1 and min(residuals)>=0
  rec={'n':n,'k':k,'floating_delta_per_weighted_difference':res.fun,'delta_per_weighted_difference':str(nu[1]),'coefficient_A_minus_R':str(nu[0]),'inequality_multipliers':list(map(str,mu)),'equality_multipliers':list(map(str,nu)),'exact_dual_verified':certified,'minimum_exact_coefficient_residual':str(min(residuals)),'cell_count':len(types)}
  records.append(rec)
  if n==5:print(json.dumps(rec),flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'finite background coefficient certificates; no general SPE bound asserted beyond each displayed necessary row','records':records},indent=2)+'\n')
