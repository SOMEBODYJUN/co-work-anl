"""Full min/max/allowed/cost cells of the safe HI relaxation, not SPE cones.

LP points are discoveries only; accepted inequalities must replay exact HI.
Excluded actions at a floating cell boundary may become allowed on replay.
"""
from pathlib import Path
import argparse,importlib.util,itertools,json,math,random,time
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-ffea274483aa4105a317300038fe04ce/credible_counterexample/cone_search.py'
spec=importlib.util.spec_from_file_location('old_cone',OLD)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Cells(module.Search):
 def interval(self,w,rng):
  u=np.einsum('lak,k->la',self.pay,w);n=len(self.states);d=len(w);p=self.p
  low=np.zeros((n,p,d),dtype=np.int32);high=low.copy();g=np.zeros((n,d),dtype=np.int32)
  lv=np.zeros((n,p));hv=lv.copy();gv=np.zeros(n);rows=set();select={}
  def choose(vals,maximize=False):
   target=max(vals) if maximize else min(vals)
   return rng.choice([i for i,v in enumerate(vals) if abs(v-target)<1e-7])
  def add(row):
   if np.any(row):rows.add(row.tobytes())
  for q,t in self.leaf_index.items():
   i=self.index[q];low[i]=high[i]=self.pay[t];lv[i]=hv[i]=u[t]
  for i in range(len(self.children)-1,-1,-1):
   ch=self.children[i];f=choose([lv[j,a] for a,j in enumerate(ch)],True)
   lco=low[ch[f],f];floor=lv[ch[f],f]
   allowed=[a for a,j in enumerate(ch) if hv[j,a]>=floor-1e-7]
   for a,j in enumerate(ch):
    add(lco-low[j,a]);add((high[j,a]-lco) if a in allowed else (lco-high[j,a]))
   vsel=[];zsel=[]
   for j in range(p):
    v=allowed[choose([lv[ch[a],j] for a in allowed])]
    z=allowed[choose([hv[ch[a],j] for a in allowed],True)]
    low[i,j]=low[ch[v],j];high[i,j]=high[ch[z],j]
    lv[i,j]=lv[ch[v],j];hv[i,j]=hv[ch[z],j]
    for a in allowed:add(low[ch[a],j]-low[i,j]);add(high[i,j]-high[ch[a],j])
    vsel.append(v);zsel.append(z)
   a=allowed[choose([gv[ch[a]] for a in allowed])]
   for b in allowed:add(g[ch[b]]-g[ch[a]])
   g[i]=lco+g[ch[a]];gv[i]=floor+gv[ch[a]]
   select[i]={'floor':f,'allowed':allowed,'low':vsel,'high':zsel,'cost':a}
  return gv[0]/self.scale,g[0],np.array([np.frombuffer(x,dtype=np.int32) for x in rows]),select

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=7);ap.add_argument('--m',type=int,default=5)
 ap.add_argument('--steps',type=int,default=500);ap.add_argument('--seed',type=int,default=610222)
 ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rng=random.Random(args.seed)
 s=Cells(args.p,args.m);queue=list(module.seeds(args.p,args.m));best=0;records=[];started=time.time()
 private=np.zeros((1<<args.p)-1)
 for a in range(args.p):private[(1<<a)-1]=1
 queue.insert(0,private)
 for j in range(8):
  near=private*60
  for a in range(rng.randrange(1,4)):near[rng.randrange(len(near))]+=rng.randrange(1,4)
  queue.insert(0,near)
 for step in range(args.steps):
  if not queue or step%10==0:
   w=np.zeros((1<<args.p)-1)
   for j in range(rng.randrange(5,18)):w[rng.randrange(len(w))]+=rng.randrange(1,15)
   queue.append(w)
  w=queue.pop(0);G,g,rows,choices=s.interval(w,rng);vals=s.obj@w;obj=int(np.argmax(vals));ratio=float(max(vals)/G)
  if ratio>best+1e-8:
   best=ratio;records.append({'step':step,'kind':'replay_float_HI','ratio':ratio,'G':G,'opt':float(max(vals)),'weights':w.tolist()})
   print('BEST',step,ratio,'G',G,'OPT',max(vals),flush=True)
  if step%5==4:obj=rng.randrange(len(s.portfolios))
  res=linprog(-s.obj[obj].astype(float),A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=g[None,:],b_eq=[s.scale],bounds=(0,None),method='highs')
  if res.success:
   x=res.x;x[x<1e-10]=0;queue.append(x)
   score=float(s.obj[obj]@x)
   if score>best+1e-8:
    records.append({'step':step,'kind':'cell_LP_unreplayed','ratio':score,'weights':x.tolist(),'min_slack':float(min(rows@x)),'portfolio':s.portfolios[obj]})
    print('LP_CANDIDATE',step,score,flush=True)
   if step%3==0:
    y=x*120
    for j in range(2):y[rng.randrange(len(y))]+=rng.choice([1,2,3])
    queue.append(y)
  if step%10==0:
   args.output.write_text(json.dumps({'p':args.p,'m':args.m,'steps':step,'best_replayed':best,'records':records,'seconds':time.time()-started,'status':'floating HI cells, not SPE evidence'},indent=2))
   print('STEP',step,'best',best,'seconds',time.time()-started,flush=True)
 args.output.write_text(json.dumps({'p':args.p,'m':args.m,'steps':args.steps,'best_replayed':best,'records':records,'seconds':time.time()-started,'status':'floating HI cells, not SPE evidence'},indent=2))

if __name__=='__main__':main()
