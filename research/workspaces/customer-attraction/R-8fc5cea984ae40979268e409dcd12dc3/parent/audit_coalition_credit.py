"""Exact load arithmetic, not an SPE search or a general half proof."""
from fractions import Fraction as F
import json


def credit(p, c, a, d0, d):
    return p * max(F(0), F(1, c) - F(1, d0)) + a * (F(1, d0) - F(1, d))


def main():
    tuples = groups = 0
    maxima = []
    for m in range(1, 13):
        best_m = F(0)
        for a in range(1, m + 1):
            best = F(0)
            for c in range(1, m + 1):
                for p in range(min(c, m - a) + 1):
                    for d in range(p + a, m + 1):
                        endpoints = max(credit(p, c, a, p + a, d), credit(p, c, a, d, d))
                        actual = max(credit(p, c, a, d0, d) for d0 in range(p + a, d + 1))
                        assert actual == endpoints, (m, p, c, a, d)
                        groups += 1
                        tuples += d - p - a + 1
                        best = max(best, actual)
            expected = 2 * F(a, a + 1) - F(a, m) if a < m else F(0)
            assert best == expected, (m, a, best, expected)
            if a < m:
                assert credit(1, 1, a, a + 1, m) == expected
            best_m = max(best_m, best)
        maxima.append({"m": m, "max_credit": str(best_m)})
    witness = credit(1, 1, 3, 4, 7)
    assert witness == F(15, 14)
    assert all(F(row["max_credit"]) <= 1 for row in maxima if row["m"] <= 6)
    assert next(row["m"] for row in maxima if F(row["max_credit"]) > 1) == 7
    # The exact subsequence is 2 - 3/(a+1) + 1/(a+1)^2.
    for a in (1, 2, 3, 10, 100, 1000):
        m = (a + 1) ** 2
        val = credit(1, 1, a, a + 1, m)
        assert val == 2 - F(3, a + 1) + F(1, (a + 1) ** 2)
    print(json.dumps({"status": "passed", "scope": "integer load algebra only; no SPE certification", "fixed_parameter_groups": groups, "load_tuples": tuples, "maxima": maxima, "witness": str(witness)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
