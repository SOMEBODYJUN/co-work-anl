#!/usr/bin/env python3
"""Restricted count-Markov SPE candidate MILP, NOT a complete-SPE reduction."""
from pathlib import Path
import sys,time,json
from itertools import product
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,independently_verify,serializable
from terminal_cap_iteration import optimize


def compositions(total,p):
 if p==1:
  yield (total,);return
 for first in range(total+1):
  for rest in compositions(total-first,p-1):yield (first,)+rest


def inc(k,a):return tuple(x+(i==a) for i,x in enumerate(k))

def solve(p,path,seconds):
 m=len(path);n=(1<<p)-1;root=(0,)*p;q=tuple(path.count(a) for a in range(p))
 nodes=tuple(k for d in range(m) for k in compositions(d,p))
 u={};z={};num=n
 for k in nodes:
  for a in range(p):u[k,a]=num;num+=1
 for k in nodes:
  for a in range(p):z[k,a]=num;num+=1
 lo=np.zeros(num);hi=np.full(num,m,dtype=float);integ=np.zeros(num,dtype=np.uint8)
 for idx in z.values():hi[idx]=1;integ[idx]=1
 k=root
 for a in path:lo[z[k,a]]=hi[z[k,a]]=1;k=inc(k,a)
 hi[u[root,path[0]]]=1
 rows=[];cols=[];vals=[];lower=[];upper=[]
 def add(row,lb=-np.inf,ub=np.inf):
  ix=len(lower)
  for j,v in row.items():
   if v:rows.append(ix);cols.append(j);vals.append(float(v))
  lower.append(lb);upper.append(ub)
 def child(k,t):
  if sum(k)<m:return {u[k,t]:1}
  if not k[t]:return {}
  return {j:v for j,v in enumerate(payoff_row(p,k,t)) if v}
 def diff(k,t,ch,ct):
  row={u[k,t]:1}
  for j,v in child(ch,ct).items():row[j]=row.get(j,0)-v
  return row
 w=coverage_row(p,[a for a,c in enumerate(q) if c]);add({j:v for j,v in enumerate(w) if v},1,1)
 add({j:1 for j in range(n)},ub=m*p)
 for a in range(p):
  row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u[root,path[0]]]=-m;add(row,ub=0)
 add({u[root,a]:c for a,c in enumerate(q) if c},1,1)
 for k in nodes:
  add({z[k,a]:1 for a in range(p)},1,1)
  for a in range(p):
   for t in range(p):
    row=diff(k,t,inc(k,a),t);row[z[k,a]]=m;add(row,ub=m)
    row=diff(k,t,inc(k,a),t);row[z[k,a]]=-m;add(row,lb=-m)
   for b in range(p):
    if b==a:continue
    row=diff(k,a,inc(k,b),b);row[z[k,a]]=-m;add(row,lb=-m)
 A=coo_matrix((vals,(rows,cols)),shape=(len(lower),num)).tocsc()
 objective=np.zeros(num);objective[:n]=-m*np.array(payoff_row(p,q,path[-1]),dtype=float)
 started=time.monotonic()
 result=milp(objective,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lower),np.array(upper)),options={'time_limit':seconds,'mip_rel_gap':0.0})
 meta={'status':int(result.status),'message':result.message,'variables':num,'binary_actions':len(z),'decision_states':len(nodes),'constraints':len(lower),'elapsed_seconds':time.monotonic()-started,'floating_objective_not_certificate':float(-result.fun) if result.fun is not None else None}
 if result.x is None:return None,meta
 markov={k:max(range(p),key=lambda a:result.x[z[k,a]]) for k in nodes}
 actions={h:markov[tuple(h.count(a) for a in range(p))] for d in range(m) for h in product(range(p),repeat=d)}
 cone=StrategyCone(p,m,actions);assert cone.root==q
 exact=optimize(cone,path[-1])
 if exact is not None:assert independently_verify(cone,exact[1])
 return {'cap':str(exact[0]) if exact else None,'clones':exact[1] if exact else None,'markov_actions':[{'counts':k,'action':a} for k,a in sorted(markov.items())]},meta


def main():
 reports=[]
 for p,path,seconds in [(4,(0,0,0,0,1),20),(4,(0,0,1,1,2),20),(4,(0,1,1,2,3),20),(5,(0,0,0,0,0,1),20)]:
  result,meta=solve(p,path,seconds)
  rec={'topics':p,'path':path,'restricted_markov_scope':True,'result':result,'metadata':meta};reports.append(rec)
  print(json.dumps(serializable({k:v for k,v in rec.items() if k!='result'}|{'exact_cap':result['cap'] if result else None})),flush=True)
  Path(__file__).with_name('markov_cap_joint.json').write_text(json.dumps(serializable({'universal_claim':False,'reports':reports}),indent=2)+'\n')

if __name__=='__main__':main()
