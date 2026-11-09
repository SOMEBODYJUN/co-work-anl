"""Compare the explicit ordered full-code menu to independent exact game recursion."""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from random import Random

rng = Random(4601)
counts = {"disjoint": 0, "overlap": 0, "suffixes": 0, "ties": 0}
for d in (2, 3):
    half = 1 << (d - 1)
    for iteration in range(20):
        i = rng.randrange(half)
        x = [rng.randrange(1, 6) for _ in range(half)]
        if iteration == 0:
            x = [2] * half
            x[i] = 3
        published_instance = d == 2 and iteration == 2
        if published_instance:
            i, x = 0, [10, 1]
        overlap = iteration % 2 == 1 or iteration == 4
        if iteration == 4:
            i, x = 0, [12, 2] if d == 2 else [12, 1, 1, 1]
        X = [frozenset((0, j, k) for k in range(x[j])) for j in range(half)]
        Y = [frozenset((1, k) for k in range(4) if overlap and rng.randrange(2)) for j in range(half)]
        if iteration == 4:
            shared = frozenset((1, k) for k in range(3 if d == 2 else 11))
            Y = [frozenset(), shared] if d == 2 else [frozenset(), shared, shared, frozenset()]
        N = [X[j] | Y[j] for j in range(half)]
        G = max(map(len, N))
        h = 6 * G + 1
        bank = [frozenset((2, a, (c >> a) & 1) for a in range(d)) for c in range(2 * half)]
        mask = 2 * half - 1
        ell = i ^ mask
        topics = [X[j] for j in range(half)] + N + [bank[j] | N[j] for j in range(half)] + bank[half:]
        prefix = tuple(j for j in range(half) if j != i) + (half + i, 2 * half + ell)
        b = {c: sum(c in topics[a] for a in prefix) for c in frozenset.union(*topics)}

        @lru_cache(None)
        def pay(a, terminal):
            return sum(Fraction(h if c[0] == 2 else 1, b[c] + sum(c in topics[t] for t in terminal)) for c in topics[a])

        @lru_cache(None)
        def solve(history):
            if len(history) == 3:
                return None, frozenset((history,))
            children = [solve(history + (a,))[1] for a in range(len(topics))]
            threshold = max(min(pay(a, z) for z in child) for a, child in enumerate(children))
            return threshold, frozenset(z for a, child in enumerate(children) for z in child if pay(a, z) >= threshold)

        F = {(j, s): sum(Fraction(1, b[c] + 1 + (c in N[j])) for c in N[s])
             for j, s in product(range(half), repeat=2)}
        A = {}
        for j in range(half):
            S = [s for s in range(half) if (s ^ i) & (i ^ j) == 0]
            A[j] = [s for s in S if F[j, s] == max(F[j, t] for t in S)]
        M = max(min(F[s, j] for s in A[j]) for j in range(half))
        menu = {(2 * half + j, 2 * half + s, 2 * half + (ell ^ j ^ s))
                for j in A for s in A[j] if F[s, j] >= M}
        assert solve(()) == (Fraction(d * h, 2) + M, menu), (d, iteration)
        highest_tail = max(pay(z[1], z) for z in menu)
        lowest_first = min(pay(z[0], z) for z in menu)
        assert lowest_first >= (highest_tail + Fraction(d * h, 2)) / 2
        assert lowest_first / highest_tail > (Fraction(38, 39) if d == 2 else Fraction(6 * d + 1, 6 * d + 2))
        if iteration == 4:
            assert M == (4 if d == 2 else 6)
            assert highest_tail == Fraction(d * h, 2) + (6 if d == 2 else Fraction(23, 2))
        if published_instance:
            assert Fraction(d * h, 2) + M == Fraction(193, 3)
        if not overlap:
            designated = (2 * half + i, 2 * half + i, 2 * half + ell)
            comparison = 2 * x[i] - 3 * max(x[j] for j in range(half) if j != i)
            assert (designated in menu) == (comparison >= 0)
            assert comparison <= 0 or menu == {designated}
            counts["ties"] += comparison == 0
        counts["overlap" if overlap else "disjoint"] += 1
        counts["suffixes"] += len(menu)
print(counts)
