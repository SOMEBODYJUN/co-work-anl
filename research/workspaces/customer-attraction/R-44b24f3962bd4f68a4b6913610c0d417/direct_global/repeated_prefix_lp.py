from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog

def calc(m):
 rows=[]; obj=[]; cells=[]
 for a,b,d,ell in product(range(2),range(2),range(m+1),range(m+1)):
  p=(m-2)*a; den=(p+1)*(p+2)
  for h in range(max(0,d+ell-m),min(d,ell)+1):
   uA=F(a,m-1+b) if a else F(0)
   uB=F(b,1+(m-1)*a) if b else F(0)
   rows.append([m*uA-F(d,p+1)+F(h,den),m*uB-F(d,p+a+1),m*uB-F(ell,p+a+1),F(d*ell-m*h,den),m*uA-F(ell,p+2),uA-F(b,p+2),m*uB-a])
   obj.append(F(2)*int(a+b>0)-int(d>0)); cells.append((a,b,d,ell,h))
 arr=np.array(rows,dtype=float)
 res=linprog(np.zeros(arr.shape[1]),A_ub=arr,b_ub=np.array(obj,dtype=float),bounds=(0,None),method='highs')
 if res.success:
  print(m,'PROOF',dict(enumerate(res.x.tolist())))
 else:
  res2=linprog(np.array(obj,dtype=float),A_ub=-arr.T,b_ub=np.zeros(arr.shape[1]),A_eq=[[int(a+b>0) for a,b,*_ in cells]],b_eq=[1],bounds=(0,None),method='highs')
  print(m,'gap',res2.fun,'support',[(cells[i],round(x,8)) for i,x in enumerate(res2.x) if x>1e-8] if res2.success else res2.message)
for m in range(2,21):calc(m)
