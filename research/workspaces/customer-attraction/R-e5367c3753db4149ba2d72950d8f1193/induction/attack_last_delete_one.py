"""LP attack LAST-DELETE-ONE on seven named old full-strategy cones.
No random strategy sampling. A rational witness, if any, is checked exactly.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import lcm,gcd
from functools import reduce
import json,sys
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
NAMES=['coverage_opportunity_failure','prefix_balance_failure','individual_security_failure','root_tax_failure','global_decorrelation_failure','residual_counterexample','local_security_increment']

def attack(name):
 inp=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text());p=len(inp['topics']);m=inp['players']
 raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text());s=raw.get('strategy',raw)
 acts={tuple(x['history']):x['action'] for x in s['actions']};kinds=list(range(1,1<<p))
 def leaf(h,stop=m):
  h=tuple(h)
  while len(h)<stop:h+=acts[h],
  return h
 def coeff(z,i):
  return [F(1,sum((mask>>a)&1 for a in z)) if (mask>>z[i])&1 else F() for mask in kinds]
 def sub(a,b):return [x-y for x,y in zip(a,b)]
 rows=[]
 for h in acts:
  c=coeff(leaf(h),len(h))
  for a in range(p):rows.append(sub(c,coeff(leaf(h+(a,)),len(h))))
 mat=np.array(rows,dtype=float)
 best=None;calls=0
 for h in acts:
  i=len(h)
  if i==m-1:continue
  # Retain every original ordered node, not only root.
  z=leaf(h);rhs=[x+y for x,y in zip(coeff(z,i),coeff(z,m-1))]
  for a in range(p):
   td=leaf(h+(a,),m-1);obj=sub(rhs,coeff(td,i));calls+=1
   res=linprog(np.array(obj,dtype=float),A_ub=-mat,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,len(kinds))),b_eq=[1],bounds=(0,None),method='highs')
   if res.success and res.fun < -1e-8:
    weights=[F(float(v)).limit_denominator(1000000) if v>1e-10 else F() for v in res.x]
    den=lcm(*(v.denominator for v in weights));ints=[int(v*den) for v in weights];g=reduce(gcd,ints);ints=[v//g for v in ints]
    slacks=[sum(v*w for v,w in zip(row,ints)) for row in rows];gap=sum(v*w for v,w in zip(obj,ints))
    assert min(slacks)>=0 and gap<0,(min(slacks),gap)
    witness=dict(source_cone=name,players=m,topics=inp['topics'],customers=[dict(mask=mask,multiplicity=w) for mask,w in zip(kinds,ints) if w],actions=s['actions'],history=h,deviation=a,actual_leaf=z,reduced_deviation_leaf=td,objective=str(gap),min_IC=str(min(slacks)),full_IC_rows=len(rows))
    (HERE/'last_delete_one_failure.json').write_text(json.dumps(witness,indent=2)+'\n')
    return dict(name=name,calls=calls,found=True,gap=str(gap),history=h,deviation=a)
 return dict(name=name,calls=calls,found=False)
if __name__=='__main__':
 reports=[]
 for n in NAMES:
  r=attack(n);reports.append(r);print(json.dumps(r),flush=True)
  if r['found']:break
 (HERE/'last_delete_one_attack_report.json').write_text(json.dumps(dict(candidate='max_T U_i(-last forced T) <= u_i+u_last on each old leaf',scope='fixed named exact full-strategy cones; floating LP only discovers; reported witness ICs and gap rational',reports=reports),indent=2)+'\n')
