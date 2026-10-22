"""Floating discovery: jointly attack the full-terminal extra-one construction.

This tests a stronger construction than EXTRA-ONE-LEADER and cannot disprove
that free-background candidate unless a separate convex lower bound is supplied.
All complete-history policy inequalities are retained. Output is not a proof.
"""
from pathlib import Path
import argparse, json, random, sys, time
import numpy as np
from scipy.optimize import linprog, minimize

ROOT = Path(__file__).resolve().parents[5]
OLD = ROOT/'research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security'
sys.path.insert(0, str(OLD))
from extra_mass_probe import game_policy

OUT = Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--games',type=int,default=200)
    ap.add_argument('--starts',type=int,default=8)
    ap.add_argument('--rounds',type=int,default=8)
    ap.add_argument('--seed',type=int,default=977310)
    args=ap.parse_args()
    rng=random.Random(args.seed); nr=np.random.default_rng(args.seed)
    rows=[]; best=-1e99; begin=time.time()
    for game in range(args.games):
        k=rng.choice([4,5,6]);r=rng.choice([3,4,5])
        member=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)],dtype=float)
        past=[0]*k
        for _ in range(rng.randrange(9)): past[rng.randrange(k)]+=1
        w0=np.array([rng.randrange(1,20) if rng.random()<.35 else 0 for _ in range(1,(1<<k))],dtype=int)
        if not np.any(w0): continue
        G,c,actions,target=game_policy(w0,member,r,past,rng)
        def terminal(h):
            while len(h)<r: h=h+(actions[h],)
            return np.bincount(h,minlength=k)
        T=np.array([terminal((a,)) for a in range(k)])
        loads=T@member; beta=1+np.array(past)@member
        def coeff(p): return (p@member)/(beta+p@loads)
        def maximize_p(w,p):
            def fun(pp):
                t=pp@member;den=beta+pp@loads
                return -np.dot(w,t/den)
            def jac(pp):
                t=pp@member;den=beta+pp@loads
                return -(member@(w/den)-loads@(w*t/den**2))
            ans=minimize(fun,p,jac=jac,bounds=[(0,1)]*k,
                constraints=[{'type':'eq','fun':lambda pp:pp.sum()-1,'jac':lambda pp:np.ones(k)}],
                method='SLSQP',options={'maxiter':400,'ftol':1e-12})
            return ans.x,-ans.fun
        for start in range(args.starts):
            p=nr.dirichlet(np.ones(k)*rng.choice([.1,.3,1.,3.]))
            w=w0.astype(float)/np.dot(c,w0)
            for step in range(args.rounds):
                p,value=maximize_p(w,p)
                f=coeff(p)
                ans=linprog(c-f,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=c[None,:],b_eq=[1.],bounds=(0,None),method='highs')
                if not ans.success:break
                w=ans.x;gap=-ans.fun
                if gap>best+1e-9:
                    best=gap
                    rec={'game':game,'start':start,'step':step,'topics':k,'remaining':r,'past':past,'gap':gap,'elapsed':time.time()-begin}
                    print(json.dumps(rec),flush=True)
                if gap>1e-7:
                    packet=dict(status='FLOATING CANDIDATE ONLY',topics=k,remaining=r,past=past,weights=w.tolist(),p=p.tolist(),gap=gap,
                        actions=[{'history':list(h),'action':a} for h,a in sorted(actions.items())],path=list(target))
                    (OUT/'push_joint_candidate.json').write_text(json.dumps(packet,indent=2)+'\n')
                    return
        rows.append({'game':game,'topics':k,'remaining':r,'past':past,'best_so_far':best})
        if game%10==0:print(json.dumps({'games':game+1,'best':best,'elapsed':time.time()-begin}),flush=True)
    report=dict(status='finite floating no separation',seed=args.seed,games=args.games,starts=args.starts,rounds=args.rounds,best=best,elapsed=time.time()-begin,runs=rows)
    (OUT/'push_joint_numerical.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='runs'}),flush=True)


if __name__=='__main__': main()
