from itertools import product
from fractions import Fraction as F
from math import lcm
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
import json
letters='abtsqr';k=len(letters);patterns=list(product((0,1),repeat=k))[1:]
# first allzero not important; product [1:] removes 000000
U=np.array([[[F(p[i],1+p[j]) if p[i] else F(0) for p in patterns] for j in range(k)] for i in range(k)],object)
W=np.array([int(p[0] or p[1]) for p in patterns],float)
R=np.array([int(not(p[0] or p[1]) and (p[2] or p[3])) for p in patterns],float)
best=0
for choices in product(range(k),repeat=3):
 replies=[1,choices[0],4,5,choices[1],choices[2]]
 rows=[]
 for a in range(k):
  for b in range(k):
   if b!=replies[a]:rows.append(U[replies[a],a]-U[b,a])
  if a:rows.append(U[0,1]-U[a,replies[a]])
 A=np.array(rows,float)
 res=linprog(-R,A_ub=-A,b_ub=np.zeros(len(rows)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
 if res.success and -res.fun>best+1e-8:
  best=-res.fun;print('BEST',best,tuple(letters[i] for i in replies),flush=True)
 if res.success and -res.fun>1+1e-8:
  w=[F(v).limit_denominator(1000000) for v in res.x];scale=lcm(*(v.denominator for v in w));w=[int(v*scale) for v in w]
  inst=Instance(tuple(letters),tuple(CustomerType(frozenset(i for i,b in enumerate(p) if b),v) for p,v in zip(patterns,w) if v),2)
  solver=ExactSPESolver(inst);out=(1,1,0,0,0,0)
  if out in solver.outcomes():
   cert=solver.certificate(out);verify_certificate(inst,cert).assert_valid()
   obj={'instance':inst.to_dict(),'outcome':out,'certificate':cert.to_dict(),'residual':sum(int(R[i])*w[i] for i in range(len(w))),'welfare':inst.welfare(out)}
   path='research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/global_proof/residual_counterexample.json'
   open(path,'w').write(json.dumps(obj,indent=2));print('FOUND',path,flush=True);quit()
print('FINAL',best)
