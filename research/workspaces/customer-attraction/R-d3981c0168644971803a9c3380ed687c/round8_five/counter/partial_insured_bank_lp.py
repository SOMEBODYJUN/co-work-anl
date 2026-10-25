"""One targeted repair of the bank-deviation failure: insure half the bank mass.
Types contain one optimal T, any actual membership, and zero or one insurer.
This is a necessary-floor LP, not an asserted SPE.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from math import lcm
import numpy as np,json
from scipy.optimize import linprog
P=20;M=5;PATH=(0,1,2,3,4);edges=list(combinations(range(5),2))
types=[tuple(a for a in range(5) if S>>a&1)+(5+j,)+(() if e<0 else (10+e,)) for S in range(1,32) for j in range(5) for e in range(-1,10)]
types +=[(5+j,)+tuple(10+k for k,e in enumerate(edges) if j in e) for j in range(5)]
q=[PATH.count(a) for a in range(P)]
def row(q,a):return [F(1,sum(q[b] for b in typ)) if a in typ else F(0) for typ in types]
rows=[];labels=[]
for i,a in enumerate(PATH):
 old=[PATH[:i].count(b) for b in range(P)];actual=row(q,a);r=M-i
 for t in range(P):
  dev=old[:];dev[t]+=r;rows.append([x-y for x,y in zip(actual,row(dev,t))]);labels.append((i+1,t))
W=[F(any(a<5 for a in typ)) for typ in types];L=[1-v for v in W];insured=[F(bool(w) and any(a>=10 for a in typ)) for typ,w in zip(types,W)]
res=linprog(-np.array(L,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=np.array([W,insured],float),b_eq=[1,.5],bounds=(0,None),method='highs');assert res.success,res.message
# Materialize a bounded integer proposal. Rounding does not certify LP feasibility.
scale=10**6
x=[F(round(float(t)*scale)) for t in res.x]
dot=lambda a,b:sum((v*w for v,w in zip(a,b)),F(0))
primal=all(t>=0 for t in x) and dot(W,x)==scale and dot(insured,x)==F(scale,2) and all(dot(r,x)>=0 for r in rows)
report={'scope':'one designed partial bank insurance repair; rounded integer proposal from necessary security LP; no SPE claim','target_path':PATH,'W':str(dot(W,x)),'L':str(dot(L,x)),'F_insured':str(dot(insured,x)),'necessary_rows_all_pass':primal,'LP_ratio_float':float(1-res.fun),'minimum_rounded_security_slack':str(min(dot(r,x) for r in rows)),'point':[(types[j],str(v)) for j,v in enumerate(x) if v]}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='point'},indent=2))
