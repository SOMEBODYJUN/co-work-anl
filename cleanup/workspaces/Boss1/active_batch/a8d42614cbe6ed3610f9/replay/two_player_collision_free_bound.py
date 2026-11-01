"""Necessary true-reply relaxation for collision-free two-player SPE.
LP dual discovery, followed by exact coefficient verification.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
names=['C','D','T1','T2','R1','R2'];p=len(names)
masks=[v for v in range(1,1<<p)if not(v&1 and v&2)]
def b(v,a):return (v>>a)&1
def u(a,bb):return [F(b(v,a),1+b(v,bb))for v in masks]
def sub(x,y):return [a-bb for a,bb in zip(x,y)]
def unit(a):return [F(b(v,a))for v in masks]
W=[F(bool(v&3))for v in masks];O=[F(bool(v&12))for v in masks]
rows=[];rn=[]
def add(row,name):rows.append(row);rn.append(name)
for j in range(2):add(sub(unit(0),u(2+j,4+j)),f'root_T{j+1}')
for a in range(2,p):add(sub(unit(1),u(a,0)),f'actual_last_{names[a]}')
for j in range(2):
 for a in range(p):
  if a!=4+j:add(sub(u(4+j,2+j),u(a,2+j)),f'BR_R{j+1}_{names[a]}')
sol=linprog(-np.array(O,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=[np.array(W,float)],b_eq=[1.],bounds=(0,None),method='highs')
print(sol.message,'ratio',-sol.fun)
beta=F(float(-sol.fun)).limit_denominator(1000000)
mult=[F(float(-d)).limit_denominator(1000000)for d in sol.ineqlin.marginals]
residual=[beta*w-o-sum(mm*rr[t]for mm,rr in zip(mult,rows))for t,(w,o)in enumerate(zip(W,O))]
assert min(residual)>=0 and min(mult)>=0
weights=[F(float(x)).limit_denominator(1000000)for x in sol.x]
assert all(sum(a*w for a,w in zip(row,weights))>=0 for row in rows)
assert sum(a*w for a,w in zip(W,weights))==1
assert sum(a*w for a,w in zip(O,weights))==beta
out={'names':names,'ratio':str(beta),'multipliers':{n:str(x)for n,x in zip(rn,mult)if x},'minimum_residual':str(min(residual)),'positive_residuals':[[v,str(x)]for v,x in zip(masks,residual)if x],'primal':[[v,str(w)]for v,w in zip(masks,weights)if w]}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
