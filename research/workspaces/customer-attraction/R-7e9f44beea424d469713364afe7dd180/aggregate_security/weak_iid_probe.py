"""Root iid-potential KKT plus complete SPE-policy cone: numerical search only."""
import json,math,random
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,linprog
from customer_attraction import Instance,CustomerType,ExactSPESolver
from probe import policy_matrix
OUT=Path(__file__).resolve().parent
rng=random.Random(9748102)

def fg(n,t):
    F=sum((-1)**(j+1)*math.comb(n,j)*t**j/j for j in range(1,n+1))
    g=sum((-1)**(j+1)*math.comb(n,j)*t**(j-1)/n for j in range(1,n+1))
    return F,g

def optimal_iid(w,M,n):
    def fun(q):
        ft,gt=fg(n,q@M)
        return -w@ft,-n*(M@(w*gt))
    k=len(M)
    result=minimize(fun,np.ones(k)/k,jac=True,method='SLSQP',bounds=[(0,1)]*k,constraints={'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)},options={'ftol':1e-11,'maxiter':200})
    q=result.x.copy();q[q<1e-7]=0;q/=q.sum()
    t=q@M;Z=w@(1-(1-t)**n)
    return q,Z

def step(G,c,M,q,n):
    t=q@M;_,g=fg(n,t)
    Z=1-(1-t)**n
    E=M*g-Z/n
    A=np.vstack([-G,E])
    res=linprog(-Z,A_ub=A,b_ub=np.zeros(len(A)),A_eq=c[None,:],b_eq=[1.],bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(res.message)
    return res.x,-res.fun

best=1.
for n,k,runs in [(3,4,250),(3,6,150),(4,6,120),(5,7,80),(6,7,40)]:
 for trial in range(runs):
    cs=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,15)) for mask in range(1,1<<k) if rng.random()<rng.choice([.1,.3,.5,1.])]
    ins=Instance(tuple(map(str,range(k))),tuple(cs),n)
    sol=ExactSPESolver(ins);out=min(sol.outcomes(),key=ins.welfare)
    cert=sol.certificate(out,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
    G,c,M,R,qterminal=policy_matrix(cert.actions,n,k)
    w0=np.zeros((1<<k)-1)
    for cc in cs:w0[sum(1<<a for a in cc.topics)-1]=cc.multiplicity
    qi,z0=optimal_iid(w0,M,n)
    starts=[qi,np.ones(k)/k,np.random.default_rng(trial+1000*n).dirichlet(np.ones(k))]
    for st,q in enumerate(starts):
     w,Z=step(G,c,M,q,n)
     if Z>best+1e-7:
        best=Z
        rec=dict(n=n,k=k,trial=trial,start=st,Z_over_W=Z,weak_ratio=(1-1/(2*n))*Z,q=q.tolist(),weights=w.tolist(),actions={','.join(map(str,h)):int(a) for h,a in cert.actions.items()},on_path=qterminal,status='numerical_only')
        (OUT/'weak_iid_best.json').write_text(json.dumps(rec,indent=2)+'\n')
        print(json.dumps({x:rec[x] for x in ['n','k','trial','start','Z_over_W','weak_ratio']}),flush=True)
     if (1-1/(2*n))*Z>1+1e-6:
        print('WEAK_CANDIDATE',flush=True);raise SystemExit
print('FINISHED',best,flush=True)
