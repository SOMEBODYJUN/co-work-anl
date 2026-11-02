"""Candidate generator: all histories, deviations only to a benchmark J.
Not SPE unless the omitted action comparisons also pass.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import CustomerType,Instance,ExactSPESolver
from customer_attraction.exact import _increment

class RestrictedSolver(ExactSPESolver):
 def __init__(self,instance,J):
  super().__init__(instance);self.J=J
 def _solve(self,k):
  if k in self._outcomes:return self._outcomes[k]
  if sum(k)==self.instance.players:result=frozenset({k})
  else:
   children=[self._solve(_increment(k,a)) for a in range(self.instance.topic_count)]
   floor=max(min(self._utility(q,a) for q in children[a]) for a in self.J)
   self._thresholds[k]=floor
   result=frozenset(q for a,ch in enumerate(children) for q in ch if self._utility(q,a)>=floor)
  self._outcomes[k]=result;return result

def terms(actions,n,p):
 out={}
 for d in range(n,-1,-1):
  for h in product(range(p),repeat=d):
   out[h]=tuple(h.count(a) for a in range(p)) if d==n else out[h+(actions[h],)]
 return out
@lru_cache(None)
def form(a,q):
 return tuple(F(1,sum(q[b] for b in range(len(q)) if mask>>b&1)) if mask>>a&1 else F(0) for mask in range(1,1<<len(q)))
def optimize(actions,n,p,J):
 ts=terms(actions,n,p);rows=set()
 for h,a in actions.items():
  actual=form(a,ts[h])
  for b in J:
   rows.add(tuple(x-y for x,y in zip(actual,form(b,ts[h+(b,)]))))
 rows=tuple(rows);G=np.array(rows,dtype=float)
 rootmask=sum(1<<a for a,c in enumerate(ts[()]) if c)
 c=tuple(F(bool(mask&rootmask)) for mask in range(1,1<<p))
 jm=sum(1<<a for a in J);o=tuple(F(bool(mask&jm)) for mask in range(1,1<<p))
 lp=linprog(-np.array(o,dtype=float),A_ub=-G,b_ub=np.zeros(len(rows)),A_eq=np.array([c],dtype=float),b_eq=[1.],bounds=(0,None),method='highs')
 if not lp.success:return None
 w=tuple(F(float(x)).limit_denominator(10000000) for x in lp.x)
 exact=all(sum(x*y for x,y in zip(row,w))>=0 for row in rows) and sum(x*y for x,y in zip(c,w))==1
 val=sum(x*y for x,y in zip(o,w))
 return dict(value=str(val),float_value=-lp.fun,exact=exact,w=w,root=ts[()],rows=len(rows),ts=ts)
def audit(actions,ts,w,n,p,J):
 neg=[];kept=0
 for h,a in actions.items():
  ua=sum(x*y for x,y in zip(form(a,ts[h]),w))
  for b in range(p):
   ub=sum(x*y for x,y in zip(form(b,ts[h+(b,)]),w));gap=ua-ub
   if b in J:assert gap>=0;kept+=1
   elif gap<0:neg.append((h,b,str(gap)))
 return dict(kept_comparisons=kept,omitted_negative_count=len(neg),negative_examples=neg[:12])

def run(n=4,p=6,rounds=20,seed=730):
 rng=random.Random(seed);J=tuple(range(n));best=0;reports=[]
 for step in range(rounds):
  masses={mask:rng.choice([0,0,0,1,1,2,3,5,8]) for mask in range(1,1<<p)}
  if step%4==0:
   # sparse incidence and private clients generate different backward regions.
   masses={mask:(rng.randint(1,10) if mask.bit_count()<=2 and rng.random()<.5 else 0) for mask in range(1,1<<p)}
  ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),v) for mask,v in masses.items() if v),n)
  solver=RestrictedSolver(ins,J);target=min(solver.outcomes(),key=lambda q:(ins.welfare(q),q))
  cert=solver.certificate(target)
  got=optimize(cert.actions,n,p,J)
  if got is None:continue
  val=got['float_value']
  if val>best+1e-7:
   best=val;record=dict(step=step,value=got['value'],float_value=val,exact=got['exact'],root=got['root'],rows=got['rows']);reports.append(record)
   print(json.dumps(record),flush=True)
   if got['exact']:
    record['audit']=audit(cert.actions,got['ts'],got['w'],n,p,J)
    record['masses']={mask:str(v) for mask,v in enumerate(got['w'],1) if v}
    record['actions']=[dict(h=h,a=a) for h,a in sorted(cert.actions.items())]
   Path(__file__).with_name('benchmark_restriction_probe.json').write_text(json.dumps(dict(players=n,topics=p,J=J,rounds=step+1,best=reports),indent=2))
  if val>2+1e-7 and got['exact']:break
 return reports
if __name__=='__main__':run(*map(int,sys.argv[1:]))
