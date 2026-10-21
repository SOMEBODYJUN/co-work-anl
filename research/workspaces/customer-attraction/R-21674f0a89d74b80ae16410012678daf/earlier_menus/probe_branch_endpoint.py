from itertools import product
import numpy as np
from scipy.optimize import linprog

def compositions(n,k):
 if k==1:
  yield (n,);return
 for a in range(n+1):
  for tail in compositions(n-a,k-1):yield (a,)+tail

def rows(n,ps):
 A=[];y=[];states=[]
 patterns=list(product(range(2),repeat=3))
 for hist in compositions(n,8):
  d=sum(v*t for v,(t,q,r) in zip(hist,patterns)); e=sum(v*q for v,(t,q,r) in zip(hist,patterns));f=sum(v*r for v,(t,q,r) in zip(hist,patterns))
  for p in ps:
   rootQ=sum(v*t/(p+1+q+r) for v,(t,q,r) in zip(hist,patterns))
   middle=sum(v*q/(p+t+1+r) for v,(t,q,r) in zip(hist,patterns))
   final=sum(v*r/(p+t+q+1) for v,(t,q,r) in zip(hist,patterns))
   floor=sum(v/(p+t+2) for v,(t,q,r) in zip(hist,patterns))
   price=sum(v/(p+t+q+1) for v,(t,q,r) in zip(hist,patterns))
   for a,b,c in product(range(2),repeat=3):
    s=a+b+c;alpha=a/(p+s) if a else 0; beta=b/(p+s) if b else 0; gamma=c/(p+s) if c else 0
    vals=[n*alpha-rootQ,n*alpha-e/(p+3),n*alpha-f/(p+3)]
    vals.extend([n*middle-k*floor for k in [d,e,f]])
    vals.extend([middle-k*floor for k in [a,b,c]])
    vals.extend([n*final-k*price for k in [d,e,f]])
    vals.extend([final-k*price for k in [a,b,c]])
    vals.extend([n*gamma-k/(p+a+b+1) for k in [d,e,f]])
    vals.extend([n*beta-k/(p+a+2) for k in [d,e,f]])
    A.append(vals); y.append(int(p+s>0)+n*alpha-int(d>0)); states.append((p,a,b,c,hist))
 return np.array(A),np.array(y),states
if __name__=='__main__':
 for n in [3,4,5,6,8,10]:
  A,y,states=rows(n,range(n-2))
  res=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=y,bounds=(0,None),method='highs')
  print(n,len(y),res.success,res.x if res.success else res.message,flush=True)
