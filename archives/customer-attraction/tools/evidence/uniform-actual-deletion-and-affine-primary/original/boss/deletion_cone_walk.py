"""Full-strategy-cone discovery attack on the uniform deletion cap.
Floating output is not a mathematical certificate. Γ includes every ordered node,
compressed by equal (prefix counts,target terminal) obligations.
"""
from pathlib import Path
import importlib.util,json
import numpy as np
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('old_cone',ROOT/'research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/counterexample/cone_search.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def run(k,m,starts,steps,seed):
 game=module.Game(k,m);rng=np.random.default_rng(seed);best=0;records=[]
 for start in range(starts):
  w=rng.exponential(1,len(game.types));w[rng.random(len(w))<.65]=0
  if start==0:
   w[:]=0;w[1]=2;w[12]=2;w[13]=3
   for a in range(4,k):w[(1<<a)-1]=2
  for step in range(steps):
   values,welfare,outcomes,floors,_=game.solve(w,rng)
   def score(d):
    load=np.array(game.terminals[d])@game.inc.T
    f=np.where(load>0,(m+1)/(m*(load+1)),1)
    return max((game.inc.T*f)@w)/welfare[d] if welfare[d]>1e-10 else 0
   target=max(outcomes[(0,)*k],key=score)
   G,target,choices,W,O=game.cone(w,rng,forced_target=int(target))
   q=game.terminals[target];load=np.array(q)@game.inc.T
   f=np.where(load>0,(m+1)/(m*(load+1)),1)
   candidates=[]
   for a in range(k):
    objective=game.inc[:,a]*f
    lp=game.optimize(G,target,objective)
    if lp.success:candidates.append((float(objective@lp.x)*(m-.5),a,lp))
   ratio,a,lp=max(candidates,key=lambda z:z[0]);w=lp.x
   rec={'start':start,'step':step,'q':q,'ratio':ratio,'query':a,'rows':len(G),'states':len(choices)}
   records.append(rec)
   if ratio>best+1e-8:
    best=ratio;print(json.dumps(rec),flush=True)
    data={'status':'FLOAT_DISCOVERY_ONLY','k':k,'m':m,'seed':seed,'weights':w.tolist(),'record':rec,'choices':[{'q':q,'target':d,'action':a,'children':list(children)} for (q,d),(a,children) in choices.items()],'records':records}
    Path(__file__).with_name(f'deletion_cone_k{k}_m{m}.json').write_text(json.dumps(data,indent=2))
   if ratio>1+1e-7:return
 print(json.dumps({'status':'FINITE_NO_COUNTEREXAMPLE','best':best,'cones':len(records)}))
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6);ap.add_argument('--m',type=int,default=5);ap.add_argument('--starts',type=int,default=10);ap.add_argument('--steps',type=int,default=4);a=ap.parse_args()
 run(a.k,a.m,a.starts,a.steps,71021)
