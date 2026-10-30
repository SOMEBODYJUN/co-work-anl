#!/usr/bin/env python3
"""Exact finite audit for UM-FINITE-PALETTE-GCD-BARRIER-v1.

This audit does not solve the LST LP and is not a proof of the theorem.  It
checks the arithmetic part independently: common rational gcd computation,
the fact that every integral load lies on that grid, and the two-case final
inequality for every grid target T <= OPT and every possible support maximum
b <= min(B,T) on small exhaustive instances.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import itertools
import json
from math import gcd, lcm
from pathlib import Path
import platform
import random
import sys


def grid(P):
    finite = [p for row in P for p in row if p is not None]
    positive = [p for p in finite if p > 0]
    assert positive
    D = lcm(*(p.denominator for p in finite))
    ints = [int(p * D) for p in positive]
    G = 0
    for q in ints:
        G = gcd(G, q)
    return F(G, D), max(finite), D


def loads(P, assignment):
    m, n = len(P), len(P[0])
    out = [F(0) for _ in range(m)]
    for j, i in enumerate(assignment):
        p = P[i][j]
        if p is None:
            return None
        out[i] += p
    return tuple(out)


def exact_opt(P):
    m, n = len(P), len(P[0])
    best = None
    count = 0
    for a in itertools.product(range(m), repeat=n):
        ls = loads(P, a)
        if ls is None:
            continue
        count += 1
        value = max(ls)
        if best is None or value < best:
            best = value
    assert best is not None
    return best, count


def check_one(name, P):
    m, n = len(P), len(P[0])
    assert m >= 1 and n >= 1
    assert all(any(P[i][j] is not None for i in range(m)) for j in range(n))
    positive = [p for row in P for p in row if p is not None and p > 0]
    if not positive:
        return {"name": name, "opt": "0", "zero_only": True}

    g, B, D = grid(P)
    opt, feasible = exact_opt(P)
    rho = F(2) - g / B
    # A positive optimum is a nonzero grid point.
    assert opt > 0 and (opt / g).denominator == 1

    all_loads = 0
    for a in itertools.product(range(m), repeat=n):
        ls = loads(P, a)
        if ls is None:
            continue
        all_loads += 1
        for load in ls:
            assert (load / g).denominator == 1

    # Recheck the exact two-case inequality for every possible grid T <= OPT
    # and every support maximum b allowed by (4).  This is the arithmetic
    # conclusion of the proof, independent of any floating-point calculation.
    # The cap T + min(B,T) - g is monotone in T and piecewise linear with
    # its only breakpoint at B.  Checking g, min(B,OPT), and OPT therefore
    # covers the exact two-case inequality without enumerating a potentially
    # enormous rational grid (the denominator lcm can have many bits).
    targets = sorted({g, min(B, opt), opt})
    checks = 0
    for T in targets:
        candidates = [F(0), min(B, T)]
        for b in candidates:
            if b > min(B, T):
                continue
            cap = T + b - g
            assert cap <= rho * opt
            checks += 1

    return {
        "name": name,
        "machines": m,
        "jobs": n,
        "finite_edges": len([p for row in P for p in row if p is not None]),
        "feasible_assignments": feasible,
        "assignments_with_all_edges_finite": all_loads,
        "common_denominator_bits": D.bit_length(),
        "g": str(g),
        "B": str(B),
        "g_over_B": str(g / B),
        "opt": str(opt),
        "rho": str(rho),
        "grid_targets_checked": len(targets),
        "arithmetic_inequalities_checked": checks,
        "zero_only": False,
    }


def fixtures():
    rng = random.Random(20261019)
    out = []
    out.append(("zero_edges_and_infinity", [
        [F(0), F(3, 2), None, F(5, 2), F(1, 2)],
        [F(4), F(0), F(1), None, F(3, 2)],
        [None, F(2), F(3, 2), F(1), F(0)],
    ]))
    out.append(("fixed_palette", [
        [F(1, 2), F(3, 2), None, F(5, 2), F(1, 2), F(3, 2)],
        [F(5, 2), F(1, 2), F(3, 2), F(1, 2), None, F(5, 2)],
        [F(3, 2), None, F(5, 2), F(3, 2), F(1, 2), F(1, 2)],
    ]))
    out.append(("coprime_rationals", [
        [F(7, 11), F(5, 13), None, F(19, 17), F(2, 7), F(11, 23)],
        [F(3, 5), F(17, 19), F(1, 29), None, F(13, 31), F(7, 37)],
    ]))
    huge = 10**100 + 267
    out.append(("large_denominator", [
        [F(1, huge), F(3, huge), None, F(2, huge), F(7, huge)],
        [F(2, huge), F(1, huge), F(5, huge), None, F(3, huge)],
    ]))
    # A few deterministic random matrices with zero/infinity edges.
    for r in range(6):
        m, n = 3, 7
        P = []
        for i in range(m):
            row = []
            for j in range(n):
                if rng.random() < 0.16:
                    row.append(None)
                else:
                    row.append(F(rng.randint(0, 17), rng.randint(1, 9)))
            P.append(row)
        for j in range(n):
            if all(P[i][j] is None for i in range(m)):
                P[rng.randrange(m)][j] = F(rng.randint(1, 9), rng.randint(1, 7))
        out.append((f"random_{r}", P))
    return out


def main():
    records = [check_one(name, P) for name, P in fixtures()]
    assert len(records) == 10
    assert any(r["name"] == "fixed_palette" and r["g_over_B"] == "1/5"
               for r in records)
    payload = {
        "audit": "finite_palette_gcd_barrier",
        "claim": "UM-FINITE-PALETTE-GCD-BARRIER-v1",
        "status": "finite_exact_arithmetic_audit_not_a_universal_proof",
        "python": sys.version,
        "platform": platform.platform(),
        "seed": 20261019,
        "instances": records,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
