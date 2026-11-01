from pathlib import Path
import json,sys
from itertools import product,combinations
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,dot,integer_clones,independently_verify,serializable
ROOT=Path(__file__).resolve().parents[5]

def optimize(cone,a,J):
 norm=payoff_row(cone.topics,cone.root,a);o=coverage_row(cone.topics,J)
 r=linprog(-np.array(o,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([norm],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
 if not r.success:return {'status':r.message}
 w=tuple(F(float(x)).limit_denominator(10**7) for x in r.x)
 ok=cone.verify(w) and dot(norm,w)==1
 return {'status':'exact' if ok else 'float','ratio':str(dot(o,w)),'approx':-r.fun,'weights':w if ok else None,'J':J,'a':a}

def load_cone(path):
 raw=json.loads(path.read_text());game=json.loads((ROOT/'examples/customer_attraction'/path.name).read_text())
 actions={tuple(z['history']):z['action'] for z in raw['strategy']['actions']}
 return StrategyCone(len(game['topics']),game['players'],actions)
if __name__=='__main__':
 c=load_cone(ROOT/'evidence/certificates/customer_attraction/individual_security_failure.json')
 best=0
 for J in combinations(range(c.topics),c.players):
  r=optimize(c,c.actions[()],J)
  if r.get('approx',0)>best:
   best=r['approx'];print(json.dumps(serializable(r)),flush=True)
