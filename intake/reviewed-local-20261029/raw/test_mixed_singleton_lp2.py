from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
N=6; S=7; PAIRS=list(combinations_with_replacement(range(S),2)); PAIRS.sort()
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]; A=[F(1,12)]*6
route=(0,0,0,0,1,0)

def rows(I,E):
 final=int(bool(I&1)); J=E | (final<<5); z=J.bit_count(); share=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
 if I.bit_count()==1: floor=A
 elif I==(1<<S)-1: floor=[F(1,6)]*N
 else: floor=B
 out=[share[t]-floor[t] for t in range(N)]
 p=(E&15).bit_count();d=(E>>4)&1
 out += [share[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
 h=p
 for j,k in PAIRS:
  v=((I>>j)&1)+((I>>k)&1); out.append(share[-2]+share[-1]- (F(v,h+v) if v else 0)+F(d,(h+1)*(h+2)))
 for t in range(N-1):
  pt=(J & ((1<<t)-1)).bit_count(); den=pt+N-t
  for j in range(S): out.append(share[t]-F((I>>j)&1,den))
 return J,out
for target_name in ['U','OPT6']:
 cols=[]; R=[]; tar=[]
 for I in range(1,1<<S):
  # route restrict true actual memberships to route labels (except final is already route label 0)
  for E in range(1<<5):
   J,co=rows(I,E)
   # route check: each prior coverage bit must contain I route label
   if any(((E>>t)&1) and not ((I>>route[t])&1) for t in range(5)): continue
   cols.append((I,E,J)); R.append(co)
   tar.append((F(1) if I==(1<<6) else F(int(bool(J))-1,2)) if target_name=='OPT6' else F(int(bool(J))-1,2))
 A_mat=np.array([[float(x) for x in row] for row in R]); b=np.array([float(x) for x in tar]);
 res=linprog(np.zeros(A_mat.shape[1]),A_ub=A_mat,b_ub=b,bounds=(0,None),method='highs')
 print(target_name,'cols',len(cols),'rows',A_mat.shape[1],'status',res.status,res.message)
 if res.success:
  print('min',min(b-A_mat@res.x)); print([(i,float(x)) for i,x in enumerate(res.x) if x>1e-8])
