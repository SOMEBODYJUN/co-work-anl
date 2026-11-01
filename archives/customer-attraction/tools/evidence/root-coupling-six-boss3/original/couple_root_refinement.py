"""All couplings supported by one fixed 92-cell root refinement.
Each column is a full five-index root-reply histogram for one old atom.
Infeasibility excludes this particular refinement only, not all refinements.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import numpy as np,json
from scipy.optimize import linprog
HERE=Path(__file__).parent
old=json.loads((HERE/'enhanced_2396_exact_obstruction.json').read_text())['atom_masses'];cells=json.loads((HERE/'root_menu_completion_exact.json').read_text())['positive_refinements']
from offdiagonal_probe import types
d=[sum(n*t for n,(t,x,y) in zip(a['AB_hist'],types)) for a in old]
def compositions(n,k):
 if k==0:
  if n==0:yield ()
 elif k==1:yield(n,)
 else:
  for i in range(n+1):
   for tail in compositions(n-i,k-1):yield(i,)+tail
columns=[];patterns={}
for a in range(len(old)):
 pats={t:[tuple(r['replies']) for r in cells if r['atom']==a and r['t']==t] for t in (0,1)};patterns[a]=pats
 for c0,c1 in product(compositions(5-d[a],len(pats[0])),compositions(d[a],len(pats[1]))):
  hist=[(t,v,int(n)) for t,c in ((0,c0),(1,c1)) for v,n in zip(pats[t],c) if n]
  columns.append((a,hist))
def offrow(hist,j,k):
 count=sum(n*v[k] for t,v,n in hist);z=F()
 for t,v,n in hist:
  total=t+sum(v);den=t+sum(v[:j])+4-j;u=F(v[j],total) if v[j] else F()
  z+=n*(4*u-F(count-v[k],den))/5
 return z
A=np.array([[float(offrow(h,j,k)) for a,h in columns] for j in range(4) for k in range(4)])
E=[];b=[]
for r in cells:
 E.append([sum(n for t,v,n in h if t==r['t'] and tuple(v)==tuple(r['replies']))/5 if a==r['atom'] else 0. for a,h in columns]);b.append(float(F(r['mass'])))
E=np.array(E);n=len(columns)
r=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-A,np.ones(16)],b_ub=np.zeros(16),A_eq=np.c_[E,np.zeros(len(E))],b_eq=b,bounds=[(0,None)]*n+[(None,None)],method='highs')
report={'scope':'all couplings with the support and marginals of the particular 92-cell root refinement only; no SPE claim','columns':n,'equalities':len(E),'status':r.message,'margin':float(r.x[-1]) if r.success else None,'point':r.x[:-1].tolist() if r.success else None,'column_specs':columns,'dual_rows':(-r.ineqlin.marginals).tolist() if r.success else None,'dual_equalities':r.eqlin.marginals.tolist() if r.success else None}
(HERE/'couple_root_refinement.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ('scope','columns','equalities','status','margin')},indent=2))
