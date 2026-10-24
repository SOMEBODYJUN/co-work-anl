"""Attack the precise general candidate m*u_i >= OPT_m-W.
Each fixed full strategy is retained on every ordered history. Customer weights
range over all nonempty interest types. A positive objective against any legal
m-topic comparison union refutes the candidate, not Q-CAG-HALF.
"""
import json
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

BASE=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent

names=['aggregate_theta_failure','individual_security_failure','global_decorrelation_failure','root_tax_failure','optimal_last_query_failure','onpath_budget_failure']
results=[]
for name in names:
    inp=BASE/'examples/customer_attraction'/f'{name}.json'
    cert=BASE/'evidence/certificates/customer_attraction'/f'{name}.json'
    if not inp.exists() or not cert.exists(): continue
    ins=json.loads(inp.read_text()); d=json.loads(cert.read_text())
    actions={tuple(e['history']):e['action'] for e in d['strategy']['actions']}
    k=len(ins['topics']); m=ins.get('players',max(map(len,actions))+1); masks=range(1,1<<k)
    def leaf(h):
        h=tuple(h)
        while len(h)<m: h+=actions[h],
        return h
    def prof(z,i):
        counts=[sum(bool(s&(1<<a)) for a in z) for s in masks]
        return np.array([float(bool(s&(1<<z[i])))/c if c else 0. for s,c in zip(masks,counts)])
    ic=[]
    for h in actions:
        i=len(h); base=prof(leaf(h),i)
        for a in range(k): ic.append(prof(leaf(h+(a,)),i)-base)
    z=leaf(()); covered=np.array([float(any(s&(1<<a) for a in z)) for s in masks]); best=(0,None)
    for support in combinations(range(k),min(k,m)):
        coveropt=np.array([float(any(s&(1<<a) for a in support)) for s in masks])
        for i in range(m):
            objective=coveropt-covered-m*prof(z,i)
            res=linprog(-objective,A_ub=ic,b_ub=np.zeros(len(ic)),A_eq=np.ones((1,len(list(masks)))),b_eq=[1],bounds=(0,None),method='highs')
            if res.success and -res.fun>best[0]+1e-9:
                best=(-res.fun,{'comparison':support,'player':i,'weights':{str(s):float(w) for s,w in zip(masks,res.x) if w>1e-9}})
    entry={'source':name,'players':m,'topics':k,'objective':best[0],'attaining':best[1]}; results.append(entry)
    print(json.dumps(entry),flush=True)
(OUT/'gap_profit_floor_attack.json').write_text(json.dumps(results,indent=2))
