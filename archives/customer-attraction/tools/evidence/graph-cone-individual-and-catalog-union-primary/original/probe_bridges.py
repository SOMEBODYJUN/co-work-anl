import json, sys, importlib.util
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('strategy_lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py');lib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lib;spec.loader.exec_module(lib)

def probe(cone,name):
 best_missing=(-float('inf'),None);best_individual=(-float('inf'),None)
 root_path=[];h=()
 while len(h)<cone.players:
  a=cone.actions[h];root_path.append(a);h=h+(a,)
 for J in combinations(range(cone.topics),min(cone.topics,cone.players)):
  o=lib.coverage_row(cone.topics,J)
  objectives=[('missing',None,tuple((1-c)*v-c for c,v in zip(cone.welfare,o)))]
  for i,a in enumerate(root_path):
   u=lib.payoff_row(cone.topics,cone.root,a)
   objectives.append(('individual',i,tuple(v-2*cone.players*t for v,t in zip(o,u))))
  for typ,i,obj in objectives:
   res=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
   if not res.success:raise RuntimeError(res.message)
   val=-res.fun
   if typ=='missing' and val>best_missing[0]:best_missing=(val,J)
   if typ=='individual' and val>best_individual[0]:best_individual=(val,(J,i))
   if val>1e-7:
    vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(vals) or lib.dot(cone.welfare,vals)!=1: vals=cone.recover_vertex(res.x)
    if vals is None or not cone.verify(vals) or lib.dot(cone.welfare,vals)!=1: continue
    exact=lib.dot(obj,vals)
    if exact<=0:continue
    clones=lib.integer_clones(vals)
    assert lib.independently_verify(cone,clones)
    out={'name':name,'type':typ,'player':i,'J':J,'objective':str(exact),'root_path':root_path,'clones':clones,'actions':[{'history':h,'action':a} for h,a in cone.actions.items()]}
    path=Path(__file__).parent/f'bridge_counterexample_{name}_{typ}_{i}.json'
    path.write_text(json.dumps(out,indent=2))
    print('FOUND',typ,name,i,J,exact,path,flush=True)
    return out
 print('SAFE',name,'missing',best_missing,'individual',best_individual,flush=True)

if __name__=='__main__':
 for name in ['individual_security_failure','root_tax_failure']:
  d=json.load(open(ROOT/f'evidence/certificates/customer_attraction/{name}.json'))
  acts={tuple(x['history']):x['action'] for x in d['strategy']['actions']}
  p=max(max(h,default=0) for h in acts)+1;n=max(map(len,acts))+1
  probe(lib.StrategyCone(p,n,acts),name)
