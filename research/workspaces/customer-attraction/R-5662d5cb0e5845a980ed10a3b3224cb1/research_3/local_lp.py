from fractions import Fraction as F
from itertools import product
import numpy as np
from scipy.optimize import linprog

names=[]
def row(name):
 names.append(name);return len(names)-1
# source 5 optimal query menus, actual last menu capacity
idx={n:row(n) for n in ['S','Z','V','PAIR']}
for j in range(6):row(f'REPLY_ACT_{j}')
for i in range(4):
 row(f'SAFE_OPT_{i}')
 for j in range(6):row(f'SAFE_ACT_{i}_{j}')
for j in range(6):row(f'LAST_ACT_{j}')
rows=[];targets=[];types=[]
for e in product((0,1),repeat=6):
 p=sum(e[:4]);a,b=e[4:];c=sum(e);w=int(c>0)
 u=[F(v,c) if c else F(0) for v in e]
 for d in range(7):
  for ell in range(7):
   for k in range(max(0,d+ell-6),min(d,ell)+1):
    D=(p+1)*(p+2)
    r=[6*u[4]-F(d,p+1)+F(k,D),6*u[5]-F(ell,p+a+1),F(d*ell-6*k,D),u[4]+u[5]+F(a,D)-F(d,3*(p+1))+F(d*(d-1),30*D)]
    r += [F(ell-6*v,p+1)+F(v*d-k,D) for v in e]
    for i in range(4):
     den=sum(e[:i])+6-i
     r += [6*u[i]-F(d,den)]
     r += [u[i]-F(v,den) for v in e]
    r += [u[5]-F(v,p+a+1) for v in e]
    rows.append([float(v) for v in r]);targets.append((w,int(d>0)));types.append((e,d,ell,k))
A=np.array(rows);w=np.array([v[0] for v in targets]);o=np.array([v[1] for v in targets]);
res=linprog(np.r_[np.zeros(len(names)),1],A_ub=np.c_[A,-w],b_ub=-o,bounds=[(0,None)]*len(names)+[(None,None)],method='highs')
print(res.message, 'states',len(types))
if res.success:
 print('bound',res.fun)
 for n,v in zip(names,res.x):
  if v>1e-8: print(n,v,F(v).limit_denominator(100000))
 y=-res.ineqlin.marginals
 print('primal support',sum(y>1e-8))
 for t,v in zip(types,y):
  if v>1e-8:print(t,v)
