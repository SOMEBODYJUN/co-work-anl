"""Independent Fraction attack on dynamic and mixed maximal-theme floors.

No imports from the canonical solver, model, primary audit, or earlier audits.
Each child menu is independently selectable at each ordered history, retaining
all history-dependent pure ties. Finite success audits the implementation and
does not replace the universal proof. Default execution prints a report only;
--output refuses to overwrite an existing frozen report.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from random import Random
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / 'research/current/customer_attraction/dynamic_maxima_bound.md'


def case(themes, n):
    # Keep duplicate action labels; only inclusion maxima are deduplicated.
    themes = tuple(sorted(themes))
    k = len(themes)
    maxima = tuple(a for a in sorted(set(themes))
                   if not any(a != b and a & b == a for b in themes))
    s = len(maxima)
    assert s >= 1
    union = 0
    core = maxima[0]
    for a in maxima:
        union |= a
        core &= a
    c, u = core.bit_count(), union.bit_count()
    customers = tuple(1 << i for i in range(union.bit_length()) if union & (1 << i))
    interests = tuple(tuple(a for a, theme in enumerate(themes) if theme & x) for x in customers)
    core_interests = tuple(tuple(j for j, theme in enumerate(maxima) if theme & x) for x in customers)
    routes = tuple(tuple(j for j, m in enumerate(maxima) if theme & m == theme) for theme in themes)
    private = sum(1 for x, incidence in zip(customers, core_interests)
                  if len(incidence) == 1 and not core & x)
    shared = u-c-private
    refined = n == 5 and 2 <= s <= 5
    b = (F(2,25), F(1,11), F(2,19), F(1,8), F(2,15))
    stats = {'states': 0, 'current_comparisons': 0, 'root_outcomes': 0, 'budgets': 0,
             'refined_comparisons': 0, 'mixed_comparisons': 0,
             'singleton_comparisons': 0, 'duplicate_label_cases': int(k != len(set(themes))),
             'routed_budget_comparisons': 0, 'complete_strategies': 0,
             'ordered_histories': 0, 'ordered_deviation_comparisons': 0}
    raw_a, raw_b = [], []
    for t in range(n):
        if t == n-1:
            raw_a.append(F(1,n+s-1))
            raw_b.append(F(n+1,n*(n+s-1)))
        else:
            z = F(t)+F(s*(n-t),2)
            raw_a.append(F(n+t,2*(t+1))/z)
            raw_b.append(1/z)
    env_a = tuple(min(raw_a[t:]) for t in range(n))
    env_b = tuple(min(raw_b[t:]) for t in range(n))
    if s >= 2:
        assert all(raw_b[t] <= raw_b[t+1] for t in range(n-1))

    @lru_cache(None)
    def utility(a, q):
        return sum((F(1, sum(q[b] for b in interest)) for x, interest in zip(customers, interests)
                    if themes[a] & x), F(0))

    @lru_cache(None)
    def solve(p):
        t = sum(p)
        stats['states'] += 1
        if t == n:
            return frozenset((p,))
        children = []
        for a in range(k):
            pa = list(p)
            pa[a] += 1
            children.append(solve(tuple(pa)))
        threshold = max(min(utility(a, q) for q in child) for a, child in enumerate(children))
        claimed = (F(c,n)+F(u-c,max(F(t)+F(s*(n-t),2),F(n+s-1)))) if s >= 2 else F(0)
        allowed = set()
        for a, child in enumerate(children):
            for q in child:
                payoff = utility(a, q)
                if payoff >= threshold:
                    stats['current_comparisons'] += 1
                    assert payoff >= claimed, (themes, n, p, a, q, payoff, claimed)
                    if s >= 2:
                        mixed_floor = F(c,n)+private*env_a[t]+shared*env_b[t]
                        assert payoff >= mixed_floor, (themes,n,p,a,q,payoff,mixed_floor)
                        stats['mixed_comparisons'] += 1
                    elif t == n-1:
                        assert themes[a] == maxima[0]
                        stats['singleton_comparisons'] += 1
                    if refined:
                        refined_floor = F(c,5) + F(private,9) + b[t]*shared
                        assert payoff >= refined_floor, (themes,n,p,a,q,payoff,refined_floor)
                        stats['refined_comparisons'] += 1
                    allowed.add(q)
        assert allowed

        # Attack prefix budget for three independent legal route choices.
        r = n-t
        for mode in range(3):
            route = tuple(options[0] if mode == 0 else options[-1] if mode == 1
                          else options[(a+t) % len(options)] for a, options in enumerate(routes))
            route_counts = [sum(p[a] for a in range(k) if route[a] == j) for j in range(s)]
            weights = [F(pj) + (F(r,2) if r >= 2 else 1) for pj in route_counts]
            g = [F(0) for _ in range(s)]
            routed_g = [F(0) for _ in range(s)]
            for x, actual, incidence in zip(customers, interests, core_interests):
                if core & x:
                    continue
                covered = sum(p[a] for a in actual)
                routed_covered = sum(route_counts[j] for j in incidence)
                for j in incidence:
                    denominator = route_counts[j]+1 if len(incidence) == 1 else covered+r
                    g[j] += F(1, denominator)
                    routed_denominator = route_counts[j]+1 if len(incidence) == 1 else routed_covered+r
                    routed_g[j] += F(1,routed_denominator)
            if s >= 2:
                assert sum(weights[j]*g[j] for j in range(s)) >= u-c
                assert max(g) >= F(u-c, sum(weights))
                assert sum(weights[j]*routed_g[j] for j in range(s)) >= u-c
                assert max(routed_g) >= F(u-c,sum(weights))
                raw_floor = ((F(n+t,2*(t+1))*private+shared)/sum(weights)
                             if r >= 2 else (private+F(n+1,n)*shared)/sum(weights))
                assert max(routed_g) >= raw_floor
                if refined:
                    assert max(routed_g) >= F(private,9)+b[t]*shared
                stats['routed_budget_comparisons'] += 1
            stats['budgets'] += 1
        return frozenset(allowed)

    roots = solve((0,) * k)
    stats['root_outcomes'] = len(roots)
    floor = (F(c)+(u-c)*sum((1/max(F(t)+F(s*(n-t),2),F(n+s-1))
                           for t in range(n)),F(0))) if s >= 2 else F(u)
    for q in roots:
        covered = 0
        for a, multiplicity in enumerate(q):
            if multiplicity:
                covered |= themes[a]
        assert covered.bit_count() >= floor, (themes, n, q, covered.bit_count(), floor)
        if s >= 2:
            assert covered.bit_count() >= c+private*sum(env_a)+shared*sum(env_b)
        if refined:
            assert sum(b) == F(67027,125400)
            refined_welfare = c + F(5*private,9) + F(67027,125400)*shared
            assert covered.bit_count() >= refined_welfare

    # Independently expand one supported root into all ordered histories,
    # then replay every one-step deviation under that actual full policy.
    if n <= 2 or (n == 3 and k <= 3):
        strategy = {}
        target = min(roots)

        def expand(h, p, desired):
            if len(h) == n:
                assert p == desired
                return
            children = []
            for a in range(k):
                pa = list(p)
                pa[a] += 1
                children.append((tuple(pa),solve(tuple(pa))))
            threshold = max(min(utility(a,q) for q in child) for a,(_,child) in enumerate(children))
            chosen = next(a for a,(_,child) in enumerate(children)
                          if desired in child and utility(a,desired) >= threshold)
            strategy[h] = chosen
            for a,(pa,child) in enumerate(children):
                qa = desired if a == chosen else min(child,key=lambda q:(utility(a,q),q))
                expand(h+(a,),pa,qa)

        def follow(h):
            while len(h) < n:
                h += (strategy[h],)
            return tuple(h.count(a) for a in range(k))

        expand((),(0,)*k,target)
        assert follow(()) == target
        assert len(strategy) == sum(k**t for t in range(n))
        for h,a in strategy.items():
            actual = follow(h)
            for alternative in range(k):
                deviation = follow(h+(alternative,))
                assert utility(a,actual) >= utility(alternative,deviation)
                stats['ordered_deviation_comparisons'] += 1
        stats['complete_strategies'] += 1
        stats['ordered_histories'] += len(strategy)
    return stats


def random_catalog(rng, s, x):
    # One mandatory private customer per maximum ensures distinct antichain.
    maxima = [1 << j for j in range(s)]
    for i in range(s, x):
        incidence = rng.randrange(1, 1 << s)
        for j in range(s):
            if incidence & (1 << j):
                maxima[j] |= 1 << i
    themes = set(maxima)
    # Random internal subthemes include core omissions and multi-parent routes.
    for _ in range(rng.randrange(4)):
        base = maxima[rng.randrange(s)]
        themes.add(base & rng.getrandbits(x))
    if rng.random() < 0.25:
        themes.add(0)
    return themes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--random-cases',type=int,default=180)
    args = parser.parse_args()
    rng = Random(782993)
    totals = {key: 0 for key in ['cases', 'states', 'current_comparisons', 'root_outcomes', 'budgets',
                              'refined_comparisons','mixed_comparisons','singleton_comparisons',
                              'duplicate_label_cases','routed_budget_comparisons','complete_strategies',
                              'ordered_histories','ordered_deviation_comparisons']}
    # Exhaust all antichains and internal actions on at most three customers.
    for x in range(2, 4):
        masks = range(1 << x)
        for size in range(2, min(5, len(masks))+1):
            for themes in combinations(masks, size):
                maxima = [a for a in themes if not any(a != b and a & b == a for b in themes)]
                if len(maxima) < 2:
                    continue
                for n in range(1, 5):
                    stats = case(themes, n)
                    totals['cases'] += 1
                    for key, value in stats.items():
                        totals[key] += value
    for serial in range(args.random_cases):
        s = rng.randrange(2, 7)
        x = rng.randrange(s, s+7)
        themes = random_catalog(rng, s, x)
        n = rng.randrange(1, 7)
        stats = case(themes, n)
        totals['cases'] += 1
        for key, value in stats.items():
            totals[key] += value
    # No globally private customers, crossing incidences, shared subactions with
    # several containing maxima, and optional core omitted by internal actions.
    for s in range(3, 6):
        for graph in ('cycle', 'complete'):
            edges = [(i,(i+1)%s) for i in range(s)] if graph == 'cycle' else list(combinations(range(s),2))
            for add_core in (False,True):
                maxima = [0]*s
                for x, edge in enumerate(edges):
                    for j in edge:
                        maxima[j] |= 1 << x
                if add_core:
                    maxima = [a | (1 << len(edges)) for a in maxima]
                themes = set(maxima)
                themes.update((0, maxima[0]&maxima[1], maxima[0]&((1 << len(edges))-1)))
                for n in range(1, 7):
                    stats = case(themes,n)
                    totals['cases'] += 1
                    for key,value in stats.items():
                        totals[key] += value
    # Unique maximal coverage and repeated fullmax/subset labels, including zero.
    for themes in ((0,), (0,0), (7,3,1,0), (7,7,3,3,0), (3,5,3,1,0)):
        for n in range(1,6):
            stats = case(themes,n)
            totals['cases'] += 1
            for key,value in stats.items():
                totals[key] += value

    # Exact arithmetic crosschecks of four-maximal and Jensen corollaries.
    assert [sum((1/max(F(t)+F(4*(n-t),2),F(n+3)) for t in range(n)),F(0))
            for n in (3,4,5)] == [F(1,2),F(31,56),F(211,360)]
    for n in range(2,101):
        total = sum((F(n)+max(F(3*r,2),F(4)) for r in range(1,n+1)),F(0))
        assert total == F(7*n*n+3*n+14,4)
        if n >= 6:
            assert F(4*n*n,7*n*n+3*n+14) > F(1,2)
    output = {'status':'passed','arithmetic':'Fraction','seed':782993,
              'counts':totals,
              'scope':'independent complete continuation menus and exact routing budgets; universal proof separate',
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'proof_sha256':hashlib.sha256(PROOF.read_bytes()).hexdigest(),
              'proof_path':str(PROOF.relative_to(ROOT))}
    if args.output:
        path = args.output if args.output.is_absolute() else ROOT/args.output
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite {path}')
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('x') as stream:
            stream.write(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
