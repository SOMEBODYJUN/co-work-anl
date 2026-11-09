"""Check the sharp two-provider omission and static-gap tradeoff exactly."""
from fractions import Fraction
from itertools import combinations_with_replacement, product

RESPONSE = (1, 4, 4, 4, 5, 4)
OTHER_PAIRS = tuple(
    (i, j) for i, j in combinations_with_replacement(range(6), 2)
    if (i, j) != (2, 3)
)
ENDPOINT_17 = {2: 3, 4: 3, 8: 3, 17: 2, 33: 2, 52: 1, 54: 1, 56: 1, 58: 1}
ENDPOINT_27 = {1: 4, 2: 5, 4: 3, 8: 3, 20: 2, 24: 2, 36: 2, 40: 2, 49: 2, 50: 2}
TERMINAL_MULTIPLIERS = {
    (0, 2): 126, (0, 3): 126, (0, 4): 12, (0, 5): 16,
    (2, 3): 14, (2, 5): 16, (4, 1): 12, (4, 3): 12,
    (5, 1): 16, (5, 3): 16,
}
ROOT_MULTIPLIERS = {2: 42, 4: 56}


def covers(mask, i, j):
    return int(bool(mask & ((1 << i) | (1 << j))))


def profit(mask, chosen, other):
    if not (mask >> chosen) & 1:
        return Fraction(0)
    return Fraction(1, 1 + ((mask >> other) & 1))


def terminal_slack(mask, i, j):
    return profit(mask, RESPONSE[i], i) - profit(mask, j, i)


def root_slack(mask, i):
    return profit(mask, 0, 1) - profit(mask, i, RESPONSE[i])


def check_dual():
    residuals = []
    for mask in range(1, 64):
        actual = covers(mask, 0, 1)
        designated = covers(mask, 2, 3)
        omitted = designated * (1 - actual)
        pair_slack = sum(designated - covers(mask, 1, j) for j in (2, 3))
        terminal = sum(
            coefficient * terminal_slack(mask, *key)
            for key, coefficient in TERMINAL_MULTIPLIERS.items()
        )
        root = sum(
            coefficient * root_slack(mask, i)
            for i, coefficient in ROOT_MULTIPLIERS.items()
        )
        remainder = 7 * actual - (91 * (omitted - actual) + 77 * pair_slack + terminal + root)
        assert remainder >= 0, (mask, remainder)
        residuals.append(remainder)
    return len(residuals), sum(x > 0 for x in residuals), max(residuals)


def check_primal(weights):
    def count(function, *args):
        return sum(n * function(mask, *args) for mask, n in weights.items())

    assert all(count(terminal_slack, i, j) >= 0 for i, j in product(range(6), repeat=2))
    assert all(count(root_slack, i) >= 0 for i in range(6))
    w = count(covers, 0, 1)
    o = count(covers, 2, 3)
    r = sum(n for mask, n in weights.items() if covers(mask, 2, 3) and not covers(mask, 0, 1))
    gap = min(o - count(covers, i, j) for i, j in OTHER_PAIRS)
    assert gap == o - count(covers, 1, 2) == o - count(covers, 1, 3)
    assert 22 * gap + 13 * r == 14 * w
    return sum(weights.values()), w, o, r, gap


def check_mixtures():
    print('dual columns, positive residuals, max residual', *check_dual())
    assert check_primal(ENDPOINT_17) == (17, 9, 10, 8, 1)
    assert check_primal(ENDPOINT_27) == (27, 13, 14, 14, 0)
    for a, b in product(range(11), repeat=2):
        if not (a or b):
            continue
        masks = ENDPOINT_17.keys() | ENDPOINT_27.keys()
        weights = {
            mask: a * ENDPOINT_17.get(mask, 0) + b * ENDPOINT_27.get(mask, 0)
            for mask in masks
        }
        assert check_primal(weights) == (17*a+27*b, 9*a+13*b, 10*a+14*b, 8*a+14*b, a)
    print('120 exact full-policy mixtures, 5040 incentive and 2400 competing-pair comparisons')


def check_general_catalogues():
    from itertools import combinations
    from random import Random

    generator = Random(373)
    catalogues = [x for size in range(1, 9) for x in combinations(range(8), size)]
    catalogues += [
        tuple(generator.randrange(1 << 7) for _ in range(generator.randrange(2, 10)))
        for _ in range(6000)
    ]
    paths = comparisons = applicable = high_residual = 0
    for catalogue in catalogues:
        labels = range(len(catalogue))
        pairs = list(combinations_with_replacement(labels, 2))
        pair_cover = {
            (i, j): (catalogue[i] | catalogue[j]).bit_count() for i, j in pairs
        }
        replies = []
        floor = []
        for a in labels:
            values = [2 * catalogue[b].bit_count() - (catalogue[a] & catalogue[b]).bit_count()
                      for b in labels]
            best = [b for b in labels if values[b] == max(values)]
            replies.append(best)
            floor.append(min(2 * catalogue[a].bit_count() - (catalogue[a] & catalogue[b]).bit_count()
                             for b in best))
        for a in labels:
            for b in replies[a]:
                first = 2 * catalogue[a].bit_count() - (catalogue[a] & catalogue[b]).bit_count()
                if first < max(floor):
                    continue
                paths += 1
                actual = catalogue[a] | catalogue[b]
                w = actual.bit_count()
                for i, j in pairs:
                    comparisons += 1
                    r = ((catalogue[i] | catalogue[j]) & ~actual).bit_count()
                    if 9*r > 5*w:
                        assert b not in (i, j)
                        high_residual += 1
                    if b in (i, j):
                        continue
                    g = pair_cover[i, j] - max(value for pair, value in pair_cover.items()
                                               if pair != (i, j))
                    assert 22*g + 13*r <= 14*w, (catalogue, a, b, i, j)
                    applicable += 1
    print('general catalogues, attainable paths, all comparisons, valid bound, high residual',
          len(catalogues), paths, comparisons, applicable, high_residual)


def check_included_terminal_endpoint():
    a, b, c = set(range(4)), set(range(4, 9)), set(range(9, 14))
    p, q = {0, 1, 4, 5, 9, 10}, {0, 1, 4, 5, 11, 12}
    catalogue = (a, b, c, p, q)
    response = (1, 3, 3, 4, 3)

    def doubled_profit(theme, other):
        return 2 * len(theme) - len(theme & other)

    for i, j in enumerate(response):
        assert doubled_profit(catalogue[i], catalogue[j]) == 8
        assert doubled_profit(catalogue[j], catalogue[i]) == max(
            doubled_profit(theme, catalogue[i]) for theme in catalogue
        )
    pairs = {(i, j): len(catalogue[i] | catalogue[j])
             for i, j in combinations_with_replacement(range(5), 2)}
    assert [pair for pair, size in pairs.items() if size == max(pairs.values())] == [(1, 2)]
    assert len(a | b) == 9 and len((b | c) - (a | b)) == 5
    print('included terminal sharp endpoint: 30 incentive and 15 pair rows')


if __name__ == '__main__':
    check_mixtures()
    check_included_terminal_endpoint()
    check_general_catalogues()
