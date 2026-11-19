"""Compare minimum position-specific SPE pay to a common collection of blocker labels.

A prefix is stored as counts only to memoize identical feasible outcome sets.
Each branch independently selects its own full-history equilibrium continuation.
"""
from functools import lru_cache
from itertools import product
import argparse
import json
import random
from first_experiment import PLAYERS, SCALE, bump, metrics


@lru_cache(None)
def counts(total, k):
    if k == 1:
        return ((total,),)
    return tuple((a,) + rest for a in range(total + 1)
                 for rest in counts(total - a, k - 1))


def investigate(w, k, min_remaining, max_remaining, samples):
    leaf = metrics(w, k)

    @lru_cache(None)
    def ev(p):
        if sum(p) == PLAYERS:
            return frozenset((p,)), None
        branches = [ev(bump(p, a))[0] for a in range(k)]
        u = max(min(leaf(c)[0][a] for c in b) for a, b in enumerate(branches))
        return frozenset(c for a, b in enumerate(branches) for c in b if leaf(c)[0][a] >= u), u

    ans = {r: [0, 0, None] for r in range(min_remaining, max_remaining+1)}
    for r in ans:
        for p in counts(PLAYERS-r, k):
            _, u = ev(p)
            candidates = []
            for b in counts(r-1, k):
                pc = tuple(t + s for t, s in zip(p, b))
                candidates.append((max(leaf(bump(pc, a))[0][a] for a in range(k)), b))
            v, b = min(candidates)
            ans[r][0] += 1
            if v > u:
                ans[r][1] += 1
                if ans[r][2] is None:
                    ans[r][2] = {"w": w, "prefix": p, "min_SPE_pay_times60": u,
                                 "minimax_pay_times60": v, "minimizer": b}
    return ans


def main():
    f=argparse.ArgumentParser()
    f.add_argument("--k",type=int,default=3)
    f.add_argument("--bits",type=int,default=2)
    f.add_argument("--draws",type=int)
    f.add_argument("--seed",type=int,default=20261119)
    f.add_argument("--rmin",type=int,default=3)
    f.add_argument("--rmax",type=int,default=3)
    args=f.parse_args()
    k=args.k
    if args.draws is None:
        catalogs=product(range(args.bits+1),repeat=(1<<k)-1)
    else:
        rng=random.Random(args.seed)
        catalogs=(tuple(rng.choice((0,0,0,0,1,2,4,7,11,17)) for _ in range((1<<k)-1))
                  for _ in range(args.draws))
    summary={r:[0,0,None] for r in range(args.rmin,args.rmax+1)}
    for w in catalogs:
        ans=investigate(w,k,args.rmin,args.rmax,None)
        for r,(n,q,example) in ans.items():
            summary[r][0]+=n
            summary[r][1]+=q
            if example and summary[r][2] is None:
                summary[r][2]=example
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
