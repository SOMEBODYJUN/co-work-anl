"""Five-site reduction for every fixed rational 1 < a < phi.

Only exact rational arithmetic is used.  This constructs an instance; it is
not a polynomial-time solver for SUBSET SUM or for the resulting game.
All site/customer indices in JSON are zero based.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
import argparse
import json


def constants(a):
    a = F(a)
    if not (a > 1 and a*a < a+1):
        raise ValueError("require a rational 1 < a < phi")
    # a is fixed in the complexity theorem. This search is independent
    # of the SUBSET SUM instance.
    k = 1
    while True:
        e = F(1, 2**k)
        r2 = a + e
        r3 = max(F(1), a*r2/2) + 4*e
        r4 = max(F(1), r2/a, a*r3/2) + e
        r10 = 1 + 1/a
        if (1 < r4 < r3 < r2 < r10
                and r2 > a
                and r2 > a*r10/2
                and r3 > a*r2/2
                and r4 > a*r3/2
                and a*r4 > r2
                and a*r4 < 2
                and r2+r3+r4 < 4):
            break
        k += 1
    eta = min(
        F(1),
        (r10-r2)/(1+1/(2*a)),
        2-a*r4,
        r4-1,
        (4-r2-r3-r4)/3,
    ) / 4
    assert eta > 0
    return dict(a=a, epsilon=e, r2=r2, r3=r3, r4=r4, eta=eta)


def reduction(numbers, target, a):
    """Construct the rational reduction, including auditable parameters.

    Domain: nonempty explicit list of positive integers and
    0 <= target <= sum(numbers). This restricted SUBSET SUM is NP-hard.
    Trivial targets need not be removed for this construction.
    """
    numbers = list(numbers)
    if not numbers or any(type(x) is not int or x <= 0 for x in numbers):
        raise ValueError("numbers must be an explicit nonempty positive integer list")
    if type(target) is not int or not 0 <= target <= sum(numbers):
        raise ValueError("target must be an integer between zero and the sum")
    c = constants(a)
    a = c["a"]
    base = 2*sum(numbers) + 1
    bounded = []
    marker_sum = 0
    for j, b in enumerate(numbers):
        marker = base * 5**j
        marker_sum += marker
        bounded += [marker+b, marker]
    U = sum(bounded)
    original_target = marker_sum + target
    complemented_target = 2*U-original_target
    d0 = complemented_target-U
    Q0 = 2*U+complemented_target+1
    n = len(bounded)
    raw_micro = [Q0+x for x in bounded] + [Q0]*(n+1)
    W0 = sum(raw_micro)
    assert d0 > 0
    scale = c["eta"] / (W0+d0+Q0)
    micro = [scale*x for x in raw_micro]
    W, d, Q = scale*W0, scale*d0, scale*Q0
    H = 1-W-d
    T = (H+1-Q)/2
    v1 = T/a
    v2 = c["r2"]-H
    v3 = c["r3"]-H
    z = c["r4"]-1+d
    P = 1-v2-v3-z-W
    # H, v1, v2, v3, z, P, followed by micro customers.
    weights = [H, v1, v2, v3, z, P] + micro
    sites = [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4] + list(range(6, len(weights))),
        [2, 3, 4, 5] + list(range(6, len(weights))),
    ]
    assert all(w > 0 for w in weights)
    reach = [sum((weights[i] for i in s), F(0)) for s in sites]
    assert reach == [H+v1, c["r2"], c["r3"], c["r4"], F(1)]
    assert 1 < reach[3] < reach[2] < reach[1] < reach[0]
    assert z-d > W
    assert T > a*reach[3]/2
    assert a*v3 < a*v2 < T
    pars = dict(c, W=W, d=d, Q=Q, H=H, T=T, v1=v1, v2=v2,
                v3=v3, z=z, P=P, scale=scale, W0=W0, d0=d0, Q0=Q0,
                bounded=bounded, bounded_target=complemented_target,
                raw_micro=raw_micro, reach=reach)
    instance = dict(weights=weights, locations=sites, U1=list(range(5)),
                    U2=list(range(5)))
    return instance, pars


def integer_instance(instance):
    """Uniformly scale to positive binary integers, preserving all factors."""
    den = lcm(*(F(w).denominator for w in instance["weights"]))
    weights = [int(F(w)*den) for w in instance["weights"]]
    common = reduce(gcd, weights)
    result = dict(instance, weights=[w//common for w in weights])
    return result, F(den, common)


def serial(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): serial(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serial(v) for v in obj]
    return obj


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--factor", required=True)
    p.add_argument("--numbers", required=True, help="comma-separated positive integers")
    p.add_argument("--target", required=True, type=int)
    p.add_argument("--output", required=True)
    p.add_argument("--metadata", help="optional separate parameter JSON")
    args = p.parse_args()
    inst, pars = reduction([int(x) for x in args.numbers.split(",")],
                           args.target, F(args.factor))
    integer, scale = integer_instance(inst)
    with open(args.output, "x", encoding="utf-8") as f:
        json.dump(serial(integer), f, indent=2)
        f.write("\n")
    if args.metadata:
        with open(args.metadata, "x", encoding="utf-8") as f:
            json.dump(serial(dict(parameters=pars, integer_scale=scale)), f, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
