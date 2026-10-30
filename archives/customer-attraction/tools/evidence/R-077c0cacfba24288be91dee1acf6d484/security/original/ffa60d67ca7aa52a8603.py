"""Discovery: deform the known five-player individual-security input.

Two exchangeable groups; complement-pair types, two special complement
types, and two special private types. Exact set-valued BI root threshold;
the fractional cap is a one-variable convex symmetric minimization.
"""
import json,random
from pathlib import Path
from scipy.optimize import minimize_scalar
from customer_attraction import Instance,CustomerType,ExactSPESolver
OUT=Path(__file__).resolve().parent
rng=random.Random(271810)
best=0
for it in range(300):
    m=rng.choice([3,4]);a=rng.randrange(1,9);b=rng.randrange(0,10);c=rng.randrange(0,12);d=rng.randrange(0,8)
    k=2*m;omega=set(range(k));cs=[]
    for i in range(m):
        for j in range(m,2*m):cs.append(CustomerType(frozenset(omega-{i,j}),a+b*int(i==m-1 and j==2*m-1)))
    for s in [m-1,2*m-1]:
        if c:cs.append(CustomerType(frozenset(omega-{s}),c))
        if d:cs.append(CustomerType(frozenset({s}),d))
    ins=Instance(tuple(map(str,range(k))),tuple(cs),m);solver=ExactSPESolver(ins);u=solver.threshold([0]*k)
    def cap(y):
        x=(1-2*y)/(2*(m-1));l=m-1
        oo=1+l*(1-2*x);os=1+l*(1-x-y);ss=1+l*(1-2*y);co=1+l*(1-y)
        ordinary=a*((m-2)*(m-1)/oo+(2*m-3)/os+1/ss)+b/ss+2*c/co
        special=a*((m-1)**2/oo+(m-1)/os)+c/co+d/(1+l*y)
        return max(ordinary,special)
    ans=minimize_scalar(cap,bounds=(0,.5),method='bounded',options={'xatol':1e-13})
    val=min(ans.fun,cap(0),cap(.5));ratio=val/float(u)
    if ratio>best+1e-8:
        best=ratio;record={'status':'numerical discovery only','m':m,'a':a,'b':b,'c':c,'d':d,'root_min':str(u),'fractional_t':val,'ratio_t/root':ratio,'q_special_each':ans.x}
        print(json.dumps(record),flush=True)
    if ratio>1+1e-6:
        (OUT/'symmetric_family_candidate.json').write_text(json.dumps(record,indent=2)+'\n');break
else:print('FINISHED_NO_WITNESS',best,flush=True)
