"""Exploratory exact-policy-cone LP for m M_alpha <= W+G_alpha.
All customer coordinates are nonempty interest masks on p labels.
No claim follows from failure to find a separating vector.
"""
from pathlib import Path
import json,itertools,sys
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]

def policy_cone(cert):
    acts={tuple(r['history']):r['action'] for r in cert['actions']}
    m=max(max(acts.values()),max((max(h) for h in acts if h),default=0))+1
    n=max(map(len,acts))+1
    masks=np.arange(1,1<<m,dtype=np.int64)
    incl=((masks[:,None]>>np.arange(m))&1).astype(float)
    def terminal(h):
        while len(h)<n:h=h+(acts[h],)
        return h
    terms={h:terminal(h) for h in acts}
    def row(a,z):
        counts=np.bincount(z,minlength=m)
        load=incl@counts
        return np.divide(incl[:,a],load,out=np.zeros(len(masks)),where=load>0)
    rows=[]
    for h,act in acts.items():
        base=row(act,terms[h])
        for a in range(m):
            if a!=act: rows.append(base-row(a,terminal(h+(a,))))
    gamma=np.array(rows)
    gamma=np.unique(np.round(gamma,14),axis=0)
    z=terms[()]
    load=incl@np.bincount(z,minlength=m)
    covered=(load>0).astype(float)
    alpha=F(n-1,n)
    gden=1+float(alpha)*load
    G=covered/gden
    objs=np.array([n*incl[:,a]/gden-covered-G for a in range(m)])
    return n,m,masks,gamma,objs,z

def scan(cert,individual=False):
    n,m,masks,gamma,objs,z=policy_cone(cert)
    if individual:
        inc=((masks[:,None]>>np.arange(m))&1).astype(float)
        load=inc@np.bincount(z,minlength=m)
        cov=(load>0).astype(float)
        base=objs.copy()
        objs=np.concatenate([base+cov-n*np.divide(inc[:,b],load,out=np.zeros(len(masks)),where=load>0) for b in sorted(set(z))])
    results=[]
    optima=[]
    for a,obj in enumerate(objs):
        r=linprog(-obj,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
        if not r.success:raise RuntimeError(r.message)
        optima.append(float(-r.fun))
        if -r.fun>1e-8:
            supp=[(int(mask),float(v)) for mask,v in zip(masks,r.x) if v>1e-8]
            results.append({'query':a,'gap':-r.fun,'support':supp})
    return {'scope':'exploratory floating LP; no exact cone certificate','individual':individual,'n':n,'p':m,'root':z,'rows':len(gamma),'optima':optima,'separators':results}

if __name__=='__main__':
    results={}
    for name in [x for x in sys.argv[1:] if not x.startswith('--')]:
        d=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
        cert=d.get('certificate',d.get('strategy',d))
        if 'actions' not in cert:continue
        v=scan(cert,individual='--individual' in sys.argv);results[name]=v;print(name,json.dumps(v),flush=True)
    if results:
        Path(__file__).with_name('refined_fractional_scan_individual_results.json' if '--individual' in sys.argv else 'refined_fractional_scan_results.json').write_text(json.dumps(results,indent=2)+'\n')
