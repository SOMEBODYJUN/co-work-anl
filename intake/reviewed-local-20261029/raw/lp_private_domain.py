from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
n=6;s=7
B=[F(2,42-5*t) for t in range(n-1)]+[F(7,72)]; A=[F(1,12)]*n
pairs=list(combinations_with_replacement(range(s),2)); baseN=n+s+len(pairs)
cols=[]; target=[]; mat=[]
for I in range(1,1<<s):
 for E in range(1<<5):
  final=int(bool(I&1));J=E|(final<<5);z=J.bit_count();sh=[F((J>>t)&1,z) if z else F() for t in range(n)]; floor=A if I.bit_count()==1 else B
  rs=[sh[t]-floor[t] for t in range(n)]
  rs += [sh[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(s)]
  h=(E&15).bit_count();d=(E>>4)&1
  rs += [sh[-2]+sh[-1]-(F(((I>>a)&1)+((I>>b)&1),h+((I>>a)&1)+((I>>b)&1)) if (((I>>a)&1)+((I>>b)&1)) else 0)+F(d,(h+1)*(h+2)) for a,b in pairs]
  # root deviations to each max Bj: u0 - sum_{j in I} 1/6
  rs += [sh[0] - F((I>>j)&1,6) for j in range(s)]
  cols.append((I,E,J));mat.append([float(x) for x in rs]);target.append(float(F(int(bool(J)))- (F(0) if I==64 else F(1,2))))
M=np.array(mat);b=np.array(target);rowsN=baseN+s;AUB=np.hstack([M,np.ones((len(cols),1))]);c=np.zeros(rowsN+1);c[-1]=-1
for mode in ['all','early4','not_uncovered']:
 sel=[]
 for idx,(I,E,J) in enumerate(cols):
  if mode=='early4' and I.bit_count()==1 and I not in (1,64) and not (E&15):continue
  if mode=='not_uncovered' and I.bit_count()==1 and I not in (1,64) and not E:continue
  sel.append(idx)
 res=linprog(c,A_ub=AUB[sel],b_ub=b[sel],bounds=[(0,None)]*rowsN+[(None,None)],method='highs')
 print(mode,'success',res.success,'eps',res.x[-1], 'cols',len(sel))
 if res.success:
  print([(i,round(v,8)) for i,v in enumerate(res.x[:-1]) if v>1e-8])
