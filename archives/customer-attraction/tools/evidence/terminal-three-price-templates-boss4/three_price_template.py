from itertools import product
from scipy.optimize import linprog
import numpy as np
from fractions import Fraction as F
import json
from pathlib import Path

def rows(tau,pbg=0):
 out=[];rhs=[];states=[]
 for a,b,c,q,r in product(range(2),repeat=5):
  den=pbg+a+b+c
  al,be,ga=(F(v,den) if v else F() for v in (a,b,c))
  def u(v,*o):return F(v,pbg+sum(o)+v) if v else F()
  for d,l in [(0,0),(1,0),(1,tau),(tau,0),(tau,tau)]:
   D=(pbg+1+a)*(pbg+2+a)
   # kQ,kR,P,Z,S,F,J (V coefficient S/tau)
   row=[3*al-F(3*q,pbg+3),3*al-F(3*r,pbg+3),tau*ga-F(d,pbg+1+a+b),tau*ga-F(l,pbg+1+a+b),tau*be-F(d,pbg+1+a)+F(d*l,tau*D),al-u(c,q,r),tau*u(r,c,q)-F(d,pbg+1+c+q)]
   target=tau*al+be+ga-min(F(1),d)/(pbg+1)
   out.append(row);rhs.append(target);states.append((a,b,c,q,r,d,l))
 return out,rhs,states
res=[]
for tau in [F(1),F(3,2),F(2),F(3),F(4),F(6),F(10),F(30),F(100)]:
 A,b,states=rows(tau)
 lp=linprog(np.ones(7),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),bounds=(0,None),method='highs')
 rr={'tau':str(tau),'success':lp.success,'message':lp.message}
 if lp.success:rr['lambda']=[str(F(v).limit_denominator(1000000)) for v in lp.x]
 res.append(rr)
print(json.dumps(res,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2))
