"""Exact regression checks for a symbolic prefix/tail template obstruction.

No LP/SPE search. The universal proof, source contracts and limitations are
in architecture_audit.md. A Farkas vector below is not a CAG counterexample.
"""
from fractions import Fraction as F
from itertools import product
import json


def harmonic(n):
    return sum((F(1, r) for r in range(1, n + 1)), F(0))


def local_rows(n, tau, e, o):
    load = sum(e)
    shares = [F(a, load) if load else F(0) for a in e]
    prefix = []
    before = 0
    for i in range(n - 2):
        prefix.append(tau * shares[i] - F(o, before + n - i))
        before += e[i]
    p = sum(e[:-2])
    tail = tau * shares[-2] + shares[-1] / 2 - F(o, p + 1)
    if p == 0:
        tail += F(o * e[-2], 4)
    return prefix + [tail], F(2 * bool(load) - o)


def farkas_check(n, tau):
    # Omitted comparison customer, early-only noncomparison customers,
    # penultimate-only noncomparison customer.
    columns = [(F(1), (0,) * n, 1)]
    for i in range(n - 2):
        e = tuple(int(j == i) for j in range(n))
        columns.append((F(1) / (tau * (n - i)), e, 0))
    penult = tuple(int(j == n - 2) for j in range(n))
    columns.append((F(1) / tau, penult, 0))
    sums = [F(0)] * (n - 1)
    target = F(0)
    for mass, e, o in columns:
        assert mass > 0
        rows, t = local_rows(n, tau, e, o)
        sums = [a + mass * b for a, b in zip(sums, rows)]
        target += mass * t
    assert sums == [F(0)] * (n - 1)
    assert target == -1 + (2 * harmonic(n) - 1) / tau
    return target


def recurrence_identity(n, tau):
    # Arbitrary rational terminal payoffs: this tests an identity, not SPE.
    u = [F((i + 2) ** 2, i + 3) for i in range(n)]
    O = F(13, 3)
    P = F(0)
    weighted = F(0)
    for i in range(n):
        r = n - i
        slack = P + r * tau * u[i] - O
        weight = F(1) / (r * tau)
        for s in range(1, r):
            weight *= 1 - F(1) / (s * tau)
        assert weight >= 0
        weighted += weight * slack
        P += u[i]
    remaining = F(1)
    for r in range(1, n + 1):
        remaining *= 1 - F(1) / (r * tau)
    assert P == O * (1 - remaining) + weighted


def all_big_replay(n):
    # At every ordered history, payoffs depend only on its length, number
    # of B0 choices and number of the queried singleton choices. For n>=3
    # all count pairs below are feasible, since there is another label.
    comparisons = 0
    minimum = None
    for t in range(n):
        for a in range(t + 1):
            for q in range(t - a + 1):
                if n == 2 and a + q != t:
                    continue
                prescribed = F(n, a + n - t)
                deviation = F(1, q + 1)
                gap = prescribed - deviation
                assert gap >= 0
                minimum = gap if minimum is None else min(minimum, gap)
                comparisons += 1
    assert minimum == 0
    assert F(2 * n - 1, n) == 2 - F(1, n)
    # n distinct disjoint blocks are necessary to cover the entire union.
    assert n + (n - 1) == 2 * n - 1
    return comparisons


def projection_corner_check():
    checked = 0
    # The general proof uses a slope and a p>=1 inequality. These checks
    # audit boundary evaluation only and are not the universal argument.
    for p, a, o, tau in product(range(25), (0, 1), (0, 1),
                                 (F(1), F(3, 2), F(9, 2), F(6), F(25))):
        D = (p + 1) * (p + 2)
        for q, ell in product((F(o) / tau, F(1)), (F(0), F(1))):
            projected = -F(o, p + 1)
            if p == 0:
                projected += F(o * a, 4)
            raw = (-tau * q / (p + 1) + tau * q * ell / D
                   - ell / (2 * (p + a + 1)))
            assert projected >= raw
            checked += 1
    return checked


def shared_defect_identity():
    checked = 0
    for n, I, Dp, Ds, extra in product(range(2, 16), range(5), range(5),
                                       range(5), (F(0), F(1, 3), F(2))):
        # Exactly the two scalar conclusions used from the old spectrum:
        # W>=I and W>=Dp+(I+Ds)/n. No claim of SPE realizability here.
        W = max(F(I), F(Dp) + F(I + Ds, n)) + extra
        eta = 1 - F(1, n)
        target = (1 + eta) * W + eta * Ds - (I + Dp + Ds)
        slack = W - Dp - F(I + Ds, n) + eta * (W - I)
        assert target == slack and target >= 0
        if Ds <= W / (n - 1):
            assert I + Dp + Ds <= 2 * W
        checked += 1
    return checked


def main():
    family_counts = 0
    for n in range(3, 41):
        threshold = 2 * harmonic(n) - 1
        assert threshold < n
        assert farkas_check(n, F(n)) < 0
        assert farkas_check(n, threshold) == 0
        assert farkas_check(n, threshold + F(1, 7)) < 0
        for tau in (F(1), F(3, 2), F(n)):
            recurrence_identity(n, tau)
        family_counts += all_big_replay(n)
    all_big_replay(2)
    assert 2 * harmonic(6) - 1 == F(39, 10)
    assert farkas_check(6, F(6)) == -F(7, 20)
    assert farkas_check(6, F(9, 2)) == -F(2, 15)
    print(json.dumps({
        "status": "passed",
        "scope": "implementation audit; universal results have analytic proofs",
        "n_regression_range": [3, 40],
        "n6_tau_necessary_upper_bound": str(F(39, 10)),
        "n6_tau6_farkas_target": str(-F(7, 20)),
        "n6_tau9over2_farkas_target": str(-F(2, 15)),
        "all_big_history_count_cases": family_counts,
        "projection_corner_cases": projection_corner_check(),
        "shared_defect_algebra_cases": shared_defect_identity(),
        "is_counterexample_to_half": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
