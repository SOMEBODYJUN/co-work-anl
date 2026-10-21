"""All-fresh full-history policies: finite numerical cones only."""
import argparse,itertools,json,random,runpy,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
PRE=runpy.run_path('research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_boss/cone_opportunity_attack.py')['prepare']

def main():
 ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=7);ps.add_argument('--players',type=int,default=5);ps.add_argument('--trials',type=int,default=12);ps.add_argument('--seed',type=int,default=2610211);ps.add_argument('--output',required=True);args=ps.parse_args();k=args.topics;m=args.players;rng=random.Random(args.seed);records=[]
 for tr in range(args.trials):
  actions={h:rng.choice([a for a in range(k) if a not in h]) for dep in range(m) for h in itertools.product(range(k),repeat=dep)}
  h=()
  while len(h)<m:h+=actions[h],
  cert={'terminal_counts':[h.count(a) for a in range(k)],'actions':[{'history':q,'action':a} for q,a in actions.items()]}
  p,m,masks,member,act,term,root,path,pay,rows,w=PRE(cert)
  rows=np.unique(rows,axis=0)
  best={'value':-1e99};n=len(masks)
  for comp in itertools.combinations(range(k),min(k,m)):
   o=(member[list(comp)].sum(axis=0)>0).astype(float)
   for a in sorted(set(path)):
    target=o-w-m*pay(root,a)
    ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
    if ans.success and -ans.fun>best['value']+1e-10:best={'value':float(-ans.fun),'comparison':comp,'target_action':a,'root':root,'path':path,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'cert':cert}
  best['trial']=tr;records.append(best)
  print(json.dumps({a:b for a,b in best.items() if a not in ('weights','cert')}),flush=True)
  Path(args.output).write_text(json.dumps({'scope':'numerical fixed complete full-history cones; arbitrary fresh policy choices','parameters':vars(args),'records':records},indent=2)+'\n')
  if best['value']>1e-8:break
if __name__=='__main__':main()
