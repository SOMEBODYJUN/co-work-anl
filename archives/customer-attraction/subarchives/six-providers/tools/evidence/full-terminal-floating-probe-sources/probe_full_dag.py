"""Floating discovery only, full-terminal path menus in a complete SPE DAG cone."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from probe_path_menu import cap_lp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_m6_dag.json'
d=json.loads(SOURCE.read_text());nodes=d['nodes'];n=d['instance']['players'];k=len(d['instance']['topics'])
bits=np.array([[(t>>a)&1 for a in range(k)] for t in range(1,1<<k)],float)
gamma=[]
def row(a,z):return bits[:,a]/np.maximum(bits@np.array(z),1)
for node in nodes:
    if 'action' not in node:continue
    a0=node['action'];r0=row(a0,node['target'])
    for a,child in enumerate(node['children']):
        if a!=a0:gamma.append(r0-row(a,nodes[child]['target']))
gamma=np.array(gamma);gamma=np.unique(gamma,axis=0)
bg=[];node=nodes[d['root']]
while 'action' in node:
    for child in node['children']:bg.append(nodes[child]['target'])
    node=nodes[node['children'][node['action']]]
bg=np.unique(bg,axis=0);coeff=bits[None,:,:]/(1+bg@bits.T)[:,:,None]
c=(bits@np.array(nodes[d['root']]['target'])>0).astype(float)
rng=np.random.default_rng(48692);best=None
seed=np.zeros((1<<k)-1)
for t in d['instance']['customers']:seed[sum(1<<a for a in t['topics'])-1]+=t['multiplicity']
p,cap=cap_lp(seed,coeff)
print(json.dumps(dict(gamma=gamma.shape,backgrounds=bg.tolist(),seed_W=float(c@seed),seed_cap=float(cap),seed_gap=float(n*cap-c@seed),seed_p=p.tolist())),flush=True)
for start in range(25):
    p0=p if start==0 else rng.dirichlet(np.ones(k)*.4)
    last=None
    for it in range(15):
        beta=coeff@p0
        r=linprog(np.r_[c,-n],A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],b_ub=np.zeros(len(gamma)+len(beta)),A_eq=[np.r_[np.ones(len(c)),0]],b_eq=[1],bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
        assert r.success,r.message
        w=r.x[:-1];p0,v=cap_lp(w,coeff);gap=n*v-c@w
        if best is None or gap>best['gap']+1e-9:
            best=dict(status='floating discovery only; full-terminal path-menu support',source=str(SOURCE.relative_to(ROOT)),start=start,it=it,gap=float(gap),W=float(c@w),cap=float(v),p=p0.tolist(),weights={str(t):float(x) for t,x in enumerate(w,1) if x>1e-9},backgrounds=bg.tolist())
            print(json.dumps(best),flush=True);(HERE/'full_dag_best.json').write_text(json.dumps(best,indent=2))
        if last is not None and abs(gap-last)<1e-9:break
        last=gap
