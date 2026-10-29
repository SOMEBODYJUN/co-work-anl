from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
N=6; S=7
PAIRS=list(combinations_with_replacement(range(S),2))
# all incidence nonempty and earlier memberships E 5 bits, final determined by I contains actual final 0

def cols(omit=6, singles=None):
    out=[]
    if singles is None: singles=set(range(S))
    for I in range(1,1<<S):
      if I.bit_count()==1 and (I.bit_length()-1 not in singles): continue
      for E in range(1<<5):
        final=int(bool(I&1)); J=E|(final<<5); z=J.bit_count()
        sh=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
        target=F(int(bool(J)),1) - (F(0) if I==(1<<omit) else F(1,2))
        out.append((I,E,J,sh,target))
    return out

def path_rows(path,omit=6,singles=None):
    C=cols(omit,singles)
    rows=[]; names=[]
    # shared mixed floor rows on non-singleton types
    B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
    for t in range(N):
      row=[]
      for I,E,J,sh,target in C:
        row.append(sh[t]-B[t] if I.bit_count()>=2 else F(0))
      rows.append(row); names.append(f'M{t}')
    # Q t,j all current max deviation floors
    for t in range(N):
      r=N-t
      p=[0]*S
      for a in path[:t]: p[a]+=1
      for j in range(S):
        row=[]
        for I,E,J,sh,target in C:
          # denominator p_I+r
          pI=sum(p[k] for k in range(S) if I>>k&1)
          val=F(1,pI+r) if I>>j&1 else F(0)
          row.append(sh[t]-val)
        rows.append(row); names.append(f'Q{t}{j}')
    # pair tax at prefix t=4
    p=path[:4]; hpos=range(4)
    for j,k in PAIRS:
      row=[]
      for I,E,J,sh,target in C:
        h=sum((E>>q)&1 for q in range(4)); d=(E>>4)&1
        v=(I>>j&1)+(I>>k&1)
        tax=F(d,(h+1)*(h+2))
        val=sh[4]+sh[5]-(F(v,h+v) if v else F(0))+tax
        row.append(val)
      rows.append(row); names.append(f'T{j}{k}')
    # ordering singleton masses w_j>=w_omit for j != omit
    for j in range(S):
      if j==omit: continue
      row=[]
      for I,E,J,sh,target in C:
        row.append(F(1) if I==(1<<j) else (F(-1) if I==(1<<omit) else F(0)))
      rows.append(row); names.append(f'O{j}>{omit}')
    return C,rows,names

def solve(path,omit=6,singles=None):
    C, rows, names=path_rows(path,omit,singles)
    # matrix cols by row; include t variable
    A=[]; y=[]
    for ci,c in enumerate(C):
      A.append([float(row[ci]) for row in rows]+[1.0]); y.append(float(c[-1]))
    m=len(rows)
    res=linprog([0.0]*m+[-1.0],A_ub=np.array(A),b_ub=np.array(y),bounds=[(0,None)]*m+[(None,None)],method='highs')
    return res,C,rows,names

if __name__=='__main__':
  paths=[(0,0,0,0,0),(0,1,2,3,4),(0,1,2,3,5),(0,0,1,2,3),(0,1,1,1,1),(0,1,0,2,3),(0,1,2,0,3),(0,1,2,3,0)]
  for singles in ({0,6},{1,6},{0,1},{0,1,6},{0,1,2}):
   print('SINGLES',singles)
   for p in paths:
    r,_,_,names=solve(p,singles=singles)
    print(p,'t',r.x[-1])
