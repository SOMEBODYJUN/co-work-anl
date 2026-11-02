"""First-two aggregate security is a stronger exploratory candidate."""
import json,random,sys
from pathlib import Path
import numpy as np
from customer_attraction import Instance,CustomerType,ExactSPESolver
from probe import policy_matrix,security,cone_step
OUT=Path(__file__).resolve().parent
rng=random.Random(51237218)
best=1e6
for n,k,runs in [(3,6,200),(4,6,300),(5,7,300),(6,7,200)]:
 for trial in range(runs):
    density=rng.choice([.08,.2,.5,1.])
    cs=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,21)) for mask in range(1,1<<k) if rng.random()<density]
    ins=Instance(tuple(map(str,range(k))),tuple(cs),n)
    solver=ExactSPESolver(ins);outcomes=solver.outcomes()
    q=min(outcomes,key=ins.welfare)
    cert=solver.certificate(q,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
    G,c,member,R,_=policy_matrix(cert.actions,n,k)
    w=np.zeros((1<<k)-1)
    for cc in cs:w[sum(1<<a for a in cc.topics)-1]=cc.multiplicity
    p,v=security(w,member,R)
    pref=None;u12=1e9;chosenq=None
    for q in outcomes:
        pay=ins.topic_payoffs(q)
        for a in range(k):
            h=[0]*k;h[a]+=1;h=tuple(h)
            if q not in solver.outcomes(h) or pay[a]<solver.threshold((0,)*k):continue
            for b in range(k):
                hh=list(h);hh[b]+=1;hh=tuple(hh)
                if q in solver.outcomes(hh) and pay[b]>=solver.threshold(h):
                    if pay[a]+pay[b]<u12:u12=pay[a]+pay[b];pref=(a,b);chosenq=q
    ratio=float(u12)/(2*v) if v else 1
    if ratio<best-1e-8:
        best=ratio;print(json.dumps(dict(n=n,k=k,trial=trial,ratio=ratio,prefix=pref,u12=str(u12),v=v)),flush=True)
    if ratio<1-1e-7:
        rec=dict(instance=ins.to_dict(),prefix=pref,outcome=chosenq,u12=str(u12),v=v,p=p.tolist(),ratio=ratio,status='numerical_only')
        (OUT/'prefix_pair_failure.json').write_text(json.dumps(rec,indent=2)+'\n')
        raise SystemExit
print('FINISHED',best,flush=True)
