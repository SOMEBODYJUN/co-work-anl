#!/usr/bin/env python3
"""Compressed exact certificates for WC-R1-MULTIPLIER-BARRIER v1."""
from fractions import Fraction as F
from math import comb
from decimal import Decimal, localcontext
from pathlib import Path
import argparse
import hashlib
import json


def powersums(k, d):
    out = [k]
    for p in range(1, d + 1):
        num = (k + 1) ** (p + 1) - 1 - sum(comb(p + 1, r) * out[r] for r in range(p))
        quo, rem = divmod(num, p + 1)
        assert rem == 0
        out.append(quo)
    return out


def finite_ratio(d, eps, target_t, s):
    k = target_t // eps
    assert k >= 1
    ps = powersums(k, d)
    u = k * eps
    light_last = eps ** (d + 1) * ps[d]
    light_first = eps * sum((comb(d, r) * eps ** r * ps[r] for r in range(d + 1)), F(0))
    return ((1 + u) ** d + s * light_last) / (1 + s * light_first)


def limit_ratio(d, t, s):
    return ((d + 1) * (1 + t) ** d + s * t ** (d + 1)) / (d + 1 + s * ((1 + t) ** (d + 1) - 1))


def dec(q):
    with localcontext() as ctx:
        ctx.prec = 20
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def positive_fingerprint(q):
    assert q > 0
    raw = f"{q.numerator:x}/{q.denominator:x}".encode()
    return {"sign": "+", "numerator_bits": q.numerator.bit_length(),
            "denominator_bits": q.denominator.bit_length(), "hex_fraction_sha256": hashlib.sha256(raw).hexdigest()}


def make_case(d, alpha, t0):
    assert alpha >= 1 and limit_ratio(d, t0, F(1)) > alpha
    d0 = alpha * ((1 + t0) ** (d + 1) - 1) - t0 ** (d + 1)
    assert d0 > 0
    lammax = (d + 1) * ((1 + t0) ** d - alpha) / d0
    assert lammax > 1
    lam = (1 + lammax) / 2
    t1 = 1 / (alpha + 1)
    d1 = (1 + t1) ** (d + 1) - 1 - alpha * t1 ** (d + 1)
    assert d1 > 0
    cap = lam + 1 + (d + 1) * (alpha * (1 + t1) ** d - 1) / d1
    assert cap > lam > 1
    assert limit_ratio(d, t0, lam) > alpha
    assert limit_ratio(d, t1, cap) < 1 / alpha
    levels = 1
    while lam ** levels <= cap:
        levels += 1
    denominator = 2
    while True:
        eps = F(1, denominator)
        if eps <= min(t0, t1):
            adjacent = finite_ratio(d, eps, t0, lam)
            extreme = finite_ratio(d, eps ** levels, t1, cap)
            if adjacent > alpha and extreme < 1 / alpha:
                break
        denominator *= 2
    # The complete finite multiset has classes j=0..levels, weight Q^(-j),
    # count ceil(T*Q^j)+1. Check required clone counts without expansion.
    total = 0
    largest_class = 0
    tmax = max(t0, t1)
    for j in range(levels + 1):
        z = tmax * denominator ** j
        count = -(-z.numerator // z.denominator) + 1
        total += count
        largest_class = count
        if j >= 1:
            assert t0 // eps <= count
    assert t1 // (eps ** levels) <= largest_class
    return {
        "d": d, "alpha": str(alpha), "t0": str(t0), "t1": str(t1),
        "lambda": str(lam), "C": str(cap), "L": levels, "Q": denominator,
        "class_weight_formula": "a_j=Q^(-j), j=0,...,L",
        "class_count_formula": "N_j=ceil(max(t0,t1)*Q^j)+1",
        "total_players": str(total),
        "adjacent_ratio_decimal": dec(adjacent), "target_alpha_decimal": dec(alpha),
        "extreme_ratio_decimal": dec(extreme), "inverse_alpha_decimal": dec(1 / alpha),
        "adjacent_strict_gap": positive_fingerprint(adjacent - alpha),
        "extreme_strict_gap": positive_fingerprint(1 / alpha - extreme),
        "chain_strict_gap": positive_fingerprint(lam ** levels - cap),
        "all_checks": "exact rational; no expanded player list or game-state claim",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="multiplier_evidence.json")
    args = parser.parse_args()
    # Independently check power-sum recurrence at manageable values.
    for k in range(1, 20):
        assert powersums(k, 12) == [sum(j ** p for j in range(1, k + 1)) for p in range(13)]
    cases = [(2, F(6, 5), F(4, 5)), (4, F(2), F(3, 4)),
             (8, F(4), F(3, 5)), (16, F(10), F(2, 5))]
    rows = [make_case(*case) for case in cases]
    Path(args.output).write_text(json.dumps({"claim": "WC-R1-MULTIPLIER-BARRIER v1", "records": rows}, indent=2) + "\n")
    for row in rows:
        print(f"d={row['d']}, excluded alpha={row['alpha']}, L={row['L']}, Q={row['Q']}, player count digits={len(row['total_players'])}")
    print("All compressed finite certificates verified exactly.")


if __name__ == "__main__":
    main()
