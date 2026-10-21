"""Numerical discovery for fractional actual-load caps; no theorem inference."""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]

def run(name):
    game=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    k,m=len(game['topics']),game['players']
    if k>7: return None
    pol={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
    @lru_cache(None)
    def end(h): return h if len(h)==m else end(h+(pol[h],))
    masks=list(range(1,1<<k))
    bits=np.array([[(t>>a)&1 for t in masks] for a in range(k)],dtype=int)
    def rho(a,z): return bits[a]/np.maximum(sum(bits[b] for b in z),1)
    rows=[(h,a) for h in pol for a in range(k) if a!=pol[h]]
    G=np.array([rho(pol[h],end(h))-rho(a,end(h+(a,))) for h,a in rows])
    z=end(()); load=sum(bits[b] for b in z); c=(load>0).astype(int)
    records=[]
    for a in range(k):
        g=bits[a]/(1+(m-1)*load/m)
        obj=(m-F(1,2))*g-c
        lp=linprog(-np.array(obj,dtype=float),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success: raise RuntimeError(lp.message)
        w=[F(float(v)).limit_denominator(1000000) for v in lp.x]
        def u(a,q):
            return sum((v/F(sum(b in [(i) for i in range(k) if t>>i&1] for b in q)) for t,v in zip(masks,w) if v and t>>a&1),F(0))
        minimum=min((u(pol[h],end(h))-u(b,end(h+(b,))) for h,b in rows),default=F(0))
        W=sum(v for v,l in zip(w,load) if l)
        cap=sum((v/(1+F(m-1,m)*int(l)) for t,v,l in zip(masks,w,load) if t>>a&1),F(0))
        gap=F(2*m-1,2)*cap-W
        records.append({'query':a,'gap_float':float(-lp.fun),'gap_exact':str(gap),'minimum_spe_slack':str(minimum),'W':str(W),'cap':str(cap),'weights':{str(t):str(v) for t,v in zip(masks,w) if v}})
    return {'name':name,'players':m,'topics':k,'path':z,'rows':len(rows),'records':records}

if __name__=='__main__':
    results=[]
    for name in ['aggregate_theta_failure','individual_security_failure','local_security_increment','root_tax_failure','global_decorrelation_failure','root_stationary_kernel','iid_empirical_kernel']:
        try:
            r=run(name)
            if r:
                results.append(r)
                best=max(r['records'],key=lambda x:F(x['gap_exact']))
                print(json.dumps({'name':name,'best':best}),flush=True)
        except FileNotFoundError:
            continue
    Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2))
