import importlib.util,pathlib,itertools,json
import numpy as np
from scipy.optimize import linprog
HERE=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('cone',HERE/'cone_floor_attack.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rng=np.random.default_rng(8932);best=10
for p,n,iterations in [(5,3,20),(6,4,20),(7,5,20)]:
 f=mod.Cone(p,n)
 for iteration in range(iterations):
  w=rng.choice([0,0,0,1,2,4,8,16],len(f.M)).astype(float)
  f.setup(w);root=f.R((0,)*p)
  for target in sorted(root,key=lambda z:f.cov[z]@w)[:3]:
   gamma,nodes=f.policy(target);loads=f.den[target];covered=(loads>0).astype(float)
   gc=np.divide(covered,1+(n-1)/n*loads)
   g=f.M.T*np.where(loads>0,(n+1)/(loads+1),n)
   for a in range(p):
    objective=covered+gc-g[a]
    out=linprog(objective,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
    if not out.success:continue
    if out.fun<best-1e-8:
     best=out.fun;print(p,n,iteration,'slack/W',best,'target',f.C[target].tolist(),'a',a,flush=True)
     (HERE/'static_common_best.json').write_text(json.dumps(dict(p=p,n=n,weights=out.x.tolist(),target=f.C[target].tolist(),a=a,slack=best,policy=[dict(h=h,a=v[0]) for h,v in nodes.items()])))
    if best<-1e-7:print('BRIDGE FAIL');raise SystemExit
print('DONE',best)
