#!/usr/bin/env python3
"""Fixed-path full-history MILP for half/weak-individual candidate generation.

Generalizes the existing cone_attack_joint_milp interface by normalizing either
root welfare or the first mover's utility. Both give every topic size <=m and
the same valid M=m, hence every real continuation utility is bounded by m.
Floating MILP results only select a full tree; exact LP and replay decide claims.
"""
import argparse,json,time
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import sys
sys.path.insert(0,str(Path(__file__).parent))
from last_share_probe import *
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
from customer_attraction_strategy_lp import coverage_row

def propose(p,path,J,normalization,seconds):
 m=len(path);n=(1<<p)-1;q=tuple(path.count(a) for a in range(p));nodes=tuple(h for d in range(m) for h in product(range(p),repeat=d))
 u={(h,a):n+i*p+a for i,h in enumerate(nodes) for a in range(p)};off=n+len(nodes)*p
 z={(h,a):off+i*p+a for i,h in enumerate(nodes) for a in range(p)};nv=off+len(nodes)*p
 lo=np.zeros(nv);hi=np.full(nv,m,dtype=float);integrality=np.zeros(nv,dtype=np.uint8)
 for j in z.values():hi[j]=1;integrality[j]=1
 for d,a in enumerate(path):lo[z[path[:d],a]]=hi[z[path[:d],a]]=1
 hi[u[(),path[0]]]=1
 ii=[];jj=[];xx=[];lb=[];ub=[]
 def add(row,l=-np.inf,h=np.inf):
  k=len(lb)
  for j,x in row.items():
   if x:ii.append(k);jj.append(j);xx.append(float(x))
  lb.append(l);ub.append(h)
 def child(h,a):
  if len(h)<m:return {u[h,a]:1}
  qq=tuple(h.count(b) for b in range(p))
  return {j:x for j,x in enumerate(payoff_row(p,qq,a)) if x} if qq[a] else {}
 def diff(h,a,hh,b):
  r={u[h,a]:1}
  for j,x in child(hh,b).items():r[j]=r.get(j,0)-x
  return r
 w=coverage_row(p,(a for a in range(p) if q[a]));normal=w if normalization=='welfare' else payoff_row(p,q,path[0])
 add({j:x for j,x in enumerate(normal) if x},1,1)
 for a in range(p):
  row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u[(),path[0]]]=-m;add(row,h=0)
 if normalization=='welfare':add({u[(),a]:v for a,v in enumerate(q) if v},1,1)
 else:add({u[(),path[0]]:1},1,1)
 for h in nodes:
  add({z[h,a]:1 for a in range(p)},1,1)
  for a in range(p):
   for b in range(p):
    row=diff(h,b,h+(a,),b);row[z[h,a]]=m;add(row,h=m)
    row=diff(h,b,h+(a,),b);row[z[h,a]]=-m;add(row,l=-m)
   for b in range(p):
    if b!=a:
     row=diff(h,a,h+(b,),b);row[z[h,a]]=-m;add(row,l=-m)
 A=coo_matrix((xx,(ii,jj)),shape=(len(lb),nv)).tocsc();obj=np.zeros(nv);obj[:n]=-np.asarray(coverage_row(p,J),float)
 start=time.time();r=milp(obj,integrality=integrality,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,lb,ub),options={'time_limit':seconds,'mip_rel_gap':0})
 meta={'status':int(r.status),'message':r.message,'floating_objective':None if r.fun is None else float(-r.fun),'floating_bounds_are_not_certificates':True,'seconds':time.time()-start,'variables':nv,'constraints':len(lb)}
 if r.x is None:return None,meta,normal
 acts={h:max(range(p),key=lambda a:r.x[z[h,a]]) for h in nodes};cone=StrategyCone(p,m,acts)
 assert cone.root==q
 return cone,meta,normal

def exact_goal(cone,J,normal):
 obj=coverage_row(cone.topics,J);r=linprog(-np.asarray(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.asarray([normal],float),b_eq=[1],bounds=(0,None),method='highs')
 if not r.success:return {'status':r.message}
 vals=tuple(F(float(x)).limit_denominator(10**7) for x in r.x)
 if not(cone.verify(vals) and dot(normal,vals)==1):
  original=cone.welfare;cone.welfare=normal;vals=cone.recover_vertex(r.x);cone.welfare=original
 if vals is None or not cone.verify(vals) or dot(normal,vals)!=1:return {'status':'exact_recovery_failed'}
 clones=integer_clones(vals);assert independently_verify(cone,clones);inst=instance_from_clones(cone.topics,cone.players,clones)
 checked=verify_certificate(inst,StrategyCertificate(cone.actions,cone.root));checked.assert_valid();pay=inst.player_payoffs(checked.terminal_history);w=inst.welfare(cone.root);opt=inst.optimal_welfare()
 return {'status':'exact_SPE','objective':dot(obj,vals),'instance':inst.to_dict(),'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'path':checked.terminal_history,'payoffs':pay,'welfare':w,'optimum':opt,'half_gap':2*w-opt,'weak_individual_gap':(2*cone.players-1)*pay[0]-opt}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--path',default='0,1,2');ap.add_argument('--portfolio',default='0,1,2');ap.add_argument('--normalization',choices=['welfare','first'],default='first');ap.add_argument('--seconds',type=float,default=40);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 path=tuple(map(int,a.path.split(',')));J=tuple(map(int,a.portfolio.split(',')));cone,meta,norm=propose(a.topics,path,J,a.normalization,a.seconds)
 out={'normalization':a.normalization,'fixed_path':path,'portfolio':J,'milp':meta}
 if cone is not None:out['exact']=exact_goal(cone,J,norm)
 a.output.write_text(json.dumps(serializable(out),indent=2)+'\n');print(json.dumps(serializable({k:v for k,v in out.items() if k!='exact'}|({'exact_summary':{k:v for k,v in out['exact'].items() if k not in ('instance','strategy')}} if 'exact' in out else {}))),flush=True)
if __name__=='__main__':main()
