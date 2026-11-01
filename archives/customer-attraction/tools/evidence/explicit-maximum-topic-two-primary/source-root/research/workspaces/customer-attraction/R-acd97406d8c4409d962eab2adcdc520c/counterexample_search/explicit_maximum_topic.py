"""Finite old-support relaxation with an explicit unknown maximum theme.

The membership y_i may split each original atom, so y_i in [0,x_i].
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
# Reuse construction of 437 original plus 3087 certified menu rows; no solve.
namespace={'__file__':str(HERE/'augment_background_menus.py')}
exec(compile((HERE/'augment_background_menus.py').read_text().split('res=linprog')[0],'<original and background-menu row construction>','exec'),namespace)
rows=namespace['rows'];bits=namespace['bits'];menus=namespace['menus'];coefs=namespace['coefs'];w=namespace['w'];o=namespace['o'];N=len(bits)
rows=[list(row)+[F(0)]*N for row in rows]
labels=['base:'+str(i) for i in range(len(rows))]
root=[F(b[0],sum(b[:5])) if b[0] else F(0) for b in bits]
def add(x,y,label):rows.append(list(x)+list(y));labels.append(label)
for i in range(N):
 xx=[F(0)]*N;yy=xx.copy();xx[i]=1;yy[i]=-1;add(xx,yy,'M-membership-bound:'+str(i))
add([5*u for u in root],[-F(1)]*N,'root-max-size-bound')
for j in range(21):
 name,t,_=menus[0][j];count=[mm[j][2] for mm in menus]
 add([-F(c,t) for c in count],[F(1)]*N,'M-larger-than-menu-average:'+name)
 add([80*t*u-5*c for u,c in zip(root,count)],[-15*t+4*c for c in count],'root-max-strong:'+name)
for family,path,first in [('actual',[0,1,2,3,4],0),('second',[0,4,5,6,7],2),('third',[0,1,4,8,9],3)]:
 for i in range(first,5):
  k=5-i;rp=[F(b[path[i]],sum(b[j] for j in path)) if b[path[i]] else F(0) for b in bits];pref=[sum(b[j] for j in path[:i]) for b in bits];muw=[F(1,pp+k) for pp in pref]
  add(rp,[-v for v in muw],'M-legal:'+family+':'+str(i))
  if k==1:continue
  nu0,nu1=coefs[k]
  for j in range(21):
   name,t,_=menus[0][j];count=[mm[j][2] for mm in menus]
   # A=M, R=a known menu of t themes.
   add([t*u+(nu0-nu1)*mu*c for u,mu,c in zip(rp,muw,count)],[-(1+nu0)*t*mu+nu1*mu*c for mu,c in zip(muw,count)],'pair-M-R:'+family+':'+str(i)+':'+name)
   # A=known menu, R=M.
   add([t*u-(1+nu0)*mu*c for u,mu,c in zip(rp,muw,count)],[(nu0*t-nu1*(t-c))*mu for mu,c in zip(muw,count)],'pair-A-M:'+family+':'+str(i)+':'+name)
res=linprog(-np.array(o+[0]*N,dtype=float),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=np.array([w+[0]*N],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
report={'scope':'finite old64 atom-support relaxation with explicit maximum theme and certified background-menu rows','universal_bound_proved':False,'rows':len(rows),'columns':2*N,'status':res.message,'floating_objective':None if res.fun is None else -res.fun}
if res.x is not None:
 support=[i for i,x in enumerate(res.x) if x>1e-8]
 active=[i for i,row in enumerate(rows) if abs(sum(float(v)*x for v,x in zip(row,res.x)))<1e-7]
 A=[[F(v) for v in (w+[0]*N) if False]]
 A=[[F((w+[0]*N)[j]) for j in support]]+[[rows[i][j] for j in support] for i in active]
 rhs=[F(1)]+[F(0)]*len(active);pivots={}
 for rr,bb in zip(A,rhs):
  rr=list(rr)
  for c,(basis,brhs) in sorted(pivots.items()):
   if rr[c]:
    v=rr[c];rr=[x-v*y for x,y in zip(rr,basis)];bb-=v*brhs
  nz=next((c for c,v in enumerate(rr) if v),None)
  if nz is None:
   assert bb==0
   continue
  v=rr[nz];pivots[nz]=([x/v for x in rr],bb/v)
  if len(pivots)==len(support):break
 if len(pivots)!=len(support):raise AssertionError(('active rank',len(pivots),len(support)))
 solution=[F(0)]*len(support)
 for c,(rr,bb) in sorted(pivots.items(),reverse=True):solution[c]=bb-sum(rr[j]*solution[j] for j in range(c+1,len(support)))
 point=[F(0)]*(2*N)
 for j,v in zip(support,solution):point[j]=v
 assert all(x>=0 for x in point) and sum(x*y for x,y in zip(w,point))==1
 assert all(sum(x*y for x,y in zip(row,point))>=0 for row in rows)
 exact_objective=sum(x*y for x,y in zip(o,point));assert exact_objective>2
 report['exact_primal_point']=list(map(str,point));report['exact_primal_objective']=str(exact_objective);report['exact_primal_verified_all_rows']=True
 report['floating_point']=['%.17g'%v for v in res.x]
 report['floating_max_topic_size']=sum(res.x[N:])
 report['floating_root_payoff']=sum(float(u)*v for u,v in zip(root,res.x))
 print(json.dumps({k:v for k,v in report.items() if k not in ('floating_point','exact_primal_point')},indent=2))
(HERE/'explicit_maximum_topic.json').write_text(json.dumps(report,indent=2)+'\n')
