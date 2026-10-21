"""Discover FF-LEADER failures with nonempty legal prefix; numerical only."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog, minimize
from background_security_probe import build, compositions

HERE=Path(__file__).resolve().parent

def oracle(p,w,bits,base,q0=None):
    alpha=bits@p
    def fun(q):
        den=1+base+2*(bits@q)
        return np.sum(w*alpha/den)
    def jac(q):
        den=1+base+2*(bits@q)
        return -2*((w*alpha/den**2)@bits)
    res=minimize(fun,np.ones(6)/6 if q0 is None else q0,jac=jac,
      bounds=[(0,1)]*6,constraints=[dict(type='eq',fun=lambda q:q.sum()-1,jac=lambda q:np.ones(6))],
      method='SLSQP',options=dict(ftol=1e-12,maxiter=300))
    assert res.success,res.message
    return res.x,res.fun

def fractional(p,prefix):
    masks,gamma,_,cover=build(prefix,'leader')
    bits=np.array([[(t>>a)&1 for a in range(6)]for t in masks],float)
    base=bits@np.array(prefix);alpha=bits@p
    cuts=[alpha/(1+base+2*(bits@q)) for q in np.r_[np.eye(6),[np.ones(6)/6]]]
    q0=np.ones(6)/6
    for it in range(75):
        cutsmat=np.array(cuts)
        res=linprog(np.r_[cover,-1],
          A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-cutsmat,np.ones(len(cutsmat))]],
          b_ub=np.zeros(len(gamma)+len(cutsmat)),A_eq=[np.r_[np.ones(len(masks)),0]],b_eq=[1],
          bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
        if not res.success:return None
        w=res.x[:-1]; q0,lower=oracle(p,w,bits,base,q0)
        if res.x[-1]-lower<2e-9:break
        cuts.append(alpha/(1+base+2*(bits@q0)))
    return dict(prefix=prefix,gap=float(lower-cover@w),safe_lower=lower,leader=float(cover@w),
      p=p.tolist(),q=q0.tolist(),weights=[(int(t),float(x))for t,x in zip(masks,w)if x>1e-9],cuts=len(cuts))

def main():
    rng=np.random.default_rng(374)
    prefixes=[q for d in range(1,5) for q in compositions(d,6)
      if q[:3]==tuple(sorted(q[:3],reverse=True)) and q[3:]==tuple(sorted(q[3:],reverse=True))]
    trace=[];best=None
    for prefix in prefixes:
        for p in [np.ones(6)/6]+[rng.dirichlet(np.ones(6))for _ in range(2)]:
            item=fractional(p,prefix)
            if item is None:continue
            trace.append(item)
            if best is None or item['gap']>best['gap']+1e-9:
                best=item;print(json.dumps(dict(best=best,checked=len(trace))),flush=True)
            if item['gap']>1e-6:
                (HERE/'fractional_background_probe.json').write_text(json.dumps(dict(best=best,trace=trace),indent=2));return
    (HERE/'fractional_background_probe.json').write_text(json.dumps(dict(best=best,trace=trace),indent=2))
    print(json.dumps(dict(prefixes=len(prefixes),starts=len(trace),best=best)),flush=True)

if __name__=='__main__':main()
