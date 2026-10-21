import itertools,json
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
k=6;masks=list(range(1,1<<k));reply=[1,3,3,4,3,4]
def p(a,b):return np.array([int(mask>>a&1)*(2-int(mask>>b&1)) for mask in masks],dtype=float)
def cov(a,b):return np.array([int(mask&((1<<a)|(1<<b))!=0) for mask in masks],dtype=float)
W=cov(0,1);O=cov(2,5);R=O*(1-W)
rows=[];lb=[]
for a in range(k):
 for b in range(k):rows.append(p(reply[a],a)-p(b,a));lb.append(0)
 rows.append(p(0,1)-p(a,reply[a]));lb.append(0)
for a,b in itertools.combinations_with_replacement(range(k),2):
 if (a,b)!=(2,5):rows.append(O-cov(a,b));lb.append(1)
rows.append(R-W);lb.append(1)
res=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),bounds=Bounds(0,np.inf),constraints=LinearConstraint(np.array(rows),np.array(lb),np.inf),options={'time_limit':30})
print(res.message)
if res.x is not None:
 weights=np.rint(res.x).astype(int)
 assert np.all(np.dot(np.array(rows),weights)>=np.array(lb))
 obj={'reply':reply,'weights':{mask:int(w) for mask,w in zip(masks,weights) if w},'W':int(W@weights),'residual':int(R@weights),'OPT':int(O@weights),'customers':int(weights.sum())}
 print(json.dumps(obj,indent=2))
 open('research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/residual_unique_integer_discovery.json','x').write(json.dumps(obj,indent=2))
