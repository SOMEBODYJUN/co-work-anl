from itertools import product
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
# letters a,b,t,s,q,r; history q reply after t, r reply after s
letters='abtsqr'
names=[]
rows=[]
patterns=list(product((0,1),repeat=6))
def u(p,i,j):return F(p[i],1+p[j]) if p[i] else F(0)
# exact u own membership / own+other; own1 if>0
# actual payoff u_a(a,b), u_b(b,a)
def add(n,func):names.append(n);rows.append([func(p) for p in patterns])
for d,rep in [(2,4),(3,5)]:add('root '+letters[d],lambda p,d=d,rep=rep:u(p,0,1)-u(p,d,rep))
for d in range(2,6):add('last '+letters[d],lambda p,d=d:u(p,1,0)-u(p,d,0))
for d,rep in [(2,4),(3,5)]:
 for x in range(6):
  if x==rep:continue
  add(letters[d]+'reply vs '+letters[x],lambda p,d=d,rep=rep,x=x:u(p,rep,d)-u(p,x,d))
c=[F(int(p[0] or p[1])-int(not(p[0] or p[1]) and (p[2] or p[3]))) for p in patterns]
A=np.array(rows,float).T
res=linprog(np.ones(len(rows)),A_ub=A,b_ub=np.array(c,float),bounds=(0,None),method='highs')
print(res.message)
if res.success:
 for n,v in zip(names,res.x):
  if v>1e-6:print(n,F(v).limit_denominator(1000000))
 lam=[F(v).limit_denominator(1000000) for v in res.x]
 rem=[c[j]-sum(lam[i]*rows[i][j] for i in range(len(rows))) for j in range(len(c))]
 print('min exact',min(rem),'zero',rem.count(0))
else:

 res2=linprog(np.array(c,float),A_ub=-A.T,b_ub=np.zeros(len(rows)),A_eq=[np.array([int(p[0] or p[1]) for p in patterns])],b_eq=[1],bounds=(0,None),method='highs')
 print(res2.message,res2.fun)
 if res2.success:
  for p,v in zip(patterns,res2.x):
   if v>1e-6:print(''.join(letters[i] for i,b in enumerate(p) if b),F(v).limit_denominator(1000000))
