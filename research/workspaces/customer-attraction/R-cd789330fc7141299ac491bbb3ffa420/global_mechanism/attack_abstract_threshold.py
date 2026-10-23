import itertools,json,time,random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
root=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/global_mechanism')
rng=random.Random(2026102308);start=time.monotonic();tested=0;best=-1
for k,r,tries in [(4,3,1300),(5,3,3000),(6,3,3000),(5,4,1000)]:
 types=list(range(1,1<<k)); tuples=list(itertools.combinations_with_replacement(range(k),r));
 feat=np.zeros((len(tuples),k,len(types)))
 for qi,q in enumerate(tuples):
  for a in range(k):
   for ti,t in enumerate(types):
    feat[qi,a,ti]=((t>>a)&1)/(1+sum((t>>v)&1 for v in q))
 choices=[list(itertools.combinations_with_replacement([v for v in range(k) if v!=a],r-1)) for a in range(k)]
 menu_iterator=(itertools.product(*choices) if k==4 and r==3 else (tuple(rng.choice(c) for c in choices) for _ in range(tries)))
 for menu in menu_iterator:
  tested+=1
  p=np.ones(k)/k if rng.random()<0.7 else np.array([rng.randint(1,7) for _ in range(k)],float);p/=p.sum()
  rows=[];rhs=[]
  for a,tails in enumerate(menu):
   q=(a,)+tails; den=np.array([sum((t>>v)&1 for v in q) for t in types],float)
   util=lambda v:np.array([((t>>v)&1)/d if d else 0 for t,d in zip(types,den)])
   rows.append(np.r_[util(a),0]);rhs.append(1)
   for v in tails:rows.append(np.r_[-util(v),1]);rhs.append(-1)
  for f in feat:
   rows.append(np.r_[-p@f,1]);rhs.append(-1)
  c=np.r_[np.zeros(len(types)),-1]
  res=linprog(c,A_ub=rows,b_ub=rhs,bounds=[(0,None)]*len(types)+[(0,1)],method='highs')
  if res.success and res.x[-1]>best:
   best=float(res.x[-1]);print(json.dumps({'status':'BEST','k':k,'r':r,'delta':best,'tested':tested,'seconds':time.monotonic()-start}),flush=True)
  if res.success and res.x[-1]>1e-7:
   data={'k':k,'r':r,'menu':menu,'p':p.tolist(),'types':{str(t):float(w) for t,w in zip(types,res.x[:-1]) if w>1e-9},'delta':float(res.x[-1]),'tested':tested}
   (root/'abstract_threshold_numeric.json').write_text(json.dumps(data,indent=2));print(json.dumps({'status':'COUNTER','data':data}));raise SystemExit
  if time.monotonic()-start>52:
   print(json.dumps({'status':'TIME','tested':tested,'best':best,'seconds':time.monotonic()-start}));raise SystemExit
 print(json.dumps({'status':'BLOCK','k':k,'r':r,'tested':tested,'best':best,'seconds':time.monotonic()-start}),flush=True)
