"""Numerical legal-background version: old players fixed, no old incentives assumed."""
import argparse,itertools,json,random,runpy
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
D=runpy.run_path('research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity/count_policy_attack.py');states=D['states']

def prep(k,s,r,mass,rng):
 masks=np.arange(1,1<<k);member=np.array([[(b>>a)&1 for b in masks] for a in range(k)]);pay={}
 # diverse repeated or distinct fixed backgrounds
 old=[rng.randrange(k) for _ in range(s)];bg=tuple(old.count(a) for a in range(k));m=s+r
 def payoff(q,a):
  if (q,a) not in pay:
   den=np.array(q)@member;pay[q,a]=np.divide(member[a],den,out=np.zeros(len(masks)),where=den>0)
  return pay[q,a]
 terminal={tuple(a+b for a,b in zip(q,bg)):tuple(a+b for a,b in zip(q,bg)) for q in states(k,r)};actions={};rows=[]
 for dep in range(r-1,-1,-1):
  for rem in states(k,dep):
   q=tuple(a+b for a,b in zip(rem,bg));branches=[]
   for a in range(k):
    child=list(q);child[a]+=1;branches.append(terminal[tuple(child)])
   vals=[payoff(t,a)@mass for a,t in enumerate(branches)];mx=max(vals);chosen=rng.choice([a for a,v in enumerate(vals) if v>=mx-1e-10]);actions[q]=chosen;terminal[q]=branches[chosen]
   for a in range(k):
    if a!=chosen:rows.append(payoff(branches[a],a)-payoff(terminal[q],chosen))
 root=terminal[bg];a=actions[bg];u=payoff(root,a);w=((np.array(root)@member)>0).astype(float)
 return masks,member,np.array(rows),root,a,u,w,bg,actions

def main():
 ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=6);ps.add_argument('--old',type=int,default=1);ps.add_argument('--future',type=int,default=4);ps.add_argument('--trials',type=int,default=100);ps.add_argument('--seed',type=int,default=2026102114);ps.add_argument('--output',required=True);args=ps.parse_args();k=args.topics;s=args.old;r=args.future;m=s+r;rng=random.Random(args.seed);records=[]
 for tr in range(args.trials):
  n=(1<<k)-1;mass=np.array([rng.choice([0,0,0,1,2,5,10,30]) for _ in range(n)],float)
  masks,member,rows,root,a,u,w,bg,actions=prep(k,s,r,mass,rng);best={'value':-1e99}
  for comp in itertools.combinations(range(k),min(m,k)):
   o=(member[list(comp)].sum(axis=0)>0).astype(float);target=o-w-m*u
   ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
   if ans.success and -ans.fun>best['value']+1e-10:best={'value':float(-ans.fun),'comparison':comp,'target_action':a,'root':root,'background':bg,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'actions':[{'counts':q,'action':a} for q,a in actions.items()]}
  best['trial']=tr;records.append(best);print(json.dumps({a:b for a,b in best.items() if a not in ('weights','actions')}),flush=True)
  Path(args.output).write_text(json.dumps({'scope':'floating legal-background SPE cones; old players not optimized','parameters':vars(args),'records':records},indent=2)+'\n')
  if best['value']>1e-8:break
if __name__=='__main__':main()
