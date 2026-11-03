"""Attack the exact general shared-load payment on full ordered-history SPE cones.

This is a counterexample search for SHARED, not a proof of SHARED or Q-CAG-HALF.
Every candidate strategy is full-history backward induction. Each fixed-policy
cone retains all original IC rows. The cutting-plane game optimizes customer
weights against convex shared loads for one fixed query distribution.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path
import json, random, sys
import numpy as np
from scipy.optimize import linprog, minimize

HERE=Path(__file__).resolve().parent

def make_policy(m,k,w,seed):
    rng=random.Random(seed); scale=lcm(*range(1,m+1))
    masks=np.arange(1,1<<k)
    inc=np.array([[(mask>>a)&1 for mask in masks] for a in range(k)])
    @lru_cache(None)
    def pay(z):
        load=inc[list(z)].sum(axis=0)
        return inc @ (np.array(w)*np.array([scale//v if v else 0 for v in load]))
    policy={}
    def solve(h):
        if len(h)==m:return h
        zs=[solve(h+(a,)) for a in range(k)]
        vals=[pay(z)[a] for a,z in enumerate(zs)]
        a=rng.choice([a for a,v in enumerate(vals) if v==max(vals)])
        policy[h]=a
        return zs[a]
    z=solve(())
    return policy,z,inc,scale

def data_for(m,k,policy,inc,scale):
    @lru_cache(None)
    def leaf(h):
        return h if len(h)==m else leaf(h+(policy[h],))
    @lru_cache(None)
    def coeff(z,i):
        load=inc[list(z)].sum(axis=0)
        return inc[z[i]]*np.array([scale//v if v else 0 for v in load])
    z=leaf(())
    rows=[]
    for h in policy:
        i=len(h);base=coeff(leaf(h),i)
        rows.extend(base-coeff(leaf(h+(a,)),i) for a in range(k))
    rows=np.unique(np.array(rows),axis=0)
    cover=(inc[list(z)].sum(axis=0)>0).astype(float)
    cols=np.array([[inc[[a for j,a in enumerate(leaf(z[:i]+(b,))) if j!=i]].sum(axis=0)
                    for b in range(k)] for i in range(m)],dtype=float)
    return z,rows,cover,cols

def minimize_query(m,k,w,rho,cols,start=None):
    if start is None:start=np.full(m*k,1/k)
    def value(q):
        L=np.einsum('ia,iax->x',q.reshape(m,k),cols)/m
        return np.sum(w*rho/(1+L))
    def jac(q):
        L=np.einsum('ia,iax->x',q.reshape(m,k),cols)/m
        return (-np.einsum('iax,x->ia',cols,w*rho/(1+L)**2)/m).ravel()
    eq=np.kron(np.eye(m),np.ones((1,k)))
    res=minimize(value,start,jac=jac,bounds=[(0,1)]*(m*k),
                 constraints=[{'type':'eq','fun':lambda q:eq@q-1,'jac':lambda q:eq}],
                 method='SLSQP',options={'maxiter':400,'ftol':1e-12})
    if not res.success and np.max(np.abs(eq@res.x-1))>1e-7:raise RuntimeError(res.message)
    L=np.einsum('ia,iax->x',res.x.reshape(m,k),cols)/m
    return res.fun,res.x,rho/(1+L)

def saddle(m,k,w,inc,cols):
    eq=np.c_[np.kron(np.eye(m),np.ones((1,k))),np.zeros(m)]
    def values(x):
        L=np.einsum('ia,iax->x',x[:-1].reshape(m,k),cols)/m
        return inc@(w/(1+L))
    def jacs(x):
        L=np.einsum('ia,iax->x',x[:-1].reshape(m,k),cols)/m
        j=-np.einsum('tx,iax,x->tia',inc,cols,w/(1+L)**2)/m
        return np.c_[j.reshape(k,m*k),np.zeros(k)]
    res=minimize(lambda x:x[-1],np.r_[np.full(m*k,1/k),1.],
                 jac=lambda x:np.r_[np.zeros(m*k),1.],
                 bounds=[(0,1)]*(m*k)+[(0,None)],
                 constraints=[{'type':'eq','fun':lambda x:eq@x-1,'jac':lambda x:eq},
                              {'type':'ineq','fun':lambda x:x[-1]-values(x),
                               'jac':lambda x:np.c_[np.zeros((k,m*k)),np.ones(k)]-jacs(x)}],
                 method='SLSQP',options={'maxiter':400,'ftol':1e-12})
    if not res.success:raise RuntimeError(res.message)
    # Recover a dual p on the active query rows by LP stationarity.
    L=np.einsum('ia,iax->x',res.x[:-1].reshape(m,k),cols)/m
    active=np.where(values(res.x)>res.fun-1e-7)[0]
    # A finite zero-sum dual over the current q plus pure/nearby columns suffices
    # only for choosing the next attack p; it is not used as a certificate.
    pp=np.ones(len(active))/len(active)
    p=np.zeros(k);p[active]=pp
    return res.fun,res.x[:-1],p

def attack_fixed_p(m,k,rows,cover,cols,p,inc,max_rounds=80):
    rho=p@inc;d=len(cover);cuts=[]
    # Include each row's simultaneous pure column and the uniform shared load.
    qs=[np.full(m*k,1/k)]
    for a in range(k):
        q=np.zeros((m,k));q[:,a]=1;qs.append(q.ravel())
    for q in qs:
        L=np.einsum('ia,iax->x',q.reshape(m,k),cols)/m
        cuts.append(rho/(1+L))
    best=None
    for it in range(max_rounds):
        A=np.r_[np.c_[-rows,np.zeros(len(rows))],
                np.array([np.r_[-cut,1.] for cut in cuts])]
        sol=linprog(np.r_[np.zeros(d),-1.],A_ub=A,b_ub=np.zeros(len(A)),
                    A_eq=[np.r_[cover,0.]],b_eq=[1.],
                    bounds=[(0,None)]*(d+1),method='highs')
        if not sol.success:return None
        w=sol.x[:-1]
        val,q,cut=minimize_query(m,k,w,rho,cols)
        best=dict(value=float(val),upper=float(sol.x[-1]),w=w.tolist(),p=p.tolist(),
                  q=q.tolist(),iterations=it+1)
        if sol.x[-1]-val<2e-8:return best
        cuts.append(cut)
    return best

def run(trials=20):
    rng=random.Random(26062501);best_ratio=0.;records=[]
    for trial in range(trials):
        # These sizes pressure-test the one all-m candidate; no positive
        # conclusion is drawn from absence of a finite counterexample.
        m,k=rng.choice([(3,4),(4,4),(5,4),(5,5),(4,5),(6,4)])
        w=np.array([rng.randrange(1,8) if rng.random()<.4 else 0 for _ in range((1<<k)-1)])
        if not w.any():w[0]=1
        policy,z,inc,scale=make_policy(m,k,w,rng.randrange(1<<30))
        z,rows,cover,cols=data_for(m,k,policy,inc,scale)
        ps=[np.full(k,1/k)]
        _,_,p=saddle(m,k,w,inc,cols);ps.append(p)
        ps.append(np.array([rng.random() for _ in range(k)]));ps[-1]/=sum(ps[-1])
        local=None
        for p in ps:
            out=attack_fixed_p(m,k,rows,cover,cols,p,inc)
            if out is not None and (local is None or out['value']>local['value']):local=out
        if local is None:continue
        ratio=m*local['value'];record=dict(trial=trial,m=m,k=k,actual=list(z),ratio=ratio,
                    upper_ratio=m*local['upper'],iterations=local['iterations'])
        records.append(record)
        if ratio>best_ratio+1e-9:
            best_ratio=ratio
            payload=dict(scope='Exploratory exact-candidate cone attack, floating optimization; not a certificate',
                         record=record,details=local,policy=[dict(history=list(h),action=a) for h,a in policy.items()])
            (HERE/'shared_cone_best.json').write_text(json.dumps(payload,indent=2)+'\n')
        print(json.dumps(record),flush=True)
        (HERE/'shared_cone_run.json').write_text(json.dumps(dict(records=records,best_ratio=best_ratio),indent=2)+'\n')
        if ratio>1+1e-5:
            print('POSSIBLE SHARED COUNTEREXAMPLE: rational full IC and global KKT still required',flush=True)
            return

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 20)
