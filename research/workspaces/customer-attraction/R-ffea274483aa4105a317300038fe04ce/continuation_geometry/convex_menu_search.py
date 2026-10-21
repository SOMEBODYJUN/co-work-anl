from fractions import Fraction as F
from functools import lru_cache
import random,json
from customer_attraction import Instance,CustomerType,ExactSPESolver

def convex_relax(I):
 p=I.topic_count
 @lru_cache(None)
 def solve(k):
  if sum(k)==I.players:
   return frozenset({I.topic_payoffs(k)+(F(I.welfare(k)),)})
  childs=[]
  for a in range(p):
   ka=tuple(x+(i==a) for i,x in enumerate(k))
   childs.append(solve(ka))
  threshold=max(min(v[a] for v in C) for a,C in enumerate(childs))
  ans=set()
  for a,C in enumerate(childs):
   good=[v for v in C if v[a]>=threshold];bad=[v for v in C if v[a]<threshold]
   ans.update(good)
   for v in good:
    if v[a]==threshold:continue
    for w in bad:
     t=(threshold-w[a])/(v[a]-w[a])
     ans.add(tuple(t*x+(1-t)*y for x,y in zip(v,w)))
  # Exhaustive pair intersections; convex hull unchanged by retaining nonvertices.
  return frozenset(ans)
 return solve((0,)*p)
if __name__=='__main__':
 rng=random.Random(920004)
 for p,m,num in [(3,3,100),(4,3,100),(3,4,100)]:
  for z in range(num):
   C=[]
   for mask in range(1,1<<p):
    v=rng.randrange(6)
    if v:C.append(CustomerType(frozenset(a for a in range(p) if mask>>a&1),v))
   I=Instance(tuple(map(str,range(p))),tuple(C),m)
   S=ExactSPESolver(I); pure=S.minimum_welfare(); P=convex_relax(I); relaxed=min(v[-1] for v in P)
   if relaxed<pure:
    print(json.dumps({'p':p,'m':m,'z':z,'pure':pure,'relaxed':str(relaxed),'vectors':len(P),'instance':I.to_dict()}),flush=True);raise SystemExit
  print('DONE',p,m,flush=True)
