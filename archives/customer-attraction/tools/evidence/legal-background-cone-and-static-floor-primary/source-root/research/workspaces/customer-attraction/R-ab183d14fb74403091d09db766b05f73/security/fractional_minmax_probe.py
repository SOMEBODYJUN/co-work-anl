"""Exploration of the free fractional-background minimax. Numeric only."""
import numpy as np
from scipy.optimize import minimize

def value(masks,weights,r,background=None):
    masks=np.array(masks,dtype=float);weights=np.array(weights,dtype=float)
    U,k=masks.shape
    background=np.zeros(U) if background is None else np.array(background,dtype=float)
    if r==1:
        pay=masks.T@(weights/(1+background));return float(max(pay)),np.zeros(k),pay
    def pay(q):return masks.T@(weights/(1+background+(r-1)*masks@q))
    def obj(y):return y[-1]
    def objjac(y):return np.r_[np.zeros(k),1.]
    def cfun(y):return y[-1]-pay(y[:-1])
    def cjac(y):
        d=1+background+(r-1)*masks@y[:-1]
        return np.c_[(r-1)*masks.T@(masks*(weights/d**2)[:,None]),np.ones(k)]
    q0=np.ones(k)/k;t0=max(pay(q0))
    out=minimize(obj,np.r_[q0,t0],jac=objjac,
      constraints=[{'type':'eq','fun':lambda y:np.sum(y[:-1])-1,'jac':lambda y:np.r_[np.ones(k),0.]},
                   {'type':'ineq','fun':cfun,'jac':cjac}],bounds=[(0,1)]*k+[(0,None)],
      method='SLSQP',options={'maxiter':500,'ftol':1e-11})
    if not out.success:raise RuntimeError(out.message)
    return float(out.x[-1]),out.x[:-1],pay(out.x[:-1])

if __name__=='__main__':
    import sys,json
    from pathlib import Path
    root=Path(__file__).resolve().parents[5]
    # Two existing valid full-SPE local-budget and individual-security witnesses.
    for name,r,counts,actual in [
        ('local_security_increment',3,{4:3,13:1,14:3,20:2,23:1,27:15,29:8,30:8,31:4,32:3,34:2,43:8,45:13,46:7,49:3,51:7,53:7,54:10,59:8},[0,3,4]),
        ('individual_security_failure',3,{4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2},[0,3,4])]:
        masks=np.array([[bool(mask&(1<<j)) for j in range(6)] for mask in counts],dtype=float)
        weights=np.array(list(counts.values()),dtype=float)
        bg=np.zeros(len(masks));vals=[]
        for i,a in enumerate(actual):
            v,q,pay=value(masks,weights,r-i,bg)
            vals.append(v);bg+=masks[:,a]
        denom=masks@np.bincount(actual,minlength=6)
        utilities=[float(np.sum(weights*masks[:,a]/np.maximum(denom,1))) for a in actual]
        debts=[utilities[i]+(r-i-1)*vals[i+1]-(r-i)*vals[i] for i in range(r-1)]
        print(json.dumps(dict(name=name,values=vals,utilities=utilities,debts=debts,aggregate=sum(utilities)-r*vals[0])))
