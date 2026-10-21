from probe_tax_endpoint import rows
from scipy.optimize import linprog
import numpy as np
A,y,states=rows(3,list(range(11))+[20,50,100])
for kind in ['cover','profit']:
 for C in [2,2.25,2.5,2.75,3]:
  target=[]
  for p,a,b,c,hist in states:
   s=a+b+c;alpha=a/(p+s) if a else 0
   d=sum(hist[i]*((i>>2)&1) for i in range(8))
   W=int(p+s>0) if kind=='cover' else (s/(p+s) if s else 0)
   O=int(d>0) if kind=='cover' else (d/(p+d) if d else 0)
   target.append(W+C*alpha-O)
  r=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=target,bounds=(0,None),method='highs')
  print(kind,C,r.success,flush=True)
  if r.success: print(r.x,flush=True)
