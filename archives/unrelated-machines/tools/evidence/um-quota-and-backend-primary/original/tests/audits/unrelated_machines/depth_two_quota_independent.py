#!/usr/bin/env python3
"""Independent exact audit of the depth-two half-quota argument.

No repository implementation is imported. In the exhaustive star audit, the
oracle enumerates all disjoint full stars, while an adversarial recursion checks
ALL choices of equal-minimum greedy centers and ALL permitted leaf subsets.
The bottleneck audit has a separate assignment-enumeration oracle.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import platform
import random


def submasks_of_size(mask, size):
    """Explicit resource enumeration; size is compared with popcount first."""
    if size > mask.bit_count():
        return ()
    bits = [i for i in range(mask.bit_length()) if mask >> i & 1]
    return tuple(sum(1 << i for i in c) for c in combinations(bits, size))


def full_packing_optimum(neigh, demands):
    """Independent DP: skip a center or enumerate its full star."""
    @lru_cache(None)
    def visit(i, used):
        if i == len(neigh):
            return 0
        ans = visit(i + 1, used)
        for leaves in submasks_of_size(neigh[i] & ~used, demands[i]):
            ans = max(ans, 1 + visit(i + 1, used | leaves))
        return ans
    return visit(0, 0)


def adversarial_half_greedy_count(neigh, demands):
    """Exact minimum over ALL greedy tie-breaking / resource choices."""
    half = tuple((d + 1) // 2 for d in demands)
    @lru_cache(None)
    def visit(left, used):
        eligible = [i for i in range(len(neigh))
                    if left >> i & 1
                    and (neigh[i] & ~used).bit_count() >= half[i]]
        if not eligible:
            return 0
        q = min(half[i] for i in eligible)
        answers = []
        for i in eligible:
            if half[i] != q:
                continue
            for leaves in submasks_of_size(neigh[i] & ~used, q):
                answers.append(1 + visit(left & ~(1 << i), used | leaves))
        return min(answers)
    return visit((1 << len(neigh)) - 1, 0)


def assignment_optimum(neigh, child_k, root_k, w):
    """Enumerate each leaf destination, including unused, independently."""
    best = Fraction(0)
    for dest in product(range(-1, len(neigh)), repeat=w):
        count = [0] * len(neigh)
        valid = True
        for leaf, center in enumerate(dest):
            if center < 0:
                continue
            if not (neigh[center] >> leaf & 1):
                valid = False
                break
            count[center] += 1
        if not valid:
            continue
        selected = [i for i, d in enumerate(count) if d]
        if not selected:
            continue
        value = min([Fraction(1), Fraction(len(selected), root_k)] +
                    [Fraction(count[i], child_k[i]) for i in selected])
        best = max(best, value)
    return best


def independent_threshold_greedy(neigh, child_k, tau):
    """Deterministic implementation: reverse center/leaf ordering."""
    d = tuple((tau.numerator * k + tau.denominator - 1) //
              tau.denominator for k in child_k)
    half = tuple((x + 1) // 2 for x in d)
    left = set(range(len(neigh)))
    used = 0
    chosen = {}
    while True:
        eligible = [i for i in left
                    if (neigh[i] & ~used).bit_count() >= half[i]]
        if not eligible:
            break
        i = min(eligible, key=lambda i: (half[i], -i))
        bits = [j for j in range(neigh[i].bit_length() - 1, -1, -1)
                if ((neigh[i] & ~used) >> j) & 1]
        leaves = sum(1 << j for j in bits[:half[i]])
        assert leaves.bit_count() == half[i]
        assert not leaves & used
        assert not leaves & ~neigh[i]
        used |= leaves
        left.remove(i)
        chosen[i] = leaves
    return chosen


def independent_bottleneck(neigh, child_k, root_k):
    gamma = {Fraction(1)}
    for k, degree in [(root_k, len(neigh))] + list(zip(child_k, (x.bit_count() for x in neigh))):
        gamma.update(Fraction(h, k) for h in range(1, min(k, degree) + 1))
    best = Fraction(0)
    for tau in gamma:
        chosen = independent_threshold_greedy(neigh, child_k, tau)
        value = min([Fraction(1), Fraction(len(chosen), root_k)] +
                    [Fraction(leaves.bit_count(), child_k[i])
                     for i, leaves in chosen.items()])
        best = max(best, value)
    return best


def main():
    star_cases = 0
    equalities = 0
    for u in range(4):
        for w in range(5):
            for neigh in product(range(1 << w), repeat=u):
                for demands in product(range(1, 4), repeat=u):
                    optimum = full_packing_optimum(neigh, demands)
                    worst_g = adversarial_half_greedy_count(neigh, demands)
                    assert 2 * worst_g >= optimum, (neigh, demands, optimum, worst_g)
                    star_cases += 1
                    equalities += bool(optimum and 2 * worst_g == optimum)
    rng = random.Random(940327)
    bottleneck_cases = 0
    large = 2**100 + 267
    edge_cases = [
        ((), (), 1, 0),
        ((0,), (large,), large, 0),
        ((1,), (large,), large, 1),
        ((3, 2), (1, 1), 2, 2),
        ((1, 1), (1, 1), 2, 1),
        ((1, 1), (large, 1), large, 1),
    ]
    random_cases = []
    for _ in range(4000):
        u, w = rng.randrange(5), rng.randrange(6)
        neigh = tuple(rng.randrange(1 << w) for _ in range(u))
        ks = (1, 2, 3, 5, 7, large, large + 2)
        child = tuple(rng.choice(ks) for _ in range(u))
        root = rng.choice(ks)
        random_cases.append((neigh, child, root, w))
    for neigh, child, root, w in edge_cases + random_cases:
        exact = assignment_optimum(neigh, child, root, w)
        got = independent_bottleneck(neigh, child, root)
        assert 0 <= got <= exact <= 1, (neigh, child, root, exact, got)
        assert 2 * got >= exact, (neigh, child, root, exact, got)
        assert 2 * (2 - got) <= 3 * (2 - exact)
        bottleneck_cases += 1
    # The nested-ceiling identity for a dense finite rational grid, plus huge k.
    ceiling_cases = 0
    for numerator in range(1, 30):
        for denominator in range(1, 30):
            for k in (1, 2, 3, 4, 5, 7, 100, large):
                d = (numerator * k + denominator - 1) // denominator
                nested = (d + 1) // 2
                direct = (numerator * k + 2 * denominator - 1) // (2 * denominator)
                assert nested == direct
                assert d - nested + 1 >= nested
                ceiling_cases += 1
    result = {
        "status": "passed",
        "semantics": "finite verification is not a proof",
        "star_domain": {"U": "0..3", "W": "0..4", "d_u": "1..3", "graphs": "all bipartite graphs", "tie_breaks": "all minimum-quota center choices and all feasible leaf subsets"},
        "star_cases": star_cases,
        "nonzero_count_equalities": equalities,
        "bottleneck_cases": bottleneck_cases,
        "bottleneck_domain": "6 explicit boundary cases plus 4000 seeded instances, U<=4,W<=5; demands in {1,2,3,5,7,2**100+267,2**100+269}",
        "seed": 940327,
        "ceil_identity_cases": ceiling_cases,
        "arithmetic": "exact integers and fractions.Fraction; no numerical tolerance",
        "python": platform.python_version(),
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
