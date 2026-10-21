"""Same CCE-cone attack on existing full-tree bridge obstruction policies."""
import json,random,time
from pathlib import Path
import numpy as np
from cone_cce_search import geometry,cce_geometry,cce_dual,cone_step
ROOT=Path(__file__).resolve().parents[5]
CASES=[('individual_security_failure','individual_security_failure','strategy'),('local_security_increment','local_security_increment','strategy'),('global_decorrelation_failure','global_decorrelation_failure','strategy'),('dynamic_iid_local','dynamic_iid_local','certificate')]
results=[];rng=random.Random(20261022)
for name,stem,key in CASES:
    ins=json.loads((ROOT/f'examples/customer_attraction/{stem}.json').read_text())
    pack=json.loads((ROOT/f'evidence/certificates/customer_attraction/{stem}.json').read_text())
    raw=pack[key];policy={tuple(a['history']):a['action'] for a in raw['actions']}
    n,k=ins['players'],len(ins['topics'])
    w=np.zeros((1<<k)-1)
    for t in ins['customers']:
        mask=sum(1<<a for a in t['topics'])
        if mask:w[mask-1]+=t.get('multiplicity',1)
    gamma,_,I,c,z=geometry(n,k,policy);W,H,C=cce_geometry(n,k,I)
    lam,base=cce_dual(W,H,I,w)
    starts=[lam]+[np.array([rng.expovariate(1) for a in range(k)])*rng.uniform(.1,3)/k for _ in range(4)]
    attempts=[];best=0
    for s,lam in enumerate(starts):
        for it in range(5):
            lp,D=cone_step(gamma,c,W,H,I,lam)
            att=dict(start=s,iteration=it,status=int(lp.status),message=lp.message)
            if not lp.success:attempts.append(att);break
            lam,primal=cce_dual(W,H,I,lp.x[:-1]);best=max(best,primal.fun)
            att.update(dual_lower_bound=float(-lp.fun),CCE_ratio=float(primal.fun),gamma_min=float(np.min(gamma@lp.x[:-1])),dual_slack_min=float(np.min(D@lp.x[:-1]-lp.x[-1])))
            attempts.append(att)
            if primal.fun>1+1e-6:
                att['weights']=lp.x[:-1].tolist();att['lambda_values']=lam.tolist();break
        if best>1+1e-6:break
    rec=dict(name=name,players=n,topics=k,ordered_histories=len(policy),gamma_rows=len(gamma),seed_W=float(c@w),seed_CCE_value=float(base.fun),best_CCE_ratio=float(best),attempts=attempts)
    results.append(rec);print(json.dumps({q:rec[q] for q in ['name','players','topics','seed_W','seed_CCE_value','best_CCE_ratio']}),flush=True)
(ROOT/'research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_named.json').write_text(json.dumps(dict(scope='Numerical exact-full-policy cone attack on existing obstruction strategies; not new instances.',cases=results),indent=2)+'\n')
