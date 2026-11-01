"""Fraction checks for explicit identities, not an SPE/security theorem."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from functools import lru_cache
from math import factorial, prod, comb
from pathlib import Path
import json


def delta_sum(bits, base):
    a, *bb = bits
    k = len(bb)
    ans = Q(0)
    for choices in product((0, 1), repeat=k):
        load = sum(a if c else b for c, b in zip(choices, bb))
        h = sum((Q(1, base+j) for j in range(1, load+1)), Q(0))
        ans += (-1)**(k-sum(choices))*h
    return ans


def masksum(h):
    return frozenset(x for x in h if x != 0)


def rank(h):
    return min(2, len(masksum(h)))


@lru_cache(None)
def phi(h):
    d = len(h)
    ans = Q(0)
    for bits in product((0, 1), repeat=d):
        j = sum(bits)
        if j:
            value = rank(tuple(a for a, c in zip(h, bits) if c))
            ans += Q(factorial(j-1)*factorial(d-j), factorial(d))*value
    return ans


def main():
    identities = 0
    even_taxes = 0
    for k in range(1, 9):
        for base in (0, 1, 2, 7):
            for bits in product((0, 1), repeat=k+1):
                actual = delta_sum(bits, base)
                a, *bb = bits
                expected = Q((-1)**(k-1)*factorial(k-1)*prod(a-b for b in bb), prod(base+j for j in range(1, k+1)))
                assert actual == expected
                identities += 1
                if k % 2 == 0:
                    assert actual <= 0
                    even_taxes += 1
    k = 5
    contexts = tuple(h for d in range(5) for h in combinations_with_replacement(range(k), d))
    mono = dr = budget = star2 = 0
    for h in contexts:
        d = len(h)
        if d:
            deletion_sum = sum((phi(h)-phi(h[:i]+h[i+1:]) for i in range(d)), Q(0))
            assert deletion_sum == rank(h)
            budget += 1
        if d <= 3:
            for a in range(k):
                assert phi(tuple(sorted(h+(a,)))) >= phi(h)
                mono += 1
        if d <= 2:
            for a, b in product(range(k), repeat=2):
                assert phi(tuple(sorted(h+(a,))))-phi(h) >= phi(tuple(sorted(h+(a,b))))-phi(tuple(sorted(h+(b,))))
                dr += 1
            for a, b, c in product(range(k), repeat=3):
                gap = phi(tuple(sorted(h+(a,a))))+phi(tuple(sorted(h+(b,c))))-phi(tuple(sorted(h+(a,b))))-phi(tuple(sorted(h+(a,c))))
                assert gap <= 0
                star2 += 1
    vals = [phi(tuple(range(1, j+1))) for j in range(5)]
    fourth = sum(((-1)**(4-j)*comb(4, j)*vals[j] for j in range(5)), Q(0))
    assert vals == [0, 1, 2, Q(8,3), Q(19,6)]
    assert fourth == Q(1, 2)
    report = {'status':'exact_identity_and_separation_checks_passed', 'identity_checks':identities,'even_nonpositive_checks':even_taxes,'matroid_contexts':len(contexts),'matroid_monotonicity_checks':mono,'matroid_DR_checks':dr,'matroid_budget_checks':budget,'matroid_second_pivot_checks':star2,'matroid_fourth_difference':str(fourth),'general_SPE_or_security_claim':False}
    print(json.dumps(report, indent=2))
    Path(__file__).with_name('even_pivot_taxes_verified.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
