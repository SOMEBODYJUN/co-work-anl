"""Complete-policy cones with unequal private group sizes and one shared tail.

The prescribed root path has pairwise disjoint coverage for every weight.
Any LP candidate remains discovery until exact full ordered-history replay.
"""
from pathlib import Path
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
from anchor_general_cones import AnchorSearch

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=3);ap.add_argument('--steps',type=int,default=500)
 ap.add_argument('--seed',type=int,default=6102221);ap.add_argument('--output',type=Path,required=True)
 ap.add_argument('--excess-first',action='store_true')
 args=ap.parse_args();rng=random.Random(args.seed);k=args.k;s=AnchorSearch(k,1,individual=True);n=len(s.supports)
 actualmask=sum(1<<a for a in s.path);benchmarkmask=sum(1<<(3*i+1) for i in range(k))|(1<<(3*k))
 welfare=np.array([sum(bool(mask&actualmask) for mask in group) for group in s.supports])
 benchmark=np.array([sum(bool(mask&benchmarkmask) for mask in group) for group in s.supports])
 reward=benchmark.astype(float)
 if args.excess_first:
  reward=np.zeros(n);reward[0]=-.5;reward[1]=1
 best=-1e9;records=[];started=time.time();w=np.array([z for i in range(k) for z in [2,1]]+[0,1,1],float)
 for step in range(args.steps):
  if step%15==0:
   w=np.array([z for i in range(k) for z in [2,1]]+[0,1,1],float)*60
   if step:
    for i in range(k):w[2*i]*=rng.choice([.5,1,2,4])
    for j in range(rng.randrange(2,6)):w[rng.randrange(n)]+=rng.randrange(1,12)
  s.solve(w);rows,routes=s.cone(rng);objective=-reward.copy()
  if step%5==1:objective+=np.array([rng.random()-.5 for _ in range(n)])*1e-5
  res=linprog(objective,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=welfare[None,:],b_eq=[1],bounds=(0,None),method='highs')
  if res.success:
   score=float(reward@res.x)
   if score>best+1e-8:
    best=score;records.append({'step':step,'ratio':score,'weights':res.x.tolist(),'min_slack':float(min(rows@res.x)),'rows':len(rows),'policy_objects':len(routes)})
    print('BEST',step,best,'weights',res.x.tolist(),flush=True)
   w=res.x*240
  else:w[rng.randrange(n)]+=1
  if step%10==0:
   args.output.write_text(json.dumps({'k':k,'steps':step,'best':best,'records':records,'seconds':time.time()-started,'status':'floating complete-policy cones, not exact SPE certificate'},indent=2));print('STEP',step,'best',best,'seconds',time.time()-started,flush=True)
 args.output.write_text(json.dumps({'k':k,'steps':args.steps,'best':best,'records':records,'seconds':time.time()-started,'status':'floating complete-policy cones, not exact SPE certificate'},indent=2))

if __name__=='__main__':main()
