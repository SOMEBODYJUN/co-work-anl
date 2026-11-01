from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from functools import lru_cache
N,S=6,7
PAIRS=list(combinations(range(S),2))+[(j,j) for j in range(S)]; PAIRS.sort()
def mixed_coeffs():
 A=[];B=[]
 for t in range(N-1):
  z=F(S*(N-t),2)+t; A.append(F(N+t,2*(t+1))/z); B.append(F(1,1)/z)
 A.append(F(1,N+S-1)); B.append(F(N+1,N*(N+S-1)))
 return [min(A[t:]) for t in range(N)],[min(B[t:]) for t in range(N)]
AA,BB=mixed_coeffs()
def safe(num,den): return F(0) if num==0 else F(num,den)
@lru_cache(None)
def phi(k,p,ell,t,q):
 best=None
 for b in (0,1):
  for c in (0,1):
   for j in (0,1):
    for v in (0,1):
     for ss in range(k-2):
      for sp in range(k-2):
       z1=p+t+ss+b+c; z2=p+c+sp+j+v
       val=safe(2*t-c,z1)+safe(3*c-v,2*z2)+safe(b,2*(p+c+sp+j+1))+safe(j,4*(ell+1))+safe(5*v,12*(ell+1))+safe(v,12)+safe(q,p+t+ss+b+1)
       if best is None or val<best:best=val
 return -best
def build(omit=6,maxlab=0, useD=True, useQ=True, route=None, singleton_covered=False):
 names=[f'M{t}' for t in range(N)]+[f'L{j}' for j in range(S)]+[f'T{j}{k}' for j,k in PAIRS]
 if useD: names += [f'D{t},{j}' for t in range(N-1) for j in range(S)]
 if useQ: names += [f'Q{i},{j},{q}' for i in range(4) for j in range(S) for q in range(S)]
 names += [f'O{j}-{omit}' for j in range(S) if j!=omit]
 rows=[];rhs=[];types=[]
 for I in range(1,1<<S):
  for E in range(1<<(N-1)):
   if route is not None and any(((E>>t)&1) and not ((I>>route[t])&1) for t in range(N-1)): continue
   if singleton_covered and I.bit_count()==1 and I!=(1<<omit):
    j=I.bit_length()-1
    if j!=0 and E==0: continue
   f=bool(I&1); J=E | (int(f)<<5); ell=J.bit_count(); sh=[F((J>>t)&1,ell) if ell else F(0) for t in range(N)]
   p4=(E&15).bit_count(); d=(E>>4)&1
   floor=[F(1,N) if I.bit_count()==S else AA[t] if I.bit_count()==1 else BB[t] for t in range(N)]
   c=[sh[t]-floor[t] for t in range(N)]
   c += [sh[-1]-F((I>>j)&1,p4+d+1) for j in range(S)]
   for j,k in PAIRS:
    v=((I>>j)&1)+((I>>k)&1); tax=F(d,(p4+1)*(p4+2)); c.append(sh[-2]+sh[-1]+tax-(F(v,p4+v) if v else 0))
   if useD:
    for t0 in range(N-1):
     pt=(J&((1<<t0)-1)).bit_count(); den=pt+N-t0
     for j in range(S): c.append(sh[t0]-F((I>>j)&1,den))
   if useQ:
    for i in range(4):
     p=(J&((1<<i)-1)).bit_count(); k=N-i
     for j in range(S):
      for q in range(S):
       c.append(F(7,2)*sh[i]+F(2,3)*sh[-1]+F(1,12)*((I>>maxlab)&1)+phi(k,p,ell,(I>>j)&1,(I>>q)&1))
   for j in range(S):
    if j!=omit: c.append(F(1) if I==(1<<j) else (F(-1) if I==(1<<omit) else F(0)))
   target=F(int(bool(J)),1)-(F(0) if I==(1<<omit) else F(1,2))
   rows.append([float(v) for v in c]);rhs.append(float(target));types.append((I,E,J,target))
 return names,np.array(rows),np.array(rhs),types
def solve(omit=6,maxlab=0, useD=True,useQ=True,route=None,singleton_covered=False):
 names,A,b,t=build(omit,maxlab,useD,useQ,route,singleton_covered); r=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=b,bounds=(0,None),method='highs'); return r,names,A,b,t
if __name__=='__main__':
 for ml in range(S):
  r,n,A,b,t=solve(6,ml,True,True)
  print('maxlab',ml,'cols',len(b),'rows',len(n),'status',r.status,r.message)
  if r.success: print('min',min(b-A@r.x),'nz',sum(x>1e-8 for x in r.x))
  else:
   sep=linprog(b,A_ub=-A.T,b_ub=[0]*A.shape[1],A_eq=[[1]*len(b)],b_eq=[1],bounds=(0,None),method='highs');print('sep',sep.fun if sep.success else sep.message)
