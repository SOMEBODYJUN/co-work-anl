import random,itertools,json,sys
from fractions import Fraction
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
rng=random.Random(517392)

def comp(n,k):
 if k==1: yield (n,); return
 for a in range(n+1):
  for q in comp(n-a,k-1): yield (a,)+q

def utility(inst,b,q):
 return sum((Fraction(ct.multiplicity*sum(q[a] for a in ct.topics),sum(b[a]+q[a] for a in ct.topics)) for ct in inst.customers if sum(q[a] for a in ct.topics)),Fraction())

def run(k,r,t,rep):
 best=Fraction(1)
 for z in range(rep):
  cs=tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,13)) for mask in range(1,1<<k) if rng.random()<.55)
  inst=Instance(tuple(map(str,range(k))),cs,r+t)
  b=rng.choice(tuple(comp(t,k)))
  solver=ExactSPESolver(inst)
  opt=max(utility(inst,b,q) for q in comp(r,k))
  for c in solver.outcomes(b):
   q=tuple(c[a]-b[a] for a in range(k))
   u=utility(inst,b,q)
   if u and opt/u>best:
    best=opt/u
    if best>Fraction(19,10): print('best',k,r,t,z,str(best),'b',b,'c',c,flush=True)
   if opt>2*u:
    print('FAIL',k,r,t,z,str(opt),str(u),b,c,[(sum(1<<a for a in x.topics),x.multiplicity) for x in cs],flush=True);return False
 print('DONE',k,r,t,rep,'best',str(best),flush=True);return True
if __name__=='__main__':
 for args in [(4,3,1,3000),(5,3,2,1000),(4,4,2,1000),(5,4,1,600),(5,5,1,300)]:
  if not run(*args):break
