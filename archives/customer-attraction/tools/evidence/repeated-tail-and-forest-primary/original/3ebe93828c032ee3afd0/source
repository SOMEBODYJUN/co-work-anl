"""Definition-level audit of two terminal histories, not a full-SPE sampler.

The universal obstruction is proved algebraically in the adjacent note.
This file expands different unit customers and checks the displayed formulas.
"""
from fractions import Fraction
from itertools import product
import json


def utility(topics, path, player):
    selected = topics[path[player]]
    return sum((Fraction(1, sum(x in topics[a] for a in path)) for x in selected), Fraction())


def make_topics(k, c, a, b, d):
    cursor = 0

    def block(size):
        nonlocal cursor
        result = set(range(cursor, cursor + size))
        cursor += size
        return result

    x = [block(c) for _ in range(k)]
    p = [block(a) for _ in range(k)]
    z, e = block(b), block(d)
    topics = {f'C{i}': x[i] for i in range(k)}
    topics.update({f'A{i}': x[i] | p[i] for i in range(k)})
    topics.update({f'B{i}': x[i] | z for i in range(k)})
    topics['D'] = z | e
    return topics


def main():
    checks = 0
    feasible_r = set()
    for k, r, c, a, b, d in product((1, 2, 4), range(1, 7), (1, 2, 3),
                                  (0, 1, 4), (0, 1, 5), range(8)):
        topics = make_topics(k, c, a, b, d)
        actual = [f'C{i}' for i in range(k)] + ['D'] * r
        actual_alt = actual[:-1] + ['B0']
        deviation = ['A0'] + [f'C{i}' for i in range(1, k)] + ['B0'] * r
        deviation_alt = deviation[:-1] + ['D']
        v = tuple(utility(topics, path, len(path) - 1)
                  for path in (actual, actual_alt, deviation, deviation_alt))
        expected = (Fraction(b + d, r), Fraction(c, 2) + Fraction(b, r),
                    Fraction(c, r + 1) + Fraction(b, r), Fraction(b, r) + d)
        assert v == expected, (k, r, c, a, b, d, v, expected)
        both_br = v[0] >= v[1] and v[2] >= v[3]
        assert both_br == (Fraction(r * c, 2) <= d <= Fraction(c, r + 1))
        if both_br:
            feasible_r.add(r)
            assert r == 1 and Fraction(d) == Fraction(c, 2)
        checks += 1
    print(json.dumps({'unit_customer_two_terminal_history_checks': checks,
                      'tail_lengths_passing_both_necessary_comparisons': sorted(feasible_r),
                      'full_SPE_search': False,
                      'universal_claim_depends_on_symbolic_proof': True}, indent=2))


if __name__ == '__main__':
    main()
