from fractions import Fraction as F
from itertools import combinations_with_replacement
N=6;S=7; PAIRS=list(combinations_with_replacement(range(S),2));PAIRS.sort()
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
LAM=[F(207,355), F(417,710), F(253,426), F(133,213), F(0), F(0)] + [F(0),*([F(8,71)]*6)] + [F(0),*([F(7,71)]*6)] + [F(0)]*21

def coeff(I,E):
 final=int(bool(I&1));J=E|(final<<5);z=J.bit_count();sh=[F((J>>t)&1,z) if z else 0 for t in range(N)]
 M=[sh[t]-B[t] for t in range(N)]
 L=[sh[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
 h=(E&15).bit_count(); d=(E>>4)&1; T=[]
 for j,k in PAIRS:
  v=((I>>j)&1)+((I>>k)&1);T.append(sh[-2]+sh[-1]-(F(v,h+v) if v else 0)+F(d,(h+1)*(h+2)))
 return J,[*M,*L,*T]
for j in range(S):
 vals=[]
 for E in range(32):
  I=1<<j;J,co=coeff(I,E)
  target=F(1) if j==6 else F(int(bool(J)),1)-F(1,2)
  res=target-sum(a*b for a,b in zip(LAM,co));vals.append((res,E,J))
 print('j',j,'min',min(vals), 'all',sorted(vals)[:5])
