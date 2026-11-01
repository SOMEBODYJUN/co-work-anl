from fractions import Fraction
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B): return Fraction(1,int(B>>a&1)+int(B>>b&1)) if B>>(a,b)[i]&1 else Fraction(0)
def cov(a,b):return np.array([int(bool(B>>a&1 or B>>b&1)) for B in masks],dtype=float)
rows=[[u(a,rho[a],1,B)-u(a,b,1,B) for B in masks] for a,b in product(range(p),repeat=2)]
rows.extend([u(0,1,0,B)-u(b,rho[b],0,B) for B in masks] for b in range(p))
C=cov(0,1);O=cov(2,3);R=O*(1-C)
A=[list(-np.array(row,dtype=float))+[0] for row in rows];b=[0]*len(A)
A.append(list(-(R-C))+[0]);b.append(-.01)
labels=['rho_%d_%d'%(a,b) for a,b in product(range(p),repeat=2)]+['root_%d'%b for b in range(p)]+['residual']
for a,c in combinations_with_replacement(range(p),2):
 if (a,c)==(2,3):continue
 A.append(list(cov(a,c)-O)+[1]);b.append(0);labels.append('pair_%d_%d'%(a,c))
res=linprog([0]*len(masks)+[-1],A_ub=A,b_ub=b,A_eq=[list(C)+[0]],b_eq=[1],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
print(res.fun,res.x[-1])
print('eqlin',res.eqlin.marginals)
for l,x,s,m in zip(labels,res.ineqlin.residual,res.ineqlin.marginals,res.ineqlin.marginals):
 if abs(s)>1e-8 or abs(x)<1e-8: print(l,'slack',x,'marg',s,'rat',Fraction(float(s)).limit_denominator(10000))
print('all nonzero marg')
for i,(l,m) in enumerate(zip(labels,res.ineqlin.marginals)):
 if abs(m)>1e-8: print(i,l,m,Fraction(float(m)).limit_denominator(10000), 'slack',res.ineqlin.residual[i])
