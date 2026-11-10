#!/usr/bin/env python3
"""Exact Farkas witness on the 1631 route-compatible seven-maxima columns.

Six providers choose sequentially from a common directory with seven maximal
coverages B0,...,B6. The actual actions are routed to (0,0,0,0,1,0), and the
last actual action is B0. A column (I,J) records the maxima and actual positions
containing a customer. Every actual position in J must have its route in I,
and 5 is in J precisely when 0 is in I. Integers encode sets with bit 0 first.

The given positive rational distribution makes all six M, seven L, and 28
ordinary T rows nonnegative in expectation. At each prefix with r players
left, all R_H and script-variant R'_H for |H|=r-1 are strictly positive in
expectation using seat upper bounds U_jk=|B_j|/(p_j+k), where p_j counts
earlier actions routed to j. Its target E[W-|B1 union ... union B6|/2] is negative.
Consequently no fixed nonnegative combination of those rows can pay that
target pointwise on this column domain. Here the private B0 block is empty,
so the indicated six-maxima union equals the entire union and is optimal.
The witness is independent of both the frozen five-route witnesses and the
4064-column orbit average. It realizes directory and action memberships but
fails the true penultimate safety bound against B0, so it is not an SPE.

Baseline row formulas follow audit_route_obstruction.py (SHA-256
1947baf67c016837b786148652d687efde0556614c94c78af6e9f05f58129b0b).
The difference between R and R' follows the ASR residual review (SHA-256
01e86225106b72d67fb17716c6eb68c9e888f7d6e8b1af957f07e66f3b671054).
The script requires only Python's standard library. No optimizer is used.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json


PLAYERS = 6
MAXIMA = 7
ROUTE = (0, 0, 0, 0, 1, 0)
DENOMINATOR = 6971616396
SUPPORT = (
    (2, 16, 212881422),
    (2, 0, 106440711),
    (3, 63, 2353190850),
    (4, 0, 699241418),
    (5, 40, 73675140),
    (5, 32, 33253447),
    (8, 0, 699231936),
    (9, 46, 81924480),
    (9, 32, 49619379),
    (16, 0, 661454380),
    (17, 47, 375496710),
    (17, 32, 32778713),
    (32, 0, 698079873),
    (33, 44, 80644410),
    (33, 32, 44371092),
    (64, 0, 711520608),
    (65, 32, 57811827),
)


def has(mask, index):
    return (mask >> index) & 1


def columns():
    for incidence in range(1, 1 << MAXIMA):
        eligibility = sum(
            1 << t for t, owner in enumerate(ROUTE) if has(incidence, owner)
        )
        last = has(incidence, ROUTE[-1])
        for membership in range(1 << PLAYERS):
            if membership & ~eligibility == 0 and has(membership, PLAYERS - 1) == last:
                yield incidence, membership


def pay(membership, t):
    return F(has(membership, t), membership.bit_count() or 1)


def baseline(incidence, membership):
    beta = (F(1, 21), F(2, 37), F(1, 16), F(2, 27), F(1, 11), F(7, 72))
    size = incidence.bit_count()
    for t, shared_floor in enumerate(beta):
        floor = {1: F(1, 12), MAXIMA: F(1, 6)}.get(size, shared_floor)
        yield f"M{t}", pay(membership, t) - floor

    prior = (membership & 31).bit_count()
    for j in range(MAXIMA):
        yield f"L{j}", pay(membership, 5) - F(has(incidence, j), prior + 1)

    past = (membership & 15).bit_count()
    tax = F(has(membership, 4), (past + 1) * (past + 2))
    tail = pay(membership, 4) + pay(membership, 5)
    for j, k in combinations_with_replacement(range(MAXIMA), 2):
        hits = has(incidence, j) + has(incidence, k)
        comparison = F(hits, past + hits) if hits else F()
        yield f"T{j}{k}", tail + tax - comparison


def residual_minima(weight, t):
    r = PLAYERS - t
    length = (MAXIMA - 1) * r + 1
    prefix = [ROUTE[:t].count(j) for j in range(MAXIMA)]
    average_pay = sum(w * pay(membership, t) for (_, membership), w in weight.items())
    mean_q = {}
    mean_upper = {}
    for j, k in product(range(MAXIMA), range(1, r + 1)):
        seat = (j, k)
        mean_q[seat] = F()
        mean_upper[seat] = F()
        for (incidence, _), w in weight.items():
            if not has(incidence, j):
                continue
            route_load = sum(prefix[h] for h in range(MAXIMA) if has(incidence, h))
            upper_denom = prefix[j] + k
            q_denom = upper_denom if incidence.bit_count() == 1 else route_load + r
            mean_q[seat] += w / q_denom
            mean_upper[seat] += w / upper_denom

    base = average_pay - sum(mean_q.values(), F()) / length

    def minimum(increments):
        # A common H is chosen after averaging each seat over the distribution.
        chosen = sorted(increments, key=lambda h: (increments[h], h))[: r - 1]
        return base + sum((increments[h] for h in chosen), F()) / length, chosen

    true, true_h = minimum(mean_upper)
    variant, variant_h = minimum({h: mean_upper[h] - mean_q[h] for h in mean_q})
    return true, variant, true_h, variant_h


def main():
    domain = tuple(columns())
    assert len(set(domain)) == len(domain) == 1631
    weight = {(inc, actual): F(n, DENOMINATOR) for inc, actual, n in SUPPORT}
    assert len(weight) == 17 and set(weight).issubset(domain)
    assert min(weight.values()) > 0 and sum(weight.values(), F()) == 1

    averages = {}
    for incidence, membership in domain:
        w = weight.get((incidence, membership), F())
        for name, coefficient in baseline(incidence, membership):
            averages[name] = averages.get(name, F()) + w * coefficient
    assert len(averages) == 41 and min(averages.values()) == 0

    private = [sum((w for (i, _), w in weight.items() if i == 1 << j), F())
               for j in range(MAXIMA)]
    assert private[0] == 0 and min(private[1:]) > 0
    assert (3, 63) in weight and (5, 40) in weight
    # B0 has no private customer but contains blocks shared only with B1 and
    # only with B2. Hence B0 is also maximal in the induced directory.
    compare = ((1 << MAXIMA) - 1) & ~1
    target = sum((w * (bool(j) - F(bool(i & compare), 2))
                  for (i, j), w in weight.items()), F())
    assert target == F(-7513394, 580968033)

    expected_true = (
        F(324152667, 35826362035),
        F(251556027, 30016681705),
        F(33434801, 4384664400),
        F(874637357, 132460711524),
        F(99018961, 20140225144),
        F(711011927, 54223683080),
    )
    expected_variant = (
        F(1368169817, 214958172210),
        F(83135887, 15291517095),
        F(4458673523, 1045742459400),
        F(718210363, 264921423048),
        F(20306369, 30210337716),
        F(711011927, 54223683080),
    )
    residuals = []
    for t in range(PLAYERS):
        true, variant, true_h, variant_h = residual_minima(weight, t)
        assert true == expected_true[t] and variant == expected_variant[t]
        assert true >= variant > 0
        residuals.append({"t": t, "min_R": str(true), "min_R_prime": str(variant),
                          "H_R": true_h, "H_R_prime": variant_h})

    # Forcing B0 at t=4 gives each member at least 1/(actual old load + 2).
    # This uses the true old load, not the potentially larger route load.
    safety_40 = sum((w * (pay(j, 4) - F(has(i, 0), (j & 15).bit_count() + 2))
                     for (i, j), w in weight.items()), F())
    assert safety_40 == F(-13148647, 4647744264)

    print(json.dumps({
        "route": ROUTE,
        "columns": len(domain),
        "positive_support": len(weight),
        "baseline_averages": {name: str(value) for name, value in averages.items()},
        "all_H_minima": residuals,
        "target_omit_B0": str(target),
        "true_safety_D_4_0": str(safety_40),
    }, indent=2))


if __name__ == "__main__":
    main()
