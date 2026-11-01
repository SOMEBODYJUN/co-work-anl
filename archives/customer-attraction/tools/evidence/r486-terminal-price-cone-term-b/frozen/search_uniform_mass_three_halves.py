from fractions import Fraction as F
from itertools import product
from scipy.optimize import linprog
from pathlib import Path
import numpy as np,json
HERE=Path(__file__).resolve().parent
tau=F(3,2)

def raw(bits,d,l,p):
 a,b,c,q,r=bits;s=a+b+c
 al,be,ga=[F(v,p+s) if v else F() for v in (a,b,c)]
 def u(v,*o):return F(v,p+sum(o)+v) if v else F()
 D=(p+1+a)*(p+2+a)
 row=[3*al-F(3*q,p+3),3*al-F(3*r,p+3),tau*ga-F(d,p+1+a+b),tau*ga-F(l,p+1+a+b),tau*be-F(d,p+1+a)+F(d*l,tau*D),al-u(c,q,r),tau*u(r,c,q)-F(d,p+1+c+q)]
 target=tau*al+int(p+s>0)-min(1,d)
 return row+[al],target
A=[];b=[];labels=[]
for bits in product(range(2),repeat=5):
 for d,l in [(0,0),(1,0),(1,tau),(tau,0),(tau,tau)]:
  row,target=raw(bits,d,l,0);A.append(row);b.append(target);labels.append((bits,d,l,0))
  vals=[]
  for p in range(1,5):
   row,target=raw(bits,d,l,p);L=(p+1)*(p+2)*(p+3)
   vals.append([v*L for v in row]+[target*L])
  for k in range(4):
   A.append(vals[0][:-1]);b.append(vals[0][-1]);labels.append((bits,d,l,k+1))
   vals=[[v-u for u,v in zip(x,y)] for x,y in zip(vals,vals[1:])]
lp=linprog(np.array([0.]*7+[-1.]),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),bounds=[(0,None)]*7+[(0,2)],method='highs')
print(lp.success,lp.message)
if lp.success:
 lam=[F(v).limit_denominator(1000000) for v in lp.x]
 slack=[y-sum((x*z for x,z in zip(row,lam)),F()) for row,y in zip(A,b)]
 print(lam,'min',min(slack))
 (HERE/'uniform_mass_three_halves_certificate.json').write_text(json.dumps({'lambda':list(map(str,lam)),'min_exact_slack':str(min(slack)),'rows':len(A),'exact_nonnegative':min(slack)>=0},indent=2))
