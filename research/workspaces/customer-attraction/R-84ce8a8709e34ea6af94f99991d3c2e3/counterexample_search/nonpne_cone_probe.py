"""Finite full-history SPE cones, restricted to genuinely non-PNE root outcomes.

Observation only: neither unsuccessful search nor a floating LP establishes any
universal claim.  The existing Engine implements all-outcome recursion; final
integer witnesses use the canonical complete-history verifier.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, random, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec=importlib.util.spec_from_file_location('previous_complete_cone_engine',SOURCE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=40)
    ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5)
    ap.add_argument('--seed',type=int,default=2026102107)
    ap.add_argument('--gap-denominator',type=int,default=1000)
    args=ap.parse_args();rng=random.Random(args.seed)
    eng=mod.Engine(args.players,args.topics,rng)
    ids={tuple(q):j for j,q in enumerate(eng.terminal)}
    deviations=[]
    for q in eng.terminal:
        rows=[]
        for a,n in enumerate(q):
            if n:
                for b in range(args.topics):
                    if b!=a:
                        dest=q.copy();dest[a]-=1;dest[b]+=1
                        rows.append((a,b,ids[tuple(dest)]))
        deviations.append(rows)
    records=[];seeds=[];best=F(0);seen=set();started=time.monotonic()
    # A seed mechanism known to permit non-PNE SPE in the 3-player restriction.
    known={2:1,3:2,7:2,10:3,12:3,13:5}
    for j in range(12):
        w=[0]*len(eng.masks)
        for mask,n in known.items():w[mask-1]=n*rng.choice([1,2,3])
        for a in range(4,args.topics):w[(1<<a)-1]=rng.randint(1,6)
        for k in range(rng.randint(0,6)):w[rng.randrange(len(w))]+=rng.randint(1,4)
        seeds.append(w)
    for step in range(args.steps):
        if seeds:r=seeds.pop(0)
        else:
            # Arbitrary sparse incidence types, favoring overlaps of size 2--4.
            r=[0]*len(eng.masks)
            for k in range(rng.randint(6,20)):
                mask=sum(1<<a for a in rng.sample(range(args.topics),rng.randint(1,min(4,args.topics))))
                r[mask-1]+=rng.randint(1,20)
        eng.solve(r)
        candidates=[]
        for target in eng.R[0][0]:
            gains=[eng.u[d,b]-eng.u[target,a] for a,b,d in deviations[target]]
            if gains and max(gains)>eng.eps:
                candidates.append((int(target),int(np.argmax(gains)),float(max(gains))))
        if not candidates:
            records.append({'step':step,'root_nonpne':0});continue
        candidates.sort(key=lambda z:eng.w[z[0]])
        target,gid,gain=rng.choice(candidates[:max(1,len(candidates)//2)])
        a,b,d=deviations[target][gid]
        actions,G=eng.strategy(target)
        # Retain a static profitable deviation at every optimized cone vertex.
        gaprow=args.gap_denominator*(eng.pay[d,b].astype(np.int64)-eng.pay[target,a])-eng.L*eng.cov[target]
        G=np.vstack([G,gaprow]).astype(np.int64)
        key=hashlib.sha256(repr(actions).encode()).hexdigest()
        if key in seen:continue
        seen.add(key)
        Jid=int(np.argmax(eng.v@np.asarray(r,dtype=float)))
        result=eng.optimize(target,G,Jid)
        if result is None:
            records.append({'step':step,'root_nonpne':len(candidates),'lp':'infeasible_gap'});continue
        x,value=result
        clones=eng.exact_recover(G,target,x)
        row={'step':step,'root_nonpne':len(candidates),'target':eng.terminal[target].tolist(),
             'input_static_gain_scaled':gain,'proposal_ratio':value,'rows':len(G)}
        if clones is not None:
            inst,cert=mod.verify_canonical(args.players,args.topics,clones,actions,eng.terminal[target].tolist())
            ratio=F(inst.optimal_welfare(),inst.welfare(tuple(map(int,eng.terminal[target]))))
            row['exact_ratio']=str(ratio)
            if ratio>best:
                best=ratio
                witness={'scope':'one complete-history pure SPE, not a universal result',
                         'ratio':str(ratio),'instance':inst.to_dict(),'strategy':cert.to_dict(),
                         'nonpne_deviation':[a,b],'canonical_full_history_verified':True,
                         'parameters':vars(args),'step':step}
                (HERE/'nonpne_best.json').write_text(json.dumps(witness,indent=2)+'\n')
                print(json.dumps({'step':step,'exact_best':str(best),'root_nonpne':len(candidates)}),flush=True)
            # Perturb a certified non-PNE vertex to cross its adjacent faces.
            for j in range(2):
                nr=[float(v)*rng.choice([10,30]) for v in x]
                for k in range(rng.randint(1,4)):nr[rng.randrange(len(nr))]+=rng.random()*.2
                seeds.append(nr)
        records.append(row)
        report={'scope':'finite non-PNE SPE-cone search only; no universal proof',
                'parameters':vars(args),'best_exact_ratio':str(best),'cones':len(seen),
                'elapsed':round(time.monotonic()-started,3),'records':records}
        (HERE/'nonpne_run.json').write_text(json.dumps(report,indent=2)+'\n')
    report={'scope':'finite non-PNE SPE-cone search only; no universal proof',
            'parameters':vars(args),'best_exact_ratio':str(best),'cones':len(seen),
            'elapsed':round(time.monotonic()-started,3),'records':records}
    (HERE/'nonpne_run.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
