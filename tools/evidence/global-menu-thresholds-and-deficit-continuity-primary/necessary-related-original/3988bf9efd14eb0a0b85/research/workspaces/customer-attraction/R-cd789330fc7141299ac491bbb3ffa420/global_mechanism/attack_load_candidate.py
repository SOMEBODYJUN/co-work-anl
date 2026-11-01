import json,random,time
from fractions import Fraction
from pathlib import Path
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
root=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/global_mechanism')
rng=random.Random(2026102307)
start=time.monotonic(); tested=0; best=None
for m,k,n in [(3,4,500),(4,4,500),(5,5,300),(6,6,80),(5,7,80)]:
 for it in range(n):
  masks=rng.sample(range(1,1<<k),rng.randint(k,min(2*k+3,(1<<k)-1)))
  types=tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randint(1,12)) for mask in masks)
  ins=Instance(tuple(map(str,range(k))),types,m); opt=ins.optimal_welfare(); so=ExactSPESolver(ins)
  for c in so.outcomes():
   f=sum((Fraction(2)-Fraction(1,1+sum(c[a] for a in t.topics)))*t.multiplicity for t in types if any(c[a] for a in t.topics))
   gap=f-opt
   if best is None or gap<best[0]: best=(gap,m,k,it,c,opt,ins.welfare(c),str(f))
   if gap<0:
    cert=so.certificate(c)
    data={'instance':ins.to_dict(),'outcome':list(c),'opt':opt,'welfare':ins.welfare(c),'load_bound':str(f),'gap':str(gap),'strategy':{' '.join(map(str,h)):a for h,a in cert.actions.items()},'tested':tested,'seconds':time.monotonic()-start}
    (root/'load_candidate_counterexample.json').write_text(json.dumps(data,indent=2))
    print(json.dumps({'status':'FAIL','summary':{q:v for q,v in data.items() if q not in ('instance','strategy')},'best':list(map(str,best))}));raise SystemExit
  tested+=1
  if time.monotonic()-start>52:
   print(json.dumps({'status':'TIME','tested':tested,'best':list(map(str,best)),'seconds':time.monotonic()-start}));raise SystemExit
 print(json.dumps({'status':'BLOCK','m':m,'k':k,'tested':tested,'best':list(map(str,best)),'seconds':time.monotonic()-start}),flush=True)
print(json.dumps({'status':'DONE','tested':tested,'best':list(map(str,best)),'seconds':time.monotonic()-start}))
