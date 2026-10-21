from fractions import Fraction as F
from itertools import product

def compositions(n,k):
 if k==1:yield(n,);return
 for j in range(n+1):
  for v in compositions(n-j,k-1):yield(j,)+v

def probe(m):
 def u(q,j):
  a,b,c=q
  return (F(1,a+b)+F(1,a+c) if j==0 else
    F(1,a+b)+F(1,m*b) if j==1 else F(1,a+c)+F(1,m*c))
 def last(q):
  vals=[]
  for j in range(3):
   r=list(q);r[j]+=1;vals.append(u(r,j))
  return max((2,1,0), key=lambda j:vals[j])
 def complete(q):
  r=list(q);r[0]+=m-1-sum(r);r[last(r)]+=1;return r
 worst=None
 for n in range(m-1):
  for q in compositions(n,3):
   vals=[]
   for j in range(3):
    r=list(q);r[j]+=1;r=complete(r);vals.append(u(r,j))
   gap=vals[0]-max(vals)
   if worst is None or gap<worst[0]:worst=(gap,q,vals)
 return worst
for m in range(2,61):
 p=probe(m)
 print(m,p,flush=True)
 if p[0]<0:break
