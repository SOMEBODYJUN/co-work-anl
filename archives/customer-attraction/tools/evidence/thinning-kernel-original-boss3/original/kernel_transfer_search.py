"""Find an exact harmonic SPE with incompatible polynomial-kernel rows."""
from customer_attraction import Instance, CustomerType, ExactSPESolver
from itertools import product
from fractions import Fraction
import random,numpy as np,json

def solve(p=4,n=3,trials=1000,seed=144):
 rng=random.Random(seed)
 for it in range(trials):
  ty=[CustomerType(frozenset(i for i in range(p) if mask>>i&1),v) for mask in range(1,1<<p) if (v:=rng.randrange(10))]
  ins=Instance(tuple(map(str,range(p))),tuple(ty),n);sol=ExactSPESolver(ins)
  cert=sol.certificate(rng.choice(tuple(sol.outcomes())),action_selector=lambda h,opts:rng.choice(opts),continuation_selector=lambda h,opts:rng.choice(opts))
  def term(h):
   while len(h)<n:h=h+(cert.actions[h],)
   return h
  def payoff(h,a):
   v=[0]*n
   for t in ty:
    if a in t.topics:v[sum(b in t.topics for b in h)-1]+=t.multiplicity
   return v
  rows=[]
  for d in range(n):
   for h in product(range(p),repeat=d):
    actual=payoff(term(h),cert.actions[h])
    for a in range(p):
     dev=payoff(term(h+(a,)),a)
     row=[x-y for x,y in zip(actual,dev)]
     if any(row):rows.append((h,a,row))
  pts=[0.,1.]
  for h,a,row in rows:
   pts.extend(float(r.real) for r in np.polynomial.polynomial.polyroots(row) if abs(r.imag)<1e-8 and 0<r.real<1)
  pts=sorted(set(pts)); pts=sorted(pts+[(a+b)/2 for a,b in zip(pts,pts[1:])])
  feasible=[t for t in pts if all(sum(c*t**j for j,c in enumerate(row))>=-1e-7 for h,a,row in rows)]
  if not feasible:
   # greedily minimize incompatible subsystem
   sub=rows[:]
   for r in rows:
    cand=[s for s in sub if s!=r]
    if not any(all(sum(c*t**j for j,c in enumerate(row))>=-1e-7 for h,a,row in cand) for t in pts):sub=cand
   print('FOUND',p,n,it,'types',[(list(t.topics),t.multiplicity) for t in ty]);print('rows',sub);print('path',term(()));print('actions',list(cert.actions.items()))
   out={'p':p,'n':n,'types':[(list(t.topics),t.multiplicity) for t in ty],'rows':sub,'actions':[(list(h),a) for h,a in cert.actions.items()]}
   print(json.dumps(out));return out
  if it%100==0:print('progress',it,flush=True)
 print('not found')
if __name__=='__main__':solve()
