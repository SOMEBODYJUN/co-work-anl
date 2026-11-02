"""LP candidate attack after payoff-graph compression of a fixed full strategy.
Integer-scaled rows preserve all original history comparisons. Floating answers
are candidates only; a reported FATAL requires integer-clone exact verification.
"""
from pathlib import Path
import json,sys
from math import lcm,gcd
from itertools import combinations,product
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,verify_certificate,StrategyCertificate

class GraphCone:
 def __init__(self,p,n,actions):
  self.p=p;self.n=n;self.actions=actions;L=lcm(*range(1,n+1));self.L=L
  terminal={}
  for d in range(n,-1,-1):
   for h in product(range(p),repeat=d):terminal[h]=tuple(h.count(a)for a in range(p))if d==n else terminal[h+(actions[h],)]
  self.terminal=terminal;root=[];h=()
  while len(h)<n:a=actions[h];root.append(a);h+=(a,)
  self.path=root;self.rootq=terminal[()]
  pairs=set()
  for h,a in actions.items():
   t=(a,terminal[h])
   for b in range(p):
    s=(b,terminal[h+(b,)])
    if s!=t:pairs.add((s,t))
  vertices=sorted({v for edge in pairs for v in edge});ix={v:i for i,v in enumerate(vertices)}
  masks=np.arange(1,1<<p,dtype=np.int64);bits=((masks[:,None]>>np.arange(p))&1).astype(np.int16)
  self.bits=bits
  fs=np.empty((len(vertices),len(masks)),dtype=np.int16)
  for i,(a,q)in enumerate(vertices):
   load=bits@np.array(q,dtype=np.int16);hit=bits[:,a].astype(bool)
   fs[i,:]=0;fs[i,hit]=L//load[hit]
  rows=np.array([fs[ix[t]]-fs[ix[s]]for s,t in sorted(pairs)],dtype=np.int16)
  self.rows=np.unique(rows,axis=0);self.matrix=-self.rows.astype(float)
  self.rootpay={a:self.f(a,self.rootq)for a in set(root)}
  print('COMPRESSED',p,n,'histories',len(actions),'vertices',len(vertices),'edges',len(pairs),'rows',len(self.rows),flush=True)
 def f(self,a,q):
  load=self.bits@np.array(q,dtype=np.int16);hit=self.bits[:,a].astype(bool)
  result=np.zeros(len(load),dtype=np.int16);result[hit]=self.L//load[hit];return result
 def exact(self,x):
  vals=[Fraction(float(t)).limit_denominator(10**7)for t in x]
  denominator=lcm(*(t.denominator for t in vals));clones=[int(t*denominator)for t in vals]
  common=gcd(*clones);clones=[t//common for t in clones]
  support=[(i,t)for i,t in enumerate(clones)if t]
  for row in self.rows:
   if sum(int(row[i])*t for i,t in support)<0:return None
  return clones
 def optimize(self,J,a):
  o=np.any(self.bits[:,J],axis=1).astype(float)
  u=self.rootpay[a].astype(float)/self.L
  res=linprog(-o,A_ub=self.matrix,b_ub=np.zeros(len(self.rows)),A_eq=[u],b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:raise RuntimeError(res.message)
  beta=-res.fun
  if beta>2*self.n-1+1e-7 and len(J)<=self.n:
   clones=self.exact(res.x)
   if clones:
    O=sum(t for z,t in enumerate(clones)if any(self.bits[z,b]for b in J));ui=Fraction(sum(int(k)*t for k,t in zip(self.rootpay[a],clones)),self.L)
    if O>(2*self.n-1)*ui:
     obj={'scope':'fixed complete SPE strong individual bridge counterexample; not necessarily half failure','p':self.p,'n':self.n,'J':list(J),'player_topic':a,'rootpath':self.path,'clones':clones,'O':O,'ui':str(ui),'actions':[{'history':h,'action':b}for h,b in self.actions.items()]}
     path=Path(__file__).parent/'strong_individual_counterexample.json';path.write_text(json.dumps(obj,indent=2));print('FATAL',O,ui,O/ui,path,flush=True);return obj
  return beta

if __name__=='__main__':
 cert=json.load(open(ROOT/'evidence/certificates/customer_attraction/five_individual_security.json'))
 actions={tuple(x['history']):x['action']for x in cert['strategy']['actions']}
 cone=GraphCone(10,5,actions)
 # Total catalog union is a stronger target; one successful bound certifies every J.
 print('TOTAL_UNION_AUXILIARY',cone.optimize(tuple(range(10)),cone.path[0]),flush=True)
 # Representative comparison covers all original customers; variants are then exhaustive.
 Js=list(combinations(range(10),5));preferred=(0,1,2,4,9);Js.remove(preferred);Js.insert(0,preferred)
 best=0
 for k,J in enumerate(Js):
  value=cone.optimize(J,cone.path[0])
  if isinstance(value,dict):break
  if value>best:best=value;print('BEST',k,J,best,flush=True)
  if k%20==0:print('PROGRESS',k,'of',len(Js),flush=True)
 else:print('DONE',best,flush=True)
