import json,itertools,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def counts(n,k):
 if k==1: yield (n,); return
 for j in range(n+1):
  for q in counts(n-j,k-1): yield (j,)+q

def value(inst,support):
 bg=list(counts(inst.players-1,len(support)))
 M=np.array([[sum(t.multiplicity/(1+sum(q[j] for j,a in enumerate(support) if a in t.topics)) for t in inst.customers if a in t.topics) for q in bg] for a in range(inst.topic_count)])
 c=np.r_[np.zeros(len(bg)),1.]
 res=linprog(c,A_ub=np.c_[M,-np.ones(inst.topic_count)],b_ub=np.zeros(inst.topic_count),A_eq=[np.r_[np.ones(len(bg)),0]],b_eq=[1],bounds=[(0,None)]*len(bg)+[(None,None)],method='highs')
 return res.fun,[(bg[j],float(v)) for j,v in enumerate(res.x[:-1]) if v>1e-8]

if __name__=='__main__':
 for p in Path('examples/customer_attraction').glob('*.json'):
  d=json.loads(p.read_text()); inst=Instance.from_dict(d)
  if inst.topic_count>7 or inst.players>5: continue
  s=ExactSPESolver(inst); outcomes=s.outcomes()
  worst=None
  for q in outcomes:
   sup=tuple(a for a,v in enumerate(q) if v)
   v,Q=value(inst,sup); W=inst.welfare(q); gap=inst.players*v-W
   if worst is None or gap>worst['gap']:worst=dict(name=p.stem,counts=q,gap=gap,W=W,cap=v,Q=Q)
  print(json.dumps(worst),flush=True)
