#!/usr/bin/env python3
"""Exact implementation audit, not the all-k/all-background proof."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json


def add(*ps):
    out = [0] * max(map(len, ps))
    for p in ps:
        for i, v in enumerate(p):
            out[i] += v
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def mul(*ps):
    out = [1]
    for p in ps:
        nxt = [0] * (len(out) + len(p) - 1)
        for i, v in enumerate(out):
            for j, w in enumerate(p):
                nxt[i + j] += v * w
        out = nxt
    return out


def scale(s, p):
    return [s * v for v in p]


def abc(k):
    return (F(2 * (k - 2), k), F(7 * k - 16, k * (2 * k - 5)),
            F(k - 4, (k - 1) * (2 * k - 5)))


def slack(k, b, d, h):
    a, bb, c = abc(k)
    target = F(d, b + d) if d else F(0)
    return a * F(d, b + k) + (bb * d + c * h) / (b + 1 + h) - target


# Independently expand the h=k-1 numerator as polynomials in k,
# keeping the quadratic, linear, and constant coefficients in d separate.
kpoly = [0, 1]
km1, km2, km4, km5, twicekm5 = [-1, 1], [-2, 1], [-4, 1], [-5, 1], [-5, 2]
q_d2 = add(scale(2, mul(km1, km2)), mul(kpoly, twicekm5))
q_d1 = add(scale(2, mul(km1, km2, km5)), mul(kpoly, km4),
           scale(-1, mul(kpoly, kpoly, twicekm5)))
q_d0 = mul(kpoly, km4, km5)
assert q_d2 == [4, -11, 4]
assert q_d1 == [-20, 30, -10]
assert q_d0 == [0, 20, -9, 1]
q_at_one = add(q_d2, q_d1, q_d0)
assert q_at_one == [-16, 39, -15, 1]
shifted = [sum(v * comb(i, j) * 12 ** (i-j)
               for i, v in enumerate(q_at_one) if i >= j)
           for j in range(4)]
assert shifted == [20, 111, 21, 1]

count = 0
minimum = None
for k in range(12, 81):
    a, bb, c = abc(k)
    assert a >= 0 and bb >= 0 and c >= 0
    assert a * k == 2 * (k-2)
    assert bb * k + c * (k-1) == 4
    assert (1-bb) * (2*k-5) == a * (k-4)
    assert a-(1-bb) > 0
    for b in [k-5, k-4, k, 2*k, 10*k, 10**6]:
        for d in range(k+1):
            for h in [F(0), F(1, 2), F(k-1, 2), F(k-1)]:
                s = slack(k, b, d, h)
                assert s >= 0, (k, b, d, h, s)
                minimum = s if minimum is None else min(minimum, s)
                count += 1

full_h_count = 0
for k in range(12, 33):
    for b in range(k-5, k-1):
        for d in range(k+1):
            for h in range(k):
                assert slack(k, b, d, h) >= 0
                full_h_count += 1

counterexamples = []
for k in range(6, 101):
    b, q = k-6, 1
    kval = F(q, b+k)
    theta = F(q, b+1)
    opt = F(k*q, b+1)
    difference = opt - 2*(k-2)*kval - 4*theta
    assert difference == F(2*q, (k-5)*(k-3)) > 0
    # Concavity: no theme's marginal for a second seat exceeds an unused
    # theme's first marginal, hence all-one allocation is optimal.
    def value(n):
        return F(n*q, b+n) if n else F(0)
    first = value(1)
    for n in range(1, k):
        assert value(n+1)-value(n) <= first
    if k in [6, 12, 20, 100]:
        counterexamples.append({"k": k, "uniform_background": b,
            "K": str(kval), "theta": str(theta), "F": str(opt),
            "strict_bridge_gap": str(difference)})


def signed_error(k, t, b, d):
    if d == 0:
        return F(0)
    aa = F(2*(k-2), k)
    return F(d, b+d) - aa*F(d, b+k) - min(
        t*d/(k*(b+1)), (t*d/k+4-t)/(b+k))


signed_checks = 0
for k in range(2, 25):
    aa = F(2*(k-2), k)
    for b in [0, 1, k//2, k, 3*k]:
        for d in range(k+1):
            for t in [F(0), F(1), F(2), F(7, 2), F(4)]:
                err = signed_error(k, t, b, d)
                for h in [F(0), F(k-1, 3), F(k-1)]:
                    target = F(d, b+d) if d else F(0)
                    budget = (aa*F(d, b+k)
                              +(t*d/k+(4-t)*h/(k-1))/(b+1+h)+err)
                    assert target <= budget
                    signed_checks += 1

twelve_t = F(68, 19)
mixed_gap = signed_error(12, twelve_t, 0, 1) + 110*signed_error(12, twelve_t, 10, 1)
assert signed_error(12, twelve_t, 0, 1) == F(137, 171)
assert signed_error(12, twelve_t, 10, 1) == -F(5, 418)
assert mixed_gap == -F(88, 171)
# Exact marginal check for the stated F-optimal disjoint allocation.
assert F(10, 11) > F(20, 12)-F(10, 11) == F(25, 33)
assert F(1) > F(25, 33)

result = {
    "status": "exact implementation audit passed; independent review pending",
    "main_target": "Q-CAG-HALF remains OPEN",
    "proved_scope_in_companion_text": "all k>=12, all legal backgrounds b_x>=k-5, all full-history pure SPE",
    "polynomial_coefficients_ascending_k": {
        "d_squared": q_d2, "d": q_d1, "constant": q_d0,
        "Q_at_one": q_at_one, "Q_at_one_shift_k_equals_12_plus_t": shifted},
    "finite_fraction_checks": count,
    "finite_integer_h_checks": full_h_count,
    "finite_signed_penalty_checks": signed_checks,
    "mixed_background_example_signed_gap": str(mixed_gap),
    "finite_k_range": [12, 80],
    "finite_backgrounds": "k-5,k-4,k,2k,10k,1000000; plus k-5..k-2 for k<=32",
    "minimum_pointwise_slack": str(minimum),
    "strict_lower_background_bridge_counterexamples": counterexamples,
    "all_quantifier_reason": "affine h endpoints, monotonic b, integer-d quadratic differences, nonnegative polynomial in k-12",
    "not_proved": ["root half coverage", "low-background half profit", "any current-profit-only inductive recurrence"],
}
target = Path(__file__).with_name("joint_baseline_audit.json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
