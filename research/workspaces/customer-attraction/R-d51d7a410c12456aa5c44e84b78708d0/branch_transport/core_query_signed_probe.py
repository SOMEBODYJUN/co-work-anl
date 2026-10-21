"""Attack the actual-node menu bridge with signed perturbations.

Policy always picks a fresh core action. Extra query labels are never picked
by the policy. Uniform positive type mass gives zero slack for all fresh
comparisons, positive slack for old comparisons, and a common query baseline
on all distinct core backgrounds. A signed LP direction can thus be compiled
with a sufficiently large uniform positive bias if its zero-base rows obey.
"""
from __future__ import annotations
import argparse, importlib.util, json, random
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

P=Path(__file__).with_name('actual_menu_probe.py')
spec=importlib.util.spec_from_file_location('menu',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def run(a):
    rng=random.Random(a.seed);n=a.players;core=a.core;k=core+a.queries
    p=np.r_[np.zeros(core),np.ones(a.queries)/a.queries]
    results=[]
    for case in range(a.cases):
        policy={h:rng.choice([t for t in range(core) if t not in h]) for d in range(n) for h in product(range(k),repeat=d)}
        G,R,I,c,z,bs=m.menu_geometry(n,k,policy)
        base=G@np.ones(len(c))
        assert min(base)>-1e-7
        # Positive base rows can be made feasible by a finite uniform bias.
        Z=G[abs(base)<1e-7]
        bgload=np.array(bs)
        distinct=np.sum(bgload>0,axis=1)==n-1
        B=R[distinct]*(I@p)[None,:]
        baseline=float(B[0].sum())
        assert max(abs(B.sum(axis=1)-baseline))<1e-7
        assert abs(c.sum()/n-baseline)<1e-7
        # t <= (query value in B) - W/n for every minimum-base menu.
        A=np.vstack((np.c_[-Z,np.zeros(len(Z))],np.c_[c[None,:]/n-B,np.ones(len(B))]))
        lp=linprog(np.r_[np.zeros(len(c)),-1],A_ub=A,b_ub=np.zeros(len(A)),bounds=[(-1,1)]*len(c)+[(None,None)],method='highs')
        assert lp.success
        gap=-lp.fun
        rec=dict(case=case,n=n,k=k,core=core,menus=len(bs),distinct_menus=int(sum(distinct)),zero_base_rows=len(Z),gap=gap)
        if gap>1e-7:
            rec.update(weights=lp.x[:-1].tolist(),p=p.tolist(),backgrounds=bs,policy=[dict(history=h,action=t) for h,t in policy.items()])
            results.append(rec);print(json.dumps({key:rec[key] for key in ['case','n','k','menus','gap']}),flush=True);break
        results.append(rec)
        if case%20==0: print(json.dumps(rec),flush=True)
    return dict(status='numerical signed-direction exploration; positive witness requires exact reconstruction',seed=a.seed,records=results)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3);ap.add_argument('--core',type=int,default=3);ap.add_argument('--queries',type=int,default=2)
    ap.add_argument('--cases',type=int,default=200);ap.add_argument('--seed',type=int,default=2026102109);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.write_text(json.dumps(run(a),indent=2)+'\n')
