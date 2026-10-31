"""Count-Markov MILP only proposes a subset of full-history SPE policies.
Every accepted policy is expanded to all ordered histories and checked exactly.
No MILP bound is claimed as a full-history or exact bound.
"""
from pathlib import Path
import sys,json,time,argparse
from itertools import product,combinations
from fractions import Fraction
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,serializable,integer_clones,instance_from_clones,independently_verify
from customer_attraction import StrategyCertificate,verify_certificate

def counts_at(p,d):
 if p==1:return [(d,)]
 return [(a,)+t for a in range(d+1) for t in counts_at(p-1,d-a)]
def inc(k,a):return tuple(x+(i==a) for i,x in enumerate(k))
def candidate(p,path,J,seconds,rootcap=1):
 m=len(path);n=(1<<p)-1;nodes=tuple(k for d in range(m) for k in counts_at(p,d));Ui={};Zi={};ind=n
 for k in nodes:
  for a in range(p):Ui[k,a]=ind;ind+=1
 for k in nodes:
  for a in range(p):Zi[k,a]=ind;ind+=1
 lo=np.zeros(ind);hi=np.full(ind,m,dtype=float);integer=np.zeros(ind,dtype=np.uint8)
 for j in Zi.values():hi[j]=1;integer[j]=1
 k=(0,)*p
 for a in path:lo[Zi[k,a]]=hi[Zi[k,a]]=1;k=inc(k,a)
 root=(0,)*p;rootq=tuple(path.count(a) for a in range(p));hi[Ui[root,path[0]]]=rootcap
 rows=[];cols=[];vals=[];lb=[];ub=[]
 def add(row,l=-np.inf,u=np.inf):
  i=len(lb);lb.append(l);ub.append(u)
  for j,x in row.items():
   if x:rows.append(i);cols.append(j);vals.append(float(x))
 def child(k,t):
  if sum(k)<m:return {Ui[k,t]:1}
  if not k[t]:return {}
  return {j:x for j,x in enumerate(payoff_row(p,k,t)) if x}
 def diff(k,t,c,b):
  out={Ui[k,t]:1}
  for j,x in child(c,b).items():out[j]=out.get(j,0)-x
  return out
 w=coverage_row(p,(a for a,x in enumerate(rootq) if x))
 add({j:x for j,x in enumerate(w) if x},1,1)
 add({j:1 for j in range(n)},u=m*p)
 for a in range(p):
  row={j:1 for j in range(n) if (j+1)&(1<<a)};row[Ui[root,path[0]]]=-m;add(row,u=0)
 add({Ui[root,a]:x for a,x in enumerate(rootq) if x},1,1)
 for k in nodes:
  add({Zi[k,a]:1 for a in range(p)},1,1)
  for a in range(p):
   z=Zi[k,a]
   for t in range(p):
    row=diff(k,t,inc(k,a),t);row[z]=m;add(row,u=m)
    row=diff(k,t,inc(k,a),t);row[z]=-m;add(row,l=-m)
   for b in range(p):
    if b==a:continue
    row=diff(k,a,inc(k,b),b);row[z]=-m;add(row,l=-m)
 A=coo_matrix((vals,(rows,cols)),shape=(len(lb),ind)).tocsc();obj=np.zeros(ind);obj[:n]=-np.array(coverage_row(p,J),dtype=float)
 started=time.monotonic();res=milp(obj,integrality=integer,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lb),np.array(ub)),options={'time_limit':seconds,'mip_rel_gap':0.,'presolve':True})
 meta={'status':int(res.status),'message':res.message,'seconds':time.monotonic()-started,'variables':ind,'binary_actions':len(Zi),'constraints':len(lb),'floating_objective':None if res.fun is None else -res.fun,'floating_bound':getattr(res,'mip_dual_bound',None),'scope':'single count-Markov policy, candidate generator only'}
 if res.x is None:return None,meta
 policy={k:max(range(p),key=lambda a:res.x[Zi[k,a]]) for k in nodes}
 actions={h:policy[tuple(h.count(a) for a in range(p))] for d in range(m) for h in product(range(p),repeat=d)}
 cone=StrategyCone(p,m,actions)
 if cone.root!=rootq:raise AssertionError('root path lost')
 return cone,meta

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=7);ap.add_argument('--path',default='0,1,1,1,1');ap.add_argument('--J',default='2,3,4,5,6');ap.add_argument('--seconds',type=float,default=40);ap.add_argument('--rootcap',type=float,default=1);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();path=tuple(map(int,args.path.split(',')));J=tuple(map(int,args.J.split(',')))
 cone,meta=candidate(args.p,path,J,args.seconds,args.rootcap);print(json.dumps(meta),flush=True);record={'parameters':vars(args)|{'out':str(args.out)},'milp':meta}
 if cone is not None:
  result=cone.optimize(J);print(json.dumps(serializable({k:v for k,v in result.items() if k not in ('values','dual_support')})),flush=True)
  if result['certified']:
   point=integer_clones(result['values']);ins=instance_from_clones(cone.topics,cone.players,point);cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(ins,cert).assert_valid()
   if not independently_verify(cone,point):raise AssertionError('independent verify failed')
   W=ins.welfare(cone.root);OPT=ins.optimal_welfare();record.update({'strategy':cert.to_dict(),'clones':point,'W':W,'OPT':OPT,'ratio':Fraction(OPT,W),'path_utilities':ins.player_payoffs(path),'LP_value':result['value']})
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(serializable(record),indent=2)+'\n')
if __name__=='__main__':main()
