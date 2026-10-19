#!/usr/bin/env python3
"""Exact finite audit for dense positive n^2-bounded UM normal form.

This script is an independent finite check, not the universal proof.  It uses
only the Python standard library and never imports repository mathematics.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
import platform
import sys


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def round_dense(P, k, T):
    """Return the fully finite positive integer instance and bad-edge flags."""
    m, n = len(P), len(P[0])
    assert m >= 1 and n >= 8 * k and k >= 2 and T > 0
    H = n * n
    Q, forbidden = [], []
    for row in P:
        qr, fr = [], []
        for p in row:
            bad = p is None or p > T
            q = H if bad else max(1, ceil_fraction(F(4 * k * n) * p / T))
            assert 1 <= q <= H
            if not bad:
                assert q <= 4 * k * n <= H
                assert p <= T * F(q, 4 * k * n)
                assert q <= F(4 * k * n) * p / T + 1
            qr.append(q)
            fr.append(bad)
        Q.append(qr)
        forbidden.append(fr)
    return Q, forbidden


def two_machine_loads(P):
    """Independently enumerate every assignment, using a common exact scale."""
    assert len(P) == 2 and len(P[0]) == len(P[1])
    n = len(P[0])
    D = lcm(*(p.denominator for row in P for p in row if p is not None))
    V = [[None if p is None else int(p * D) for p in row] for row in P]
    result = []
    for bits in range(1 << n):
        loads = [0, 0]
        for j in range(n):
            i = (bits >> j) & 1
            v = V[i][j]
            if v is None:
                result.append(None)
                break
            loads[i] += v
        else:
            result.append(tuple(F(x, D) for x in loads))
    return result, D


def make_fixtures():
    n = 16
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    return [
        (
            "coprime_common_denominators",
            [[F((7 * j + 3) % 19, 11) for j in range(n)],
             [F((11 * j + 1) % 23, 13) for j in range(n)]],
        ),
        (
            "zero_and_infinity_edges",
            [[None if j % 5 == 0 else F((j * j + 3) % 29, 17) for j in range(n)],
             [F(0) if j % 5 == 0 else F((13 * j + 7) % 31, 19) for j in range(n)]],
        ),
        (
            "distinct_prime_denominators",
            [[F(j + 1, primes[j]) for j in range(n)],
             [F(2 * j + 3, primes[-j - 1]) for j in range(n)]],
        ),
        (
            "333_bit_scale_with_zeros_and_infinities",
            [[F(0) if j else F(1, 10 ** 100 + 267) for j in range(n)],
             [F(1, 10 ** 100 + 267) if j % 2 == 0 else None for j in range(n)]],
        ),
    ]


def audit_fixture(name, P):
    n, k = len(P[0]), 2
    alpha, eta = 2 - F(1, k), F(1, 4 * k)
    assert all(any(P[i][j] is not None for i in range(2)) for j in range(n))
    L = max(min(p for p in col if p is not None) for col in zip(*P))
    U = sum(min(p for p in col if p is not None) for col in zip(*P))
    assert L > 0 and L <= U <= n * L

    source_loads, D = two_machine_loads(P)
    opt = min(max(loads) for loads in source_loads if loads is not None)
    assert L <= opt <= U
    T, grid_index = L, 0
    while T < opt:
        T *= 1 + eta
        grid_index += 1
    assert opt <= T <= (1 + eta) * opt
    Q, forbidden = round_dense(P, k, T)

    rounded_loads = []
    for bits in range(1 << n):
        loads = [0, 0]
        for j in range(n):
            i = (bits >> j) & 1
            loads[i] += Q[i][j]
        rounded_loads.append(tuple(loads))
    optq = min(max(loads) for loads in rounded_loads)
    assert optq <= F(4 * k * n) * opt / T + n
    assert optq <= (4 * k + 1) * n

    # Challenge every possible alpha-approximate output, including deliberately
    # nonoptimal ones.  The theorem must hold for every such output.
    qualifying, worst = 0, F(0)
    for bits, qloads in enumerate(rounded_loads):
        cq = max(qloads)
        if cq > alpha * optq:
            continue
        qualifying += 1
        assert cq < n * n
        assert all(not forbidden[(bits >> j) & 1][j] for j in range(n))
        loads = source_loads[bits]
        assert loads is not None
        for i in range(2):
            assert loads[i] <= T * F(qloads[i], 4 * k * n)
            assert loads[i] <= alpha * (opt + T / F(4 * k))
        c = max(loads)
        assert c <= alpha * (opt + T / F(4 * k))
        assert c <= (2 - F(1, 2 * k)) * opt
        worst = max(worst, c / opt)

    return {
        "fixture": name,
        "machines": 2,
        "jobs": n,
        "reciprocal_gap_parameter_k": k,
        "good_grid_index": grid_index,
        "common_scale_bits": D.bit_length(),
        "assignments_exhausted": 1 << n,
        "rounded_optimum": optq,
        "qualifying_assignments": qualifying,
        "qualifying_per_machine_pullback_checks": 2 * qualifying,
        "worst_original_ratio_among_qualifying": str(worst),
    }


def audit_boundaries():
    # The zero test is a complete exact characterization, including no jobs.
    zero_examples = [
        [[], []],
        [[F(0), None], [F(1), F(0)]],
        [[F(0)]],
    ]
    for P in zero_examples:
        m, n = len(P), len(P[0])
        chosen = [next(i for i in range(m) if P[i][j] == 0) for j in range(n)]
        loads = [F(0)] * m
        for j, i in enumerate(chosen):
            loads[i] += P[i][j]
        assert max(loads) == 0
    # A positive-optimum instance can have zero and forbidden edges elsewhere.
    P = [[F(0), F(1, 7)], [None, F(1, 11)]]
    loads, _ = two_machine_loads(P)
    assert min(max(x) for x in loads if x is not None) == F(1, 11)
    assert not all(any(row[j] == 0 for row in P) for j in range(2))
    return len(zero_examples) + 1


def main():
    constant_checks = 0
    for k in range(2, 10001):
        a = F(1, k)
        lhs = (2 - a) * (1 + a / 4 + a * a / 16)
        rhs = 2 - a / 2 - a * a / 8 - a * a * a / 16
        assert lhs == rhs and lhs <= 2 - a / 2
        assert (2 - a) * (4 * k + 1) < 8 * k
        constant_checks += 1
    fixtures = [audit_fixture(name, P) for name, P in make_fixtures()]
    result = {
        "schema": "um-dense-small-integer-equivalence-exact-audit-v1",
        "evidence_level": "finite exact-arithmetic checks; universal proof is separate",
        "software": {
            "python_version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "dependencies": "Python standard library only",
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "imports_repository_code": False,
            "randomness": "none; fixed fixtures and exhaustive assignments",
        },
        "constant_identity_checks": constant_checks,
        "boundary_examples": audit_boundaries(),
        "assignments_exhausted_total": sum(x["assignments_exhausted"] for x in fixtures),
        "qualifying_per_machine_pullback_checks_total": sum(
            x["qualifying_per_machine_pullback_checks"] for x in fixtures
        ),
        "fixtures": fixtures,
        "limitations": [
            "The supplied approximation oracle is represented by all schedules meeting its guarantee on each fixture.",
            "All exhaustive fixtures use m=2,n=16,k=2; the identities also check k=2 through 10000.",
            "The script does not establish a sub-2 algorithm or a no-sub-2 hardness theorem.",
        ],
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
