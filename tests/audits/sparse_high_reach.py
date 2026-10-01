"""Independent exact incidence audit for SPARSE-HIGH-ACYCLIC.

Run: python3 tests/audits/sparse_high_reach.py > evidence/runs/2026-10-01/sparse_high_reach.json
No floating point arithmetic or calls to the production single-overlap solver.
The finite random audit is only an attack on mistakes, not a universal proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
R = Q(9, 5)
SEED = 6384201
TRIALS = 400


def reach(weights, sites):
    return [sum((weights[k] for k in c), Q(0)) for c in sites]


def menu(weights, sites, n):
    rs = reach(weights, sites)
    out = {}
    for i in range(n):
        for j in range(n):
            s, t = i, n+j
            common = sites[s] & sites[t]
            assert len(common) <= 1
            w = weights[next(iter(common))] if common else Q(0)
            V = rs[s]+rs[t]-w
            if not common:
                lo = hi = rs[s]
            elif rs[s]<rs[t]:
                lo = hi = rs[s]
            elif rs[s]>rs[t]:
                lo = hi = rs[s]-w
            else:
                lo, hi = rs[s]-w, rs[s]
            # Pure rule uses the smaller tagged index when reaches tie.
            if not common or rs[s]<rs[t] or (rs[s]==rs[t] and s<t):
                x = rs[s]
            else:
                x = rs[s]-w
            out[i,j] = (lo, hi, V, x, V-x)
    return rs, out


def ratio(v, x):
    if not v:return Q(0)
    return v/x if x else None


def exact_optimum(weights, sites, n):
    rs, tab=menu(weights, sites, n)
    d1=[max(tab[i,j][0] for i in range(n)) for j in range(n)]
    d2=[max(tab[i,j][2]-tab[i,j][1] for j in range(n)) for i in range(n)]
    best=None
    for i in range(n):
        for j in range(n):
            lo,hi,V,_,_=tab[i,j]
            x=min(hi,max(lo,V*d1[j]/(d1[j]+d2[i]) if d1[j]+d2[i] else lo))
            a,b=ratio(d1[j],x),ratio(d2[i],V-x)
            if a is not None and b is not None:
                z=max(Q(1),a,b)
                if best is None or z<best:best=z
    return best


def cycles(successors):
    found=[];visited=set()
    for root in range(len(successors)):
        if root in visited:continue
        path=[];where={};p=root
        while p not in visited and p not in where:
            where[p]=len(path);path.append(p);p=successors[p]
        if p in where:found.append(path[where[p]:])
        visited.update(path)
    return found


def attack(weights, sites, n, r):
    rs,tab=menu(weights, sites, n)
    a=max(rs[:n]);d=max(rs[n:])
    b1=[max(range(n),key=lambda i:(tab[i,j][3],-i)) for j in range(n)]
    b2=[max(range(n),key=lambda j:(tab[i,j][4],-j)) for i in range(n)]
    rings=cycles([n+j for j in b2]+b1)
    pure_stable=any(
        max(tab[k,j][3] for k in range(n))<=r*tab[i,j][3]
        and max(tab[i,k][4] for k in range(n))<=r*tab[i,j][4]
        for i in range(n) for j in range(n))
    balanced=all(r*rs[i]>=a for i in range(n)) and all(r*rs[n+j]>=d for j in range(n))
    if not pure_stable:
        assert not balanced
        for ring in rings:
            assert any((r*rs[v]<a if v<n else r*rs[v]<d) for v in ring)
            for v in ring:
                if v<n and r*rs[v]>=a:
                    assert (rs[n+b2[v]],n+b2[v])<(rs[v],v)
                if v>=n and r*rs[v]>=d:
                    j=v-n;i=b1[j]
                    assert (rs[i],i)<(rs[v],v)
    # The interval oracle is independently assembled from incidence sets.
    optimum=exact_optimum(weights,sites,n)
    if optimum is not None and optimum>r:assert not pure_stable
    return dict(reach=list(map(str,rs)),pure_stable=pure_stable,
                optimum=str(optimum),rings=rings,balanced=balanced)


def random_instance(n,rng):
    cells={(i,j) for i in range(n) for j in range(n)}
    blocks=[]
    while cells:
        i,j=rng.choice(sorted(cells))
        choices=[]
        for ai in range(1,1<<n):
            if not ai&(1<<i):continue
            aa=[u for u in range(n) if ai&(1<<u)]
            for bj in range(1,1<<n):
                if not bj&(1<<j):continue
                bb=[v for v in range(n) if bj&(1<<v)]
                if all((u,v) in cells for u in aa for v in bb):choices.append((aa,bb))
        aa,bb=rng.choice(choices)
        if rng.randrange(5):blocks.append((aa,bb,rng.randint(1,8)))
        cells.difference_update((u,v) for u in aa for v in bb)
    weights=[];sites=[set() for _ in range(2*n)]
    for aa,bb,w in blocks:
        k=len(weights);weights.append(Q(w))
        for i in aa:sites[i].add(k)
        for j in bb:sites[n+j].add(k)
    for s in range(2*n):
        if rng.randrange(3):
            k=len(weights);weights.append(Q(rng.randint(1,12)));sites[s].add(k)
    return weights,sites


def long_cycle_three():
    n=3;M=4*n*n
    weights=[];sites=[set() for _ in range(2*n)]
    ra=[M+2*(n-i)+2 for i in range(1,n+1)]
    rb=[M+2*(n-j)+1 for j in range(1,n+1)]
    for i in range(1,n+1):
        for j in range(1,n):
            w=2*(j+1-i)+1 if i<=j else 2*(i-j)+1
            k=len(weights);weights.append(Q(w));sites[i-1].add(k);sites[n+j-1].add(k)
    for s,R in enumerate(ra+rb):
        w=Q(R)-sum((weights[k] for k in sites[s]),Q(0))
        k=len(weights);weights.append(w);sites[s].add(k)
    return weights,sites


def main():
    lower=json.loads((ROOT/'examples/heterogeneous/rho_lower.json').read_text())
    weights=list(map(Q,lower['weights']))
    sites=list(map(set,lower['locations']))
    sharp=attack(weights,sites,2,R)
    assert sharp['optimum']==str(Q(80193772,44504187))
    assert not sharp['pure_stable'] and not sharp['balanced']
    assert all(R*Q(t)>=max(map(Q,sharp['reach'][2:])) for t in sharp['reach'][2:])
    long=attack(*long_cycle_three(),3,R)
    assert long['balanced'] and long['pure_stable']
    assert len(long['rings'])==1 and len(long['rings'][0])==6
    rng=random.Random(SEED);counts={'pure_bad':0,'mixed_bad':0,'balanced':0,'ties':0,'zero_reach':0}
    for z in range(TRIALS):
        n=2+z%4
        weights,sites=random_instance(n,rng)
        rs=reach(weights,sites)
        counts['ties']+=int(len(set(rs))<len(rs))
        counts['zero_reach']+=int(Q(0) in rs)
        r=(Q(1),Q(3,2),R,Q(2))[z%4]
        result=attack(weights,sites,n,r)
        counts['pure_bad']+=int(not result['pure_stable'])
        counts['mixed_bad']+=int(Q(result['optimum'])>r) if result['optimum']!='None' else 0
        counts['balanced']+=int(result['balanced'])
    print(json.dumps({'schema_version':1,'recorded_on':'2026-10-01',
                      'name':'sparse_high_reach','python_version':sys.version.split()[0],
                      'base_commit':'9e5253f0c187ffdc30d5b742d4937ba52095cea9',
                      'source_sha256':{
                          'tests/audits/sparse_high_reach.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          'examples/heterogeneous/rho_lower.json':hashlib.sha256((ROOT/'examples/heterogeneous/rho_lower.json').read_bytes()).hexdigest()},
                      'replay_commands':['python3 tests/audits/sparse_high_reach.py > evidence/runs/2026-10-01/sparse_high_reach.json'],
                      'limitations':'Finite rational audits do not prove a universal bound; lower example is inherited and its four local NE are unique.',
                      'observed':{'claim':'SPARSE-HIGH-ACYCLIC','arithmetic':'fractions.Fraction',
                      'seed':SEED,'trials':TRIALS,'sizes':'n=2,3,4,5 repeated',
                      'r_values':['1','3/2','9/5','2'],
                      'random_counts':counts,'sharp_lower':sharp,'long_cycle_n3':long}},
                     ensure_ascii=False,indent=2))


if __name__=='__main__':main()
