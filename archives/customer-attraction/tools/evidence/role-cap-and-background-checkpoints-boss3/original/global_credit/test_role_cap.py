"""One precise candidate test on six old complete SPEs, no new game search.
Candidate: every optimal ordered tuple and legal owner assignment makes the
full-O INIT + fixed SAFE/CLIP row kernel obey A_j <= 2 u_j.  A positive result
would not prove the weaker existential choice of owners or general HALF.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def run(name):
 d=json.loads(Path('examples/customer_attraction/'+name+'.json').read_text())
 ce=json.loads(Path('evidence/certificates/customer_attraction/'+name+'.json').read_text())
 m,k=d['players'],len(d['topics'])
 typ=[(frozenset(c['topics']),int(c.get('multiplicity',1))) for c in d['customers']]
 sigma={tuple(x['history']):x['action'] for x in ce.get('strategy',ce)['actions']}
 histories=[h for i in range(m) for h in product(range(k),repeat=i)]
 assert set(histories)==set(sigma)
 @lru_cache(None)
 def finish(h):
  return h if len(h)==m else finish(h+(sigma[h],))
 @lru_cache(None)
 def loads(z):return tuple(sum(a in ss for a in z) for ss,n in typ)
 @lru_cache(None)
 def pay(z,i):
  return sum((F(n,c) for (ss,n),c in zip(typ,loads(z)) if z[i] in ss),F())
 z=finish(())
 u=tuple(pay(z,i) for i in range(m))
 checks=0
 for h in histories:
  for a in range(k):
   assert pay(finish(h),len(h))>=pay(finish(h+(a,)),len(h));checks+=1
 @lru_cache(None)
 def kernel(h,mode):
  i=len(h);b=finish(h);a=sigma[h];aa=finish(z[:i]+(a,));v=pay(b,i)
  if not v:return tuple(F() for _ in range(m))
  ca,cb=loads(aa),loads(b)
  ed=[];neg=F();diag=F()
  for x,(ss,n) in enumerate(typ):
   if a not in ss:continue
   ja={j for j in range(m) if j!=i and aa[j] in ss}
   jb={j for j in range(m) if j!=i and b[j] in ss}
   unit=F(n,ca[x]*cb[x]);neg+=len(jb-ja)*unit
   diag+=(1+len(ja&jb))*unit
   for j in ja-jb:ed.append((j,x,unit))
  p=sum((q for j,x,q in ed),F())
  assert diag+p==v
  if mode=='clip':
   cancel=min(p,neg+u[i]-pay(aa,i));kept=[]
   for j,x,q in sorted(ed,key=lambda e:(e[0]>=i,e[0],e[1])):
    rem=min(cancel,q);cancel-=rem
    if q>rem:kept.append((j,x,q-rem))
   assert not cancel
   ed=kept;diag=min(v,u[i])
  out=[F() for _ in range(m)];out[i]+=diag/v
  for j,x,q in ed:
   if j<i:out[j]+=q/v
   else:
    de=kernel(aa[:j],mode)
    for l in range(m):out[l]+=q/v*de[l]
  assert sum(out)==1
  return tuple(out)
 @lru_cache(None)
 def src(i,a,x,mode):
  aa=finish(z[:i]+(a,));ss,n=typ[x];c=loads(aa)[x]
  assert a in ss and c>0
  out=[F() for _ in range(m)]
  for j in range(m):
   if aa[j] not in ss:continue
   if j<=i:out[j]+=F(1,c)
   else:
    ke=kernel(aa[:j],mode)
    for l in range(m):out[l]+=F(1,c)*ke[l]
  assert sum(out)==1
  return tuple(out)
 def cov(t):return sum(n for ss,n in typ if any(a in ss for a in t))
 tuples=list(product(range(k),repeat=m));opt=max(map(cov,tuples));opts=[t for t in tuples if cov(t)==opt]
 ans={}
 for mode in ('safe','clip'):
  best=None;viol=[];best_max=1e10;best_tuple=None;worst_min=0
  for t in opts:
   xx=[x for x,(ss,n) in enumerate(typ) if any(a in ss for a in t)]
   for target in range(m):
    val=F();owners={}
    for x in xx:
     elig=[i for i in range(m) if t[i] in typ[x][0]]
     oi=max(elig,key=lambda i:src(i,t[i],x,mode)[target]);owners[x]=oi
     val+=typ[x][1]*src(oi,t[oi],x,mode)[target]
    if val>2*u[target]:
     vv=(val/(2*u[target]),t,target,val,owners)
     if best is None or vv[0]>best[0]:best=vv
   # Fractional-owner feasibility for this one fixed row kernel.  The final
   # column is a common ratio t, so optimum <=1 means the role cap is feasible.
   pairs=[(x,i) for x in xx for i in range(m) if t[i] in typ[x][0]]
   aub=np.zeros((m,len(pairs)+1));aeq=np.zeros((len(xx),len(pairs)+1))
   for col,(x,i) in enumerate(pairs):
    ke=src(i,t[i],x,mode)
    for j in range(m):aub[j,col]=float(ke[j])
    aeq[xx.index(x),col]=1
   for j in range(m):aub[j,-1]=-float(2*u[j])
   obj=np.zeros(len(pairs)+1);obj[-1]=1
   rr=linprog(obj,A_ub=aub,b_ub=np.zeros(m),A_eq=aeq,b_eq=np.array([typ[x][1] for x in xx]),bounds=(0,None),method='highs')
   assert rr.success
   if rr.fun<best_max:best_max=float(rr.fun);best_tuple=t
   worst_min=max(worst_min,float(rr.fun))
  ans[mode]={'any_universal_cap2_violation':best is not None,'best_fractional_owner_max_ratio_over_optimal_tuples':best_max,'best_tuple':best_tuple,'worst_opt_tuple_fractional_owner_ratio':worst_min}
  if best:
   ratio,t,target,val,owners=best
   actual=[F() for _ in range(m)]
   for x,owner in owners.items():
    ke=src(owner,t[owner],x,mode)
    for j in range(m):actual[j]+=typ[x][1]*ke[j]
   ans[mode]['witness']={'tuple':t,'target_role_zero_based':target,'mass':str(val),'cap2':str(2*u[target]),'ratio':str(ratio),'owners_by_type':owners,'all_role_mass':list(map(str,actual))}
 return {'name':name,'players':m,'types':len(typ),'actual':z,'u':list(map(str,u)),'W':cov(z),'OPT':opt,'complete_ic_checks':checks,'optimal_ordered_tuples':len(opts),'modes':ans}

if __name__=='__main__':
 names=['portfolio_matching_failure','root_tax_failure','individual_security_failure','eight_cce_welfare_gap','coverage_opportunity_failure','prefix_balance_failure']
 result=[run(name) for name in names]
 out={'scope':'exact old-SPE kernels, universal-owner candidate only; owner LP floats diagnostic, not a proof','cases':result}
 Path(__file__).with_name('role_cap_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
