from fractions import Fraction
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B):
    return Fraction(1,int(B>>a&1)+int(B>>b&1)) if B>>(a,b)[i]&1 else Fraction(0)
def cov(a,b):return np.array([int(bool(B>>a&1 or B>>b&1)) for B in masks],dtype=float)
A=[];labels=[]
for a,b in product(range(p),repeat=2): A.append([float(2*(u(a,rho[a],1,B)-u(a,b,1,B))) for B in masks]);labels.append(('response',a,b))
for b in range(p):A.append([float(2*(u(0,1,0,B)-u(b,rho[b],0,B))) for B in masks]);labels.append(('root',b))
C=cov(0,1);O=cov(2,3);R=O*(1-C); A.append(list(R-C));labels.append(('cover-gap',))
for a,b in combinations_with_replacement(range(p),2):
 if (a,b)==(2,3):continue
 A.append(list(O-cov(a,b)));labels.append(('omit',a,b))
A=np.array(A);b=np.array([0]*42+[1]+[1]*20); # wait rows: 36+6=42 then 1+14=15 => total57
print(A.shape,b.shape)
res=linprog(np.ones(len(masks)),A_ub=-A,b_ub=-b,bounds=(0,None),method='highs')
print(res.success,res.fun)
# inequality marginals on -A x <= -b; dual marginals <=0; y=-marginals >=0
ys=-res.ineqlin.marginals
print('dual objective',ys@b,'max constraint',ys@A)
for i,y in enumerate(ys):
 if y>1e-8: print(i,labels[i],y,Fraction(float(y)).limit_denominator(1000000))
print('min dual slack',np.min(1-ys@A),'max dual slack',np.max(1-ys@A))
