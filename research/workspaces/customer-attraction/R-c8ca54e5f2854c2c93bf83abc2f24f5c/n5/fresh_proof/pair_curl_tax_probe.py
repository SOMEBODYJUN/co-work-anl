from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
import itertools,json
# Labels a,b,r,s,p,q,k,l. Branches a,r,s; b,p,q; a,p,k; b,r,l.
n=8
bits=np.array([[(mask>>i)&1 for i in range(n)] for mask in range(1,1<<n)], dtype=float)
def u(a,others,bg=0):
    return bits[:,a]/(bg+1+bits[:,others].sum(axis=1))
for bg in range(3):
  rows=[];names=[]
  def add(name,x):rows.append(x);names.append(name)
  add('first_a',u(2,[0,3],bg)-u(4,[0,6],bg))
  add('first_b',u(4,[1,5],bg)-u(2,[1,7],bg))
  for pre,chosen in [([0,2],3),([1,4],5),([0,4],6),([1,2],7)]:
    for t in range(n):
      add('last_%s_%d'%(str(pre),t),u(chosen,pre,bg)-u(t,pre,bg))
  curl=u(0,[2,3],bg)+u(1,[4,5],bg)-u(0,[4,5],bg)-u(1,[2,3],bg)
  tau=bits[:,2]*(1-bits[:,3])/((bg+bits[:,0]+1)*(bg+bits[:,0]+2))+bits[:,4]*(1-bits[:,5])/((bg+bits[:,1]+1)*(bg+bits[:,1]+2))
  res=linprog(curl,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=tau[None,:],b_eq=[1],bounds=(0,None),method='highs')
  print(bg,'tax_norm',res.status,res.fun,flush=True)
  if res.success:
      print('support',[(i+1,round(float(v),8)) for i,v in enumerate(res.x) if v>1e-8])
      print('dual',[(names[i],round(-v,8)) for i,v in enumerate(res.ineqlin.marginals) if v < -1e-8],flush=True)
