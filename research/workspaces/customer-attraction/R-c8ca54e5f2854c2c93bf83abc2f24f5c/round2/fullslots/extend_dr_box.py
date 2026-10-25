"""Optional extension check for the exact finite-domain DR counterexample.
This is a single feasibility check, not a CAG search.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
base=Path(__file__).resolve().parent
src=json.loads((base/'dr_counterexample_exact.json').read_text())
known={tuple(map(int,s.split(','))):v for s,v in src['potential'].items()}
k=4;cap=4
states=list(product(range(cap+1),repeat=k));ind={q:i for i,q in enumerate(states)}
def plus(q,a):r=list(q);r[a]+=1;return tuple(r)
rows=[];rhs=[]
def put(d,j,v):d[j]=d.get(j,0)+v
for q in states:
 for a in range(k):
  if q[a]<cap:
   rows.append({ind[q]:1,ind[plus(q,a)]:-1});rhs.append(0)
 for a in range(k):
  for b in range(a,k):
   if q[a]+1+(a==b)<=cap and q[b]+1<=cap:
    qa=plus(q,a);qb=plus(q,b);qab=plus(qa,b)
    r={};put(r,ind[q],1);put(r,ind[qab],1);put(r,ind[qa],-1);put(r,ind[qb],-1)
    rows.append(r);rhs.append(0)
A=lil_matrix((len(rows),len(states)))
for n,r in enumerate(rows):
 for j,v in r.items():A[n,j]=v
bounds=[(known[q],known[q]) if q in known else (0,160) for q in states]
res=linprog(np.zeros(len(states)),A_ub=A.tocsr(),b_ub=rhs,bounds=bounds,method='highs')
out={'status':res.status,'message':res.message,'states':len(states),'inequalities':len(rows)}
if res.x is not None:
 from fractions import Fraction as F
 vals={q:F(float(res.x[ind[q]])).limit_denominator(1000000) for q in states}
 margins=[]
 for r,b in zip(rows,rhs):
  d=F(b)-sum((v*vals[states[j]] for j,v in r.items()),F());assert d>=0,d;margins.append(d)
 assert all(vals[q]==v for q,v in known.items())
 out['exact_recheck']='passed';out['minimum_margin']=str(min(margins));out['maximum_denominator']=max(v.denominator for v in vals.values())
 (base/'dr_box_extension_exact.json').write_text(json.dumps({','.join(map(str,q)):str(v) for q,v in vals.items()},indent=2)+'\n')
(base/'dr_box_extension_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
