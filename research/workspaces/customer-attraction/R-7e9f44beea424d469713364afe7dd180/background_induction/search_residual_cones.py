from search_background import *
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import StrategyCertificate,verify_certificate
import numpy as np
from scipy.optimize import linprog
from math import lcm
rng=random.Random(73882);q=6;r=3;masks=list(range(1,1<<q));best=0
for trial in range(500):
 weights={mask:rng.randrange(1,15)for mask in rng.sample(masks,rng.randrange(6,22))}
 ins=Instance(tuple(map(str,range(q))),tuple(CustomerType(frozenset(a for a in range(q)if mask>>a&1),w)for mask,w in weights.items()),r)
 oracle=ExactSPESolver(ins);outs=sorted(oracle.outcomes());target=rng.choice(outs)
 cert=oracle.certificate(target,action_selector=lambda h,aa:rng.choice(aa),continuation_selector=lambda h,cc:rng.choice(cc))
 def final(h):
  while len(h)<r:h=h+(cert.actions[h],)
  return h
 actual=final(());actualmask=sum(1<<a for a in set(actual))
 def utilcoeff(h,a):
  return [Fraction(int(bool(mask>>a&1)),sum(int(bool(mask>>x&1))for x in h)) if mask>>a&1 else Fraction(0)for mask in masks]
 rows=[]
 for h,a in cert.actions.items():
  on=utilcoeff(final(h),a)
  for b in range(q):
   off=utilcoeff(final(h+(b,)),b)
   rows.append([x-y for x,y in zip(on,off)])
 arr=np.array(rows,dtype=float);welfare=np.array([int(bool(mask&actualmask))for mask in masks]);
 for comp in combinations(range(q),r):
  compmask=sum(1<<a for a in comp);missing=np.array([int(not mask&actualmask and bool(mask&compmask))for mask in masks])
  if not any(missing):continue
  res=linprog(-missing,A_ub=-arr,b_ub=np.zeros(len(rows)),A_eq=[welfare],b_eq=[1],bounds=(0,None),method='highs')
  if res.success and -res.fun>best+1e-8:
   best=-res.fun;print(trial,'best',best,'actual',actual,'comp',comp,flush=True)
   if best>1+1e-7:
    fr=[Fraction(float(v)).limit_denominator(100000)for v in res.x];scale=lcm(*(v.denominator for v in fr));ww={mask:int(v*scale)for mask,v in zip(masks,fr)if v}
    ii=Instance(tuple(map(str,range(q))),tuple(CustomerType(frozenset(a for a in range(q)if mask>>a&1),w)for mask,w in ww.items()),r)
    ver=verify_certificate(ii,cert);ver.assert_valid()
    obj={'trial':trial,'q':q,'m':r,'weights':ww,'certificate':cert.to_dict(),'actual':actual,'comparison':comp,'W':sum(w for mask,w in ww.items()if mask&actualmask),'missing':sum(w for mask,w in ww.items()if not mask&actualmask and mask&compmask)}
    (ROOT/'residual_union_counterexample.json').write_text(json.dumps(obj,indent=2));print(obj);raise SystemExit
print('done best',best)
