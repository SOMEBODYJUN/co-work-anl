from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
N,S=6,7
PAIRS=list(combinations(range(S),2))+[(j,j) for j in range(S)]; PAIRS.sort()
def mixed_coeffs():
 A=[];B=[]
 for t in range(N-1):
  z=F(S*(N-t),2)+t; A.append(F(N+t,2*(t+1))/z); B.append(F(1,1)/z)
 A.append(F(1,N+S-1)); B.append(F(N+1,N*(N+S-1)))
 return [min(A[t:]) for t in range(N)],[min(B[t:]) for t in range(N)]
AA,BB=mixed_coeffs()
def build(omit=6, route=None):
 names=[f'M{t}' for t in range(N)]+[f'L{j}' for j in range(S)]+[f'T{j}{k}' for j,k in PAIRS]+[f'D{t},{j}' for t in range(N-1) for j in range(S)]+[f'O{j}-{omit}' for j in range(S) if j!=omit]
 rows=[]; rhs=[]; types=[]
 for I in range(1,1<<S):
  for E in range(1<<(N-1)):
   if route is not None and any(((E>>t)&1) and not ((I>>route[t])&1) for t in range(N-1)): continue
   f=bool(I&1); J=E | (int(f)<<5); q=J.bit_count(); sh=[F((J>>t)&1,q) if q else F(0) for t in range(N)]
   p=(E&15).bit_count(); d=(E>>4)&1
   floor=[F(1,N) if I.bit_count()==S else AA[t] if I.bit_count()==1 else BB[t] for t in range(N)]
   c=[sh[t]-floor[t] for t in range(N)]
   c += [sh[-1]-F((I>>j)&1,p+d+1) for j in range(S)]
   for j,k in PAIRS:
    v=((I>>j)&1)+((I>>k)&1); tax=F(d,(p+1)*(p+2)); c.append(sh[-2]+sh[-1]+tax-(F(v,p+v) if v else 0))
   for t in range(N-1):
    pt=(J&((1<<t)-1)).bit_count(); den=pt+N-t
    for j in range(S): c.append(sh[t]-F((I>>j)&1,den))
   # ordering rows P_j-P_omit >=0, where each singleton mass is a column
   for j in range(S):
    if j!=omit: c.append(F(1) if I==(1<<j) else (F(-1) if I==(1<<omit) else F(0)))
   target=F(int(bool(J)),1)-(F(0) if I==(1<<omit) else F(1,2))
   rows.append([float(v) for v in c]);rhs.append(float(target));types.append((I,E,J,target))
 return names,np.array(rows),np.array(rhs),types
def solve(omit=6,route=None):
 names,A,b,types=build(omit,route)
 r=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
 return r,names,A,b,types
if __name__=='__main__':
 for o in range(S):
  r,n,A,b,t=solve(o);print('omit',o,'cols',len(b),'rows',len(n),'status',r.status,r.message)
  if r.success: print('min',min(b-A@r.x),[(n[i],x) for i,x in enumerate(r.x) if x>1e-8])
  else:
   sep=linprog(b,A_ub=-A.T,b_ub=np.zeros(A.shape[1]),A_eq=np.ones((1,len(b))),b_eq=[1],bounds=(0,None),method='highs'); print('sep',sep.fun if sep.success else sep.message)
