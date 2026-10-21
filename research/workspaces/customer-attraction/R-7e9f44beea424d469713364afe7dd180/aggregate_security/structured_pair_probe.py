"""Sacrificial-prefix policies; all history Gamma retained."""
import json,itertools,random
from pathlib import Path
import numpy as np
from probe import policy_matrix,security,cone_step
OUT=Path(__file__).resolve().parent
rng=random.Random(915830)
for groups,width,n in [(3,2,4),(3,3,5),(4,2,5)]:
 k=groups*width
 for mode in range(6):
  actions={}
  def choose(h):
   if len(h)==n:return h
   if not h:a=0
   elif len(h)<groups:
    gs=[x//width for x in h]
    avail=[g for g in range(groups) if g not in gs]
    g=(avail[0] if mode%2==0 else avail[-1]) if avail else ((gs[-1]+1)%groups)
    a=width*g+mode//2%width
   else:
    g=h[groups-1]//width
    av=[a for a in range(width*g,width*(g+1)) if a not in h]
    a=av[0] if av else width*g+(mode//2)%width
   actions[h]=a
   chosen=None
   for b in range(k):
    r=choose(h+(b,))
    if b==a:chosen=r
   return chosen
  actual=choose(())
  G,c,member,R,q=policy_matrix(actions,n,k)
  pair=(member[actual[0]]+member[actual[1]])/np.maximum(np.array(q)@member,1)
  best=0
  for st in range(5):
   p=np.ones(k)/k if st==0 else np.random.default_rng(9971*mode+st).dirichlet(np.ones(k))
   for iteration in range(8):
    w,v=cone_step(G,pair,member,R,p)
    p,v=security(w,member,R)
    ratio=2*v
    if ratio>best+1e-8:
     best=ratio;print(json.dumps(dict(n=n,k=k,mode=mode,start=st,it=iteration,ratio=ratio)),flush=True)
    if ratio>1+1e-7:
     record=dict(n=n,k=k,mode=mode,ratio=ratio,weights=w.tolist(),p=p.tolist(),on_path=actual,actions={','.join(map(str,h)):a for h,a in actions.items()},status='numerical_only')
     (OUT/'structured_pair_failure.json').write_text(json.dumps(record,indent=2)+'\n')
     raise SystemExit
