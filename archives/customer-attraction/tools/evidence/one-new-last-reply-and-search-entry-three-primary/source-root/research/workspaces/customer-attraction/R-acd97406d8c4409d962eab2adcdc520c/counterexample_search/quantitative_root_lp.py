"""A uniform relaxation of one root deviation plus its true last response.

Floating solutions discover candidate general coefficients only.
"""
from fractions import Fraction as F
from itertools import product
from scipy.optimize import linprog
import json
from pathlib import Path
records=[]
for m in range(2,21):
 types=list(product(range(2),range(2),range(2),range(m-1)))
 def div(x,d):return F(x,d) if x else F(0)
 rows=[]
 for a,b,d,h in types:
  uA=div(a,h+a+b);uB=div(b,h+a+b);uD=div(d,h+a+d)
  rows.append((m*uA-a,b-a,h-(m-2)*a,uD-uB,a-d,d*(1-a)))
 aub=[[float(row[i]) for row in rows]+[-1 if i<2 else -(m-2) if i==2 else 0] for i in range(4)]
 eq=[[row[i] for row in rows]+[0] for i in (4,5)]
 res=linprog([0]*len(types)+[1],A_ub=aub,b_ub=[0]*4,A_eq=eq,b_eq=[0,1],bounds=(0,None),method='highs')
 rec={'m':m,'status':res.message,'delta_per_directed_difference':res.fun,'candidate_fraction':str(F(res.fun).limit_denominator(10**7)),'dual_inequality_multipliers':[str(F(-x).limit_denominator(10**7)) for x in res.ineqlin.marginals],'dual_equality_multipliers':[str(F(x).limit_denominator(10**7)) for x in res.eqlin.marginals],'nonzero_types':[[list(ty),str(F(x).limit_denominator(10**7))] for ty,x in zip(types,res.x) if x>1e-8]}
 records.append(rec);print(json.dumps(rec),flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'floating relaxation discovery; no theorem certified in this file','records':records},indent=2)+'\n')
