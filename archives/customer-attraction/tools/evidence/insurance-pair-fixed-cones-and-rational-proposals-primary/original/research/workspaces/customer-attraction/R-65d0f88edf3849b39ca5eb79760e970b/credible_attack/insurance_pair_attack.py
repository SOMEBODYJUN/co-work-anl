"""Attack only the universal insurance conjecture D>=3(h-ell).
H,L are fixed full SPE profiles; LP includes all their ordered-history ICs.
Not a search for fixed-player positive bounds or a proof of Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json, sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def path(actions,h=()):
 while h in actions: h += (actions[h],)
 return h

def urow(z,i,masks):
 a=z[i]
 return [F(bool(mask>>a&1),sum(bool(mask>>b&1) for b in z)) if mask>>a&1 else F(0) for mask in masks]

def icrows(actions,p,m,masks):
 rows=[]
 for k in range(m):
  for h in product(range(p),repeat=k):
   base=urow(path(actions,h),k,masks)
   for a in range(p):
    if a==actions[h]: continue
    dev=urow(path(actions,h+(a,)),k,masks)
    rows.append([x-y for x,y in zip(base,dev)])
 return rows

def main(name='root_tax_failure'):
 d=json.load(open(ROOT/'examples/customer_attraction'/f'{name}.json')); inst=Instance.from_dict(d.get('instance',d)); s=ExactSPESolver(inst); p=inst.topic_count; m=inst.players; masks=list(range(1,1<<p)); M=s.threshold((0,)*p)
 cases=[]
 for t in s.outcomes():
  for z in s.ordered_outcomes(t):
   h=inst.player_payoffs(z)[0]
   if h>M or not cases:
    cert=s.certificate(on_path=z)
    if not any(c[0]==z[0] and c[1]==t for c in cases): cases.append((z[0],t,h,cert.actions,z))
 lows=[]
 for t in s.outcomes():
  for z in s.ordered_outcomes(t):
   if inst.player_payoffs(z)[0]==M:
    lows.append((t,s.certificate(on_path=z).actions,z));break
  if lows:break
 if not lows: raise ValueError('no low profile')
 low=lows[0]; lr=urow(low[2],0,masks); lics=icrows(low[1],p,m,masks)
 best=None
 for a,t,h,actions,z in cases:
  hr=urow(z,0,masks); cr=[int(any(mask>>b&1 for b in z)) for mask in masks]
  rows=lics+icrows(actions,p,m,masks); A=-np.array(rows,dtype=float)
  # Every support is a legitimate m-topic comparison. The LP need not maximize actual OPT.
  for size in range(1,min(p,m)+1):
   for support in combinations(range(p),size):
    orow=[int(any(mask>>b&1 for b in support)) for mask in masks]
    objective=[3*(x-y)-2*c+o for x,y,c,o in zip(hr,lr,cr,orow)]
    res=linprog(-np.array(objective,dtype=float),A_ub=A,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success: continue
    value=-res.fun
    if best is None or value>best['float_objective']+1e-9:
     w=[F(float(x)).limit_denominator(100000) for x in res.x]
     exact_ic=min(sum(x*y for x,y in zip(row,w)) for row in rows)
     obj=sum(x*y for x,y in zip(objective,w))
     best={'float_objective':value,'exact_objective':str(obj),'min_exact_ic':str(exact_ic),'high_path':z,'low_path':low[2],'comparison':support,'weights':{str(mask):str(x) for mask,x in zip(masks,w) if x},'source':name}
     print(json.dumps(best),flush=True)
     if exact_ic>=0 and obj>0:
      (OUT/'insurance_pair_candidate.json').write_text(json.dumps(best,indent=2)+'\n')
      return
 (OUT/f'insurance_pair_{name}.json').write_text(json.dumps(best,indent=2)+'\n')

if __name__=='__main__': main(*sys.argv[1:])
