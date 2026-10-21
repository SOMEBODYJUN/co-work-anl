"""Exploratory necessary-condition LP. Any bad point is not an SPE."""
from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog

def run(m):
 rows=[];target=[];cells=[]
 for bits in product(range(2),repeat=m):
  pre=bits[:-2];a,b=bits[-2:];p=sum(pre);n=p+a+b
  alpha=F(a,n) if a else F(0);beta=F(b,n) if b else F(0)
  Rs=[];Ls=[];before=0
  for j,e in enumerate(pre):
   Rs.append((F(e,n) if e else F(0))-F(a,before+m-j))
   Ls.append(beta-F(e,p+a+1))
   before+=e
  for d,l in ((0,0),(0,m),(1,0),(1,m),(m,0),(m,m)):
   G=m*alpha+beta/2-F(d,p+1)-F(l,2*m*(p+a+1))+F(d*l,m*(p+1)*(p+2))
   rows.append(Rs+Ls);target.append(2*int(n>0)-int(d>0)-G);cells.append((bits,d,l))
 res=linprog(np.zeros(2*(m-2)),A_ub=np.array(rows,float),b_ub=np.array(target,float),bounds=(0,None),method='highs')
 if res.success:
  print(m,'HALF',res.x)
 else:
  arr=np.array(rows,float)
  dual=linprog(np.array(target,float),A_ub=-arr.T,b_ub=np.zeros(arr.shape[1]),A_eq=[[1]*len(cells)],b_eq=[1],bounds=(0,None),method='highs')
  print(m,'NO',dual.fun,[(cells[i],x) for i,x in enumerate(dual.x) if x>1e-8] if dual.success else dual.message)
for m in range(3,11):run(m)
