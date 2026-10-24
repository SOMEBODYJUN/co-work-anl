"""Counterexample probe for exact general LAST: m v_2(actual pre-last b)<=W.
This is not a proof of LAST or Q-CAG-HALF. Static games use independent query.
"""
import json, sys
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, ExactSPESolver

def matrix(inst,b):
    k=inst.topic_count
    return [[sum((Fraction(c.multiplicity,1+sum(b[t] for t in c.topics)+(a in c.topics)) for c in inst.customers if t in c.topics),Fraction()) for a in range(k)] for t in range(k)]
def value(inst,b):
    mat=matrix(inst,b); k=inst.topic_count
    arr=np.array(mat,float)
    res=linprog([0.]*k+[1.],A_ub=np.column_stack([arr,-np.ones(k)]),b_ub=np.zeros(k),A_eq=[[1.]*k+[0.]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    return res.fun,res,mat

def action_map(j):
    if isinstance(j,dict):
      if 'actions' in j: return {tuple(x['history']):x['action'] for x in j['actions']}
      for v in j.values():
       ans=action_map(v)
       if ans:return ans
    return None

if __name__=='__main__':
  root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
  for p in (root/'examples/customer_attraction').glob('*.json'):
    cp=root/'evidence/certificates/customer_attraction'/p.name
    if not cp.exists():continue
    try:
      inst=Instance.from_dict(json.loads(p.read_text()))
      acts=action_map(json.loads(cp.read_text()))
      if acts is None:continue
      h=()
      while len(h)<inst.players:h=h+(acts[h],)
      b=inst.counts(h[:-1]);w=inst.welfare(inst.counts(h))
      v,res,mat=value(inst,b)
      print(p.name,h,'W',w,'mM',inst.players*v,'gap',w-inst.players*v,flush=True)
    except (ValueError,KeyError,TypeError) as ex: print(p.name,'skip',type(ex).__name__)
