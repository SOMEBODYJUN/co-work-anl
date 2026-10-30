#!/usr/bin/env python3
"""Reproduce exact finite-state checks and high-precision asymptotic samples.

Only Python standard-library arithmetic is used. Fraction tests are exact.
Decimal samples are numerical evidence, not proofs or interval certificates.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import math
import sys


def ratios(d, n, k, w, beta):
    a = (1 + w) ** d
    return ((1 + n * beta * a) / ((1 + n * w) ** k + n * beta),
            ((1 + w) ** k + beta * w ** d) / ((n * w) ** k + beta * a))


def costs(d, n, k, w, beta, state):
    weights = [Fraction(1)] + [w] * n
    strategy = [tuple(range((n + 1) * state[0], (n + 1) * (state[0] + 1)))]
    for i, side in enumerate(state[1:], 1):
        strategy.append((side * (n + 1), (1 - side) * (n + 1) + i))
    loads = [Fraction(0)] * (2 * (n + 1))
    for weight, resources in zip(weights, strategy):
        for e in resources:
            loads[e] += weight
    latency = [x ** k if e % (n + 1) == 0 else beta * x ** d
               for e, x in enumerate(loads)]
    return [sum((latency[e] for e in resources), Fraction(0)) for resources in strategy]


def exact_checks():
    games = states = deviations = 0
    for d in (2, 3, 4, 6):
        for n in range(1, 5):
            for k in range(1, d + 1):
                for w in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)):
                    for beta in (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(1)):
                        r_h, r_l = ratios(d, n, k, w, beta)
                        games += 1
                        for state in product((0, 1), repeat=n + 1):
                            before = costs(d, n, k, w, beta, state)
                            m = sum(s == state[0] for s in state[1:])
                            j = 0 if m == 0 else next(i for i in range(1, n + 1)
                                                    if state[i] == state[0])
                            after_state = list(state)
                            after_state[j] = 1 - state[j]
                            after = costs(d, n, k, w, beta, after_state)
                            bound = r_h if m == 0 else r_l
                            assert before[j] >= bound * after[j]
                            assert before[j] >= min(r_h, r_l) * after[j]
                            for i in range(n + 1):
                                flipped = list(state)
                                flipped[i] = 1 - state[i]
                                ci = costs(d, n, k, w, beta, flipped)[i]
                                if i == 0:
                                    expected_num = (1 + m*w)**k + (n-m)*beta*(1+w)**d + m*beta
                                    expected_den = (1 + (n-m)*w)**k + m*beta*(1+w)**d + (n-m)*beta
                                elif state[i] == state[0]:
                                    expected_num = (1 + m*w)**k + beta*w**d
                                    expected_den = ((n-m+1)*w)**k + beta*(1+w)**d
                                else:
                                    expected_num = ((n-m)*w)**k + beta*(1+w)**d
                                    expected_den = (1+(m+1)*w)**k + beta*w**d
                                assert before[i] == expected_num
                                assert ci == expected_den
                                deviations += 1
                            states += 1
    return {"games": games, "profiles": states, "deviations": deviations,
            "method": "Fraction; resource-level costs compared against formulas and designated attacks",
            "all_passed": True}


def log1p(x):
    # Avoid rounding 1+x to 1 when d is much larger than the precision.
    if abs(x) >= Decimal("0.01"):
        return (1 + x).ln()
    term = x
    total = x
    j = 1
    while True:
        j += 1
        term *= -x
        new = total + term / j
        if new == total:
            return total
        total = new


def sample(power):
    # Extra digits make the displayed integer floor n stable at all listed inputs.
    with localcontext() as ctx:
        ctx.prec = max(100, power + 80)
        d = Decimal(10) ** power
        D = d.ln()
        H = D.ln()
        h = H - (2 * H).ln()
        if h <= 0:
            raise ValueError("candidate denominator is nonpositive")
        w = D / (2 * d)
        n = int(4 * d * H / D**2)
        k = int((D / (2 * h)).to_integral_value(rounding="ROUND_CEILING"))
        e = Decimal(1).exp()
        S = (d * H).sqrt() / D
        q = e.sqrt() / (2 * S)
        ln_a = d * log1p(w)
        a = ln_a.exp()
        beta = q / a
        x = n * w
        big_a = (k * log1p(x)).exp()
        big_b = (k * log1p(w)).exp()
        big_c = (k * x.ln()).exp()
        # w**d is safely negligible, but it is retained via logarithms.
        log_tail = d * w.ln()
        tail = log_tail.exp() if log_tail > Decimal(-ctx.Emax) else Decimal(0)
        r_h = (1 + n * q) / (big_a + n * beta)
        r_l = (big_b + beta * tail) / (big_c + q)
        def out(v):
            return format(v, ".38g")
        assert 0 < w <= 1 and 0 < beta <= 1 and 1 <= k <= d and n >= 1
        assert big_c <= (1 / d.sqrt()) * (1 + Decimal("1e-70"))
        return {"d": str(int(d)), "power10": power, "precision_digits": ctx.prec,
                "n": str(n), "k": k, "w": out(w), "beta": out(beta),
                "q": out(q), "S": out(S), "RH": out(r_h), "RL": out(r_l),
                "RH_over_S": out(r_h / S), "RL_over_S": out(r_l / S),
                "min_over_S": out(min(r_h, r_l) / S),
                "target_limit": out(2/e.sqrt()), "nw": out(x),
                "k_nw": out(k*x), "n_beta": out(n*beta),
                "C_over_q": out(big_c/q)}


def main():
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    result = {"claim": "WC-R1-LF-SHARP v1", "exact": exact_checks(),
              "samples": [sample(p) for p in (4, 8, 16, 32, 64, 128, 256, 512, 1024)]}
    path = Path(__file__).with_name("verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["exact"], indent=2))
    for row in result["samples"]:
        print("d=1e%s k=%s RH/S=%s RL/S=%s" %
              (row["power10"], row["k"], row["RH_over_S"][:15], row["RL_over_S"][:15]))
    print("Wrote", path)


if __name__ == "__main__":
    main()
