"""Finite direct complete-history policy mutations, not a universal theorem.

Mutates actual ordered off-path nodes, recomputes every branch incentive row,
then optimizes nonnegative unit-client multiplicities in that full strategy cone.
The mutations need not be SPE at the starting weights; LP enforces the whole
new tree. Every accepted best witness receives independent canonical verification.
"""
from __future__ import annotations
from fractions import Fraction as F
import argparse, hashlib, importlib.util, json, random, sys, time
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec=importlib.util.spec_from_file_location('existing_complete_cone_engine',SOURCE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


def cone(eng,actions):
    terms={}
    rows=[]
    for depth in range(eng.m,-1,-1):
        for h in __import__('itertools').product(range(eng.p),repeat=depth):
            if depth==eng.m:
                q=tuple(h.count(a) for a in range(eng.p));terms[h]=eng.index[eng.m][q]
            else:
                a=actions[h];dest=terms[h+(a,)];terms[h]=dest
                for b in range(eng.p):
                    if b!=a:rows.append(eng.pay[dest,a]-eng.pay[terms[h+(b,)],b])
    G=np.unique(np.array(rows,dtype=np.int16),axis=0)
    G=G[np.any(G,axis=1)]
    return terms,G


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=60)
    ap.add_argument('--seed',type=int,default=2026102131)
    ap.add_argument('--distinct-denominator',type=int,default=0)
    args=ap.parse_args();rng=random.Random(args.seed)
    stem='ordered_policy_mutation_distinct' if args.distinct_denominator else 'ordered_policy_mutation'
    eng=mod.Engine(5,7,rng);p,m=eng.p,eng.m
    r=mod.baseline(m,p);target,_=eng.solve(r,diverse=True)
    initial,_=eng.strategy(target);pool=[(dict(initial),np.asarray(r,dtype=float))]
    best=F(0);records=[];seen=set();started=time.monotonic()
    for step in range(args.steps):
        actions,r=pool[-1] if step%4 else rng.choice(pool)
        actions=dict(actions);terms,G=cone(eng,actions)
        root=terms[()]
        path=();protected=set()
        while len(path)<m:
            protected.add(path);path=path+(actions[path],)
        eng.u=np.einsum('tam,m->ta',eng.pay,r)
        candidates=[]
        for h,a in actions.items():
            if h in protected:continue
            actual=eng.u[terms[h],a]
            for b in range(p):
                if b!=a:
                    gap=actual-eng.u[terms[h+(b,)],b]
                    candidates.append((abs(gap),h,b))
        candidates.sort(key=lambda z:z[0])
        # Rotate a handful of near-tie choices; same-count histories are distinct.
        band=candidates[:max(10,len(candidates)//20)]
        for gap,h,b in rng.sample(band,min(len(band),rng.randint(1,4))):actions[h]=b
        terms,G=cone(eng,actions)
        key=hashlib.sha256(repr(sorted(actions.items())).encode()).hexdigest()
        if key in seen:continue
        seen.add(key)
        root=terms[()]
        if args.distinct_denominator:
            extra=[args.distinct_denominator*(eng.inc[a]!=eng.inc[b]).astype(np.int64)-eng.cov[root]
                   for a in range(p) for b in range(a)]
            G=np.vstack([G,extra]).astype(np.int64)
        current=eng.v@r
        jid=int(np.argmax(current)) if step%3 else rng.randrange(len(eng.portfolios))
        result=eng.optimize(root,G,jid)
        if result is None:continue
        x,value=result
        row={'step':step,'proposal_ratio':value,'rows':len(G),'root':eng.terminal[root].tolist()}
        # Keep moves improving the current optimized geometry, plus occasional
        # equal or downhill moves so this is not merely a single-cone LP sweep.
        if value>=1.45 or rng.random()<.12:
            pool.append((actions,x))
            if len(pool)>30:pool.pop(rng.randrange(len(pool)-1))
        if value>float(best)+1e-9:
            clones=eng.exact_recover(G,root,x)
            if clones is not None:
                inst,cert=mod.verify_canonical(m,p,clones,list(actions.items()),eng.terminal[root].tolist())
                ratio=F(inst.optimal_welfare(),inst.welfare(tuple(map(int,eng.terminal[root]))))
                row['exact_ratio']=str(ratio)
                if ratio>best:
                    best=ratio
                    report={'scope':'one genuine complete-history pure SPE; not universal',
                            'parameters':vars(args),'step':step,'ratio':str(ratio),
                            'instance':inst.to_dict(),'strategy':cert.to_dict(),
                            'canonical_full_history_verified':True}
                    (HERE/(stem+'_best.json')).write_text(json.dumps(report,indent=2)+'\n')
                    print(json.dumps({'step':step,'best_exact':str(best),'rows':len(G)}),flush=True)
        records.append(row)
        if step%10==0:
            (HERE/(stem+'_run.json')).write_text(json.dumps({'scope':'finite full-history strategy mutations only',
                'best_exact':str(best),'cones':len(seen),'elapsed':time.monotonic()-started,'records':records},indent=2)+'\n')
    report={'scope':'finite full-history strategy mutations only; no zero-counterexample theorem',
            'parameters':vars(args),'best_exact':str(best),'cones':len(seen),
            'elapsed':time.monotonic()-started,'records':records}
    (HERE/(stem+'_run.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
