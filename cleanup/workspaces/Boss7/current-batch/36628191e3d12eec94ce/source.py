from fractions import Fraction
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B):
    return Fraction(1,int(B>>a&1)+int(B>>b&1)) if B>>(a,b)[i]&1 else Fraction(0)
def cov(a,b):return np.array([int(bool(B>>a&1 or B>>b&1)) for B in masks],dtype=float)
rows=[[2*(u(a,rho[a],1,B)-u(a,b,1,B)) for B in masks] for a,b in product(range(p),repeat=2)]
rows.extend([2*(u(0,1,0,B)-u(b,rho[b],0,B)) for B in masks] for b in range(p))
C=cov(0,1);O=cov(2,3);R=O*(1-C)
A=[np.array(row,dtype=float) for row in rows];lower=[0]*len(A)
A.append(R-C);lower.append(1)
for a,b in combinations_with_replacement(range(p),2):
    if (a,b)==(2,3):continue
    A.append(O-cov(a,b));lower.append(1)
res=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),bounds=Bounds(np.zeros(len(masks)),np.full(len(masks),np.inf)),constraints=LinearConstraint(A,lower,np.full(len(A),np.inf)),options={'time_limit':40})
print(res.message)
if res.x is not None:
 w={B:int(round(x)) for B,x in zip(masks,res.x) if x>.5};print(w);print('total',sum(w.values()))
