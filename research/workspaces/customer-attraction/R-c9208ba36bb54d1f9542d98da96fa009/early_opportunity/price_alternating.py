"""Alternating fixed-policy cone / fractional price search; numerical only."""
import argparse,itertools,json,random,runpy
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
D=runpy.run_path('research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity/count_policy_attack.py');prepare=D['prepare']

def price(member,mass,u):
 k,n=member.shape
 # variables queries z, capped coverage y
 c=np.concatenate([np.full(k,u),-mass]);rows=np.hstack([-member.T,np.eye(n)])
 a=linprog(c,A_ub=rows,b_ub=np.zeros(n),bounds=[(0,None)]*k+[(0,1)]*n,method='highs')
 return a.x[:k],-a.fun

def main():
 ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=7);ps.add_argument('--players',type=int,default=5);ps.add_argument('--trials',type=int,default=100);ps.add_argument('--seed',type=int,default=2026102116);ps.add_argument('--output',required=True);args=ps.parse_args();k=args.topics;m=args.players;rng=random.Random(args.seed);records=[];n=(1<<k)-1
 for tr in range(args.trials):
  start=np.array([rng.choice([0,0,0,1,2,5,10]) for _ in range(n)],float);masks,member,pay,actions,term,root,rows=prepare(k,m,start,rng);w=((np.array(root)@member)>0).astype(float);best={'value':-1e99}
  for a in [a for a in range(k) if root[a]]:
   u=pay(root,a);mass=start/(u@start)
   for it in range(10):
    z,b=price(member,mass,1);cover=np.minimum(1,z@member);tau=sum(z);target=cover-w
    ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=u.reshape((1,n)),b_eq=[1],bounds=(0,None),method='highs')
    if not ans.success:break
    value=-ans.fun-tau
    if value>best['value']+1e-9:best={'value':float(value),'trial':tr,'iteration':it,'root':root,'target_action':a,'queries':list(map(float,z)),'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-8},'actions':[{'counts':q,'action':a} for q,a in actions.items()]}
    if np.linalg.norm(mass-ans.x)<1e-8:break
    mass=ans.x
  records.append(best);print(json.dumps({a:b for a,b in best.items() if a not in ('weights','actions')}),flush=True)
  Path(args.output).write_text(json.dumps({'scope':'alternating LP numerical local search only; root price candidate','parameters':vars(args),'records':records},indent=2)+'\n')
  if best['value']>1e-8:break
if __name__=='__main__':main()
