"""Floating full-type cone attack for the 3x3 sacrificial-group policies."""
from pathlib import Path
from functools import lru_cache
from itertools import combinations_with_replacement
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
p=Path(__file__).with_name('group_pair_probe.py')
spec=importlib.util.spec_from_file_location('base',p);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
M=base.member;n=base.n;k=base.k;scale=base.scale;d=M.shape[1]
@lru_cache(None)
def row(a,q):
    den=np.array(q)@M
    return (M[a]*(scale//np.maximum(den,1))).astype(np.int16)
B=[]
for tup in combinations_with_replacement(range(k),n-1):
    den=1+sum((M[a] for a in tup),start=np.zeros(d,dtype=np.int64))
    B.append(M.T/den[:,None])
B=np.array(B)
rng=np.random.default_rng(210106)
reports=[]
for same in [False,True]:
    actions,*_,path=base.build_policy(same)
    @lru_cache(None)
    def terminal(h):
        if len(h)==n:return tuple(h.count(a) for a in range(k))
        return terminal(h+(actions[h],))
    rows={}
    for h,a in actions.items():
        own=row(a,terminal(h))
        for b in range(k):
            g=own-row(b,terminal(h+(b,)))
            rows[g.tobytes()]=g
    G=np.array(list(rows.values()),dtype=float)/scale
    q=terminal(());pair=(row(path[0],q)+row(path[1],q)).astype(float)/scale
    print('cone',same,G.shape,flush=True)
    best=0.;queries=[np.ones(k)/k]+[rng.dirichlet(np.ones(k)) for _ in range(3)]
    for qi,p in enumerate(queries):
        for step in range(5):
            beta=B@p
            A=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(len(beta))]])
            out=linprog(np.r_[np.zeros(d),-2.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[pair,0]],b_eq=[1],bounds=[(0,None)]*d+[(None,None)],method='highs')
            rec={'same':same,'query':qi,'step':step,'status':out.status}
            if not out.success:reports.append(rec);break
            w=out.x[:-1];ratio=-out.fun;rec.update(ratio=ratio,nonzero_types=int(sum(w>1e-8)),gamma_min=float(np.min(G@w)))
            reports.append(rec);print(json.dumps(rec),flush=True)
            if ratio>1+1e-7:
                rec.update(weights=w.tolist(),p=p.tolist());break
            mat=B.transpose(0,2,1)@w
            sec=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
            if not sec.success:raise ValueError(sec.message)
            p2=sec.x[:-1]
            if max(abs(p2-p))<1e-8:break
            p=p2
        if ratio>1+1e-7:break
    if ratio>1+1e-7:break
Path(__file__).with_name('group_pair_full_types_numerical.json').write_text(json.dumps({'scope':'Floating discovery only','reports':reports},indent=2)+'\n')
