from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

def test(k):
 masks=np.arange(1,1<<k); mem=np.array([[(s>>a)&1 for s in masks] for a in range(k)])
 def pay(a,b):return mem[a]/(1+mem[b])
 best=(-1,None)
 for reply in product(range(k),repeat=k):
  rootvals=[pay(a,reply[a]) for a in range(k)]
  rows=[rootvals[0]-rootvals[a] for a in range(1,k)]
  rows += [pay(reply[a],a)-pay(b,a) for a in range(k) for b in range(k) if b!=reply[a]]
  c=((mem[0]+mem[reply[0]])>0).astype(float)
  ul=pay(reply[0],0)
  for t,s in combinations_with_replacement(range(k),2):
   o=((mem[t]+mem[s])>0).astype(float)
   obj=o-2*c+ul
   res=linprog(-obj,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
   if res.status==0 and -res.fun>best[0]+1e-8:
    best=(-res.fun,(reply,(t,s),res.x))
    print('BEST',k,best,flush=True)
   if res.status==3:print('unbounded',reply,t,s);return
   if res.status==0 and -res.fun>1e-7:return best
 return best
if __name__=='__main__':
 print(test(4))
