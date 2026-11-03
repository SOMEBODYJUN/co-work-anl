"""A targeted ADM falsification attempt: strict full-history IC would make all tail SPE unique.
The LP explores one existing complete strategy cone, not any fixed-size theorem.
"""
import sys,json
from pathlib import Path
from itertools import product
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent;ROOT=P.parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

ins=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction/root_tax_failure.json').read_text()))
q=ins.topic_count;m=ins.players;path=(2,3,0,0)
s=ExactSPESolver(ins);cert=s.certificate(on_path=path);acts=cert.actions
masks=list(range(1,1<<q));inc=np.array([[bool(B>>a&1) for a in range(q)] for B in masks],dtype=float)
terms={}
def term(h):
 if h in terms:return terms[h]
 if len(h)==m:
  r=np.bincount(h,minlength=q);terms[h]=r;return r
 r=term(h+(acts[h],));terms[h]=r;return r

def payoff(a,c):
 d=inc@c
 return np.divide(inc[:,a],d,out=np.zeros(len(masks)),where=d>0)
def insertion(c):return (inc/(1+inc@c)[:,None]).T
C=[]
for h,a in acts.items():
 for b in range(q):
  if b!=a:C.append(payoff(a,term(h))-payoff(b,term(h+(b,))))
C=np.unique(np.array(C),axis=0)
z=term(());covered=(inc@z>0).astype(float)
menus=np.unique(np.array([term(path[:i]+(a,)) for i in range(m) for a in range(q)]),axis=0)
K=np.array([insertion(c) for c in menus]) # menu,query,type
# First check whether this cone can strictly implement the full strategy.
n=len(masks)
res=linprog([0]*n+[-1],A_ub=np.column_stack([-C,np.ones(len(C))]),b_ub=np.zeros(len(C)),A_eq=[list(covered)+[0]],b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
assert res.success
strict=res.x[-1]
records=[]
# A positive strict margin rules out every alternate tail SPE by backward induction.
if strict>=-1e-9:
 for support in [(a,b) for a in range(q) for b in range(a+1,q)]+[tuple(range(q))]:
  p=np.zeros(q);p[list(support)]=1/len(support)
  for it in range(8):
   H=np.einsum('j,mjn->mn',p,K)
   A=np.vstack([np.column_stack([-C,np.zeros(len(C))]),np.column_stack([-H,np.ones(len(H))])]);b=np.r_[np.full(len(C),-min(strict/100,1e-6)),np.full(len(H),-1/m)]
   r=linprog([0]*n+[-1],A_ub=A,b_ub=b,A_eq=[list(covered)+[0]],b_eq=[1],bounds=[(0,None)]*n+[(None,None)],method='highs')
   if not r.success:break
   w=r.x[:-1];KM=np.einsum('mjn,n->mj',K,w)
   pr=linprog([0]*q+[-1],A_ub=np.column_stack([-KM,np.ones(len(menus))]),b_ub=np.zeros(len(menus)),A_eq=[[1]*q+[0]],b_eq=[1],bounds=[(0,None)]*q+[(None,None)],method='highs')
   p=pr.x[:-1];gap=pr.x[-1]-1/m
   records.append(dict(support=support,iteration=it,gap=gap,p=p.tolist(),w=w.tolist(),strict_margin=float(min(C@w))))
   if gap>1e-6:break
  if records and records[-1]['gap']>1e-6:break
out=dict(scope=__doc__,instance_source='examples/customer_attraction/root_tax_failure.json',path=path,topic_count=q,players=m,IC_rows=len(C),strict_margin_max=strict,records=sorted(records,key=lambda x:x['gap'],reverse=True)[:5])
(P/'strict_cone_discovery.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
