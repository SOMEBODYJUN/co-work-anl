from itertools import combinations,product
from functools import lru_cache
import random,json,time

def solve(phi,m,p,cap=1000000):
 states=[tuple(frozenset(q) for q in combinations(range(p),t)) for t in range(m+1)]
 def U(q,a):return phi[q]-phi[q-{a}]
 def acts(k):return tuple(a for a in range(p) if a not in k)
 @lru_cache(None)
 def R(k):
  if len(k)==m:return frozenset([k])
  vals={a:R(k|{a}) for a in acts(k)}
  floor=max(min(U(q,a) for q in vals[a]) for a in acts(k))
  return frozenset(q for a in acts(k) for q in vals[a] if U(q,a)>=floor)
 full=R(frozenset())
 assignments=[tuple(states[m])];peak=1
 for t in range(m-1,-1,-1):
  ids={k:i for i,k in enumerate(states[t+1])}; new=set()
  for row in assignments:
   choices=[]
   for k in states[t]:
    aas=acts(k);qs=[row[ids[k|{a}]] for a in aas]
    vals=[U(q,a) for a,q in zip(aas,qs)];vmax=max(vals)
    choices.append(tuple(set(q for q,v in zip(qs,vals) if v==vmax)))
   estimate=1
   for z in choices:estimate*=len(z)
   if estimate>cap:return full,None,dict(level=t,estimate=estimate,peak=peak)
   new.update(product(*choices))
   if len(new)>cap:return full,None,dict(level=t,estimate=len(new),peak=peak)
  assignments=new;peak=max(peak,len(new))
 return full,{z[0] for z in assignments},dict(peak=peak)

if __name__=='__main__':
 rng=random.Random(786);start=time.time();skipped=0
 for i in range(1000):
  m=3;p=6;phi={frozenset(q):rng.randrange(10) for t in (m-1,m) for q in combinations(range(p),t)}
  f,k,info=solve(phi,m,p)
  if k is None:skipped+=1;continue
  if f!=k:
   print(json.dumps({'trial':i,'onlyfull':[sorted(q) for q in f-k],'phi':{','.join(map(str,sorted(q))):v for q,v in phi.items()},'info':info}));break
 else:print(json.dumps(dict(equal=1000-skipped,skipped=skipped,seconds=time.time()-start)))
