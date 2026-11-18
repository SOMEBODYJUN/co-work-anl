"""Discover and exact-check a rational dual for one fixed strengthened B mode.
The saved certificate's acceptance uses Fractions, not solver status.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).parent
s=importlib.util.spec_from_file_location('cut',BASE/'probe_shared_B_TQ_cut.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
types,eq,ub,br=m.model(4,1)
pattern=[(0,1),(1,0),(2,3),(3,2)]
rows=list(ub);rhs=[1.0]*5;names=['extra-size-'+str(k) for k in range(5)]
for j,(a,y) in enumerate(pattern):
 rs,bs,ns,*_=br[j,a,y];rows.extend(rs);rhs.extend(bs);names.extend('branch'+str(j)+'-'+n for n in ns)
obj=np.zeros(len(types)+1);obj[-1]=1
z=linprog(obj,A_ub=np.array(rows),b_ub=np.array(rhs),A_eq=np.array(eq),b_eq=np.ones(6),bounds=[(0,None)]*(len(types)+1),method='highs')
assert z.success
lam=[F(float(x)).limit_denominator(10**8) for x in z.ineqlin.marginals]
y=[F(float(x)).limit_denominator(10**8) for x in z.eqlin.marginals]
A=[[F(float(x)).limit_denominator(60) for x in row] for row in rows]
E=[[F(float(x)).limit_denominator(60) for x in row] for row in eq]
b=[F(float(x)).limit_denominator(60) for x in rhs]
res=[F(int(k==len(types)))-sum((v*row[k] for v,row in zip(lam,A)),F())-sum((v*row[k] for v,row in zip(y,E)),F()) for k in range(len(types)+1)]
value=sum((v*x for v,x in zip(lam,b)),F())+sum(y,F())
assert all(v<=0 for v in lam)
assert min(res)>=0,(min(res),value)
assert value>=F(1,2)
cert={'scope':'One fixed B pair pattern and its extra-label/new-anchor renamings only; exact dual for a necessary relaxation, not full q5 or original-target proof.',
      'pattern':pattern,'bound':str(value),'columns':len(types)+1,'inequality_rows':len(rows),'equality_rows':6,
      'lambda':[str(v) for v in lam],'equality_dual':[str(v) for v in y],
      'nonzero_inequality_dual':[{'row':i,'name':names[i],'multiplier':str(v)} for i,v in enumerate(lam) if v],
      'minimum_reduced_cost':str(min(res)),'reduced_cost':[str(v) for v in res]}
(BASE/'shared-B-pair-TQ-rational-dual.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({k:v for k,v in cert.items() if k not in ('lambda','reduced_cost')},indent=2))
