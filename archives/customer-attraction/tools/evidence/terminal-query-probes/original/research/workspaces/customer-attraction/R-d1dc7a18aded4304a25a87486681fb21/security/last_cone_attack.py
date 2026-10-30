"""Candidate-only fixed full SPE-cone alternating LP for general LAST.
Exact target: m min_Q max_T E_Q K_b(T,A) > actual W.
Negative output is not general evidence. Float LP only proposes candidates.
"""
from pathlib import Path
import sys,json
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,integer_clones,instance_from_clones,independently_verify,dot
from probe_last import Instance,action_map,value

def prelast(cone):
 h=()
 while len(h)<cone.players:h+=(cone.actions[h],)
 return h,tuple(h[:-1].count(a) for a in range(cone.topics))
def tensor(cone,b):
 k=cone.topics
 return np.array([[[1/(1+sum(b[j] for j in range(k) if mask&(1<<j))+bool(mask&(1<<a))) if mask&(1<<t) else 0 for mask in range(1,1<<k)] for a in range(k)] for t in range(k)])
def row_opt(K,w):
 mat=np.einsum('tan,n->ta',K,w);k=len(mat)
 res=linprog([0.]*k+[-1.],A_ub=np.column_stack([-mat.T,np.ones(k)]),b_ub=np.zeros(k),A_eq=[[1.]*k+[0.]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 return res.x[:-1],res.x[-1]
def weights_opt(cone,K,p):
 k=cone.topics;n=K.shape[2]
 C=cone.players*np.einsum('t,tan->an',p,K)
 rows=np.vstack([np.column_stack([-cone.matrix,np.zeros(len(cone.rows))]),np.column_stack([-C,np.ones(k)])])
 res=linprog([0.]*n+[-1.],A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[list(map(float,cone.welfare))+[0.]],b_eq=[1.],bounds=[(0,None)]*n+[(None,None)],method='highs')
 if not res.success:return None
 return res.x[:-1],res.x[-1]
def run():
 rng=np.random.default_rng(942137)
 best=0
 for path in (ROOT/'examples/customer_attraction').glob('*.json'):
  cp=ROOT/'evidence/certificates/customer_attraction'/path.name
  if not cp.exists():continue
  try:
   inst=Instance.from_dict(json.loads(path.read_text()));acts=action_map(json.loads(cp.read_text()))
   if inst.topic_count>7 or acts is None:continue
   cone=StrategyCone(inst.topic_count,inst.players,acts);h,b=prelast(cone);K=tensor(cone,b)
  except (KeyError,ValueError,TypeError):continue
  n=K.shape[2];orig=np.zeros(n)
  for c in inst.customers:
   mask=sum(1<<j for j in c.topics)
   if mask:orig[mask-1]+=c.multiplicity
  orig/=sum(orig*np.array(cone.welfare,float))
  local=0
  for attempt in range(9):
   p,_=row_opt(K,orig) if attempt==0 else (rng.dirichlet(np.ones(cone.topics)),None)
   for it in range(12):
    res=weights_opt(cone,K,p)
    if res is None:break
    w,v=res;p,v2=row_opt(K,w)
    local=max(local,cone.players*v2)
    if cone.players*v2>1+1e-7:
     exact=tuple(Fraction(float(x)).limit_denominator(10**8) for x in w)
     if not cone.verify(exact) or dot(cone.welfare,exact)!=1:exact=cone.recover_vertex(w)
     if exact is None:print('RECOVERY FAILED',path.name,cone.players*v2,flush=True);break
     clones=integer_clones(exact);newinst=instance_from_clones(cone.topics,cone.players,clones)
     vv,rr,mm=value(newinst,b);W=newinst.welfare(cone.root)
     if cone.players*vv>W+1e-7 and independently_verify(cone,clones):
      out={'candidate':'LAST','source':path.name,'path':h,'clones':clones,'instance':newinst.to_dict(),'actions':[{'history':x,'action':a} for x,a in sorted(cone.actions.items())],'p':p.tolist(),'mM':cone.players*vv,'W':W}
      Path(__file__).with_name('last_candidate.json').write_text(json.dumps(out,indent=2)+'\n')
      print('CANDIDATE',path.name,'mM/W',cone.players*vv/W,flush=True);return
    if abs(v-cone.players*v2)<1e-9:break
  best=max(best,local)
  print(path.name,'max mM/W',round(local,10),flush=True)
 print('NO CANDIDATE; no general inference',best)
if __name__=='__main__':run()
