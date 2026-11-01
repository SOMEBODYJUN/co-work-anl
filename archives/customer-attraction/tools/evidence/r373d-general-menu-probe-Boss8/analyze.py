from fractions import Fraction as F

def compositions(n,k):
 if k==1:yield(n,);return
 for j in range(n+1):
  for v in compositions(n-j,k-1):yield(j,)+v

def u(m,q,j):
 a,b,c=q
 return (F(1,a+b)+F(1,a+c) if j==0 else F(1,a+b)+F(1,m*b) if j==1 else F(1,a+c)+F(1,m*c))
def last(m,q):
 vals=[]
 for j in range(3):
  r=list(q);r[j]+=1;vals.append(u(m,r,j))
 return max((2,1,0), key=lambda j:vals[j])
def complete(m,q):
 r=list(q);r[0]+=m-1-sum(r);r[last(m,r)]+=1;return r
for m in range(2,61):
 vals=[]
 for n in range(m-1):
  for q in compositions(n,3):
   if q==(0,0,0): continue
   out=[]
   for j in range(3):
    r=list(q);r[j]+=1;r=complete(m,r);out.append(u(m,r,j))
   vals.append((out[0]-max(out),q,out))
 w=min(vals,key=lambda x:x[0]) if vals else None
 print(m,'count',len(vals),'min-ex-empty',w,'neg',sum(x[0]<0 for x in vals),'pos',sum(x[0]>0 for x in vals))
