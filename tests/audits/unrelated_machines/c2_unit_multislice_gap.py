#!/usr/bin/env python3
"""Exact finite audit for UM-C2-LOAD-UNIT-GAP-v1; no third-party modules.

This checks finite inputs/formulas, not the general PSD proof.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import argparse
import hashlib
import json
import time


def falling(x, k):
    value = Q(1)
    for h in range(k):
        value *= x - h
    return value


class UnitGap:
    def __init__(self, m):
        assert m >= 3
        self.m, self.n, self.t = m, m + 1, Q(m + 1, m)
        self.edges = tuple((j, i) for j in range(self.n) for i in range(m))

    def moment(self, literal_set):
        jobs = {}
        for j, i in literal_set:
            if j in jobs and jobs[j] != i:
                return Q(0)
            jobs[j] = i
        assert len(jobs) <= 4
        counts = [0] * self.m
        for i in jobs.values():
            counts[i] += 1
        value = Q(1)
        for a in counts:
            value *= falling(self.t, a)
        return value / falling(Q(self.n), len(jobs))

    def monomials(self, max_degree):
        result = [frozenset()]
        for k in range(1, max_degree + 1):
            for jobs in combinations(range(self.n), k):
                for colors in product(range(self.m), repeat=k):
                    result.append(frozenset(zip(jobs, colors)))
        return result

    def check_linear_constraints(self):
        onehot = row = 0
        for S in self.monomials(3):
            v = self.moment(S)
            for j in range(self.n):
                assert sum(self.moment(S | {(j, i)}) for i in range(self.m)) == v
                onehot += 1
            for i in range(self.m):
                assert sum(self.moment(S | {(j, i)}) for j in range(self.n)) == self.t * v
                row += 1
        b1 = self.monomials(1)
        localizer = 0
        for i in range(self.m):
            for S in b1:
                for U in b1:
                    V = S | U
                    assert self.t * self.moment(V) == sum(
                        self.moment(V | {(j, i)}) for j in range(self.n)
                    )
                    localizer += 1
        negative = self.moment({(0, 0), (1, 0), (2, 0)})
        assert negative == -Q(1, self.m**4)
        return {"onehot_equalities": onehot, "row_recurrences": row,
                "zero_localizer_entries": localizer,
                "same_machine_triple": str(negative)}

    def full_moment_matrix(self):
        basis = self.monomials(2)
        matrix = [[self.moment(S | U) for U in basis] for S in basis]
        return matrix


def exact_psd_ldl(matrix):
    """Fraction Schur elimination; a zero pivot must have a zero remaining row."""
    A = [row[:] for row in matrix]
    n, rank = len(A), 0
    pivots = []
    for k in range(n):
        p = A[k][k]
        assert p >= 0, ("negative pivot", k, str(p))
        if p == 0:
            assert all(A[k][j] == 0 for j in range(k + 1, n)), ("nonzero zero-pivot row", k)
            continue
        rank += 1
        pivots.append(p)
        nonzero = [j for j in range(k + 1, n) if A[k][j]]
        for z, i in enumerate(nonzero):
            for j in nonzero[z:]:
                A[i][j] -= A[k][i] * A[k][j] / p
                A[j][i] = A[i][j]
    return {"dimension": n, "rank": rank, "psd": True,
            "positive_pivots": len(pivots),
            "min_positive_pivot": str(min(pivots))}


def expected_color(m, n, degree, func):
    t = Q(n, m)
    total = Q(0)
    for colors in product(range(m), repeat=degree):
        value = Q(1)
        for a in range(m):
            value *= falling(t, colors.count(a))
        total += value / falling(Q(n), degree) * func(colors)
    return total


def check_color_gram(m):
    n, t = m + 1, Q(m + 1, m)
    # One trace/nontrace-mixed symmetric row-zero kernel and a nonzero skew kernel.
    v = [1, -1] + [0] * (m - 2)
    B = [[Q(a * b) for b in v] for a in v]
    C = [[Q(0) for _ in range(m)] for _ in range(m)]
    C[0][1] = C[1][2] = C[2][0] = 1
    C[1][0] = C[2][1] = C[0][2] = -1
    F = sum(x * x for row in B for x in row)
    H = sum(B[a][a]**2 for a in range(m))
    trace = sum(B[a][a] for a in range(m))
    Fc = sum(x * x for row in C for x in row)
    D = expected_color(m, n, 2, lambda z: B[z[0]][z[1]]**2)
    O = expected_color(m, n, 3, lambda z: B[z[0]][z[1]] * B[z[0]][z[2]])
    Z = expected_color(m, n, 4, lambda z: B[z[0]][z[1]] * B[z[2]][z[3]])
    assert D == (t*t*F-t*H)/falling(Q(n), 2)
    assert O == (-t*t*F+2*t*H)/falling(Q(n), 3)
    assert Z == (t*t*(trace*trace+2*F)-6*t*H)/falling(Q(n), 4)
    K = t*t/Q(n*(n-3))*(F-Q(m,n-2)*H+Q(trace*trace,(n-1)*(n-2)))
    symmetric = expected_color(m, n, 4, lambda z: (
        B[z[0]][z[2]]-B[z[0]][z[3]]-B[z[1]][z[2]]+B[z[1]][z[3]])**2)
    antisymmetric = expected_color(m, n, 3, lambda z: (
        C[z[0]][z[1]]+C[z[1]][z[2]]+C[z[2]][z[0]])**2)
    assert symmetric == 4*(D-2*O+Z) == 4*K
    assert antisymmetric == 3*t*t/Q((n-1)*(n-2))*Fc
    assert symmetric > 0 and antisymmetric > 0
    return {"m": m, "symmetric_four_point_norm": str(symmetric),
            "antisymmetric_cycle_norm": str(antisymmetric), "symmetric_K": str(K)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-m", nargs="+", type=int, default=[3, 4])
    parser.add_argument("--max-formula-m", type=int, default=8)
    args = parser.parse_args()
    output = {"claim": "UM-C2-LOAD-UNIT-GAP-v1", "arithmetic": "fractions.Fraction",
              "scope": "finite exact checks; general PSD is proved separately",
              "full_moment_audits": [], "color_formula_checks": []}
    for m in args.full_m:
        started = time.monotonic()
        instance = UnitGap(m)
        data = {"m": m, "n": instance.n, "T": str(instance.t),
                "integer_OPT": 2, "ratio": str(Q(2, 1)/instance.t)}
        data.update(instance.check_linear_constraints())
        data["M2"] = exact_psd_ldl(instance.full_moment_matrix())
        expected_rank = 1 + m*(m-1) + m*m*(m-1)*(m-2)//2
        assert data["M2"]["rank"] == expected_rank
        data["elapsed_seconds"] = round(time.monotonic()-started, 3)
        output["full_moment_audits"].append(data)
    for m in range(3, args.max_formula_m+1):
        output["color_formula_checks"].append(check_color_gram(m))
    with open(__file__, "rb") as handle:
        output["script_sha256"] = hashlib.sha256(handle.read()).hexdigest()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
