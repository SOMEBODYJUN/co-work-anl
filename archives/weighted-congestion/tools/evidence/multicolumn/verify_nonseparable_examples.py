#!/usr/bin/env python3
"""New independent finite supplement; not a recovered historical audit.

All resource costs are rebuilt literally. Rational powers are enclosed by
certified rational root intervals; no binary floating-point acceptance.
"""
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys


def integer_root(n, degree):
    if n < 2 or degree == 1:
        return n
    lo, hi = 0, 1
    while hi**degree <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**degree <= n:
            lo = mid
        else:
            hi = mid
    return lo


@lru_cache(None)
def power_interval(value, exponent, bits):
    assert value > 0 and exponent > 0
    base = value**exponent.numerator
    degree = exponent.denominator
    rn = integer_root(base.numerator, degree)
    rd = integer_root(base.denominator, degree)
    if rn**degree == base.numerator and rd**degree == base.denominator:
        exact = Q(rn, rd)
        return exact, exact
    lo = Q(integer_root(base.numerator // base.denominator, degree))
    hi = lo + 1
    assert lo**degree < base < hi**degree
    for _ in range(bits):
        mid = (lo + hi) / 2
        if mid**degree < base:
            lo = mid
        else:
            hi = mid
    assert lo**degree <= base <= hi**degree
    return lo, hi


def literal_two_states(n, degree, private_cost, constant):
    # n players have a singleton strategy; the final player has {f} or {e}.
    fixed = [frozenset(('e', 'h')) if private_cost else frozenset(('e',))
             for _ in range(n)]
    answers = []
    for active in (frozenset(('f',)), frozenset(('e',))):
        strategies = fixed + [active]
        loads = {r: sum(r in strategy for strategy in strategies)
                 for r in ('e', 'h', 'f')}
        fees = {'e': Q(loads['e'])**degree, 'h': Q(private_cost), 'f': constant}
        answers.append(tuple(sum((fees[r] for r in strategy), Q(0))
                             for strategy in strategies))
    assert all(x > 0 for costs in answers for x in costs)
    return answers


def power_case(n, degree, exponent, constant, private_cost, target):
    bad, good = literal_two_states(n, degree, private_cost, constant)
    bits = 128
    while True:
        bad_upper = sum(power_interval(c, exponent, bits)[1] for c in bad)
        good_lower = sum(power_interval(c, exponent, bits)[0] for c in good)
        if bad_upper < good_lower:
            break
        bits *= 2
        assert bits <= 1024
    improvement = bad[-1] / good[-1]
    assert improvement > target >= 1
    assert good[-1] < bad[-1]  # the other state is an exact PNE
    return dict(n=n, degree=degree, p=exponent, K=constant, H=private_cost,
                target=target, current_costs=bad, deviation_state_costs=good,
                root_bisection_bits=bits, bad_objective_upper=bad_upper,
                good_objective_lower=good_lower,
                unique_global_minimum_certified=True,
                active_improvement=improvement, other_state_is_exact_PNE=True)


def product_case(n, degree, target):
    upper = (1 + Q(1, n))**(degree*n)
    assert upper > target
    constant = (upper + target) * Q((n+1)**degree, 2)
    bad, good = literal_two_states(n, degree, 0, constant)
    a = b = Q(1)
    for value in bad:
        a *= value
    for value in good:
        b *= value
    assert a < b and bad[-1] > target*good[-1]
    return dict(n=n, degree=degree, target=target, K=constant,
                current_costs=bad, deviation_state_costs=good,
                bad_product=a, good_product=b,
                active_improvement=bad[-1]/good[-1],
                finite_threshold=upper,
                unique_product_and_log_minimum_certified=True,
                other_state_is_exact_PNE=good[-1] < bad[-1])


def main():
    affine = [power_case(1, 1, p, Q(100), H, Q(10))
              for p, H in ((Q(2), 10**4), (Q(3, 2), 10**8),
                           (Q(11, 10), 10**30))]
    concave = [power_case(n, d, p, Q(K), 0, target)
               for n, d, p, K, target in
               ((100, 1, Q(1), 200, Q(19, 10)),
                (100, 2, Q(1), 30300, Q(29, 10)),
                (100, 2, Q(1, 2), 200**2, Q(3)),
                (100, 3, Q(1, 3), 200**3, Q(7)),
                (100, 3, Q(2, 3), 174**3, Q(5)))]
    products = [product_case(n, d, target) for n, d, target in
                ((1, 3, Q(7)), (100, 1, Q(8, 3)),
                 (100, 2, Q(7)), (100, 3, Q(19)))]
    report = dict(status='all new exact assertions passed',
                  provenance='new finite implementation; not historical verify_nonseparable.py',
                  arithmetic='Fraction and integer root certificates; no binary64 acceptance',
                  python=sys.version,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  affine_p_greater_than_one=affine,
                  power_p_at_most_one=concave,
                  positive_product_and_log=products,
                  scope='12 finite two-state games; general real-p and limit claims require the archived proofs')
    print(json.dumps(report, default=str, indent=2))


if __name__ == '__main__':
    main()
