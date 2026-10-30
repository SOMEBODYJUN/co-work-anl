#!/usr/bin/env python3
"""Exact finite checks for the geometric-alphabet normal-form lemmas.

This is an audit of a standard transformation, not an implementation of the
unknown sub-2 scheduling algorithm used in the existential implication.
Only the standard library is used. Infinity is represented by None.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
import random
from typing import Sequence


def ceil_frac(x: F) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def grid(n: int, h: int | None = None) -> dict:
    h = n.bit_length() if h is None else h
    assert n >= 1 and h >= 1
    b = F(h + 1, h)
    powers = [F(1)]
    while powers[-1] < h * n:
        powers.append(powers[-1] * b)
    rounded = [ceil_frac(x) for x in powers]
    return {
        "n": n,
        "h": h,
        "b": b,
        "powers": powers,
        "rounded": rounded,
        "sentinel": n * n,
    }


def encode_retained(z: F, g: dict) -> tuple[int, int]:
    assert 0 <= z <= g["h"] * g["n"]
    target = max(F(1), z)
    lo, hi = 0, len(g["powers"]) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if g["powers"][mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    r = lo
    assert g["powers"][r] >= target
    assert r == 0 or g["powers"][r - 1] < target
    return g["rounded"][r], r


def encode(p: F | None, T: F, g: dict) -> int:
    assert T > 0
    if p is None or p > T:
        return g["sentinel"]
    assert p >= 0
    q, _ = encode_retained(F(g["h"] * g["n"]) * p / T, g)
    return q


def loads(P: Sequence[Sequence[F | None]], assignment: tuple[int, ...]):
    answer = [F(0) for _ in P]
    for j, i in enumerate(assignment):
        if P[i][j] is None:
            return None
        answer[i] += P[i][j]
    return tuple(answer)


def schedules(P):
    m, n = len(P), len(P[0])
    for a in product(range(m), repeat=n):
        ell = loads(P, a)
        if ell is not None:
            yield max(ell, default=F(0)), a, ell


def all_valid_jobs(P) -> bool:
    return all(any(P[i][j] is not None for i in range(len(P)))
               for j in range(len(P[0])))


def check_grid(g: dict, every_boundary: bool = True):
    n, h, b = g["n"], g["h"], g["b"]
    R = len(g["powers"]) - 1
    assert b ** h >= 2
    # ceil(log2(h*n)) is exactly bit_length(h*n-1).
    assert R <= h * (h * n - 1).bit_length()
    assert g["powers"][R] >= h * n
    assert R == 0 or g["powers"][R - 1] < h * n
    if n >= 16 and h == n.bit_length():
        assert n >= 2 ** (h - 1) > 2 * (h + 2)
        assert max(g["rounded"]) < n * n
        assert len(set(g["rounded"]) | {n*n}) <= (
            h * (h * n - 1).bit_length() + 2)

    probes = {F(0), F(1), F(h*n), F(1, 2**127 + 101)}
    if every_boundary:
        for a, c in zip(g["powers"], g["powers"][1:]):
            if a <= h*n:
                probes.add(a)
            if c <= h*n:
                probes.add(c)
            if (a+c)/2 <= h*n:
                probes.add((a+c)/2)
        for p in g["powers"]:
            if 1 <= p <= h*n:
                q, r = encode_retained(p, g)
                assert g["powers"][r] == p
                assert q == ceil_frac(p)
    else:
        for i in [0, R//4, R//2, 3*R//4, R]:
            probes.add(min(F(h*n), g["powers"][i]))
    for z in probes:
        q, _ = encode_retained(z, g)
        assert z <= q <= b*z + 1

    T = F(17, 101)
    assert encode(F(0), T, g) == 1
    assert encode(T, T, g) == g["rounded"][-1]
    assert encode(T + F(1, 2**257 + 193), T, g) == n*n
    assert encode(None, T, g) == n*n
    assert encode(T / (h*n), T, g) == 1
    assert encode(T / (h*n*(2**131+91)), T, g) == 1
    return {
        "n": str(n), "h": h, "R": R,
        "distinct": len(set(g["rounded"]) | {n*n}),
        "max_retained": str(max(g["rounded"])),
        "max_power_bits": max(g["powers"][-1].numerator.bit_length(),
                              g["powers"][-1].denominator.bit_length()),
        "probes": len(probes),
    }


def check_matrix(P, g: dict, counts: dict):
    """Independent enumeration checks the mathematical encoding inequalities."""
    assert all_valid_jobs(P)
    n, h, b = g["n"], g["h"], g["b"]
    originals = list(schedules(P))
    opt, opt_a, _ = min(originals)
    counts["matrices"] += 1
    counts["original_assignments"] += len(originals)
    zero_iff = all(any(P[i][j] == 0 for i in range(len(P)))
                   for j in range(n))
    assert (opt == 0) == zero_iff
    if opt == 0:
        counts["zero_opt_matrices"] += 1

    # Both exact equality and a slightly excessive threshold occur. An
    # additional fixed rational threshold exercises discarded original edges.
    Ts = {F(1, 3), F(7, 11)}
    if opt > 0:
        Ts |= {opt, b*opt}
    for T in sorted(Ts):
        Q = [[F(encode(p, T, g)) for p in row] for row in P]
        transformed = list(schedules(Q))
        qopt, _, _ = min(transformed)
        counts["threshold_instances"] += 1
        counts["transformed_assignments"] += len(transformed)
        for qC, a, qell in transformed:
            retained = all(P[i][j] is not None and P[i][j] <= T
                           for j, i in enumerate(a))
            if not retained:
                assert qC >= n*n
                counts["sentinel_assignments"] += 1
                continue
            pell = loads(P, a)
            assert pell is not None
            for pi, qi in zip(pell, qell):
                assert pi <= T*qi/(h*n)
                assert qi <= b*(h*n/T)*pi + n
            counts["retained_assignments"] += 1
        if T >= opt:
            witness = loads(Q, opt_a)
            assert witness is not None
            assert max(witness) <= b*(h*n/T)*opt + n
            assert qopt <= b*(h*n/T)*opt + n <= (h+2)*n
            counts["optimal_witness_checks"] += 1

            # Audit any approximate output, without pretending an algorithm
            # with this guarantee is available: enumerate all qualifying ones.
            alpha = F(3, 2)
            if alpha*qopt < n*n:
                counts["strict_sentinel_cases"] += 1
                for qC, a, _ in transformed:
                    if qC <= alpha*qopt:
                        retained = all(P[i][j] is not None and P[i][j] <= T
                                       for j, i in enumerate(a))
                        assert retained
                        pC = max(loads(P, a))
                        assert pC <= alpha*(b*opt + T/h)
                        counts["all_qualifying_output_checks"] += 1


def check_actual_large_branch():
    """Enumerate every possible load pair, with actual h>=8k.

    The 32762 labeled zero jobs all have original times (0,0), and rounded
    times (1,1). Their complete effect is represented exactly by the integer
    count t sent to machine 0; every t is attainable. Thus 64*(32762+1)
    pairs cover every complete transformed schedule's original/rounded loads.
    No unknown scheduling backend is invoked.
    """
    n, k = 32768, 2
    g = grid(n)
    h, b, alpha = g["h"], g["b"], F(2)-F(1,k)
    assert h == 16 == 8*k
    P = [
        (F(3), F(1,2), F(1,3), F(1,2**89+9), None, F(3,2)),
        (F(1,2), F(1), F(2,3), F(1,7), F(1,4), None),
    ]
    r = len(P[0])
    zeros = n-r
    original_schedules = list(schedules(P))
    opt, opt_a, _ = min(original_schedules)
    assert opt == F(11,6)+F(1,2**89+9)
    L = max(min(p for p in col if p is not None) for col in zip(*P))
    U = sum(min(p for p in col if p is not None) for col in zip(*P))
    T = L
    H = 0
    while T < opt:
        T *= b
        H += 1
    assert T <= U and opt <= T <= b*opt
    assert H == 4
    Q = [[encode(p,T,g) for p in row] for row in P]
    assert encode(F(0),T,g) == 1
    assert encode(None,T,g) == n*n
    assert P[0][0] > T and Q[0][0] == n*n
    records = []
    qopt = None
    qopt_certificate = None
    for a in product(range(2), repeat=r):
        qbase = [sum(Q[i][j] for j in range(r) if a[j] == i)
                 for i in range(2)]
        # The exact integer minimizer of max(A+t,B+zeros-t) is obtained by
        # clamping floor/ceil of their intersection to [0,zeros].
        intersection_twice = qbase[1]+zeros-qbase[0]
        trial = {0, zeros}
        for t in [intersection_twice//2, intersection_twice//2+1]:
            trial.add(max(0,min(zeros,t)))
        bestC, best_t = min((max(qbase[0]+t,qbase[1]+zeros-t),t)
                            for t in trial)
        if qopt is None or bestC < qopt:
            qopt, qopt_certificate = bestC, (a,best_t)
        records.append((a, qbase))
    assert qopt is not None
    assert F(qopt) <= b*(h*n/T)*opt+n <= (h+2)*n
    assert alpha*qopt < n*n
    max_qualifying_qC = (alpha*qopt).numerator//(alpha*qopt).denominator
    total_pairs = qualifying_pairs = 0
    qualifying_flexible_patterns = 0
    largest_original = F(0)
    smallest_zero_count = zeros
    largest_zero_count = 0
    for a, qbase in records:
        pell = loads(P,a)
        retained = all(P[i][j] is not None and P[i][j] <= T
                       for j,i in enumerate(a))
        # This interval is independently checked against every zero-count
        # load pair below; its endpoints use integer inequalities only.
        lower = max(0, qbase[1]+zeros-max_qualifying_qC)
        upper = min(zeros, max_qualifying_qC-qbase[0])
        count_for_pattern = 0
        for t in range(zeros+1):
            qC = max(qbase[0]+t, qbase[1]+zeros-t)
            assert qC >= qopt
            total_pairs += 1
            qualifies = qC <= max_qualifying_qC
            assert qualifies == (lower <= t <= upper)
            if qualifies:
                qualifying_pairs += 1
                count_for_pattern += 1
        if count_for_pattern:
            assert count_for_pattern == upper-lower+1
            assert retained and pell is not None
            pC = max(pell)
            assert pC <= alpha*(b*opt+T/h) <= alpha*b*b*opt
            assert pC <= (F(2)-F(1,2*k))*opt
            # Machinewise back-translation at the endpoint that minimizes
            # each machine's rounded load gives all intermediate t as well.
            assert pell[0] <= T*(qbase[0]+lower)/(h*n)
            assert pell[1] <= T*(qbase[1]+zeros-upper)/(h*n)
            largest_original = max(largest_original,pC)
            qualifying_flexible_patterns += 1
            smallest_zero_count = min(smallest_zero_count,lower)
            largest_zero_count = max(largest_zero_count,upper)
    assert total_pairs == 2**r*(zeros+1)
    assert qualifying_pairs > 0
    a,t = qopt_certificate
    qbase = [sum(Q[i][j] for j in range(r) if a[j] == i)
             for i in range(2)]
    assert max(qbase[0]+t,qbase[1]+zeros-t) == qopt
    return {
        "n": n, "m": 2, "h": h, "k": k,
        "nonzero_jobs": r, "zero_jobs": zeros,
        "original_opt": str(opt), "L": str(L), "U": str(U),
        "first_good_T": str(T), "grid_steps_to_good_T": H,
        "rounded_flexible_rows": Q,
        "rounded_opt": qopt,
        "rounded_opt_certificate": {
            "flexible_assignment": list(qopt_certificate[0]),
            "zero_count_on_machine0": qopt_certificate[1],
        },
        "total_exact_load_pairs": total_pairs,
        "qualifying_alpha_load_pairs": qualifying_pairs,
        "qualifying_flexible_patterns": qualifying_flexible_patterns,
        "qualifying_zero_count_range": [smallest_zero_count,largest_zero_count],
        "largest_qualifying_original_load": str(largest_original),
        "alpha": str(alpha),
        "transfer_ratio_bound": str(alpha*b*b),
        "claimed_ratio": str(F(2)-F(1,2*k)),
        "sentinel": n*n,
        "scope": "Every transformed schedule is covered by one flexible pattern and zero-job count; no sub-2 backend assumed or run.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4096)
    parser.add_argument("--large-bits", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20261019)
    args = parser.parse_args()
    assert args.max_n >= 16
    grid_records = []
    probe_total = 0
    for n in range(16, args.max_n + 1):
        row = check_grid(grid(n))
        probe_total += row["probes"]
        if n in {16,17,31,32,100,1000,args.max_n}:
            grid_records.append(row)

    large_records = []
    for n in sorted({10**6, 2**30, 2**60, 2**args.large_bits}):
        large_records.append(check_grid(grid(n), every_boundary=False))

    counts = {key: 0 for key in [
        "matrices", "zero_opt_matrices", "original_assignments",
        "threshold_instances", "transformed_assignments",
        "sentinel_assignments", "retained_assignments",
        "optimal_witness_checks", "strict_sentinel_cases",
        "all_qualifying_output_checks",
    ]}
    # Exhaustive palettes on actual labeled matrices. Small h is intentional:
    # this tests the encoding lemmas, not a claimed approximation transfer.
    palettes = [([F(0), F(1,2), F(1), None], [2,3]),
                ([F(0), F(1,3), F(2,7), F(5,11), None], [2])]
    for palette, sizes in palettes:
        for n in sizes:
            for h in [1,2]:
                g = grid(n, h)
                if max(g["rounded"]) >= n*n:
                    continue
                for entries in product(palette, repeat=2*n):
                    P = [entries[:n], entries[n:]]
                    if all_valid_jobs(P):
                        check_matrix(P, g, counts)

    rng = random.Random(args.seed)
    palette = [F(0), F(1,3), F(2,7), F(5,11), F(2),
               F(1,2**89+9), None]
    for n in [4,5]:
        for h in [1,2]:
            g = grid(n, h)
            assert max(g["rounded"]) < n*n
            accepted = 0
            while accepted < 80:
                P = [tuple(rng.choice(palette) for _ in range(n))
                     for _ in range(2)]
                if all_valid_jobs(P):
                    check_matrix(P, g, counts)
                    accepted += 1

    ratios = []
    for k in range(2,1001):
        alpha, b = F(2)-F(1,k), F(1)+F(1,8*k)
        exact = F(2)-F(1,2*k)-F(7,32*k*k)-F(1,64*k*k*k)
        assert alpha*b*b == exact < F(2)-F(1,2*k)
        if k in [2,3,10,100,1000]:
            ratios.append({"k": k, "ratio_bound": str(exact),
                           "claimed_bound": str(F(2)-F(1,2*k))})
    print(json.dumps({
        "status": "passed",
        "arithmetic": "fractions.Fraction; no float comparisons",
        "seed": args.seed,
        "grid_interval": [16,args.max_n],
        "grid_count": args.max_n-15,
        "grid_probe_count": probe_total,
        "grid_samples": grid_records,
        "large_grid_only": large_records,
        "small_h_transformation_checks": counts,
        "ratio_identity_k_interval": [2,1000],
        "ratio_samples": ratios,
        "actual_large_branch_fixture": check_actual_large_branch(),
        "scope": "Finite checks of encoding lemmas only; no unknown sub-2 backend; no hardness proof.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
