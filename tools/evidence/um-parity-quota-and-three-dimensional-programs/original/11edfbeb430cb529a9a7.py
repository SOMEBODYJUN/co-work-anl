#!/usr/bin/env python3
"""Exact small checks for the high-dimensional quota obstruction."""
from fractions import Fraction as F


def quota_value(nu, q, K):
    return max(min(F(nu[t], q), F(t, K)) for t in range(1, K + 1))


def pair_disjoint_subsets(A, B, t):
    A, B = set(A), set(B)
    da, db = A - B, B - A
    if len(da) >= t and len(db) >= t:
        return set(list(da)[:t]), set(list(db)[:t])
    # |A|=|B| implies |A\B|=|B\A|.  Fill both sets from the intersection.
    I = list(A & B)
    a = len(da)
    need = t - a
    assert len(da) == len(db) and a < t
    assert 2 * need <= len(I)
    return da | set(I[:need]), db | set(I[need:need + need])


def main():
    q = 5
    for K in range(2, 9):
        # q hyperedges, each with K-1 private resources plus one common c.
        nu = {t: q if t < K else 1 for t in range(1, K + 1)}
        b = quota_value(nu, q, K)
        assert b == F(K - 1, K)
        # The full K-layer sees only one edge, while the partial layer tends to 1.
        assert F(nu[K], q) == F(1, q)

    # Two arbitrary K-sets can both pay a low quota t whenever 2t <= K.
    for K in range(2, 30):
        A = set(range(K))
        for shift in range(K + 1):
            B = set(range(shift, shift + K))
            for t in range(1, K // 2 + 1):
                A1, B1 = pair_disjoint_subsets(A, B, t)
                assert len(A1) == len(B1) == t
                assert A1.isdisjoint(B1)

    # Degree-2 tournament family: full K-bundle matching is one per group,
    # while a regular orientation gives every label almost all K resources.
    for s in (2, 4, 6):
        assert s % 2 == 0
        K = s * s
        labels = list(range(s + 1))
        shared = {(i, j): f"c{i},{j}" for i in labels for j in labels if i < j}
        private = {i: {f"p{i},{u}" for u in range(K - s)} for i in labels}
        bundles = {}
        for i in labels:
            bundles[i] = set(private[i]) | {
                shared[tuple(sorted((i, j)))]
                for j in labels if j != i
            }
            assert len(bundles[i]) == K
        # Orient i -> j when (j-i) mod (s+1) is in 1,...,s/2.
        chosen = {}
        for i in labels:
            out = {shared[tuple(sorted((i, j)))] for j in labels if j != i
                   and (j - i) % (s + 1) in range(1, s // 2 + 1)}
            chosen[i] = private[i] | out
            assert len(chosen[i]) == K - s // 2
        assert all(chosen[i].isdisjoint(chosen[j]) for i in labels for j in labels if i < j)
        assert max(len(x) for x in chosen.values()) == K - s // 2

    print("kdm_high_dimensional_quota: PASS")


if __name__ == "__main__":
    main()
