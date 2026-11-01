from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
N=6; S=7
PAIRS=list(combinations_with_replacement(range(S),2)); PAIRS.sort()
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
# mixed private envelope A=1/12 each t
A=[F(1,12)]*6

def rows(I,E):
 final=int(bool(I&1)); J=E | (final<<5); z=J.bit_count()
 share=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
 # M rows: core 1/6, singleton A, shared B
 if I.bit_count()==1: floor=A
 elif I==(1<<S)-1: floor=[F(1,6)]*N
 else: floor=B
 M=[share[t]-floor[t] for t in range(N)]
 L=[share[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
 h=(E & ((1<<(N-2))-1)).bit_count(); d=(E>>(N-2))&1
 T=[]
 for j,k in PAIRS:
  v=((I>>j)&1)+((I>>k)&1)
  tax=F(d,(h+1)*(h+2))
  T.append(share[-2]+share[-1]-(F(v,h+v) if v else 0)+tax)
 return J,[*M,*L,*T]
cols=[]; rowsF=[]; target=[]
for I in range(1,1<<S):
 for E in range(1<<(N-1)):
  J,co=rows(I,E); cols.append((I,E,J)); rowsF.append(co); target.append((F(1,1) if I==(1<<6) else F(int(bool(J)),1)-F(1,2)))
A_mat=np.array([[float(rowsF[c][r]) for r in range(41)] for c in range(len(cols))])
b=np.array([float(x) for x in target])
# vars lambda 41, eps. Constraints A*lam + eps <= target
Aub=np.zeros((len(cols),42)); Aub[:,:41]=A_mat; Aub[:,41]=1
bub=b
c=np.zeros(42); c[41]=-1
res=linprog(c,A_ub=Aub,b_ub=bub,bounds=[(0,None)]*42,method='highs')
print('status',res.status,res.message,'eps',res.x[41] if res.success else None)
if res.success:
 print('min slack',min(bub[i]-Aub[i,:41]@res.x[:41] for i in range(len(cols))))
 print('nonzero',[(i,res.x[i]) for i in range(41) if res.x[i]>1e-8])
 # exact rationalize and check
 from fractions import Fraction
 lam=[Fraction(float(x)).limit_denominator(1000000) for x in res.x[:41]]
 mn=None; arg=None
 for idx,(I,E,J) in enumerate(cols):
  rr=target[idx]-sum(lam[r]*rowsF[idx][r] for r in range(41))
  if mn is None or rr<mn: mn,arg=rr,(I,E,J)
 print('rational min',mn,arg)
 print('rational lam',[(i,x) for i,x in enumerate(lam) if x])
