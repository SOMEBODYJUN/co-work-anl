import itertools,numpy as np,json
from scipy.optimize import linprog

def test(seed,n=3,p=4,tries=10):
 rng=np.random.default_rng(seed)
 profiles=list(itertools.combinations_with_replacement(range(p),n)); backs=list(itertools.combinations_with_replacement(range(p),n-1))
 ix={s:i for i,s in enumerate(profiles)};ib={s:i+len(ix) for i,s in enumerate(backs)};K=len(ix)+len(ib)
 def ur(a,b):
  z=np.zeros(K);z[ix[tuple(sorted((*b,a)))]]=1;z[ib[tuple(sorted(b))]]=-1;return z
 phi=rng.random(K)*100
 def u(a,b):return ur(a,b)@phi
 acts={}
 def end(h):
  while len(h)<n:h+=(acts[h],)
  return h
 for k in reversed(range(n)):
  for h in itertools.product(range(p),repeat=k):
   vals=[u(a,end(h+(a,))[:k]+end(h+(a,))[k+1:]) for a in range(p)]
   acts[h]=max(range(p),key=lambda a:vals[a])
 z=end(());pay=[ur(a,z[:i]+z[i+1:]) for i,a in enumerate(z)];W=np.sum(pay,axis=0)
 rows=[]
 for h,a0 in acts.items():
  zz=end(h);b0=zz[:len(h)]+zz[len(h)+1:]
  for a in range(p):
   za=end(h+(a,));ba=za[:len(h)]+za[len(h)+1:]
   rows.append(ur(a0,b0)-ur(a,ba))
 menus=set()
 for i in range(n):
  for a in range(p):
   zz=end(z[:i]+(a,));menus.add(tuple(sorted(zz[:i]+zz[i+1:])))
 for q in [np.ones(p)/p,*[rng.dirichlet(np.ones(p)) for _ in range(tries-1)]]:
  M=np.array([sum((q[a]*ur(a,b) for a in range(p)),np.zeros(K)) for b in menus])
  AA=np.vstack([np.column_stack([-np.array(rows),np.zeros(len(rows))]),np.column_stack([-M,np.ones(len(M))])])
  res=linprog(np.r_[W/n,-1],A_ub=AA,b_ub=np.zeros(len(AA)),bounds=[(-1,1)]*K+[(None,None)],method='highs')
  if res.success and -res.fun>1e-8:
   return {'seed':seed,'gap':-res.fun,'path':z,'p':q.tolist(),'menus':list(menus),'phi':res.x[:-1].tolist(),'profiles':profiles,'backs':backs,'payoffs':[v@res.x[:-1] for v in pay],'actions':[(h,a) for h,a in acts.items()]}
for i in range(300):
 r=test(i,n=3,p=4)
 if r:
  print(json.dumps(r));break
else: print('none')
