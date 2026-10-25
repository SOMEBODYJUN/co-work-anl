"""Finite full-history IC-cone attack on the parent's q_i=p full-load helper."""
from attack_shared_cone import make_policy,data_for
from pooled_full_probe import attack
from fractions import Fraction
from math import lcm
from pathlib import Path
import json,random,sys
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent

def one(m,k,seed):
    rng=random.Random(seed)
    w=np.array([rng.randrange(1,7) if rng.random()<.25 else 0 for _ in range((1<<k)-1)])
    if not w.any():w[0]=1
    policy,z,inc,scale=make_policy(m,k,w,rng.randrange(1<<30))
    z,rows,cover,cols=data_for(m,k,policy,inc,scale)
    fullcols=cols+inc[None,:,:]
    avgfull=fullcols.mean(axis=0)
    ps=[np.full(k,1/k)]
    ps.extend(np.random.default_rng(seed).dirichlet(np.full(k,.5),8))
    best=(-1,None)
    for p0 in ps:
        p=p0.copy()
        for it in range(4):
            cost=(p@inc)/(1+p@avgfull)
            lp=linprog(-cost,A_ub=-rows,b_ub=np.zeros(len(rows)),
                       A_eq=[cover],b_eq=[1.],bounds=(0,None),method='highs')
            if not lp.success:continue
            ratio=-m*lp.fun
            if ratio>best[0]:
                best=(ratio,dict(p=p.tolist(),weights=lp.x.tolist(),iteration=it,
                                ic_min=float(np.min(rows@lp.x)),normalization=float(cover@lp.x)))
            if ratio>1+1e-6:
                # Rationalize both p and the exact full-IC cone weights.
                pf=[Fraction(float(a)).limit_denominator(100000) for a in p]
                pf[-1]+=1-sum(pf)
                wf=[Fraction(float(a)).limit_denominator(1000000) for a in lp.x]
                ics=[sum(int(a)*b for a,b in zip(row,wf)) for row in rows]
                W=sum(int(a)*b for a,b in zip(cover,wf))
                rho=[sum(pf[a]*int(inc[a,x]) for a in range(k)) for x in range(len(wf))]
                L=[sum(pf[a]*sum(int(fullcols[i,a,x]) for i in range(m)) for a in range(k))/m for x in range(len(wf))]
                F=sum(wf[x]*rho[x]/(1+L[x]) for x in range(len(wf)))
                if min(ics)>=0 and F>W/m and min(pf)>=0:
                    mult=lcm(*(a.denominator for a in wf))
                    return dict(exact_counterexample=True,m=m,k=k,actual=list(z),
                                p=[str(a) for a in pf],weights={str(mask):int(a*mult) for mask,a in enumerate(wf,1) if a},
                                normalized_gap=str(F-W/m),IC_min=str(min(ics)),
                                policy=[dict(history=list(h),action=a) for h,a in policy.items()])
            ans=attack(m,k,inc,lp.x,fullcols,1.)
            p=np.array(ans['p'])
    return dict(exact_counterexample=False,m=m,k=k,actual=list(z),ratio=float(best[0]),details=best[1])

if __name__=='__main__':
    rng=random.Random(2726025);records=[]
    for t in range(int(sys.argv[1]) if len(sys.argv)>1 else 24):
        m,k=rng.choice([(3,6),(4,5),(5,5),(5,6),(4,6),(3,7),(6,4)])
        out=one(m,k,rng.randrange(1<<30));records.append(out)
        print(json.dumps({k:v for k,v in out.items() if k not in ('policy','weights','details')}),flush=True)
        (HERE/'pooled_full_cone_attack.json').write_text(json.dumps(dict(scope='Exact-candidate finite attack; floating negatives are not proof',records=records),indent=2)+'\n')
        if out['exact_counterexample']:
            (HERE/'pooled_full_helper_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
            break
