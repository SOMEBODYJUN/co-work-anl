#!/usr/bin/env python3
"""Finite attack on the auxiliary cap (m+1) max_i u_i <= 2 W.

Canonical all-SPE outcome sets provide seeds. Every reported optimized witness
is a complete ordered-history strategy checked with rational arithmetic.
The search is not exhaustive and gives no universal conclusion when silent.
"""
from __future__ import annotations
import argparse, json, random, sys, time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import StrategyCone, payoff_row, dot, integer_clones, instance_from_clones, independently_verify, serializable

def inc(k,a): return tuple(x+(j==a) for j,x in enumerate(k))

def paths_by_action(solver,q):
    """For each position/action realizable with q, retain one legal ordered path."""
    p,m=solver.instance.topic_count,solver.instance.players
    states={(0,)*p:()}; result={}
    for i in range(m):
        nxt={}
        for k,h in states.items():
            floor=solver.threshold(k)
            for a in range(p):
                kk=inc(k,a)
                if q in solver.outcomes(kk) and solver._utility(q,a)>=floor:
                    hh=h+(a,); nxt.setdefault(kk,hh)
        states=nxt
    # Recursively retain a path for each specified position/action.  Counts can
    # merge only after preserving the queried action label in the memo key.
    for pos in range(m):
        for a in range(p):
            if not q[a]: continue
            @lru_cache(None)
            def seek(k):
                d=sum(k)
                if d==m:return () if k==q else None
                floor=solver.threshold(k)
                for b in ([a] if d==pos else range(p)):
                    kk=inc(k,b)
                    if q not in solver.outcomes(kk) or solver._utility(q,b)<floor:continue
                    tail=seek(kk)
                    if tail is not None:return (b,)+tail
                return None
            path=seek((0,)*p)
            if path is not None:result[pos,a]=path
    return result

def credible_policy(solver,q,path,rng,mode):
    p,m=solver.instance.topic_count,solver.instance.players;actions={}
    def visit(h,k,target):
        if len(h)==m:return
        floor=solver.threshold(k)
        menu=[a for a in range(p) if target in solver.outcomes(inc(k,a)) and solver._utility(target,a)>=floor]
        a=path[len(h)] if h==path[:len(h)] else rng.choice(menu)
        assert a in menu;actions[h]=a;own=solver._utility(target,a)
        for b in range(p):
            child=inc(k,b)
            if b==a:nextq=target
            else:
                qs=[z for z in solver.outcomes(child) if solver._utility(z,b)<=own]
                if mode=='high':
                    value=max(solver._utility(z,b) for z in qs);qs=[z for z in qs if solver._utility(z,b)==value]
                elif mode=='low':
                    value=min(solver._utility(z,b) for z in qs);qs=[z for z in qs if solver._utility(z,b)==value]
                nextq=rng.choice(sorted(qs))
            visit(h+(b,),child,nextq)
    visit((),(0,)*p,q)
    cert=StrategyCertificate(actions,q);verify_certificate(solver.instance,cert).assert_valid()
    return StrategyCone(p,m,actions)

def optimize(cone,action):
    objective=payoff_row(cone.topics,cone.root,action)
    res=linprog(-np.asarray(objective,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),
      A_eq=np.asarray([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return None
    values=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
    if not(cone.verify(values) and dot(cone.welfare,values)==1):values=cone.recover_vertex(res.x)
    if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:return None
    clones=integer_clones(values)
    assert independently_verify(cone,clones)
    inst=instance_from_clones(cone.topics,cone.players,clones)
    checked=verify_certificate(inst,StrategyCertificate(cone.actions,cone.root));checked.assert_valid()
    path=checked.terminal_history;payoffs=inst.player_payoffs(path);w=inst.welfare(cone.root)
    beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    dual=tuple(F(float(-v)).limit_denominator(10**7) for v in res.ineqlin.marginals)
    dual_ok=all(v>=0 for v in dual) and all(beta*ww-sum(v*row[j] for v,row in zip(dual,cone.rows))>=oo for j,(ww,oo) in enumerate(zip(cone.welfare,objective)))
    return {'value':dot(objective,values),'instance':inst.to_dict(),'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),
       'path':path,'payoffs':payoffs,'welfare':w,'optimum':inst.optimal_welfare(),'objective_action':action,
       'exact_dual_bound':beta if dual_ok else None,'checked_histories':checked.checked_histories,'checked_deviations':checked.checked_deviations}

def compiler_seed(p,m,rng):
    # Arbitrary Boolean potentials compile to signed CAG incidences.  A large
    # common positive bias only supplies legal, continuation-rich seeds; every
    # eventual reported point comes from the nonnegative full-strategy cone.
    table=[rng.randrange(4) if 1<=b.bit_count()<=m else 0 for b in range(1<<p)]
    c=table[:]
    for a in range(p):
        for b in range(1<<p):
            if b>>a&1:c[b]-=c[b^(1<<a)]
    z=[0]+[(-1)**(b.bit_count()+1)*b.bit_count()*c[b] for b in range(1,1<<p)]
    x=z[:]
    for a in range(p):
        for b in range(1<<p):
            if not b>>a&1:x[b]-=x[b|(1<<a)]
    k=4*sum(abs(v) for v in x[1:])+1
    return [x[b]+k for b in range(1,1<<p)]

def seeds(p,m,rng,compiler=False):
    # Sharp disjoint family: m-1 customers in A, two in B.
    x=[0]*((1<<p)-1);x[0]=m-1;x[1]=2;yield x
    # Customer incidences with sparse, low integer weights preserve credible ties.
    while True:
        if compiler:
            yield compiler_seed(p,m,rng)
            continue
        x=[0]*((1<<p)-1)
        count=rng.randint(p,4*p)
        for _ in range(count):
            size=rng.choices(range(1,p+1),weights=[8,8,4]+[1]*(p-3))[0]
            mask=sum(1<<a for a in rng.sample(range(p),size));x[mask-1]+=rng.randint(1,6)
        yield x

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=5)
    ap.add_argument('--trials',type=int,default=100);ap.add_argument('--cones',type=int,default=1);ap.add_argument('--seed',type=int,default=71021)
    ap.add_argument('--compiler-seeds',action='store_true')
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    rng=random.Random(args.seed);best=bestlast=F(0);records=[];start=time.time();cone_count=0
    for trial,x in zip(range(args.trials),seeds(args.topics,args.players,rng,args.compiler_seeds)):
        inst=instance_from_clones(args.topics,args.players,x);solver=ExactSPESolver(inst)
        choices=[]
        for q in sorted(solver.outcomes()):
            w=inst.welfare(q)
            if not w:continue
            paths=paths_by_action(solver,q)
            for (pos,a),path in paths.items():choices.append((inst.topic_payoff(a,q)/w,pos,a,path,q))
        if not choices:continue
        choices.sort(reverse=True)
        # Attack an arbitrary player, then separately a truly last mover.
        selected=[choices[0],max((z for z in choices if z[1]==args.players-1))]
        for raw,pos,a,path,q in dict.fromkeys(selected):
            for j in range(args.cones):
                cone=credible_policy(solver,q,path,rng,('high','uniform','low')[j%3]);cone_count+=1
                rec=optimize(cone,a)
                if rec is None:continue
                value=rec['value'];last=rec['payoffs'][-1]/rec['welfare']
                if value>best or last>bestlast:
                    best=max(best,value);bestlast=max(bestlast,last);rec.update(trial=trial,queried_position=pos,source_clones=x)
                    records.append(rec)
                    report={'scope':'finite sampled full-history SPE cones; auxiliary payoff cap only','players':args.players,'topics':args.topics,
                      'seed':args.seed,'trials_completed':trial+1,'cones_checked':cone_count,'best_any_share':best,'best_last_share':bestlast,'sharp_candidate_cap':F(2,args.players+1),'elapsed_seconds':time.time()-start,'improvements':records}
                    args.output.write_text(json.dumps(serializable(report),ensure_ascii=False,indent=2)+'\n')
                    print(json.dumps(serializable({'trial':trial,'cones':cone_count,'best_any_share':best,'best_last_share':bestlast,'payoffs':rec['payoffs'],'welfare':rec['welfare'],'path':rec['path']})),flush=True)
                    if best>F(2,args.players+1) or bestlast>F(2,args.players+1):return
        if trial%20==0:print(json.dumps({'progress':trial,'elapsed':time.time()-start}),flush=True)
    report={'scope':'finite sampled full-history SPE cones; auxiliary payoff cap only','players':args.players,'topics':args.topics,
      'seed':args.seed,'trials_completed':args.trials,'cones_checked':cone_count,'best_any_share':best,'best_last_share':bestlast,'sharp_candidate_cap':F(2,args.players+1),'elapsed_seconds':time.time()-start,'improvements':records}
    args.output.write_text(json.dumps(serializable(report),ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
