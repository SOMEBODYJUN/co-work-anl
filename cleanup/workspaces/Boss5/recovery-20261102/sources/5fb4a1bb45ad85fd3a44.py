#!/usr/bin/env python3
"""Exact finite regression, not a proof of the universally stated theorems."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent


def weak_compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in weak_compositions(total - first, parts - 1):
                yield (first,) + tail


def independent_payoffs(rows):
    r = len(rows[0])
    result = []
    for j in range(r):
        dist = [F(1)]
        for row in rows:
            new = [F(0)] * (len(dist) + 1)
            for k, prob in enumerate(dist):
                new[k] += prob * (1-row[j])
                new[k+1] += prob * row[j]
            dist = new
        result.append(sum((prob/F(k+1) for k, prob in enumerate(dist)), F(0)))
    return result


def singleton_regression():
    cases = backgrounds = constructed = 0
    for r in range(1, 8):
        for k in range(0, 10):
            cases += 1
            a, s = divmod(k, r)
            value = (F(r-s,a+1)+F(s,a+2))/r
            minimum = None
            minimizers = []
            for h in weak_compositions(k, r):
                backgrounds += 1
                observed = sum((F(1,1+x) for x in h),F(0))/r
                assert observed >= value
                balanced = all(x in (a,a+1) for x in h)
                assert (observed == value) == balanced
                if observed == value:
                    minimizers.append(h)
                minimum = observed if minimum is None else min(minimum, observed)
            assert minimum == value
            assert len(minimizers) == comb(r,s)
            # Uniform high-load s-subset gives the claimed exact dual.
            for j in range(r):
                dual = sum((F(1,1+h[j]) for h in minimizers),F(0))/len(minimizers)
                assert dual == value
            # The proved necessary divisibility condition is not inferred from computation.
            if s == 0 or r % s == 0:
                rows = []
                for j in range(r):
                    for unused in range(a):
                        rows.append([F(int(i == j)) for i in range(r)])
                if s:
                    width = r // s
                    for block in range(s):
                        rows.append([F(int(block*width <= i < (block+1)*width),width) for i in range(r)])
                assert len(rows) == k
                if rows:
                    assert independent_payoffs(rows) == [value]*r
                else:
                    assert value == 1
                constructed += 1
    return dict(parameter_cases=cases, background_vectors=backgrounds,
                independent_optima_explicitly_constructed=constructed)


def quantitative_regression():
    rng = random.Random(20261021)
    cases = 0
    minimum_ratio = None
    for n in range(3, 11):
        r = n-1
        value = F(n+1,2*n)
        bound = F(r*(n-2),2*n*n*(n*n+2*r*r))
        assert bound > 0
        assert bound < F(1,2*r*n)
        for unused in range(150):
            rows = []
            for i in range(r):
                masses = [rng.randint(0,12) for j in range(n)]
                if not sum(masses):
                    masses[0] = 1
                rows.append([F(x,sum(masses)) for x in masses])
            payoffs = independent_payoffs(rows)
            delta = max(payoffs)-value
            assert delta >= bound
            ratio = delta/bound
            minimum_ratio = ratio if minimum_ratio is None else min(minimum_ratio,ratio)
            cases += 1
    return dict(exact_random_product_cases=cases,
                minimum_gap_to_proved_bound_ratio=str(minimum_ratio))


def thirty_six_regression():
    customers = []
    for x in range(3):
        for y in range(3,6):
            customers.append(({x,y},1))
    for xs in combinations(range(3),2):
        for ys in combinations(range(3,6),2):
            customers.append((set(xs+ys),3))
    assert sum(w for unused,w in customers) == 36

    def payoff(a, bg):
        return sum((F(w,1+sum(b in topicset for b in bg))
                    for topicset,w in customers if a in topicset),F(0))

    counts = dict(same_group_distinct=0,cross_group=0,repeated=0)
    good = []
    for bg in combinations_with_replacement(range(6),2):
        values = [payoff(a,bg) for a in range(6)]
        if bg[0] == bg[1]:
            kind,expected = 'repeated',F(37,3)
        elif (bg[0]//3) == (bg[1]//3):
            kind,expected = 'same_group_distinct',F(10)
            good.append(bg)
        else:
            kind,expected = 'cross_group',F(97,9)
        assert sum(values,F(0))/6 == expected
        counts[kind] += 1
    assert counts == dict(same_group_distinct=6,cross_group=9,repeated=6)
    assert [payoff(a,(0,1)) for a in range(6)] == list(map(F,[9,9,12,10,10,10]))
    assert [payoff(a,(0,3)) for a in range(6)] == [F(25,3),F(12),F(12),F(25,3),F(12),F(12)]
    assert [payoff(a,(0,0)) for a in range(6)] == [F(7),F(15),F(15),F(37,3),F(37,3),F(37,3)]
    for t in [F(i,10) for i in range(11)]:
        for a in range(6):
            observed = sum((payoff(a,bg)*(t if bg[0]<3 else 1-t)/3 for bg in good),F(0))
            assert observed == 10
    for mass in [F(i,10) for i in range(11)]:
        p = [mass/3]*3+[(1-mass)/3]*3
        for bg in combinations_with_replacement(range(6),2):
            observed = sum((p[a]*payoff(a,bg) for a in range(6)),F(0))
            assert observed >= 10
    # Enumerate every possible positive support rectangle, not probabilities.
    supports = [set(i for i in range(6) if mask>>i & 1) for mask in range(1,64)]
    optimal_face_rectangles = 0
    for left in supports:
        for right in supports:
            valid = all(i != j and i//3 == j//3 for i in left for j in right)
            if valid:
                optimal_face_rectangles += 1
                assert left.isdisjoint(right)
                assert len(left) == 1 or len(right) == 1
    path = (0,3,4)
    utilities = [payoff(path[i],path[:i]+path[i+1:]) for i in range(3)]
    assert utilities == [F(10),F(12),F(12)]
    assert sum(utilities) == 34
    return dict(customer_count=36,background_classes=counts,security_value='10',
                support_rectangles_on_optimal_face=optimal_face_rectangles,
                existing_spe_path=list(path),path_payoffs=list(map(str,utilities)),
                existing_spe_full_tree_reverified=False)


def main():
    result = dict(identity='Static correlation boundary; not a half-coverage or aggregate-security counterexample',
                  singleton=singleton_regression(),
                  product_gap=quantitative_regression(),
                  existing_36=thirty_six_regression(),
                  proof_status='General claims rely on the accompanying self-contained proofs; finite exact computation is regression only.')
    target = HERE/'correlation_boundary_audit.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
