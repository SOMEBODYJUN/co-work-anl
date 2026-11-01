"""Attack exact universal candidate u_first >= v_(r+1)(0), on a named full strategy cone.
No finite negative result is a proof of the universal candidate.
"""
import itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
# root adjustment explicit below, script can run from repository root
J=json.load(open('evidence/certificates/customer_attraction/individual_security_failure.json'))
acts={tuple(row['history']):row['action'] for row in J['strategy']['actions']}
m,p=3,6
masks=list(range(1,1<<p))
def outcome(h):
 h=tuple(h)
 while len(h)<m:h=h+(acts[h],)
 return h
def row(h,a):
 z=outcome(h)
 return [F(1,sum(1 for t in z if mask>>t&1)) if mask>>a&1 else F(0) for mask in masks]
gamma=[]
for h,a in acts.items():
 actual=row(h,a)
 for b in range(p):
  dev=row(h+(b,),b)
  gamma.append([x-y for x,y in zip(actual,dev)])
first=row((),acts[()])
def counts(n,p,pre=()):
 if p==1:yield pre+(n,);return
 for k in range(n+1):yield from counts(n-k,p-1,pre+(k,))
backgrounds=list(counts(m,p))
def coeff(q,probs):
 return [sum(probs[a] for a in range(p) if mask>>a&1)/F(1+sum(q[a] for a in range(p) if mask>>a&1)) for mask in masks]
# Explicit candidate distributions from named instance (no broad catalogue scan).
queries={'uniform':[F(1,p)]*p,'v3_original':[F(x,82) for x in [10,10,21,10,10,21]],'v4_original':[F(x,118) for x in [25,25,9,25,25,9]]}
reports=[]
for name,probs in queries.items():
 G=[[-float(x) for x in row]+[0.] for row in gamma]
 G += [[-float(x) for x in coeff(q,probs)]+[1.] for q in backgrounds]
 sol=linprog([0.]*len(masks)+[-1.],A_ub=G,b_ub=[0.]*len(G),A_eq=[[float(x) for x in first]+[0.]],b_eq=[1.],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
 data={'query':name,'status':sol.message,'bound_candidate':-sol.fun if sol.success else None}
 if sol.success:
  w=[F(float(x)).limit_denominator(1000000) for x in sol.x[:-1]]
  d=sum(x*y for x,y in zip(w,first)); slack=min(sum(x*y for x,y in zip(w,g)) for g in gamma)
  bound=min(sum(x*y for x,y in zip(w,coeff(q,probs))) for q in backgrounds)
  data.update({'exact_reconstruction_IC':str(slack),'root':str(d),'fixed_query_guarantee':str(bound),'w':{str(mask):str(x) for mask,x in zip(masks,w) if x}})
 reports.append(data)
print(json.dumps(reports,indent=2))
