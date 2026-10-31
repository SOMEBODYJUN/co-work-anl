from functools import lru_cache
from fractions import Fraction
import itertools
import numpy as np
from math import lcm
for m in [3,4,5]:
 z=np.load(__file__.replace('check_last_ratio.py','last_ratio.py')+f'.{m}.npz',allow_pickle=True)
 bits=z['bits']; xx=[Fraction(float(x)).limit_denominator(10**7) for x in z['weights']]
 den=lcm(*(x.denominator for x in xx));weights=[int(x*den) for x in xx]
 n=len(bits); Q=lcm(*range(1,m+1))
 def pay(out):
  cc=bits[list(out)].sum(axis=0).astype(int)
  return tuple(sum(w*int(bits[t,j])* (Q//int(c) if c else 0) for j,(w,c) in enumerate(zip(weights,cc))) for t in out)
 @lru_cache(None)
 def solve(h):
  i=len(h)
  if i==m:return (h,)
  opts=[solve(h+(a,)) for a in range(n)]
  floors=[min(pay(o)[i] for o in sub) for sub in opts]
  floor=max(floors)
  return tuple(o for sub in opts for o in sub if pay(o)[i]>=floor)
 if m<=4:
  oo=solve(())
  print('m',m,'den',den,'nSPE',len(oo),'target',tuple(range(m)) in oo)
  rr=max((Fraction(pay(o)[-1],sum(pay(o))),o,pay(o)) for o in oo)
  print('lastmax',rr,'W',sum(rr[2]))
