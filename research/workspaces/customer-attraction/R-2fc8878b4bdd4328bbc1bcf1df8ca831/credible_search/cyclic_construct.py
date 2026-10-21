"""Focused cyclic-catalog construction, not another joint MILP.

Reuse the old all-SPE float oracle only to propose a suffix. Rotate that one
suffix to all first-action branches. Linear optimization is restricted to
cyclic customer-type orbits, so root utilities remain exactly tied. Any saved
point is reconstructed as integer customers and verified on the complete tree.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
SOURCE = ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec = importlib.util.spec_from_file_location('cyclic_old_engine',SOURCE)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
RECOVER_SOURCE = SOURCE.parent.parent/'global_proof/individual_face_walk.py'
spec2 = importlib.util.spec_from_file_location('cyclic_old_recover',RECOVER_SOURCE)
recovery = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(recovery)


def rotate(mask,p):
    return ((mask<<1)&((1<<p)-1)) | (mask>>(p-1))


def orbit_matrix(p):
    unseen=set(range(1,1<<p));orbits=[]
    while unseen:
        a=min(unseen);B={a};b=rotate(a,p)
        while b!=a:B.add(b);b=rotate(b,p)
        unseen.difference_update(B);orbits.append(tuple(sorted(B)))
    A=np.zeros(((1<<p)-1,len(orbits)),dtype=np.int64)
    for i,B in enumerate(orbits):
        for mask in B:A[mask-1,i]=1
    return orbits,A


def equivariant_policy(eng,target,rng):
    class FirstZero:
        def __init__(self):self.first=True
        def choice(self,values):
            if self.first:
                self.first=False
                assert 0 in values
                return 0
            return rng.choice(values)
    eng.rng=FirstZero()
    actions,_ = eng.strategy(target)
    base=dict(actions)
    actions={():0}
    for depth in range(1,eng.m):
        for h in product(range(eng.p),repeat=depth):
            a=h[0];normalized=tuple((b-a)%eng.p for b in h)
            actions[h]=(base[normalized]+a)%eng.p
    return actions


def rows_for(eng,actions):
    terminals={}
    def tr(h):
        if h not in terminals:
            terminals[h]=(eng.index[eng.m][tuple(h.count(a) for a in range(eng.p))]
                          if len(h)==eng.m else tr(h+(actions[h],)))
        return terminals[h]
    rows=[]
    for h,a in actions.items():
        actual=tr(h)
        for b in range(eng.p):
            if a!=b:rows.append(eng.pay[actual,a]-eng.pay[tr(h+(b,)),b])
    G=np.unique(np.array(rows,dtype=np.int64),axis=0)
    return tr(()),G


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=3)
    ap.add_argument('--topics',type=int,default=7)
    ap.add_argument('--steps',type=int,default=12)
    ap.add_argument('--seed',type=int,default=78123)
    ap.add_argument('--goal',choices=['individual','half'],default='individual')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    rng=random.Random(args.seed);m,p=args.players,args.topics
    eng=old.Engine(m,p,rng);orbits,A=orbit_matrix(p)
    # Rotated portfolios have identical coverage on every orbit coordinate.
    objectives={tuple(map(int,row@A)):i for i,row in enumerate(eng.v)}
    records=[];best=Fraction(0);saved=None
    endpoints=[]
    for step in range(args.steps):
        if step<len(orbits):
            z=np.zeros(len(orbits),dtype=np.int64);z[step]=1
        elif endpoints and rng.random()<.5:
            z=np.array(rng.choice(endpoints),dtype=float)
            z=z*rng.choice([1,5,20])+np.array([rng.random()*.01 for _ in orbits])
        else:
            z=np.array([rng.randint(1,10) if rng.random()<.3 else 0 for _ in orbits])
            if not np.any(z):z[rng.randrange(len(z))]=1
        r=A@z
        eng.rng=rng;eng.solve(r)
        child=eng.R[1][eng.children[0][0][0]]
        values=eng.u[child,0] if args.goal=='individual' else eng.w[child]
        targets=child[values<=values.min()+eng.eps]
        target=int(rng.choice(list(targets)))
        actions=equivariant_policy(eng,target,rng)
        target,G=rows_for(eng,actions)
        GO=np.unique(G@A,axis=0);GO=GO[np.any(GO!=0,axis=1)]
        norm=eng.cov[target]@A
        for obj,jid in objectives.items():
            objective=np.array(obj,dtype=np.int64)
            if args.goal=='individual':objective=objective*eng.L-(2*m-1)*(eng.pay[target,0]@A)
            res=linprog(-objective.astype(float),A_ub=-GO.astype(float),b_ub=np.zeros(len(GO)),
                        A_eq=[norm.astype(float)],b_eq=[1],bounds=(0,None),method='highs')
            if not res.success:continue
            endpoints.append(res.x.tolist())
            orbit_clones=recovery.recover(GO,norm,res.x)
            if orbit_clones is None:continue
            clones=(A@np.array(orbit_clones,dtype=object)).tolist()
            O=int(max(eng.v@np.array(clones,dtype=object)))
            W=int(eng.cov[target]@np.array(clones,dtype=object))
            u=Fraction(int(eng.pay[target,0]@np.array(clones,dtype=object)),eng.L)
            ratio=Fraction(O,u) if args.goal=='individual' else Fraction(O,W)
            records.append({'step':step,'J':eng.portfolios[jid],'value':str(ratio)})
            if ratio>best:
                inst,cert=old.verify_canonical(m,p,clones,list(actions.items()),eng.terminal[target].tolist())
                assert inst.optimal_welfare()==O and inst.welfare(eng.terminal[target].tolist())==W
                assert inst.topic_payoff(0,eng.terminal[target].tolist())==u
                best=ratio
                saved={'scope':'cyclic-catalog full-history pure SPE construction; finite point only',
                       'parameters':dict(vars(args)),'engine_source':str(SOURCE.relative_to(ROOT)),
                       'engine_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                       'orbits':orbits,'orbit_clones':orbit_clones,'ratio':str(ratio),
                       'instance':inst.to_dict(),'strategy':cert.to_dict(),
                       'W':W,'OPT':O,'first_utility':str(u),'full_strategy_verified':True,
                       'records':records}
                saved['parameters']['output']=str(args.output)
                args.output.write_text(json.dumps(saved,indent=2)+'\n')
                print(json.dumps({'step':step,'goal':args.goal,'ratio':str(ratio),'W':W,'OPT':O,'first_utility':str(u)}),flush=True)
            threshold=2*m-1 if args.goal=='individual' else 2
            if ratio>threshold:
                print('EXACT COUNTEREXAMPLE',flush=True);return
    if saved:
        saved['records']=records
        saved['completed_steps']=args.steps
        args.output.write_text(json.dumps(saved,indent=2)+'\n')


if __name__=='__main__':main()
