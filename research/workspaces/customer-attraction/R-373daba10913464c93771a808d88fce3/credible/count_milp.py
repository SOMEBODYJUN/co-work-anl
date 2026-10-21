"""Count-policy MILP candidate search; complete ordered-history verification follows extraction.
No floating bounds certify a general statement. Deterministic seed 37381021.
"""
from __future__ import annotations
from pathlib import Path
import sys,json,time,argparse
from fractions import Fraction
from itertools import product,combinations_with_replacement,combinations
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp,linprog
from scipy.sparse import coo_matrix
R=Path(__file__).resolve().parents[5];sys.path[:0]=[str(R),str(R/'tests/audits')]
from customer_attraction import *
from customer_attraction_strategy_lp import *
def inc(k,a):return tuple(x+(i==a) for i,x in enumerate(k))
def states(p,m):
 return tuple(tuple(h.count(a) for a in range(p)) for d in range(m) for h in combinations_with_replacement(range(p),d))
def run(p,path,seconds):
 m=len(path);n=2**p-1;ks=states(p,m);idx=n
 ui={};zi={}
 for k in ks:
  for a in range(p):ui[k,a]=idx;idx+=1
 for k in ks:
  for a in range(p):zi[k,a]=idx;idx+=1
 lo=np.zeros(idx);hi=np.full(idx,float(m));integ=np.zeros(idx,np.uint8)
 for z in zi.values():hi[z]=1;integ[z]=1
 k=(0,)*p
 for a in path:lo[zi[k,a]]=hi[zi[k,a]]=1;k=inc(k,a)
 rootq=k;w=coverage_row(p,(a for a in range(p) if k[a]));rootact=path[0]
 ri=[];rj=[];rx=[];lbs=[];ubs=[]
 def add(row,lb=-np.inf,ub=np.inf):
  z=len(lbs)
  for j,x in row.items():
   if x:ri.append(z);rj.append(j);rx.append(float(x))
  lbs.append(lb);ubs.append(ub)
 def ex(k,a):
  if sum(k)<m:return {ui[k,a]:1}
  return {j:x for j,x in enumerate(payoff_row(p,k,a)) if x} if k[a] else {}
 def diff(k,a,t,b):
  o={ui[k,a]:1}
  for j,x in ex(t,b).items():o[j]=o.get(j,0)-x
  return o
 add({j:x for j,x in enumerate(w) if x},1,1)
 for a in range(p):
  row={j:1 for j in range(n) if j+1&(1<<a)};row[ui[(0,)*p,rootact]]=-m;add(row,ub=0)
 for k in ks:
  add({zi[k,a]:1 for a in range(p)},1,1)
  for a in range(p):
   child=inc(k,a);z=zi[k,a]
   for t in range(p):
    row=diff(k,t,child,t);row[z]=m;add(row,ub=m)
    row=diff(k,t,child,t);row[z]=-m;add(row,lb=-m)
   for b in range(p):
    if a==b:continue
    row=diff(k,a,inc(k,b),b);row[z]=-m;add(row,lb=-m)
 target=coverage_row(p,range(min(m,p)))
 obj=tuple(v-ww-m*u for v,ww,u in zip(target,w,payoff_row(p,rootq,rootact)))
 c=np.zeros(idx);c[:n]=-np.array(obj,float)
 A=coo_matrix((rx,(ri,rj)),shape=(len(lbs),idx)).tocsc()
 t=time.time();rr=milp(c,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lbs),np.array(ubs)),options={'time_limit':seconds,'mip_rel_gap':0.0,'presolve':True,'random_seed':37381021,'threads':1})
 meta={'p':p,'m':m,'path':path,'seconds':time.time()-t,'status':int(rr.status),'objective':None if rr.fun is None else float(-rr.fun),'floating_only':True,'message':rr.message,'count_nodes':len(ks),'binaries':len(zi)}
 if rr.x is None:return meta
 policy={k:max(range(p),key=lambda a:rr.x[zi[k,a]]) for k in ks}
 actions={h:policy[tuple(h.count(a) for a in range(p))] for d in range(m) for h in product(range(p),repeat=d)}
 cone=StrategyCone(p,m,actions)
 rr2=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([w],float),b_eq=[1],bounds=(0,None),method='highs')
 if not rr2.success:meta['exact_recovery']='infeasible extracted cone';return meta
 vals=tuple(Fraction(float(x)).limit_denominator(10**6) for x in rr2.x)
 if not cone.verify(vals) or dot(w,vals)!=1:vals=cone.recover_vertex(rr2.x)
 if vals is None or not cone.verify(vals) or dot(w,vals)!=1:meta['exact_recovery']='failed';return meta
 cs=integer_clones(vals);ins=instance_from_clones(p,m,cs);cert=StrategyCertificate(actions,cone.root);v=verify_certificate(ins,cert);v.assert_valid()
 meta['exact_objective']=str(dot(obj,vals));meta['welfare']=ins.welfare(cone.root);meta['optimum']=ins.optimal_welfare();meta['utilities']=list(map(str,ins.player_payoffs(v.terminal_history)));meta['integer_clones']=cs;meta['strategy']=cert.to_dict();meta['verified_histories']=v.checked_histories
 return meta
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=20);ap.add_argument('--p',type=int,default=4);ap.add_argument('--path',default='0,0,0,1,1');a=ap.parse_args()
 out=run(a.p,tuple(map(int,a.path.split(','))),a.seconds);label='-'.join(map(str,out['path']));(Path(__file__).parent/f'count_milp_{a.p}_{label}.json').write_text(json.dumps(out));print(json.dumps({k:v for k,v in out.items() if k not in ('strategy','integer_clones')}))
