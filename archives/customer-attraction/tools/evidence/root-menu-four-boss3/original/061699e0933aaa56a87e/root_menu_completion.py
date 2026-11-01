"""Necessary root-menu completion of the frozen 2396-row obstruction.
Each variable refines a frozen atom by T_i membership and four actual root replies.
Only necessary averaged true-node inequalities are imposed; feasibility is not SPE.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
import json,sys
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent
old=json.loads((HERE/'enhanced_2396_exact_obstruction.json').read_text())['atom_masses']
from offdiagonal_probe import types,quads,paths,labels
masses=[F(a['mass']) for a in old]
bits=np.array([list(map(int,a['bits'])) for a in old]);weights=np.array(list(map(float,masses)))
menus=[(n,1,bits[:,i]) for i,n in enumerate(labels)]
menus.append(('T',5,np.array([sum(n*t[0] for n,t in zip(a['AB_hist'],types)) for a in old])))
for j in range(3):menus.append(('L'+str(j),5,np.array([a['menus_lh'][j][0] for a in old])))
for tag,key,ts,ns in [('AB','AB_hist',types,'XY'),('AE','AE_hist',types,'XY'),('S','second_hist',quads,'UVW')]:
 for po,nm in enumerate(ns,1):menus.append((tag+':'+nm,5,np.array([sum(n*t[po] for n,t in zip(a[key],ts)) for a in old])))
d=menus[10][2]
variables=[(a,t,v) for a in range(len(old)) for t in (0,1) if (d[a] if t else 5-d[a]) for v in product((0,1),repeat=4)]
ai=np.array([a for a,t,v in variables]);tt=np.array([t for a,t,v in variables]);vv=np.array([v for a,t,v in variables]);total=tt+vv.sum(axis=1)
pay=vv/np.maximum(total[:,None],1);root=tt/np.maximum(total,1)
rows=[];names=[];spec=[]
def add(n,r,s):
 if np.any(np.abs(r)>1e-15):names.append(n);rows.append(r);spec.append(s)
# Constant old node values are embedded as same fixed mass per variable.
pathidx={n:[labels.index(c) for c in p] for n,p in paths.items()}
root_actual=np.where(bits[:,0],1/np.maximum(bits[:,:5].sum(axis=1),1),0.)
add('root:exact-opt',root_actual[ai]-root,('root',))
for j in range(4):
 den=tt+vv[:,:j].sum(axis=1)+4-j
 for nm,size,count in menus:add(f'rootreply:{j}:menu:{nm}',pay[:,j]-count[ai]/size/den,('menu',j,nm))
 for pos in range(5):
  val=tt if pos==0 else vv[:,pos-1]
  add(f'rootreply:{j}:own:{pos}',pay[:,j]-val/den,('own',j,pos))
for pn,idx in pathidx.items():
 for j in range({'actual':0,'second':2,'third':3}[pn],5):
  p=bits[:,idx[:j]].sum(axis=1);load=bits[:,idx].sum(axis=1);u=bits[:,idx[j]]/np.maximum(load,1)
  for k in range(4):add(f'{pn}:{j}:new-root-menu:{k}',u[ai]-vv[:,k]/(p[ai]+5-j),('reverse',pn,j,k))
# True root branches leave four, three, two optimizing suffix players.
for r,beta in [(4,F(1499,750)),(3,F(5,3))]:
 start=4-r;bg=tt+vv[:,:start].sum(axis=1);R=pay[:,start:].sum(axis=1)
 for ids in combinations_with_replacement(range(10),r):
  load=bits[:,ids].sum(axis=1)[ai];cmp=load/np.maximum(bg+load,1)
  add(f'root:r{r}:profit:'+''.join(labels[i] for i in ids),float(beta)*R-cmp,('profit',r,ids))
bg=tt+vv[:,:2].sum(axis=1);H=pay[:,2:].sum(axis=1)+vv[:,2]/((bg+1)*(bg+2))
for ia,ib in combinations_with_replacement(range(len(menus)),2):
 na,sa,ca=menus[ia];nb,sb,cb=menus[ib];x=ca[ai]/sa;y=cb[ai]/sb
 cmp=(x+y)/(bg+1)-2*x*y/((bg+1)*(bg+2))
 add('root:r2:tax:'+na+'|'+nb,H-cmp,('tax',ia,ib))
# Every old atom's t=0,1 masses are fixed, not chosen by the optimizer.
E=[];rhs=[];groups=[]
for a in range(len(old)):
 for t in (0,1):
  n=int(d[a] if t else 5-d[a])
  if not n:continue
  E.append(np.array([int(aa==a and bt==t) for aa,bt,v in variables]));rhs.append(float(masses[a]*n/5));groups.append((a,t))
A=np.array(rows);E=np.array(E);n=len(variables)
# Maximize a common margin; t<0 certifies infeasibility of this necessary relaxation
# only after exact primal/dual recovery. Floats are proposals.
r=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=np.c_[E,np.zeros(len(E))],b_eq=rhs,bounds=[(0,None)]*n+[(None,None)],method='highs')
report={'scope':'necessary averaged true root-optimal-deviation menu completion of 2396 LP point, not a complete SPE','variables':n,'inequalities':len(rows),'equalities':len(E),'status':r.message,'margin':float(r.x[-1]) if r.success else None,'negative_margin_is_only_floating_evidence':True,'row_names':names,'row_specs':spec,'variables_spec':variables,'groups':groups,'point':r.x[:-1].tolist() if r.success else None,'dual_rows':(-r.ineqlin.marginals).tolist() if r.success else None,'dual_equalities':r.eqlin.marginals.tolist() if r.success else None}
(HERE/'root_menu_completion.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ('scope','variables','inequalities','equalities','status','margin')},indent=2))
