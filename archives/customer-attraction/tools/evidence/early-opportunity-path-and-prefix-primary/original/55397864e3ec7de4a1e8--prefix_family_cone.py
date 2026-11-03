"""All-interest reweighting of an exact n-player prefix-debt family policy."""
import argparse,itertools,json,runpy
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
D=runpy.run_path('research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity/count_policy_attack.py');states=D['states']
def main():
 ps=argparse.ArgumentParser();ps.add_argument('--players',type=int,default=5);ps.add_argument('--coefficient',type=float);ps.add_argument('--output',required=True);args=ps.parse_args();m=args.players;k=m+2;x=m-2;masks=np.arange(1,1<<k);n=len(masks);member=np.array([[(mask>>a)&1 for mask in masks] for a in range(k)]);mass=np.zeros(n)
 for j in range(m):
  leaf=1<<(j+2);mass[leaf-1]+=x;mass[(2|leaf)-1]+=x
  if j<m-1:mass[(1|leaf)-1]+=1
  else:mass[(3|leaf)-1]+=m-1
 pay={}
 def payoff(q,a):
  if (q,a) not in pay:
   den=np.array(q)@member;pay[q,a]=np.divide(member[a],den,out=np.zeros(n),where=den>0)
  return pay[q,a]
 terminal={q:q for q in states(k,m)};actions={};rows=[]
 for dep in range(m-1,-1,-1):
  for q in states(k,dep):
   branches=[]
   for a in range(k):
    child=list(q);child[a]+=1;branches.append(terminal[tuple(child)])
   if dep==m-1:
    values=[payoff(t,a)@mass for a,t in enumerate(branches)];mx=max(values);chosen=next(a for a in [1,0]+list(range(2,k)) if values[a]>=mx-1e-9)
   else:chosen=0 if sum(q)==q[1] else 1
   actions[q]=chosen;terminal[q]=branches[chosen];now=payoff(terminal[q],chosen)
   rows.extend(payoff(branches[a],a)-now for a in range(k) if a!=chosen)
 rows=np.array(rows);maxbase=float(np.max(rows@mass));assert maxbase<1e-7,maxbase
 root=terminal[(0,)*k];w=((np.array(root)@member)>0).astype(float);best={'value':-1e99};coef=m if args.coefficient is None else args.coefficient
 for comp in itertools.combinations(range(k),m):
  o=(member[list(comp)].sum(axis=0)>0).astype(float)
  for a in [0,1]:
   target=o-w-coef*payoff(root,a);ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
   if ans.success and -ans.fun>best['value']+1e-10:best={'value':float(-ans.fun),'comparison':comp,'target_action':a,'root':root,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'actions':[{'counts':q,'action':a} for q,a in actions.items()]}
 best.update(m=m,k=k,coefficient=coef,max_base_incentive_violation=maxbase,scope='numerical full legal policy cone only; base policy exact known family');Path(args.output).write_text(json.dumps(best,indent=2)+'\n');print(json.dumps({a:b for a,b in best.items() if a not in ['weights','actions']}))
if __name__=='__main__':main()
