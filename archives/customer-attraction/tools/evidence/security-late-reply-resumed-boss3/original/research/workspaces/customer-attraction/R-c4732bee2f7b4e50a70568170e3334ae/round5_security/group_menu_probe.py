from __future__ import annotations
import importlib.util,itertools as it,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('menu',P/'menu_union_probe.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
k=6;n=3;members,full=mod.old.data(k,n)
policy={():0}
for a in range(k):
 policy[a,]=3 if a<3 else 0
 for b in range(k):
  group=range(3) if b<3 else range(3,6)
  policy[a,b]=next(c for c in group if c not in(a,b))
terminals={}
def rec(h):
 if len(h)==n:terminals[h]=h;return h
 for a in range(k):rec(h+(a,))
 terminals[h]=terminals[h+(policy[h],)];return terminals[h]
rec(())
gamma,c,_=mod.old.cone(members,policy,terminals)
bgs=mod.menus(k,n,policy,terminals);static=mod.matrix(members,bgs)
ps=[np.array([0,0,.5,0,0,.5]),np.ones(k)/k]
rng=np.random.default_rng(105215);ps.extend(rng.dirichlet(np.ones(k)) for _ in range(50))
best=0.;witness=None
for p0 in ps:
 p=p0
 for _ in range(10):
  ans=mod.old.optimize(members,static,gamma,c,p,n)
  gap=-ans.fun
  if gap>best+1e-10:
   best=gap;witness={'w':ans.x[:-1].tolist(),'p':p.tolist(),'t':float(ans.x[-1]),'backgrounds':bgs}
  p,v=mod.old.safety(static,ans.x[:-1])
print(json.dumps({'best_gap':best,'witness':witness,'backgrounds':bgs}))
(P/'group_menu_probe.json').write_text(json.dumps({'best_gap':best,'witness':witness,'backgrounds':bgs},indent=2)+'\n')
