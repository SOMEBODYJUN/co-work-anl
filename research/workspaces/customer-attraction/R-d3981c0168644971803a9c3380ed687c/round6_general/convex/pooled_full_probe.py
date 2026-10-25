"""Named finite attacks on q_i=p pooled full-load sufficient helper.

The queried candidate is F_p((1/m)sum_i E_(B~p)c(Z_i(B)))<=W/m.
This helper implies the parent's free full-load convex menu cap. A failure
would refute only this specified-query helper, not the free cap or half.
"""
from functools import lru_cache
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate

def read_named(name):
    a=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    s=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    game=Instance.from_dict(a)
    sd=s.get('strategy',s)
    if 'terminal_counts' not in sd:
        policy={tuple(row['history']):row['action'] for row in sd['actions']}
        h=()
        while len(h)<game.players:h=h+(policy[h],)
        sd=dict(sd,terminal_counts=list(game.counts(h)))
    cert=StrategyCertificate.from_dict(sd)
    audit=verify_certificate(game,cert);audit.assert_valid()
    m=game.players;k=game.topic_count
    inc=np.array([[int(j in c.topics) for c in game.customers] for j in range(k)])
    w=np.array([c.multiplicity for c in game.customers])
    @lru_cache(None)
    def leaf(h):
        return h if len(h)==m else leaf(h+(cert.actions[h],))
    z=leaf(());W=game.welfare(game.counts(z))
    cols=np.array([[inc[list(leaf(z[:i]+(b,)))].sum(axis=0) for b in range(k)] for i in range(m)])
    return m,k,inc,w,cols,W,dict(histories=audit.checked_histories,deviations=audit.checked_deviations)

def attack(m,k,inc,w,cols,W):
    averaged=cols.mean(axis=0)
    def val(p):
        return np.sum(w*(p@inc)/(1+p@averaged))
    def jac(p):
        den=1+p@averaged;rho=p@inc
        return inc@(w/den)-averaged@(w*rho/den**2)
    rng=np.random.default_rng(720259)
    starts=[np.full(k,1/k)]+list(np.eye(k))
    starts.extend(rng.dirichlet(np.ones(k),8))
    best=(-1,None)
    for p in starts:
        res=minimize(lambda p:-val(p),p,jac=lambda p:-jac(p),bounds=[(0,1)]*k,
                     constraints=[{'type':'eq','fun':lambda p:p.sum()-1,'jac':lambda p:np.ones(k)}],
                     method='SLSQP',options={'maxiter':600,'ftol':1e-12})
        if res.success and -res.fun>best[0]:best=(-res.fun,res.x)
    return dict(F=float(best[0]),W_over_m=W/m,gap=float(best[0]-W/m),p=best[1].tolist())

if __name__=='__main__':
    names=['aggregate_theta_failure','individual_security_failure','root_tax_failure',
           'global_decorrelation_failure','fractional_actual_load_failure','eight_cce_welfare_gap']
    out=[]
    for name in names:
        m,k,inc,w,cols,W,audit=read_named(name)
        ans=dict(name=name,m=m,k=k,W=W,full_SPE=audit,**attack(m,k,inc,w,cols,W))
        print(json.dumps(ans),flush=True);out.append(ans)
    Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Finite floating specified-query helper attack; not proof',records=out),indent=2)+'\n')
