"""Joint full-count-history pure strategy/customer MILP candidate generator.

A count-dependent policy is one legitimate complete ordered-history strategy,
not a model restriction for any universal conclusion. Every integer policy is
expanded and then exact-rationally reconstructed/verified before acceptance.
This file generates candidates only; solver bounds are not certificates.
"""
from __future__ import annotations
from functools import lru_cache
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse,json,math,sys,time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import CustomerType,Instance,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,serializable

def comps(n,p):
 if p==1:yield (n,);return
 for i in range(n+1):
  for q in comps(n-i,p-1):yield (i,)+q

def addone(q,a):return tuple(x+(j==a) for j,x in enumerate(q))

def run(m,p,path,J,seconds,symmetry):
 masks=tuple(range(1,1<<p))
 if symmetry:
  # Only the last p-2 topic labels are exchangeable in the instance.
  orbit={}
  for b in masks:orbit.setdefault((b&1,(b>>1)&1,(b>>2).bit_count()),[]).append(b)
  cols=tuple(tuple(v) for k,v in sorted(orbit.items()))
 else:cols=tuple((b,) for b in masks)
 n=len(cols);nodes=tuple(q for d in range(m) for q in comps(d,p))
 u={};z={};nextvar=n
 for q in nodes:
  for a in range(p):u[q,a]=nextvar;nextvar+=1
 for q in nodes:
  for a in range(p):z[q,a]=nextvar;nextvar+=1
 lo=np.zeros(nextvar);hi=np.full(nextvar,m,dtype=float);integ=np.zeros(nextvar,dtype=np.uint8)
 for j in z.values():hi[j]=1;integ[j]=1
 q0=(0,)*p;pathq=q0
 for a in path:lo[z[pathq,a]]=hi[z[pathq,a]]=1;pathq=addone(pathq,a)
 hi[u[q0,path[0]]]=1
 @lru_cache(None)
 def row(q,a):
  if not q[a]:return (0,)*n
  return tuple(sum(Fraction(1,sum(q[b] for b in range(p) if mask&(1<<b))) for mask in col if mask&(1<<a)) for col in cols)
 def cov(sup):
  t=sum(1<<a for a in sup)
  return tuple(sum(bool(mask&t) for mask in col) for col in cols)
 ii=[];jj=[];xx=[];lbs=[];ubs=[]
 def add(r,lb=-np.inf,ub=np.inf):
  i=len(lbs)
  for j,x in r.items():
   if x:ii.append(i);jj.append(j);xx.append(float(x))
  lbs.append(lb);ubs.append(ub)
 def expr(q,a):
  if sum(q)<m:return {u[q,a]:1}
  return {j:v for j,v in enumerate(row(q,a)) if v}
 def diff(q,a,child,b):
  r={u[q,a]:1}
  for j,v in expr(child,b).items():r[j]=r.get(j,0)-v
  return r
 w=cov(a for a in range(p) if pathq[a]);v=cov(J)
 add({j:x for j,x in enumerate(w) if x},1,1)
 add({j:len(col) for j,col in enumerate(cols)},ub=m*p)
 for a in range(p):
  r={j:sum(bool(mask&(1<<a)) for mask in col) for j,col in enumerate(cols)};r[u[q0,path[0]]]=-m;add(r,ub=0)
 add({u[q0,a]:q for a,q in enumerate(pathq) if q},1,1)
 for q in nodes:
  add({z[q,a]:1 for a in range(p)},1,1)
  for a in range(p):
   for t in range(p):
    r=diff(q,t,addone(q,a),t);r[z[q,a]]=m;add(r,ub=m)
    r=diff(q,t,addone(q,a),t);r[z[q,a]]=-m;add(r,lb=-m)
   for b in range(p):
    if b==a:continue
    r=diff(q,a,addone(q,b),b);r[z[q,a]]=-m;add(r,lb=-m)
 A=coo_matrix((xx,(ii,jj)),shape=(len(lbs),nextvar)).tocsc()
 objective=np.zeros(nextvar);objective[:n]=-np.array(v)
 started=time.monotonic()
 sol=milp(objective,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lbs),np.array(ubs)),options={'time_limit':seconds,'mip_rel_gap':0.,'presolve':True})
 meta={'status':int(sol.status),'message':sol.message,'variables':nextvar,'binaries':len(z),'rows':len(lbs),'nnz':len(xx),'seconds':time.monotonic()-started,'customer_orbits':len(cols),'objective':float(-sol.fun) if sol.fun is not None else None,'solver_bound_not_certificate':float(-sol.mip_dual_bound) if hasattr(sol,'mip_dual_bound') and sol.mip_dual_bound is not None else None}
 if sol.x is None:return meta,None
 pol={q:max(range(p),key=lambda a:sol.x[z[q,a]]) for q in nodes}
 actions={h:pol[tuple(h.count(a) for a in range(p))] for d in range(m) for h in product(range(p),repeat=d)}
 cone=StrategyCone(p,m,actions);res=cone.optimize(J)
 meta['exact_reconstruction']=bool(res['certified'])
 if not res['certified']:return meta,None
 vals=res['values'];den=math.lcm(*(x.denominator for x in vals));clones=[int(x*den) for x in vals];g=math.gcd(*clones);clones=[x//g for x in clones]
 ins=Instance(tuple(str(a) for a in range(p)),tuple(CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),k) for mask,k in enumerate(clones,1) if k),m)
 cert=StrategyCertificate(actions,cone.root);checked=verify_certificate(ins,cert);checked.assert_valid()
 proof={'instance':ins.to_dict(),'strategy':cert.to_dict(),'ratio':Fraction(ins.optimal_welfare(),ins.welfare(cone.root)),'W':ins.welfare(cone.root),'OPT':ins.optimal_welfare(),'payoffs':ins.player_payoffs(path),'exact_cone_objective':res['value'],'exact_SPE_verified':True}
 return meta,proof

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=5);ap.add_argument('--p',type=int,default=7);ap.add_argument('--path',default='0,0,0,0,1');ap.add_argument('--portfolio',default='2,3,4,5,6');ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--symmetry',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 meta,proof=run(args.m,args.p,tuple(map(int,args.path.split(','))),tuple(map(int,args.portfolio.split(','))),args.seconds,args.symmetry)
 report={'scope':'finite candidate generation in count-dependent complete-history policies','universal_result':False,'parameters':vars(args)|{'output':str(args.output)},'milp':meta,'proof':proof}
 args.output.write_text(json.dumps(serializable(report),indent=2)+'\n');print(json.dumps(serializable(meta)))
