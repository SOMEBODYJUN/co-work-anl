"""Exact finite audit for UM-SINGLE-LAYER-QUOTA-VALUE-v1.
Independent brute force: tree choices versus disjoint t-subsets.
"""
from fractions import Fraction as F
from itertools import combinations, product
import random

def nu(sets, t):
    best = 0
    for mask in range(1 << len(sets)):
        I = [i for i in range(len(sets)) if mask >> i & 1]
        if len(I) <= best:
            continue
        opts = [list(combinations(sorted(sets[i]), t)) for i in I]
        if any(not o for o in opts):
            continue
        for choice in product(*opts):
            flat = [z for B in choice for z in B]
            if len(set(flat)) == len(flat):
                best = len(I)
                break
    return best

def formula(sets, q, K):
    return max((min(F(1), F(nu(sets, t), q), F(t, K))
                for t in range(0, K + 1)), default=F(0))

def treescore(sets, q, K):
    best = F(0)
    for s in range(1, len(sets) + 1):
        for I in combinations(range(len(sets)), s):
            choices = []
            for i in I:
                choices.append([B for t in range(1, min(K, len(sets[i])) + 1)
                                for B in combinations(sorted(sets[i]), t)])
            for choice in product(*choices):
                flat = [z for B in choice for z in B]
                if len(set(flat)) != len(flat):
                    continue
                b = min(F(1), F(s, q), *(F(len(B), K) for B in choice))
                best = max(best, b)
    return best

def run():
    universe = (0, 1, 2)
    nonempty = [set(z for z, bit in zip(universe, mask) if bit)
                for mask in product((0, 1), repeat=3) if any(mask)]
    cases = 0
    for q in range(1, 4):
        for K in range(1, 5):
            for N in range(1, 4):
                for idx in product(range(len(nonempty)), repeat=N):
                    sets = [nonempty[i] for i in idx]
                    assert formula(sets, q, K) == treescore(sets, q, K), (sets, q, K)
                    cases += 1
    rng = random.Random(20261017)
    for _ in range(100):
        N = rng.randint(1, 4)
        sets = []
        for _ in range(N):
            s = {z for z in range(4) if rng.randrange(2)}
            sets.append(s or {rng.randrange(4)})
        q, K = rng.randint(1, 4), rng.randint(1, 4)
        assert formula(sets, q, K) == treescore(sets, q, K), (sets, q, K)
    print({"exhaustive_cases": cases, "random_cases": 100, "status": "passed"})

if __name__ == "__main__":
    run()
