"""Finite exact attack on two candidate comparisons with the last payoff.

Candidate A: every earlier u_i >= u_m/2.
Candidate B: sum_{i<m} u_i >= (m-1)u_m/2.
Neither candidate is the main half-coverage target. A counterexample here must
be expanded and checked as a full ordered-history SPE before being accepted.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import random
from cex_exact_sweep import IntegerSetSolver, instance, ExactSPESolver


def run(trials=1000, seed=20261022, p=7, m=5):
    s=IntegerSetSolver(p,m);rng=random.Random(seed)
    bestind=Fraction(0);bestagg=Fraction(0);records=[]
    for t in range(trials):
        w=[rng.randrange(1,21) if rng.random()<.1 else 0 for _ in range((1<<p)-1)]
        out=s.solve(w)
        for q in out['root_outcomes']:
            j=s.tindex[q]
            @lru_cache(None)
            def path(k,last):
                if sum(k)==m-1:
                    child=k[:last]+(k[last]+1,)+k[last+1:]
                    if child==q and j in s.last_outcomes[s.sindex[k]]: return (last,)
                    return None
                idx=s.sindex[k]
                threshold=max(min(s.last_utility[c,a] for c in s.last_outcomes[ch]) for a,ch in enumerate(s.children[idx]))
                for a,ch in enumerate(s.children[idx]):
                    if j in s.last_outcomes[ch] and s.last_utility[j,a]>=threshold:
                        nxt=k[:a]+(k[a]+1,)+k[a+1:];tail=path(nxt,last)
                        if tail is not None:return (a,)+tail
                return None
            for a in range(p):
                if not q[a]:continue
                z=path((0,)*p,a)
                if z is None:continue
                us=[int(s.last_utility[j,b]) for b in z]
                if not min(us):continue
                ind=Fraction(us[-1],min(us[:-1]));agg=Fraction((m-1)*us[-1],2*sum(us[:-1]))
                if ind>bestind or agg>bestagg:
                    bestind=max(bestind,ind);bestagg=max(bestagg,agg)
                    r=dict(trial=t,weights=w,path=z,payoffs_scaled=us,scale=s.scale,individual=str(ind),aggregate=str(agg))
                    records.append(r)
                    print(json.dumps({k:v for k,v in r.items() if k!='weights'}),flush=True)
                if ind>2 or agg>1:
                    inst=instance(p,m,w);sol=ExactSPESolver(inst);cert=sol.certificate(on_path=z)
                    from customer_attraction import verify_certificate
                    verify_certificate(inst,cert).assert_valid()
                    return dict(scope='Full SPE counterexample to proposed last-payoff bridge only',
                                players=m,topics=p,trials_run=t+1,seed=seed,records=records,
                                instance=inst.to_dict(),strategy=cert.to_dict())
    return dict(scope='finite exact last-payoff bridge probe; no universal conclusion',
                players=m,topics=p,trials_run=trials,seed=seed,records=records,
                best_individual=str(bestind),best_aggregate=str(bestagg))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--trials',type=int,default=1000)
    ap.add_argument('--seed',type=int,default=20261022);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    result=run(args.trials,args.seed);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
