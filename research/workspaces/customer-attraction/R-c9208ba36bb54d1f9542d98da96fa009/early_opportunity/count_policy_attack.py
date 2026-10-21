"""Numerical attacks on OPT-W <= m times each used-theme payoff.
Count-dependent complete policies are a legal subset, not all full-history SPE.
"""
import argparse,itertools,json,math,random,time
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def states(k,n):
 if k==1: yield (n,);return
 for v in range(n+1):
  for t in states(k-1,n-v): yield (v,)+t


def prepare(k,m,mass,rng):
 masks=np.arange(1,1<<k)
 member=np.array([[(b>>a)&1 for b in masks] for a in range(k)])
 @lru_cache(None)
 def pay(q,a):
  den=np.array(q)@member
  return np.divide(member[a],den,out=np.zeros(len(masks)),where=den>0)
 actions={};term={q:q for q in states(k,m)};rows=[]
 for dep in range(m-1,-1,-1):
  for q in states(k,dep):
   branches=[]
   for a in range(k):
    child=list(q);child[a]+=1;child=tuple(child)
    branches.append(term[child])
   values=[pay(t,a)@mass for a,t in enumerate(branches)]
   mx=max(values);choice=rng.choice([a for a,v in enumerate(values) if v>=mx-1e-10])
   actions[q]=choice;term[q]=branches[choice]
   chosen=pay(term[q],choice)
   rows.extend(pay(branches[a],a)-chosen for a in range(k) if a!=choice)
 zero=(0,)*k;root=term[zero]
 return masks,member,pay,actions,term,root,np.array(rows)


def attack(k,m,trial,rng):
 n=(1<<k)-1
 # Diverse sparse, dense and almost-exchangeable starts.
 if trial%3==0:
  mass=np.array([rng.choice([0,0,0,1,2,3,8,20]) for _ in range(n)],float)
 elif trial%3==1:
  mass=np.array([rng.expovariate(1) if rng.random()<.3 else 0 for _ in range(n)])
 else:
  mass=np.array([1+rng.random()*.05 for _ in range(n)])
 masks,member,pay,actions,term,root,rows=prepare(k,m,mass,rng)
 w=((np.array(root)@member)>0).astype(float)
 support=tuple(a for a in range(k) if root[a])
 best={'value':-math.inf}
 for comp in itertools.combinations(range(k),min(m,k)):
  o=(member[list(comp)].sum(axis=0)>0).astype(float)
  for a in support:
   target=o-w-m*pay(root,a)
   ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
   if ans.success and -ans.fun>best['value']+1e-10:
    best={'value':float(-ans.fun),'comparison':comp,'target_action':a,'root':root,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'actions':[{'counts':q,'action':a} for q,a in actions.items()]}
 return best


def main():
 p=argparse.ArgumentParser();p.add_argument('--topics',type=int,default=6);p.add_argument('--players',type=int,default=5);p.add_argument('--trials',type=int,default=40);p.add_argument('--seed',type=int,default=20261021);p.add_argument('--output',required=True);args=p.parse_args()
 rng=random.Random(args.seed);records=[];start=time.time()
 for trial in range(args.trials):
  rec=attack(args.topics,args.players,trial,rng);rec['trial']=trial;records.append(rec)
  print(json.dumps({k:v for k,v in rec.items() if k not in ['weights','actions']}),flush=True)
  Path(args.output).write_text(json.dumps({'scope':'floating LP, legal complete count policies only','parameters':vars(args),'elapsed':time.time()-start,'records':records},indent=2)+'\n')
  if rec['value']>1e-8: break
if __name__=='__main__':main()
