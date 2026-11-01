"""All-customer-type necessary relaxation for terminal share; not a full SPE solver."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

def build(m):
 p=2*m-1; masks=list(range(1,1<<p));actual=list(range(m));branch=[m-1]+list(range(m,p))
 def payoff(path,i):
  return tuple(F(1,sum((b>>a)&1 for a in path)) if (b>>path[i])&1 else F(0) for b in masks)
 def conservative(prefix,r,a):
  return tuple(F(1,r+sum((b>>t)&1 for t in prefix)) if (b>>a)&1 else F(0) for b in masks)
 au=[payoff(actual,i) for i in range(m)];bu=[payoff(branch,i) for i in range(m)]
 rows=[];names=[]
 for which,path,u in [('actual',actual,au),('branch',branch,bu)]:
  start=0 if which=='actual' else 1
  for i in range(start,m):
   for a in range(p):
    v=conservative(path[:i],m-i,a)
    rows.append(tuple(x-y for x,y in zip(u[i],v)));names.append([which,i,a])
 rows.append(tuple(x-y for x,y in zip(au[0],bu[0])));names.append(['root actual vs last theme'])
 welfare=tuple(F(any((b>>a)&1 for a in actual)) for b in masks)
 return p,masks,actual,branch,au,bu,rows,names,welfare

if __name__=='__main__':
 import sys
 for m in map(int,sys.argv[1:] or [3,4,5]):
  p,masks,actual,branch,au,bu,rows,names,welfare=build(m)
  res=linprog(-np.array(au[-1],float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=np.array([welfare],float),b_eq=[1],bounds=(0,None),method='highs')
  out={'m':m,'status':res.message,'objective_last_share':-res.fun,'candidate_share':2/(m+1),'positive_types':[[b,F(float(x)).limit_denominator(10**6).__str__()] for b,x in zip(masks,res.x) if x>1e-7],'dual':[[name,F(float(-mu)).limit_denominator(10**6).__str__()] for name,mu in zip(names,res.ineqlin.marginals) if -mu>1e-7]}
  print(json.dumps(out),flush=True)
  Path(__file__).with_name(f'terminal_share_symbolic_m{m}.json').write_text(json.dumps(out,indent=2))
