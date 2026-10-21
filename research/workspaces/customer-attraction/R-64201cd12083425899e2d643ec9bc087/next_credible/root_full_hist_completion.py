"""Root refinement with genuine five-index reply histograms and shared root menus.
Finite-column necessary relaxation; no full SPE or universal bound is asserted.
"""
from pathlib import Path
from itertools import product
import json,sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE=Path(__file__).parent
# Reuse exact same 1310 definitions and their primitive (a,t,v) coefficients.
ns={'__file__':str(HERE/'root_menu_completion.py')};src=(HERE/'root_menu_completion.py').read_text();exec(compile(src.split('# Maximize a common margin')[0],'<root menu row definitions>','exec'),ns)
old=ns['old'];d=ns['d'];primitive=ns['variables'];base=ns['A'];names=ns['names'];spec=ns['spec'];mass=ns['masses'];cellid={(a,t,tuple(v)):i for i,(a,t,v) in enumerate(primitive)}
cols=[];seen=set()
def add(a,h):
 key=(a,tuple((t,tuple(v),n) for t,v,n in h if n))
 if key not in seen:seen.add(key);cols.append((a,h))
for a in range(len(old)):
 for v0,v1 in product(product((0,1),repeat=4),repeat=2):
  h=[]
  if d[a]<5:h.append((0,v0,int(5-d[a])))
  if d[a]>0:h.append((1,v1,int(d[a])))
  add(a,h)
# Include every coupling supported by the previous strict refinement.
for a,h in json.loads((HERE/'couple_root_refinement.json').read_text())['column_specs']:add(a,h)

def off(h,j,k):
 count=sum(n*v[k] for t,v,n in h);z=0.
 for t,v,n in h:
  total=t+sum(v);den=t+sum(v[:j])+4-j;u=v[j]/total if v[j] else 0.;z+=n*(4*u-(count-v[k])/den)/5
 return z
rr=[];cc=[];val=[]
for ci,(a,h) in enumerate(cols):
 for t,v,n in h:rr.append(cellid[a,t,tuple(v)]);cc.append(ci);val.append(n/5)
P=coo_matrix((val,(rr,cc)),shape=(len(primitive),len(cols))).tocsr()
B=(P.T@base.T).T
O=np.array([[off(h,j,k) for a,h in cols] for j in range(4) for k in range(4)])
A=np.r_[B,O];n=len(cols);E=np.zeros((len(old),n))
for ci,(a,h) in enumerate(cols):E[a,ci]=1.
r=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=np.c_[E,np.zeros(len(old))],b_eq=list(map(float,mass)),bounds=[(0,None)]*n+[(None,None)],method='highs')
report={'scope':'finite-column necessary full root-reply histogram completion of 2396 LP point, not complete SPE','columns':n,'rows':len(A),'equalities':len(old),'status':r.message,'margin':float(r.x[-1]) if r.success else None,'row_names':names+[f'root:{j}:off-menu:{k}' for j in range(4) for k in range(4)],'row_specs':spec+[('off',j,k) for j in range(4) for k in range(4)],'column_specs':cols,'point':r.x[:-1].tolist() if r.success else None,'dual_rows':(-r.ineqlin.marginals).tolist() if r.success else None,'dual_equalities':r.eqlin.marginals.tolist() if r.success else None}
(HERE/'root_full_hist_completion.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ('scope','columns','rows','equalities','status','margin')},indent=2))
