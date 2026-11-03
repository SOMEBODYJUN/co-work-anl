"""Discovery only: integer extra-opponent leader threshold, full ordered policies."""
import importlib.util,itertools,json,random,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[6]
spec=importlib.util.spec_from_file_location('base',ROOT/'research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/background_pair_probe.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
rng=random.Random(1021721)


def run(n,k,bg,w):
 M,sunk,R0,scale=base.representation(n,k,bg)
 actions,G,pair,actual=base.policy_cone(n,k,M,sunk,scale,w,rng)
 h=np.array([actual.count(a) for a in range(k)])@M
 root=M[actual[0]]/np.maximum(sunk+h,1)
 Bs=np.array([tuple(z.count(a) for a in range(k)) for z in itertools.combinations_with_replacement(range(k),n)])
 R=1/(1+sunk+Bs@M)
 starts=[base.security(w,M,R)[0],np.ones(k)/k]
 best=None
 for p in starts:
  old=0.
  for j in range(8):
   nw,v=base.cone_step(G,root,M,R,p)
   p,v=base.security(nw,M,R)
   if best is None or v>best['ratio']:
    best={'ratio':float(v),'n':n,'k':k,'background':bg,'actual':actual,'weights':nw.tolist(),'p':p.tolist(),'actions':{','.join(map(str,h)):int(a) for h,a in actions.items()}}
   if v>1+1e-7 or v<old+1e-9:break
   old=v
 return best

out={'scope':'finite float discovery only','completed':0,'best':None}
for i in range(220):
 n,k=rng.choice([(3,6),(3,7),(4,5),(4,6)])
 bg=[0]*k
 if i%3:
  for _ in range(rng.choice([1,2,4,8])):bg[rng.randrange(k)]+=1
 w=np.array([rng.randrange(1,20) if rng.random()<rng.choice([.2,.5,1.]) else 0 for mask in range(1,1<<k)])
 z=run(n,k,bg,w)
 if out['best'] is None or z['ratio']>out['best']['ratio']+1e-8:
  out['best']=z;print(i,z['ratio'],n,k,bg,flush=True)
 out['completed']=i+1
 if i%10==0 or z['ratio']>1+1e-7:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 if z['ratio']>1+1e-7:break
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
