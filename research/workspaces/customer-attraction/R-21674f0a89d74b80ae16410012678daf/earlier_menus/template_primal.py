from probe_branch_endpoint import rows
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
A,y,states=rows(3,[0])
w=np.array([int(a+b+c>0) for p,a,b,c,hist in states])
res=linprog(y,A_ub=-A.T,b_ub=np.zeros(A.shape[1]),A_eq=[w],b_eq=[1],bounds=(0,None),method='highs')
print(res.success,res.fun)
for x,state in zip(res.x,states):
 if x>1e-8:print(Fraction(float(x)).limit_denominator(100000),state)
