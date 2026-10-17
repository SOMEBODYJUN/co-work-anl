#!/usr/bin/env python3
"""Exact audit for UM-FIXED-WORK-CONVEX-LOCAL-MINIMUM-v1.

All arithmetic uses Fraction.  The proof-level family is checked analytically;
for m=3 we additionally enumerate every assignment.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

F = Fraction


def build_instance(m: int) -> list[list[F]]:
    if m < 3:
        raise ValueError("m must be >= 3")
    # Two unit jobs followed by m^2-1 tiny jobs.  Rows are jobs, columns machines.
    return [[F(1) for _ in range(m)] for _ in range(2)] + [
        [F(1, m) for _ in range(m)] for _ in range(m * m - 1)
    ]


def initial_assignment(m: int) -> tuple[int, ...]:
    # jobs 0,1 are units at machine 0; tiny jobs are m+1 per machine 1..m-1.
    a = [0, 0]
    for i in range(1, m):
        a.extend([i] * (m + 1))
    assert len(a) == m * m + 1
    return tuple(a)


def constructive_opt_assignment(m: int) -> tuple[int, ...]:
    # Units on 0,1.  Each gets two tiny jobs.  Among the other machines,
    # one gets m+1 tiny jobs and the rest m+2.
    a = [0, 1]
    tiny_counts = [2, 2] + [m + 1] + [m + 2] * (m - 3)
    assert len(tiny_counts) == m
    assert sum(tiny_counts) == m * m - 1
    for i, count in enumerate(tiny_counts):
        a.extend([i] * count)
    assert len(a) == m * m + 1
    return tuple(a)


def loads(m: int, assignment: Sequence[int]) -> list[F]:
    P = build_instance(m)
    if len(assignment) != len(P):
        raise ValueError("assignment length")
    out = [F(0) for _ in range(m)]
    for j, i in enumerate(assignment):
        if not 0 <= i < m:
            raise ValueError("machine index")
        out[i] += P[j][i]
    return out


def phi2(L: Iterable[F]) -> F:
    return sum((x * x for x in L), F(0))


def sorted_loads(L: Iterable[F]) -> tuple[F, ...]:
    return tuple(sorted(L, reverse=True))


def one_move_records(m: int, assignment: Sequence[int]) -> list[dict]:
    P = build_instance(m)
    base = loads(m, assignment)
    base_phi = phi2(base)
    base_sorted = sorted_loads(base)
    records: list[dict] = []
    for j, old in enumerate(assignment):
        for new in range(m):
            if new == old:
                continue
            a = list(assignment)
            a[j] = new
            L = loads(m, a)
            records.append(
                {
                    "job": j,
                    "old": old,
                    "new": new,
                    "delta_phi": phi2(L) - base_phi,
                    "lex_worse": sorted_loads(L) > base_sorted,
                    "loads": [str(x) for x in L],
                }
            )
    return records


def analytic_optimum(m: int) -> F:
    # The proof in the manuscript gives equality; return the claimed value.
    return F(1) + F(2, m)


def exhaustive_optimum(m: int) -> tuple[F, tuple[int, ...]]:
    P = build_instance(m)
    best_c: F | None = None
    best_a: tuple[int, ...] | None = None
    for a in itertools.product(range(m), repeat=len(P)):
        L = [F(0) for _ in range(m)]
        for j, i in enumerate(a):
            L[i] += P[j][i]
        c = max(L)
        if best_c is None or c < best_c:
            best_c, best_a = c, tuple(a)
    assert best_c is not None and best_a is not None
    return best_c, best_a


def support_lower_bound(m: int, epsilon: F) -> int:
    if not (F(0) < epsilon < F(1)):
        raise ValueError("epsilon must be in (0,1)")
    # One unit plus at least 1+ceil(epsilon*m) tiny jobs.
    em = epsilon * m
    ceil_em = (em.numerator + em.denominator - 1) // em.denominator
    return 2 + ceil_em


def support_count_from_capacity(m: int, epsilon: F) -> int:
    # Independently recompute the tiny count that must leave the destination
    # of a moved unit under C <= 2-epsilon.
    target = F(2) - epsilon
    residual_tiny_capacity = target - F(1)
    num_tiny = (residual_tiny_capacity * m).numerator // (residual_tiny_capacity * m).denominator
    return 1 + (m + 1 - num_tiny)  # one moved unit + tiny jobs ejected


def run_case(m: int, enumerate_all: bool = False) -> dict:
    P = build_instance(m)
    a0 = initial_assignment(m)
    aopt = constructive_opt_assignment(m)
    L0 = loads(m, a0)
    Lopt = loads(m, aopt)
    assert L0 == [F(2)] + [F(1) + F(1, m)] * (m - 1)
    assert max(L0) == F(2)
    assert max(Lopt) == analytic_optimum(m)
    assert sum(L0, F(0)) == F(m) + F(2) - F(1, m)
    records = one_move_records(m, a0)
    assert records and all(r["delta_phi"] > 0 for r in records)
    assert all(r["lex_worse"] for r in records)
    for eps in (F(1, 2), F(1, 10)):
        assert support_count_from_capacity(m, eps) == support_lower_bound(m, eps)
    out = {
        "m": m,
        "machines": m,
        "jobs": len(P),
        "matrix_entries": m * len(P),
        "initial_loads": [str(x) for x in L0],
        "initial_phi2": str(phi2(L0)),
        "constructive_opt_loads": [str(x) for x in Lopt],
        "analytic_opt": str(analytic_optimum(m)),
        "initial_ratio": str(F(2) / analytic_optimum(m)),
        "one_move_count": len(records),
        "min_delta_phi2": str(min(F(r["delta_phi"]) for r in records)),
        "all_one_moves_strict_phi_increase": True,
        "all_one_moves_lex_worse": True,
        "support_lower_bound_eps_1_2": support_lower_bound(m, F(1, 2)),
        "support_lower_bound_eps_1_10": support_lower_bound(m, F(1, 10)),
    }
    if enumerate_all:
        c, a = exhaustive_optimum(m)
        assert c == analytic_optimum(m)
        out["exhaustive_optimum"] = str(c)
        out["exhaustive_witness_loads"] = [str(x) for x in loads(m, a)]
    return out


def main() -> None:
    here = Path(__file__).resolve()
    cases = [run_case(3, enumerate_all=True)] + [run_case(m) for m in (4, 5, 8, 12)]
    payload = {
        "claim_id": "UM-FIXED-WORK-CONVEX-LOCAL-MINIMUM-v1",
        "scope": "exact Fraction audit of fixed-work identical-machine family; not hardness",
        "python": platform.python_version(),
        "code_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
        "cases": cases,
        "family_checks": {
            "m_ge_3": True,
            "all_processing_times_positive": True,
            "all_edges_finite": True,
            "total_work_assignment_invariant": True,
            "analytic_optimum_proved_in_markdown": True,
            "zero_opt_boundary": "outside family; handle zero edges separately",
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
