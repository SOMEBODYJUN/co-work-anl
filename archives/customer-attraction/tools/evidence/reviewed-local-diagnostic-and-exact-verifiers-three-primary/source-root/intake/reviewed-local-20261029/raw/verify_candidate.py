from fractions import Fraction as Q
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
n=6;s=7
B=[Q(2,42-5*t) for t in range(n-1)]+[Q(7,72)];A=[Q(1,12)]*n
pairs=list(combinations_with_replacement(range(s),2))
rowsN=n+s+len(pairs)+s
cols=[]; rows=[]; targets=[]
for I in range(1,1<<s):
 for E in range(32):
  final=int(bool(I&1));J=E|(final<<5);z=J.bit_count();sh=[Q((J>>t)&1,z) if z else Q() for t in range(n)];floor=A if I.bit_count()==1 else B
  rs=[sh[t]-floor[t] for t in range(n)]+[sh[-1]-Q((I>>j)&1,E.bit_count()+1) for j in range(s)];h=(E&15).bit_count();d=(E>>4)&1
  rs += [sh[-2]+sh[-1]-(Q(((I>>a)&1)+((I>>b)&1),h+((I>>a)&1)+((I>>b)&1)) if (((I>>a)&1)+((I>>b)&1)) else Q())+Q(d,(h+1)*(h+2)) for a,b in pairs]
  rs += [sh[0]-Q((I>>j)&1,6) for j in range(s)]
  cols.append((I,E,J));rows.append(rs);targets.append(Q(int(bool(J)))-(Q(0) if I==64 else Q(1,2)))
# float LP for domain with included singleton E !=0
sel=[i for i,(I,E,J) in enumerate(cols) if not (I.bit_count()==1 and I not in (1,64) and not E)]
M=np.array([[float(x) for x in rows[i]] for i in sel]);b=np.array([float(targets[i]) for i in sel]);AUB=np.hstack([M,np.ones((len(sel),1))]);c=np.zeros(rowsN+1);c[-1]=-1
res=linprog(c,A_ub=AUB,b_ub=b,bounds=[(0,None)]*rowsN+[(None,None)],method='highs')
print('eps',res.x[-1])
for den in [100,1000,10000,100000,1000000,10000000]:
 lam=[Q(float(v)).limit_denominator(den) for v in res.x[:-1]]
 vals=[targets[i]-sum(lam[j]*rows[i][j] for j in range(rowsN)) for i in sel]
 print('den',den,'min',min(vals),'arg',cols[sel[vals.index(min(vals))]],'nz',[(i,x) for i,x in enumerate(lam) if x])
