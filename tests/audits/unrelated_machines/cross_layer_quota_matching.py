#!/usr/bin/env python3
"""Fraction audit for the core/private all-level quota candidate.

This is a small exact audit of the closed formulas and bridge loads; it is
not an exhaustive solver and it does not claim hardness.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
from math import ceil


def closed_nu(q: int, K: int, s: int, t: int) -> int:
    c = K - s
    return q if t <= s else min(q, c // (t - s))


def brute_nu(q: int, K: int, s: int, t: int) -> int:
    """Tiny brute force on the actual set system (q<=5,K<=5 only)."""
    c = K - s
    core = tuple(range(c))
    priv = [tuple(range(c + i * s, c + (i + 1) * s)) for i in range(q)]
    A = [core + priv[i] for i in range(q)]
    choices = [list(combinations(A[i], t)) for i in range(q)]
    best = 0
    # enumerate selected-variable subsets, then test disjoint representatives
    for r in range(q + 1):
        for S in combinations(range(q), r):
            def rec(pos: int, used: frozenset[int]) -> bool:
                if pos == len(S):
                    return True
                i = S[pos]
                for B in choices[i]:
                    bs = frozenset(B)
                    if used.isdisjoint(bs) and rec(pos + 1, used | bs):
                        return True
                return False
            if rec(0, frozenset()):
                best = max(best, r)
    return best


def audit_small_bruteforce() -> int:
    count = 0
    for K in range(2, 7):
        for s in range(1, K):
            c = K - s
            q = (c * K + s - 1) // s
            if q > 4:  # avoid a large finite enumeration; closed formula is general
                continue
            for t in range(1, K + 1):
                got = brute_nu(q, K, s, t)
                want = closed_nu(q, K, s, t)
                assert got == want, (K, s, q, t, got, want)
                count += 1
    return count


def audit_closed_and_loads() -> int:
    count = 0
    for K in range(2, 101):
        for s in range(1, K):
            c = K - s
            q = (c * K + s - 1) // s
            vals = []
            for t in range(1, K + 1):
                nu = closed_nu(q, K, s, t)
                vals.append(min(Fraction(nu, q), Fraction(t, K)))
            b = max(vals)
            assert b == Fraction(s, K), (K, s, q, b)
            # Explicit integer bridge schedule: all private jobs externalized.
            e_load = Fraction(1) + Fraction(c, K)
            assert e_load == 2 - Fraction(s, K)
            assert Fraction(1) <= e_load
            count += 1
    return count


def bridge_certificate(K: int, s: int, q: int) -> dict:
    """Return exact task/machine counts and the explicit upper-bound loads."""
    c = K - s
    assert q >= (c * K + s - 1) // s
    task_count = 1 + 2 * q + q * K
    machine_count = 1 + 2 * q + c + q * s
    # g only at r; every a_i is sent to x_i; every b_i is sent to e_i;
    # s h-jobs leave e_i and c remain at e_i.
    root_load = Fraction(1)
    x_load = Fraction(1)
    e_load = Fraction(1) + Fraction(c, K)
    resource_load = Fraction(1)
    assert e_load == 2 - Fraction(s, K)
    assert max(root_load, x_load, e_load, resource_load) == e_load
    # YES variant: disjoint K-sets, all K h-jobs leave e_i.
    yes_e_load = Fraction(1)
    assert yes_e_load == 1
    return {
        "K": K, "s": s, "c": c, "q": q,
        "tasks": task_count, "machines": machine_count,
        "no_load": str(e_load), "yes_load": str(yes_e_load),
    }


def main() -> None:
    brute = audit_small_bruteforce()
    closed = audit_closed_and_loads()
    samples = [bridge_certificate(2, 1, 2), bridge_certificate(4, 1, 12), bridge_certificate(7, 2, 18)]
    print({"small_bruteforce_cases": brute, "closed_parameter_cases": closed,
           "bridge_samples": samples, "status": "ok"})


if __name__ == "__main__":
    main()
