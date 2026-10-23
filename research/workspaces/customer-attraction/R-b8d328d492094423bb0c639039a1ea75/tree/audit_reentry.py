"""Exact replay of the non-SPE bank tree in bank_reentry_identity.md."""
from fractions import Fraction as F
from itertools import product
import json


def run(q):
    m = 2 * q
    bits = [1, 0] * (q - 1) + [1, 1]

    def sigma(history):
        main = [a for a, b in history]
        if 0 not in main:
            bank = bits[len(history)]
        else:
            first_zero = main.index(0) + 1
            bank = int(first_zero % 2 == 0 and first_zero < m)
        return (0, bank)

    def finish(prefix):
        h = list(prefix)
        while len(h) < m:
            h.append(sigma(h))
        return h

    prefix = []
    leaves = [finish(prefix)]
    for i in range(m):
        current = sigma(prefix)
        assert current[1] == bits[i]
        prefix.append((1, current[1]))
        leaves.append(finish(prefix))
    loads = [sum(b for a, b in leaf) for leaf in leaves]
    delta = [F(bits[i], loads[i]) - F(bits[i], loads[i + 1]) for i in range(m)]
    entry_exit = F(bits[0], loads[0]) - F(bits[-1], loads[-1])
    for i in range(m - 1):
        if bits[i + 1] != bits[i]:
            entry_exit += F(bits[i + 1] - bits[i], loads[i + 1])
    formula = sum((F(1, r) for r in range(1, q + 1)), F())
    formula -= sum((F(1, 2 * q - r) for r in range(1, q)), F())
    formula -= F(1, q + 1)
    assert sum(delta) == entry_exit == formula
    assert all(x >= 0 for x in delta)
    return {"q": q, "m": m, "bits": bits, "loads": loads,
            "delta": list(map(str, delta)), "total": str(formula),
            "root_bank_welfare": 1, "is_spe_certified": False}


def exhaustive(m):
    checked = 0
    # Compatible adjacent continuation loads suffice for the algebraic bound.
    for bits in product((0, 1), repeat=m):
        prefix = [sum(bits[:i]) for i in range(m + 1)]
        choices = []
        for i in range(m + 1):
            if i == 0:
                lo, hi = bits[0], bits[0] + m - 1
            elif i == m:
                lo = hi = prefix[-1]
            else:
                lo = prefix[i] + bits[i]
                hi = lo + m - i - 1
            choices.append(range(lo, hi + 1))
        for loads in product(*choices):
            value = sum((F(1, loads[i]) - F(1, loads[i + 1])
                         for i in range(m) if bits[i]), F())
            k = sum(bits[i] and (i == 0 or not bits[i - 1]) for i in range(m))
            assert value <= sum((F(1, r) for r in range(1, k + 1)), F())
            checked += 1
    return checked


if __name__ == "__main__":
    print(json.dumps({
        "status": "algebra/replay only; explicit trees are not SPE certified",
        "families": [run(q) for q in (1, 2, 3, 5, 10, 50)],
        "exhaustive_adjacent_load_cases": {str(m): exhaustive(m) for m in range(1, 6)},
    }, indent=2))
