from pathlib import Path
import json,itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
ROOT=Path(__file__).parent
obj=json.loads((ROOT/'truncated_potential_candidate.json').read_text());q=obj['q'];r=obj['r'];policy={tuple(c):a for c,a in obj['policy']};masks=list(range(1,1<<q))
def comp(h):return tuple(h.count(a)for a in range(q))
def finish(h):
 while len(h)<r:h=h+(policy[comp(h)],)
 return h
def util(h,a):return [Fraction(1,sum((mask>>b)&1 for b in h))if mask>>a&1 else Fraction(0)for mask in masks]
rows=[];lb=[];ub=[]
for d in range(r):
 for h in itertools.product(range(q),repeat=d):
  a=policy[comp(h)];on=util(finish(h),a)
  for b in range(q):
   if b==a:continue
   off=util(finish(h+(b,)),b);rows.append([int(6*(x-y))for x,y in zip(on,off)]);lb.append(0);ub.append(np.inf)
actual=finish(());compmask=sum(1<<a for a in obj['comparison']);pot=[sum((Fraction(1,j)for j in range(1,sum((mask>>a)&1 for a in actual)+1)),Fraction(0))-int(bool(mask&compmask))for mask in masks]
rows.append([int(6*x)for x in pot]);lb.append(-np.inf);ub.append(-1)
# Distinct and nonempty topic sets.
for a in range(q):
 rows.append([int(bool(mask>>a&1))for mask in masks]);lb.append(1);ub.append(np.inf)
 for b in range(a):
  rows.append([int(bool(mask>>a&1)!=bool(mask>>b&1))for mask in masks]);lb.append(1);ub.append(np.inf)
res=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(np.array(rows),np.array(lb),np.array(ub)),options={'time_limit':30})
print(res.message,'objective',res.fun)
if res.x is not None:
 obj['weights']={mask:int(round(v))for mask,v in zip(masks,res.x)if v>.5};obj['integer_weights']=True;obj['minimization_message']=res.message;(ROOT/'harmonic_obstruction_minimized.json').write_text(json.dumps(obj,indent=2)+'\n');print(obj['weights'])
