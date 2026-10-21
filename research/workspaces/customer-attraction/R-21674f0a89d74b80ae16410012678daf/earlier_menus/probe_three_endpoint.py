from itertools import product
import numpy as np
from scipy.optimize import linprog

def rows(tau, ps):
  A=[]; y=[]; states=[]
  for p in ps:
   for a,b,c,q,r in product(range(2),repeat=5):
    s=a+b+c; den=p+s
    alpha=a/den if a else 0; beta=b/den if b else 0; gamma=c/den if c else 0
    den2=p+c+q+r
    for d in sorted(set([0,1,tau])):
     for ell in [0,tau]:
      o=min(1,d); w=int(p+s>0); D=(p+a+1)*(p+a+2)
      vals=[alpha-q/(p+3),alpha-r/(p+3),tau*gamma-d/(p+a+b+1),tau*gamma-ell/(p+a+b+1),tau*beta-d/(p+a+1)+d*ell/(tau*D),alpha-(c/den2 if c else 0),tau*(r/den2 if r else 0)-d/(p+c+q+1)]
      A.append(vals);y.append(w+tau*alpha-o);states.append((p,a,b,c,q,r,d,ell))
  return np.array(A),np.array(y),states
for tau in [1,1.25,1.5,2,2.5,3,4,5,10,25]:
 A,y,states=rows(tau,list(range(10))+[20,50,100])
 res=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=y,bounds=(0,None),method='highs')
 print(tau,res.success,res.x if res.success else res.message)
