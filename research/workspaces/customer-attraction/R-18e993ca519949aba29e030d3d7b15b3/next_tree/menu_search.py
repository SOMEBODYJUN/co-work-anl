from pathlib import Path
import json,itertools,sys
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]

def load(name):
 d=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
 st=d.get('strategy',d); acts={tuple(v['history']):v['action'] for v in st['actions']}
 n=max(map(len,acts))+1; p=max(acts.values())+1
 return acts,n,p

def build(acts,n,p):
 types=range(1,2**p)
 def end(h):
  while len(h)<n:h+= (acts[h],)
  return h
 def val(a,z):return np.array([int(t>>a&1)/sum(t>>b&1 for b in z) if t>>a&1 else 0 for t in types])
 rows=[]
 for h,a0 in acts.items():
  for a in range(p):rows.append(val(a0,end(h))-val(a,end(h+(a,))))
 z=end(());c=np.array([int(any(t>>a&1 for a in z)) for t in types]);
 menus=set()
 for i in range(n):
  for a in range(p):
   zz=end(z[:i]+(a,));menus.add(tuple(sorted(zz[:i]+zz[i+1:])))
 M=np.array([np.array([1/(1+sum(t>>b&1 for b in B)) for t in types]) for B in sorted(menus)])
 return np.array(rows),c,M,sorted(menus),z

def go(name,tries=200):
 acts,n,p=load(name);G,c,M,menus,z=build(acts,n,p)
 rng=np.random.default_rng(18)
 queries=[np.ones(p)/p,*np.eye(p),*[rng.dirichlet(np.ones(p)*a) for a in [.1,.3,1,3] for _ in range(tries//4)]]
 best=(-1,None)
 for q in queries:
  qt=np.array([sum(q[a] for a in range(p) if t>>a&1) for t in range(1,2**p)])
  A=np.vstack([np.column_stack([-G,np.zeros(len(G))]),np.column_stack([-M*qt,np.ones(len(M))])])
  res=linprog(np.r_[np.zeros(len(c)),-1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[c,0]],b_eq=[1],bounds=(0,None),method='highs')
  if res.success and n*res.x[-1]>best[0]+1e-9:
   best=(n*res.x[-1],(q,res.x))
 print(name,'n,p=',n,p,'path',z,'menus',len(menus),'best n v_menu/W=',best[0])
 if best[0]>1.0000001:
  q,x=best[1]
  out={'name':name,'n':n,'p':p,'menus':menus,'q':q.tolist(),'weights':[(i+1,v) for i,v in enumerate(x[:-1]) if v>1e-9],'value':x[-1]}
  Path(__file__).with_name(name+'_menu_candidate.json').write_text(json.dumps(out,indent=2))
 return best
if __name__=='__main__':
 for name in sys.argv[1:] or ['individual_security_failure','root_stationary_kernel','root_tax_failure','worst_cce_welfare_failure','empirical_iid_kernel','local_security_increment']:
  go(name)
