"""Finite discovery diagnostic for the direct all-player half floor.
All optimized rows come from the entire ordered-history policy, not only a path.
A float LP is never accepted as an exact counterexample.
"""
import argparse,importlib.util,itertools,json,math,random,sys,time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('floor_lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
lib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lib;spec.loader.exec_module(lib)
OUT=Path(__file__).parent

def random_policy(k,m,w,rng):
    """Random independent tie selection at every ordered history; exact integer payoffs."""
    scale=math.lcm(*range(1,m+1));actions={};terminals={}
    @lru_cache(None)
    def pay(z,a):
        return sum(v*(scale//sum(z[b] for b in range(k) if mask>>b&1))
                   for mask,v in enumerate(w,1) if v and mask>>a&1)
    for depth in range(m,-1,-1):
        for h in itertools.product(range(k),repeat=depth):
            if depth==m:terminals[h]=tuple(h.count(a) for a in range(k));continue
            vals=[pay(terminals[h+(a,)],a) for a in range(k)]
            acts=[a for a,v in enumerate(vals) if v==max(vals)]
            a=rng.choice(acts);actions[h]=a;terminals[h]=terminals[h+(a,)]
    return actions

def exact_candidate(c,r,u,J,policy):
    # The equality for normalization is u.w=1, unlike the library recoverer W.w=1.
    vals=tuple(Fraction(float(v)).limit_denominator(10**7) for v in r.x)
    if not c.verify(vals) or lib.dot(u,vals)!=1:return None
    O=lib.dot(lib.coverage_row(c.topics,J),vals)
    if O<=2*c.players:return None
    clones=lib.integer_clones(vals)
    assert lib.independently_verify(c,clones)
    return {'players':c.players,'topics':c.topics,'portfolio':J,'objective':str(O),
            'clones':clones,'actions':[{'history':h,'action':a} for h,a in policy.items()]}

def run(k,m,cases,seed):
    rng=random.Random(seed);records=[];best=-1
    for case in range(cases):
        # Adversarial tie geometry: odd cycle, then periodically perturbed cycle.
        w=[0]*((1<<k)-1)
        for a in range(k):w[((1<<a)|(1<<((a+1)%k)))-1]=1
        if case%4==3:
            for _ in range(k//2):
                mask=rng.randrange(1,1<<k);w[mask-1]+=rng.randrange(1,3)
        policy=random_policy(k,m,w,rng);c=lib.StrategyCone(k,m,policy)
        path=[];h=()
        while len(h)<m:path.append(policy[h]);h+=(policy[h],)
        # Test each distinct on-path payoff; cheap total-union upper filter first.
        local=[]
        for a in sorted(set(path)):
            u=lib.payoff_row(k,c.root,a)
            kwargs=dict(A_ub=-c.matrix,b_ub=np.zeros(len(c.rows)),A_eq=[np.array(u,float)],b_eq=[1],bounds=(0,None),method='highs')
            rr=linprog(-np.ones(len(u)),**kwargs)
            if not rr.success:raise RuntimeError(rr.message)
            cap=-rr.fun
            if cap<=2*m+1e-7:
                local.append({'action':a,'union_upper_float':cap});continue
            lb=-1;bestJ=None
            for J in itertools.combinations(range(k),min(m,k)):
                rr=linprog(-np.array(lib.coverage_row(k,J),float),**kwargs)
                if not rr.success:raise RuntimeError(rr.message)
                if -rr.fun>lb:lb=-rr.fun;bestJ=J
                if -rr.fun>2*m+1e-7:
                    candidate=exact_candidate(c,rr,u,J,policy)
                    if candidate:
                        (OUT/'direct_floor_candidate.json').write_text(json.dumps(candidate,indent=2)+'\n')
                        return records,candidate
            best=max(best,lb)
            local.append({'action':a,'union_upper_float':cap,'portfolio_bound_float':lb,'portfolio':bestJ})
        rec={'case':case,'k':k,'m':m,'policy_rows':len(c.rows),'path':path,'checks':local}
        records.append(rec)
        (OUT/f'direct_floor_probe_n{m}_k{k}_seed{seed}.json').write_text(json.dumps({'scope':'finite floating diagnostics only','seed':seed,'records':records},indent=2)+'\n')
        print(case,local,flush=True)
    return records,None
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=4);ap.add_argument('--cases',type=int,default=24);ap.add_argument('--seed',type=int,default=231026)
    a=ap.parse_args();run(a.topics,a.players,a.cases,a.seed)
