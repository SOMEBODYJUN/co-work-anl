#!/usr/bin/env python3
"""Attack the general candidate F_r(b)-P <= r min remaining u.

The full ordered strategy is fixed; every nonempty customer interest type is
allowed a nonnegative multiplicity. Floating LPs only discover witnesses. Any
reported witness is rationalized and every full-history inequality is checked
with Fraction before being saved.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
from math import gcd, lcm
import argparse
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def counts(p, total):
    if p == 1:
        yield (total,)
    else:
        for n in range(total+1):
            for tail in counts(p-1, total-n):
                yield (n,)+tail


def read_strategy(path):
    d = json.loads(path.read_text())
    for name in ("strategy", "certificate"):
        if name in d:
            d = d[name]
            break
    if "actions" not in d or "terminal_counts" not in d:
        return None
    a = {tuple(row["history"]): row["action"] for row in d["actions"]}
    p = len(d["terminal_counts"])
    m = sum(d["terminal_counts"])
    expected = {h for t in range(m) for h in product(range(p), repeat=t)}
    if set(a) != expected:
        return None
    return p, m, a


def probe(path, roots_only=False, max_checks=0):
    got = read_strategy(path)
    if got is None:
        return {"source":str(path.relative_to(ROOT)), "skip":"not a complete strategy"}
    p, m, actions = got
    if p > 7 or m > 5:
        return {"source":str(path.relative_to(ROOT)), "skip":"scope cap", "p":p,"m":m}
    masks = range(1, 1 << p)
    memberships = tuple(tuple(t for t in range(p) if mask >> t & 1) for mask in masks)

    @lru_cache(None)
    def finish(h):
        if len(h) == m:
            return h
        return finish(h+(actions[h],))

    @lru_cache(None)
    def payoff(path, selected):
        return tuple(F(int(selected in s), sum(t in s for t in path))
                     if selected in s else F(0) for s in memberships)

    @lru_cache(None)
    def terminal(h):
        z = finish(h)
        return tuple(z.count(t) for t in range(p))

    exact_rows=[]
    for h in sorted(actions, key=lambda h:(len(h), h)):
        a=actions[h]
        actual=payoff(finish(h),a)
        for t in range(p):
            if t==a:
                continue
            alt=payoff(finish(h+(t,)),t)
            row=tuple(x-y for x,y in zip(actual,alt))
            if any(row):
                exact_rows.append(row)
    exact_rows=list(dict.fromkeys(exact_rows))
    aub=-np.array(exact_rows,dtype=float)
    bub=np.zeros(len(exact_rows))
    eq=np.ones((1,len(memberships)))
    best=F(0);checks=0;worst=None
    # Equal count histories can have different realized continuations, so retain
    # each distinct (background, remaining terminal) pair.
    states={}
    for h in sorted(actions,key=lambda h:(len(h),h)):
        if roots_only and h:
            continue
        r=m-len(h)
        # r<=2 has an independent stronger floor proof; only attack r>=3.
        if r <= 2:
            continue
        b=tuple(h.count(t) for t in range(p))
        c=terminal(h)
        states.setdefault((b,c),h)
    for (b,c),h in states.items():
        r=m-len(h)
        remaining=tuple(v-w for v,w in zip(c,b))
        pcoef=tuple(F(sum(remaining[t] for t in s),sum(c[t] for t in s))
                    if sum(remaining[t] for t in s) else F(0) for s in memberships)
        for topic in range(p):
            if not remaining[topic]:
                continue
            ucoef=payoff(finish(h),topic)
            for q in counts(p,r):
                fcoef=tuple(F(sum(q[t] for t in s),sum((b[t]+q[t]) for t in s))
                            if sum(q[t] for t in s) else F(0) for s in memberships)
                obj=tuple(v-w-r*u for v,w,u in zip(fcoef,pcoef,ucoef))
                if all(v<=0 for v in obj):
                    continue
                checks+=1
                sol=linprog(-np.array(obj,dtype=float),A_ub=aub,b_ub=bub,
                            A_eq=eq,b_eq=[1.],bounds=(0,None),method="highs")
                if sol.success and -sol.fun>float(best)+1e-9:
                    vals=[F(float(x)).limit_denominator(1000000) for x in sol.x]
                    den=lcm(*(v.denominator for v in vals))
                    weights=[int(v*den) for v in vals]
                    div=gcd(*weights)
                    weights=[v//div for v in weights]
                    slack=min(sum(v*x for v,x in zip(row,weights)) for row in exact_rows)
                    gap=sum(v*x for v,x in zip(obj,weights))
                    if slack>=0 and gap>0:
                        total=sum(weights)
                        best=gap/total
                        worst={"history":h,"terminal_path":finish(h),"r":r,
                               "background":b,"comparison":q,"topic":topic,
                               "weights":[{"mask":mask,"multiplicity":weights[mask-1]}
                                          for mask in masks if weights[mask-1]],
                               "comparison_profit":str(sum(v*x for v,x in zip(fcoef,weights))),
                               "actual_profit":str(sum(v*x for v,x in zip(pcoef,weights))),
                               "designated_payoff":str(sum(v*x for v,x in zip(ucoef,weights))),
                               "gap":str(gap),"minimum_SPE_slack":str(slack),
                               "normalized_gap":str(best),"full_SPE_rows":len(exact_rows)}
                        output={"source":str(path.relative_to(ROOT)),"players":m,"topics":p,
                                "scope":"exact witness to the auxiliary gap candidate, not half",
                                "witness":worst}
                        (HERE/"gap_cone_witness.json").write_text(json.dumps(output,indent=2)+"\n")
                        print(json.dumps(output),flush=True)
                        return output
                if max_checks and checks>=max_checks:
                    return {"source":str(path.relative_to(ROOT)),"checks":checks,"stopped":"cap"}
    return {"source":str(path.relative_to(ROOT)),"players":m,"topics":p,
            "full_SPE_rows":len(exact_rows),"states":len(states),"checks":checks,"witness":worst}


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("paths",nargs="*")
    ap.add_argument("--roots-only",action="store_true")
    ap.add_argument("--max-checks",type=int,default=0)
    args=ap.parse_args()
    sources=[ROOT/s for s in args.paths] if args.paths else sorted((ROOT/"evidence/certificates/customer_attraction").glob("*.json"))
    reports=[]
    for path in sources:
        out=probe(path,args.roots_only,args.max_checks)
        reports.append(out)
        print(json.dumps(out),flush=True)
        (HERE/"gap_cone_probe_report.json").write_text(json.dumps(reports,indent=2)+"\n")
        if out.get("witness"):
            break
