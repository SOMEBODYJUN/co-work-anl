from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
N=6;S=7;PAIRS=list(combinations_with_replacement(range(S),2)); PRIVATE=[F(1,12)]*6; SHARED=[F(2,42-5*t) for t in range(5)]+[F(7,72)]
def allowed(I,E,mode):
  # mode: included singleton E among first4 (base), plus position4, plus empty
  if I.bit_count()!=1 or I in (1,1<<6): return True
  j=I.bit_length()-1
  if mode==0:return bool(E&0b1111)
  if mode==1:return bool(E&0b1111) or bool(E&(1<<4))
  if mode==2:return True
  if mode==3:return E in (0,16)
  if mode==4:return bool(E&0b1111) or E==16 or E==0
  if mode==5:return E in (0,16) or bool(E&0b1111)

def cols(mode,omit=6):
  out=[]
  for I in range(1,1<<S):
    for E in range(1<<5):
      if not allowed(I,E,mode):continue
      J=E | ((1 if I&1 else 0)<<5); z=J.bit_count(); sh=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
      target=F(int(bool(J)),1)-(F(0) if I==(1<<omit) else F(1,2))
      out.append((I,E,J,sh,target))
  return out
def rows_for(C):
  rows=[]; names=[]
  # M rows private/shared depending incidence singleton
  for t in range(N):
    row=[]
    for I,E,J,sh,target in C: row.append(sh[t]-(PRIVATE[t] if I.bit_count()==1 else SHARED[t]))
    rows.append(row); names.append(f'M{t}')
  # L
  for j in range(S):
    row=[sh[5]-F((I>>j)&1,E.bit_count()+1) for I,E,J,sh,target in C];rows.append(row);names.append(f'L{j}')
  # singleton ordering rows w_j - w_omit >= 0
  for j in range(S):
    if j==6: continue
    row=[F(1) if I==(1<<j) else (F(-1) if I==(1<<6) else F(0)) for I,E,J,sh,target in C]
    rows.append(row); names.append(f'O{j}')
  # T
  for j,k in PAIRS:
    row=[]
    for I,E,J,sh,target in C:
      p=(E&15).bit_count();d=(E>>4)&1;v=((I>>j)&1)+((I>>k)&1)
      row.append(sh[4]+sh[5]-(F(v,p+v) if v else 0)+F(d,(p+1)*(p+2)))
    rows.append(row);names.append(f'T{j}{k}')
  return rows,names
def solve(mode):
  C=cols(mode); rows,names=rows_for(C);m=len(rows)
  A=[];b=[]
  for ci,c in enumerate(C):A.append([float(r[ci]) for r in rows]+[1.]);b.append(float(c[-1]))
  r=linprog([0.]*m+[-1],A_ub=np.array(A),b_ub=np.array(b),bounds=[(0,None)]*m+[(None,None)],method='highs')
  return r,C,rows,names
for mode in range(6):
 r,C,rows,names=solve(mode);print(mode,len(C),'t=',r.x[-1])
 if r.x[-1]<1e-8:
  print([(n,float(v)) for n,v in zip(names,r.x[:-1]) if v>1e-7])
