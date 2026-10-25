"""Named auxiliary test C<=0 at shared-load optimum, on existing insurance.
Only menus are reconstructed. Full-SPE theorem is inherited from peer; floating
optimizer and its C sign are exploratory, not exact certificates.
"""
from itertools import product
from functools import lru_cache
import numpy as np
from scipy.optimize import minimize
import json,sys
from pathlib import Path
m=int(sys.argv[1]);banks=m-1;acts=tuple(product(range(m),range(banks)));k=len(acts)
inc=np.array([[int(x==a) for x in range(m)]+[int(x==b) for x in range(banks)] for a,b in acts]);w=np.r_[np.ones(m),2*np.ones(banks)]
@lru_cache(None)
def action(h):
 if not h:return(0,0)
 aa,ab=h[0];mode='BASE';target=None;usedb={ab}
 for j,a in enumerate(h[1:],1):
  if mode=='BASE':
   prescribed=(aa,min(set(range(banks))-usedb))
   if a!=prescribed:
    if a[1] in usedb:mode='EXIT'
    else:mode='PUNISH';target=a[1]
  elif mode=='PUNISH' and a[1] in usedb:mode='EXIT'
  usedb.add(a[1])
 freea=set(range(m))-{a for a,b in h};freeb=set(range(banks))-usedb;last=len(h)==m-1
 if mode=='BASE':return(min(freea),ab) if last else(aa,min(freeb))
 if mode=='PUNISH':return(min(freea),target) if last else(min(freea),min(freeb))
 return(min(freea),min(freeb))
@lru_cache(None)
def finish(h):return h if len(h)==m else finish(h+(action(h),))
z=finish(());ad={a:j for j,a in enumerate(acts)}
cols=np.array([[sum(inc[ad[t]] for j,t in enumerate(finish(z[:i]+(b,))) if j!=i) for b in acts] for i in range(m)])
p=np.full(k,1/k);rho=p@inc
objective=lambda q:np.sum(w*rho/(1+np.einsum('ij,ijx->x',q.reshape(m,k),cols)/m))
def jac(q):
 L=np.einsum('ij,ijx->x',q.reshape(m,k),cols)/m
 return(-np.einsum('ijx,x->ij',cols,w*rho/(1+L)**2)/m).ravel()
res=minimize(objective,np.full(m*k,1/k),jac=jac,bounds=[(0,1)]*(m*k),constraints=[{'type':'eq','fun':lambda q:q.reshape(m,k).sum(axis=1)-1,'jac':lambda q:np.kron(np.eye(m),np.ones((1,k)))}],method='SLSQP',options={'ftol':1e-12,'maxiter':500})
q=res.x.reshape(m,k);L=np.einsum('ij,ijx->x',q,cols)/m;t=1/(1+L)
C=sum(p[a]*np.sum(w*inc[a]*t*t*(cols[i,a]-L)) for i in range(m) for a in range(k))
D=sum(p[a]*np.sum(w*inc[a]*t*t*(cols[i,a]-L)**2/(1+cols[i,a])) for i in range(m) for a in range(k))
us=[np.sum(w*inc[ad[z[i]]]/(1+cols[i,ad[z[i]]])) for i in range(m)]
IC=sum(us)-sum(p[a]*np.sum(w*inc[a]/(1+cols[i,a])) for i in range(m) for a in range(k))
assert abs(sum(us)-m*objective(res.x)-(IC-C+D))<1e-8
out={'scope':'existing insurance family; floating shared minimizer only; named C<=0 diagnostic','m':m,'success':bool(res.success),'F':res.fun,'C':C,'D':D,'IC':IC,'W_minus_mF':sum(us)-m*res.fun,'L':L.tolist(),'q':q.tolist()}
print(json.dumps({j:out[j] for j in out if j not in ('q','L')},indent=2))
Path(__file__).with_name(f'insurance_shared_covariance_m{m}.json').write_text(json.dumps(out,indent=2)+'\n')
# Exact candidate witness. For the named m=6 test only, reconstruct a rational
# feasible L and certify it is the global convex optimum by coordinate bounds.
if m==6:
 from fractions import Fraction as F
 from scipy.optimize import linprog
 l0=F(8,3);lout=F(7,15);Lf=[l0]+[lout]*5+[F(1)]*5
 aeq=np.r_[np.kron(np.eye(m),np.ones((1,k))),cols.reshape(m*k,-1).T]
 beq=np.r_[np.ones(m),[float(m*l) for l in Lf]]
 lp=linprog(np.zeros(m*k),A_eq=aeq,b_eq=beq,bounds=[(0,None)]*(m*k),method='highs')
 assert lp.success
 qf=[[F(float(v)).limit_denominator(100000) for v in row] for row in lp.x.reshape(m,k)]
 assert all(sum(row)==1 and min(row)>=0 for row in qf)
 assert all(sum(qf[i][a]*int(cols[i,a,x]) for i in range(m) for a in range(k))==m*Lf[x] for x in range(len(Lf)))
 # Every menu column has at least the following anchor-0 competitor count.
 mins=[min(int(cols[i,a,0]) for a in range(k)) for i in range(m)]
 assert mins==[1,1,2,3,4,5] and F(sum(mins),m)==l0
 tf=[1/(1+l) for l in Lf];pf=F(1,k)
 Cf=sum(pf*sum(F(int(w[x]))*int(inc[a,x])*tf[x]**2*(F(int(cols[i,a,x]))-Lf[x]) for x in range(len(Lf))) for i in range(m) for a in range(k))
 Df=sum(pf*sum(F(int(w[x]))*int(inc[a,x])*tf[x]**2*(F(int(cols[i,a,x]))-Lf[x])**2/(1+int(cols[i,a,x])) for x in range(len(Lf))) for i in range(m) for a in range(k))
 uif=[sum(F(int(w[x]))*int(inc[ad[z[i]],x])/(1+int(cols[i,ad[z[i]],x])) for x in range(len(Lf))) for i in range(m)]
 icf=sum(uif)-sum(pf*sum(F(int(w[x]))*int(inc[a,x])/(1+int(cols[i,a,x])) for x in range(len(Lf))) for i in range(m) for a in range(k))
 Ff=sum(F(1,m)*tf[x] for x in range(m))+sum(F(2,banks)*tf[x] for x in range(m,len(Lf)))
 assert Ff==F(71,44) and sum(uif)-m*Ff==icf-Cf+Df and Cf>0
 # KKT certificate on q supports (weights are query marginal * t^2).
 rhof=[F(1,m)]*m+[F(1,banks)]*banks
 gradcols=[[sum(F(int(w[x]))*rhof[x]*tf[x]**2*int(cols[i,a,x]) for x in range(len(Lf))) for a in range(k)] for i in range(m)]
 assert all(qf[i][a]==0 or gradcols[i][a]==max(gradcols[i]) for i in range(m) for a in range(k))
 exact={'scope':'Exact old insurance m6 auxiliary C<=0 counterexample; complete SPE theorem inherited, not reaudited here','p':'uniform 30 topics','L':[str(x) for x in Lf],'q':[[[a,str(v)] for a,v in enumerate(row) if v] for row in qf],'menu_minimum_anchor_load':mins,'F_optimum':str(Ff),'C':str(Cf),'D':str(Df),'IC':str(icf),'W_minus_mF':str(sum(uif)-m*Ff),'C_positive':Cf>0,'KKT_exact':True,'all_exact_balance_checks':True}
 Path(__file__).with_name('insurance_shared_covariance_m6_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
 print(json.dumps({j:exact[j] for j in exact if j not in ('q','L')},indent=2))
