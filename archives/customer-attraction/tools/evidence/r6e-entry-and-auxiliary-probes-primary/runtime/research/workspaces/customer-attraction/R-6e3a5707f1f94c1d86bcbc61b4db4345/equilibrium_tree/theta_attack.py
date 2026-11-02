"""Candidate generator for W >= (m-1/2)*theta. Floats are exploratory only."""
from pathlib import Path
import sys, json, random
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,instance_from_clones
from customer_attraction import Instance,ExactSPESolver
from cone_attack_credible_variants import credible_cone

def counts(p,n):
    if p==1:
        yield (n,)
    else:
        for i in range(n+1):
            for c in counts(p-1,n-i): yield (i,)+c

def joining(p,m):
    masks=np.arange(1,1<<p)
    membership=np.array([[(mask>>a)&1 for mask in masks] for a in range(p)])
    prefixes=list(counts(p,m-1))
    return np.array([membership/(1+np.asarray(b)@membership) for b in prefixes])

def optimize(cone,x,j,iterations=12):
    best=None
    for it in range(iterations):
        selected=np.argmax(j@x,axis=1)
        rows=j[np.arange(len(j)),selected,:]
        A=np.vstack([np.c_[-cone.matrix,np.zeros(len(cone.rows))],
                     np.c_[-rows,np.ones(len(rows))]])
        c=np.r_[np.zeros(len(x)),-1.]
        r=linprog(c,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.array(cone.welfare,float),0]],b_eq=[1],bounds=(0,None),method='highs')
        if not r.success: return best
        x=r.x[:-1]
        theta=np.min(np.max(j@x,axis=1))
        if best is None or theta>best[0]+1e-9: best=(theta,x)
        else: return best
    return best

if __name__=='__main__':
    rng=random.Random(6712)
    for name in ['aggregate_theta_failure','individual_security_failure','root_tax_failure','prefix_balance_failure','root_stationary_kernel','eight_cce_welfare_gap']:
        inst=Instance.from_dict(json.loads((ROOT/f'examples/customer_attraction/{name}.json').read_text()))
        p,m=inst.topic_count,inst.players
        j=joining(p,m)
        s=ExactSPESolver(inst)
        source=np.zeros((1<<p)-1)
        for t in inst.customers:source[sum(1<<a for a in t.topics)-1]+=t.multiplicity
        for i in range(4):
            target=rng.choice(sorted(s.worst_outcomes()))
            cone,stats=credible_cone(s,target,rng,'uniform_credible')
            out=optimize(cone,source,j)
            if out:
                theta,x=out
                print(json.dumps({'seed':name,'sample':i,'p':p,'m':m,'theta_per_W':theta,'W_per_theta':1/theta,'weak_threshold':m-.5,'root':cone.root,'rows':len(cone.rows)}),flush=True)
                if theta>1/(m-.5)+1e-8:
                    path=Path(__file__).with_name('theta_float_candidate.json')
                    path.write_text(json.dumps({'p':p,'m':m,'theta':theta,'weights':list(x),'actions':[[list(h),a] for h,a in cone.actions.items()]}))
                    break
