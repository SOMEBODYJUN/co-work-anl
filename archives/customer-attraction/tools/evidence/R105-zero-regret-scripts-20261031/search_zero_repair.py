"""Attack only the general actual-regret-only welfare-repair implication.

Exploratory finite search, not a search/claim for a half-coverage counterexample.
No output is a proof until an independently replayed exact certificate is saved.
"""
from itertools import combinations_with_replacement
import json
import random
from pathlib import Path


def table(w, k, n):
    out = {}
    for z in combinations_with_replacement(range(k), n):
        cs = [z.count(a) for a in range(k)]
        cov = sum(v for mask,v in enumerate(w) if any(cs[a] and mask >> a & 1 for a in range(k)))
        u = [sum(v * (6 // sum(cs[b] for b in range(k) if mask >> b & 1))
                 for mask,v in enumerate(w) if cs[a] and mask >> a & 1) if cs[a] else 0
             for a in range(k)]
        out[z] = (u,cov)
    return out


def search(seed=420261024, trials=100000, k=4, require_actual_root=False):
    rng = random.Random(seed)
    for it in range(trials):
        w = [0]+[rng.randrange(0,26) if rng.random()<.65 else 0 for _ in range(2**k-1)]
        t2,t3 = table(w,k,2),table(w,k,3)
        def get(t,z,a):return t[tuple(sorted(z))][0][a]
        nb = [[a for a in range(k) if get(t2,(r,a),a)==max(get(t2,(r,b),b) for b in range(k))] for r in range(k)]
        nf = max(min(get(t2,(r,a),r) for a in nb[r]) for r in range(k))
        maxnew = max(t2[tuple(sorted((r,a)))][1] for r in range(k) for a in nb[r] if get(t2,(r,a),r)>=nf)
        all_ob = [[[a for a in range(k) if get(t3,(d,r,a),a)==max(get(t3,(d,r,b),b) for b in range(k))] for r in range(k)] for d in range(k)]
        root_floor=0
        if require_actual_root:
            minima=[]
            for d,ob in enumerate(all_ob):
                floor=max(min(get(t3,(d,r,a),r) for a in ob[r]) for r in range(k))
                minima.append(min(get(t3,(d,r,a),d) for r in range(k) for a in ob[r] if get(t3,(d,r,a),r)>=floor))
            root_floor=max(minima)
        for d,ob in enumerate(all_ob):
            for r in range(k):
                for f in ob[r]:
                    if f not in nb[r] or t2[tuple(sorted((r,f)))][1]<=maxnew:continue
                    if require_actual_root and get(t3,(d,r,f),d)<root_floor:continue
                    vo,vn = get(t3,(d,r,f),r),get(t2,(r,f),r)
                    choices = [[a for a in ob[b] if get(t3,(d,b,a),b)<=vo and get(t2,(b,a),b)<=vn] for b in range(k)]
                    if not all(choices):continue
                    choices[r] = [f]
                    result={'seed':seed,'trial':it,'weights':w,'background':d,'path':[r,f], 'actual_root_required':require_actual_root,
                            'old_policy':[c[0] for c in choices], 'old_welfare':t2[tuple(sorted((r,f)))][1],
                            'maximum_new_SPE_welfare':maxnew}
                    print(json.dumps(result), flush=True)
                    return result
    print(json.dumps({'seed':seed,'trials':trials,'found':False}),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--actual-root',action='store_true');parser.add_argument('--trials',type=int,default=100000)
    a=parser.parse_args();result=search(trials=a.trials,require_actual_root=a.actual_root)
    if result:Path(__file__).with_name('zero_repair_actual_root_candidate.json' if a.actual_root else 'zero_repair_candidate.json').write_text(json.dumps(result,indent=2)+'\n')
