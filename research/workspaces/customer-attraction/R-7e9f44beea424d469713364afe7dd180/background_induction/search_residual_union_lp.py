from fractions import Fraction
from itertools import product
import json,numpy as np
from scipy.optimize import linprog
from pathlib import Path
ROOT=Path(__file__).parent
q=5;masks=list(range(1,1<<q));actual=(0,1);comp=(2,3)
def pay(a,b,focal):return np.array([float(Fraction(bool(mask>>focal&1), int(bool(mask>>a&1))+int(bool(mask>>b&1)))) if mask&(1<<focal) else 0.0 for mask in masks])
paytab={(a,b,f):pay(a,b,f)for a in range(q)for b in range(q)for f in {a,b}}
welfare=np.array([int(bool(mask&3))for mask in masks]);missing=np.array([int(not mask&3 and bool(mask&12))for mask in masks]);best=0
for k,replies in enumerate(product(range(q),repeat=q-1)):
 reply=(1,)+replies
 rows=[]
 for a in range(q):
  for b in range(q):rows.append(paytab[a,reply[a],reply[a]]-paytab[a,b,b])
 for a in range(q):rows.append(paytab[0,1,0]-paytab[a,reply[a],a])
 res=linprog(-missing,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[welfare],b_eq=[1],bounds=(0,None),method='highs')
 if res.success and -res.fun>best+1e-8:
  best=-res.fun;print(k,'best',best,'reply',reply,flush=True)
  if best>1+1e-7:
   den=[Fraction(float(x)).limit_denominator(10000)for x in res.x]
   from math import lcm,gcd
   scale=lcm(*(x.denominator for x in den));weights={m:int(x*scale)for m,x in zip(masks,den)if x}
   obj={'q':q,'m':2,'reply':reply,'weights':weights,'missing_over_W':str(Fraction(str(best))),'actual':actual,'comparison':comp}
   (ROOT/'residual_union_counterexample.json').write_text(json.dumps(obj,indent=2));print(obj);break
print('done best',best)
