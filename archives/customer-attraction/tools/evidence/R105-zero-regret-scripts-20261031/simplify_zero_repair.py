"""Shrink only the already found counterexample to a universal repair claim."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

k=4
def coef(z,a):
    return np.array([6//sum(bool(mask>>b&1) for b in z) if mask>>a&1 else 0 for mask in range(1,16)],dtype=float)
def cov(z):return np.array([int(any(mask>>b&1 for b in z)) for mask in range(1,16)],dtype=float)
old=[2,2,1,2]
new=[2,3,1,1]
rows=[]; lower=[]
def add(c,margin):rows.append(c); lower.append(margin)
for r in range(k):
    for a in range(k):
        if a!=old[r]:add(coef((0,r,old[r]),old[r])-coef((0,r,a),a),1)
        if a!=new[r]:add(coef((r,new[r]),new[r])-coef((r,a),a),1)
    if r!=2:
        add(coef((0,2,1),2)-coef((0,r,old[r]),r),1)
        add(coef((2,1),2)-coef((r,old[r]),r),0)
    if r!=3:add(coef((3,1),3)-coef((r,new[r]),r),1)
add(cov((2,1))-cov((3,1)),1)
r=milp(np.ones(15),integrality=np.ones(15),bounds=Bounds(0,np.inf),constraints=LinearConstraint(rows,lower,np.inf),options={'time_limit':30})
if not r.success:raise RuntimeError(r.message)
w=[0]+list(map(lambda x:int(round(x)),r.x))
assert all(np.dot(c,w[1:])>=b for c,b in zip(rows,lower))
out={'weights':w,'background':0,'path':[2,1],'old_policy':old,'new_policy':new,'total_clients':sum(w),
     'purpose':'Counterexample to actual-regret-only welfare repair; not Q-CAG-HALF counterexample.'}
Path(__file__).with_name('zero_repair_simplified.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
