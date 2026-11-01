from fractions import Fraction
from itertools import product
from math import lcm,gcd
from functools import reduce
import json,random,sys
import numpy as np
from scipy.optimize import linprog
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
rng=random.Random(73667)
m=3;g=3;k=9;L=6
cmasks=[x for x in range(1,1<<k) if x&385]
umasks=[6,24,96];masks=cmasks+umasks
cc=len(cmasks);n=len(masks)
obj=np.zeros(n);obj[cc:]=[-1.5,-1,0]
normal=np.zeros(n);normal[:cc]=1
histories=[h for d in range(m) for h in product(range(k),repeat=d)]
def coeff(path,action):
 out=np.zeros(n,dtype=np.int64)
 for i,mask in enumerate(masks):
  if mask>>action&1:
   z=sum(bool(mask>>a&1) for a in path)
   out[i]=L//z
 return out
for it in range(12):
 weights=[0]*n
 for j in rng.sample(range(cc),rng.randrange(3,14)):weights[j]=rng.randint(1,5)
 weights[cmasks.index(1)]+=rng.randint(10,30)
 weights[cmasks.index(128)]+=rng.randint(10,30)
 weights[cmasks.index(256)]+=rng.randint(10,30)
 weights[cc:]=[1,1,1]
 inst=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w) for mask,w in zip(masks,weights) if w),m)
 sol=ExactSPESolver(inst)
 paths=[h for h in sol.ordered_outcomes() if set(h)==set([0,7,8])]
 if not paths:continue
 path=rng.choice(paths)
 cert=sol.certificate(on_path=path,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
 def follow(h):
  while len(h)<m:h=h+(cert.actions[h],)
  return h
 rows=[]
 for h in histories:
  a=cert.actions[h];z=coeff(follow(h),a)
  for b in range(k):
   if b!=a:rows.append(coeff(follow(h+(b,)),b)-z)
 result=linprog(obj,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=normal[None,:],b_eq=[1],bounds=(0,None),method='highs')
 if not result.success:continue
 ratio=-result.fun
 print(it,'path',path,'ratio',ratio,flush=True)
 if ratio>1.000001:
  x=[Fraction(float(v)).limit_denominator(1000000) if v>1e-8 else Fraction(0) for v in result.x]
  mult=lcm(*(v.denominator for v in x))
  xx=[int(v*mult) for v in x];d=reduce(gcd,xx);xx=[v//d for v in xx]
  new=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w) for mask,w in zip(masks,xx) if w),m)
  v=verify_certificate(new,cert)
  if not v.valid:print('rational_failure');continue
  out={'iteration':it,'ratio':str(Fraction(3*xx[cc]+2*xx[cc+1],2*sum(xx[:cc]))),'instance':new.to_dict(),'certificate':cert.to_dict(),'path':path,'W':sum(xx[:cc]),'spectrum_part':str(Fraction(3*xx[cc]+2*xx[cc+1],2)),'OPT':new.optimal_welfare()}
  Path(__file__).with_name('group_spectrum_cone_counterexample.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));break
