from pathlib import Path
import sys, importlib.util, random, json
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
source=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec=importlib.util.spec_from_file_location('cone',source); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rng=random.Random(602617);eng=mod.Engine(3,6,rng)
best=-10; records=[]
for it in range(150):
 r=[0]*len(eng.masks)
 if it%3==0:
  r=mod.baseline(3,6)
  for j in range(10):r[rng.randrange(len(r))]+=rng.choice([0,1,2,3,9])
 else:
  for j in range(rng.randrange(4,18)):r[rng.randrange(len(r))]+=rng.randrange(1,15)
 target,_=eng.solve(r,diverse=True);acts,G=eng.strategy(target);a=acts[0][1]
 for rd in range(4):
  price=eng.pay[target,a]@r/eng.L
  n,p=len(eng.masks),eng.p
  lp=linprog(np.r_[np.repeat(price,p),-np.array(r)],A_ub=np.hstack([-eng.inc.T,np.eye(n)]),b_ub=np.zeros(n),bounds=[(0,1)]*(n+p),method='highs')
  z=lp.x[:p];coverage=np.minimum(1,z@eng.inc)
  objective=coverage-(sum(z)-1)*eng.pay[target,a]/eng.L-eng.cov[target]
  lp2=linprog(-objective,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[eng.cov[target]],b_eq=[1.],bounds=(0,None),method='highs')
  if not lp2.success:break
  r=lp2.x
  if -lp2.fun>best+1e-9:
   best=-lp2.fun; cl=eng.exact_recover(G,target,r)
   rec={'it':it,'round':rd,'score':best,'actual':eng.terminal[target].tolist(),'root_action':a,'z':z.tolist(),'clones':cl,'actions':acts}
   if cl:
    inst,cert=mod.verify_canonical(3,6,cl,acts,eng.terminal[target].tolist());rec['instance']=inst.to_dict();rec['certificate']=cert.to_dict()
   (HERE/'three_price_best.json').write_text(json.dumps(rec,indent=2))
   print(json.dumps({k:rec[k] for k in ['it','round','score','actual','root_action','z']}),flush=True)
 records.append({'it':it,'best':best})
 if best>1e-7:break
(HERE/'three_price_report.json').write_text(json.dumps({'scope':'finite cone attack, no universal proof','best':best,'records':records},indent=2))
