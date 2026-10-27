import numpy as np
from scipy.optimize import linprog
from itertools import product
from fractions import Fraction as F
M=6
names=['S','Z','V','LastA','LastB','LastT']
for i in range(4):
 names+= [f'E{i+1}{t}' for t in ['A','B','T']]
rows=[]; rhs=[]; types=[]
for es in product((0,1),repeat=4):
 for a,b in product((0,1),repeat=2):
  p=sum(es); den=p+a+b
  share=lambda t: F(t,den) if den else F(0)
  for d,ell in product(range(7),repeat=2):
   # joint sum overlap q=d ell? S and Z separately need intersection j=sum_i t_i r_i
   for j in range(max(0,d+ell-6),min(d,ell)+1):
    # S=6u5-sum U(T_i,R_i), Z=6u6-sum U(R_i,A), V=sum_i!=j (U(R_i,T_i)-U(R_j,T_i))
    S=6*share(a)-F(d,p+1)+F(j,(p+1)*(p+2))
    Z=6*share(b)-F(ell,p+a+1)
    V=F(d*ell-6*j,(p+1)*(p+2))
    lastA=share(b)-F(a,p+a+1)
    lastB=F(0) # actual B to B identity
    lastT=6*share(b)-F(d,p+a+1)
    vals=[S,Z,V,lastA,lastB,lastT]
    pref=0
    for i in range(4):
     denom=pref+6-i
     vals += [share(es[i])-F(a,denom),share(es[i])-F(b,denom),6*share(es[i])-F(d,denom)]
     pref+=es[i]
    rows.append([float(v) for v in vals]); rhs.append(2*(den>0)-(d>0)); types.append((es,a,b,d,ell,j))
mat=np.array(rows); rhs=np.array(rhs)
r=linprog(np.zeros(len(names)),A_ub=mat,b_ub=rhs,bounds=[(0,None)]*len(names),method='highs')
print('types',len(types),'vars',len(names),r.message)
if r.success:
 print({n:v for n,v in zip(names,r.x) if v>1e-8})
else:
 # primal min 2W-O for unit W
 w=np.array([int(sum(t[0])+t[1]+t[2]>0) for t in types])
 rr=linprog(rhs,A_ub=-mat.T,b_ub=np.zeros(len(names)),A_eq=w[None,:],b_eq=[1],bounds=(0,None),method='highs')
 print(rr.message,rr.fun)
 if rr.success: print([(types[i],x) for i,x in enumerate(rr.x) if x>1e-8])
