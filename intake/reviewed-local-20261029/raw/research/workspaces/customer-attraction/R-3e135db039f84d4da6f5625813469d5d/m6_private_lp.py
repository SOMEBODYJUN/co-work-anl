from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

n,S=6,7
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
PAIRS=list(combinations_with_replacement(range(S),2))

def col(I,E):
    final=int(bool(I&1)); J=E|(final<<5); z=J.bit_count()
    sh=[F((J>>t)&1,z) if z else F(0) for t in range(n)]
    h=(E&((1<<4)-1)).bit_count(); d=(E>>4)&1
    rows=[]; # six weak mixed rows: private 1/12, all nonprivate B_t, core weakened to B_t
    for t in range(n):
        floor=F(1,12) if I.bit_count()==1 else B[t]
        rows.append(sh[t]-floor)
    rows += [sh[5]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
    for j,k in PAIRS:
        v=((I>>j)&1)+((I>>k)&1)
        tax=F(d,(h+1)*(h+2))
        rows.append(sh[4]+sh[5]-(F(v,h+v) if v else F(0))+tax)
    return J,rows

def solve(omit):
    cols=[]; A=[]; y=[]
    for I in range(1,1<<S):
      for E in range(1<<5):
        J,r=col(I,E)
        target=F(int(bool(J)),1)- (F(0) if I==(1<<omit) else F(1,2))
        # rows 6+7+28; plus ordering rows j!=omit: P_j-P_omit
        rr=list(r)
        for j in range(S):
          if j!=omit: rr.append(F(1) if I==(1<<j) else (F(-1) if I==(1<<omit) else F(0)))
        A.append([float(x) for x in rr]); y.append(float(target)); cols.append((I,E,J,target,rr))
    # Find lambda>=0 s.t. sum lambda*rr <= target, maximizing min residual t.
    m=len(A[0]); c=np.zeros(m+1); c[-1]=-1
    Aub=[]; bub=[]
    for aa,yy in zip(A,y):
      Aub.append(aa+[1.0]); bub.append(yy)
    res=linprog(c,A_ub=np.array(Aub),b_ub=np.array(bub),bounds=[(0,None)]*m+[(None,None)],method='highs')
    return res,cols

if __name__=='__main__':
 for o in range(S):
  res,cols=solve(o); print('omit',o,'success',res.success,'t',res.x[-1] if res.success else None,'fun',res.fun if res.success else res.message)
