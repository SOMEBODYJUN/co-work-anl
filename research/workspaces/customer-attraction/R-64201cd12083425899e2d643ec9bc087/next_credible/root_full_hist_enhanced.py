"""Additional old/new root menu cross-BR and two-player tax constraints.
Finite histogram columns; all rows are necessary and feasibility is not SPE.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import json,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent
ns={'__file__':str(HERE/'root_full_hist_completion.py')};src=(HERE/'root_full_hist_completion.py').read_text();exec(compile(src.split('r=linprog(')[0],'<full root hist columns>','exec'),ns)
old=ns['old'];cols=ns['cols'];A=ns['A'];E=ns['E'];mass=ns['mass'];menus=ns['ns']['menus'];basebits=ns['ns']['bits'];names=ns['names']+[f'root:{j}:off-menu:{k}' for j in range(4) for k in range(4)];spec=list(ns['spec'])+[('off',j,k) for j in range(4) for k in range(4)]
from offdiagonal_probe import types,quads,paths,labels
ai=np.array([a for a,h in cols]);count=np.array([[sum(n*v[k] for t,v,n in h) for k in range(4)] for a,h in cols]);extra=[]
def add(n,r,sp):names.append(n);spec.append(sp);extra.append(r)
def feature_old(a):
 b=dict(zip(labels,basebits[a]));out={};tax={}
 def q(n,d):return n/d if n else 0.
 for rr,(pn,path) in enumerate(paths.items()):
  p=sum(b[k] for k in path[:3]);load=sum(b[k] for k in path);H=q(b[path[3]]+b[path[4]],load)+q(b[path[3]],(p+1)*(p+2));tax[pn]=(H,1/(p+1),1/(p+2));ell,h=old[a]['menus_lh'][rr];d=sum(n*t[0] for n,t in zip(old[a]['AB_hist'],types));out['L'+str(rr)]=(q(ell,p+1)-q(h,(p+1)*(p+2)),q(d,p+2)+q(5-d,p+1))
 for tag,key,prefix,ts in [('AB','AB_hist','AB',types),('AE','AE_hist','AE',types),('S','second_hist','A',quads)]:
  p=sum(b[k] for k in prefix);hist=old[a][key];m=len(ts[0])-1
  for j in range(1,m+1):
   U=sum(n*q(t[j],p+sum(t)) for n,t in zip(hist,ts));D=sum(n*q(1,p+sum(t[:j])+m-j+1) for n,t in zip(hist,ts));out[tag+str(j)]=(U,D)
  H=sum(n*(q(t[-2]+t[-1],p+sum(t))+q(t[-2],(p+sum(t[:-2])+1)*(p+sum(t[:-2])+2))) for n,t in zip(hist,ts));D1=sum(n*q(1,p+sum(t[:-2])+1) for n,t in zip(hist,ts));D2=sum(n*q(1,p+sum(t[:-2])+2) for n,t in zip(hist,ts));tax[tag]=(H,D1,D2)
 return out,tax
features=[feature_old(a) for a in range(len(old))]
for title in features[0][0]:
 U=np.array([o[0][title][0] for o in features])[ai];D=np.array([o[0][title][1] for o in features])[ai]
 for k in range(4):add('old-index:'+title+':rootmenu:'+str(k),5*U-count[:,k]*D,('old-index',title,k))
for group in features[0][1]:
 H,D1,D2=[np.array([o[1][group][i] for o in features])[ai] for i in range(3)]
 for k in range(4):
  c=count[:,k]
  for mi,(mn,size,mc) in enumerate(menus):
   z=mc[ai];add('old-tax:'+group+':root'+str(k)+'|'+mn,5*size*H-(size*c+5*z-2*c*z)*D1-2*c*z*D2,('old-tax',group,k,mi))
 for k,l in combinations_with_replacement(range(4),2):
  c=count[:,k];z=count[:,l];add('old-tax:'+group+':root'+str(k)+'|root'+str(l),25*H-(5*c+5*z-2*c*z)*D1-2*c*z*D2,('old-tax-root',group,k,l))
rootfeatures=[]
for a,h in cols:
 H=D1=D2=0.
 for t,v,n in h:
  total=t+sum(v);bg=t+sum(v[:2]);H+=n*((v[2]+v[3])/total if v[2]+v[3] else 0.)+n*v[2]/((bg+1)*(bg+2));D1+=n/(bg+1);D2+=n/(bg+2)
 rootfeatures.append((H,D1,D2))
H,D1,D2=np.array(rootfeatures).T
for k in range(4):
 c=count[:,k]
 for mi,(mn,size,mc) in enumerate(menus):
  z=mc[ai];add('root-tax:root'+str(k)+'|'+mn,5*size*H-(size*c+5*z-2*c*z)*D1-2*c*z*D2,('root-tax',k,mi))
for k,l in combinations_with_replacement(range(4),2):
 c=count[:,k];z=count[:,l];add('root-tax:root'+str(k)+'|root'+str(l),25*H-(5*c+5*z-2*c*z)*D1-2*c*z*D2,('root-tax-root',k,l))
A=np.r_[A,extra];n=len(cols)
r=linprog(np.r_[np.zeros(n),-1.],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=np.c_[E,np.zeros(len(old))],b_eq=list(map(float,mass)),bounds=[(0,None)]*n+[(None,None)],method='highs')
report={'scope':'finite-column necessary full root histogram completion including old/new shared menus and tax; not a complete SPE','columns':n,'rows':len(A),'equalities':len(old),'status':r.message,'margin':float(r.x[-1]) if r.success else None,'row_names':names,'row_specs':spec,'column_specs':cols,'point':r.x[:-1].tolist() if r.success else None,'dual_rows':(-r.ineqlin.marginals).tolist() if r.success else None,'dual_equalities':r.eqlin.marginals.tolist() if r.success else None}
(HERE/'root_full_hist_enhanced.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ('scope','columns','rows','equalities','status','margin')},indent=2))
