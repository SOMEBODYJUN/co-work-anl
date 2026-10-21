from convex_menu_search import *
from scipy.optimize import linprog
import numpy as np

def relax_states(I):
 p=I.topic_count
 @lru_cache(None)
 def solve(k):
  if sum(k)==I.players:return frozenset({I.topic_payoffs(k)+(F(I.welfare(k)),)})
  childs=[solve(tuple(x+(i==a) for i,x in enumerate(k))) for a in range(p)]
  threshold=max(min(v[a] for v in C) for a,C in enumerate(childs));ans=set()
  for a,C in enumerate(childs):
   good=[v for v in C if v[a]>=threshold];bad=[v for v in C if v[a]<threshold];ans.update(good)
   for v in good:
    if v[a]==threshold:continue
    for w in bad:
     t=(threshold-w[a])/(v[a]-w[a]);ans.add(tuple(t*x+(1-t)*y for x,y in zip(v,w)))
  return frozenset(ans)
 solve((0,)*p)
 return solve
if __name__=='__main__':
 rng=random.Random(819732)
 for p,m,num in [(3,3,300),(4,3,300),(4,4,200),(5,4,100)]:
  for z in range(num):
   C=[]
   for mask in range(1,1<<p):
    v=rng.randrange(5)
    if v:C.append(CustomerType(frozenset(a for a in range(p) if mask>>a&1),v))
   I=Instance(tuple(map(str,range(p))),tuple(C),m);S=ExactSPESolver(I);rel=relax_states(I)
   S.outcomes()
   for k,Q in S._outcomes.items():
    cols=[a for a in range(p) if k[a]]+[p]
    H=[I.topic_payoffs(q)+(F(I.welfare(q)),) for q in Q]
    points=[tuple(v[a] for a in cols) for v in H]
    Eq=np.array([[float(v[j]) for v in points] for j in range(len(cols))]+[[1]*len(points)])
    for y in rel(k):
     yy=tuple(y[a] for a in cols)
     if yy in points:continue
     rr=linprog(np.zeros(len(points)),A_eq=Eq,b_eq=np.array([float(v) for v in yy]+[1]),bounds=(0,None),method='highs')
     if not rr.success:
      print(json.dumps({'p':p,'m':m,'z':z,'k':k,'cols':cols,'relaxed':list(map(str,yy)),'pure':[list(map(str,v)) for v in points],'instance':I.to_dict()}),flush=True);raise SystemExit
  print('DONE',p,m,flush=True)
