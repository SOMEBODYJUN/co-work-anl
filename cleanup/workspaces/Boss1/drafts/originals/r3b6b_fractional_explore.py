"""Exploratory fractional log benchmark. Numerical findings are not proofs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
import json, numpy as np
from scipy.optimize import minimize
from customer_attraction.model import Instance

def benchmark(ins,b):
 r=ins.players-sum(b); k=ins.topic_count
 C=np.array([[int(a in x.topics) for a in range(k)] for x in ins.customers],float)
 w=np.array([x.multiplicity for x in ins.customers],float)
 z=C@np.array(b,float)
 if r==1:return max(C.T@(w/(1+z))),None
 def obj(q):return -sum(w*np.log(1+z+(r-1)*(C@q)))
 def jac(q):return -(r-1)*(C.T@(w/(1+z+(r-1)*(C@q))))
 opt=minimize(obj,np.full(k,1/k),jac=jac,method='SLSQP',bounds=[(0,1)]*k,constraints=[{'type':'eq','fun':lambda q:sum(q)-1,'jac':lambda q:np.ones(k)}],options={'ftol':1e-11,'maxiter':1000})
 g=C.T@(w/(1+z+(r-1)*(C@opt.x)))
 return float(g@opt.x), {'q':opt.x.tolist(),'g':g.tolist(),'success':opt.success,'error':max(g)-g@opt.x}
if __name__=='__main__':
 ins=Instance.from_dict(json.loads(Path(sys.argv[1]).read_text()))
 for b in [(0,)*ins.topic_count,(1,)+(0,)*(ins.topic_count-1)]:
  print(b,benchmark(ins,b))
