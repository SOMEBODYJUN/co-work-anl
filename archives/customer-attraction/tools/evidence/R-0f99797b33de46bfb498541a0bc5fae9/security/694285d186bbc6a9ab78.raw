"""Diagnostic only: complete SPE strategy cone with fixed iid Nash q.
The tested target is first-mover u >= lambda_(r+1)(b), not a sum bridge.
Every ordered-history incentive is included (duplicate rows may be removed).
"""
from pathlib import Path
import sys,json,itertools,math,random
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize,linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver
HERE=Path(__file__).parent

def iid(k,r,w,base):
    masks=np.arange(1,1<<k)
    mem=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
    bb=np.array(base)@mem
    def calc(q):
        t=q@mem
        gg=np.zeros(len(masks)); ff=np.zeros(len(masks))
        for j in range(r+2):
            prob=math.comb(r+1,j)*t**j*(1-t)**(r+1-j)
            hh=np.array([sum(1/(int(b)+l) for l in range(1,j+1)) for b in bb])
            ff+=prob*hh
        for j in range(r+1):
            gg+=math.comb(r,j)*t**j*(1-t)**(r-j)/(bb+j+1)
        return -w@ff,-(r+1)*(mem@(w*gg)),mem*gg
    res=minimize(lambda q:calc(q)[:2],np.ones(k)/k,jac=True,bounds=[(0,1)]*k,
        constraints={'type':'eq','fun':lambda q:sum(q)-1,'jac':lambda q:np.ones(k)},method='SLSQP',options={'ftol':1e-12,'maxiter':100})
    q=np.maximum(0,res.x);q/=sum(q)
    a=calc(q)[2]@w
    return q,float(q@a),float(max(a)-q@a)

def policy(k,r,w,base,seed):
    # Exact BI with prefix fixed; reconstruct only the subtree below base.
    I=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),int(x)) for mask,x in enumerate(w,1) if x),r+sum(base))
    E=ExactSPESolver(I)
    E.outcomes(base)
    counts0=tuple(base)
    root_floor=E.threshold(base)
    rng=random.Random(seed)
    choices={}
    def rec(h,c,desired=None):
        if len(h)==r:return
        floor=E.threshold(c)
        admiss=[]
        for a in range(k):
            cc=c[:a]+(c[a]+1,)+c[a+1:]
            for z in E.outcomes(cc):
                if E._utility(z,a)>=floor and (desired is None or z==desired):admiss.append((a,z))
        if len(h)==0:
            v=min(E._utility(z,a) for a,z in admiss)
            admiss=[(a,z) for a,z in admiss if E._utility(z,a)==v]
        a,z=rng.choice(admiss); choices[h]=a
        for b in range(k):
            cc=c[:b]+(c[b]+1,)+c[b+1:]
            if b==a:zz=z
            else:
                mini=min(E._utility(t,b) for t in E.outcomes(cc))
                zz=rng.choice([t for t in E.outcomes(cc) if E._utility(t,b)==mini])
            rec(h+(b,),cc,zz)
    rec((),counts0)
    return choices,float(root_floor)

def matrices(k,r,pol,base):
    masks=np.arange(1,1<<k)
    mem=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
    bb=np.array(base)@mem
    hs=[h for d in range(r) for h in itertools.product(range(k),repeat=d)]
    z={h:h for h in itertools.product(range(k),repeat=r)}
    for h in reversed(hs):z[h]=z[h+(pol[h],)]
    def util(a,t):
        loads=bb+mem[list(t)].sum(axis=0)
        return np.divide(mem[a],loads,out=np.zeros(len(masks)),where=loads>0)
    gam=np.array([util(pol[h],z[h])-util(a,z[h+(a,)]) for h in hs for a in range(k) if a!=pol[h]])
    gam=np.unique(np.round(gam,14),axis=0)
    return gam,util(pol[()],z[()]),mem,bb,z

def fixed_q(k,r,pol,base,q):
    gam,d,mem,bb,z=matrices(k,r,pol,base)
    t=q@mem
    g=sum(math.comb(r,j)*t**j*(1-t)**(r-j)/(bb+j+1) for j in range(r+1))
    alpha=mem*g
    av=q@alpha
    support=np.flatnonzero(q>1e-8)
    # Nash alpha_a<=avg, equality on support; sum w=1.
    ub=np.r_[-gam,alpha-av]
    eq=np.r_[np.ones((1,len(d))),alpha[support]-av]
    lp=linprog(d-av,A_ub=ub,b_ub=np.zeros(len(ub)),A_eq=eq,b_eq=np.r_[1,np.zeros(len(support))],bounds=(0,None),method='highs')
    return lp,dict(gamma_rows=len(gam),histories=len(pol),root=z[()],q=q.tolist(),base=base)

def main():
    rng=np.random.default_rng(235091)
    report=[];best=0
    for case in range(120):
        k=4 if case<50 else 5
        r=[3,4,5][case%3]
        base=[0]*k
        if case%4==1:base[int(rng.integers(k))]=1
        if case%4==2:
            for _ in range(2):base[int(rng.integers(k))]+=1
        w=rng.integers(0,12,size=(1<<k)-1)
        w[rng.random(len(w))<.5]=0
        if not any(w):continue
        pol,u=policy(k,r,w,base,case)
        q,lam,err=iid(k,r,w,base)
        if err>1e-6:continue
        # rational q keeps the proposed exact certificate finite and reviewable.
        qq=np.array([int(round(v*10000)) for v in q]);qq=qq/qq.sum()
        lp,data=fixed_q(k,r,pol,base,qq)
        rec=dict(case=case,k=k,r=r,initial_u=u,initial_lambda=lam,q_kkt_error=err,lp_success=lp.success,**data)
        if lp.success:
            rec['gap']=float(-lp.fun)
            if -lp.fun>best:
                best=-lp.fun
                print('BEST',case,k,r,best,flush=True)
            if -lp.fun>1e-7:
                rec['weights']=lp.x.tolist();rec['policy']={','.join(map(str,h)):a for h,a in pol.items()}
                (HERE/'extra_iid_positive_float.json').write_text(json.dumps(rec,indent=2)+'\n')
                print('POSITIVE',json.dumps({key:rec[key] for key in ['case','k','r','gap','base','q']}),flush=True)
                report.append(rec);break
        report.append(rec)
        if case%10==0:print('case',case,'best',best,flush=True)
    (HERE/'extra_iid_probe_report.json').write_text(json.dumps({'status':'finite floating diagnostic, no general claim','cases':report,'best_gap':best},indent=2)+'\n')
if __name__=='__main__':main()
