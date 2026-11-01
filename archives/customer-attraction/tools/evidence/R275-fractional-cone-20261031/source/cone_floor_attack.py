import importlib.util, pathlib, functools, itertools,json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
HERE=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('scan',HERE/'floor_scan.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Cone(mod.Fast):
 def setup(self,w):
  self.U=self.coefs@w
  self.R.cache_clear(); self.th={}
 @functools.lru_cache(None)
 def R(self,k):
  if sum(k)==self.n:return np.array([self.ids[k]],dtype=int)
  ch=[self.R(k[:a]+(k[a]+1,)+k[a+1:]) for a in range(self.p)]
  th=max(self.U[x,a].min() for a,x in enumerate(ch));self.th[k]=th
  return np.unique(np.concatenate([x[self.U[x,a]>=th-1e-8] for a,x in enumerate(ch)]))
 def policy(self,target):
  nodes={}
  def expand(h,k,desired):
   if len(h)==self.n:return desired
   kids=[k[:a]+(k[a]+1,)+k[a+1:] for a in range(self.p)]
   opts=[a for a,ch in enumerate(kids) if desired in self.R(ch) and self.U[desired,a]>=self.th[k]-1e-8]
   chosen=opts[0]
   terms=[]
   for a,ch in enumerate(kids):
    d=desired if a==chosen else min(self.R(ch),key=lambda z:self.U[z,a])
    terms.append(expand(h+(a,),ch,d))
   nodes[h]=(chosen,terms)
   return terms[chosen]
  expand((),(0,)*self.p,target)
  gamma=np.array([self.coefs[terms[chosen],chosen]-self.coefs[term,a] for chosen,terms in nodes.values() for a,term in enumerate(terms) if a!=chosen])
  return gamma,nodes
if __name__=='__main__':
 rng=np.random.default_rng(1238);best=10
 for p,n,iterations in [(5,3,30),(6,4,20),(7,5,10)]:
  f=Cone(p,n)
  benchmarks=[]
  for support in itertools.combinations(range(p),min(p,n)):
   benchmarks.append((support,(f.M[:,support].sum(axis=1)>0).astype(float)))
  for iteration in range(iterations):
   w=rng.choice([0,0,0,1,2,4,8,16],len(f.M)).astype(float)
   if iteration%3==2:
    prev=json.loads((HERE/'cone_best.json').read_text()) if (HERE/'cone_best.json').exists() else None
    if prev and prev['p']==p and prev['n']==n:
     w=np.array(prev['weights'])+rng.choice([0,0,0,.01,.1],len(f.M))
   f.setup(w);root=f.R((0,)*p)
   # root eligible min utility target
   scored=[]
   for z in root:
    v=np.where(f.C[z]>0,f.U[z],np.inf);scored.append((v.min(),z,int(v.argmin())))
   _,target,a=min(scored)
   gamma,nodes=f.policy(target)
   for a in np.flatnonzero(f.C[target]):
    for support,o in benchmarks:
     out=linprog(f.coefs[target,a],A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=o[None,:],b_eq=[1],bounds=(0,None),method='highs')
     if not out.success:continue
     ratio=2*n*out.fun
     if ratio<best-1e-8:
      best=ratio;print(p,n,iteration,'ratio',ratio,'target',f.C[target].tolist(),'a',a,'support',support,flush=True)
      (HERE/'cone_best.json').write_text(json.dumps(dict(p=p,n=n,weights=out.x.tolist(),target=f.C[target].tolist(),a=int(a),support=support,ratio=ratio,policy=[dict(h=h,a=v[0]) for h,v in nodes.items()])))
     if ratio<1-1e-7:print('FLOOR FAIL');raise SystemExit
 print('DONE',best)
