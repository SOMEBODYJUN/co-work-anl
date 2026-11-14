from fractions import Fraction
from itertools import combinations, permutations, product

labels = (0, 1, 2, 3)


def coverage(support):
    s = set(support)
    assert len(s) <= 3
    return 1 + Fraction(len(s) - 1, 5) if 0 in s else Fraction(3 * len(s), 5)


def payoff(z, i):
    total = Fraction(0)
    for order in permutations(range(3)):
        previous = {z[j] for j in order[:order.index(i)]}
        total += coverage(previous | {z[i]}) - coverage(previous)
    return total / 6


def main():
    supports = [set(s) for size in range(4) for s in combinations(labels, size)]
    for a, b in product(supports, repeat=2):
        if len(a | b) <= 3:
            assert coverage(a) + coverage(b) >= coverage(a | b) + coverage(a & b)
        if a <= b:
            assert coverage(a) <= coverage(b)
    rows = []
    for size in range(3):
        for h in product(labels, repeat=size):
            trailing = (0,) * (2 - size)
            u = payoff(h + (0,) + trailing, size)
            for b in labels[1:]:
                gap = u - payoff(h + (b,) + trailing, size)
                assert gap >= 0, (h, b, gap)
                rows.append(gap)
    assert len(rows) == 63
    assert min(rows) == 0
    assert payoff((0, 0, 0), 0) == Fraction(1, 3)
    assert max(coverage(z) for z in product(labels, repeat=3)) == Fraction(9, 5)
    print(f'{len(rows)} true comparisons, {rows.count(0)} ties, OPT/K=9/5')


if __name__ == '__main__':
    main()
