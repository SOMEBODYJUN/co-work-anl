"""Optimize a small interpretable coefficient family, exact verify afterwards."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

def frac(a,b):return F(a,b) if a else F(0)

def features(p,t,q,b,c,j,v):
 z1=p+t+b+c;z2=p+c+j+v
 return [frac(t,z1),frac(c,z2),F(b),frac(q,p+t+b+1)-frac(c,z1),frac(j,p+t+b+1)-frac(c,z1),frac(v,p+t+b+1)-frac(c,z1),frac(b,p+c+j+1)-frac(v,z2),frac(v,p+c+2)-frac(j,z2),frac(j+v,p+t+1)-frac(j*v+b,(p+t+1)*(p+t+2))-frac(b+c,z1)]

# theta 9 coordinates. Target=(1-beta)t/(p+3)+beta*q/(p+1+2t)+alpha*t
# beta=theta[3]; alpha=theta[2]; source weights sum 1.
rows=[];rhs=[];states=[]
for p in range(4):
 for t,q,b,c,j,v in product((0,1),repeat=6):
  co=features(p,t,q,b,c,j,v)
  co[3]-=frac(q,p+1+2*t)-frac(t,p+3)
  co[2]-=t
  rows.append(co);rhs.append(frac(t,p+3));states.append((p,t,q,b,c,j,v))
res=[]
for alpha in [F(0),F(1,144),F(1,100),F(1,96),F(1,84),F(1,80),F(1,72),F(1,64),F(1,60),F(1,48),None]:
 eq=[[1,1,0,0,0,0,0,0,0]];br=[1]
 if alpha is not None:eq.append([0,0,1,0,0,0,0,0,0]);br.append(float(alpha))
 obj=[0,0,0,-1,0,0,0,0,0]
 sol=linprog(obj,A_ub=-np.array(rows,dtype=float),b_ub=-np.array(rhs,dtype=float),A_eq=eq,b_eq=br,bounds=(0,None),method='highs')
 if not sol.success:res.append({'alpha':str(alpha),'error':sol.message});continue
 th=[F(float(v)).limit_denominator(10**7) for v in sol.x]
 sl=[sum(v*w for v,w in zip(row,th))-r for row,r in zip(rows,rhs)]
 good=min(sl)>=0 and th[0]+th[1]==1 and (alpha is None or th[2]==alpha)
 rec={'alpha':str(alpha),'theta':list(map(str,th)),'beta':str(th[3]),'verified':good,'minimum_slack':str(min(sl)),'zero_slacks':sum(v==0 for v in sl)}
 print(rec,flush=True);res.append(rec)
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'p=0..3 exact all 256 type/hidden combinations; valid only for theta passing exact verification','results':res},indent=2)+'\n')
