import sys,numpy as np
from scipy.optimize import linprog
sys.path.insert(0,'/workspace/scratch/66f324ff79fa/co-work-anl/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d')
import m6_requery_lp as q
from fractions import Fraction as F
names,A,b,types=q.build(6,0,True,True,None,True)
groups=[]
groups += [[names.index(f'M{i}')] for i in range(6)]
groups += [[names.index('L0')],[names.index(f'L{j}') for j in range(1,6)],[names.index('L6')]]
groups += [[names.index('T00')],[names.index(f'T0{j}') for j in range(1,6)],[names.index('T06')],[names.index(f'T{j}{k}') for j in range(1,6) for k in range(j+1,6)],[names.index('T66')]]
groups += [[names.index('D0,0')]]
R=np.column_stack([A[:,g].sum(axis=1) for g in groups])
if __name__=='__main__':
 for objname,c in [('zero',np.zeros(R.shape[1])),('sum',np.ones(R.shape[1]))]:
  r=linprog(c,A_ub=R,b_ub=b,bounds=(0,None),method='highs'); print(objname,r.status,r.fun,min(b-R@r.x),len(r.x));
  print([(i,x,F(float(x)).limit_denominator(100000)) for i,x in enumerate(r.x) if x>1e-8])
