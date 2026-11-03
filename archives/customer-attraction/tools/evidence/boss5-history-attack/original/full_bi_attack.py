"""Independent ordered-history backward induction, then fixed full-policy LP."""
import argparse,itertools,json,random,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def main():
 ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=7);ps.add_argument('--players',type=int,default=5);ps.add_argument('--trials',type=int,default=100);ps.add_argument('--seed',type=int,default=2026102117);ps.add_argument('--output',required=True);args=ps.parse_args();k=args.topics;m=args.players;rng=random.Random(args.seed);masks=np.arange(1,1<<k);n=len(masks);member=np.array([[(mask>>a)&1 for mask in masks] for a in range(k)]);pay={};records=[]
 def payoff(q,a):
  if (q,a) not in pay:
   den=np.array(q)@member;pay[q,a]=np.divide(member[a],den,out=np.zeros(n),where=den>0)
  return pay[q,a]
 for tr in range(args.trials):
  mass=np.array([rng.choice([0,0,0,0,1,2,8,30]) for _ in range(n)],float)
  if tr%3==0 and k==m+2:
   mass=np.zeros(n);x=m-2
   for j in range(m):
    leaf=1<<(j+2);mass[leaf-1]+=x;mass[(2|leaf)-1]+=x;mass[((1 if j<m-1 else 3)|leaf)-1]+=1 if j<m-1 else m-1
  actions={};terminal={h:tuple(h.count(a) for a in range(k)) for h in itertools.product(range(k),repeat=m)};rows=[]
  for dep in range(m-1,-1,-1):
   for h in itertools.product(range(k),repeat=dep):
    branches=[terminal[h+(a,)] for a in range(k)];values=[payoff(q,a)@mass for a,q in enumerate(branches)];mx=max(values);chosen=rng.choice([a for a,v in enumerate(values) if v>=mx-1e-9]);actions[h]=chosen;terminal[h]=branches[chosen];now=payoff(terminal[h],chosen)
    rows.extend(payoff(branches[a],a)-now for a in range(k) if a!=chosen)
  rows=np.unique(np.array(rows),axis=0);root=terminal[()];a=actions[()];u=payoff(root,a);w=((np.array(root)@member)>0).astype(float)
  # all m-topic comparison sets, only first actual mover targeted
  best={'value':-1e99}
  for comp in itertools.combinations(range(k),min(k,m)):
   o=(member[list(comp)].sum(axis=0)>0).astype(float);target=o-w-m*u;ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
   if ans.success and -ans.fun>best['value']+1e-10:best={'value':float(-ans.fun),'trial':tr,'root':root,'target_action':a,'comparison':comp,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'certificate':{'terminal_counts':root,'actions':[{'history':h,'action':a} for h,a in actions.items()]},'unique_rows':len(rows)}
  records.append(best);print(json.dumps({a:b for a,b in best.items() if a not in ['weights','certificate']}),flush=True);Path(args.output).write_text(json.dumps({'scope':'numerical full ordered-history BI policies; root target only, all m-theme comparison sets','parameters':vars(args),'records':records},indent=2)+'\n')
  if best['value']>1e-8:break
if __name__=='__main__':main()
