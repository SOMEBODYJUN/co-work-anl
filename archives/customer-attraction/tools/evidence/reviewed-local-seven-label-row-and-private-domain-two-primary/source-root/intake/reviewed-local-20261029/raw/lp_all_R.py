from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
n=6;s=7;B=[F(2,42-5*t) for t in range(n-1)]+[F(7,72)];A=[F(1,12)]*n;pairs=list(combinations_with_replacement(range(s),2));rowsN=n+s+len(pairs)+n*s
cols=[];targets=[];mat=[]
for I in range(1,1<<s):
 for E in range(32):
  final=int(bool(I&1));J=E|(final<<5);z=J.bit_count();sh=[F((J>>t)&1,z) if z else F() for t in range(n)];floor=A if I.bit_count()==1 else B
  rs=[sh[t]-floor[t] for t in range(n)]+[sh[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(s)];h=(E&15).bit_count();d=(E>>4)&1
  rs += [sh[-2]+sh[-1]-(F(((I>>a)&1)+((I>>b)&1),h+((I>>a)&1)+((I>>b)&1)) if (((I>>a)&1)+((I>>b)&1)) else 0)+F(d,(h+1)*(h+2)) for a,b in pairs]
  rs += [F((I>>j)&1,6) for i in range(n) for j in range(s)]
  cols.append((I,E,J));mat.append([float(x) for x in rs]);targets.append(float(F(int(bool(J)))-(F(0) if I==64 else F(1,2))))
M=np.array(mat);b=np.array(targets);AUB=np.hstack([M,np.ones((len(cols),1))]);c=np.zeros(rowsN+1);c[-1]=-1
res=linprog(c,A_ub=AUB,b_ub=b,bounds=[(0,None)]*rowsN+[(None,None)],method='highs');print(res.success,res.x[-1],len(cols),rowsN);print([(i,v) for i,v in enumerate(res.x[:-1]) if v>1e-8])
