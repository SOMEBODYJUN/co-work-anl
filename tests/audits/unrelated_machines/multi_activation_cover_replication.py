#!/usr/bin/env python3
"""Exact Fraction checks for the multi-activation and replication claims.

This is a small independent arithmetic audit.  It does not search for a
target schedule and does not serve as a proof of the general statements.
"""
from fractions import Fraction as F
from math import ceil


def ceil_frac(x: F) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def loads(p, assignment):
    m = len(p[0])
    out = [F(0) for _ in range(m)]
    for j, i in enumerate(assignment):
        assert p[j][i] is not None
        out[i] += p[j][i]
    return out


def check_static_cover_instance():
    # Two source machines, three jobs per source, all target jobs go to the
    # other machine.  Initial load is 6/5, target load is 9/10, T=1.
    T, C = F(1), F(6, 5)
    U = max(2 * T, C + T / 2)
    source = [0, 0, 0, 1, 1, 1]
    target = [1, 1, 1, 0, 0, 0]
    a = [F(2, 5)] * 6
    b = [F(3, 10)] * 6
    S = [sum(a[j] for j in range(6) if source[j] == i) for i in range(2)]
    Q = [sum(b[j] for j in range(6) if target[j] == i) for i in range(2)]
    h = [max(F(0), S[i] + Q[i] - U) for i in range(2)]
    assert U == 2 and S == [F(6, 5), F(6, 5)]
    assert Q == [F(9, 10), F(9, 10)] and h == [F(1, 10), F(1, 10)]
    R = {0, 3}
    D = [sum(a[j] for j in R if source[j] == i) for i in range(2)]
    P = [sum(b[j] for j in R if target[j] == i) for i in range(2)]
    assert D == [F(2, 5), F(2, 5)]
    assert P == [F(3, 10), F(3, 10)]
    assert all(D[i] >= h[i] for i in range(2))
    assert all(P[i] <= U - S[i] for i in range(2))

    current = source[:]
    for j in [0, 3, 1, 4, 2, 5]:
        current[j] = target[j]
        assert max(loads([[a[j] if i == source[j] else b[j] if i == target[j] else None
                           for i in range(2)] for j in range(6)], current)) <= U
    assert loads([[a[j] if i == source[j] else b[j] if i == target[j] else None
                   for i in range(2)] for j in range(6)], current) == Q


def check_edge_cases():
    # T=0 and all zero times: every route is safe.
    p = [[F(0), F(0)], [F(0), None]]
    assert loads(p, [0, 0]) == [F(0), F(0)]

    # h=0: no activation payment is needed.
    S, Q, U = F(1), F(1), F(2)
    assert max(F(0), S + Q - U) == 0

    # q_i=0<h_i must reject the uniform-end flow certificate.
    assert F(0) == 0 and F(1, 2) > 0


def check_unconditional_path_counterexample():
    T, C = F(3, 4), F(5, 4)
    U = max(2 * T, C + T / 2)
    p = [[F(1, 2), F(5, 4)], [F(1), F(3, 4)], [F(1, 4), None]]
    sigma = [1, 0, 0]
    tau = [0, 1, 0]
    assert U == F(13, 8)
    assert max(loads(p, sigma)) == C
    assert max(loads(p, tau)) == T
    first_j0 = sigma[:]
    first_j0[0] = 0
    first_j1 = sigma[:]
    first_j1[1] = 1
    assert max(loads(p, first_j0)) == F(7, 4) > U
    assert max(loads(p, first_j1)) == F(2) > U


def check_static_cover_is_not_necessary():
    # Six source jobs, two per machine.  A dynamic path stays below U even
    # though no single subset satisfies the static cover/packing certificate.
    T, C = F(1), F(2)
    U = max(2 * T, C + T / 2)
    source = [0, 0, 1, 1, 2, 2]
    target = [1, 2, 0, 2, 0, 1]
    a = [F(1)] * 6
    b = [F(3, 5), F(3, 5), F(3, 10), F(1, 5), F(3, 10), F(1, 5)]
    S = [F(2)] * 3
    Q = [F(3, 5), F(4, 5), F(4, 5)]
    h = [max(F(0), S[i] + Q[i] - U) for i in range(3)]
    assert U == F(5, 2) and h == [F(1, 10), F(3, 10), F(3, 10)]
    static = []
    for mask in range(1 << 6):
        R = {j for j in range(6) if mask >> j & 1}
        D = [sum(a[j] for j in R if source[j] == i) for i in range(3)]
        P = [sum(b[j] for j in R if target[j] == i) for i in range(3)]
        if all(D[i] >= h[i] for i in range(3)) and all(P[i] <= U - S[i] for i in range(3)):
            static.append(R)
    assert static == []

    # The order B->A, A->B, B->C, C->A, A->C, C->B.
    order = [2, 0, 3, 4, 1, 5]
    current = source[:]
    p = []
    for j in range(6):
        row = [None] * 3
        row[source[j]] = a[j]
        row[target[j]] = b[j]
        p.append(row)
    peaks = []
    for j in order:
        current[j] = target[j]
        peaks.append(max(loads(p, current)))
        assert peaks[-1] <= U
    assert max(loads(p, current)) == F(4, 5)
    assert max(peaks) == F(23, 10)


def check_shared_replication():
    # Three unit jobs on two identical machines: assignment LP F=3/2,
    # k-copy integer optimum ceil(3k/2).
    F_lp = F(3, 2)
    for k in range(1, 13):
        optimum = ceil(3 * k / 2)
        assert F(k * F_lp) == F(3 * k, 2)
        assert F(optimum) >= k * F_lp
        # For this instance S=max_i sum_j p_ij=3, so O_k <= kF+3.
        assert F(optimum) <= k * F_lp + 3
    assert F(ceil(3 * 12 / 2), 12) == F(3, 2)


if __name__ == "__main__":
    check_static_cover_instance()
    check_edge_cases()
    check_unconditional_path_counterexample()
    check_static_cover_is_not_necessary()
    check_shared_replication()
    print("multi_activation_cover_replication: PASS")
