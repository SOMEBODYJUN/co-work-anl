"""Directed finite attack on the uniform deletion sufficient interface.
Exact SPE outcome sets; float scores for discovery, no universal inference.
"""
from pathlib import Path
import importlib.util,json,random
import numpy as np
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('old_exact',ROOT/'research/workspaces/customer-attraction/R-d28e1c3c70cf4adfbb52398ac7cf4c7b/experiments/cex_exact_sweep.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def run(k,m,trials=500,seed=71021):
 eng=module.IntegerSetSolver(k,m);bits=np.array([[(T>>a)&1 for T in eng.types] for a in range(k)])
 caps=[]
 for q in eng.terminals:
  load=np.array(q)@bits
  f=np.where(load>0,(m+1)/(m*(load+1)),1)
  caps.append(bits*f)
 caps=np.array(caps)
 rng=random.Random(seed);best=0;champ=[0]*len(eng.types);champ[0]=m
 for a in range(1,k):champ[(1<<a)-1]=1
 records=[]
 for t in range(trials):
  if t%50==1:w=[rng.randrange(1,m+2) if rng.random()<.3 else 0 for _ in eng.types]
  else:
   w=champ.copy()
   if t:
    for _ in range(rng.randrange(1,4)):
     j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.choice([-2,-1,1,2]))
  out=eng.solve(w);root=out['root_outcomes'];local=0
  for q in root:
   idx=eng.tindex[q];W=int(eng.last_welfare[idx])
   if not W:continue
   values=caps[idx]@w;a=int(np.argmax(values));ratio=float(values[a])*(m-.5)/W
   local=max(local,ratio)
   if ratio>best+1e-10:
    best=ratio;champ=w.copy();row={'k':k,'m':m,'trial':t,'q':q,'query':a,'ratio':ratio,'W':W,'weights':{T:int(v) for T,v in zip(eng.types,w) if v}}
    records.append(row);print(json.dumps(row),flush=True)
    if ratio>1+1e-8:return {'status':'CANDIDATE','records':records,'seed':seed}
  if local>=best-1e-10:champ=w.copy()
 return {'status':'FINITE_NO_COUNTEREXAMPLE','k':k,'m':m,'trials':trials,'seed':seed,'records':records}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=5);ap.add_argument('--m',type=int,default=5);ap.add_argument('--trials',type=int,default=500)
 args=ap.parse_args();out=run(args.k,args.m,args.trials)
 Path(__file__).with_name(f'deletion_outcome_k{args.k}_m{args.m}.json').write_text(json.dumps(out,indent=2))
 print(json.dumps({a:b for a,b in out.items() if a!='records'}))
