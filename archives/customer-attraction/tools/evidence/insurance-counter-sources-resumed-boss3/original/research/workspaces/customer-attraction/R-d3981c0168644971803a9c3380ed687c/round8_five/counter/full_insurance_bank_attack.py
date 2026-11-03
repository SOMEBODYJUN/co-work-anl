"""Targeted full-tree attack: opt-private omissions, outside-opt K5 insurance.
Every target branch is AABBC. Banking client belongs to any nonempty subset of
A/B/C and exactly one T_i; X_i belongs to T_i and four outside-opt pair insurers.
Numerical policy iteration selects candidates only. No float is a proof.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import json,time,argparse
P=18;M=5;PATH=(0,0,1,1,2)
EDGES=list(combinations(range(5),2))
TYPES=[tuple(a for a in range(3) if S>>a&1)+(3+j,) for S in range(1,8) for j in range(5)]+[(3+j,)+tuple(8+k for k,e in enumerate(EDGES) if j in e) for j in range(5)]
def counts(p,total):
 if p==1:yield (total,);return
 for j in range(total+1):
  for t in counts(p-1,total-j):yield (j,)+t
def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
class Attack:
 def __init__(self):
  self.I=np.array([[a in typ for a in range(P)] for typ in TYPES],float)
  self.Q=tuple(counts(P,M));self.Qi={q:i for i,q in enumerate(self.Q)}
  den=np.array(self.Q)@self.I.T
  self.pay=np.divide(self.I.T[None,:,:],den[:,None,:],out=np.zeros((len(self.Q),P,len(TYPES))),where=den[:,None,:]>0)
  self.pay*=(np.array(self.Q)>0)[:,:,None]
  self.cover=(den>0).astype(float);self.states=tuple(q for d in range(M,-1,-1) for q in counts(P,d))
  self.root=(0,)*P;self.target=self.Qi[tuple(PATH.count(a) for a in range(P))]
 def solve(self,x):
  self.U=self.pay@x;self.W=self.cover@x;self.R={};self.floor={}
  for q in self.states:
   if sum(q)==M:self.R[q]=np.array([self.Qi[q]],int);continue
   ch=[self.R[inc(q,a)] for a in range(P)]
   f=max(self.U[c,a].min() for a,c in enumerate(ch));self.floor[q]=f
   self.R[q]=np.unique(np.concatenate([c[self.U[c,a]>=f-1e-9] for a,c in enumerate(ch)]))
  return self.target in self.R[self.root]
 def policy_rows(self):
  actions={};terms={};keys=set()
  def go(h,q,t):
   terms[h]=t
   if len(h)==M:return
   candidates=[a for a in range(P) if t in self.R[inc(q,a)] and self.U[t,a]>=self.floor[q]-1e-8]
   a=PATH[len(h)] if h==PATH[:len(h)] else candidates[0]
   if a not in candidates:raise ValueError('target ordered path infeasible')
   actions[h]=a
   for b in range(P):
    if b==a:dest=t
    else:
     menu=self.R[inc(q,b)];v=self.U[menu,b];dest=int(menu[np.argmin(v)])
    go(h+(b,),inc(q,b),dest)
    keys.add((t,a,dest,b))
  go((),self.root,self.target)
  rows=np.unique(np.array([self.pay[t,a]-self.pay[d,b] for t,a,d,b in keys]),axis=0)
  return rows,actions
 def optimize(self,rows):
  return linprog(-np.ones(len(TYPES)),A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[self.cover[self.target]],b_eq=[1],bounds=(0,None),method='highs')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rounds',type=int,default=3);ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));args=ap.parse_args()
 start=time.time();a=Attack();x=np.zeros(len(TYPES));
 for S,mass in [(1,2),(2,2),(4,1)]:
  for j in range(5):x[(S-1)*5+j]=mass/5
 x[-5:]=.4
 log=[];best=None
 for it in range(args.rounds):
  feasible=a.solve(x)
  print(json.dumps({'iteration':it,'target_feasible':bool(feasible),'root_outcomes':len(a.R[a.root]),'elapsed':time.time()-start}),flush=True)
  if not feasible:break
  rows,actions=a.policy_rows();out=a.optimize(rows)
  rec={'iteration':it,'rows':len(rows),'target_feasible_float':bool(feasible),'LP_success':bool(out.success),'LP_ratio_float':float(-out.fun) if out.success else None,'elapsed':time.time()-start}
  log.append(rec);print(json.dumps(rec),flush=True)
  if not out.success:break
  x=out.x;best={'point':[str(F(float(v)).limit_denominator(10**7)) for v in x], 'types':TYPES, 'path':PATH,'ratio_float':float(-out.fun),'rows':len(rows)}
  if -out.fun>2+1e-6:
   best['full_strategy']=[(h,v) for h,v in actions.items()]
   break
 args.output.write_text(json.dumps({'scope':'Designed opt-private / outside-opt K5 pair insurance complete SPE policy attack; numerical guide only','universal_claim':False,'log':log,'best_candidate':best},indent=2)+'\n')
