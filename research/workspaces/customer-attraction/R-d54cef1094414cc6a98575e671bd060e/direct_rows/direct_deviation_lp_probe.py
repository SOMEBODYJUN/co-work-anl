from fractions import Fraction as F
from itertools import combinations
import sys, numpy as np
from scipy.optimize import linprog
sys.path.append('/workspace/scratch/f77104eb3bb8/co-work-anl/research/workspaces/customer-attraction/R-70d2119f50a642dc94b386eb142f1f2d/six_2')
import seven_maxima_lp as s
N,S=6,7; aa,bb=s.mixed_coeffs(); pairs=list(combinations(range(S),2))+[(j,j) for j in range(S)]; pairs.sort()
def build(route=None):
 rows=[]; names=[]; cols=[]; rhs=[]
 names += [f'M{t}' for t in range(N)]
 names += [f'L{j}' for j in range(S)]
 names += [f'T{j}{k}' for j,k in pairs]
 names += [f'D{t},{j}' for t in range(N-1) for j in range(S)]
 for I in range(1,1<<S):
  f=bool(I&1); m=I.bit_count()
  for J0 in range(1<<(N-1)):
   if route is not None and any(((J0>>t)&1) and not ((I>>route[t])&1) for t in range(N-1)): continue
   J=J0 | (int(f)<<(N-1)); q=J.bit_count(); cover=int(q>0)
   p=(J0&((1<<(N-2))-1)).bit_count(); d=(J0>>(N-2))&1
   sh=[F((J>>t)&1,q) if q else F(0) for t in range(N)]
   floor=[F(1,N) if m==S else aa[t] if m==1 else bb[t] for t in range(N)]
   c=[sh[t]-floor[t] for t in range(N)]
   c += [sh[-1]-F((I>>j)&1,p+d+1) for j in range(S)]
   for j,k in pairs:
    z=((I>>j)&1)+((I>>k)&1); tax=F(d,(p+1)*(p+2))
    c.append(sh[-2]+sh[-1]+tax-(F(z,p+z) if z else F(0)))
   for t in range(N-1):
    pt=(J&((1<<t)-1)).bit_count(); den=pt+N-t
    for j in range(S): c.append(sh[t]-F((I>>j)&1,den))
   cols.append([float(x) for x in c]); rhs.append(cover-F(1,2))
 A=np.array(cols); b=np.array(rhs)
 return names,A,b
for route in [None,(0,0,0,0,1,0)]:
 names,A,b=build(route); res=linprog(np.zeros(len(names)),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
 print({'route':route,'columns':len(b),'rows':len(names),'status':int(res.status),'message':res.message})
 if res.success: print('min_surplus',float(np.min(b-A@res.x)))
 else:
  sep=linprog(b,A_ub=-A.T,b_ub=np.zeros(len(names)),A_eq=np.ones((1,len(b))),b_eq=[1],bounds=(0,None),method='highs')
  print('dual_separator',sep.fun if sep.success else sep.message)
