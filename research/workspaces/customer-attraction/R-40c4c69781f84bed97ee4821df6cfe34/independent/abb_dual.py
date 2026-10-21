"""Valid seven-slack symmetric tail-ABB candidate certificate search."""
from itertools import product
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
OUT=Path(__file__).resolve().parent

def entries(k,l,tax=False):
 m=k+l
 # d=0 has minimum ell=0 unless negative Z, impossible for nonnegative multiplier.
 corners=((0,0),(1,0),(1,m),(m,0),(m,m))
 for a,b,q,r in product((0,1),repeat=4):
  p=(k-1)*a+(l-2)*b
  c=k*a+l*b
  ua=F(a,c) if a else F(0)
  vb=F(b,c) if b else F(0)
  for d,ell in corners:
   D=(p+a+1)*(p+a+2)
   den=p+b+q+r
   ub=F(b,den) if b else F(0)
   ur=F(r,den) if r else F(0)
   vec=[3*ua-F(3*q,p+3),3*ua-F(3*r,p+3),m*vb-F(d,p+a+b+1),m*vb-F(ell,p+a+b+1),m*vb-F(d,p+a+1)+F(d*ell,m*D),ua-ub,m*ur-F(d,p+b+q+1)]
   credit=F(0) if c==0 else (1+F(c,c+1) if tax else F(2))
   yield (a,b,q,r,d,ell),vec,credit-int(d>0)

records=[]
for l in range(2,9):
 for k in range(1,61):
  es=list(entries(k,l)); mat=np.array([[float(v) for v in row] for _,row,_ in es]);rhs=np.array([float(v) for _,_,v in es])
  sol=linprog(np.ones(7)*.001,A_ub=mat,b_ub=rhs,bounds=(0,None),method='highs')
  rec={'k':k,'l':l,'success':sol.success}
  if sol.success:
   fs=[F(float(v)).limit_denominator(10**8) for v in sol.x]
   exact=all(sum(x*y for x,y in zip(vec,fs))<=val for _,vec,val in es)
   rec.update({'multipliers':list(map(str,fs)),'exact_rationalization':exact})
  records.append(rec)
print(json.dumps({'tested':len(records),'feasible':sum(r['success'] for r in records),'infeasible':[(r['k'],r['l']) for r in records if not r['success']][:60],'first':records[:12]},indent=2))
(OUT/'abb_dual_report.json').write_text(json.dumps(records,indent=2))
