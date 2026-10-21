import itertools,numpy as np
from scipy.optimize import linprog

def test(seed,n=3,p=3):
 rng=np.random.default_rng(seed)
 profiles=list(itertools.combinations_with_replacement(range(p),n)); backs=list(itertools.combinations_with_replacement(range(p),n-1))
 phi={q:rng.integers(0,30) for q in profiles};base={b:rng.integers(0,10) for b in backs}
 def u(a,b):return phi[tuple(sorted((*b,a)))]-base[tuple(sorted(b))]
 acts={}
 def end(h):
  while len(h)<n:h+=(acts[h],)
  return h
 for k in reversed(range(n)):
  for h in itertools.product(range(p),repeat=k):
   vals=[u(a,end(h+(a,))[:k]+end(h+(a,))[k+1:]) for a in range(p)]
   acts[h]=max(range(p),key=lambda a:vals[a])
 z=end(());pay=[u(a,z[:i]+z[i+1:]) for i,a in enumerate(z)];W=sum(pay)
 menus=set()
 for i in range(n):
  for a in range(p):
   zz=end(z[:i]+(a,));menus.add(tuple(sorted(zz[:i]+zz[i+1:])))
 M=np.array([[u(a,b) for a in range(p)] for b in menus]);
 r=linprog([*([0]*p),-1],A_ub=np.column_stack([-M,np.ones(len(M))]),b_ub=np.zeros(len(M)),A_eq=[[*(np.ones(p)),0]],b_eq=[1],bounds=[(0,None)]*p+[(None,None)])
 if n*r.x[-1]>W+1e-8:return seed,z,pay,menus,r.x,phi,base
for i in range(10000):
 r=test(i)
 if r:
  print(r);break
else:print('none')
