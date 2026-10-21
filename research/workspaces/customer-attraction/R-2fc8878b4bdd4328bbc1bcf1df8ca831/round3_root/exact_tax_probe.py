"""Attack the stronger actual fractional-load budget on complete SPE cones.

Discovery uses scipy LP. A proposed violation is reconstructed over rationals
and independently checked against every ordered history and every deviation.
The candidate bridge is m max_T g(T) <= W + G, alpha=(m-1)/m,
g(T)=sum_{x in T}1/(1+alpha*c_x), G=sum_{c_x>0}1/(1+alpha*c_x).
"""
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'work.py').is_file() and (p/'.git').exists())
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver, CustomerType
from fractions import Fraction as F
from itertools import product
from math import lcm, gcd
import numpy as np
from scipy.optimize import linprog
import argparse, json, random, time

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=4)
    ap.add_argument('--p',type=int,default=6);ap.add_argument('--trials',type=int,default=50)
    ap.add_argument('--seed',type=int,default=2026102171);args=ap.parse_args()
    m,p=args.m,args.p;rng=random.Random(args.seed);types=tuple(range(1,1<<p))
    histories=[h for k in range(m) for h in product(range(p),repeat=k)]
    def row(q,a):
        return tuple(F(1,sum(q[b] for b in range(p) if mask>>b&1)) if mask>>a&1 else F(0) for mask in types)
    cache={}
    def R(q,a):
        if (q,a) not in cache:cache[q,a]=row(q,a)
        return cache[q,a]
    best=None;start=time.monotonic();records=[]
    for trial in range(args.trials):
        weights={b:rng.randint(1,15) for b in types if rng.random()<rng.uniform(.08,.6)}
        if not weights:weights={1:1}
        ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if b>>a&1),w)for b,w in weights.items()),m)
        solver=ExactSPESolver(ins);outs=tuple(solver.outcomes())
        target=min(outs,key=ins.welfare) if trial%2 else rng.choice(outs)
        cert=solver.certificate(target,action_selector=lambda h,acts:rng.choice(acts),continuation_selector=lambda h,opts:rng.choice(opts))
        actions=cert.actions
        def terminal(h):
            while len(h)<m:h=h+(actions[h],)
            return ins.counts(h),h
        eq=[]
        for h in histories:
            q,path=terminal(h);r=R(q,actions[h])
            for a in range(p):
                if a==actions[h]:continue
                qd,_=terminal(h+(a,));rd=R(qd,a)
                eq.append(tuple(x-y for x,y in zip(r,rd)))
        gam=np.array(eq,dtype=float)
        actual=terminal(())[0];loads=[sum(actual[a]for a in range(p) if b>>a&1)for b in types]
        W=tuple(F(c>0)for c in loads);G=tuple(F(m,m+(m-1)*c)if c else F(0)for c in loads)
        for a in range(p):
            obj=tuple(F(m*m,m+(m-1)*c)*bool(b>>a&1)-w-g for b,c,w,g in zip(types,loads,W,G))
            res=linprog(-np.array(obj,dtype=float),A_ub=-gam,b_ub=np.zeros(len(gam)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
            if res.status==3:raise RuntimeError('unexpected unbounded full SPE cone')
            if not res.success:continue
            val=-res.fun
            if best is None or val>best+1e-8:
                best=val;print(json.dumps({'trial':trial,'topic':a,'best':best,'actual':actual,'seconds':time.monotonic()-start}),flush=True)
            if val>1e-7:
                rat=[F(float(x)).limit_denominator(1000000) for x in res.x]
                if any(sum(x*y for x,y in zip(r,rat))<0 for r in eq):
                    print('rational reconstruction failed',flush=True);continue
                scale=lcm(*(x.denominator for x in rat));iw=[int(x*scale) for x in rat]
                divisor=gcd(*iw);iw=[w//divisor for w in iw]
                violation=sum(x*y for x,y in zip(obj,iw))
                if violation<=0:continue
                newins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if b>>a&1),w)for b,w in zip(types,iw)if w),m)
                from customer_attraction import verify_certificate
                report=verify_certificate(newins,cert);report.assert_valid()
                data={'status':'exact_full_SPE_counterexample_to_auxiliary_bridge','m':m,'p':p,'seed':args.seed,'trial':trial,'query':a,'instance':newins.to_dict(),'strategy':cert.to_dict(),'exact_violation':str(violation),'bridge':'m max_T g(T) <= W+G','actual_counts':actual}
                out=Path(__file__).with_name(f'exact_tax_failure_m{m}p{p}.json');out.write_text(json.dumps(data,indent=2)+'\n')
                print(json.dumps({'saved':str(out),'violation':str(violation),'clients':sum(iw)}),flush=True);return
        records.append({'trial':trial,'outcomes':len(outs),'rows':len(eq)})
    Path(__file__).with_name(f'exact_tax_scan_m{m}p{p}.json').write_text(json.dumps({'m':m,'p':p,'trials':records,'seed':args.seed,'best':best,'status':'finite_probe_only','seconds':time.monotonic()-start},indent=2)+'\n')
if __name__=='__main__':main()
