"""Fresh, exact finite checks for the 035b repair; no general theorem is inferred."""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
from collections import Counter
import json


def perfect(q, triples):
    return any(all(len({a[t] for a in chosen}) == q for t in range(3))
               for chosen in combinations(triples, q))


def half_jobs(q, triples):
    s = len(triples)
    jobs = []
    for x in range(q):
        choices = [(x, 1)] + [(q+a, 2) for a, v in enumerate(triples) if v[0] == x]
        jobs.extend([tuple(choices)] * 3)
    for a, (_, y, z) in enumerate(triples):
        jobs.append(((q+a, 1), (q+s+y, 2)))
        jobs.append(((q+a, 1), (2*q+s+z, 2)))
    return 3*q+s+1, jobs


def feasible(m, jobs, cap):
    groups = list(Counter(tuple(sorted(v)) for v in jobs).items())
    options = tuple(g[0] for g in groups)
    counts = tuple(g[1] for g in groups)
    @lru_cache(None)
    def dfs(rem, loads):
        if not any(rem):
            return True
        viable = [(sum(loads[i]+p <= cap for i,p in options[g]), -len(options[g]), g)
                  for g,c in enumerate(rem) if c]
        count, _, g = min(viable)
        if count == 0:
            return False
        nxt = list(rem); nxt[g] -= 1; nxt = tuple(nxt)
        for i,p in options[g]:
            if loads[i]+p <= cap:
                ls = list(loads); ls[i] += p
                if dfs(nxt, tuple(ls)):
                    return True
        return False
    answer = dfs(counts, (0,)*m)
    return answer, dfs.cache_info().misses


def half_check():
    tests = yes = states = 0
    for q in range(3):
        universe = list(product(range(q), repeat=3))
        for mask in range(1 << len(universe)):
            triples = [a for i,a in enumerate(universe) if mask >> i & 1]
            source = perfect(q, triples)
            m, jobs = half_jobs(q, triples)
            actual, ns = feasible(m, jobs, 2)
            assert actual == source
            allsmall, _ = feasible(m, jobs, 3)
            assert allsmall
            assert m == len(triples)+3*q+1
            assert len(jobs) == 3*q+2*len(triples)
            assert sum(map(len,jobs)) == 3*q+7*len(triples)
            tests += 1; yes += source; states += ns
    extras = [
        (1, [(0,0,0)]*2),
        (2, [(0,0,0),(0,0,0),(1,1,1)]),
        (2, [(0,0,0),(0,1,1)]),
        (3, [(0,0,0),(1,1,1),(2,2,2)]),
        (3, [(0,0,0),(1,1,1),(2,1,2)]),
    ]
    for q, triples in extras:
        m,jobs=half_jobs(q,triples); actual,ns=feasible(m,jobs,2)
        assert actual == perfect(q,triples)
        states += ns
    for delta in [F(0), F(1,3), F(49,100), F(499999,1000000)]:
        assert (2*(1+delta)).numerator // (2*(1+delta)).denominator == 2
    m,jobs=half_jobs(1,[])
    assert not feasible(m,jobs,2)[0] and feasible(m,jobs,3)[0]
    return dict(exhaustive_sources=tests, exhaustive_yes=yes, extra_sources=len(extras),
                raw_schedule_states=states, delta_endpoint_checked=True)


def optimum(m, jobs):
    ans = None
    for choices in product(*jobs):
        loads = [F(0)]*m
        for i,p in choices:
            loads[i] += p
        peak = max(loads)
        ans = peak if ans is None else min(ans, peak)
    return ans if ans is not None else F(0)


def pair_check():
    cases = equal = 0
    for vals in product([F(0),F(1,3),F(1),F(5,3)], repeat=4):
        a,b,c,d = vals
        old = [[(0,a),(1,b)],[(1,c),(2,d)]]
        opt = optimum(3,old)
        for H in [F(1,3),F(1),F(5,3)]:
            new=[[(0,a),(3,H)],[(1,b),(3,H)],[(1,c),(4,H)],[(2,d),(4,H)]]
            optp=optimum(5,new)
            assert min(opt,2*H) <= optp <= max(opt,H)
            if H <= opt <= 2*H:
                assert optp == opt
                equal += 1
            cases += 1
    assert optimum(2,[[(0,F(0)),(1,F(7))]]) == 0
    assert optimum(3,[[(0,F(0)),(2,F(1))],[(1,F(7)),(2,F(1))]]) == 1
    # At C=2H both child jobs can be at the middle machine: strictness is necessary.
    assert F(1)+F(1) == 2*F(1)
    coupling_entries=0
    for a in [F(0),F(1),F(1,97),F(13,101),F(1,2)]:
        mu={('j','u0'):a/3,('j','u1'):2*a/3,('u2',):(1-a)/4,('u3',):3*(1-a)/4}
        nu={('v0',):a/5,('v1',):4*a/5,('j','v2'):(1-a)/7,('j','v3'):6*(1-a)/7}
        mu={s:w for s,w in mu.items() if w}; nu={s:w for s,w in nu.items() if w}
        z={}
        for s,w in mu.items():
            for r,v in nu.items():
                if ('j' in s) != ('j' in r):
                    denom=a if 'j' in s else 1-a
                    assert denom > 0
                    z[s,r]=w*v/denom
        assert sum(z.values()) == 1
        assert all(sum(v for (s,r),v in z.items() if s==ss)==w for ss,w in mu.items())
        assert all(sum(v for (s,r),v in z.items() if r==rr)==w for rr,w in nu.items())
        coupling_entries += len(z)
    return dict(subdivision_inputs=cases, equal_value_inputs=equal,
                full_marginal_probability_cases=5, coupling_entries=coupling_entries)


def slot_check():
    witnesses = matchings = joint = 0
    def check(p,x,h):
        nonlocal witnesses, matchings, joint
        m=len(p); n=len(x[0]); adjacency=[[] for _ in range(n)]; slots=[]
        ell=[sum(p[i][j]*x[i][j] for j in range(n)) for i in range(m)]
        b=[max([p[i][j] for j in range(n) if x[i][j]] or [F(0)]) for i in range(m)]
        for i in range(m):
            pos=F(0)
            for j in sorted(range(n),key=lambda j:(-p[i][j],j)):
                end=pos+x[i][j]
                for k in range(pos.numerator//pos.denominator, -(-end.numerator//end.denominator)):
                    if min(end,k+1)>max(pos,k):
                        key=(i,k)
                        if key not in slots: slots.append(key)
                        adjacency[j].append(key)
                pos=end
        found=False
        for assign in product(*adjacency):
            if len(set(assign)) != n: continue
            found=True; loads=[F(0)]*m
            for j,(i,k) in enumerate(assign): loads[i]+=p[i][j]
            assert all(loads[i] <= ell[i]+b[i] for i in range(m))
            if all(ell[i] <= F(5,4)-h[i] for i in range(m)):
                assert all(loads[i]+h[i] <= F(7,4) for i in range(m))
                joint+=1
            matchings+=1
        assert found
        witnesses+=1
    for n in range(4):
        for times in product([F(0),F(1,4),F(1,2)], repeat=2*n):
            p=[times[:n],times[n:]]
            for splits in product([F(0),F(1,2),F(1)], repeat=n):
                x=[splits,tuple(1-v for v in splits)]
                check(p,x,[F(0),F(0)])
                check(p,x,[F(3,4),F(0)])
    check([[F(1,2),F(1,4)],[F(1,3),F(0)]],
          [[F(1,97),F(96,97)],[F(96,97),F(1,97)]],[F(3,4),F(0)])
    # Zero target/empty task are included above; the zero-time-only witness uses no division by T.
    return dict(fractional_witnesses=witnesses, all_support_matchings=matchings,
                joint_capacity_matchings=joint, long_denominator_case=True)


def search_check():
    cases=0
    for opt in range(1,10):
        for upper in range(opt,12):
            for mask in range(1 << (opt-1)):
                accepts=lambda k: k>=opt or (k>0 and bool(mask >> (k-1)&1))
                low,high=0,upper
                while high-low>1:
                    mid=(high+low)//2
                    if accepts(mid): high=mid
                    else: low=mid
                    assert low<opt and accepts(high)
                assert high<=opt
                cases+=1
    return dict(nonmonotone_one_sided_patterns=cases)


if __name__ == '__main__':
    result={'half_unit':half_check(),'subdivision':pair_check(),
            'ordered_slots':slot_check(),'threshold_search':search_check(),
            'limits':'Finite exact checks only. General statements rely on the cited proofs; no general H finder, CONFIG solver, or global coupling is implemented.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
