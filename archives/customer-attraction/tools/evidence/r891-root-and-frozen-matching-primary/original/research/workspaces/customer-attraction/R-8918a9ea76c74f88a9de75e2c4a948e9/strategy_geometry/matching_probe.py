"""Target a stated all-input matching bridge inside saved full SPE cones.
No finite negative result establishes the bridge. A positive exact feasible
point refutes only this bridge, never half unless separately OPT>2W.
"""
from pathlib import Path
import sys, json
from itertools import combinations, permutations
from fractions import Fraction as F
import importlib.util
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('audit_cone', ROOT/'tests/audits/customer_attraction_strategy_lp.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

def probe(cone, comparators, optimal=True):
 p,m=cone.topics,cone.players;n=(1<<p)-1
 actual=[]
 h=()
 while len(h)<m:h=h+(cone.actions[h],)
 actual=list(h)
 c=cone.welfare;o=mod.coverage_row(p,set(comparators))
 e=tuple(ci*(1-oi) for ci,oi in zip(c,o))
 rows=[];ds=[]
 for pi in set(permutations(comparators)):
  d=[F(0)]*n
  for i,T in enumerate(pi):
   q=list(cone.root);q[actual[i]]-=1;q[T]+=1
   r=mod.payoff_row(p,tuple(q),T)
   d=[a+b for a,b in zip(d,r)]
  ds.append(tuple(d));rows.append([float(cj+ej-dj) for cj,ej,dj in zip(c,e,d)]+[1.])
 Aub=[[-float(x) for x in r]+[0.] for r in cone.rows]
 if optimal:
  for J in combinations(range(p),min(m,p)):
   oo=mod.coverage_row(p,J)
   Aub.append([float(a-b) for a,b in zip(oo,o)]+[0.])
 Aub.extend(rows)
 res=linprog([0.]*n+[-1.],A_ub=Aub,b_ub=[0.]*len(Aub),A_eq=[[float(x) for x in c]+[0.]],b_eq=[1.],bounds=[(0,None)]*n+[(None,None)],method='highs')
 if not res.success:return {'status':res.message}
 val=-res.fun
 if val<=1e-8:return {'value':val}
 w=[F(float(x)).limit_denominator(10**6) for x in res.x[:n]]
 if not cone.verify(w) or mod.dot(c,w)!=1:return {'value':val,'exact':False}
 if optimal and any(mod.dot(mod.coverage_row(p,J),w)>mod.dot(o,w) for J in combinations(range(p),min(m,p))):return {'value':val,'exact':False}
 exact=min(mod.dot(d,w) for d in ds)-mod.dot(c,w)-mod.dot(e,w)
 clones=mod.integer_clones(w)
 return {'value':val,'exact':str(exact),'clones':clones,'comparators':comparators,'actual':actual,'direct_verified':mod.independently_verify(cone,clones)}

def main():
 d=json.load(open(ROOT/'evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json'))
 best={'value':-1};num=0
 for ci,entry in enumerate(d['cone_proofs']):
  cone=mod.StrategyCone(5,4,{tuple(x['history']):x['action'] for x in entry['actions']})
  for J in combinations(range(5),4):
   r=probe(cone,J);num+=1
   if r.get('value',-1)>best['value']:
    best=dict(r,cone=ci);print('best',json.dumps(best),flush=True)
   if r.get('exact') not in (None,False) and F(r['exact'])>0:
    out=dict(r,cone=ci,actions=entry['actions'],scope='only a counterexample to frozen matching bridge')
    Path(__file__).with_name('matching_bridge_counterexample.json').write_text(json.dumps(out,indent=2));return
 print(json.dumps({'probes':num,'best':best,'universal_bridge_proved':False}))
if __name__=='__main__':main()
